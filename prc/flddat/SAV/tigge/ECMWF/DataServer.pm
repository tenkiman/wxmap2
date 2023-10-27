package ECMWF::DataServer;
use LWP::UserAgent;
use HTTP::Request;
use Data::Dumper;

my $VERSION = 0.3;

sub new {
	my ($class,@args) = @_;
	my $self = {@args};

	return bless($self,$class);
}

sub _call {
	my ($self,$action,@args) = @_;

	my $ua  = LWP::UserAgent->new( agent => "ecmwf-dataserver-client-$VERSION", keep_alive => 1, env_proxy => 1, timeout => 60);
	my $req = HTTP::Request->new(POST => $self->{portal});

	$req->header("Content-Type" => "application/x-www-form-urlencoded");

	my %args = (
			_token   => $self->{token},
			_email   => $self->{email},
			_action  => $action,
			_version => $VERSION,
			@args
			);

	$req->content(join("&",map { "$_=$args{$_}" } keys %args));

	my $res = $ua->request($req);

	die $res->status_line if($res->is_error);

	my $json = $res->content;
	$json =~ s/ : / => /gs;


	my $result =  eval "$json";

#	print Dumper($result);

	die $result->{error} if($result->{error});
	put($result->{message}) if($result->{message});

	return $result;
}

sub retrieve {
	my ($self,@args) = @_;

	put("ECMWF data server batch tool version $VERSION");
	my $user =  $self->_call("user_info");
	put("Welcome to ",$user->{name}, " from " , $user->{organisation});
	my $r   = $self->_call("retrieve",@args);
	my $rid = $r->{request};

	my $last   = "";
	my $sleep = 0;

	while(!($r->{status}  =~ /abort|complete/))
	{
		
		my $text = "$r->{status}. $r->{info}";
		
		put("Request $text") if($text ne $last);
		$last = $text;

		sleep($sleep);

		$r = $self->_call("status", request => $rid);

		$sleep++ if($sleep < 60);
	}


	my %args = @args;
	put("Request $r->{status}.") if($r->{status} ne $last);

	if(exists $r->{reason})
	{
		foreach my $m (@{$r->{reason}})
		{
			put($m);
		}
	}

	if(exists $r->{result})
	{
		put("Downloading ",bytename($r->{size}));
		my $size = $self->_transfer($r->{result},$args{target}) ;
		die "Counld not download all data" unless($r->{size} ==  $size);
	}

	$r = $self->_call("delete", request => $rid);

	die "Request aborted" if($r->{status}  =~ /abort/);

}

sub _transfer {
	my ($self,$url,$target) = @_;

	my $ua = LWP::UserAgent->new( agent => "ecmwf-dataserver-client", keep_alive => 1, env_proxy => 1, timeout => 60);

	put("Transfer from $url to $target");

	open(OUT,">$target") or die "$target: $!";

	my $response = $ua->request(HTTP::Request->new(GET => $url),sub {
			my $content = shift;
			syswrite(OUT,$content) or die "$target: $!";
			});

	close(OUT) or die "$target: $!";

	die $response->status_line if($response->is_error);
	put("Done");
	return $response->content_length;

}


sub nextbytes
{   
	my ($letter) = @_;
	return "P" if ($letter eq "T");
	return "T" if ($letter eq "G");
	return "G" if ($letter eq "M");
	return "M" if ($letter eq "K");
	return "K" if ($letter eq "b");
	die "Cannot continue with $letter bytes\n";
}   

# Transforms number of bytes onto a divisor of 1024 with proper prefix
sub bytename
{
	my ($n) = @_;
	my $l = "b";    
	while(1024 < $n)
	{
		$l = nextbytes($l);
		$n /= 1024;
	}
	$n = sprintf("%g",$n);
	$l = "" if($l eq "b");
	return "$n ${l}bytes";
}


sub put {
	my (@args) = @_;
	my ($sec,$min,$hour,$day,$mon,$year) = localtime;
	my $time = sprintf("%04d-%02d-%02d %02d:%02d:%02d", $year+1900, $mon+1, $day, $hour, $min, $sec);
	print $time," ", @args, "\n";
}

1;


