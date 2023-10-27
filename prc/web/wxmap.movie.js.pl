#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};
require("$perldir/mf.pl");
require("$perldir/wxmap.env.pl");

wxmap_env();

$prodcenter=$WXMAP{"WXMAP_PROD_CENTER"};
$basewxmap=$WXMAP{"WXMAP_HTML_BASE"};
$baseicon=$WXMAP{"WXMAP_HTML_BASE_ICON"};
$webdir=$WXMAP{"WXMAP_WEB_DIR"};
$webmast=wxmap_master() ;

$dogsm=1;
$doocnhtml=0;
$hmodel=0;

$timecdtg=dtg("time");
$curdtg=dtg6();

$narg=$#ARGV+1;

$i=0;
if($narg >= 1 ) {

  $tdtg=dtg_command_prc($ARGV[$i]) if($narg >$i); $i++;
  $area=$ARGV[$i] if($narg >$i); $i++;
  $hmodel=$ARGV[$i] if($narg >$i); $i++;

} else {
  print "\n**** current dtg: $curdtg ****\n";
  print "\n$0 :: Arguments:\n\n";
  print "   tdtg  : YYYYmmddhh | curNNN\n";
  print "   area  : ";
  foreach $a (@areas) {
    print "$a | ";
  }
  print"\n";
  print " hmodel  :";
  print"\n";
  print "Try again...\n";
  exit;
}


if($area eq 'all') {

    foreach $area (@areas) {
	$cmd="wxmap.movie.js.pl $tdtg $area $model";
	print "$cmd\n";
	system($cmd);
    }
    
    exit;

}

$wxdtg='.';
$wxdtg=".$tdtg." if($doregen);


if($area eq 'troplant') {
	  
    $obasin1='tropepac';
    $obasin2='tropwpac';
    $obasin3='conus';
    #$obasin4='europe';

} elsif($area eq 'tropepac') {

    $obasin1='troplant';
    $obasin2='tropwpac';
    $obasin3='conus';
    #$obasin4='conus';

} elsif($area eq 'tropwpac') {

    $obasin1='troplant';
    $obasin2='tropepac';
    $obasin3='conus';
    #$obasin4='asia';

} elsif($area eq 'conus') {
    $obasin1='troplant';
    $obasin2='tropepac';
    $obasin3='tropwpac';
    #$obasin4='europe';

# --------------------------------- do long plotted

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

} elsif($area eq 'tropenso') {
    $obasin1='tropsio';
    $obasin2='tropswpac';
    $obasin3='tropwpac';
    $obasin4='tropepac';

} elsif($area eq 'wconus') {
    $obasin1='tropepac';
    $obasin2='conus';
    $obasin3='europe';
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
    $obasin2='tropwpac';
    $obasin3='tropepac';
}


$nbreak1=20;

$curhh=substr($tdtg,8,2);

$cdtg=dtg6();

$atype=$area_type{$area};
@maptype=split(' ',$plot_type_plots{$atype});

$tdtgm12=dtg4inc($tdtg,-12);
$tdtgm24=dtg4inc($tdtg,-24);
$tdtgm36=dtg4inc($tdtg,-36);
$tdtgm48=dtg4inc($tdtg,-48);

$tdtgp12=dtg4inc($tdtg,+12);
$tdtgp24=dtg4inc($tdtg,+24);
$tdtgp36=dtg4inc($tdtg,+36);
$tdtgp48=dtg4inc($tdtg,+48);

$data_time="$tdtg";

# --- TC structure link
#
#

(%stmareas)=TcstructDb($tdtg);
@carqstms=keys(%stmareas);
foreach $carqstm (@carqstms) {
    $areas=$stmareas{$carqstm};
}

@hmodels=mod_db_run($curhh);

if($dogsm) {
    if( ($curhh eq '00' || $curhh eq '12') && ($area eq 'tropwpac')) {
	push(@hmodels,'gsm');
    }
}

if($hmodel ne 0 && $hmodel ne 'all') {
    @hmodels=();
    @amodels=();
    push(@hmodels,$hmodel);
    push(@amodels,$hmodel);

}

#
# create a data base with model graphics file for the target dtg
# set dotau=1 to get beg and end tau
#

mod_db_plot(1);

#
#   main loop for creating the model home pages
#

foreach $model (@hmodels) {

    @t=split(/ /,$plot_type_taus{$atype});
    if($t[0] eq 'default') {
	$taubeg=0;
	$tauend=$model_ntau{$model};
	$tauinc=$model_tauinc{$model};
    } else {
	$taubeg=$t[0];
	$tauend=$t[1];
	$tauinc=$t[2];
    }


    $hfilehead="$webdir/web_$model/$tdtg";
    $mapdir="$model_http_gdir{$model}/$tdtg";

    $center=$model_center{$model}; 
    $praccum=$model_praccum{$model};

#    $ntau=$tauend;
#    $last_tau_count=$ntau/$tauinc+1;
#    
#    $body_tau_count="";
#    for($i=1;$i<=$last_tau_count;$i++) {
#	$body_tau_count=$body_tau_count." $i";
#    }
#    $ngif=$body_tau_count;
    


  $maptitle{'prp'}="Previous $praccum-hr Precipitation Rate [mm/day] and Sea Level Pressure [hPa]";
  $shortmaptitle{'prp'}="slp / precip $praccum-hr [mm/d]";

  $modelbkg=$model_bkg{$model};

  foreach $mplot (plot_types($model)) {

      if($ng{$model,$mplot} > 0) {

  
#
#  pull beg/end tau from hash
#
	$taubeg=$ng{$model,$mplot,'taubeg'};
	$tauend=$ng{$model,$mplot,'tauend'};
	$beg_tau_count=($taubeg/$tauinc)+1;
	$last_tau_count=($tauend/$tauinc)+1;

#
# mf 20010523 -- last_tau_count is really number of images in loop
#
	$last_tau_count=$last_tau_count - $beg_tau_count + 1;

	$image_beg_tau=sprintf("%03d",$taubeg);

	$fcst_begin=$taubeg;
	$mt=$maptitle{$mplot};
	$mtfile="${hfilehead}/${model}.movie.${mplot}.$area.htm";

	if($verb) {
	    print"TTTTTTTTTTTBBBBBBBBBBBBBBEEEEEEEEEE: $model $mplot $taubeg : $tauend\n";
	    print"TTTTTTTTTTTBBBBBBBBBBBBBBEEEEEEEEEE: $beg_tau_count : $last_tau_count\n";
	    print"TTTTTTTTTTTBBBBBBBBBBBBBBEEEEEEEEEE: $image_beg_tau\n";
	    print "MMMaking movie html: $mtfile\n";
	}

	open(MT,">$mtfile") || die "unable to open: $mtfile\n";




#--------------------------------------------------
#
# html head  
#
#--------------------------------------------------

$mmmtfile="${basewxmap}web_${model}/$tdtg/${model}.${mplot}.000.$area.htm";

#<form>
#<td width=10 align="center">
#<input type="button" name="back" value="back" onClick="history.back();">
#</form>
#</td>

$urlhfile1="${basewxmap}web_${model}/$tdtg/${model}.movie.${mplot}.$obasin1.htm";
$urlhfile2="${basewxmap}web_${model}/$tdtg/${model}.movie.${mplot}.$obasin2.htm";
$urlhfile3="${basewxmap}web_${model}/$tdtg/${model}.movie.${mplot}.$obasin3.htm";
#$urlhfile4="${basewxmap}web_${model}/$tdtg/${model}.movie.${mplot}.$obasin4.htm";

print MT <<"EOF";
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

<title>$model_desc{$model} $tdgt $m Movie</title>

</head>

<body text=black link=blue vlink=purple bgcolor=#fcf1da onLoad="launch()">

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
//menu1[3]='<a href=\"$urlhfile4\">$obasin4</a>'

</script>

<script language=\"javascript\" src=\"../../js/dropdown.js\" type=\"text/javascript\"></script>
<script language=\"javascript\" src=\"../../js/wxmain.js\" type=\"text/javascript\">

<script language=\"javascript\" type=\"text/javascript\">

model='${model}';
model='${model_grf_name{$model}}';
modres='$model_gridres{$model}';
dtg='${data_time}';

parea='${area}';
ptype='${mplot}';
ptau='${tau}';
opentype='internal';
cvalue='None';


function pswap() 
{

if(model == 'gfs') {
  plotdir='../../plt_ncep_gfs';
} else if (model == 'fim') {
  plotdir='../../plt_esrl_fim';

} else if (model == 'fv3e') {
  plotdir='../../plt_esrl_fv3e';
} else if (model == 'fv3g') {
  plotdir='../../plt_esrl_fv3g';

} else if (model == 'fimx') {
  plotdir='../../plt_esrl_fimx';
} else if (model == 'ngp') {
  plotdir='../../plt_fnmoc_ngp';
} else if (model == 'ngpc') {
  plotdir='../../plt_fnmoc_ngpc';
} else if (model == 'navg') {
  plotdir='../../plt_fnmoc_navg';
} else if (model == 'ukm') {
  plotdir='../../plt_ukmo_ukm';
} else if (model == 'ecm') {
  plotdir='../../plt_ecmwf_ecm';
} else if (model == 'gsm') {
  plotdir='../../plt_jma_gsm';
} else if (model == 'ecmt') {
  plotdir='../../plt_ecmwf_ecmt';
} else if (model == 'ecmg') {
  plotdir='../../plt_ecmwf_ecmg';
} else if (model == 'cmc') {
  plotdir='../../plt_cmc_cmc';
} else if (model == 'ocn') {
  plotdir='../../plt_fnmoc_ocn';
}

//ukm10.uas.000.troplant.png
    if(opentype == 'external') {
	value=cvalue;
    } else {
	value=plotdir + '/' + dtg + '/' + model + modres + '.' + ptype + '.' + ptau + '.' + parea + '.png';
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
$model_desc{$model} <font color=red><i>$tdtg</font></i> <b>Loop</b> of $mt
</td>
</tr>
</table>

<table border=1 cellpadding=0 cellspacing=0>
<tr>
EOF


    print MT "</tr></table><tr><table border=1 cellpadding=0 cellspacing=0>\n";


#-------------------- 1st row ---------------------
#
#  tau buttons
#
#--------------------------------------------------

	$mmmtfile="${basewxmap}web_${model}/$tdtg/${model}.${mplot}.000.$area.htm";

###	print MT "<td class=button1 width=150><a href=\"$mmmtfile\">Single-Map Taus:</a></td>";
####	print MT "<td class=button1 width=150>Single-Map Taus:</td>";

print MT "
<td>
<input type='button' class='btn85a'
onMouseOver=\"className='btn85aover';\" onMouseOut=\"className='btn85a';\"
value='Single Taus' name=tctrk
onClick=\"cvalue=\'$mmmtfile\';opentype='page',swaphtm();\">
</td>
";



	plot_taus2($model);

#------------------- tau buttons ---------------------
$tau='000';
for ($j=0;$j<=$#plottaus;$j++) {
    $ttt=$plottaus[$j]*1;

    $ttt000=sprintf("%03d",$ttt);
    $gfile="${model_grf_name{$model}}$model_gridres{$model}.$mplot.$ttt000.$area.png";
    print"QQQ $model $ttt000 $gfile  $gfile_truth{$gfile}\n" if($verb);
    if($gfile_truth{$gfile}) {
	$urltaufile="${basewxmap}web_$model/$data_time/${model}.${mplot}.$ttt000.$area.htm";
	print MT "
<td>
<input type='button' class='btnsmltau'
onMouseOver=\"className='btnsmltauover'; ptau='${ttt000}',pswap();\"
onMouseOut=\"className='btnsmltau';\"
value='${ttt000}' name=taub
onClick=\"cvalue='$urltaufile';opentype='page',swaphtm();\">
</td>
";
		
    }
}


print MT "</tr></table>\n";



foreach $mm (@models) {
    $truth=( $ng{$mm,$mplot} > 0 );
    if( $truth) {
	$mmmtfile="${basewxmap}web_${mm}/$tdtg/${mm}.movie.${mplot}.$area.htm";

	print MT "
<td>
<input type='button' class='btnsmlmod'
onMouseOver=\"className='btnsmlmodover';\" onMouseOut=\"className='btnsmlmod';\"
value='$mm' name=tctrk
onClick=\"cvalue=\'$mmmtfile\';opentype='page',swaphtm();\">
</td>
";


    } else {

	$donot=1;
	if($mm eq 'ocn' && $doocnhtml == 0) {
	    $donot=0;
	}
	
	if($donot) {
	    print MT "
<td>
<input type='button' class='btnsmlmodnot'
value='$mm' name=tctrk
onClick=\"cvalue=\'$mmmtfile\';opentype='page',swaphtm();\">
</td>
";
	
	}

    }
    
} 


#
# make js for dropdown menus for misc plots
#
print MT "
<script type=\"text/javascript\">
//Contents for menu 1
var menu2=new Array()
";

$npo=0; 

foreach $mmm (plot_types($model)) {
    
    if($ng{$model,$mmm} > 0) {
	    
	$bmmm=$mapbutton{$mmm};
	$mmmtfile="${basewxmap}web_${model}/$tdtg/${model}.movie.${mmm}.$area.htm";
	$bmplot=$mapbutton{$mmm};
	$bmt=$shortmaptitle{$mmm};
	print MT "menu2[$npo]='<a href=\"$mmmtfile\">$bmplot - $bmt</a>'\n";
	    
	$npo++;
	
    }

}

print MT"
</script>
";

$npo=0;
$npomax=4;

foreach $mmm (plot_types($model)) {

    if($npo <= $npomax) { 

	if($ng{$model,$mmm} > 0) {
	    
	    $bmmm=$mapbutton{$mmm};
	    $mmmtfile="${basewxmap}web_${model}/$tdtg/${model}.movie.${mmm}.$area.htm";
	    print MT "
<td>
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';\" onMouseOut=\"className='btnsml';\"
value='$bmmm' name=tctrk
onClick=\"cvalue=\'$mmmtfile\';opentype='page',swaphtm();\">
</td>
";

	} else {

	
	    print MT "
<td>
<input type='button' class='btnsmlnot'
onMouseOver=\"className='btnsmlnotover';\" onMouseOut=\"className='btnsmlnot';\"
value='$bmmm' name=tctrk
</td>
";
	
	
	}

	$npo++;
	

    }

}

print MT "
<td>
<input type='button' class='btn100pull'
onMouseover=\"dropdownmenu(this, event, menu2, '300px')\" ;
onMouseout=\"delayhidemenu()\";
value='LOOPS...' name='tctrk'\">
</td>
";



print MT "
<td>
<input type='button' class='btn75a'
onMouseOver=\"className='btn75aover';\" onMouseOut=\"className='btn75a';\"
value='HELP' name=tctrk
onClick=\"cvalue=\'${basewxmap}wx.help.htm\';opentype='page',swaphtm();\">
</td>
";



print MT "</tr><tr></table><table border=1 cellpadding=0 cellspacing=0>\n";


    foreach $carqstm (@carqstms) {
      $carqareas=$stmareas{$carqstm};
      @tt=split(' ',$carqareas);
      foreach $ttt (@tt) {
	$testarea=$ttt;
	if($testarea eq $area) {
	  $cgiopt="dtg=$tdtg&storm=$carqstm&model=$model&tau=undef";
	  print MT "<td><a href=\"/cgi-bin/wxmap/tcstruct1.cgi?$cgiopt\"><b><i>$carqstm</i></b></a></td>\n";


	}
      }
  }

      $truth=0;
      foreach $mm (@models) {
	$truth=( $ng{$mm,$mplot} > 0 );

	if( $truth) {
###	  print MT "<td><a href=\"${basewxmap}web_$mm.$area.$tdtg.htm\"><img src=\"${baseicon}${mm}.home.gif\"  img border=\"0\" ></a></td>\n";

print MT "
<td>
<input type='button' class='btn50grn'
onMouseOver=\"className='btn50grnover';\" onMouseOut=\"className='btn50grn';\"
value='${mm}.H' name=tctrk
onClick=\"cvalue=\'${basewxmap}$mm.$area.$tdtg.htm\';opentype='page',swaphtm();\">
</td>
";

	}
      } 

####	print MT "<td><a href=\"${basewxmap}wx.htm\"><img src=\"${baseicon}wxmap.home.gif\" \
###img border=\"0\" ></a></td>\n";


print MT "
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


print MT "
<td>
<input type='button' class='btn100pull'
onMouseover=\"dropdownmenu(this, event, menu1, '150px')\" ;
onMouseout=\"delayhidemenu()\";
value='BASINS...' name='tctrk'\">
</td>
";


	print MT "</tr></table>";

#######################################################################
#
# jscript set up  
# put animation in table 20070917
#
#######################################################################

$jscripthead="

<table>
<tr>
<td>
<SCRIPT LANGUAGE=\"JavaScript\">
// <!--
//
// step 1: define above the location of the images
//
//============================================================
//                >> jsImagePlayer 1.0 <<
//            for Netscape3.0+, September 1996
//============================================================
//                  by (c)BASTaRT 1996
//             Praha, Czech Republic, Europe
//
// feel free to copy and use as long as the credits are given
//          by having this header in the code
//
//          contact: xholecko\@sgi.felk.cvut.cz
//          http://sgi.felk.cvut.cz/~xholecko
//
//============================================================
// Thanx to Karel & Martin for beta testing and suggestions!
//============================================================
//
//     modified by D. Watson and A. Earnhart (CIRA/CSU), 7/30/97
//     and Greg Thompson (NCAR/RAP) Dec. 11 1997
//
//============================================================
 
//********* SET UP THESE VARIABLES - MUST BE CORRECT!!!*********************
 
//
// step 2: define variables used to determine images
//
image_plot=\"$mplot\";
image_area=\"$area\";
image_dtg=\"$tdtg\";
image_href=\"${basewxmap}$model_http_gdir{$model}/\";
image_model_type=\"${model_grf_name{$model}}\";
image_model_res=\"$model_gridres{$model}\";
image_model = image_href + image_dtg + \"/\" + image_model_type + image_model_res ;
image_beg_tau= \"$image_beg_tau\";

image_type = \"png\";

";

print MT $jscripthead;

#--------------------------------------------------
#
# jscriptp html body
#
#--------------------------------------------------

jscript_body($baseicon);


#--------------------------------------------------
#
# html tail
#
#--------------------------------------------------

print MT <<"EOF";

</body>
</html>

EOF

close(MT);

    }

  }

}


exit;


sub jscript_body($iconbase) {

  my($iconbase)=@_;


print MT <<"EOF";

//
// step 3: define dimensions of image (would be nice if this were interactively done)
//         Presently these ARE NOT used below. See step 9
//

animation_height  = 743;
animation_width  = 1225;
 
//**************************************************************************
 
//=== THE CODE STARTS HERE - no need to change anything below ===
 
//=== global variables ====
theImages = new Array();      //holds the images
imageNum = new Array();       //keeps track of which images to omit from loop
theTaus = new Array();
theTausMask = new Array();

normal_delay = 500;
normal_delay = 200;           // mod to faster animation 20070909
normal_delay = 300;           // too fast -- 20070910
delay = normal_delay;         //delay between frames in 1/100 seconds
delay_step = 50;
delay_max = 4000;
delay_min = 50;
dwell_multipler = 3;
dwell_step = 1;
end_dwell_multipler   = dwell_multipler;
start_dwell_multipler = dwell_multipler;

timeID = null;
status = 0;                      // 0-stopped, 1-playing
play_mode = 0;                   // 0-normal, 1-loop, 2-sweep
size_valid = 0;

//=== taus ====

EOF

#
#  load the taus in the .js theTaus array
#

  $nplots=0;
  $jplot=0;
  $beg_tau_count=-999;
  $decjplot=0;
  $mid12_tau_count=0;
  $mid12_tau=48;

  for ($j=0;$j<=$#plottaus;$j++) {
      $ttt=$plottaus[$j]*1;
      $ttt000=sprintf("%03d",$ttt);
      $gfile="${model_grf_name{$model}}$model_gridres{$model}.$mplot.$ttt000.$area.png";
      if($gfile_truth{$gfile}) {
	  print MT "theTaus[$jplot] = \'$ttt000\' ; \n";
	  print MT "theTausMask[$jplot] = 1 ; \n";
	  if($beg_tau_count == -999) {
	      $beg_tau_count=$jplot;
	      $fcst_begin=$ttt;
	  }
	  if($ttt == $mid12_tau) {
	    $mid12_tau_count=$jplot;
          }	    
	  $jplot++;
      } else {
	  $decjplot=1;
###	   print MT "theTausMask[$j] = 0 ; \n";
      }
  }

  $jplot-- if($decjplot);

### -- if last_tau < $mid12_tau -- set to 999

  $last_tau_count=$jplot;
  if($mid12_tau_count == 0) {
     $mid12_tau_count=999;
  } 
	
  print MT "nTaus = $jplot ; \n";

print MT <<"EOF";

first_image = $beg_tau_count;
mid12_image = $mid12_tau_count;
last_image = $last_tau_count;
fcst_begin = $fcst_begin;
current_image = first_image;     //number of the current image

//===> Make sure the first image number is not bigger than the last image number
if (first_image > last_image)
{
   var help = last_image;
   last_image = first_image;
   first_image = help;
}
 
//===> Preload the first image (while page is downloading)
   theImages[0] = new Image();
//
// step 4: construct filename of first image
//
   theImages[0].src = image_model + "." + image_plot + "." + 
                      theTaus[0] + "." + image_area + "." + image_type;
   imageNum[0] = true;
 
//==============================================================
//== All previous statements are performed as the page loads. ==
//== The following functions are also defined at this time.   ==
//==============================================================
 
//===> Stop the animation
function stop()
{
//== cancel animation (timeID holds the expression which calls the fwd or bkwd function) ==
  if (status == 1)
    clearTimeout (timeID);
// 20130415 -- not getting to the clearTimeout that stops the animation; force
  clearTimeout (timeID);
  status = 0;
  play_mode=0;
}
 
 
//===> Display animation in fwd direction in either loop or sweep mode
function animate_fwd()
{
   current_image++;                      //increment image number
 
  //== check if current image has exceeded loop bound ==
  if (current_image > last_image) {
    if (play_mode == 1) {              //fwd loop mode - skip to first image
      current_image = first_image;
    }
    if (play_mode == 2) {              //sweep mode - change directions (go bkwd)
      current_image = last_image;
      animate_rev();
      return;
    }
  }
 
  //== check to ensure that current image has not been deselected from the loop ==
  //== if it has, then find the next image that hasn't been ==
  while (imageNum[current_image-first_image] == false) {
    current_image++;
    if (current_image > last_image) {
      if (play_mode == 1)
        current_image = first_image;
      if (play_mode == 2) {
        current_image = last_image;
        animate_rev();
        return;
      }
    }
  }

  document.animation.src = theImages[current_image-first_image].src;   //display image onto screen
  document.control_form.frame_nr.value = current_image;                //display image number

  delay_time = delay;
  if (current_image == first_image)  delay_time = start_dwell_multipler*delay;
  if (current_image > mid12_image)  delay_time = delay*2.0;
  if (current_image == last_image)   delay_time = end_dwell_multipler*delay;

  //== call "animate_fwd()" again after a set time (delay_time) has elapsed ==
  timeID = setTimeout("animate_fwd()", delay_time);
}

//===> Display animation in reverse direction
function animate_rev()
{
  current_image--;                      //decrement image number

  //== check if image number is before lower loop bound ==
  if (current_image < first_image) {
    if (play_mode == 1) {               //rev loop mode - skip to last image
       current_image = last_image;
    }
    if (play_mode == 2) {
      current_image = first_image;     //sweep mode - change directions (go fwd)
      animate_fwd();
      return;
    }
  }

  //== check to ensure that current image has not been deselected from the loop ==
  //== if it has, then find the next image that hasn't been ==
  while (imageNum[current_image-first_image] == false) {
    current_image--;
    if (current_image < first_image) {
      if (play_mode == 1)
        current_image = last_image;
      if (play_mode == 2) {
        current_image = first_image;
        animate_fwd();
        return;
      }
    }
  }
 
  document.animation.src = theImages[current_image-first_image].src;   //display image onto screen
  document.control_form.frame_nr.value = current_image;                //display image number

  delay_time = delay;

  if (current_image == first_image) delay_time = start_dwell_multipler*delay;
  if (current_image == last_image)   delay_time = end_dwell_multipler*delay;
 
  //== call "animate_rev()" again after a set amount of time (delay_time) has elapsed ==
  timeID = setTimeout("animate_rev()", delay_time);
}
 
 
//===> Changes playing speed by adding to or substracting from the delay between frames
function change_speed(dv)
{
  delay+=dv;
  //== check to ensure max and min delay constraints have not been crossed ==
  if(delay > delay_max) delay = delay_max;
  if(delay < delay_min) delay = delay_min;
}
 
//===> functions that changed the dwell rates.
function change_end_dwell(dv) {
  end_dwell_multipler+=dv;
  if ( end_dwell_multipler < 1 ) end_dwell_multipler = 0;
}
 
function change_start_dwell(dv) {
  start_dwell_multipler+=dv;
  if ( start_dwell_multipler < 1 ) start_dwell_multipler = 0;
}
 
//===> Increment to next image
function incrementImage(number)
{
  stop();

  //== if image is last in loop, increment to first image ==
  if (number > last_image) number = first_image;

  //== check to ensure that image has not been deselected from loop ==
  while (imageNum[number-first_image] == false) {
    number++;
   if (number > last_image) number = first_image;
  }
 
  current_image = number;
  document.animation.src = theImages[current_image-first_image].src;   //display image
  document.control_form.frame_nr.value = current_image;                //display image number
}
 
//===> Decrement to next image
function decrementImage(number)
{
  stop();
 
  //== if image is first in loop, decrement to last image ==
  if (number < first_image) number = last_image;
 
  //== check to ensure that image has not been deselected from loop ==
  while (imageNum[number-first_image] == false) {
    number--;
   if (number < first_image) number = last_image;
  }
 
  current_image = number;
  document.animation.src = theImages[current_image-first_image].src;   //display image
  document.control_form.frame_nr.value = current_image;                //display image number
}
 
//===> "Play forward"
function fwd()
{
  stop();
  status = 1;
  play_mode = 1;
  animate_fwd();
}
 
//===> "Play reverse"

function rrev()
{
  stop();
  status = 1;
  play_mode = 1;
  animate_rev();
}

//===> "play sweep"
function sweep() {
  stop();
  status = 1;
  play_mode = 2;
  animate_fwd();
}
 
//===> Change play mode (normal, loop, swing)
function change_mode(mode)
{
   play_mode = mode;
}
 
//===> Load and initialize everything once page is downloaded (called from 'onLoad' in <BODY>)
function launch()
{
  for (var i = first_image + 1; i <= last_image; i++)
  {
    if ( fcst_begin > 0)
      var fcst_length = theTaus[i];
    else var fcst_length = theTaus[i-1];

    theImages[i-first_image] = new Image();

//
// step 5: construct filenames using the tau
//

    theImages[i-first_image].src = 
    image_model + "." + image_plot + "." + 
               fcst_length + "." + image_area + "." + image_type;

    imageNum[i-first_image] = true;
    document.animation.src = theImages[i-first_image].src;
    document.control_form.frame_nr.value = i;
 
  }
 
  // this needs to be done to set the right mode when the page is manually reloaded
  change_mode (1);
  fwd();
}
 
//===> Check selection status of image in animation loop
function checkImage(status,i)
{
  if (status == true)
    imageNum[i] = false;
  else imageNum[i] = true;
}
 
//==> Empty function - used to deal with image buttons rather than HTML buttons
function func()
{
}
 
//===> Sets up interface - this is the one function called from the HTML body
function animation()
{
  count = first_image;
}
 
// -->

</SCRIPT>

 
<NOSCRIPT>
<P ALIGN=LEFT>
<BR>
<H1>
This requires Javascript for an animation of the model forecast plots.
You will need Netscape version 3.0 or higher or Internet Explorer 3.0
or higher and Javascript enabled to view this.
</H1>
</P>
</NOSCRIPT>
<!-- Write javascript code --------------------------------------->



<SCRIPT>
//--------------------------------------------------------------
//Javascript slider code
//--------------------------------------------------------------

versionButton = 1

var browser = new Object();

if (navigator.appName.substring(0,8) == "Netscape")
{
browser.name = "NN";
}

if (navigator.appName.substring(0,9) == "Microsoft")
{
browser.name = "MSIE";
}


browser.version = Math.round(parseFloat(navigator.appVersion) * 1000);

if ((browser.name == "MSIE" && browser.version >= 4000) || (browser.name == "NN" && browser.version >= 3000)) versionButton = 3; 
if (versionButton == 3)
{
EOF



for($i=$beg_tau_count;$i<=$last_tau_count;$i++) {

$hh="
  toc${i}on = new Image(60, 20);
  toc${i}on.src = \"../../icon/on.slider.gif\";
";

print MT $hh;

}

for($i=$beg_tau_count;$i<=$last_tau_count;$i++) {

    $hh="
  toc${i}off = new Image(60, 20);
  toc${i}off.src = \"../../icon/off.slider.gif\";
";

    print MT $hh;

}

#
#  end of slider script
#
$hh="

}

function img_act(imgName,imgNum)
{
  if (versionButton == 3)
  {
   stop();
   current_image = imgNum;
   //display image
   document.animation.src = theImages[current_image-first_image].src;
   //display image number
   document.control_form.frame_nr.value = current_image;
    imgOn = eval(imgName + \"on.src\");
    document [imgName].src = imgOn;
  }
}


function img_inact(imgName)
{
  if (versionButton == 3)
  {
    imgOff = eval(imgName + \"off.src\");
    document [imgName].src = imgOff;
  }
}

// -->

</script>

<!-- End of Write javascript code ------------------------------------->
";

print MT $hh;

print MT <<"EOF";
<! //
<! // step 8: define location of buttons
<! //

<P ALIGN=left>
<TABLE ALIGN=left BORDER=1 CELLPADDING=0 CELLSPACING=0>
  <TR>
  <TD ALIGN=CENTER VALIGN=MIDDLE>
<!--    <IMG NAME="animation" width= height=540 BORDER=0 ALT="image"> -->
    <IMG NAME="animation" width=$WXMAP{'WXMAP_PLOT_XSIZE'} height=$WXMAP{'WXMAP_PLOT_YSIZE'} BORDER=0 ALT="image">
  </TD>
    <TD BGCOLOR="#9FC1FF" WIDTH=100 ALIGN=CENTER VALIGN=MIDDLE>
      <FONT SIZE=-1 COLOR="#3300CC"> Loop Mode:</FONT><BR>
      <A HREF="JavaScript: func()" onClick="change_mode(1);fwd()">
      <IMG BORDER=0 SRC="${iconbase}nrm_button.gif" ALT="Normal"></A>
      <A HREF="JavaScript: func()" onClick="sweep()">
      <IMG BORDER=0 SRC="${iconbase}swp_button.gif" ALT="Back and Forth"></A>
      <BR> <HR WIDTH="70%" SIZE=2>
      <FONT SIZE=-1 COLOR="#3300CC">Animate Frames:</FONT><BR>
      <A HREF="JavaScript: func()" onClick="change_mode(1);rrev()">
      <IMG BORDER=0 SRC="${iconbase}rev_button.gif" ALT="REV"></A>
      <A HREF="JavaScript: func()" onClick="stop()">
      <IMG BORDER=0 SRC="${iconbase}stp_button.gif" ALT="STOP"></A>
      <A HREF="JavaScript: func()" onClick="change_mode(1);fwd()">
      <IMG BORDER=0 SRC="${iconbase}fwd_button.gif" ALT="FWD"></A>
      <BR> <HR WIDTH="70%" SIZE=2>
      <FONT SIZE=-1 COLOR="#3300CC"> Dwell First:</FONT><BR>
      <A HREF="JavaScript: func()" onClick="change_start_dwell(-dwell_step)">
      <IMG BORDER=0 SRC="${iconbase}dw1_minus.gif" ALT="dec start dwell"></A>
      <A HREF="JavaScript: func()" onClick="change_start_dwell(dwell_step)">
      <IMG BORDER=0 SRC="${iconbase}dw1_plus.gif" ALT="inc start dwell"></A><BR>
      <FONT SIZE=-1 COLOR="#3300CC"> Dwell Last:</FONT><BR>
      <A HREF="JavaScript: func()" onClick="change_end_dwell(-dwell_step)">
      <IMG BORDER=0 SRC="${iconbase}dw2_minus.gif" ALT="dec end dwell"></A>
      <A HREF="JavaScript: func()" onClick="change_end_dwell(dwell_step)">
      <IMG BORDER=0 SRC="${iconbase}dw2_plus.gif" ALT="inc end dwell"></A>
      <BR> <HR WIDTH="70%" SIZE=2>
      <FONT SIZE=-1 COLOR="#3300CC">Adjust Speed:</FONT><BR>
      <A HREF="JavaScript: func()" onClick="change_speed(delay_step)">
      <IMG BORDER=0 SRC="${iconbase}slw_button.gif" ALT="--"></A>
      <A HREF="JavaScript: func()" onClick="change_speed(-delay_step)">
      <IMG BORDER=0 SRC="${iconbase}fst_button.gif" ALT="++"></A>
      <BR> <HR WIDTH="70%" SIZE=2>
      <FONT SIZE=-1 COLOR="#3300CC">Advance One:</FONT><BR>
      <A HREF="JavaScript: func()" onClick="decrementImage(--current_image)">
      <IMG BORDER=0 SRC="${iconbase}mns_button.gif" ALT="-1"></A>
      <A HREF="JavaScript: func()" onClick="incrementImage(++current_image)">
      <IMG BORDER=0 SRC="${iconbase}pls_button.gif" ALT="+1"></A>
      <HR WIDTH="70%" SIZE=2>
      <FORM METHOD="POST" NAME="control_form">
      <FONT SIZE=-1 COLOR="#3300CC">Frame No:</FONT>
        <FONT SIZE=-1>
          <INPUT TYPE="text" NAME="frame_nr" VALUE=9 SIZE="1" onFocus="this.select()" 
            onChange="go2image(this.value)">
          </INPUT>
        </FONT>
      </FORM>
<font SIZE=-1 COLOR=#3300CC>Frame Slider</font>
<table BORDER=0 CELLSPACING=0 CELLPADDING=0 BGCOLOR="#999999">
<tr>
EOF


$sliderwidth=5;
$sliderheight=25;
for($i=$beg_tau_count;$i<=$last_tau_count;$i++) {

$hh="<td>
<a href=JavaScript:func() 
onMouseover = img_act(\'toc${i}\',${i}) onMouseout = img_inact(\'toc${i}\')>
<img src=\' ../../icon/off.slider.gif\' width=$sliderwidth height=$sliderheight border=0 name=\'toc${i}\'></a>
</td>
";

print MT $hh;


}

#
# latlon show .js
#

###$llmohtm= LatLonMouseOver($area);

#-- don't know how to set up showlatlon.js to work on a loop...

$llmohtm='';

print MT <<"EOF";

     </tr>
   </table>

</td>
</tr>
</table>


$llmohtm

EOF

 }


sub movie_html{

local($model,$area,$plot,$bdtg,$edtg,$tauanal,$tauinc)=@_;
local($dtg,$i);

print "$model $plot $bdtg $edtg $tauanal $tauinc\n";

###########################################
#
#  set up movies
#
###########################################

$dtg=$bdtg;
$numgif=0;
while ( ($dtg*1 <= $edtg*1) || ( $edtg eq $bdtg) ) {

  $gdir="$model_archive_grfdir{$model}/$dtg";
  $mdir="$model_archive_moviedir{$model}";
  $gname="$gdir/$model.$plot.$tauanal.$area.png";
  $gname_movie="$mdir/$model.$plot.$tauanal.$numgif.$area.png";
  print "DDD: $i $gdir \n$gname\n $gname_movie\n";


  $dtg=dtg4inc($dtg,$tauinc);
  $numgif++;

}

exit;

  $gdir="$model_archive_grfdir{$model}/$dtg";

foreach $plot (plot_types($model)) {

  @t=split(/ /,$taus{$model,'all'});
  @t=split(/ /,$taus{$model,'prp'}) if($plot eq 'prp');

  for($tau=$taubeg;$tau<=$tauend;$tau+=$tauinc) {

    $numtau=$tau/$tauinc+1;

    $gname="$gdir/$model.$plot.$tau.$area.png";
    $gname_movie="$mdir/$model.$plot.$numtau.$area.png";

    $siz=-1;
    $siz=(-s $gname) if(-e $gname) ;

    if ($siz > $minsiz) {

      $cmd="ln -s $gname $gname_movie";
      system($cmd);
    }  
      
  }

}

}


sub TcstructDb ($tdtg) {

    my($verb);
    $verb=0;

    $dbdir="/wxmap_old/dat2/tc/tcstruct";

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

	print "QQQQQ tcdb :: $stm :: $areastc1\n";

	push @stms,$stm;

    }

    return(%stmareas)

}

