//print("<a href=\"index.php?date=$date&cycle=$cycle&area=$area&model=$model&parm=$parameterString&vtime=$vtime&maxHour=$maxHour\">$parameterString</a> |\n");
<?php
$date=$_POST["date"];
if($date==""){
	$date=$_GET["date"];
}
$vtime=$_POST["vtime"];
if($vtime==""){
	$vtime=$_GET["vtime"];
}
$maxHour=$_POST["maxHour"];
if($maxHour==""){
	$maxHour=$_GET["maxHour"];
}
$cycle=$_GET["cycle"];
$model=$_GET["model"];
$parm=$_GET["parm"];
$area=$_GET["area"];

#$zoom=$_GET["zoom"];

if($zoom == ""){
	$zoom = 1;
}


#############################################################################
##### DEFINE MODELS/PARAMETERS - this section shared with get_models.pl #####
#############################################################################
$m = 0;
$models[$m] = "gfs"; $m++;
$models[$m] = "nam"; $m++;
$models[$m] = "wave"; $m++;
$numModels = $m;

#GFS AREAS
$m = 0; $a = 0;
$areas[$m][$a] = "carib";  $a++;
$areas[$m][$a] = "npac";  $a++;
$numAreas[$m] = $a;

#NAM AREAS
$m = 1; $a = 0;
$areas[$m][$a] = "carib";  $a++;
$areas[$m][$a] = "npac";  $a++;
$areas[$m][$a] = "namer";  $a++;
$numAreas[$m] = $a;

#WW3 AREAS
$m = 2; $a = 0;
$areas[$m][$a] = "carib";  $a++;
$areas[$m][$a] = "npac";  $a++;
$numAreas[$m] = $a;

#GFS PARAMETERS
$m = 0; $p = 0;
$parameterName[$m][$p] = "MSLP_Precip";		$parameterList[$m][$p] = "slp_m_loop";		$p++;
$parameterName[$m][$p] = "10m_Wnd_6hrPrecip";	$parameterList[$m][$p] = "ten_m_loop";		$p++;
$parameterName[$m][$p] = "850mb_Hgt_Wnd_RV";	$parameterList[$m][$p] = "85v_mu_loop";		$p++;
$parameterName[$m][$p] = "700mb_Hgt_RH_Omega";	$parameterList[$m][$p] = "700_mu_loop";		$p++;
$parameterName[$m][$p] = "500mb_Hgt_Wnd_AV";	$parameterList[$m][$p] = "500_mu_loop";		$p++;
$parameterName[$m][$p] = "200mb_Hgt_Wnd";	$parameterList[$m][$p] = "200_mu_loop";		$p++;
$numParameters[$m] = $p;

#NAM PARAMETERS
$m = 1; $p = 0;
$parameterName[$m][$p] = "MSLP_Precip";		$parameterList[$m][$p] = "slp_m_loop";		$p++;
$parameterName[$m][$p] = "500mb_Hgt_Wnd_AV";	$parameterList[$m][$p] = "500_m_loop";		$p++;
$parameterName[$m][$p] = "200mb_Hgt_Wnd";	$parameterList[$m][$p] = "200_m_loop";		$p++;
$numParameters[$m] = $p;

#WW3 PARAMETERS
$m = 2; $p = 0;
$parameterName[$m][$p] = "Hgt_Swell";		$parameterList[$m][$p] = "gw3_m_loop";		$p++;
$parameterName[$m][$p] = "Peak_Dir_Period";	$parameterList[$m][$p] = "pw3_m_loop";		$p++;
$parameterName[$m][$p] = "Wind_Dir_Period";	$parameterList[$m][$p] = "sw3_m_loop";		$p++;
$numParameters[$m] = $p;


#############################################################################
### END DEFINE MODELS/PARAMETERS - this section shared with get_models.pl ###
#############################################################################

?>

<HTML>
     <HEAD><!--<META HTTP-EQUIV="Refresh" CONTENT="300">-->
     <TITLE> <?php if($vtime =="") {print("TPC-generated NCEP Model Animations $date $cycle". "Z $area $model $parm");
     		   }else{print("Forecast evolution $area $model $parm");}?> Loop </TITLE>
     </HEAD>
     <BODY onLoad="switch_image('')">
     <CENTER>
    <?php
    $currentTime = time();

$hour = date("H",$currentTime);
$minutes = date("i",$currentTime);
$seconds = date("s",$currentTime);

if($cycle == ""){
    if($hour >= 3 && $hour < 9){
	$cycle = "00";
    }elseif($hour >= 9 && $hour < 15){
	$cycle = "06";
    }elseif($hour >= 15 && $hour < 21){
	$cycle = "12";
    }else{
	$cycle = "18";
    }
}

print("<font color=red><b>Model</b></font>: \n");
$modelNumber = 0;
if($model == ""){ $model = "gfs"; }
for ($m = 0;$m<$numModels;$m++){
    
    if($model == $models[$m]){
	$modelNumber = $m;
	print(" <b>$models[$m]</b> \n");			
    }else{
	print("<a href=\"index.php?date=$date&cycle=$cycle&area=$area&model=$models[$m]&parm=$parm&vtime=$vtime&maxHour=$maxHour\">$models[$m]</a> \n");
    }
}

$model = $models[$modelNumber];
print("&nbsp;&nbsp;||&nbsp;&nbsp;<font color=red><b>Area</b></font>: \n");

if($area == ""){ $area = "carib"; }
$areaNumber = 0;
for ($a = 0;$a<$numAreas[$modelNumber];$a++){
    $areaString = $areas[$modelNumber][$a];
    if($area == $areas[$modelNumber][$a]){
	$areaNumber = $a;			
	print(" <b>$areaString</b> \n");
	
    }else{
	print("<a href=\"index.php?date=$date&cycle=$cycle&area=$areaString&model=$model&parm=$parm&vtime=$vtime&maxHour=$maxHour\">$areaString</a> \n");
    }
}
$area = $areas[$modelNumber][$areaNumber];

print("<br><font color=red><b>Plot Type</b></font>:&nbsp;&nbsp;|\n");
if($parm == ""){ $parm = "MSLP_Precip"; }
$parameterNumber = 0;
for ($p = 0;$p<$numParameters[$modelNumber];$p++){
    $parameterString = $parameterName[$modelNumber][$p];
    if($parm == $parameterName[$modelNumber][$p]){
	$parameterNumber = $p;
	print(" <b>$parameterString</b> |\n");
	
    }else{
	print("<a href=\"index.php?date=$date&cycle=$cycle&area=$area&model=$model&parm=$parameterString&vtime=$vtime&maxHour=$maxHour\">$parameterString</a> |\n");
    }
}
$parm = $parameterName[$modelNumber][$parameterNumber];


print("<br>\n");


print("<table><tr>\n");
if($vtime == ""){
    $numDays = 0;		
    if($handle = opendir('.')){
	while(false !== ($file = readdir($handle))){								
	    if(preg_match("/\d{8}/", $file)){									
		$directories[$numDays] = $file;
		$numDays++;					
	    }
	}
    }
    closedir($handle);
    sort($directories);
    
    ### Date pull down menu		
    print("<td valign =\"TOP\"><font color=red><b>Date</b></font>:</td><td><form method=\"POST\" name=\"dateselect\" action=\"index.php?date=$date&cycle=$cycle&area=$area&model=$model&parm=$parm&maxHour=$maxHour\">\n<select size=\"0\" name=\"date\" onchange=dateselect.submit()>\n");		
    if($date == ""){ $date = $directories[$numDays-1]; }
    for($i=$numDays-1;$i>=0;$i--){
	if($directories[$i] == $date){
	    $selected = " SELECTED";
	}else{
	    $selected = "";
	}
	print("<option value=\"$directories[$i]\"$selected>$directories[$i]</option>\n");
    }		
    print("</select></form></td><td valign =\"TOP\">@\n");	


    ### Run links
    foreach (array("00", "06", "12", "18") as $run){
	if($run == $cycle){
	    print(" <b>$run" . "Z</b> \n");
	}else{
	    print(" <a href=\"index.php?date=$date&cycle=$run&area=$area&model=$models[$modelNumber]&parm=$parm&maxHour=$maxHour\">$run" . "Z</a> \n");
	}
    }
    
}else{
    print("<td valign=\"TOP\"><a href=\"index.php?date=$date&cycle=$cycle&area=$area&model=$model&parm=$parm\">View a model run</a> ");
}
print("</td>\n");

?>	



    <?php
#### Get list of radar images in this directory
    if($maxHour == ""){
	$maxHour = 1000;
    }

if($vtime == ""){
    $imagePath = "$date/$cycle/$area/$model/$parm";
    $numimages = 0;
    $numhours = 0;
    if(file_exists($imagePath)){
	if($handle = opendir($imagePath)){
	    while(false !== ($file = readdir($handle))){								
		if(preg_match("/(\d\d\d)m?\.[gif|png]/", $file, $matches)){									
		    if($matches[1] <= $maxHour){						
			$radarimages[$numimages] = "$imagePath/$file";
			$numimages++;						
		    }
		    $imageHours[$numhours] = $matches[1];
		    $numhours++;
		}
		
	    }
	    closedir($handle);
	}
    }	
    
}else{	
    $numimages = 0;
    for($i=240;$i>=0;$i-=6){
	$imageDate = $vtime - $i*3600;
	$imageHour = sprintf("%03d",$i);

	$dateFolder = date("Ymd",$imageDate);
	$cycleFolder = date("H", $imageDate);
	$imagePath = "$dateFolder/$cycleFolder/$area/$model/$parm";
	if(file_exists($imagePath)){
	    if($handle = opendir($imagePath)){
		while(false !== ($file = readdir($handle))){
		    if(preg_match("/.*$imageHour.?\.[gif|png]/", $file)){
			$radarimages[$numimages] = "$imagePath/$file";
			$numimages++;
		    }
		}
		closedir($handle);
	    }
	}		
    }	
}
$size = getimagesize("$radarimages[0]");
#print("|$radarimages[0]|");
$height = $size[1] * $zoom;
$width = $size[0] * $zoom;



if($vtime == ""){
    print("<td valign =\"TOP\"><b><font color=red>through</b></font></td><td><form method=\"POST\" name=\"maxhourselect\" action=\"index.php?date=$date&cycle=$cycle&area=$area&model=$model&parm=$parm&vtime=$vtime\">\n<select size=\"0\" name=\"maxHour\" onchange=maxhourselect.submit()>\n");	
    for($i=0;$i<$numhours;$i++){
	if($imageHours[$i] == $maxHour || ($i == $numhours -1 && $maxHour >= $imageHours[$i])){
	    $selected = " SELECTED";
	}else{
	    $selected = "";
	}
	print("<option value=\"$imageHours[$i]\"$selected>$imageHours[$i] Hours</option>\n");				
    }
    print("</select></form></td>\n");
}

print("<td valign =\"TOP\"> || Show all forecasts verifying at:</td><td><form method=\"POST\" name=\"vtimeselect\" action=\"index.php?date=$date&cycle=$cycle&area=$area&model=$model&parm=$parm\">\n<select size=\"0\" name=\"vtime\" onchange=vtimeselect.submit()>\n");	
$cycleTime = $currentTime - 3600*($hour - $cycle) - 60*$minutes - $seconds;
if($vtime == ""){
    print("<option value=\"$vtimes\" SELECTED></option>\n");		
}
for($i=0;$i<=240;$i+=6){
    $vtimes = $cycleTime + 3600*$i;
    $humanReadable = date("H\z D M d",$vtimes);
    
    if($vtime == $vtimes){
	$selected = " SELECTED";
    }else{
	$selected = "";
    }
    print("<option value=\"$vtimes\"$selected>$humanReadable</option>\n");		
    
}
print("</select></form></td>\n");


print("</tr></table> \n");

if($numimages == 0 ){
    if($vtime == ""){
	print("<br><br><b>THIS MODEL RUN IS NOT AVAILABLE YET</b>");
    }else{
	print("<br><br><b>NO RUNS OF THE \"$model\" MODEL VERIFY AT THIS TIME</b>");
    }
    
    exit;
}
?>


<script language="Javascript">
// <!--
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
//          contact: xholecko@sgi.felk.cvut.cz
//          http://sgi.felk.cvut.cz/~xholecko
//
//============================================================
// Thanx to Karel & Martin for beta testing and suggestions!
//============================================================
//  New GUI Design by Brian Hughes, NOAA/NESDIS/SAB 12/17/99
//  Assorted hacks added by T. Spindler NHC/TPC 7/25/00
//============================================================

//********* SET UP VARIABLES *********************

image_name = "/storm_graphics/EP02/refresh/EP0205";
first_image = 1;
last_image = <?php print($numimages); ?>;
animation_height = 400;
animation_width = 500;
wind_value= 34;
 
//**************************************************************************
 
//=== THE CODE STARTS HERE - no need to change anything below ===
 
//=== global variables ====
theImages = new Array();      //holds the images
imageNum = new Array();       //keeps track of which images to omit from loop
normal_delay = 250;
delay = normal_delay;         //delay between frames in 1/100 seconds
delay_step = 25;
delay_max = 4000;
delay_min = 50;
dwell_multipler = 5;
dwell_step = 1;
end_dwell_multipler   = dwell_multipler;
start_dwell_multipler   = 1;
current_image = first_image;     //number of the current image
timeID = null;
status = 0;                      // 0-stopped, 1-playing
play_mode = 0;                   // 0-normal, 1-loop, 2-sweep
size_valid = 0;
num_loops = 0;			   // initializes loop number counter
 
//===> Make sure the first image number is not bigger than the last image number
if (first_image > last_image)
{
   var help = last_image;
   last_image = first_image;
   first_image = help;
}
 
//===> Preload the first image (while page is downloading)
   theImages[0] = new Image();
   theImages[0].src = "loading.gif";
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
   status = 0;
//   setTimeout("history.back()", 60000);	     //when stop function called, "kicksback" to previous document 
}						     //after 60 seconds
 
 
//===> Display animation in fwd direction in either loop or sweep mode
function animate_fwd()
{
   current_image += 1;                //increment image number
 
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
   if (current_image == 108) {
         current_image += 1;
   }
 
   document.animation.src = theImages[current_image].src;   //display image onto screen
   document.control_form.frame_nr.value = current_image;                //display image number

   delay_time = delay;
   if ( current_image == first_image) delay_time = start_dwell_multipler*delay;
   if (current_image == last_image)   delay_time = end_dwell_multipler*delay;
 
   //== call "animate_fwd()" again after a set time (delay_time) has elapsed ==
   timeID = setTimeout("animate_fwd()", delay_time);
}
 
 
//===> Display animation in reverse direction
function animate_rev()
{
   current_image -= 1;                      //decrement image number
 
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
   if (current_image == 108) {
         current_image -= 1;
   }
 
   document.animation.src = theImages[current_image].src;   //display image onto screen
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
   if (number == 108) {
         number += 1;
         if (number > last_image) number = first_image;
   }
 
   current_image = number;
   document.animation.src = theImages[current_image].src;   //display image
   document.control_form.frame_nr.value = current_image;                //display image number
}
 
//===> Decrement to next image
function decrementImage(number)
{
   stop();
 
   //== if image is first in loop, decrement to last image ==
   if (number < first_image) number = last_image;
 
   //== check to ensure that image has not been deselected from loop ==
   if (number == 108) {
         number -= 1;
   }
 
   current_image = number;
   document.animation.src = theImages[current_image].src;   //display image
   document.control_form.frame_nr.value = current_image;    //display image number
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
function rev()
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
function launch(image_type,wind_value)
{
   var numargs = launch.arguments.length;
   var i_name = "00";
   if (numargs == 1) image_type = "_sm2"; 



<?php	
	
	for ($i=1;$i<=$numimages;$i++){
		$j = $i -1;
		if($i == 0){
			$iname = "00";
		}else{
			$iname = "$i";
		}
		print(	"	
			i_name = $i;
			theImages[$i] = new Image();
      			theImages[$i].src = \"$radarimages[$j]\";
			imageNum[$i] = true;
			document.animation.src = theImages[$i].src;
			document.control_form.frame_nr.value = $i;"
      );
	}


?>

   
   if (image_type == "_sm2") shrinkImage();
   if (image_type == "") enlargeImage();
   
   // this needs to be done to set the right mode when the page is manually reloaded
   change_mode (1);	
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
 
//===> Reload graphics with new image_type
function switch_image(type)
{
  stop();
  launch(type,wind_value);
  fwd();
}

//===> Reload graphics with new image_type
function go2image(number)
{
   stop();
   current_image = number;
   document.animation.src = theImages[number].src;   //display image
   document.control_form.frame_nr.value = current_image;                //display image number
}
//===> resize graphic
function enlargeImage()
{
   document.animation.height="<?php print($height); ?>";
   document.animation.width="<?php print($width); ?>";
} 
function shrinkImage()
{
   document.animation.height="<?php print($height); ?>";
   document.animation.width="<?php print($width); ?>";
} 
// -->
</script>
<noscript>
<h4 align="center">

<hr noshade>
You must have Javascript enabled to view the loop animations.
<hr noshade>
</h4>
</noscript>



<table border="0" cellpadding="0" cellspacing="0"><tr valign="top" align="center"><td>
<form method="post" name="control_form">
<img name="animation" border="0" width="<?php print($width); ?>" height="<?php print($height); ?>" src="loading.gif"
alt="Loading Storm Graphics Loops">

<h4 style="width: 500">Image Number:
<input class="std" style="font-size: 14px; text-align: center;" type="text" name="frame_nr" value="9" size="2" onFocus="this.select()" onChange="go2image(this.value)"></input>
of <?php print($numimages); ?></h4></a>
</form>
</td><td>
<br><br><br><br><br><br><br>
<form>
<table border="1" cellpadding="2" cellspacing="2" width="0">

<tr align="center"><td>
<b>Advance One</b><br>
<input style="font-size: 11px" type="button" value=" < " onClick="decrementImage(current_image=current_image-1)">
<input style="font-size: 11px" type="button" value=" > " onClick="incrementImage(current_image=current_image+1)">
</td></tr>

<tr align="center"><td>
<b>Loop Images</b><br>
<input style="font-size: 11px" type="button" value="<<" onClick="change_mode(1);rev()">
<input style="font-size: 11px" type="button" value="Stop" onClick="stop()">
<input style="font-size: 11px" type="button" value=">>" onClick="change_mode(1);fwd()">
</td></tr>

<tr align="center"><td>
<b>Adjust Speed</b><br>
<input style="font-size: 11px" type="button" value="Slower" onClick="change_speed(delay_step)">
<input style="font-size: 11px" type="button" value="Faster" onClick="change_speed(-delay_step)">
</td></tr>



</table>
</form>
</td></tr></table>





     
     </td></tr><table>
     
     <CENTER>
<?php	
	#print(" <a href=\"index.php?name=$name&loop=0&zoom=$zoom\">|All|</a><br> ");
	
	#$factors=array(.25,.5,.75,1,1.5,2,3,5);
	#print("Zoom Factor: ");
	#foreach($factors as $zoomfactor){
	#	print(" <a href=\"index.php?name=$name&loop=$loop&zoom=$zoomfactor\">|$zoomfactor|</a> ");
	#}
	
?>
         
    
     </CENTER>
     </table>
     <HR>     
     </center>
     <i>The source imagery for this page is from <a href="http://www.nco.ncep.noaa.gov/pmb/nwprod/analysis/">NCEP Central Operations Model Analyses and Forecasts</a>. <br>
     For questions, comments, or suggestions regarding this page - contact <a href="mailto:Chris.Lauer@noaa.gov">Chris Lauer</a></i>
     </BODY>
     </HTML>
