#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};
require("$perldir/mf.pl");
require("$perldir/wxmap.env.pl");
wxmap_env();

$narg=$#ARGV+1;

$prodcenter=$WXMAP{"WXMAP_PROD_CENTER"};
$basewxmaphref=$WXMAP{"WXMAP_HTML_BASE_HREF"};
$basewxmap=$WXMAP{"WXMAP_HTML_BASE"};
$basewxmapdoc=$WXMAP{"WXMAP_HTML_BASE_DOC"};
$baseicon=$WXMAP{"WXMAP_HTML_BASE_ICON"};
$basewxmaptop=$WXMAP{"WXMAP_HTML_BASE_TOP"};
$basewxmapdoctop=$WXMAP{"WXMAP_HTML_BASE_DOC_TOP"};
$baseicontop=$WXMAP{"WXMAP_HTML_BASE_ICON_TOP"};

$webdir=$WXMAP{"WXMAP_WEB_DIR"};
$webmast=wxmap_master();

$verb=1;
$update_current="n";
$lastmodification="26 June, 1997";

$update_current="n";
$timecdtg=dtg("time");
$curdtg=dtg();

$tdtg='cur';
$tdtg=$curdtg if($tdtg eq 'cur');

$data_time="archive/$tdtg";

chdir($webdir);

$afile="wxmap.web.archive.htm";

print "WWWAAARRRCCCHHHIIIVVVEEE $afile for $tdtg\n";

$doctitle="$prodcenter NWP Weather Maps -- Web Archive";

open(WA,">$afile") || die "unable open to $afile\n";

print WA <<"EOF";
<html>
<head>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-VG0RC3XML9\"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-VG0RC3XML9');
</script>


<link rel=\"shortcut icon\" href=\"favicon.ico\">
<title>$doctitle</title>
</head>
<body background="${baseicontop}wxmap.bkg.2.gif" TEXT="#000000" LINK="#0000FF" VLINK="#006030">


<h1>$prodcenter WXMAP Web Archive</h1>
<img src="${baseicontop}colaline.gif">
<p>

A "web" is a set of maps/html documents created for a specific
model integration.  The integrations used to make the maps at
this site are run every 24 hours, hence one web is created each
day (if things are working well).  Use this page to go to a
particular integration.  The archive extends back 10 days from
the current time.  This limitation is for disk conservation.
However, the maps and web can be regenerated from archived data.

</p>

<p>

Also note that by using the <b>previous/next</b> and then the
<b>model home</b> <a href=\"${basewxmapdoctop}wxhelp.htm#wxmap
buttons\">buttons</a> you can move between integrations.

</p>

<table border=1>
<caption>Access a Previous Web by Clicking on its <a href=\"${basewxmapdoctop}what.is.a.dtg.htm\">DTG</a></caption>
<tr>
<th width=100 align=center><a href=\"${basewxmapdoctop}what.is.a.dtg.htm\">DTG</a></th>
<th width=300 align=center>Base time of the Model Runs</th>
</tr>
EOF

open(INPUT,"ls -r wx.[1,2][0-9][0-9][0-9]??????.htm |  ") || die "Can't list directory $ddir\n" ;

$index=0 ;		       
while ( <INPUT> ) {
    chop ;
    $file = $_ ;
    $tfile = $ddir . "/" . $_ ;
    ($f1,$dtg)=split(/\./, $file);

    if($dtg ne $tdtg) {

      $watchtime=dtg2time($dtg);

print WA<<"EOF";
<tr>
<td width=100 align=center><a href=\"${basewxmaptop}wx.$dtg.htm\">$dtg</a></td>
<td width=300 align=center>$watchtime</td>
</tr>
EOF

    } else {

      $watchtime=dtg2time($dtg);
print WA<<"EOF";
<tr>
<td width=100 align=center><a href=\"${basewxmaptop}wx.htm\">
<font color=red><b><i>CURRENT</i></b></a></font></td>
<td width=300 align=center><font color=red><b>$watchtime</b></font></td>
</tr>
EOF


    } 

  }

     close(INPUT);

print WA<<"EOF";
</table>
<br><br>
$webmast
</body>
</html>
EOF

close(WA);
exit;
