#!/usr/bin/env perl

require("mf.pl");
use CGI(header,param);

$verb=0;

$bdir="/wxmap2/dat/tc/tcanal";
$xszs=700;
$yszs=$xszs*(3/4);
$cgibdir="/wxmap2/cgi-bin/wxmap2";

#
# cgi input parms
#

$tdtg = &FilterNeg(param('dtg'));
$tstorm = &FilterNeg(param('storm'));
$tmodel = &FilterNeg(param('model'));
$ttau = &FilterNeg(param('tau'));
$ptype = &FilterNeg(param('ptype'));


#
# always use lower case in storm
#
$tstorm=lc($tstorm);

$inputopts="$tdtg $tstorm $tmodel $ttau $ptype";

$dbdir="/data/www/html/mfiorino/wxmap2/dat/tc/tcanal";
$dbmask="tc.db.*.txt";

$modeltitle=uc($tmodel);
$pagetitle="WxMAP TC Structure Analysis of <b>$modeltitle</b> model";
$stormtitle=uc($tstorm);

#
# returns current dtg if $tdtg = '' or 'cur'
#

TcstructDb();

if($tstorm eq '' && $tmodel eq '' && $ttau eq '') {
    $tmodel=$models[0];
    $tstorm=$stms[0];
    @taus=split(' ',$modeltaus{$tmodel,$tstorm});
    $ttau=$taus[0];
}

@taumods=split(' ',$taumodels{$ttau,$tstorm});

$taumodtest=$tmodel;

foreach $taumod (@taumods) {
    if($taumodtest eq $taumod) {
	$taumodtest=1;
	@models=@taumods;
    }
}

if(!($taumodtest)) {
    $tmodel=@taumods[0];
    @models=@taumods;
}

if($tmodel eq 'undef' && $ttau ne 'undef') {
    @models=split(' ',$taumodels{$ttau,$tstorm});
    $tmodel=$models[0];
}

if($tmodel eq 'undef' && $ttau eq 'undef') {
    $tmodel=$models[0];
}

if($ttau eq 'undef') {
    @taus=split(' ',$modeltaus{$tmodel,$tstorm});
    $ttau=$taus[0];
}

$toptitle="WxMAP TC Structure Analysis :: $tdtg";

$yyyy=substr($tdtg,0,4);

$inputfinal="$tdtg $tstorm $tmodel $ttau $ptype";
print header();

$htmlhead="

<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">
<html>
<head>
<title>
$toptitle
</title>
<link rel=\"stylesheet\" href=\"/wxmap2/css/tcstruct.css\" type=\"text/css\">
</head>
<body>
<!--
<p class=\"plttitle\" align=center>
$pagetitle<br>
<font color=red font face=\"Comic sans MS, arial\">$stormtitle :: $tdtg</font>
</p>
-->
<center>
";

$htmltest="

<p>
$inputopts
</p>
<p>
$inputfinal
</p>

";

foreach $card (@cards) {
    $htmltest="$htmltest
$card";

}

#111111111111111111111111111111111111111111111
#
# first table menu
#
#111111111111111111111111111111111111111111111

$menutable1="
<table class=clear>
<tr>
<td class=\"med\">
<table bgcolor=\"#AAAAAA\">
<tr>

<td class=\"med\">
<a href=\"/wxmap2/wx.$tdtg.htm\">
<b><i>WxMAP2 HOME</i></b>
</a>
</td>

";

foreach $dtg (@dtgs) {

    $menutable1="
$menutable1
<td class=\"med\">
<a href=\"$cgibdir/tcstruct.cgi?dtg=$dtg&storm=$tstorm&tau=undef&model=undef\">
$dtg
</a>
</td>
";  

}

    $menutable1="
$menutable1
</tr>
</table>
<td class=\"med\">
<table bgcolor=\"#AAAAAA\">
<tr>

";



foreach $stm (@stms) {

    $ucstm=uc($stm);
    $menutable1="
$menutable1
<td class=\"med\">
<a href=\"$cgibdir/tcstruct.cgi?dtg=$tdtg&storm=$stm&tau=undef&model=undef\">
$ucstm
</a>
</td>
";  

}

$menutable1="
$menutable1
</tr>
</table>

</tr>
</table>
";

$maintable="
";


$modeltable="

<table class=\"tform\" bgcolor=\"#AAAAAA\">
<tr bgcolor=\"white\">
";

foreach $model (@models) {
    $umodel=uc($model);
    $modeltable="$modeltable
<td class=\"big\" align=center>
<a href=\"$cgibdir/tcstruct.cgi?dtg=${tdtg}&storm=${tstorm}&model=$model&tau=${ttau}&ptype=$ptype\">
$umodel
</a>
</td>
";

}

$modeltable="$modeltable
</td>
</tr>
</table>
";



#----------------------------------------------------------------------
#
# tau table above 2-d plot
#
#----------------------------------------------------------------------

$menutable2="
<table bgcolor=\"#AAAAAA\">
<tr bgcolor=\"white\">
";


foreach $model (@models) {
    $umodel=uc($model);
    $menutable2="$menutable2
<td class=\"big\" align=center>
<a href=\"$cgibdir/tcstruct.cgi?dtg=${tdtg}&storm=${tstorm}&model=$model&tau=${ttau}&ptype=$ptype\">
$umodel
</a>
</td>
";

}

if($verb) {
    print "QQQ $tmodel\n";
    print "QQQ $tstorm\n";
    print "QQQ $modeltaus{$tmodel,$tstorm}\n";
}

@taus=split(' ',$modeltaus{$tmodel,$tstorm});

foreach $tau (@taus) {
    $menutable2="$menutable2
<td class=\"big\" align=center>
<a href=\"$cgibdir/tcstruct.cgi?dtg=${tdtg}&storm=${tstorm}&model=$tmodel&tau=${tau}\">
$tau
</a>
</td>
";

}


$menutable2="$menutable2
<td class=\"big\" align=center>
<a href=\"$cgibdir/tcstruct.cgi?dtg=${tdtg}&storm=${tstorm}&model=$tmodel&tau=${tau}&ptype=animate\">
animate
</a>
</td>
<td class=\"big\" align=center>
<a href=\"$cgibdir/tcstruct.cgi?dtg=${tdtg}&storm=${tstorm}&model=$tmodel&tau=${tau}&ptype=profile\">
profile
</a>
</td>
</tr>
</table>
";

$lctmodel=lc($tmodel);

$plthtml="
";

if($ptype eq 'animate') {
    $pltfile="$bdir/$yyyy/$tdtg/plt/animate.$lctmodel.$tstorm.$tdtg.gif";
    $ttau='000';
} elsif($ptype eq 'profile') {
   $pltfile="$bdir/$yyyy/$tdtg/plt/profile.$lctmodel.$tstorm.$tdtg.png";
    $ttau='000';
} else {
    $pltfile="$bdir/$yyyy/$tdtg/plt/plt.$lctmodel.$tstorm.$ttau.png";
}

$pltfile="<img src=\"$pltfile\" width=$xszs height=$yszs border=0>";

$plthtml="
$plthtml
$pltfile
";

$maintail="
</table>
</center>
</body>
</html>
";

$html="

$htmlhead

<!--
$htmltest
-->

$menutable1

$menutable2

<table border=1>

<tr>
<td align=center>
$plthtml
</td>
</tr>

$maintail

";

print $html;


sub FilterNeg {
# This function removes Dangerous Tags from various fields
	local ($fd)=@_;
	$fd=~s/[\<\>\"\'\%\;\&\+\|]//g;
	return ($fd);
}


sub TcstructDb {

    my($verb);
    $verb=0;

    $ndtgs=6;
    @dtgdbs=`(cd $dbdir ; ls -r $dbmask | head -$ndtgs)`;

    foreach $dtgdb (@dtgdbs) {
	@tt=split('\.',$dtgdb);
	$dtg=$tt[2];
	push @dtgs,$dtg;
    }
    
    if($tdtg eq 'undef' || $tdtg eq '' || $tdtg eq 'cur') {
	$tdtg=$dtgs[0];
    }

    $dbpath="$dbdir/tc.db.$tdtg.txt";

    open(DB,$dbpath) || die "unable to open $dbpath";

    @cards=<DB>;
    $ntc=$#cards + 1;

    %modeltaus={};

    foreach $card (@cards) {
	@tt=split(' ',$card);

	if($verb) {
	    print "CCC $card";
	    print "CC11 $tt[0] $#tt\n";
	}

	$stm=$tt[0];
	$stm=$stm;
	$rlat=$tt[1];
	$rlon=$tt[2];
	$vmax=$tt[3];
	$rmax=$tt[4];
	$r34=$tt[5];

	for ($i=6;$i<=$#tt;$i++) {
	    @ttt=split('\.',$tt[$i]);
	    $model=$ttt[0];
	    $tau=$ttt[1];
	    push @models,$model;
	    if($verb) {
		print "CC22 $tt[$i] $ttt[0]\n";
	    }
	    $modeltaus{$model,$stm}="$modeltaus{$model,$stm} $tau";
	    $taumodels{$tau,$stm}="$taumodels{$tau,$stm} $model";

	}

	push @stms,$stm;

    }

    @models=uniq(@models);

    if($verb) {
	foreach $model (@models) {
	    foreach $stm (@stms) {
		print "MMM $model :: $stm :: $modeltaus{$model,$stm}\n";
	    }
	}
    }


}
