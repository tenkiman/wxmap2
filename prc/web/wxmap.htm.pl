#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};
require("$perldir/mf.pl");
require("$perldir/wxmap.env.pl");
wxmap_env();

$verb=0;


$prodcenter=$WXMAP{"WXMAP_PROD_CENTER"};

$basewxmap=$WXMAP{"WXMAP_HTML_BASE"};
$basewxmapdoc=$WXMAP{"WXMAP_HTML_BASE_DOC"};
$baseicon=$WXMAP{"WXMAP_HTML_BASE_ICON"};

$basewxmaptop=$WXMAP{"WXMAP_HTML_BASE_TOP"};
$basewxmapdoctop=$WXMAP{"WXMAP_HTML_BASE_DOC_TOP"};
$baseicontop=$WXMAP{"WXMAP_HTML_BASE_ICON_TOP"};

$webdir=$WXMAP{"WXMAP_WEB_DIR"};
$webmast=wxmap_master() ;

$dbdir="/wxmap_old/dat2/tc/tcstruct";
$dbdir=$WXMAP{'WXMAP_TC_STRUCT_DAT_DIR'};

$xsize=$WXMAP{'WXMAP_PLOT_XSIZE'};

$dogsm=1;

$narg=$#ARGV+1;

$curdtg=dtg();
$curdtg=dtg6();
$tmodel='None';

$InteractiveProductButtons=0;
$InteractiveTauButtons=0;
$doocnhtml=0;

$i=0;
if($narg >= 2 ) {

  $tdtg=dtg_command_prc($ARGV[$i]) if($narg >$i); $i++;
  $area=$ARGV[$i] if($narg >$i); $i++;
  $tmodel=$ARGV[$i] if($narg >$i); $i++;

} else {
  print "\n$0 arguments:\n\n";
  print "The current dtg: $curdtg\n\n";
  print "   tdtg  : YYYYmmddhh | curNNN\n";
  print "   area  : ";
  foreach $a (@areas) {
    print "$a | ";
  }

  print "  tmodel : individual model\n";
  print"\n\n";
  exit;
}


plot_taus2($tmodel);

if($area eq 'all') {

    foreach $area (@areas) {
	$cmd="wxmap.htm.pl $tdtg $area";
	print "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC: $cmd\n";
	system($cmd);
    }
    
    exit;

}

chomp($tmodel);

#
# parse TC struct db cards for storms
#

(%stmareas)=TcstructDb($tdtg);
@carqstms=keys(%stmareas);
foreach $carqstm (@carqstms) {
    $areas=$stmareas{$carqstm};
###    print "AAAAAAA $carqstm $areas\n";
}

($ntc,$tcareas)=tc_bt_posits();

$atype=$area_type{$area};
#
# -- check if a valid type
#
$aiok=0;
foreach $aaa (@plot_type) {
  $aiok=1 if($atype eq $aaa);
}
if($aiok == 0) {
  print "EEEE $0: invalid area type: $atype\n";
  print "EEEE $0: komarimashita ne!! ja sayoonara\n";
  exit(88);
}

# -- model run check
#
$tdtghh=substr($tdtg,8,2);
#$model_run{$model,$tdtghh}
#
# -- model run check

$tdtgm6=dtg4inc($tdtg,-6);
$tdtgm12=dtg4inc($tdtg,-12);
$tdtgm24=dtg4inc($tdtg,-24);
$tdtgm36=dtg4inc($tdtg,-36);
$tdtgm48=dtg4inc($tdtg,-48);
$tdtgm60=dtg4inc($tdtg,-60);
$tdtgm72=dtg4inc($tdtg,-72);
$tdtgm96=dtg4inc($tdtg,-96);
$tdtgm120=dtg4inc($tdtg,-120);

$tdtgp6=dtg4inc($tdtg,+6);
$tdtgp12=dtg4inc($tdtg,+12);
$tdtgp24=dtg4inc($tdtg,+24);
$tdtgp36=dtg4inc($tdtg,+36);
$tdtgp48=dtg4inc($tdtg,+48);
$tdtgp60=dtg4inc($tdtg,+60);
$tdtgp72=dtg4inc($tdtg,+72);
$tdtgp96=dtg4inc($tdtg,+96);
$tdtgp120=dtg4inc($tdtg,+120);

$data_time="$tdtg";
$timecdtg=dtg("time");
$curhh=substr($tdtg,8,2);


##################################################
#
#  set up url and html properties (e.g., with tables, buttons)
#
##################################################

set_url();
set_html_prop();

##################################################
#
# create a data base with model graphics file for the target dtg
#
##################################################

@hmodels=mod_db_run($curhh);


if($tmodel ne 'None') {
    foreach $hmodel (@hmodels) {
	if($tmodel eq $hmodel) {
	    push(@nhmodels,$tmodel);
	    @hmodels=@nhmodels;
	}
    }
}


if($dogsm) {
    if( ($curhh eq '00' || $curhh eq '12') && ($area eq 'tropwpac')) {
	push(@hmodels,'gsm');
    }
}

mod_db_plot();

if($ng{'all'} == 0) {
  print"\nThere are no maps to make html for $tdtg\n";
  exit;
}

set_sst_html();

##################################################
#
# create the main page
#
##################################################

chdir($webdir);

wxmap_home();

$wxdtg='.';
$wxdtg=".$tdtg." if($doregen);

##################################################
#
#   main loop for creating the model home pages
#
##################################################

#
#  make list of only models run at this hour
#


foreach $model (@hmodels) {

plot_taus2($model);

if($ng{$model} != 0) {

$homefile="${model}.$area.$tdtg.htm";
$center=$model_center{$model};
$hfileheaddir="$webdir/web_$model/$tdtg";
$hfilehead="$webdir/";

if ( ! (-d $hfileheaddir) ) {
    print "MMMMMMMMMMaking $hfileheaddir in $webdir\n";
    system("mkdir -p $hfileheaddir");
}


print "III wxmap.htm.pl: working on $model for: $tdtg :: $ng{$model}\n";

open(WX,">$homefile") || die "unable to open homefile: $homefile\n";

$doctitle="$prodcenter $model_desc{$model} Weather Maps -- $area_desc{$area}";
$center=$model_center{$model};
$praccum=$model_praccum{$model};

@t=split(/ /,$plot_type_taus{$atype});
$tauincrun=$model_tauinc_run{$model};

if($t[0] eq "default") {
  $taubeg=0;
  $tauend=$model_ntau{$model};
  $tauinc=$model_tauinc{$model};
} else {
  $taubeg=$t[0];
  $tauend=$t[1];
  $tauinc=$t[2];
}

$ntau=$tauend;
$ntau=$plottaus[$#plottaus];


@maptype=split(' ',$plot_type_plots{$atype});
$maptitle{'prp'}="Previous $praccum-h Precip Rate [mm/day] and SLP [hPa]";
$shortmaptitle{'prp'}="slp / precip $praccum-hr [mm/d]";


$modelbkg=$model_bkg{$model};

print WX <<"EOF";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
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
<link rel=\"stylesheet\" type=\"text/css\" href=\"css/wxmain.css\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"css/dropdown.css\">

<title>$doctitle</title>

<style type=\"text/css\">
table {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size :9pt;
	font-style : normal;
	font-weight : normal;
	vertical-align : middle;
/*background-color: gold*/
}
</style>



</head>

<body background="${baseicontop}${modelbkg}" TEXT="#000000" LINK="#0000FF" VLINK="#006030">

<script language=\"javascript\" src=\"js/wxmain.js\" type=\"text/javascript\"></script>

<h2><font face="arial"><i>$prodcenter NWP Weather Maps</i></font><br>
<font face="arial"color=red>$model_desc{$model} Home Page for $dtg{$model}</font><br>
<font face="arial"color=blue><i>$area_desc{$area}</i></font></h2>
EOF

#
# the table
#

print WX <<"header";
<table border=1 cellpadding=0 cellspacing=0>
<caption align=center>
</caption>
<tr>
<td align=right colspan=3>Forecast Time [h]</td>
header

####for ($i=0;$i<=$ntau;$i+=$tauinc) {
for ($i=0;$i<=$#plottaus;$i++) {
    $itau=$plottaus[$i];
    print WX "<th width=$width{'tau'} align=center >$itau</th>\n";
}

print WX "<td width=$width{'tau'} align=center >&nbsp<td></tr>\n";

#
#   row 2
#

print WX <<"header";
<tr>
<th width=$width{'maptitle'} align=center > Weather Map</th>
<th width=$width{'mapname'} align=center>Name</th>
<td width=$width{'tau'} align=center>All &tau;</td>
header

###for ($i=0;$i<=$ntau;$i+=$tauinc) {
for ($i=0;$i<=$#plottaus;$i++) {
    $itau=$plottaus[$i];

  if($itau<10) {
    $tau="00$i";
  } elsif($itau<100) {
    $tau="0$itau";
  } else { 
    $tau=$itau;
  } 

  print WX "<td width=$width{'tau'} align=center >\n";
  $urlamfile="${basewxmaptop}web_$model/$data_time/${model}.allmap.${tau}.$area.htm";
  print WX "<a href=\"$urlamfile\"><img src=\"${baseicontop}all.maps.button.gif\" ALT=\"All Maps\" img border=\"0\"></a></th>\n";
}

print WX "<th width=$width{'movie'} align=left>Loop</th></tr>\n";



foreach $m (plot_types($model)) {


  $mt=$maptitle{$m};
  $atfile="$webdir/web_$model/$tdtg/$model.alltau.${m}.$area.htm";

  open(AT,">$atfile") || die "unable to open atfile: $atfile\n";

print AT <<"EOF";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
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
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/wxmain.css\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/dropdown.css\">


<title>All Taus $model_desc{$model}</title>
</head>
<br><b>$model_desc{$model} <font color=red><i>$tdtg</font></i> $mt maps for
<font color=blue>All Times</font> </b><br>
<body>


Click on the map to return to that individual map<br>
EOF

  print WX "<td width=$width{'maptitle'} align=right> $mt </td> \n";
  print WX "<td width=$width{'mapname'} align=center><b>$m</b></td>\n";
  print WX "<td width=$width{'tau'} align=center>\n";

  $urlatfile="${basewxmaptop}web_$model/$tdtg/${model}.alltau.$m.$area.htm";
  print WX "<a href=\"$urlatfile\"><img src=\"${baseicontop}all.times.button.gif\" ALT=\"All Times\" img border=\"0\"></a></td>\n";

###  for ($i=0;$i<=$ntau;$i+=$tauinc) {
for ($i=0;$i<=$#plottaus;$i++) {
    $itau=$plottaus[$i];
  
    $tau=sprintf("%03d",$itau);

    $amfile="$webdir/web_$model/$tdtg/${model}.allmap.${tau}.$area.htm";
    open(AM,">${amfile}") || die "unable to amfile: $amfile\n";

print AM <<"EOF";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
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
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/wxmain.css\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/dropdown.css\">

<title>All Maps for $model_desc{$model} t= ${itau} h</title>
</head>
<body>
<b>$model_desc{$model} <font color=red><i>$tdtg</font></i> <font color=blue>All Maps</font></b><br>


</body>
Click on the map to return to that individual map<br>
EOF

$gfile="${model_grf_name{$model}}${model_grf_ext{$model}}.$m.$tau.$area.png";

  $there=$gfile_truth{$gfile};
###  print "qqq-------------- $m $model $mt $i $ntau $mm $gfile ... there: $there\n";

  if($there ne 1) {
      $there=0;
  }

    if( !$there  ) {

	print WX "
<td>
<input type='button' class='btnmediietau'
onMouseOver=\"className='btnmediietauover';\"
onMouseOut=\"className='btnmediietau';\"
value='${tau}' name=taub
onClick=\"value='$urlhfile';opentype='',swaphtm();\">
</td>";


    } else {

      $gfile="${model_grf_name{$model}}${model_grf_ext{$model}}.$m.${tau}.$area.png";
      $hfile="${hfileheaddir}/${model}.$m.${tau}.$area.htm";
      $urlhfile="web_$model/$tdtg/${model}.$m.${tau}.$area.htm";


	print WX "
<td>
<input type='button' class='btnmedhaitau'
onMouseOver=\"className='btnmedhaitauover';\"
onMouseOut=\"className='btnmedhaitau';\"
value='${tau}' name=taub
onClick=\"cvalue='$urlhfile';opentype='page',swaphtm();\">
</td>";



##################################################
#
#  make the PLOT html
#
##################################################

open(WH,">$hfile") || die "unable to open hfile: $hfile\n";


if($area eq 'troplant') {
	  
    $obasin1='tropepac';
    $obasin2='tropwpac';
    $obasin3='conus';
    $obasin4='asia';

} elsif($area eq 'tropepac') {

    $obasin1='troplant';
    $obasin2='tropwpac';
    $obasin3='conus';
    $obasin4='asia';

} elsif($area eq 'tropwpac') {

    $obasin1='troplant';
    $obasin2='tropepac';
    $obasin3='conus';
    $obasin4='asia';

} elsif($area eq 'conus') {
    $obasin1='troplant';
    $obasin2='tropepac';
    $obasin3='tropwpac';
    $obasin4='asia';
	
# ------------------------------------------------------------- not run in wxmap2.com
} elsif($area eq 'tropswpac') {
    $obasin1='tropsio';
    $obasin2='tropoz';
    $obasin3='tropnio';
    $obasin4='tropepac';

} elsif($area eq 'tropnio') {
    $obasin1='tropwpac';
    $obasin2='tropsio';
    $obasin3='tropswpac';
    $obasin4='tropepac';

} elsif($area eq 'tropsio') {
    $obasin1='tropswpac';
    $obasin2='tropoz';
    $obasin3='tropnio';
    $obasin4='tropepac';

} elsif($area eq 'tropoz') {
    $obasin1='tropsio';
    $obasin2='tropswpac';
    $obasin3='tropwpac';
    $obasin4='tropepac';

} elsif($area eq 'wconus') {
    $obasin1='tropepac';
    $obasin2='conus';
    $obasin3='nhem';
    $obasin4='troplant';


} elsif($area eq 'nhem') {
    $obasin1='conus';
    $obasin2='wconus';
    $obasin3='troplant';
    $obasin4='tropepac';

} elsif($area eq 'europe') {
    $obasin1='conus';
    $obasin2='wconus';
    $obasin3='troplant';
    $obasin4='asia';

} elsif($area eq 'asia') {
    $obasin1='conus';
    $obasin2='tropepac';
    $obasin3='troplant';
    $obasin4='tropwpac';
}

$urlhfile1="${basewxmap}web_$model/$data_time/${model}.$m.${tau}.$obasin1.htm";
$urlhfile2="${basewxmap}web_$model/$data_time/${model}.$m.${tau}.$obasin2.htm";
$urlhfile3="${basewxmap}web_$model/$data_time/${model}.$m.${tau}.$obasin3.htm";
$urlhfile4="${basewxmap}web_$model/$data_time/${model}.$m.${tau}.$obasin4.htm";


$urlhfile="${basewxmap}web_$model/$data_time/${model}.$m.${tau}.$area.htm";
$urlgfile="${basewxmap}$model_http_gdir{$model}/$data_time/$gfile";

$web1="
<\!DOCTYPE HTML PUBLIC \"\-//W3C//DTD HTML 4.01 Transitional//EN\">
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
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/wxmain.css\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/dropdown.css\">

<title>$model_desc{$model} $dtg{$model} $itau h </title>

</head>
<body text=black link=blue vlink=purple bgcolor=#fcf1da onLoad=pswap()>

<script type=\"text/javascript\">

/***********************************************
* AnyLink Drop Down Menu- © Dynamic Drive (www.dynamicdrive.com)
* This notice MUST stay intact for legal use
* Visit http://www.dynamicdrive.com/ for full source code
***********************************************/

//Contents for menu 1
var menu1=new Array()

menu1[0]='<a href=\"$urlhfile1\">$obasin1</a>'
menu1[1]='<a href=\"$urlhfile2\">$obasin2</a>'
menu1[2]='<a href=\"$urlhfile3\">$obasin3</a>'
menu1[3]='<a href=\"$urlhfile4\">$obasin4</a>'

</script>


<script language=\"javascript\" src=\"../../js/dropdown.js\" type=\"text/javascript\"></script>
<script language=\"javascript\" src=\"../../js/wxmain.js\" type=\"text/javascript\"></script>

<script language=\"javascript\" type=\"text/javascript\">

model='${model}';
dtg='${data_time}';

parea='${area}';
ptype='${m}';
ptau='${tau}';
opentype='internal';
cvalue='None';


function pswap()
{

if(model == 'gfs') {
  plotdir='../../plt_ncep_gfs';
  modname='$model_grf_name{gfs}';
  modres='$model_grf_ext{gfs}';

} else if (model == 'fim') {
  plotdir='../../plt_esrl_fim';
  modname='$model_grf_name{fim}';
  modres='$model_grf_ext{fim}';

} else if (model == 'fv3e') {
  plotdir='../../plt_esrl_fv3e';
  modname='$model_grf_name{fv3e}';
  modres='$model_grf_ext{fv3e}';

} else if (model == 'fv3g') {
  plotdir='../../plt_esrl_fv3g';
  modname='$model_grf_name{fv3g}';
  modres='$model_grf_ext{fv3g}';

} else if (model == 'fimx') {
  plotdir='../../plt_esrl_fimx';
  modname='$model_grf_name{fimx}';
  modres='$model_grf_ext{fimx}';

} else if (model == 'ecmn') {
  plotdir='../../plt_ecmwf_ecm';
  modname='$model_grf_name{ecmn}';
  modres='$model_grf_ext{ecmn}';

} else if (model == 'ecmt') {
  plotdir='../../plt_ecmwf_ecmt';
  modname='$model_grf_name{ecmt}';
  modres='$model_grf_ext{ecmt}';

} else if (model == 'ecmg') {
  plotdir='../../plt_ecmwf_ecmg';
  modname='$model_grf_name{ecmg}';
  modres='$model_grf_ext{ecmg}';

} else if (model == 'ngp') {
  plotdir='../../plt_fnmoc_ngp';
  modname='$model_grf_name{ngp}';
  modres='$model_grf_ext{ngp}';

} else if (model == 'ngpc') {
  plotdir='../../plt_fnmoc_ngpc';
  modname='$model_grf_name{ngpc}';
  modres='$model_grf_ext{ngpc}';

} else if (model == 'navg') {
  plotdir='../../plt_fnmoc_navg';
  modname='$model_grf_name{navg}';
  modres='$model_grf_ext{navg}';

} else if (model == 'ukm') {
  plotdir='../../plt_ukmo_ukm';
  modname='$model_grf_name{ukm}';
  modres='$model_grf_ext{ukm}';

} else if (model == 'ecm') {
  plotdir='../../plt_ecmwf_ecm';
  modname='$model_grf_name{ecm}';
  modres='$model_grf_ext{ecm}';

} else if (model == 'gsm') {
  plotdir='../../plt_jma_gsm';
  modname='$model_grf_name{gsm}';
  modres='$model_grf_ext{gsm}';


} else if (model == 'cmc') {
  plotdir='../../plt_cmc_cmc';
  modname='$model_grf_name{cmc}';
  modres='$model_grf_ext{cmc}';

} else if (model == 'ocn') {
  plotdir='../../plt_fnmoc_ocn';
  modname='$model_grf_name{ocn}';
  modres='$model_grf_ext{ocn}';

}


//ukm10.uas.000.troplant.png
    if(opentype == 'external') {
	value=cvalue;
    } else {
	value=plotdir + '/' + dtg + '/' + modname + modres + '.' + ptype + '.' + ptau + '.' + parea + '.png';
    }

myUrl=value;
if (value != '') if (document.images) {
  document.images.myImage.src = value;
  document.images.myImage.alt = value;
  var el=document.images.myImage;
  while(el.nodeName.toLowerCase() != 'a') {
    el=el.parentNode;
    el.setAttribute('href',myUrl);
  }
//alert(value)
}

}

</script>


<table class='title'>
<tr><td width=900>
$model_desc{$model} <font color=red><i>$tdtg</font></i> <font color=blue>t = $itau h</font> forecast of $mt
</td>
</tr>
</table>

<table border=1 cellpadding=0 cellspacing=0>

<tr>
";


print WH $web1;

#---------- tau stepping -----------------


#---------- 1st row of mini buttons ---------------
#
#  other models
#  other plot
#
#--------------------------------------------------
print AT <<"EOF";
<br><b>$model_desc{$model} t = $itau h forecast </b><br>
<a href=\"$urlhfile\"><img src=\"$urlgfile\"></a>
EOF



# BBBBBBBBBBBBBBBBBBBBBBBBBBBB  333333333333333333333333333333333333333333333333333333333333333 -->
#-------------------- 3rd row ---------------------
# loop mode

      $urlmoviefile="${basewxmap}web_$model/$data_time/${model}.movie.${m}.$area.htm";
#########3      print WH "<td><a href=\"$urlmoviefile\"><img src=\"${baseicon}${model}.${m}.movie.gif\" alt=\"${m} movie\" img border=\"0\" ></a></td>\n";

$phpopt1="dtg=$tdtg&tau=$ttt000&area=$area&plot=${m}&model=${model}&veri=1&tau=${tau}";
$phpopt2="dtg=$tdtg&tau=$ttt000&area=$area&plot=${m}&model=${model}&veri=2&tau=${tau}";
$phphref1="../../w2animgif.php?$phpopt1";
$phphref2="../../w2animgif.php?$phpopt2";

print WH "
<td>
<input type='button' class='btn85'
onMouseOver=\"className='btn85over';\" onMouseOut=\"className='btn85';\"
value='Loop Taus' name=tctrk
onClick=\"cvalue=\'$urlmoviefile\';opentype='page',swaphtm();\">
</td>
";


#------------------- tau buttons ---------------------

###      for($ttt=$plot_tau{'beg'};$ttt<=$plot_tau{'end'};$ttt+=$plot_tau{'inc'}) {
for ($j=0;$j<=$#plottaus;$j++) {
    $ttt=$plottaus[$j]*1;

	$ttt000=sprintf("%03d",$ttt);
	$gfile="${model_grf_name{$model}}${model_grf_ext{$model}}.$m.$ttt000.$area.png";
	if($gfile_truth{$gfile}) {
	  $urltaufile="${basewxmap}web_$model/$data_time/${model}.${m}.$ttt000.$area.htm";
	  $taubutton="${baseicon}tau.$ttt000.gif";
	  $taubutton="${baseicon}tau.$ttt000.display.gif" if($ttt000 eq $tau);

if($InteractiveTauButtons ) {

	  print WH "
<td>
<input type='button' class='btnsmltau'
onMouseOver=\"className='btnsmltauover'; ptau='${ttt000}',pswap();\"
onMouseOut=\"className='btnsmltau';\"
value='${ttt000}' name=taub
onClick=\"cvalue='$urltaufile';opentype='page',swaphtm();\">
</td>";

} else {
#	  print WH "
#<td>
#<a href=\"$urltaufile\">
#<img src=\"$taubutton\" img border=\"0\"></a>
#</td>
#";

	  print WH "
<td>
<input type='button' class='btnsmltau'
onMouseOver=\"className='btnsmltauover';\"
onMouseOut=\"className='btnsmltau';\"
value='${ttt000}' name=taub
onClick=\"cvalue='$urltaufile';opentype='page',swaphtm();\">
</td>";


      }

	}



      }

print WH "
<td>
<input type='button' class='btn75model'
onMouseOver=\"className='btn75modelover';\" onMouseOut=\"className='btn75model';\"
value='VERI Tau' name=tctrk
onClick=\"cvalue=\'$phphref1\';opentype='page',swaphtm();\">
</td>
<td>
<input type='button' class='btn75model'
onMouseOver=\"className='btn75modelover';\" onMouseOut=\"className='btn75model';\"
value='R-R Con Tau' name=tctrk
onClick=\"cvalue=\'$phphref2\';opentype='page',swaphtm();\">
</td>
";

# EEEEEEEEEEEEEEEEEEEEEEEEEEEEE 333333333333333333333333333333333333333333333333333333333333333 -->



      print WH "</tr><tr></table><table border=1 cellpadding=0 cellspacing=0>";
# BBBBBBBBBBBBBBBBBBBBBBBBBBBB  111111111111111111111111111111111111111111111111111111111111111 -->
#---------- other models -----------------

$curmodfile="${model_grf_name{$model}}${model_grf_ext{$model}}.$m.${tau}.$area.png";

#----------------
# php model looper
#-------------------
#?dtg=2007092500&tau=072&area=tropepac&plot=n850

$ttt000=sprintf("%03d",$tau);

$phpopt="dtg=$tdtg&tau=$ttt000&area=$area&plot=$m";
$phphref="../../w2animgif.php?$phpopt";

print WH"
<td>
<input type='button' class='btn85model'
onMouseOver=\"className='btn85modelover';\" onMouseOut=\"className='btn85model';\"
value='Loop Models' name=tctrk
onClick=\"cvalue=\'$phphref\';opentype='page',swaphtm();\">
</td>
";

      foreach $mm (@models) {
	  $truth=0;
	  $testmodfile="${model_grf_name{$mm}}${model_grf_ext{$mm}}.$m.${tau}.$area.png";
	  $there=$gfile_truth{$testmodfile};
	  $truth=1 if($there && ($testmodfile));
	  $urlomfile="${basewxmap}web_$mm/$data_time/${mm}.$m.${tau}.$area.htm";

	  $omm='gfs';
	  if($model eq 'ocn' && $mm eq $omm) {
	      $ommplot='uas';
	      $urlomfile="${basewxmap}web_$omm/$data_time/${omm}.$ommplot.${tau}.$area.htm";
	      $truth=1;
	  }

	  if( $truth) {
	      print WH "
<td>
<input type='button' class='btnsmlmod'
onMouseOver=\"className='btnsmlmodover';model='${mm}',pswap();\"
onMouseOut=\"className='btnsmlmod';\"
value='$mm' name=tctrk
onClick=\"cvalue='$urlomfile';opentype='page',swaphtm();\">
</td>
";


	  } else {

	      $donot=1;
	      if($mm eq 'ocn' && $doocnhtml == 0) {
		  $donot=0;
	      }

	      if($donot) {
		  print WH "
<td>
<input type='button' class='btnsmlmodnot'
value='$mm' name=tctrk
onClick=\"cvalue='';opentype='page';\">
</td>
";
	      }
	  }
      }



# ------------------------- put gfs buttons on ocn plot page WH
      if($model eq 'ocn' && $doocnhtml) {

	  $omodel='gfs';
	  foreach $mplot (plot_types($omodel)) {

	      $gfile="${model_grf_name{$omodel}}${model_grf_ext{$omodel}}.$mplot.$tau.$area.png";
	      $there=$gfile_truth{$gfile};

	      if($there) {
		  $hfile="${hfileheaddir}/${omodel}.$mplot.${tau}.$area.htm";
		  $hfile2="${omodel}.$mplot.${tau}.$area.htm";
		  $urlhfile="${basewxmap}web_$omodel/$tdtg/${omodel}.$mplot.${tau}.$area.htm";

		  print WH "
<td>
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';\" onMouseOut=\"className='btnsml';\"
value='$mplot' name=tctrk
onClick=\"cvalue='$urlhfile';opentype='page',swaphtm();\">
</td>
";
	      } else {

		  $donot=1;
		  if($model eq 'ocn' && $doocnhtml == 0) {
		      $donot=0;
		  }

		  if($donot) {

		      print WH "
<td>
<input type='button' class='btnsmlnot'
onMouseOver=\"className='btnsmlnotover';\" onMouseOut=\"className='btnsmlnot';\"
value='$mplot' name=tctrk>
</td>
";
		  }

	      }

	  }

      }



#---------- other plots  -----------------


#
# make js for dropdown menus for misc plots
#
print WH "
<script type=\"text/javascript\">
//Contents for menu 1
var menu2=new Array()
";

$npo=0;

foreach $mplot (plot_types($model)) {

    $gfile="${model_grf_name{$model}}${model_grf_ext{$model}}.$mplot.$tau.$area.png";
    $there=$gfile_truth{$gfile};
    $bmplot=$mapbutton{$mplot};
    $bmt=$shortmaptitle{$mplot};
    if($there) {
	$hfile="${hfileheaddir}/${model}.$mplot.${tau}.$area.htm";
	$hfile2="${model}.$mplot.${tau}.$area.htm";
	$urlhfile="${basewxmap}web_$model/$tdtg/${model}.$mplot.${tau}.$area.htm";
	print WH "menu2[$npo]='<a href=\"$urlhfile\">$bmplot - $bmt</a>'\n";
    }
    $npo++;
}

print WH"
</script>
";

$npo=0;
$npomax=4;

      foreach $mplot (plot_types($model)) {


	  $gfile="${model_grf_name{$model}}${model_grf_ext{$model}}.$mplot.$tau.$area.png";
	  $there=$gfile_truth{$gfile};
	  $bmplot=$mapbutton{$mplot};

	  if($npo <= $npomax) { 

	      if($there) {
		  $hfile="${hfileheaddir}/${model}.$mplot.${tau}.$area.htm";
		  $hfile2="${model}.$mplot.${tau}.$area.htm";
		  $urlhfile="${basewxmap}web_$model/$tdtg/${model}.$mplot.${tau}.$area.htm";

		  if($InteractiveProductButtons ) {
		      print WH "
<td>
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';ptype='${mplot}',pswap();\"
onMouseOut=\"className='btnsml';\"
value='$bmplot' name=tctrk
onClick=\"cvalue='$hfile2';opentype='page',swaphtm();\">
</td>
";
		  } else {

		      print WH "
<td>
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';\" onMouseOut=\"className='btnsml';\"
value='$bmplot' name=tctrk
onClick=\"cvalue='$hfile2';opentype='page',swaphtm();\">
</td>
";
		  }

	      } else {

		  print WH "
<td>
<input type='button' class='btnsmlnot'
onMouseOver=\"className='btnsmlnotover';\" onMouseOut=\"className='btnsmlnot';\"
value='$bmplot' name=tctrk>
</td>
";
	      }

	      $npo++;


	  }

      }

print WH "
<td>
<input type='button' class='btn100pull'
onMouseover=\"dropdownmenu(this, event, menu2, '300px')\" ;
onMouseout=\"delayhidemenu()\";
value='PLOTS...' name=tctrk
\">
</td>
";

$urlamfile="${model}.allmap.${tau}.$area.htm";
$urlatfile="${model}.alltau.${m}.$area.htm";
print WH "
<td>
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='Allmap' name=tctrk
onClick=\"cvalue=\'$urlamfile\';opentype='page',swaphtm();\">
</td>
";

print WH "
<td>
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='Alltau' name=tctrk
onClick=\"cvalue=\'$urlatfile\';opentype='page',swaphtm();\">
</td>
";

#------------- help ------------------------
print WH "
<td>
<input type='button' class='btn75a'
onMouseOver=\"className='btn75aover';\" onMouseOut=\"className='btn75a';\"
value='HELP' name=tctrk
onClick=\"cvalue=\'${basewxmap}wx.help.htm\';opentype='page',swaphtm();\">
</td>
";



# ------------------------- add ocn plot buttons to met model pages WH


      if($model ne 'ocn' && $doocnhtml) {
	  $omodel='ocn';
	  foreach $mplot (plot_types($omodel)) {

	      $gfile="${model_grf_name{$omodel}}${model_grf_ext{$omodel}}.$mplot.$tau.$area.png";
	      $there=$gfile_truth{$gfile};

	      if($there) {
		  $hfile="${hfileheaddir}/${omodel}.$mplot.${tau}.$area.htm";
		  $hfile2="${omodel}.$mplot.${tau}.$area.htm";
		  $urlhfile="${basewxmap}web_$omodel/$tdtg/${omodel}.$mplot.${tau}.$area.htm";
		  print WH "
<td>
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';\" onMouseOut=\"className='btnsml';\"
value='$mplot' name=tctrk
onClick=\"cvalue='$urlhfile';opentype='page',swaphtm();\">
</td>
";
	      } else {

		  $donot=1;
		  if($model eq 'ocn' && $doocnhtml == 0) {
		      $donot=0;
		  }
		  if($donot) {
		      print WH "
<td>
<input type='button' class='btnsmlnot'
onMouseOver=\"className='btnsmlnotover';\" onMouseOut=\"className='btnsmlnot';\"
value='$mplot' name=tctrk>
</td>
";
		  }
	      }
	  }

      }
  }


# EEEEEEEEEEEEEEEEEEEEEEEEEEEE  111111111111111111111111111111111111111111111111111111111111111 -->

  print WH "</tr><tr></table><table border=1 cellpadding=0 cellspacing=0>";

# BBBBBBBBBBBBBBBBBBBBBBBBBBBB  222222222222222222222222222222222222222222222222222222222222222 -->
#-------------------- 2nd row ---------------------
#
#  movies
#  home pages
#  other tropical basin
#  help
#
#--------------------------------------------------


#---------- other resources : sat image/winds  -----------------

if($url{'sat',$area}) {
	  
###      print WH "<td class=button><a href=\"$url{'sat',$area}\" >SatPix</td>\n" 
print WH "
<td>
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='SatPix' name=tctrk
onClick=\"cvalue=\'$url{'sat',$area}\';opentype='external',pswap();\">
</td>
";
      }

      if($url{'sat_v_hi',$area}) {
###	  print WH "<td class=button><a href=\"$url{'sat_v_hi',$area}\" >SatVhi</a></td>\n";
print WH "
<td>
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" 
onMouseOut=\"className='btn50etc';\"
value='SatVhi' name=tctrk
onClick=\"cvalue=\'$url{'sat_v_hi',$area}\';opentype='external',pswap();\">
<!--
onClick=\"cvalue=\'$url{'sat_v_hi',$area}\';opentype='page',swaphtm();\">
-->
</td>
";
      }

      if($url{'sat_v_lo',$area}) {
print WH "
<td>
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='SatVlo' name=tctrk
onClick=\"cvalue=\'$url{'sat_v_lo',$area}\';opentype='external',pswap();\">
</td>
";

      }

      if($url{'sat_v_sh',$area}) {
print WH "
<td>
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='SatShr' name=tctrk
onClick=\"cvalue=\'$url{'sat_v_sh',$area}\';opentype='external',pswap();\">
</td>
";
}

#------------------------------------------------------------
# 20030315 -- tc struct buttons
#
#

foreach $carqstm (@carqstms) {
    $carqareas=$stmareas{$carqstm};
    @tt=split(' ',$carqareas);
    foreach $ttt (@tt) {
	$testarea=$ttt;
	if($testarea eq $area) {
	    $phpopt="dtg=$tdtg&storm=$carqstm&model=$model";
#		  print WH "<td class=button2><a href=\"../../tcstruct.php?$phpopt\"><b><i>$carqstm</i></b></a></td>\n";
	    $phphref="../../tcstruct.php?$phpopt";

	    $phpstm=substr($carqstm,0,3);
	    print WH "
<td>
<input type='button' class='btn50red'
onMouseOver=\"className='btn50redover';\" onMouseOut=\"className='btn50red';\"
value='$phpstm' name=tctrk
onClick=\"cvalue=\'$phphref\';opentype='page',swaphtm();\">
</td>
";
	      }
    }
}

#---------- other resources : sst  -----------------

      if( $sstfilecur_there) {
	print WH "<td><a href=$ssturlcur><img src=\"$button{'fnmoc_sst','img'}\"  img border=\"0\" alt=\"$button{'fnmoc_sst','alt'}\"></a></td>\n";
      } elsif( $sstfilem06_there) {
	  print WH "<td><a href=$ssturlm06><img src=\"$button{'fnmoc_sst','img'}\"  img border=\"0\" alt=\"$button{'fnmoc_sst','alt'}\"></a></td>\n";
      } elsif( $sstfilem12_there) {
	  print WH "<td><a href=$ssturlm12><img src=\"$button{'fnmoc_sst','img'}\"  img border=\"0\" alt=\"$button{'fnmoc_sst','alt'}\"></a></td>\n";
      }

     $truth=0;
foreach $mm (@models) {
    $truth=( $ng{$mm} > 0 );
    if( $truth) {

	print WH "
<td>
<input type='button' class='btn50grn'
onMouseOver=\"className='btn50grnover';\" onMouseOut=\"className='btn50grn';\"
value='$mm.H' name=tctrk
onClick=\"cvalue=\'${basewxmap}$mm.$area.$tdtg.htm\';opentype='page',swaphtm();\">
</td>
";

    }
} 

#------------ wxmap home -------------------



print WH "
<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2.H' name=tctrk
onClick=\"cvalue=\'${basewxmap}wx${wxdtg}htm\';opentype='page',swaphtm();\">
</td>
";

#
# -------------------  other basins
#

print WH "

<td>
<input type='button' class='btn100pull'
onMouseover=\"dropdownmenu(this, event, menu1, '150px')\" ;
onMouseout=\"delayhidemenu()\";
value='BASINS...' name='tctrk'\">
</td>
";



#--------------- back button
print WH "
<td>
<input type='button' class='btnsmletc'
onMouseOver=\"className='btnsmletcover';\" onMouseOut=\"className='btnsmletc';\"
value='<-B' name=tctrk
onClick=\"history.back();\">
</td>
";

#--------------- forward button
print WH "
<td>
<input type='button' class='btnsmletc'
onMouseOver=\"className='btnsmletcover';\" onMouseOut=\"className='btnsmletc';\"
value='F->' name=tctrk
onClick=\"history.forward();\">
</td>
";




# EEEEEEEEEEEEEEEEEEEEEEEEEEEE  222222222222222222222222222222222222222222222222222222222222222 -->

      print WH "</tr></table>";



#------------------- the image and right hand buttons ----------------
#
#  FINALLY, the image
#
#------------------- the image and right hand buttons ----------------

$web1="
<table border=1 cellpadding=0 cellspacing=0>
<tr>
<td width=$xsize>
<a name='link' href='myUrl' target='_blank'><img name='myImage' width='$xsize'></a>
<!--
<img src=\"$urlgfile\">
-->
";

print WH $web1;

##################################################
#
#----- previous runs
#
##################################################

      $taup120=dtg000($tau*1+120);
      $taup96=dtg000($tau*1+96);
      $taup72=dtg000($tau*1+72);
      $taup48=dtg000($tau*1+48);
      $taup36=dtg000($tau*1+36);
      $taup24=dtg000($tau*1+24);
      $taup12=dtg000($tau*1+12);
      $taup6=dtg000($tau*1+6);
      $taum0=dtg000($tau*1+0);
      $taup0=dtg000($tau*1-0);
      $taum6=dtg000($tau*1-6);
      $taum12=dtg000($tau*1-12);
      $taum24=dtg000($tau*1-24);
      $taum36=dtg000($tau*1-36);
      $taum48=dtg000($tau*1-48);
      $taum72=dtg000($tau*1-72);
      $taum96=dtg000($tau*1-96);
      $taum120=dtg000($tau*1-120);

      print WH "</td><td valign=top align=left width=$width{'vbbs'}>\n";

      if($taup120*1 <= $ntau) { 
	$urlp120file="${basewxmap}web_$model/${tdtgm120}/${model}.${m}.${taup120}.$area.htm";

print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T-120' name=tctrk
onClick=\"cvalue=\'$urlp120file\';opentype='page',swaphtm();\">
";

      }

      if($taup96*1 <= $ntau) { 
	$urlp96file="${basewxmap}web_$model/${tdtgm96}/${model}.${m}.${taup96}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T-96' name=tctrk
onClick=\"cvalue=\'$urlp96file\';opentype='page',swaphtm();\">
";


      }

      if($taup72*1 <= $ntau) { 
	$urlp72file="${basewxmap}web_$model/${tdtgm72}/${model}.${m}.${taup72}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T-72' name=tctrk
onClick=\"cvalue=\'$urlp72file\';opentype='page',swaphtm();\">
";
      }


      if($taup48*1 <= $ntau) { 
	$urlp48file="${basewxmap}web_$model/${tdtgm48}/${model}.${m}.${taup48}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T-48' name=tctrk
onClick=\"cvalue=\'$urlp48file\';opentype='page',swaphtm();\">
";
      }

      if($taup36*1 <= $ntau && $tauinc == 12 ) { 
	$urlp36file="${basewxmap}web_$model/${tdtgm36}/${model}.${m}.${taup36}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T-36' name=tctrk
onClick=\"cvalue=\'$urlp36file\';opentype='page',swaphtm();\">
";
      }
     
      if($taup24*1 <= $ntau) { 
	$urlp24file="${basewxmap}web_$model/${tdtgm24}/${model}.${m}.${taup24}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T-24' name=tctrk
onClick=\"cvalue=\'$urlp24file\';opentype='page',swaphtm();\">
";
      }

      if($taup12*1 <= $ntau && $tauinc == 12) { 
	$urlp12file="${basewxmap}web_$model/${tdtgm12}/${model}.${m}.${taup12}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T-12' name=tctrk
onClick=\"cvalue=\'$urlp12file\';opentype='page',swaphtm();\">
";
      }

      if($taup6*1 <= $ntau && $tauincrun == 6) { 
	  $urlp6file="${basewxmap}web_$model/${tdtgm6}/${model}.${m}.${taup0}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T-6' name=tctrk
onClick=\"cvalue=\'$urlp6file\';opentype='page',swaphtm();\">
";
      }

      if($taum6*1 <= $ntau && $tauincrun == 6) { 
	  $urlm6file="${basewxmap}web_$model/${tdtgp6}/${model}.${m}.${taum0}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T+6' name=tctrk
onClick=\"cvalue=\'$urlm6file\';opentype='page',swaphtm();\">
";
      }

      if($taum12*1 >= 0 && $tauinc == 12) { 
	$urlm12file="${basewxmap}web_$model/${tdtgp12}/${model}.${m}.${taum12}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T+12' name=tctrk
onClick=\"cvalue=\'$urlm12file\';opentype='page',swaphtm();\">
";
      }

      if($taum24*1 >= 0 && $tauinc == 12) { 
	$urlm24file="${basewxmap}web_$model/${tdtgp24}/${model}.${m}.${taum24}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T+24' name=tctrk
onClick=\"cvalue=\'$urlm24file\';opentype='page',swaphtm();\">
";
      }

      if($taum36*1 >= 0 && $tauinc == 12) { 
	$urlm36file="${basewxmap}web_$model/${tdtgp36}/${model}.${m}.${taum36}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T+36' name=tctrk
onClick=\"cvalue=\'$urlm36file\';opentype='page',swaphtm();\">
";
      }

      if($taum48*1 >= 0 && $tauinc == 12) { 
	$urlm48file="${basewxmap}web_$model/${tdtgp48}/${model}.${m}.${taum48}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T+48' name=tctrk
onClick=\"cvalue=\'$urlm48file\';opentype='page',swaphtm();\">
";
      }

      if($taum72*1 >= 0 && $tauinc == 12) { 
	$urlm72file="${basewxmap}web_$model/${tdtgp72}/${model}.${m}.${taum72}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T+72' name=tctrk
onClick=\"cvalue=\'$urlm72file\';opentype='page',swaphtm();\">
";
      }

      if($taum96*1 >= 0 && $tauinc == 12) { 
	$urlm96file="${basewxmap}web_$model/${tdtgp96}/${model}.${m}.${taum96}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T+96' name=tctrk
onClick=\"cvalue=\'$urlm96file\';opentype='page',swaphtm();\">
";
      }

      if($taum120*1 >= 0 && $tauinc == 12) { 
	$urlm120file="${basewxmap}web_$model/${tdtgp120}/${model}.${m}.${taum120}.$area.htm";
print WH "
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='T+120' name=tctrk
onClick=\"cvalue=\'$urlm120file\';opentype='page',swaphtm();\">
";
      }



###################################################
#
#  previous analyses
#
###################################################

      if($tau eq "000") {

      print WH "</td><td valign=top align=left width=$width{'vbbs'} nowrap>\n";

      $urlm72file="${basewxmap}web_$model/${tdtgm72}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An-72' name=tctrk
onClick=\"cvalue=\'$urlm72file\';opentype='page',swaphtm();\">
";

      $urlm48file="${basewxmap}web_$model/${tdtgm48}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An-48' name=tctrk
onClick=\"cvalue=\'$urlm48file\';opentype='page',swaphtm();\">
";


      $urlm36file="${basewxmap}web_$model/${tdtgm36}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An-36' name=tctrk
onClick=\"cvalue=\'$urlm24file\';opentype='page',swaphtm();\">
";


      $urlm24file="${basewxmap}web_$model/${tdtgm24}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An-24' name=tctrk
onClick=\"cvalue=\'$urlm24file\';opentype='page',swaphtm();\">
";

      $urlm12file="${basewxmap}web_$model/${tdtgm12}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An-12' name=tctrk
onClick=\"cvalue=\'$urlm12file\';opentype='page',swaphtm();\">
";

      if($tauincrun == 6) { 
      $urlm6file="${basewxmap}web_$model/${tdtgm6}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An-6' name=tctrk
onClick=\"cvalue=\'$urlm6file\';opentype='page',swaphtm();\">
";

      $urlp6file="${basewxmap}web_$model/${tdtgp6}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An+6' name=tctrk
onClick=\"cvalue=\'$urlp6file\';opentype='page',swaphtm();\">
";

  }

      $urlp12file="${basewxmap}web_$model/${tdtgp12}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An+12' name=tctrk
onClick=\"cvalue=\'$urlp12file\';opentype='page',swaphtm();\">
";

      $urlp24file="${basewxmap}web_$model/${tdtgp24}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An+24' name=tctrk
onClick=\"cvalue=\'$urlp24file\';opentype='page',swaphtm();\">
";

      $urlp36file="${basewxmap}web_$model/${tdtgp36}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An+36' name=tctrk
onClick=\"cvalue=\'$urlp36file\';opentype='page',swaphtm();\">
";

      $urlp48file="${basewxmap}web_$model/${tdtgp48}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An+48' name=tctrk
onClick=\"cvalue=\'$urlp48file\';opentype='page',swaphtm();\">
";


      $urlp72file="${basewxmap}web_$model/${tdtgp72}/${model}.${m}.000.$area.htm";
print WH "
<input type='button' class='btn50etc'
onMouseOver=\"className='btn50etcover';\" onMouseOut=\"className='btn50etc';\"
value='An+72' name=tctrk
onClick=\"cvalue=\'$urlp72file\';opentype='page',swaphtm();\">
";

  }

      $dobottom=0;

      if($dobottom) {

print WH <<"EOF";
</td>
</tr>
</table>
<i>Click on the buttons above and to the right of the map to manuever through 
the data and go to other maps</i><br> 
When in doubt, hit the <b><i>HELP!</b></i> button.<br>
EOF

print WH $webmast;


      } else { 


	 $llmohtm= LatLonMouseOver($area);

print WH <<"EOF";
</td>
</tr>
</table>

$llmohtm

</body>
</html>

EOF



      close(WH);

    }

##################################################
#
# create the all map file
#
##################################################

    foreach $mm (plot_types($model)) {

      $mtm=$maptitle{$mm};
      $gfile="${model_grf_name{$model}}${model_grf_ext{$model}}.$mm.$tau.$area.png";
      $there=$gfile_truth{$gfile};

      if( $there  ) { 

	$gfile="${model_grf_name{$model}}${model_grf_ext{$model}}.$mm.${tau}.$area.png";
	$hfile="${model}.$mm.${tau}.$area.htm";
	$urlhfile="${basewxmap}web_$model/$data_time/$hfile";
        $urlgfile="${basewxmap}$model_http_gdir{$model}/$data_time/$gfile";

print AM <<"EOF";
<br><b>$model_desc{$model} t = $itau forecast of $mtm</b><br>
<a href=\"$urlhfile\"><img src=\"$urlgfile\" img border=\"0\"></a>
EOF


      }

    }

    print AM "</html>\n";
    close(AM);

  }  #------------- end of tau loop
		      
    $mvfile="${basewxmaptop}web_$model/$tdtg/$model.movie.$m.$area.htm";

print WX "</td><td width=$width{'movie'} align=center><a href=\"$mvfile\"><img src=\"${baseicontop}java.movie.button.gif\" ALT=\"Java Movie\" img border=\"0\"></a></td></tr>\n";

  print AT "</body></html>\n";
  close(AT);

}  #------------- end of map  loop

print WX "</table>";

htm_wx2();

print WX $htm{'add'};
print WX $htm{'other'};
print WX $htm{'tail'};

close(WX);

}

}


exit;

##################################################
#
#  routine to create html below main map table 
#  in each model/area home
#
##################################################

sub htm_wx {

$htm{'add'}="";
if($area =~ "trop") {
  $htm{'add'}="$htm{'add'}
<a href=\"$url{'tcstruct'}\">
<img src=\"$buttontop{'tcstruct','img'}\" img border=\"0\" alt=\"$buttontop{'tcstruct','alt'}\">
</a>\n";
}

if( $sstfilecur_there) {
	
  $htm{'add'}="$htm{'add'}
<a href=$ssturlcurtop><img src=\"$buttontop{'fnmoc_sst','img'}\"  img border=\"0\" alt=\"$buttontop{'fnmoc_sst','alt'}\"></a>\n";

} elsif( $sstfilem06_there) {
	  
  $htm{'add'}="$htm{'add'}
<a href=$ssturlm06top><img src=\"$buttontop{'fnmoc_sst','img'}\"  img border=\"0\" alt=\"$buttontop{'fnmoc_sst','alt'}\"></a>\n";

} elsif( $sstfilem12_there) {
	  
  $htm{'add'}="$htm{'add'}
<a href=$ssturlm12top><img src=\"$buttontop{'fnmoc_sst','img'}\"  img border=\"0\" alt=\"$buttontop{'fnmoc_sst','alt'}\"></a>\n";

}

$htm{'add'}="$htm{'add'}
<a href=\"$url{'tc',$area}\"><img src=\"$buttontop{'tc','img'}\" img border=\"0\" alt=\"$buttontop{'tc','alt'}\"></a>\n" if($area =~ "trop");

$htm{'add'}="$htm{'add'}
<a href=\"$url{'sat',$area}\"><img src=\"$buttontop{'sat','img'}\" img border=\"0\" alt=\"$buttontop{'sat','alt'}\"></a>\n" if($url{'sat',$area});

$htm{'add'}="$htm{'add'}
<a href=\"$url{'sat_v_hi',$area}\"><img src=\"$buttontop{'sat_v_hi','img'}\" img border=\"0\" alt=\"$buttontop{'sat_v_hi','alt'}\"></a>\n" if($url{'sat_v_hi',$area});

$htm{'add'}="$htm{'add'}
<a href=\"$url{'sat_v_lo',$area}\"><img src=\"$buttontop{'sat_v_lo','img'}\" img border=\"0\" alt=\"$buttontop{'sat_v_lo','alt'}\"></a>\n" if($url{'sat_v_lo',$area});

$htm{'add'}="$htm{'add'}
<a href=\"$url{'whitbread',$area}\"><img src=\"$buttontop{'whitbread','img'}\" img border=\"0\" alt=\"$buttontop{'whitbread','alt'}\"></a>\n" if($url{'whitbread',$area});

if($htm{'add'} ne "") {

$htm{'add'}="
<br>
<table cellpadding=0 cellspacing=0>
<tr>
<td width=$width{'c1b'} align=right>
<b><font color=darkblue>More Maps/Info:</b></font>
</td>
<td align=left valign=center>
$htm{'add'}
</td>
</tr>
</table>
";
} else {
  $htm{'add'}="<br>";
}

$htm{'other'}="
<br>
<table border=0 cellpadding=0 cellspacing=0>
<td width=$width{'c1b'} align=right>
<b><font color=darkblue>Other Models/Help:</b></font>
</td>
<td width=$width{'c2'} align=left>
";

$there=0;
foreach $mm (@models) {
  $truth=( $mm ne $model && ($ng{$mm} != 0)) ;
  if( $truth) {
    $urlhfile="${basewxmaptop}${mm}.${area}.$tdtg.htm";
    $htm{'other'}="
$htm{'other'}
<a href=\"$urlhfile\"><img src=\"${baseicontop}home.${mm}.big.gif\" img border=\"0\"></a>\n";

    $there=1;
  }
} 

if($there == 0) {
  print WH " <font color=red><b>N/A</b></font>";
}


$htm{'other'}="$htm{'other'}
<a href=\"${basewxmaptop}wx.htm\"><img src=\"${baseicontop}home.wxmap.big.gif\" img border=\"0\"></a>
<a href=\"${basewxmapdoctop}wxmap.faq.htm\"><img src=\"${baseicontop}doc.wxmap.faq.gif\" img border=\"0\">
<a href=\"${basewxmapdoctop}wxmap.www.stat.htm\"><img src=\"${baseicontop}doc.wxmap.stats.gif\" img border=\"0\">
<a href=\"${basewxmapdoctop}wxmap.help.htm\"><img src=\"${baseicontop}doc.wxmap.help.gif\" img border=\"0\">
</a>
</td>
</tr>
</table>
";


$htm{'tail'}="
<p>Click on the <b>green</b>, <b>All Map</b> or <b>All
Times buttons</b> in the main table to display the map(s).  Click on the
<b>Java Movie button</b> to animate all times, but<br>
<a href=\"${basewxmapdoc}java.animation.htm\">
<strong><i><font color=red>READ THIS DOC FIRST...</strong></i></font></a>
Other map and info buttons appear below the map table 
and you can go to other model home pages 
(<b>AVN,MRF,NGP</b> depending on availability) or <b>WXMAP Home</b>
to pick a new area.</p>
$webmast
";

}




sub htm_wx2 {

$htm{'add'}="";


$htm{'other'}="
<br>
<table border=0 cellpadding=0 cellspacing=0>
<td width=$width{'c1b'} align=right>
<b><font color=darkblue>Other:</b></font>
</td>
";


$htm{'other'}="$htm{'other'}
<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2.H' name=tctrk
onClick=\"cvalue=\'${basewxmaptop}wx${wxdtg}htm\';opentype='page',swaphtm();\">
</td>
</tr>
</table>
";


$htm{'tail'}="
$webmast<br>
";

}


#
#  main page generator
#

sub wxmap_home {

$fdtg=dtg("full");
$timecdtg=dtg("time");
$watchtimedtg=dtg("watchtime");
$watchtime=dtg2time($tdtg);


$homefile="wx.$area.$tdtg.htm";

open(WM,">$homefile") || die "unable to homefile: $homefile\n";

print WM <<"EOF";
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
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/wxmain.css\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/dropdown.css\">

<title>$prodcenter NWP Weather Maps for $area_desc{$area}</title>
</head>

<body background="${baseicontop}bkggrey.gif" TEXT="#000000" LINK="#0000FF" VLINK="#006030">


<h2><font face="arial"><i>$prodcenter NWP Weather Maps</i></font><br>
<font face="arial" color=blue ><i>$area_desc{$area}</i></font><br>
<font face="arial" color=red >Map <a href=\"${basewxmapdoctop}what.is.a.dtg.htm\">DTG</a>: $tdtg</font></h2>
<img src="${baseicontop}colaline.gif">

<p>

<table border=1 cellpadding=0 cellspacing=0>
<tr>
<td width=350 align=right>
This Page Was Created:
</td>
<td width=250 align=left>
$timecdtg
</td>
</tr>

<tr>
<td width=350 align=right>
<b><font color=red>The Base <i>Time</i> of the Maps:</i></b></font>
</td>
<td width=250 align=left>
<b>$watchtime</b>
</td>
</tr>

</table>
<p>
<table border=0 cellpadding=0 cellspacing=0>
<tr>
<td width=$width{'c1'} align=right>
<b><font color=darkblue>Area/Model Home Pages:</b></font>
</td>
<td width=$width{'c2'} align=left>
EOF

foreach $mm (@models) {

  if($ng{$mm} > 0) {
#    $urlatfile="${basewxmap}$mm/$tdtg/$mm.$area.$tdtg.htm";
    $urlatfile="${basewxmaptop}$mm.$area.$tdtg.htm";
    print WM "<a href=\"$urlatfile\"><img src=\"${baseicontop}home.${mm}.big.gif\" img border=\"0\"></a>\n";
  }
}

foreach $aa (@areas) {
  print WM "<a href=\"${basewxmaptop}wx.$aa.$tdtg.htm\"><img src=\"${baseicontop}home.area.$aa.gif\" alt=\"$aa home\" img border=\"0\"></a>\n" if($aa ne $area);
}

print WM "<a href=\"${basewxmaptop}wx.htm\"><img src=\"${baseicontop}home.wxmap.big.gif\" img border=\"0\"></a>\n";

print WM <<"EOF";
</td></tr>
</table>
<br>
<table border=0 cellpadding=0 cellspacing=0>
<td width=$width{'c1'} align=right valign=center>
<b><font color=darkblue>Click on these buttons for help:</font></b>
</td>
<td width=575 align=left valign=center>
<a href=\"${basewxmapdoctop}wxmap.intro.htm\"><img src=\"${baseicontop}doc.wxmap.intro.gif\" img border=\"0\"></a>
<a href=\"${basewxmapdoctop}wxmap.faq.htm\"><img src=\"${baseicontop}doc.wxmap.faq.gif\" img border=\"0\"></a>
<a href=\"${basewxmapdoctop}wxmap.www.stat.htm\"><img src=\"${baseicontop}doc.wxmap.stats.gif\" img border=\"0\"></a>
<a href=\"${basewxmapdoctop}wxmap.help.htm\"><img src=\"${baseicontop}doc.wxmap.help.gif\" img border=\"0\"></a>
<a href=\"${basewxmapdoctop}wxmap.doc.htm\"><img src=\"${baseicontop}doc.wxmap.doc.gif\" img border=\"0\"></a>
</td>
</tr>
</table>

<p>To look at the maps, click on a Model Home page button
(<b>IFS Home, NGP Home</b> depending on availability) in the <b><font
color=darkblue>Area/Model Home Page</font></b> button bar.  To
start at the top, click on <b>WXMAP Home</b> button ; or, to go the the maps
for a different area, click on the <b>Area Home page</b> buttons.</p>

$webmast
</body>
</html>
EOF

close(WM);

}



sub set_html_prop {

#$maptitle_width=40;
#$width{'tau'}=(100-$maptitle_width)/($ntau/$tauinc+1);
#$width{'tau'}=int($width{'tau'}*100+0.5)/100.0;

$width{'maptitle'}=300;
$width{'mapname'}=50;
$width{'tau'}=32;
$width{'movie'}=40;

$width{'c1'}=125;
$width{'c1b'}=200;
$width{'c2'}=650;
$width{'vbb'}=64;
$width{'vbbs'}=50;
$width{'vplot'}=900;

#
#  inside buttons
#

$button{'tc','img'}="${baseicon}tc.info.small.gif";
$button{'tc','alt'}="tcinfo";
$button{'tcstruct','img'}="${baseicon}tcstruct.gif";
$button{'tcstruct','alt'}="tcstruct";
$button{'allmap','img'}="${baseicon}all.maps.gif";
$button{'allmap','alt'}="all maps";
$button{'alltimes','img'}="${baseicon}all.times.gif";
$button{'alltimes','alt'}="all times";
$button{'fnmoc_sst','img'}="${baseicon}fnmoc.sst.gif";
$button{'fnmoc_sst','alt'}="SST";

$button{'sat','img'}="${baseicon}satpix.gif";
$button{'sat','alt'}="sat pix";

$button{'sat_v_hi','img'}="${baseicon}satwind.vapor.gif";
$button{'sat_v_hi','alt'}="V vapor";

$button{'sat_v_lo','img'}="${baseicon}satwind.vis.gif";
$button{'sat_v_lo','alt'}="V vis";

$button{'sat_v_ir','img'}="${baseicon}satwind.ir.gif";
$button{'sat_v_ir','alt'}="V IR";

$button{'wxmap','nlmoc'}="${baseicon}nlmoc.wxmap.big.gif";
$button{'wxmap','nlmoc'}="Navy WXMAP";
$button{'wxmap','pcmdi'}="${baseicon}pcmdi.wxmap.big.gif";
$button{'wxmap','pcmdi'}="PCMDI WXMAP";


$buttontop{'tc','img'}="${baseicontop}tc.info.small.gif";
$buttontop{'tc','alt'}="tcinfo";
$buttontop{'tcstruct','img'}="${baseicontop}tcstruct.gif";
$buttontop{'tcstruct','alt'}="tcstruct";
$buttontop{'allmap','img'}="${baseicontop}all.maps.gif";
$buttontop{'allmap','alt'}="all maps";
$buttontop{'alltimes','img'}="${baseicontop}all.times.gif";
$buttontop{'alltimes','alt'}="all times";
$buttontop{'fnmoc_sst','img'}="${baseicontop}fnmoc.sst.gif";
$buttontop{'fnmoc_sst','alt'}="SST";
$buttontop{'sat','img'}="${baseicontop}satpix.gif";
$buttontop{'sat','alt'}="sat pix";
$buttontop{'sat_v_hi','img'}="${baseicontop}satwind.vapor.gif";
$buttontop{'sat_v_hi','alt'}="V vapor";
$buttontop{'sat_v_lo','img'}="${baseicontop}satwind.vis.gif";
$buttontop{'sat_v_lo','alt'}="V vis";
$buttontop{'sat_v_ir','img'}="${baseicontop}satwind.ir.gif";
$buttontop{'sat_v_ir','alt'}="V IR";
$buttontop{'wxmap','nlmoc'}="${baseicontop}nlmoc.wxmap.big.gif";
$buttontop{'wxmap','nlmoc'}="Navy WXMAP";
$buttontop{'wxmap','pcmdi'}="${baseicontop}pcmdi.wxmap.big.gif";
$buttontop{'wxmap','pcmdi'}="PCMDI WXMAP";


}

sub set_sst_html {

$sstfilecur="${webdir}/ngp/$tdtg/ngp.sst.000.$area.htm";
$sstfilem06="${webdir}/ngp/$tdtgm06/ngp.sst.000.$area.htm";
$sstfilem12="${webdir}/ngp/$tdtgm12/ngp.sst.000.$area.htm";
$sstfilecur_there=0;

$sstfilecur_there=(-e $sstfilecur);
$sstfilem06_there=0;
$sstfilem06_there=(-e $sstfilem06);
$sstfilem12_there=0;
$sstfilem12_there=(-e $sstfilem12);

$ssturlcurtop="${basewxmaptop}ngp/$tdtg/ngp.sst.000.$area.htm";
$ssturlcur="${basewxmap}ngp/$tdtg/ngp.sst.000.$area.htm";
$ssturlm06="${basewxmap}ngp/$tdtgm06/ngp.sst.000.$area.htm";
$ssturlm12="${basewxmap}ngp/$tdtgm12/ngp.sst.000.$area.htm";
$ssturlm06top="${basewxmaptop}ngp/$tdtgm06/ngp.sst.000.$area.htm";
$ssturlm12top="${basewxmaptop}ngp/$tdtgm12/ngp.sst.000.$area.htm";

}

sub TcstructDb ($tdtg) {

    my($verb);
    $verb=0;

    $dbpath="$dbdir/tc.db.$tdtg.txt";

    open(DB,$dbpath) || return;

    @cards=<DB>;
    $ntc=$#cards + 1;

    foreach $card (@cards) {
	@tt=split(' ',$card);

	if($verb) {
	    print "CCC $card";
	    print "CC11 $tt[0] $#tt\n";
	}

	$stm=uc($tt[0]);
	$rlat=$tt[1];
	$rlon=$tt[2];
	$vmax=$tt[3];
	$rmax=$tt[4];
	$r34=$tt[5];
	$areastc1=tc_plot_area($rlat,$rlon,'');
	$stmareas{$stm}=$areastc1;

	push @stms,$stm;

    }

    return(%stmareas)

}



