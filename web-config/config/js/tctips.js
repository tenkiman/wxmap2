
/*
Please refer to readme.html for full Instructions

Text[...]=[title,text]

TC[...]=[title,text]

Style[...]=[TitleColor,       TextColor,          TitleBgColor,      TextBgColor,   TitleBgImag,
            TextBgImag,       TitleTextAlign,     TextTextAlign,     TitleFontFace, TextFontFace,
            TipPosition,      StickyStyle,        TitleFontSize,     TextFontSize,  Width,
            Height,           BorderSize,         PadTextArea,       CoordinateX ,  CoordinateY,
            TransitionNumber, TransitionDuration, TransparencyLevel ,ShadowType,    ShadowColor]

*/

var TC=[]
var MODEL=[]
var CLIMO=[]
var Style=[]
var Text=[]

var FiltersEnabled = 1 // if your not going to use transitions or filters in any of the tips set this to 0


Style[0]=["white","black","#000099","#E8E8FF","","","","","","","","","","",200,"",2,2,10,10,51,1,0,"",""]
Style[1]=["white","black","#000099","#E8E8FF","","","","","","","center","","","",200,"",2,2,10,10,"","","","",""]
Style[2]=["white","black","#000099","#E8E8FF","","","","","","","left","","","",200,"",2,2,10,10,"","","","",""]
Style[3]=["white","black","#000099","#E8E8FF","","","","","","","float","","","",200,"",2,2,10,10,"","","","",""]
Style[4]=["white","black","#000099","#E8E8FF","","","","","","","fixed","","","",200,"",2,2,1,1,"","","","",""]
Style[5]=["white","black","#000099","#E8E8FF","","","","","","","","sticky","","",200,"",2,2,10,10,"","","","",""]
Style[6]=["white","black","#000099","#E8E8FF","","","","","","","","keep","","",200,"",2,2,10,10,"","","","",""]
Style[7]=["white","black","#000099","#E8E8FF","","","","","","","","","","",200,"",2,2,40,10,"","","","",""]
Style[8]=["white","black","#000099","#E8E8FF","","","","","","","","","","",200,"",2,2,10,50,"","","","",""]
Style[9]=["white","black","#000099","#E8E8FF","","","","","","","","","","",200,"",2,2,10,10,51,0.5,75,"simple","gray"]
Style[10]=["white","black","black","white","","","right","","Impact","cursive","center","",3,5,200,150,5,20,10,0,50,1,80,"complex","gray"]
Style[11]=["white","black","#000099","#E8E8FF","","","","","","","","","","",200,"",2,2,10,10,51,0.5,45,"simple","gray"]

/*
 upamon styles
*/
Style[20]=["white","black","#000099","#E8E8FF","","","center","","","","","","","",300,"",2,2,10,10,"","","","",""]
Style[21]=["white","black","#000099","#E8E8FF","","","center","","","","","","","",150,"",2,2,10,-30,"","","","",""]
Style[22]=["white","white","#000099","red","","","center","center","","Verdana,Arial","","","",3,150,25,"","",10,-10,"","","","simple","gray"]
Style[23]=["white","black","#000099","white","","","center","","","","","","","",100,"",2,2,10,-30,"","","","",""]


Text[0]=["Me Email","Click here to send me an email "]
Text[1]=["Home Page","Click here to go to my Web site."]
Text[2]=["This is the title","Well How do you find this Tip message to be?"]
Text[3]=["Right","This tip Is right positioned"]
Text[4]=["Center","This tip Is center positioned"]
Text[5]=["Left","This tip Is left positioned"]
Text[6]=["Float","This tip Is float positioned at a (10,10) coordinate, It also \
floats with the scrollbars so it is always static"]
Text[7]=["Fixed","This tip Is fixed positioned at a (1,1) coordinate"]
Text[8]=["sticky style","This tip will sticky around<BR>This is useful when you want \
to insert a link like this <A href='http://migoicons.tripod.com'>Home Page</A>"]

Text[9]=["","uncorr ; 00-12 diurnal cycle"]
Text[10]=["","bias corr; 00-12 diurnal cycle"]
Text[11]=["Top coordinate control","This tip is right positioned with a 50 Y coordinate"]
Text[12]=["Visual effects","This tip has a Shadow and is Transparent a little and also has a random Transition applied to it "]
Text[13]=["different style","Wow this is a new style and position! "]
Text[14]=["Dirunal","difference between the 00Z and 12Z means"]
Text[15]=["","This is only text"]
Text[16]=["","Some Lists <li>list one</li> <li>list two</li> <li>list three</li> <li>list four</li>"]

/*
 help
*/

Text['help.veri']=["Help -- TC Veri Stats","Plots of TC Verification Stats<hr>\
the \"KEY\" link in the title above leads to a description of the verification plots<hr>\
mousing over the grey title buttons describes the clickable buttons below<hr>\
Plots are organized by: 1) basin; 2) Units; 3) Models; 4) statistics; 5) verification type; and 6) verification rules\
"]

Text['help.trk']=["Help -- TC track plots","Plots of model TC tracks/stats<hr>\
the \"KEY\" link in the title above leads to a description of the track plot and model stats<hr>\
Mousing over the grey title buttons describes the clickable buttons below<hr> \
Clicking on the image brings up the image in a separate window<hr> \
Plots for each TC (NNB where NN is storm number and B is basin) are organized by basin and model; if no plot is displayed, click on a different storm\
"]

/*
 verification plots
*/

Text[30]=["Verification Rule","<b>JTWC</b> - verify all positions in the best track file, \
including prewarning invest posits <hr>\
<b>NHC</b> - verify only forecasts where the initial and foreacst best track intensities \
are >= 35 kt (i.e., only TC >= tropical storms"]

Text[31]=["Verification Type",
"\
<b>Hetereo</b> - heterogenous verification (verify all forecasts) <hr> \
<b>Homo</b> - homogeneous or \"side-by-side\" comparison (verify forecasts only when both models are available)\
"]

Text[32]=["Statistic Type",
"\
<b>FE</b> - Forecast Error =  great circle distance between forecast and verifying position <hr> \
<b>POD</b> - Probability of Detection =  number of forecast / number of verifying posits [%] or the % time the model makes\
 a forecast; 100% means the model made a forecast for all possible best track verification times<hr>\
<b>% IMP CLP</b> - % FE improvement over the no-skill standard CLImatology and PERsistence (CLIPER) = \
(FE_CLIPER - FE_model/FE_CLIPER)*100 ; >0 means better than CLIPER (skill), <0 poorer than CLIPER (no skill)<hr>\
<b>VE + bias</b> - Mean Abs Vmax Error (VE) + Mean Vmax Error (bias)\
"]

Text[33]=["Model Comps",
"\
<center><b>model1</b> versus <b>model2</b><hr></center>\
<b>OFC</b> - Official Forecast (JTWC | NHC)<hr> \
<b>CLP</b> - CLImatology and PERsistence (CLIPER) (no-skill model)<hr> \
<b>GFS</b> - NCEP GFS (aka AVN) (T254 L68)<hr> \
<b>NGP</b> - FNMOC NOGAPS4.0 (T239 L30)<hr> \
<b>UKM</b> - UKMO UM (0.83x0.55 L38)<hr> \
<b>ECO</b> - ECMWF IFS (ops) (T<sub>Lf</sub>511 L60)<hr> \
<b>ECE</b> - ECMWF IFS (EPS) (T<sub>Lf</sub>255 L40)\
"]

Text[34]=["Units",
"\
<b>Nautical</b> - distance in nm (nautical miles) and speed in kt (knots = nm/hr)<hr> \
<b>Metric</b> - distance in km (kilometers) and speed in m/s (meters / second) \
"]

Text['nhem']=["Basin",
"\
<b>NHEM</b> - Entire northern Hemisphere <hr> \
<b>WPAC</b> - western North Pacific Ocean (\"W\" in ATCF)<hr> \
<b>EPAC</b> - eastern+central North Pacific Ocean (\"E/C\" in ATCF)<hr> \
<b>LANT</b> - north Atantic Ocean (\"L\" in ATCF)<hr> \
<b>NIO</b> - north Indian Ocean (Arabian Sea, Bay of Bengal) (\"A/B\" in ATCF)<hr> \
"]

Text['shem']=["Basin",
"\
<b>SHEM</b> - Entire southern Hemisphere <hr> \
<b>SWPAC</b> - southwest Pacific Ocean =  lon > 135E (eastern Australia ->, \"P\" in ATCF)<hr> \
<b>SIO</b> - south Indian Ocean =  lon < 135E (<- western Australia, \"S\" in ATCF<hr> \
<b>SLANT</b> - south Atlantic Ocean = (first well documenting TC) \"T\" (my ATCF code)\
"]

MODEL['desc']=["Models",
"\
<b>OFC</b> - Offical Forecast (JTWC | NHC)<hr> \
<b>CLP</b> - CLImatology and PERsistence (CLIPER) (no-skill model)<hr> \
<b>GFS</b> - NCEP GFS (aka AVN) (T254 L68)<hr> \
<b>NGP</b> - FNMOC NOGAPS4.0 (T239 L30)<hr> \
<b>UKM</b> - UKMO UM (0.83x0.55 L38)<hr> \
<b>ECO</b> - ECMWF IFS (ops) (T<sub>Lf</sub>511 L60)<hr> \
<b>ECE</b> - ECMWF IFS (EPS) (T<sub>Lf</sub>255 L40)\
<b>BTK</b> - Best Track\
"]


MODEL['ofc']=["Official Forecast",
"\
Warning Center Track Forecast<br>\
WESTPAC/SHEM = JTWC<br>\
EASTPAC/LANT = NHC<br>\
<br>\
"]

MODEL['clp']=["CLP - CLIPER",
"\
CLImatology - PERsistence statistical model\
<br>\
"]

MODEL['gfs']=["NCEP GFS",
"\
NCEP Global Forecast System (aka AVN)<br>\
four-times daily (00/06/12/18Z) global run <br>\
(T254 L68)<br>\
<br>\
"]

MODEL['ngp']=["FNMOC NOGAPS",
"\
FNMOC Navy Operational Global Atmospheric Prediction System<br>\
twice-daily (00/12Z) global run <br>\
[T239 L30]<br>\
<br>\
"]

MODEL['eco']=["ECMWF IFS (ops)",
"\
ECMWF Integrated Forecast System<br>\
twice-daily deterministic run<br>\
[T<sub>L</sub>511 L60]<br>\
<br>\
"]

MODEL['ece']=["ECMWF IFS (EPS)",
"\
ECMWF Integrated Forecast System<br>\
EPS - Ensemble Prediction System<br>\
twice-daily EPS control run (initialize with deterministic run analysis)<br>\
ensemble has 51-members<br>\
[T<sub>L</sub>255 L40]<br>\
<br>\
"]

MODEL['ukm']=["UK Met Office Unified Model",
"\
UKMO UM global configuration, new dynamics<br>\
[(0.83 (dlon) x 0.55 (dlat) L38)<br>\
<br>\
"]

MODEL['btk']=["Best Track",
"\
Current Operational Best Track<br>\
is rebested after seaseon<br>\
<br>\
"]


CLIMO['clm']=["CLIMO",
"\
<b>NCEP R1 Global Reanalysis</b><br>\
30-y<br>\
1970-200<br>\
Model: T62L28<br>\
"]

CLIMO['wxmap']=["WxMAP",
"\
return to main wxmap page<br>\
"]


CLIMO['mo.clm']=["WxMAP Mon Climo",
"\
go the monthly mean<br>\
wind climo <br>\
"]

CLIMO['cur.clm']=["WxMAP Cur Climo",
"\
go the current, real-time<br>\
wind climo <br>\
"]


CLIMO['clm-mod']=["MOD-CLM Loop",
"\
<b>Flicker between Climo and Model</b><br>\
"]


CLIMO['mod']=["MODEL",
"\
<b>Model 0-5 d Mean Flow</b><br>\
average tau 0-120 h<br>\
to represent lower freq<br>\
"]


CLIMO['ano']=["MODEL-CLIMO",
"\
<b>Anomaly or Departure of Model</b><br>\
from climatology<br>\
<br>\
"]


CLIMO['lm']=["Low-Mid layer",
"\
<b>Low-Mid Trop Flow</b><br>\
mass weighting of 850/700/500<br>\
<br>\
"]

CLIMO['shr']=["Shear",
"\
<b>200-850 mb Shear</b><br>\
shear magnitude < 30 kt in green<br>\
<br>\
"]

CLIMO['200']=["200 mb Level",
"\
<b>200 mb Wind</b><br>\
<br>\
"]

CLIMO['500']=["500 mb Level",
"\
<b>500 mb Wind</b><br>\
<br>\
"]

CLIMO['700']=["700 mb Level",
"\
<b>700 mb Wind</b><br>\
<br>\
"]

CLIMO['850']=["850 mb Level",
"\
<b>850 mb Wind</b><br>\
<br>\
"]

CLIMO['sfc']=["Sfc (10 m)",
"\
<b>Sfc Winds (10 m)</b><br>\
<br>\
"]

CLIMO['mjo.850']=["BOM Real-time MJO",
"\
MJO OLR and 850 mb u comp<br>\
anomaly<br>\
<br>\
"]



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  tooltip.js                                                                                          0100644 0000770 0000770 00000022455 10237777342 013031  0                                                                                                    ustar   fiorino                         fiorino                                                                                                                                                                                                                <!-- 
/*
 Pleas leave this notice.
 DHTML tip message version 1.2 copyright Essam Gamal 2003 (http://migoicons.tripod.com, migoicons@hotmail.com)
 All modifications are done in the style.js you should not modify this file.  Created on : 06/03/2003
 Script featured on and can be found at Dynamic Drive (http://www.dynamicdrive.com)
*/ 

var ua = navigator.userAgent
var ps = navigator.productSub 
var dom = (document.getElementById)? 1:0
var ie4 = (document.all&&!dom)? 1:0
var ie5 = (document.all&&dom)? 1:0
var nn4 =(navigator.appName.toLowerCase() == "netscape" && parseInt(navigator.appVersion) == 4)
var nn6 = (dom&&!ie5)? 1:0
var sNav = (nn4||nn6||ie4||ie5)? 1:0
var cssFilters = ((ua.indexOf("MSIE 5.5")>=0||ua.indexOf("MSIE 6")>=0)&&ua.indexOf("Opera")<0)? 1:0
var Style=[],Text=[],Count=0,sbw=0,move=0,hs="",mx,my,scl,sct,ww,wh,obj,sl,st,ih,iw,vl,hl,sv,evlh,evlw,tbody
var HideTip = "eval(obj+sv+hl+';'+obj+sl+'=0;'+obj+st+'=-800')"
var doc_root = ((ie5&&ua.indexOf("Opera")<0||ie4)&&document.compatMode=="CSS1Compat")? "document.documentElement":"document.body"
var PX = (nn6)? "px" :"" 

if(sNav) {
	window.onresize = ReloadTip
	document.onmousemove = MoveTip
	if(nn4) document.captureEvents(Event.MOUSEMOVE) 
}	
if(nn4||nn6) {
	mx = "e.pageX"
	my = "e.pageY"
	scl = "window.pageXOffset"
	sct = "window.pageYOffset"	
	if(nn4) {
		obj = "document.TipLayer."
		sl = "left"
		st = "top"
		ih = "clip.height"
		iw = "clip.width"
		vl = "'show'"
		hl = "'hide'"
		sv = "visibility="
	}
	else obj = "document.getElementById('TipLayer')."
} 
if(ie4||ie5) {
	obj = "TipLayer."
	mx = "event.x"
	my = "event.y"
	scl = "eval(doc_root).scrollLeft"
	sct = "eval(doc_root).scrollTop"
	if(ie5) {
		mx = mx+"+"+scl 
		my = my+"+"+sct
	}
}
if(ie4||dom){
	sl = "style.left"
	st = "style.top"
	ih = "offsetHeight"
	iw = "offsetWidth"
	vl = "'visible'"
	hl = "'hidden'"
	sv = "style.visibility="
}
if(ie4||ie5||ps>=20020823) {
	ww = "eval(doc_root).clientWidth"
	wh = "eval(doc_root).clientHeight"
}	 
else { 
	ww = "window.innerWidth"
	wh = "window.innerHeight"
	evlh = eval(wh)
	evlw = eval(ww)
	sbw=15
}	

function applyCssFilter(){
	if(cssFilters&&FiltersEnabled) { 
		var dx = " progid:DXImageTransform.Microsoft."
		TipLayer.style.filter = "revealTrans()"+dx+"Fade(Overlap=1.00 enabled=0)"+dx+"Inset(enabled=0)"+dx+"Iris(irisstyle=PLUS,motion=in enabled=0)"+dx+"Iris(irisstyle=PLUS,motion=out enabled=0)"+dx+"Iris(irisstyle=DIAMOND,motion=in enabled=0)"+dx+"Iris(irisstyle=DIAMOND,motion=out enabled=0)"+dx+"Iris(irisstyle=CROSS,motion=in enabled=0)"+dx+"Iris(irisstyle=CROSS,motion=out enabled=0)"+dx+"Iris(irisstyle=STAR,motion=in enabled=0)"+dx+"Iris(irisstyle=STAR,motion=out enabled=0)"+dx+"RadialWipe(wipestyle=CLOCK enabled=0)"+dx+"RadialWipe(wipestyle=WEDGE enabled=0)"+dx+"RadialWipe(wipestyle=RADIAL enabled=0)"+dx+"Pixelate(MaxSquare=35,enabled=0)"+dx+"Slide(slidestyle=HIDE,Bands=25 enabled=0)"+dx+"Slide(slidestyle=PUSH,Bands=25 enabled=0)"+dx+"Slide(slidestyle=SWAP,Bands=25 enabled=0)"+dx+"Spiral(GridSizeX=16,GridSizeY=16 enabled=0)"+dx+"Stretch(stretchstyle=HIDE enabled=0)"+dx+"Stretch(stretchstyle=PUSH enabled=0)"+dx+"Stretch(stretchstyle=SPIN enabled=0)"+dx+"Wheel(spokes=16 enabled=0)"+dx+"GradientWipe(GradientSize=1.00,wipestyle=0,motion=forward enabled=0)"+dx+"GradientWipe(GradientSize=1.00,wipestyle=0,motion=reverse enabled=0)"+dx+"GradientWipe(GradientSize=1.00,wipestyle=1,motion=forward enabled=0)"+dx+"GradientWipe(GradientSize=1.00,wipestyle=1,motion=reverse enabled=0)"+dx+"Zigzag(GridSizeX=8,GridSizeY=8 enabled=0)"+dx+"Alpha(enabled=0)"+dx+"Dropshadow(OffX=3,OffY=3,Positive=true,enabled=0)"+dx+"Shadow(strength=3,direction=135,enabled=0)"
	}
}

function stm(t,s) {
  if(sNav) {
  	if(t.length<2||s.length<25) {
		var ErrorNotice = "DHTML TIP MESSAGE VERSION 1.2 ERROR NOTICE.\n"
		if(t.length<2&&s.length<25) alert(ErrorNotice+"It looks like you removed an entry or more from the Style Array and Text Array of this tip.\nTheir should be 25 entries in every Style Array even though empty and 2 in every Text Array. You defined only "+s.length+" entries in the Style Array and "+t.length+" entry in the Text Array. This tip won't be viewed to avoid errors")
		else if(t.length<2) alert(ErrorNotice+"It looks like you removed an entry or more from the Text Array of this tip.\nTheir should be 2 entries in every Text Array. You defined only "+t.length+" entry. This tip won't be viewed to avoid errors.")
		else if(s.length<25) alert(ErrorNotice+"It looks like you removed an entry or more from the Style Array of this tip.\nTheir should be 25 entries in every Style Array even though empty. You defined only "+s.length+" entries. This tip won't be viewed to avoid errors.")
 	}
  	else {
		var ab = "" ;var ap = ""
		var titCol = (s[0])? "COLOR='"+s[0]+"'" : ""
		var txtCol = (s[1])? "COLOR='"+s[1]+"'" : ""
		var titBgCol = (s[2])? "BGCOLOR='"+s[2]+"'" : ""
		var txtBgCol = (s[3])? "BGCOLOR='"+s[3]+"'" : ""
		var titBgImg = (s[4])? "BACKGROUND='"+s[4]+"'" : ""	
		var txtBgImg = (s[5])? "BACKGROUND='"+s[5]+"'" : ""
		var titTxtAli = (s[6] && s[6].toLowerCase()!="left")? "ALIGN='"+s[6]+"'" : ""
		var txtTxtAli = (s[7] && s[7].toLowerCase()!="left")? "ALIGN='"+s[7]+"'" : ""   
		var add_height = (s[15])? "HEIGHT='"+s[15]+"'" : ""
		if(!s[8])  s[8] = "Verdana,Arial,Helvetica"
		if(!s[9])  s[9] = "Verdana,Arial,Helvetica"					
		if(!s[12]) s[12] = 1
		if(!s[13]) s[13] = 1
		if(!s[14]) s[14] = 200
		if(!s[16]) s[16] = 0
		if(!s[17]) s[17] = 0
		if(!s[18]) s[18] = 10
		if(!s[19]) s[19] = 10
		hs = s[11].toLowerCase() 
		if(ps==20001108){
		if(s[2]) ab="STYLE='border:"+s[16]+"px solid"+" "+s[2]+"'"
		ap="STYLE='padding:"+s[17]+"px "+s[17]+"px "+s[17]+"px "+s[17]+"px'"}
		var closeLink=(hs=="sticky")? "<TD ALIGN='right'><FONT SIZE='"+s[12]+"' FACE='"+s[8]+"'><A HREF='javascript:void(0)' ONCLICK='stickyhide()' STYLE='text-decoration:none;color:"+s[0]+"'><B>Close</B></A></FONT></TD>":""
		var title=(t[0]||hs=="sticky")? "<TABLE WIDTH='100%' BORDER='0' CELLPADDING='0' CELLSPACING='0'><TR><TD "+titTxtAli+"><FONT SIZE='"+s[12]+"' FACE='"+s[8]+"' "+titCol+"><B>"+t[0]+"</B></FONT></TD>"+closeLink+"</TR></TABLE>" : ""
		var txt="<TABLE "+titBgImg+" "+ab+" WIDTH='"+s[14]+"' BORDER='0' CELLPADDING='"+s[16]+"' CELLSPACING='0' "+titBgCol+" ><TR><TD>"+title+"<TABLE WIDTH='100%' "+add_height+" BORDER='0' CELLPADDING='"+s[17]+"' CELLSPACING='0' "+txtBgCol+" "+txtBgImg+"><TR><TD "+txtTxtAli+" "+ap+" VALIGN='top'><FONT SIZE='"+s[13]+"' FACE='"+s[9]+"' "+txtCol +">"+t[1]+"</FONT></TD></TR></TABLE></TD></TR></TABLE>"
		if(nn4) {
			with(eval(obj+"document")) {
				open()
				write(txt)
				close()
			}
		}
		else eval(obj+"innerHTML=txt")
		tbody = {
			Pos:s[10].toLowerCase(), 
			Xpos:s[18],
			Ypos:s[19], 
			Transition:s[20],
			Duration:s[21], 
			Alpha:s[22],
			ShadowType:s[23].toLowerCase(),
			ShadowColor:s[24],
			Width:parseInt(eval(obj+iw)+3+sbw)
		}
		if(ie4) { 
			TipLayer.style.width = s[14]
	 		tbody.Width = s[14]
		}
		Count=0	
		move=1
 	 }
  }
}

function MoveTip(e) {
	if(move) {
		var X,Y,MouseX = eval(mx),MouseY = eval(my); tbody.Height = parseInt(eval(obj+ih)+3)
		tbody.wiw = parseInt(eval(ww+"+"+scl)); tbody.wih = parseInt(eval(wh+"+"+sct))
		switch(tbody.Pos) {
			case "left" : X=MouseX-tbody.Width-tbody.Xpos; Y=MouseY+tbody.Ypos; break
			case "center": X=MouseX-(tbody.Width/2); Y=MouseY+tbody.Ypos; break
			case "float": X=tbody.Xpos+eval(scl); Y=tbody.Ypos+eval(sct); break	
			case "fixed": X=tbody.Xpos; Y=tbody.Ypos; break		
			default: X=MouseX+tbody.Xpos; Y=MouseY+tbody.Ypos
		}

		if(tbody.wiw<tbody.Width+X) X = tbody.wiw-tbody.Width
		if(tbody.wih<tbody.Height+Y+sbw) {
			if(tbody.Pos=="float"||tbody.Pos=="fixed") Y = tbody.wih-tbody.Height-sbw
			else Y = MouseY-tbody.Height
		}
		if(X<0) X=0 
		eval(obj+sl+"=X+PX;"+obj+st+"=Y+PX")
		ViewTip()
	}
}

function ViewTip() {
  	Count++
	if(Count == 1) {
		if(cssFilters&&FiltersEnabled) {	
			for(Index=28; Index<31; Index++) { TipLayer.filters[Index].enabled = 0 }
			for(s=0; s<28; s++) { if(TipLayer.filters[s].status == 2) TipLayer.filters[s].stop() }
			if(tbody.Transition == 51) tbody.Transition = parseInt(Math.random()*50)
			var applyTrans = (tbody.Transition>-1&&tbody.Transition<24&&tbody.Duration>0)? 1:0
			var advFilters = (tbody.Transition>23&&tbody.Transition<51&&tbody.Duration>0)? 1:0
			var which = (applyTrans)?0:(advFilters)? tbody.Transition-23:0 
			if(tbody.Alpha>0&&tbody.Alpha<100) {
	  			TipLayer.filters[28].enabled = 1
	  			TipLayer.filters[28].opacity = tbody.Alpha
			}
			if(tbody.ShadowColor&&tbody.ShadowType == "simple") {
	  			TipLayer.filters[29].enabled = 1
	  			TipLayer.filters[29].color = tbody.ShadowColor
			}
			else if(tbody.ShadowColor&&tbody.ShadowType == "complex") {
	  			TipLayer.filters[30].enabled = 1
	  			TipLayer.filters[30].color = tbody.ShadowColor
			}
			if(applyTrans||advFilters) {
				eval(obj+sv+hl)
	  			if(applyTrans) TipLayer.filters[0].transition = tbody.Transition
	  			TipLayer.filters[which].duration = tbody.Duration 
	  			TipLayer.filters[which].apply()
			}
		}
 		eval(obj+sv+vl)
		if(cssFilters&&FiltersEnabled&&(applyTrans||advFilters)) TipLayer.filters[which].play()
		if(hs == "sticky") move=0
  	}
}

function stickyhide() {
	eval(HideTip)
}

function ReloadTip() {
	 if(nn4&&(evlw!=eval(ww)||evlh!=eval(wh))) location.reload()
	 else if(hs == "sticky") eval(HideTip)
}

function htm() {
	if(sNav) {
		if(hs!="keep") {
			move=0; 
			if(hs!="sticky") eval(HideTip)
		}	
	} 
}


//-->

                                                                                                                                                                                                                   wxmain.js                                                                                           0100644 0000770 0000770 00000021004 10421231260 012602  0                                                                                                    ustar   fiorino                         fiorino                                                                                                                                                                                                                mainpage='/work/wxmap2/web';
mainpage2='file:///work/wxmap2/web';
clmroot=mainpage + '/clm' 
htype='main';
area='tropwpac';

model="gfs";
dtg="2005051212";

dtype="clm";
plevel="200";
ptype="loop";
plot='uas';
tau='000';

yyyy_basin='2005.nhem';

opentype='local';

function swap() 
{

if(model == 'gfs') {
  plotdir="../plt_ncep_gfs";
} else if (model == 'ngp') {
  plotdir="../plt_fnmoc_ngp";
} else if (model == 'ukm') {
  plotdir="../plt_ukmo_ukm";
}

value=plotdir + "/" + dtg + "/" + model + "." + dtype + "." + plevel + "." + dtg + "." + ptype + ".png";
valueloop=value;
if(ptype == 'loop') {
  valueloop= plotdir + "/" + dtg + "/" + model + "." + dtype + "." + plevel + "." + dtg + "." + ptype + ".gif";
  value=valueloop;
}

myUrl=valueloop;
if (value != '') if (document.images) {
  document.images.myImage.src = valueloop;
  document.images.myImage.alt = valueloop;
  var el=document.images.myImage;
  while(el.nodeName.toLowerCase() != 'a') {
    el=el.parentNode;
    el.setAttribute('href',myUrl);
  }
}
//alert(value);
}

function swaphtm() 



{
  if(htype == 'main') {
    value='/wxmap';
  } else if (htype == 'wxmap.home.old') {
    value=mainpage+'/' + 'wx.old.' + dtg + '.htm';
  } else if (htype == 'wxmap.archive') {
    value=mainpage+'/' + 'wxmap.web.archive.htm';
  } else if (htype == 'wxmap.fnmoc') {
    value='https://www.fnmoc.navy.mil/PUBLIC/WXMAP/';
  } else if (htype == 'wxmap.cola') {
    value='http://wxmaps.org/pix/forecasts.html';	
  } else if (htype == 'wxmap.pzal') {
    value='https://pzal.npmoc.navy.mil/wxmap/';	

  } else if (htype == 'ncep.model.veri') {
    value='http://wwwt.emc.ncep.noaa.gov/gmb/STATS/STATS.html';	

  } else if (htype == 'tc.model.veri.stat') {
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.veri.stat.' + yyyy_basin + '.htm';	

  } else if (htype == 'tc.model.veri.trk') {
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.trk.' + yyyy_basin + '.htm';	

  } else if (htype == 'tc.act.llmap') {
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.act.climo.llmap.' + yyyy_basin + '.htm';	

  } else if (htype == 'cires.tcgen.fcst') {
    value='http://cires.colorado.edu/~rpaul/genesis/tcgenforecast.html';	

  } else if (htype == 'atcf.carq') {
    value='http://www.nrlmry.navy.mil/atcf_web/index1.html';	

  } else if (htype == 'fnmoc.tc.posit') {
    value='https://www.fnmoc.navy.mil/products/TAPPS/tc_info.html';	

  } else if (htype == 'ecmwf.72.wpac') {
    value='http://www.ecmwf.int/products/forecasts/d/charts/medium/deterministic/msl_uv850_z500!Wind%20850%20and%20mslp!72!Asia!pop!od!oper!public_plots!/';	

  } else if (htype == 'ecmwf.72.na') {
    value='http://www.ecmwf.int/products/forecasts/d/charts/medium/deterministic/msl_uv850_z500!Wind%20850%20and%20mslp!72!North%20America!pop!od!oper!public_plots!/';	

  } else if (htype == 'mo.clm') {
    value=clmroot+'/' + 'monthly/wx.clm.mo.htm';
  } else if (htype == 'cur.clm') {
    value=clmroot+'/' + 'wx.clm.cur.htm';
  } else if (htype == 'cpc.mjo.anim') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/ir_anim_monthly.html';
  } else if (htype == 'cpc.mjo.disc') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjoupdate.ppt';
  } else if (htype == 'cpc.mjo.fcst') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjo_chi.shtml';

  } else if (htype == 'area') {
    value=mainpage+'/' + model + '.' + area + '.' + dtg + '.htm';
  } else if (htype == 'arealoop') {
    value=mainpage+'/' + model + '/' + dtg + '/' + model + '.movie.' + plot + '.' + area + '.htm';
  } else if (htype == 'areatau0') {
    value=mainpage+'/' + model + '/' + dtg + '/' + model + '.' + plot + '.000.' + area + '.htm';
  } else if (htype == 'areaallmap') {
    value=mainpage+'/' + model + '/' + dtg + '/' + model + '.allmap.' + tau + '.' + area + '.htm';
  } else if (htype == 'areasst') {
    value=mainpage+'/' + model + '/' + dtg + '/' + 'ngp.sst.000.' + area + '.htm';
  } else if (htype == 'areacur') {
    value=mainpage+'/' + model + '.' + area + '.htm';
  } else if (htype == 'mjo.850') {
    value='http://www.bom.gov.au/bmrc/clfor/cfstaff/matw/maproom/RMM/hov.recon.olr.u850.gif';

  } else if (htype == 'jaawin.wv.w' && (area == 'tropwpac') ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?JGMSWV01_L,24'	
  } else if (htype == 'jaawin.wv.e' && (area == 'tropwpac') ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?NGMSWV01_L,24'	
  } else if (htype == 'jaawin.wv' && (area == 'tropwpac') ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?CPACWV01_L,12';	

  } else if (htype == 'jaawin.wv.w' && (area == 'troplant') ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?CGO8WV01_L,24'	
  } else if (htype == 'jaawin.ir.e' && (area == 'troplant') ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?MGO8IR01_L,24'	
  } else if (htype == 'jaawin.wv' && (area == 'troplant') ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?CATLWV01_L,12';	


  } else if (htype == 'jaawin.wv' && (area == 'tropepac') ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?CTAMWV01_L,12';	
  } else if (htype == 'jaawin.wv' && ( area == 'tropsio' || area == 'tropnio' ) ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?IOM5WV01_L,24';	

  } else if (htype == 'jaawin.wv' && ( area == 'tropswpac') ) {
    value='https://weather.afwa.af.mil/cgi-bin/sat_loop.cgi?AGM5WV02_L,24';

  } else if (htype == 'cimssup' && area == 'tropwpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmswv.html';
  } else if (htype == 'cimssvort' && area == 'tropwpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmsvor.html';
  } else if (htype == 'cimssshr' && area == 'tropwpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmsshr.html';

  } else if (htype == 'cimssup' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9wvir.html';
  } else if (htype == 'cimssvort' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9vor.html';
  } else if (htype == 'cimssshr' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9shr.html';

  } else if (htype == 'cimssup' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8wvir.html';
  } else if (htype == 'cimssvort' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8vor4.html';
  } else if (htype == 'cimssshr' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8shr.html';

  } else if (htype == 'cimssup' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5wv.html';
  } else if (htype == 'cimssvort' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5vor.html';
  } else if (htype == 'cimssshr' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5shr.html';

  } else if (htype == 'cimssup' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmswvs3.html';
  } else if (htype == 'cimssvort' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsvore.html';
  } else if (htype == 'cimssshr' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsshSE.html';

  } else if (htype == 'nhc.home') {
    value='http://www.nhc.noaa.gov/';

  } else if (htype == 'nhc.tafb.epac') {
    value='http://www.nhc.noaa.gov/tafb-pac.shtml';

  } else if (htype == 'jtwc.home') {
    value='https://metoc.npmoc.navy.mil/jtwc.html';
  } else if (htype == 'jtwc.tdo.ref') {
    value='https://pzal.npmoc.navy.mil/training/tdo/top21/TDOPAGE21.html';

  } else if (htype == 'fnmoc.tc') {
    value='http://152.80.49.216/tc-bin/tc_home.cgi';
  } else if (htype == 'fnmoc.qs') {
    value='https://www.fnmoc.navy.mil/CGI/scat.cgi/plot=scat/parentime=current/';

  } else if (htype == 'nrl.tc') {
    value='http://www.nrlmry.navy.mil/tc_pages/tc_home.html';

  } else {
    value=mainpage+'/' + model + '.' + area + '.' + dtg + '.htm';
  }

  if(opentype == 'window') {
      window.open(value);
      opentype='internal';
  } else if (opentype == 'page') {
      parent.location.href=cvalue;
      opentype='internal';
  } else {   
      parent.location.href=value;
  }

//alert(value);
}

//http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5wv.html
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            wz_tooltip.js                                                                                       0100644 0000770 0000770 00000036312 10237777414 013546  0                                                                                                    ustar   fiorino                         fiorino                                                                                                                                                                                                                
/* This notice must be untouched at all times.

wz_tooltip.js    v. 3.26

The latest version is available at
http://www.walterzorn.com
or http://www.devira.com
or http://www.walterzorn.de

Copyright (c) 2002-2004 Walter Zorn. All rights reserved.
Created 1. 12. 2002 by Walter Zorn (Web: http://www.walterzorn.com )
Last modified: 10. 10. 2004

Cross-browser tooltips working even in Opera 5 and 6,
as well as in NN 4, Gecko-Browsers, IE4+, Opera 7 and Konqueror.
No onmouseouts required.
Appearance of tooltips can be individually configured
via commands within the onmouseovers.

LICENSE: LGPL

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License (LGPL) as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

For more details on the GNU Lesser General Public License,
see http://www.gnu.org/copyleft/lesser.html
*/



////////////////  GLOBAL TOOPTIP CONFIGURATION  /////////////////////
var ttBgColor      = "#e6ecff";
var ttBgImg        = "";           // path to background image;
var ttBorderColor  = "#003399";
var ttBorderWidth  = 1;
var ttDelay        = 500;          // time span until tooltip shows up [milliseconds]
var ttFontColor    = "#000066";
var ttFontFace     = "arial,helvetica,sans-serif";
var ttFontSize     = "11px";
var ttFontWeight   = "normal";     // alternative is "bold";
var ttOffsetX      = 8;            // horizontal offset of left-top corner from mousepointer
var ttOffsetY      = 19;           // vertical offset                   "
var ttPadding      = 3;            // spacing between border and content
var ttShadowColor  = "";
var ttShadowWidth  = 0;
var ttTemp         = 0;            // time span after which the tooltip disappears; 0 (zero) means "infinite timespan"
var ttTitleColor   = "#ffffff";    // color of caption text
var ttWidth        = 300;
////////////////////  END OF TOOLTIP CONFIG  ////////////////////////



//////////////  TAGS WITH TOOLTIP FUNCTIONALITY  ////////////////////
// List may be extended or shortened:
var tt_tags = new Array("a","area","b","big","caption","center","code","dd","div","dl","dt","em","h1","h2","h3","h4","h5","h6","i","img","input","li","map","ol","p","pre","s","small","span","strike","strong","sub","sup","table","td","th","tr","tt","u","var","ul","layer");
/////////////////////////////////////////////////////////////////////



///////// DON'T CHANGE ANYTHING BELOW THIS LINE /////////////////////
var tt_obj,                // current tooltip
tt_objW = 0, tt_objH = 0,  // width and height of tt_obj
tt_objX = 0, tt_objY = 0,
tt_offX = 0, tt_offY = 0,
xlim = 0, ylim = 0,        // right and bottom borders of visible client area
tt_above = false,          // true if T_ABOVE cmd
tt_sticky = false,         // tt_obj sticky?
tt_wait = false,
tt_vis = false,            // tooltip visibility flag
tt_dwn = false,            // true while tooltip below mousepointer
tt_u = "undefined",
tt_inputs = new Array();   // drop-down-boxes to be hidden in IE


var tt_db = (document.compatMode && document.compatMode != "BackCompat")? document.documentElement : document.body? document.body : null,
tt_n = navigator.userAgent.toLowerCase();

// Browser flags
var tt_op = !!(window.opera && document.getElementById),
tt_op6 = tt_op && !document.defaultView,
tt_ie = tt_n.indexOf("msie") != -1 && document.all && tt_db && !tt_op,
tt_n4 = (document.layers && typeof document.classes != "undefined"),
tt_n6 = (!tt_op && document.defaultView && typeof document.defaultView.getComputedStyle != "undefined"),
tt_w3c = !tt_ie && !tt_n6 && !tt_op && document.getElementById;

tt_n = "";


function tt_Int(t_x)
{
	var t_y;
	return isNaN(t_y = parseInt(t_x))? 0 : t_y;
}

function wzReplace(t_x, t_y)
{
	var t_ret = "",
	t_str = this,
	t_xI;
	while ((t_xI = t_str.indexOf(t_x)) != -1)
	{
		t_ret += t_str.substring(0, t_xI) + t_y;
		t_str = t_str.substring(t_xI + t_x.length);
	}
	return t_ret+t_str;
}
String.prototype.wzReplace = wzReplace;

function tt_N4Tags(tagtyp, t_d, t_y)
{
	t_d = t_d || document;
	t_y = t_y || new Array();
	var t_x = (tagtyp=="a")? t_d.links : t_d.layers;
	for (var z = t_x.length; z--;) t_y[t_y.length] = t_x[z];
	for (var z = t_d.layers.length; z--;) t_y = tt_N4Tags(tagtyp, t_d.layers[z].document, t_y);
	return t_y;
}

function tt_GetSelects()
{
	if (!tt_op6 && !tt_ie) return;
	var t_s = tt_op6? "input" : "select";
	if (document.all)
	{
		var t_i = document.all.tags(t_s).length; while (t_i--)
			tt_inputs[t_i] = document.all.tags(t_s)[t_i];
	}
	else if (document.getElementsByTagName)
	{
		var t_i = document.getElementsByTagName(t_s).length; while (t_i--)
			tt_inputs[t_i] = document.getElementsByTagName(t_s)[t_i];
	}
	var t_i = tt_inputs.length; while (t_i--)
	{
		tt_inputs[t_i].x = 0;
		tt_inputs[t_i].y = 0;
		var t_o = tt_inputs[t_i];
		while (t_o)
		{
			tt_inputs[t_i].x += t_o.offsetLeft || 0;
			tt_inputs[t_i].y += t_o.offsetTop|| 0;
			t_o = t_o.offsetParent;
		}
	}
}

function tt_Htm(tt, t_id, txt)
{
	var t_bgc = (typeof tt.T_BGCOLOR != tt_u)? tt.T_BGCOLOR : ttBgColor,
	t_bgimg   = (typeof tt.T_BGIMG != tt_u)? tt.T_BGIMG : ttBgImg,
	t_bc      = (typeof tt.T_BORDERCOLOR != tt_u)? tt.T_BORDERCOLOR : ttBorderColor,
	t_bw      = (typeof tt.T_BORDERWIDTH != tt_u)? tt.T_BORDERWIDTH : ttBorderWidth,
	t_ff      = (typeof tt.T_FONTFACE != tt_u)? tt.T_FONTFACE : ttFontFace,
	t_fc      = (typeof tt.T_FONTCOLOR != tt_u)? tt.T_FONTCOLOR : ttFontColor,
	t_fsz     = (typeof tt.T_FONTSIZE != tt_u)? tt.T_FONTSIZE : ttFontSize,
	t_fwght   = (typeof tt.T_FONTWEIGHT != tt_u)? tt.T_FONTWEIGHT : ttFontWeight,
	t_padd    = (typeof tt.T_PADDING != tt_u)? tt.T_PADDING : ttPadding,
	t_shc     = (typeof tt.T_SHADOWCOLOR != tt_u)? tt.T_SHADOWCOLOR : (ttShadowColor || 0),
	t_shw     = (typeof tt.T_SHADOWWIDTH != tt_u)? tt.T_SHADOWWIDTH : (ttShadowWidth || 0),
	t_tit     = (typeof tt.T_TITLE != tt_u)? tt.T_TITLE : "",
	t_titc    = (typeof tt.T_TITLECOLOR != tt_u)? tt.T_TITLECOLOR : ttTitleColor,
	t_w       = (typeof tt.T_WIDTH != tt_u)? tt.T_WIDTH  : ttWidth;
	if (t_shc || t_shw)
	{
		t_shc = t_shc || "#cccccc";
		t_shw = t_shw || 3;
	}
	if (tt_n4 && (t_fsz == "10px" || t_fsz == "11px")) t_fsz = "12px";


	var t_y = '<div id="' + t_id + '" style="position:absolute;z-index:1010;';
	t_y += 'left:0px;top:0px;width:' + (t_w+t_shw) + 'px;visibility:' + (tt_n4? 'hide' : 'hidden') + ';">';
	t_y += '<table border="0" cellpadding="0" cellspacing="0"' + (t_bc? (' bgcolor="' + t_bc + '"') : '') + ' width="' + t_w + '">';
	if (t_tit)
	{
		t_y += '<tr><td style="padding-left:3px;"><font color="' + t_titc + '" face="' + t_ff + '" ';
		t_y += 'style="color:' + t_titc + ';font-family:' + t_ff + ';font-size:' + t_fsz + ';"><b>';
		t_y += (tt_n4? '&nbsp;' : '') + t_tit + '<\/b><\/font><\/td><\/tr>';
	}
	t_y += '<tr><td><table border="0" cellpadding="' + t_padd + '" cellspacing="' + t_bw + '" width="100%">';
	t_y += '<tr><td' + (t_bgc? (' bgcolor="' + t_bgc + '"') : '') + (t_bgimg? ' background="' + t_bgimg + '"' : '');
	if (tt_n6) t_y += ' style="padding:' + t_padd + 'px;"';
	t_y += '><font color="' + t_fc + '" face="' + t_ff + '"';
	t_y += ' style="color:' + t_fc + ';font-family:' + t_ff + ';font-size:' + t_fsz + ';font-weight:' + t_fwght + ';">';
	if (t_fwght == 'bold') t_y += '<b>';
	t_y += txt;
	if (t_fwght == 'bold') t_y += '<\/b>';
	t_y += '<\/font><\/td><\/tr><\/table><\/td><\/tr><\/table>';
	if (t_shw)
	{
		var t_spct = Math.round(t_shw*1.3);
		if (tt_n4)
		{
			t_y += '<layer bgcolor="' + t_shc + '" left="' + t_w + '" top="' + t_spct + '" width="' + t_shw + '" height="0"><\/layer>';
			t_y += '<layer bgcolor="' + t_shc + '" left="' + t_spct + '" align="bottom" width="' + (t_w-t_spct) + '" height="' + t_shw + '"><\/layer>';
		}
		else
		{
			var t_opa = tt_n6? '-moz-opacity:0.85;' : tt_ie? 'filter:Alpha(opacity=85);' : '';
			t_y += '<div id="' + t_id + 'R" style="position:absolute;background:' + t_shc + ';left:' + t_w + 'px;top:' + t_spct + 'px;width:' + t_shw + 'px;height:1px;overflow:hidden;' + t_opa + '"><\/div>';
			t_y += '<div style="position:relative;background:' + t_shc + ';left:' + t_spct + 'px;top:0px;width:' + (t_w-t_spct) + 'px;height:' + t_shw + 'px;overflow:hidden;' + t_opa + '"><\/div>';
		}
	}
	t_y += '<\/div>';
	return t_y;
}

function tt_Init()
{
	if (!(tt_op || tt_n4 || tt_n6 || tt_ie || tt_w3c)) return;

	var htm = tt_n4? '<div style="position:absolute;"><\/div>' : '',
	tags,
	t_tj,
	over,
	esc = 'return escape(';
	var i = tt_tags.length; while (i--)
	{
		tags = tt_ie? (document.all.tags(tt_tags[i]) || 1)
			: document.getElementsByTagName? (document.getElementsByTagName(tt_tags[i]) || 1)
			: (!tt_n4 && tt_tags[i]=="a")? document.links
			: 1;
		if (tt_n4 && (tt_tags[i] == "a" || tt_tags[i] == "layer")) tags = tt_N4Tags(tt_tags[i]);
		var j = tags.length; while (j--)
		{
			if (typeof (t_tj = tags[j]).onmouseover == "function" && t_tj.onmouseover.toString().indexOf(esc) != -1 && !tt_n6 || tt_n6 && (over = t_tj.getAttribute("onmouseover")) && over.indexOf(esc) != -1)
			{
				if (over) t_tj.onmouseover = new Function(over);
				var txt = unescape(t_tj.onmouseover());
				htm += tt_Htm(
					t_tj,
					"tOoLtIp"+i+""+j,
					txt.wzReplace("& ","&")
				);

				t_tj.onmouseover = new Function('e',
					'tt_Show(e,'+
					'"tOoLtIp' +i+''+j+ '",'+
					(typeof t_tj.T_ABOVE != tt_u) + ','+
					((typeof t_tj.T_DELAY != tt_u)? t_tj.T_DELAY : ttDelay) + ','+
					((typeof t_tj.T_FIX != tt_u)? '"'+t_tj.T_FIX+'"' : '""') + ','+
					(typeof t_tj.T_LEFT != tt_u) + ','+
					((typeof t_tj.T_OFFSETX != tt_u)? t_tj.T_OFFSETX : ttOffsetX) + ','+
					((typeof t_tj.T_OFFSETY != tt_u)? t_tj.T_OFFSETY : ttOffsetY) + ','+
					(typeof t_tj.T_STATIC != tt_u) + ','+
					(typeof t_tj.T_STICKY != tt_u) + ','+
					((typeof t_tj.T_TEMP != tt_u)? t_tj.T_TEMP : ttTemp)+
					');'
				);
				t_tj.onmouseout = tt_Hide;
				if (t_tj.alt) t_tj.alt = "";
				if (t_tj.title) t_tj.title = "";
			}
		}
	}
	document.write(htm);
}

function tt_EvX(t_e)
{
	var t_y = tt_Int(t_e.pageX || t_e.clientX || 0) +
		tt_Int(tt_ie? tt_db.scrollLeft : 0) +
		tt_offX;
	if (t_y > xlim) t_y = xlim;
	var t_scr = tt_Int(window.pageXOffset || (tt_db? tt_db.scrollLeft : 0) || 0);
	if (t_y < t_scr) t_y = t_scr;
	return t_y;
}

function tt_EvY(t_e)
{
	var t_y = tt_Int(t_e.pageY || t_e.clientY || 0) +
		tt_Int(tt_ie? tt_db.scrollTop : 0);
	if (tt_above) t_y -= (tt_objH + tt_offY - (tt_op? 31 : 15));
	else if (t_y > ylim || !tt_dwn && t_y > ylim-24)
	{
		t_y -= (tt_objH + 5);
		tt_dwn = false;
	}
	else
	{
		t_y += tt_offY;
		tt_dwn = true;
	}
	return t_y;
}

function tt_ReleasMov()
{
	if (document.onmousemove == tt_Move)
	{
		if (document.releaseEvents) document.releaseEvents(Event.MOUSEMOVE);
		document.onmousemove = null;
	}
}

function tt_HideInput()
{
	if (!(tt_ie || tt_op6) || !tt_inputs) return;
	var t_o;
	var t_i = tt_inputs.length; while (t_i--)
	{
		t_o = tt_inputs[t_i];
		if (tt_vis && tt_objX+tt_objW > t_o.x && tt_objX < t_o.x+t_o.offsetWidth && tt_objY+tt_objH > t_o.y && tt_objY < t_o.y+t_o.offsetHeight)
			t_o.style.visibility = 'hidden';
		else t_o.style.visibility = 'visible';
	}
}

function tt_GetDiv(t_id)
{
	return (
		tt_n4? (document.layers[t_id] || null)
		: tt_ie? (document.all[t_id] || null)
		: (document.getElementById(t_id) || null)
	);
}

function tt_GetDivW()
{
	return tt_Int(
		tt_n4? tt_obj.clip.width
		: tt_obj.style.pixelWidth? tt_obj.style.pixelWidth
		: tt_obj.offsetWidth
	);
}

function tt_GetDivH()
{
	return tt_Int(
		tt_n4? tt_obj.clip.height
		: tt_obj.style.pixelHeight? tt_obj.style.pixelHeight
		: tt_obj.offsetHeight
	);
}

// Compat with DragDrop Lib: Ensure that z-index of tooltip is lifted beyond toplevel dragdrop element
function tt_SetDivZ()
{
	var t_i = tt_obj.style || tt_obj;
	if (window.dd && dd.z)
		t_i.zIndex = Math.max(dd.z+1, t_i.zIndex);
}

function tt_SetDivPos(t_x, t_y)
{
	var t_i = tt_obj.style || tt_obj;
	var t_px = (tt_op6 || tt_n4)? '' : 'px';
	t_i.left = (tt_objX = t_x) + t_px;
	t_i.top = (tt_objY = t_y) + t_px;
	tt_HideInput();
}

function tt_ShowDiv(t_x)
{
	if (tt_n4) tt_obj.visibility = t_x? 'show' : 'hide';
	else tt_obj.style.visibility = t_x? 'visible' : 'hidden';
	tt_vis = t_x;
	tt_HideInput();
}

function tt_Show(t_e, t_id, t_above, t_delay, t_fix, t_left, t_offx, t_offy, t_static, t_sticky, t_temp)
{
	if (tt_obj) tt_Hide();
	var t_mf = document.onmousemove || null;
	if (window.dd && (window.DRAG && t_mf == DRAG || window.RESIZE && t_mf == RESIZE)) return;
	var t_uf = document.onmouseup || null;
	if (t_mf && t_uf) t_uf(t_e);

	tt_obj = tt_GetDiv(t_id);
	if (tt_obj)
	{
		tt_dwn = !(tt_above = t_above);
		tt_sticky = t_sticky;
		tt_objW = tt_GetDivW();
		tt_objH = tt_GetDivH();
		tt_offX = t_left? -(tt_objW+t_offx) : t_offx;
		tt_offY = t_offy;
		if (tt_op) tt_offY += 21;
		if (tt_n4)
		{
			if (tt_obj.document.layers.length)
			{
				var t_sh = tt_obj.document.layers[0];
				t_sh.clip.height = tt_objH - Math.round(t_sh.clip.width*1.3);
			}
		}
		else
		{
			var t_sh = tt_GetDiv(t_id+'R');
			if (t_sh)
			{
				var t_h = tt_objH - tt_Int(t_sh.style.pixelTop || t_sh.style.top || 0);
				if (typeof t_sh.style.pixelHeight != tt_u) t_sh.style.pixelHeight = t_h;
				else t_sh.style.height = t_h + 'px';
			}
		}

		tt_GetSelects();

		xlim = tt_Int((tt_db && tt_db.clientWidth)? tt_db.clientWidth : window.innerWidth) +
			tt_Int(window.pageXOffset || (tt_db? tt_db.scrollLeft : 0) || 0) -
			tt_objW -
			(tt_n4? 21 : 0);
		ylim = tt_Int(window.innerHeight || tt_db.clientHeight) +
			tt_Int(window.pageYOffset || (tt_db? tt_db.scrollTop : 0) || 0) -
			tt_objH - tt_offY;

		tt_SetDivZ();
		t_e = t_e || window.event;
		if (t_fix) tt_SetDivPos(tt_Int((t_fix = t_fix.split(','))[0]), tt_Int(t_fix[1]));
		else tt_SetDivPos(tt_EvX(t_e), tt_EvY(t_e));

		var t_txt = 'tt_ShowDiv(\'true\');';
		if (t_sticky) t_txt += '{'+
				'tt_ReleasMov();'+
				'window.tt_upFunc = document.onmouseup || null;'+
				'if (document.captureEvents) document.captureEvents(Event.MOUSEUP);'+
				'document.onmouseup = new Function("window.setTimeout(\'tt_Hide();\', 10);");'+
			'}';
		else if (t_static) t_txt += 'tt_ReleasMov();';
		if (t_temp > 0) t_txt += 'window.tt_rtm = window.setTimeout(\'tt_sticky = false; tt_Hide();\','+t_temp+');';
		window.tt_rdl = window.setTimeout(t_txt, t_delay);

		if (!t_fix)
		{
			if (document.captureEvents) document.captureEvents(Event.MOUSEMOVE);
			document.onmousemove = tt_Move;
		}
	}
}

var tt_area = false;
function tt_Move(t_ev)
{
	if (!tt_obj) return;
	if (tt_n6 || tt_w3c)
	{
		if (tt_wait) return;
		tt_wait = true;
		setTimeout('tt_wait = false;', 5);
	}
	var t_e = t_ev || window.event;
	tt_SetDivPos(tt_EvX(t_e), tt_EvY(t_e));
	if (tt_op6)
	{
		if (tt_area && t_e.target.tagName != 'AREA') tt_Hide();
		else if (t_e.target.tagName == 'AREA') tt_area = true;
	}
}

function tt_Hide()
{
	if (window.tt_obj)
	{
		if (window.tt_rdl) window.clearTimeout(tt_rdl);
		if (!tt_sticky || tt_sticky && !tt_vis)
		{
			if (window.tt_rtm) window.clearTimeout(tt_rtm);
			tt_ShowDiv(false);
			tt_SetDivPos(-tt_objW, -tt_objH);
			tt_obj = null;
			if (typeof window.tt_upFunc != tt_u) document.onmouseup = window.tt_upFunc;
		}
		tt_sticky = false;
		if (tt_op6 && tt_area) tt_area = false;
		tt_ReleasMov();
		tt_HideInput();
	}
}

tt_Init();
