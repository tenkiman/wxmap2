#import sys
#import glob
#import mf
#import w2

from WxMAP2 import *
w2=W2()


# -- 20160926 -- eliminate dependence on TCw2 -- put vars methods in tcbase,tcVM
#
from tcbase import YearsBackClimo,YearsBackClimoTss,byearClimo,eyearClimo,BaseDirWWWTcSitrep,\
     RptDir,PltTcOpsDir,ClimoBasinsHemi,TCsByBasin

from ATCF import Aid

#,TrkModeltoBattributes
     
#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
#
#  set global variables and dirs here rather
#  than routine by routine
#
#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg

NyearBreak=24

def SetTCHtmlDirsVars(iyear,ihemi,icuryear,iemmdd,icemmdd,
                      ibyyyymmtss,ieyyyymmtss):

    global hdirbase,jdirbase,cdirbase
    global tpdirbase,spdirbase,trdirbase,srdirbase
    global hemi,lhemi,basinopt
    global year,curyear,emmdd,eyyyymmdd,cemmdd
    global byyyymmtss,eyyyymmtss

    hemi=ihemi
    year=iyear
    curyear=icuryear
    emmdd=iemmdd
    cemmdd=icemmdd
    eyyyymmdd=curyear+cemmdd

    byyyymmtss=ibyyyymmtss
    eyyyymmtss=ieyyyymmtss
    
    lhemi=ihemi.lower()
    
    if(lhemi=='nhem'): basinopt='NHS'
    if(lhemi=='shem'): basinopt='SHS'

    hdirbase=BaseDirWWWTcSitrep
    hdirbase=hdirbase+"/%s.%s"%(year,lhemi)
    mf.ChkDir(hdirbase,'mk')

    jdirbase=hdirbase+'/js'
    mf.ChkDir(jdirbase,'mk')

    cdirbase=hdirbase+'/css'
    mf.ChkDir(cdirbase,'mk')

    tpdirbase=hdirbase+'/plt'
    mf.ChkDir(tpdirbase,'mk')
    spdirbase=PltTcOpsDir

    trdirbase=hdirbase+'/rpt'
    mf.ChkDir(trdirbase,'mk')
    srdirbase=RptDir

    nytss=YearsBackClimoTss





#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#
# basin css
#
#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

TcSitrepCss="""

.btn { 

	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size :8pt;
	font-style : bold;
	font-weight : bold;
	color: #CCCCFF;
	width: 60px;
	align: center;
	background-color: #51588E; 
	padding: 0px;
  }	

h1 {
color : black;
font-size : 20pt;
font-weight:bold;
font-style:normal;
text-ident:0.5in;
font-family:arial,helvetica,san-serif;
}

h2 {
color : darkred;
font-size : 16pt;
font-weight:bold;
font-style:italic;
text-ident:0.5in;
font-family:verdana,arial,helvetica,san-serif;
}

h3 {
color : darkblue;
font-size : 14pt;
font-weight:bold;
font-style:normal;
text-ident:0.25in;
font-family:arial,helvetica,san-serif;
}

h4 {
font-size: 12pt;
font-family: courier new;
font-weight: bold;
line-height: 12pt;
text-align: left;
color: red
}


table.models[ {
	font-family: Arial, Helvetica, sans-serif;
	font-size: 8pt;
	font-weight: bold;
	font-style: italic;
	text-align : center;
}

table.models th {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 10pt;
	font-style : normal;
	font-weight : bold;
	text-align : center;
	vertical-align : middle;
}


table.models td.key {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 8pt;
	font-style : normal;
	font-weight : bold;
	text-align : center;
	vertical-align : middle;
	background-color : lightyellow;
        background-color : khaki;
        border: 0;
	padding: 0px;
}

table.models td.basin {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 6pt;
	font-style : normal;
	font-weight : normal;
	text-align : center;
	vertical-align : middle;
	background-color : lightyellow;
        background-color : khaki;
        border: 0;
	padding: 0px;
}

table.models td.nbsp {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 9pt;
	font-style : normal;
	font-weight : bold;
	text-align : middle;
	vertical-align : middle;
        background-color : khaki;
	padding: 0px;
}

table.models td {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 9pt;
	font-style : normal;
	font-weight : bold;
	text-align : middle;
	vertical-align : middle;
	padding-top: 2px;
	padding-bottom: 2px;
	padding-left: 5px;
	padding-right: 5px;
}

table.models td.title {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 14pt;
	font-style : italic;
	font-weight : bold;
	text-align : left;
	color: navy;
        background-color : khaki;
	vertical-align : middle;
        padding: 0px;
}

table.models td.code {
	font-family : Courier;
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 10pt;
	font-style : normal;
	font-weight : bold;
	text-align : right;
        color: red;
	background-color : lightyellow;
        background-color : khaki;
        width: 120;
        border: 0;
	vertical-align : middle;
}

table.button2 {
	width : 40px;
}

table.button2 td {
	font-family : Verdana,monospace;
	font-size : 8pt;
	font-style : normal;
	font-weight : normal;
	width : 38px;
	text-align : left;
	vertical-align : middle;
	padding: 0px;
	margin-top: 0px;
	margin-bottom: 0px;
}

table.button2 td.bdesc {
	text-align : center;
	font-weight : bold;
	vertical-align : middle;
	width : 38px;
	background-color : LightGrey;
	font-color : Black;
}


table.button2 .bhelp{
	font-family: Arial, Helvetica, sans-serif;
	font-size: 8pt;
	font-weight: bold;
	font-style: italic;
	color: White;
	background-color : Red;
	text-align : center;
	vertical-align : middle;
}

table.button {
	width : 100px;
}


table.button .lks{
	font-family: Arial, Helvetica, sans-serif;
	font-size: 8pt;
	font-weight: bold;
	font-style: italic;
	background-color : Silver;
	text-align : center;
	width : 250;
}

table.button td.d {
	font-family : Geneva, Arial, Helvetica, sans-serif;
	font-size : 8pt;
	font-style : normal;
	font-weight : normal;
	width : 100px;
	text-align : left;
	vertical-align : middle;
}

table.button td {
	font-family : Verdana,monospace;
	font-size : 8pt;
	font-style : normal;
	font-weight : normal;
	width : 100px;
	text-align : left;
	vertical-align : middle;
}


table.button th {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 8pt;
	font-style : normal;
	font-weight : bold;
	font-weight : normal;
	width : 25px;
	text-align : center;
	vertical-align : middle;
}


table.button th.d {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size : 8pt;
	font-style : normal;
	font-weight : bold;
	width : 100px;
	text-align : left;
	vertical-align : middle;
}

table.button .bhelp{
	font-family: Arial, Helvetica, sans-serif;
	font-size: 8pt;
	font-weight: bold;
	font-style: italic;
	color: White;
	background-color : Red;
	text-align : center;
	vertical-align : middle;
}

table.button .binfo{
	font-family: Arial, Helvetica, sans-serif;
	font-size: 8pt;
	font-weight: bold;
	font-style: normal;
	background-color : LightBlue;
	text-align : center;
	width : 25;
}

table.button .bbig{
	font-family: Arial, Helvetica, sans-serif;
	font-size: 10pt;
	font-weight: bold;
	font-style: italic;
	background-color : Silver;
	text-align : center;
	width : 25;
}

.bdesc {
	text-align : center;
	font-weight : bold;
	vertical-align : middle;
	background-color : LightGrey;
	font-color : Black;
}

.bdesc {
	text-align : center;
	font-weight : bold;
	vertical-align : middle;
	background-color : LightGrey;
	font-color : Black;
}


.be4 {
	background-color :  #EE82EE;
}


.b12z {
	background-color : Yellow;
}

.bda {
	background-color : #ADD8E6;
}


.bmodel {
/*	background-color : Yellow; */
	background-color : lightyellow;
        background-color : khaki;
	padding: 0px;
	width: 60;
	border: 0;
	align : center;
	vertical-align : middle;
}



.bsio {
	background-color : #ADD8E6;
}

.bshem {
	background-color : Yellow;
}

.bnhem {
	background-color : Yellow;
}

.bcpac {
	background-color : LightGreen;
}

.bnio {
	background-color : Wheat;
}

.byearcur {
	background-color : Orange;
}

.byear {
	background-color : LightGreen;
}

.khaki {
	background-color : khaki;
}


.bspac {
	background-color :  #EE82EE;
}

.bswpac {
	background-color :  #EE82EE;
}

.bwpac {
	background-color :  #EE82EE;
}

.bepac {
	background-color :  LightGrey;
}


.btnstm { 
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size: 5pt;
	font-style : bold;
	font-weight : bold;
	width: 38px;
	align: center;
	padding: 0px;
	margin-top: 0px;
	margin-bottom: 0px;
}	

"""



#jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
#
#  basic js
#
#jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj

ToolTipJs="""<!-- 
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
		var ErrorNotice = "DHTML TIP MESSAGE VERSION 1.2 ERROR NOTICE.\\n"
		if(t.length<2&&s.length<25) alert(ErrorNotice+"It looks like you removed an entry or more from the Style Array and Text Array of this tip.\\nTheir should be 25 entries in every Style Array even though empty and 2 in every Text Array. You defined only "+s.length+" entries in the Style Array and "+t.length+" entry in the Text Array. This tip won't be viewed to avoid errors")
		else if(t.length<2) alert(ErrorNotice+"It looks like you removed an entry or more from the Text Array of this tip.\\nTheir should be 2 entries in every Text Array. You defined only "+t.length+" entry. This tip won't be viewed to avoid errors.")
		else if(s.length<25) alert(ErrorNotice+"It looks like you removed an entry or more from the Style Array of this tip.\\nTheir should be 25 entries in every Style Array even though empty. You defined only "+s.length+" entries. This tip won't be viewed to avoid errors.")
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
"""

WZ_ToolTipJs="""
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

		var t_txt = 'tt_ShowDiv(\\'true\\');';
		if (t_sticky) t_txt += '{'+
				'tt_ReleasMov();'+
				'window.tt_upFunc = document.onmouseup || null;'+
				'if (document.captureEvents) document.captureEvents(Event.MOUSEUP);'+
				'document.onmouseup = new Function("window.setTimeout(\\'tt_Hide();\\', 10);");'+
			'}';
		else if (t_static) t_txt += 'tt_ReleasMov();';
		if (t_temp > 0) t_txt += 'window.tt_rtm = window.setTimeout(\\'tt_sticky = false; tt_Hide();\\','+t_temp+');';
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
"""

TcTipsJs="""

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
Text[6]=["Float","This tip Is float positioned at a (10,10) coordinate, It also \\
floats with the scrollbars so it is always static"]
Text[7]=["Fixed","This tip Is fixed positioned at a (1,1) coordinate"]
Text[8]=["sticky style","This tip will sticky around<BR>This is useful when you want \\
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

Text['help.veri']=["Help -- TC Veri Stats","Plots of TC Verification Stats<hr>\\
the \\"KEY\\" link in the title above leads to a description of the verification plots<hr>\\
mousing over the grey title buttons describes the clickable buttons below<hr>\\
Plots are organized by: 1) basin; 2) Units; 3) Models; 4) statistics; 5) verification type; and 6) verification rules\\
"]

Text['help.trk']=["Help -- TC track plots","Plots of model TC tracks/stats<hr>\\
the \\"KEY\\" link in the title above leads to a description of the track plot and model stats<hr>\\
Mousing over the grey title buttons describes the clickable buttons below<hr> \\
Clicking on the image brings up the image in a separate window<hr> \\
Plots for each TC (NNB where NN is storm number and B is basin) are organized by basin and model; if no plot is displayed, click on a different storm\\
"]

/*
 verification plots
*/

Text[30]=["Verification Rule","<b>JTWC</b> - verify all positions in the best track file, \\
including prewarning invest posits <hr>\\
<b>NHC</b> - verify only forecasts where the initial and foreacst best track intensities \\
are >= 35 kt (i.e., only TC >= tropical storms"]

Text[31]=["Verification Type",
"\\
<b>Hetereo</b> - heterogenous verification (verify all forecasts) <hr> \\
<b>Homo</b> - homogeneous or \\"side-by-side\\" comparison (verify forecasts only when both models are available)\\
"]

Text[32]=["Statistic Type",
"\\
<b>FE</b> - Forecast Error =  great circle distance between forecast and verifying position <hr> \\
<b>POD</b> - Probability of Detection =  number of forecast / number of verifying posits [%] or the % time the model makes\\
 a forecast; 100% means the model made a forecast for all possible best track verification times<hr>\\
<b>% IMP CLP</b> - % FE improvement over the no-skill standard CLImatology and PERsistence (CLIPER) = \\
(FE_CLIPER - FE_model/FE_CLIPER)*100 ; >0 means better than CLIPER (skill), <0 poorer than CLIPER (no skill)<hr>\\
<b>VE + bias</b> - Mean Abs Vmax Error (VE) + Mean Vmax Error (bias)\\
"]

Text[33]=["Model Comps",
"\\
<center><b>model1</b> versus <b>model2</b><hr></center>\\
<b>OFC</b> - Official Forecast (JTWC | NHC)<hr> \\
<b>CLP</b> - CLImatology and PERsistence (CLIPER) (no-skill model)<hr> \\
<b>GFS</b> - NCEP GFS (aka AVN) (T254 L68)<hr> \\
<b>NGP</b> - FNMOC NOGAPS4.0 (T239 L30)<hr> \\
<b>UKM</b> - UKMO UM (0.83x0.55 L38)<hr> \\
<b>ECO</b> - ECMWF IFS (ops) (T<sub>Lf</sub>511 L60)<hr> \\
<b>ECE</b> - ECMWF IFS (EPS) (T<sub>Lf</sub>255 L40)\\
"]

Text[34]=["Units",
"\\
<b>Nautical</b> - distance in nm (nautical miles) and speed in kt (knots = nm/hr)<hr> \\
<b>Metric</b> - distance in km (kilometers) and speed in m/s (meters / second) \\
"]

Text['nhem']=["Basin",
"\\
<b>NHEM</b> - Entire northern Hemisphere <hr> \\
<b>WPAC</b> - western North Pacific Ocean (\\"W\\" in ATCF)<hr> \\
<b>EPAC</b> - eastern+central North Pacific Ocean (\\"E/C\\" in ATCF)<hr> \\
<b>LANT</b> - north Atantic Ocean (\\"L\\" in ATCF)<hr> \\
<b>NIO</b> - north Indian Ocean (Arabian Sea, Bay of Bengal) (\\"A/B\\" in ATCF)<hr> \\
"]

Text['shem']=["Basin",
"\\
<b>SHEM</b> - Entire southern Hemisphere <hr> \\
<b>SWPAC</b> - southwest Pacific Ocean =  lon > 135E (eastern Australia ->, \\"P\\" in ATCF)<hr> \\
<b>SIO</b> - south Indian Ocean =  lon < 135E (<- western Australia, \\"S\\" in ATCF<hr> \\
<b>SLANT</b> - south Atlantic Ocean = (first well documenting TC) \\"T\\" (my ATCF code)\\
"]

MODEL['desc']=["Models",
"\\
<b>OFC</b> - Offical Forecast (JTWC | NHC)<hr> \\
<b>CLP</b> - CLImatology and PERsistence (CLIPER) (no-skill model)<hr> \\
<b>GFS</b> - NCEP GFS (aka AVN) (T254 L68)<hr> \\
<b>NGP</b> - FNMOC NOGAPS4.0 (T239 L30)<hr> \\
<b>UKM</b> - UKMO UM (0.83x0.55 L38)<hr> \\
<b>ECO</b> - ECMWF IFS (ops) (T<sub>Lf</sub>511 L60)<hr> \\
<b>ECE</b> - ECMWF IFS (EPS) (T<sub>Lf</sub>255 L40)\\
<b>BTK</b> - Best Track\\
"]


MODEL['ofc']=["Official Forecast",
"\\
Warning Center Track Forecast<br>\\
WESTPAC/SHEM = JTWC<br>\\
EASTPAC/LANT = NHC<br>\\
<br>\\
"]

MODEL['clp']=["CLP - CLIPER",
"\\
CLImatology - PERsistence statistical model\\
<br>\\
"]

MODEL['gfs']=["NCEP GFS",
"\\
NCEP Global Forecast System (aka AVN)<br>\\
four-times daily (00/06/12/18Z) global run <br>\\
(T254 L68)<br>\\
<br>\\
"]

MODEL['ngp']=["FNMOC NOGAPS",
"\\
FNMOC Navy Operational Global Atmospheric Prediction System<br>\\
twice-daily (00/12Z) global run <br>\\
[T239 L30]<br>\\
<br>\\
"]

MODEL['eco']=["ECMWF IFS (ops)",
"\\
ECMWF Integrated Forecast System<br>\\
twice-daily deterministic run<br>\\
[T<sub>L</sub>511 L60]<br>\\
<br>\\
"]

MODEL['ece']=["ECMWF IFS (EPS)",
"\\
ECMWF Integrated Forecast System<br>\\
EPS - Ensemble Prediction System<br>\\
twice-daily EPS control run (initialize with deterministic run analysis)<br>\\
ensemble has 51-members<br>\\
[T<sub>L</sub>255 L40]<br>\\
<br>\\
"]

MODEL['ukm']=["UK Met Office Unified Model",
"\\
UKMO UM global configuration, new dynamics<br>\\
[(0.83 (dlon) x 0.55 (dlat) L38)<br>\\
<br>\\
"]

MODEL['btk']=["Best Track",
"\\
Current Operational Best Track<br>\\
is rebested after seaseon<br>\\
<br>\\
"]


TC['desc']=["TC - NNB",
"\\
<b>NNB</b>: Storm # + ATCF 1-char basin ID<hr>\\
<b>L</b>: north Alantic<br>\\
<b>E</b>: eastern North Pacific<br>\\
<b>W</b>: western North Pacific<br>\\
<b>B</b>: Bay of Bengal<br>\\
<b>A</b>: Arabian Sea<br>\\
<b>S</b>: south Indian Ocean<br>\\
<b>P</b>: western South Pacific<br>\\
<b>T</b>: south Alantic<br>\\
"]

"""

#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#
#  basic html
#
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

TrkTailCol1="""</form>
</table></td>
"""
        
TrkHeadCol1="""
<!-- ***************** col2 -- TCs lant/epac -->
<td valign=top class='khaki'>
<table class="button2">
<!--
<tr><td class="bdesc"  onMouseOver='stm(TC["desc"],Style[20])' onMouseOut="htm()">
TC atl/epc
</td></tr>
-->

<form>
"""


TrkHeadCol2="""
<!-- ***************** col3 -- TCs lant/epac -->
<td valign=top  class='khaki'>
<table class="button2">
<!--
<tr><td class="bdesc"  onMouseOver='stm(TC["desc"],Style[20])' onMouseOut="htm()">
TC nio/wpc
</td></tr>
-->

<form>
"""

TrkModelCol="""
<!-- ***************** col4 -- models -->
<td valign=top align="left">
<table class="button2">

<!--
<tr>
<td class="bhelp" onMouseOver="stm(Text['help.trk'],Style[20])" onMouseOut="htm()" >HELP
</td></tr>

<tr><td class="bdesc"  onMouseOver='stm(MODEL["desc"],Style[20])' onMouseOut="htm()">
Model
</td></tr>
-->


<form>
<tr><td class="bmodel" onMouseOver='stm(MODEL["ofc"],Style[20])' onMouseOut='htm()'>
<input type="radio" name="tcact" onClick='model="ofc";swap();'>OFC
</td></tr>
<tr><td class="bmodel" onMouseOver='stm(MODEL["clp"],Style[20])' onMouseOut='htm()'>
<input type="radio" name="tcact" onClick='model="clp";swap();'>CLP
</td></tr>
<tr><td class="bmodel" onMouseOver='stm(MODEL["gfs"],Style[20])' onMouseOut='htm()'>
<input type="radio" name="tcact" checked onClick='model="avn";swap();'>GFS
</td></tr>
<tr><td class="bmodel" onMouseOver='stm(MODEL["ngp"],Style[20])' onMouseOut='htm()'>
<input type="radio" name="tcact" onClick='model="ngp";swap();'>NGP
</td></tr>
<tr><td class="bmodel" onMouseOver='stm(MODEL["ukm"],Style[20])' onMouseOut='htm()'>
<input type="radio" name="tcact" onClick='model="ukm";swap();'>UKM
</td></tr>
<tr><td class="bmodel" onMouseOver='stm(MODEL["eco"],Style[20])' onMouseOut='htm()'>
<input type="radio" name="tcact" onClick='model="eco";swap();'>ECO
</td></tr>
<tr><td class="bmodel" onMouseOver='stm(MODEL["ece"],Style[20])' onMouseOut='htm()'>
<input type="radio" name="tcact" onClick='model="ece";swap();'>ECE
</td></tr>
<tr><td class="bmodel" onMouseOver='stm(MODEL["btk"],Style[20])' onMouseOut='htm()'>
<input type="radio" name="tcact" onClick='model="btk";swap();'>BTK
</td></tr>
</form>
</table></td>

</td></table>
"""

TrkDocTail="""

</table>

<script language="JavaScript" type="text/javascript" src="js/wz_tooltip.js"></script>
</body>
</html>
"""

def writehtml(hdir,hname,html):
    hpath=hdir+'/'+hname
    h=open(hpath,'w')
    h.writelines(html)
    h.close()


def HtmlTrkHead(year,hemi,bstmid,bstmname,bstmclass,eyymmdd):
    
    title="Global Model TC Tracks/Stats -- %s %s as of: %s"%(year,hemi,eyymmdd)

    htitle="""Global Model TC Tracks/Stats - %s %s
<font style='color: red; font-size: 8pt; font-style: normal'> as of: %s</font>"""%(year,hemi,eyymmdd)

    html="""
<html>
<head>
<title>
%s
</title>

<link rel="stylesheet" type="text/css" href="../css/tcsitrep.css">

</head>

<body text="black" link="blue" vlink="purple" bgcolor=#fcf1da onLoad="swap()">

<!--  tc tooltip text -->
<script language="JavaScript1.2" src="js/tctips.js" type="text/javascript"></script>

<script language="javascript">
<!--
plotdir="plt/track/";
plot="tc.trk";
model="avn";
year="%s";
stid="%s";
stname="%s";
stclass="%s";
function swap() 
{
value= plotdir+plot+"."+model+"."+year+"."+stid+"."+stname+"."+stclass+".png";
valueloop= plotdir+plot+"."+model+"."+year+"."+stid+"."+stname+"."+stclass+".loop.gif";
if(model == 'btk') {
  valueloop= plotdir+plot+"."+model+"."+year+"."+stid+"."+stname+"."+stclass+".png";
}
myUrl=value;
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
// -->
</script>

<!-- NNNNNNNNNNNNNNNNNNNN new head -->

<table class="models" cellspacing=0 cellpadding=0 border=0>

<tr>

<td class='title' colspan=9 >
%s
</td>

<td class='nbsp' width=118>
&nbsp
</td>

<td class='key' width=39
onMouseOver="this.T_STATIC=true;this.T_WIDTH=200;
return escape('go to key doc')" >
<a href="key.track.htm"><i>key</i></a>
</td>

<td class='key' width=39
onMouseOver="this.T_STATIC=true;this.T_WIDTH=200;
return escape('go to main doc')" >
<a href="../doc/"><i>main</i></a>
</td>

<td class='key' width=39
style="background-color: white; color: red" 
onMouseOver="this.T_STATIC=true;this.T_TITLE=Text['help.trk'][0];this.T_WIDTH=200;
return escape(Text['help.trk'][1])" >
HELP
</td>

<!--
<td class='blant' width=80
onMouseOver="this.T_STATIC=true;this.T_TITLE=Text['help.trk'][0];this.T_WIDTH=200;
return escape(Text['help.trk'][1])" >
HELP
</td>
-->


</tr>

<tr>

<td class='code' width=200 
onMouseOver="this.T_STATIC=true;this.T_TITLE=MODEL['desc'][0];this.T_WIDTH=250;
return escape(MODEL['desc'][1])" >
MODELS:
</td>


"""%(title,year,bstmid,bstmname,bstmclass,htitle)

    models=TrkModels

    for model in models:
        html=html+HtmlTcTrkModelButton(model)



    htmNhem="""

<td class='nbsp'>
&nbsp
</td>

<td class='basin'
onMouseOver="this.T_STATIC=true;this.T_TITLE=TC['desc'][0];this.T_WIDTH=250;
return escape(TC['desc'][1])" >
WPAC
</td>

<td class='basin'
onMouseOver="this.T_STATIC=true;this.T_TITLE=TC['desc'][0];this.T_WIDTH=250;
return escape(TC['desc'][1])" >
EPAC<br>
CPAC
</td>

<td class='basin'
onMouseOver="this.T_STATIC=true;this.T_TITLE=TC['desc'][0];this.T_WIDTH=250;
return escape(TC['desc'][1])" >
LANT<br>
NIO
</td>

</tr>
</table>

<!-- ***************** table with track and stm buttons -->
<table  cellspacing=0 cellpadding=0 border=0 >
<!-- ***************** col1 -- image -->
<td valign=top>
<a name="link" href="myUrl" target="_blank"><img name="myImage"></a>
</td>


"""
    htmShem="""

<td class='nbsp'>
&nbsp
</td>

<td class='basin'
onMouseOver="this.T_STATIC=true;this.T_TITLE=TC['desc'][0];this.T_WIDTH=250;
return escape(TC['desc'][1])" >
SIO
</td>

<td class='basin'
onMouseOver="this.T_STATIC=true;this.T_TITLE=TC['desc'][0];this.T_WIDTH=250;
return escape(TC['desc'][1])" >
SPAC
</td>

<td class='basin'
onMouseOver="this.T_STATIC=true;this.T_TITLE=TC['desc'][0];this.T_WIDTH=250;
return escape(TC['desc'][1])" >
SLANT
</td>

</tr>
</table>

<!-- ***************** table with track and stm buttons -->
<table  cellspacing=0 cellpadding=0 border=0 >

<!-- ***************** col1 -- image -->
<td valign=top>
<a name="link" href="myUrl" target="_blank"><img name="myImage"></a>
</td>


"""


    if(hemi == 'NHEM'):
        html=html+htmNhem
    elif(hemi == 'SHEM'):
        html=html+htmShem


    return(html)

#hhhhhhh tctrk hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#
#
#
#hhhhhhh tctrk hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

def HtmlTcTrkModelButton(model):

    aidprop=Aid(model)
    attb=aidprop.TrkModeltoBattributes

    bname=attb[0]
    bcol=attb[1]
    fcol=attb[2]
    mname=attb[3]

    htm="""
<td class='bmodel'
onMouseOver="this.T_TITLE=MODEL['%s'][0];
this.T_STICKY=true;
this.T_STATIC=true;
this.T_WIDTH=200;
this.T_DELAY=500;
this.T_FIX=[820,10];
this.T_TEMP=2000;
return escape(MODEL['%s'][1])" >
<input type='button' class='btn'
style="background-color: %s; color: %s" 
value="%s" name="tcact" onClick='model="%s";swap();'>
</td>
"""%(model,model,bcol,fcol,bname,mname)

    return(htm)




    

#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#
#  track html and js
#
#jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj


def HtmlJsTCTrk(allhtml,alljs,tcstats,year,hemi,bstmid,eyymmdd):

    verb=0
    
    def NstmBasinCol(hbasins,stms):
        nb=0
        for h in hbasins:
            for stm in stms:
                bnum=int(stm[0:2])
                bcode=stm[-1]
                if(h == bcode):
                    nb=nb+1
        return(nb)

    #
    # html and js for track plots
    #

    stms=allhtml.keys()
    stms.sort()

    if(hemi == 'NHEM'):
        hbasins1=['W']
        hbasins2=['E','C']
        hbasins3=['L','A','B']

    if(hemi == 'SHEM'):
        hbasins1=['S']
        hbasins2=['P']
        hbasins3=['T']

    #
    # find number of stm / basin col
    #
    nbcol1=NstmBasinCol(hbasins1,stms)
    nbcol2=NstmBasinCol(hbasins2,stms)
    nbcol3=NstmBasinCol(hbasins3,stms)


    if(bstmid == 'null'): bstmid=stms[-1]
    
    bstmclass=tcstats[bstmid][0]
    bstmname=tcstats[bstmid][1]


    print bstmid,bstmname,eyymmdd
    trkhtml=HtmlTrkHead(year,hemi,bstmid,bstmname,bstmclass,eyymmdd)

    tail1=TrkTailCol1
    head1=TrkHeadCol1
    head2=TrkHeadCol2
    head3=TrkHeadCol2

    htmlcol1=[]
    htmlcol2=[]
    htmlcol3=[]
    jstip=[]

    if(nbcol1>0):
        htmlcol1.append(head1)
        for h in hbasins1:
            for stm in stms:
                bnum=int(stm[0:2])
                bcode=stm[-1]
                if(h == bcode):
                    if(verb): print 'col1: ',stm,bnum,bcode,allhtml[stm]
                    htmlcol1.append(allhtml[stm])
                    jstip.append(alljs[stm])
        htmlcol1.append(tail1)
        for h in htmlcol1:
            if(verb): print 'col1: ',h
            trkhtml=trkhtml+h

    if(nbcol2>0):
        htmlcol2.append(head2)
        for h in hbasins2:
            for stm in stms:
                bnum=int(stm[0:2])
                bcode=stm[-1]
                if(h == bcode):
                    if(verb): print 'col2: ',stm,bnum,bcode
                    htmlcol2.append(allhtml[stm])
                    jstip.append(alljs[stm])
        htmlcol2.append(tail1)
        for h in htmlcol2:
            trkhtml=trkhtml+h

    if(nbcol3>0):
        htmlcol3.append(head3)
        for h in hbasins3:
            for stm in stms:
                bnum=int(stm[0:2])
                bcode=stm[-1]
                if(verb): print 'col3: ',stm,bnum,bcode
                if(h == bcode):
                    htmlcol3.append(allhtml[stm])
                    jstip.append(alljs[stm])
        htmlcol3.append(tail1)
        for h in htmlcol3:
            trkhtml=trkhtml+h


    trkhtml=trkhtml+TrkDocTail

    trkjs=TcTipsJs

    for j in jstip:
        trkjs=trkjs+j


    hname="tc.trk.%s.%s.htm"%(year,lhemi)

    return(trkhtml,trkjs,hname)


#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#4444444444444444444444444444444444444444444444444444444444444444444444
#
#  TC verification stats html (tc4.htm)
#
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

def HtmlTCVeriStats(dowrite=1):

    hdir=hdirbase
    yearm0=year
        
    title="Global Model TC Veri Stats -- %s %s as of: %s"%(yearm0,hemi,eyyyymmdd)
    
    if(hemi=='NHEM'):

        hemisb='NHS'
        lbasins=[('NHS','NHEM'),('WPS','WPAC'),('EPS','EPAC'),('LTS','LANT'),('NIS','NIO')]

    elif(hemi == 'SHEM'):

        hemisb='SHS'
        lbasins=[('SHS','SHEM'),('P','SWPAC'),('S','SIO'),('T','SLANT')]

    else:

        print 'EEEEEE invalid hemi: %s'%(hemi)
        sys.exit()


    htmlin1=(title,title,year,lhemi,hemisb,lhemi)
    
    htmlin2=()
    
    htmlin3=()
    
    html1="""
<html>

<head>

<title>
%s
</title>

<link rel="stylesheet" type="text/css" href="../css/tcsitrep.css">
<!-- ********** tooltip script -->
<script language="javascript1.2" src="../js/tooltip.js"type="text/javascript"></script>

</head>

<body text="black" link="blue" vlink="purple" bgcolor=#fcf1da onLoad="swap()">

<!-- ********** tooltip script -->
<div id="TipLayer" style="visibility:hidden;position:absolute;z-index:1000;top:-100"></div>
<script language="JavaScript1.2" src="js/tctips.js" type="text/javascript"></script>

<h2>
%s
<font size=-1>
[
<a href="key.veri.htm" onMouseOver='stm(["","plot key doc"],Style[23])' onMouseOut="htm()"><i>KEY<i></a>,
<a href="../doc/" onMouseOver='stm(["","main doc"],Style[23])' onMouseOut="htm()">main doc</a>
]
</a>)</font>
</h2>


<script language="javascript">
<!--
plotdir="plt/veri/";
plot="tc.veri.stat";
stattype="fe";
units="english";
veriname="ops.%s.%s";
verirule="jtwc";
veritype="hetero"
basin="%s";
model1="ofc";
model2="clp";

function swap() 
{
if(veritype == 'homo') overitype = veritype+"."+model1+"."+model2;
if(veritype == 'hetero') overitype = veritype
value= plotdir+plot+"."+stattype+"."+units+"."+veriname+"."+verirule+"."+overitype+"."+basin+"."+model1+"."+model2+".png"
myUrl=value;
if (value != '') if (document.images) {
  document.images.myImage.src = value;
  document.images.myImage.alt = value;
  var el=document.images.myImage;
  while(el.nodeName.toLowerCase() != 'a') {
    el=el.parentNode;
    el.setAttribute('href',myUrl);
  }
}
//alert(value);
}
// -->
</script>

<table border >

<td valign=top>
<a name="link" href="myUrl" target="_blank"><img name="myImage"></a>
</td>


<td valign=top>

<table class="button">

<tr>
<td class="bhelp" onMouseOver="stm(Text['help.veri'],Style[20])" onMouseOut="htm()" >HELP
</td>
</tr>

<form>

<tr><td class="bdesc"  onMouseOver="stm(Text['%s'],Style[20])" onMouseOut="htm()">
Basin
</td></tr>

"""%(htmlin1)

    def basinbutton(lbasin,cbasin,ubasin,bchecked):
        bhtml="""        
<tr>
<td class="b%s">
<input type="radio" name="tcact" %s onClick='basin="%s",swap();'>%s
</td>
</tr>
"""%(lbasin,bchecked,cbasin,ubasin)
        return(bhtml)

    html2=""
    for lbasin in lbasins:
        cbasin=lbasin[0]
        basin=lbasin[1]
        bchecked=''
        if(lbasin == lbasins[0]): bchecked='checked'
        ubasin=basin
        lbasin=ubasin.lower()
        
        html2=html2+basinbutton(lbasin,cbasin,ubasin,bchecked)

    html3="""
</form>


<form>

<tr><td class="bdesc"  onMouseOver="stm(Text[33],Style[20])" onMouseOut="htm()">
Models
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" checked onClick='model1="ofc",model2="clp";swap();'>OFC v CLP
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="ofc",model2="avn";swap();'>OFC v GFS
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="ofc",model2="ngp";swap();'>OFC v NGP
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="ofc",model2="ukm";swap();'>OFC v UKM
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="ofc",model2="eco";swap();'>OFC v ECO
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="avn",model2="ngp";swap();'>GFS v NGP
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="avn",model2="eco";swap();'>GFS v ECO
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="avn",model2="ukm";swap();'>GFS v UKM
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="ece",model2="eco";swap();'>ECE v ECO
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="ngp",model2="eco";swap();'>NGP v ECO
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='model1="ukm",model2="eco";swap();'>UKM v ECO
</td></tr>
</form>

<form>
<tr><td class="bdesc"  onMouseOver="stm(Text[32],Style[20])" onMouseOut="htm()">
Stat Type
</td></tr>
<tr><td class="bda">
<input type="radio" name="tcact" checked onClick='stattype="fe";swap();'>FE
</td></tr>

<tr><td class="bda">
<input type="radio" name="tcact" onClick='stattype="pod";swap();'>POD
</td></tr>

<tr><td class="bda">
<input type="radio" name="tcact" onClick='stattype="impclp";swap();'>%% IMP CLP
</td></tr>

<tr><td class="bda">
<input type="radio" name="tcact" onClick='stattype="vmax";swap();'>VE+bias
</td></tr>
</form>

<form>
<tr><td class="bdesc"  onMouseOver="stm(Text[31],Style[20])" onMouseOut="htm()">
Veri Type
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" checked onClick='veritype="hetero";swap();'>Hetero
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='veritype="homo";swap();'>Homo
</td></tr>
</form>

<form>
<tr><td class="bdesc" onMouseOver="stm(Text[30],Style[20])" onMouseOut="htm()" >
Veri Rule
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" checked onClick='verirule="jtwc";swap();'>JTWC
</td></tr>

<tr><td class="b12z">
<input type="radio" name="tcact" onClick='verirule="nhc.pure";swap();'>NHC
</td></tr>
</form>

<form>
<tr><td class="bdesc"  onMouseOver="stm(Text[34],Style[20])" onMouseOut="htm()">
Units
</td></tr>
<tr>
<td class="be4">
<input type="radio" name="tcact" checked onClick='units="english";swap();'>Nautical
</td>
</tr>

<tr><td class="be4">
<input type="radio" name="tcact" onClick='units="metric";swap();'>Metric
</td></tr>
</form>

</table>
</td>


</tr>

</td></table>

<script language="JavaScript" type="text/javascript" src="js/wz_tooltip.js"></script>
</body>
</html>
"""%(htmlin3)

    html=html1+html2+html3
    hname="tc.veri.stat.%s.%s.htm"%(year,lhemi)
    
    if(dowrite):
        writehtml(hdir,hname,html)
    else:
        print html

    return(html)



#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#3333333333333333333333333333333333333333333333333333333333333333333333
#
#  TC activity TS html (tc3.htm)
#
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

def HtmlTCActTS(dowrite=1):

    nybacks=YearsBackClimoTss

    hdir=hdirbase

    for nyback in nybacks:
        yearm0=year
        yearp1=str(int(year)+1)
        yearmb0=str(int(year)-nyback+1)
        yearmb1=str(int(year)-nyback)
    
    titleTAB="TCact TS"
    title="TCact TS -- scaled TCdays & scaled ACE days Time Series %s-%s thru: %s"%(yearmb0,yearm0,eyyyymmdd)
    
    if(hemi=='NHEM'):

        bmmdd='0101'
        bdtgmb=yearmb0+bmmdd
        edtgmb=yearp1+bmmdd

        hbasins=ClimoBasinsHemi['NHS']
        basins=[]
        for basin in hbasins:
            basins.append(basin.upper())


    elif(hemi == 'SHEM'):

        bmmdd='0701'
        
        bdtgmb=yearmb1+'0701'
        edtgmb=yearm0+'0701'

        hbasins=ClimoBasinsHemi['SHS']
        basins=[]
        for basin in hbasins:
            basins.append(basin.upper())


    else:

        print 'EEEEEE invalid hemi: %s'%(hemi)
        sys.exit()


    byyyymm=byyyymmtss[0][0:6]
    eyyyymm=eyyyymmtss[0][0:6]


    htmlin1=(titleTAB,title,lhemi,byyyymm,eyyyymm,lhemi)
    
    htmlin2=()
    
    htmlin3=()
    
    html1="""
<html>
<head>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VG0RC3XML9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-VG0RC3XML9');
</script>


<title>
%s
</title>

<link rel="stylesheet" type="text/css" href="../css/tcsitrep.css">
<!-- ********** tooltip script -->
<script language="javascript1.2" src="../js/tooltip.js" type="text/javascript"></script>

</head>


<body text="black" link="blue" vlink="purple" bgcolor=#fcf1da onLoad="swap()">

<!-- ********** tooltip script -->
<div id="TipLayer" style="visibility:hidden;position:absolute;z-index:1000;top:-100"></div>
<script language="JavaScript1.2" src="js/tctips.js" type="text/javascript"></script>

<h2>
%s
<font size=-1>(<a href="../doc/" onMouseOver='stm(["","return to main doc"],Style[23])' onMouseOut="htm()">
main doc)</a>
</h2>


<script language="javascript">
<!--
plot="tc.act.mots";
basin="%s";
dtg1="%s";
dtg2="%s";
//tcexpr="tcstr";
tcexpr="tcace";
function swap() 
{
value = "plt/climo/" + plot + "." + basin + "." + dtg1 + "." + dtg2 + "." + tcexpr + ".png";
if (value != '') if (document.images) document.images.myImage.src = value;
//alert(value);
}
// -->
</script>

<table>
<tr>

<td>
<input type='button' class='btn200'
onMouseOver="className='btn200over';" onMouseOut="className='btn200';"
value='sTCd: scaled TC days' name=tctrk
onClick="tcexpr='tcstr',swap();">
</td>

<td>
<input type='button' class='btn200'
onMouseOver="className='btn200over';" onMouseOut="className='btn200';"
value='sACEd: scaled ACE days' name=tctrk
onClick="tcexpr='tcace',swap();">
</td>

<td>
<input type='button' class='btn200'
onMouseOver="className='btn200over';" onMouseOut="className='btn200';"
value='HUsACEd: Hurricane scaled ACE days' name=tctrk
onClick="tcexpr='huace',swap();">
</td>

</tr>
</table>

<table border >


<td valign=top>
<img name="myImage">
</td>


<td valign=top>

<table class="button2">

<tr><td class="bdesc"  onMouseOver="stm(Text['%s'],Style[20])" onMouseOut="htm()">
Basin
</td></tr>

<form>

"""%(htmlin1)


    def basinbutton(lbasin,ubasin,bchecked):
        bhtml="""        
<tr>
<td class="b%s">
<input type="radio" name="tcact" %s onClick='basin="%s",swap();'>%s
</td>
</tr>
"""%(lbasin,bchecked,lbasin,ubasin)
        return(bhtml)

    html2=""
    for basin in basins:
        bchecked=''
        if(basin == basins[0]): bchecked='checked'
        ubasin=basin
        lbasin=ubasin.lower()
        
        html2=html2+basinbutton(lbasin,ubasin,bchecked)

    html3="""
</form>
</table>
</td>

<td valign="top">

<table class="button2">
<form>

<tr><td class="bdesc">
Nyr
</td></tr>
"""

    ny=len(byyyymmtss)
    
    nytss=YearsBackClimoTss

    for n in range(0,ny):
        byyyymmts=byyyymmtss[n]
        eyyyymmts=eyyyymmtss[n]
        yearback=nytss[n]

        clsyear='byear'
        chkon=''
        if(n == 0):
            clsyear='byearcur'
            chkon='checked'
        
        htmltd="""
<tr>
<td class="%s">
<input type="radio" name="tcact" %s onClick='dtg1="%s",dtg2="%s";swap();'>%02d
</td>
</tr>"""%(clsyear,chkon,byyyymmts,eyyyymmts,int(yearback))

        html3=html3+htmltd
        n=n-1

    html3=html3+"""
</tr>

</td></table>

<script language="JavaScript" type="text/javascript" src="js/wz_tooltip.js"></script>
</body>
</html>
"""%(htmlin3)

    html=html1+html2+html3

    hname="tc.act.climo.ts.%s.%s.htm"%(year,lhemi)
    
    if(dowrite):
        writehtml(hdir,hname,html)
    else:
        print html

    return(html)


#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#2222222222222222222222222222222222222222222222222222222222222222222222
#
#  TC activity maps (tc2.htm)
#
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

def HtmlTCActMaps(dowrite=1):

    nyback=YearsBackClimo

    hdir=hdirbase

    yearp1=str(int(year)+1)
    yearm0=year

    titleTAB="TCact MAPS"
    title="TCact MAPS -- scaled sACEd, sHurACEd and sTCd maps thru: %s"%(eyyyymmdd)

    if(hemi=='NHEM'):

        bmmdd='0101'
        
        eyyyy=int(year)
        byyyy=eyyyy-nyback
        bdtgm0s=[]
        edtgm0s=[]
        yearm0s=[]
        
        for yyyy in range(byyyy,eyyyy+1):

            bdtgm0=str(yyyy) + bmmdd

            emmdd0=bmmdd
            if(emmdd != bmmdd):
                emmdd0=emmdd
                edtgm0=str(yyyy) + emmdd0
            else:
                emmdd0=bmmdd
                edtgm0=str(yyyy+1) + emmdd0
                
            yearm0=str(yyyy)

            bdtgm0s.append(bdtgm0)
            edtgm0s.append(edtgm0)
            yearm0s.append(yearm0)

        hbasins=ClimoBasinsHemi['NHS']
        basins=[]
        for basin in hbasins:
            basins.append(basin.upper())

    elif(hemi == 'SHEM'):

        bmmdd='0701'

        eyyyy=int(year)
        byyyy=eyyyy-nyback
        
        # -- case where shem year > curyear -- before the shift calendar year = shem season year
        #
        if(int(year) > int(curyear)): eyyyy=int(curyear)
        bdtgm0s=[]
        edtgm0s=[]
        yearm0s=[]
        
        for yyyy in range(byyyy,eyyyy+1):

            yyyym1=yyyy-1
            
            # -- before shem year = current year
            #
            if(int(year) > int(curyear)): yyyym1=yyyy-0
            bdtgm0=str(yyyym1) + bmmdd
            emmdd0=bmmdd
            if(emmdd != bmmdd or emmdd == bmmdd):
                emmdd0=emmdd
                yyyyemd=yyyy+0
                edtgm0=str(yyyyemd) + emmdd0
            # -- 20170123 -- not sure what case this is for...year handled above...
            else:
                emmdd0=bmmdd
                edtgm0=str(yyyy+1) + emmdd0
                
            yearm0=str(yyyy)

            bdtgm0s.append(bdtgm0)
            edtgm0s.append(edtgm0)
            yearm0s.append(yearm0)

        hbasins=ClimoBasinsHemi['SHS']
        basins=[]
        for basin in hbasins:
            basins.append(basin.upper())



    else:

        print 'EEEEEE invalid hemi: %s'%(hemi)
        sys.exit()

    htmlin1=(titleTAB,title,lhemi,bdtgm0s[-1],edtgm0s[-1],lhemi)
    
    htmlin2=()
    
    html1="""
<html>
<head>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VG0RC3XML9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-VG0RC3XML9');
</script>



<title>
%s
</title>

<link rel="stylesheet" type="text/css" href="../css/tcsitrep.css">
<!-- ********** tooltip script -->
<script language="javascript1.2" src="../js/tooltip.js" type="text/javascript"></script>

</head>

<body text="black" link="blue" vlink="purple" bgcolor=#fcf1da onLoad="swap()">

<!-- ********** tooltip script -->
<div id="TipLayer" style="visibility:hidden;position:absolute;z-index:1000;top:-100"></div>
<script language="JavaScript1.2" src="../js/tctips.js" type="text/javascript"></script>

<h2>
%s
<font size=-1>(<a href="../doc/" onMouseOver='stm(["","return to main doc"],Style[23])' onMouseOut="htm()">
main doc)</a>
</h2>


<script language="javascript">
<!--
plot="tc.act.llmap";
basin="%s";
dtg1="%s";
dtg2="%s";
//tcexpr="tcstr";
tcexpr="tcace";
function swap() 
{
value = "plt/climo/" + plot + "." + basin + "." + dtg1 + "." + dtg2 + "." + tcexpr + ".png";
if (value != '') if (document.images) document.images.myImage.src = value;
//alert(value);
}
// -->
</script>

<table>
<tr>


<td>
<input type='button' class='btn200'
onMouseOver="className='btn200over';" onMouseOut="className='btn200';"
value='sACEd: scaled ACE days' name=tctrk
onClick="tcexpr='tcace',swap();">
</td>

<td>
<input type='button' class='btn200'
onMouseOver="className='btn200over';" onMouseOut="className='btn200';"
value='HUsACEd: Hurricane scaled ACE days' name=tctrk
onClick="tcexpr='huace',swap();">
</td>
<td>

<input type='button' class='btn200'
onMouseOver="className='btn200over';" onMouseOut="className='btn200';"
value='sTCd: scaled TC days' name=tctrk
onClick="tcexpr='tcstr',swap();">
</td>

</tr>
</table>

<table width=700  border >



<td valign=top>
<img name="myImage">
</td>

<td valign=top>

<table class="button2">
<tr><td class="bdesc"  onMouseOver="stm(Text['%s'],Style[20])" onMouseOut="htm()">
Basin
</td></tr>

<form>
"""%(htmlin1)

    def basinbutton(lbasin,ubasin,bchecked):

        bhtml="""        
<tr>
<td class="b%s">
<input type="radio" name="tcact" %s onClick='basin="%s",swap();'>%s
</td>
</tr>
"""%(lbasin,bchecked,lbasin,ubasin)
        return(bhtml)

    html2=""
    for basin in basins:
        bchecked=''
        if(basin == basins[0]): bchecked='checked'
        ubasin=basin
        lbasin=ubasin.lower()
        
        html2=html2+basinbutton(lbasin,ubasin,bchecked)



    html3="""
</form>
</table>
</td>

<td valign="top">

<table class="button2">
<form>

<tr><td class="bdesc">
Year
</td></tr>
"""

    ny=len(bdtgm0s)-1
    n=ny
    
    while(n>0):
        bdtgm0=bdtgm0s[n]
        edtgm0=edtgm0s[n]
        yearm0=yearm0s[n]

        clsyear='byear'
        chkon=''
        if(n == ny):
            clsyear='byearcur'
            chkon='checked'
        
        htmltd="""
<tr>
<td class="%s">
<input type="radio" name="tcact" %s onClick='dtg1="%s",dtg2="%s";swap();'>%s
</td>
</tr>"""%(clsyear,chkon,bdtgm0,edtgm0,yearm0)

        html3=html3+htmltd
        n=n-1

        if(n%NyearBreak == 0 and n <= NyearBreak and n != 0):
            html3=html3+"""
</table>
</td>
<td valign="top">
<table class="button2">
<tr><td class="bdesc">
Year
</td></tr>

"""


    html3=html3+"""

</form>
</table>
</td>

</tr>

</td></table>

<script language="JavaScript" type="text/javascript" src="js/wz_tooltip.js"></script>
</body>
</html>

"""

    html=html1+html2+html3

    #
    # 20040825 browser doesn't like .map. ...
    #
    hname="tc.act.climo.llmap.%s.%s.htm"%(year,lhemi)
    
    if(dowrite):
        writehtml(hdir,hname,html)
    else:
        print html

    return(html)

#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#1111111111111111111111111111111111111111111111111111111111111111111111
#
#  TC activity spectrograph html (tc1.htm)
#
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

def HtmlTCActSpec(dowrite=1):

    nyback=YearsBackClimo
    
    hdir=hdirbase

    titleTAB="TCact SPEC"
    title="TCact SPEC -- %s %s Spectrograph as of: %s"%(hemi,year,eyyyymmdd)
    
    if(lhemi=='nhem'):

        eyyyy=int(year)
        byyyy=eyyyy-nyback
        bdtgm0s=[]
        edtgm0s=[]
        yearm0s=[]
        
        for yyyy in range(byyyy,eyyyy+1):

            bdtgm0=str(yyyy) + '010100'
            edtgm0=str(yyyy+1) + '010100'
            yearm0=str(yyyy)

            bdtgm0s.append(bdtgm0)
            edtgm0s.append(edtgm0)
            yearm0s.append(yearm0)

        
            
    elif(lhemi=='shem'):
        
        eyyyy=int(year)
        byyyy=eyyyy-nyback
        bdtgm0s=[]
        edtgm0s=[]
        yearm0s=[]
        
        for yyyy in range(byyyy,eyyyy+1):

            bdtgm0=str(yyyy-1) + '070100'
            edtgm0=str(yyyy) + '070100'
            yearm0=str(yyyy)

            bdtgm0s.append(bdtgm0)
            edtgm0s.append(edtgm0)
            yearm0s.append(yearm0)


    html="""
<html>
<head>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VG0RC3XML9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-VG0RC3XML9');
</script>

<title>
%s
</title>

<link rel="stylesheet" type="text/css" href="../css/tcsitrep.css">
<!-- ********** tooltip script -->
<script language="javascript1.2" src="../js/tooltip.js" type="text/javascript"></script>

</head>


<body text="black" link="blue" vlink="purple" bgcolor=#fcf1da onLoad="swap()">


<!-- ********** tooltip script -->
<div id="TipLayer" style="visibility:hidden;position:absolute;z-index:1000;top:-100"></div>
<script language="JavaScript1.2" src="js/tctips.js" type="text/javascript"></script>

<h2>
%s
<font size=-1>(<a href="../doc/" onMouseOver='stm(["","return to main doc"],Style[23])' onMouseOut="htm()">
main doc)</a>
</h2>


<script language="javascript">
<!--
plot="tc.act.spec";
dtg1="%s";
dtg2="%s";
function swap() 
{
value = "plt/climo/" + plot + "." + dtg1 + "." + dtg2 + "." + "BT.final.png";
if (value != '') if (document.images) document.images.myImage.src = value;
//alert(value);
}
// -->
</script>

<table border>

<td valign=top>
<img name="myImage">
</td>

<td valign=top>

<table class="button2">
<tr><td class="bdesc">
Year
</td></tr>

<form>
"""%(titleTAB,title,bdtgm0s[-1],edtgm0s[-1])


    ny=len(bdtgm0s)-1
    n=ny
    
    while(n>0):
        bdtgm0=bdtgm0s[n]
        edtgm0=edtgm0s[n]
        yearm0=yearm0s[n]

        clsyear='byear'
        chkon=''
        if(n == ny):
            clsyear='byearcur'
            chkon='checked'
        
        htmltd="""
<tr>
<td class="%s">
<input type="radio" name="tcact" %s onClick='dtg1="%s",dtg2="%s";swap();'>%s
</td>
</tr>"""%(clsyear,chkon,bdtgm0,edtgm0,yearm0)

        html=html+htmltd
        n=n-1

        if(n%NyearBreak == 0 and n <= NyearBreak and n != 0):
            html=html+"""
</table>
</td>
<td valign="top">
<table class="button2">
<tr><td class="bdesc">
Year
</td></tr>

"""

    html=html+"""
</form>
</table>

</td>

</td></table>

<script language="JavaScript" type="text/javascript" src="js/wz_tooltip.js"></script>
</body>
</html>
"""


    hname="tc.act.climo.spec.%s.%s.htm"%(year,lhemi)

    if(dowrite):
        writehtml(hdir,hname,html)
    else:
        print html

    return(html)



def HtmlKeyVeri(dowrite=1,bstmid='null'):

    hdir=hdirbase

    htmlin=(year,lhemi,year,lhemi,year,lhemi,year,lhemi)
    
    html="""
<html>
<head>
<title>
TC Plot Keys -- Track
</title>

<link rel="stylesheet" type="text/css" href="../css/tcsitrep.css">
<!-- ********** tooltip script -->
<script language="javascript1.2" src="../js/tooltip.js" type="text/javascript"></script>
</head>


<body text="black" link="blue" vlink="purple" bgcolor=#fcf1da onLoad="swap()">

<!-- ********** tooltip script -->
<div id="TipLayer" style="visibility:hidden;position:absolute;z-index:1000;top:-100"></div>
<script language="JavaScript1.2" src="js/tctips.js" type="text/javascript"></script>

<table class="models" border=0 >

<tr>
<th>
TC Veri Stat Keys -- Forecast Error (FE) Plot
<a href="tc.veri.stat.%s.%s.htm" onMouseOver='stm(["","TC Verification doc"],Style[23])' onMouseOut="htm()">
[return to TC Veri Stats]
</a>
</th>
</tr>

<tr>
<td valign=top>
<img src="../plt/key.veri.plot.fe.png">
</td>
</tr>



<tr>
<th>
TC Veri Stat Keys -- CTE/ATE rings/stats
<a href="tc.veri.stat.%s.%s.htm" onMouseOver='stm(["","TC Verification doc"],Style[23])' onMouseOut="htm()">
[return to TC Veri Stats]
</a>
</th>
</tr>

<tr>
<td valign=top>
<img src="../plt/key.veri.plot.cte.ate.png">
</td>
</tr>


<tr>
<th>
TC Veri Stat Keys -- Vmax (Intensity) Error (VE) Plot
<a href="tc.veri.stat.%s.%s.htm" onMouseOver='stm(["","TC Verification doc"],Style[23])' onMouseOut="htm()">
[return to TC Veri Stats]
</a>
</th>
</tr>

<tr>
<td valign=top>
<img src="../plt/key.veri.plot.ve.png">
</td>
</tr>



<tr>
<th>
TC Veri Stat Keys -- %% Improvement over CLIPER (%%Impclp) Plot
<a href="tc.veri.stat.%s.%s.htm" onMouseOver='stm(["","TC Verification doc"],Style[23])' onMouseOut="htm()">
[return to TC Veri Stats]
</a>
</th>
</tr>

<tr>
<td valign=top>
<img src="../plt/key.veri.plot.impclp.png">
</td>
</tr>



</table>

<script language="JavaScript" type="text/javascript" src="js/wz_tooltip.js"></script>
</body>
</html>
"""%(htmlin)

    hname="key.veri.htm"

    if(dowrite):
        writehtml(hdir,hname,html)
    else:
        print html


def HtmlKeyTrack(dowrite=1,bstmid='null'):

    hdir=hdirbase

    htmlin=(year,lhemi)
    
    html="""
<html>
<head>
<title>
TC Plot Keys -- Track
</title>

<link rel="stylesheet" type="text/css" href="../css/tcsitrep.css">
<!-- ********** tooltip script -->
<script language="javascript1.2" src="../js/tooltip.js" type="text/javascript"></script>
</head>

<body text="black" link="blue" vlink="purple" bgcolor=#fcf1da onLoad="swap()">

<!-- ********** tooltip script -->
<div id="TipLayer" style="visibility:hidden;position:absolute;z-index:1000;top:-100"></div>
<script language="JavaScript1.2" src="js/tctips.js" type="text/javascript"></script>

<table class="models" border=0 >

<tr>
<th>
TC Plot Keys -- Track
<a href="tc.trk.%s.%s.htm" onMouseOver='stm(["","TC track doc"],Style[23])' onMouseOut="htm()">
[return to TC tracks]
</a>
</td>
</tr>

<tr>
<td valign=top>
<img src="../plt/key.track.plot.png">
</td>
</tr>

</table>
<script language="JavaScript" type="text/javascript" src="js/wz_tooltip.js"></script>
</body>
</html>
"""%(htmlin)

    hname="key.track.htm"

    if(dowrite):
        writehtml(hdir,hname,html)
    else:
        print html



#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#5555555555555555555555555555555555555555555555555555555555555555555555
#
#  TC track html (tc5.htm)
#
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

def HtmlTCTrk(dowrite=1,bstmid='null'):

    hdir=hdirbase
    jdir=jdirbase

    pycards=[]
    rptopt=0

    ndir=w2.TcNamesDatDir
    sys.path.append(ndir)

    impcmd="from TCnames%s import tcnames"%(year)
    exec(impcmd)

    (tcs,tcstats,allhtml,alljs,bstmid)=TCsByBasin(
        year,basinopt,pycards,rptopt,tchash=tcnames)

    (html,js,hname)=HtmlJsTCTrk(allhtml,alljs,tcstats,year,hemi,bstmid,eyyyymmdd)

    if(dowrite):
        writehtml(hdir,hname,html)
    else:
        print html

    jname='tctips.js'
    jpath=jdir+'/'+jname
    j=open(jpath,'w')
    j.writelines(js)
    j.close()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
#  TC track spectrograph html (tc5.htm)
#
#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

def HtmlTCCssJs(dowrite=1):

    
    #
    # do .css .js
    #

    cname='tcsitrep.css'
    cpath=cdirbase+'/'+cname
    css=TcSitrepCss
    c=open(cpath,'w')
    c.writelines(css)
    c.close()

    jname='tooltip.js'
    jpath=jdirbase+'/'+jname
    ttjs=ToolTipJs
    j=open(jpath,'w')
    j.writelines(ttjs)
    j.close()

    jname='wz_tooltip.js'
    jpath=jdirbase+'/'+jname
    ttjs=WZ_ToolTipJs
    j=open(jpath,'w')
    j.writelines(ttjs)
    j.close()


def HtmlTCPlotFiles(doclean=1,dtypeopt=None):

    if(dtypeopt != None):
        dtypes=[dtypeopt]
    else:
        dtypes=['climo','veri','track','rpt']

    #
    # function to glob than cp files 
    #
    def cpfiles(sdir,tdir,mask,ropt=''):

        files=glob.glob("%s/%s"%(sdir,mask))

        for file in files:
            cmd="cp %s %s/."%(file,tdir)
            mf.runcmd(cmd,ropt)

    def rmfiles(sdir,mask,ropt=''):

        files=glob.glob("%s/%s"%(sdir,mask))

        for file in files:
            cmd="rm %s"%(file)
            mf.runcmd(cmd,ropt)


    ropt='norun'
    ropt=''
    
    for dtype in dtypes:

        sdir=spdirbase+"/%s/%s.%s"%(dtype,year,lhemi)
        tdir=tpdirbase+"/%s"%(dtype)
        
        maskpng="*.png"
        maskgif="*.gif"
        masks=[maskpng,maskgif]
        
        if(dtype == 'rpt'):
            sdir=srdirbase
            tdir=trdirbase
            masks=[]
            masks.append("*.%s.%s.jtwc.h*txt"%(year,lhemi))
            masks.append("*.%s.%s.nhc.pure.*txt"%(year,lhemi))

        mf.ChkDir(tdir,'mk')

        for mask in masks:
            
            if(mf.ChkDir(tdir) == 0 or mf.ChkDir(sdir) == 0):
                print "EEE either tdir: %s or sdir: %s is not there...."%(tdir,sdir)
                sys.exit()

            if(doclean):
                rmfiles(tdir,mask)
            
            cpfiles(sdir,tdir,mask,ropt)
        
    

    return()
