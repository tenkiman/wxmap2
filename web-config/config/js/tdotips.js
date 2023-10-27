

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

MODEL['ecm']=["ECMWF IFS (ops)",
"\
ECMWF Integrated Forecast System<br>\
twice-daily deterministic run<br>\
[T<sub>L</sub>799 L91]<br>\
<br>\
"]

MODEL['cmc']=["CMC CEM",
"\
CMC CEM<br>\
twice-daily deterministic run<br>\
[T99 L38]<br>\
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

CLIMO['wxmap']=["WxMAP2",
"\
return to main wxmap page<br>\
"]


CLIMO['mo.clm']=["WxMAP2 Mon Climo",
"\
go the monthly mean<br>\
wind climo <br>\
"]

CLIMO['nhcaor']=["WxMAP2",
"\
go to NHC/CPC AOR Cur Climo<br>\
"]

CLIMO['jtwcaor']=["WxMAP2",
"\
go to JTWC AOR Cur Climo<br>\
"]

CLIMO['cur.clm']=["WxMAP2 Cur Climo",
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



