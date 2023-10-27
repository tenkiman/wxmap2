mainpage='.';
clmroot=mainpage + '/web_clm' 
htype='main';
area='tropwpac';
aor='nhcaor';

model="gfs";
dtg="2008051212";

dtype="clm";
plevel="200";
ptype="loop";
plot='uas';
tau='000';

baseurl='http://tenki.wxmap2'

yyyy_basin='2006.nhem';
yyyy_basin='2007.shem';
yyyy_basin='2007.nhem';
yyyy_basin='2008.shem';
yyyy_basin='2008.nhem';
yyyy_basin='2009.shem';
yyyy_basin='2009.nhem';
yyyy_basin='2010.shem';
yyyy_basin='2010.nhem';
yyyy_basin='2011.shem';
yyyy_basin='2011.nhem';
yyyy_basin='2012.shem';
yyyy_basin='2012.nhem';
yyyy_basin='2013.shem';
yyyy_basin='2013.nhem';
yyyy_basin='2014.shem';
yyyy_basin='2015.nhem';
yyyy_basin='2016.shem';
yyyy_basin='2016.nhem';
yyyy_basin='2017.shem';
yyyy_basin='2017.nhem';
yyyy_basin='2018.shem';
yyyy_basin='2018.nhem';
yyyy_basin='2019.shem';
yyyy_basin='2019.nhem';
yyyy_basin='2020.shem';
yyyy_basin='2020.nhem';

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

function loadW2Html(value,opentype) 
{
  if(opentype == 'window') {
      window.open(value);
  } else if (opentype == 'page') {
      parent.location.href=cvalue;
  } else {   
      parent.location.href=value;
  }
//alert(value);
}



function getW2Url(htype) 

{
  if(htype == 'main') {
    value='.';
  } else if (htype == 'wxmap.home.old') {
    value=mainpage+'/' + 'wx.old.' + dtg + '.htm';
  } else if (htype == 'wxmap.archive') {
    value=mainpage+'/' + 'wxmap.web.archive.htm';
  } else if (htype == 'wxmap.fnmoc') {
    value='https://www.fnmoc.navy.mil/wxmap_cgi/index.html';
  } else if (htype == 'wxmap.cola') {
    value='http://wxmaps.org';	
  } else if (htype == 'wxmap.pzal') {
    value='https://pzal.nmci.navy.mil/wxmap/';	

  } else if (htype == 'hart.cps') {
    value='http://moe.met.fsu.edu/cyclonephase/help.html';	

  } else if (htype == 'tigge.cxml') {
    value='https://www.cawcr.gov.au/research/cyclone-exchange/';

  } else if (htype == 'tuttlog') {
    value='http://tuttlog.wordpress.com/';	

  } else if (htype == 'ships.lgem') {
    value='http://ftp.nhc.noaa.gov/atcf/stext/';	

  } else if (htype == 'ncep.model.veri') {
    value='http://www.emc.ncep.noaa.gov/gmb/STATS/STATS.html';	

  } else if (htype == 'ncep.obs.conv') {
    value='http://www.emc.ncep.noaa.gov/gmb/gdas/convention/index.html';

  } else if (htype == 'ncep.obs.sat') {
    value='http://www.emc.ncep.noaa.gov/gmb/gdas/radiance/su/opr/index.html';	
    value='https://www.emc.ncep.noaa.gov/gmb/gdas/radiance/index.html';

  } else if (htype == 'ncep.obs.gdas') {
    value='http://www.emc.ncep.noaa.gov/gmb/ssaha/';	
    value='https://www.emc.ncep.noaa.gov/gmb/gdas/index.html'

// interactive interface to forecast performance + maps including ECMWF
  } else if (htype == 'ncep.emc.stat.maps') {
    value='http://www.emc.ncep.noaa.gov/gmb/STATS_vsdb/';	

// base page with links to obs counts + stats
  } else if (htype == 'ukmo.obs') {
    value='http://www.metoffice.gov.uk/research/nwp/observations/index.html';	

  } else if (htype == 'tc.model.veri.stat') {
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.veri.stat.' + yyyy_basin + '.htm';	
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.veri.stat.' + yyyy_basin + '.htm';	

  } else if (htype == 'tc.model.veri.trk') {
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.trk.' + yyyy_basin + '.htm';	
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.trk.' + yyyy_basin + '.htm';	

  } else if (htype == 'tc.act.llmap') {
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.act.climo.llmap.' + yyyy_basin + '.htm';	
    value='tc/sitrep/cur' + '/tc.act.climo.llmap.' + yyyy_basin + '.htm';	

  } else if (htype == 'tc.act.spec') {
    value='tc/sitrep/cur' + '/tc.act.climo.spec.' + yyyy_basin + '.htm';	

  } else if (htype == 'tc.act.ts') {
    value='tc/sitrep/cur' + '/tc.act.climo.ts.' + yyyy_basin + '.htm';	

  } else if (htype == 'cires.tcgen.fcst') {
    value='http://cires.colorado.edu/~rpaul/genesis/tcgenforecast.html';	

  } else if (htype == 'atcf.carq') {
    value='http://www.nrlmry.navy.mil/atcf_web/index1.html';	
    value='http://www.nrlmry.navy.mil/atcf_web/docs/current_storms/?C=M;O=D'; // need login-passwd
    value='http://www.nrlmry.navy.mil/atcf_web/docs/carqs/' + dtgcur.substr(0,4);	

  } else if (htype == 'nrl.tc.coamps') {
    value='http://www.nrlmry.navy.mil/coamps-web/web/tc';	

  } else if (htype == 'fnmoc.tc.posit') {
    value='https://www.fnmoc.navy.mil/tc_tracks/html/index.html';	


// hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh hfip

  } else if (htype == 'tc.hfip.tceps') {
    value='http://tceps.wxmap2.com';	

  } else if (htype == 'tc.hfip.tcgen') {
    value='http://tcgen.wxmap2.com';	

  } else if (htype == 'tc.hfip.tcdiag') {
    value='http://tcdiag.wxmap2.com';	

  } else if (htype == 'tc.hfip.jtdiag') {
    value='http://jtdiag.wxmap2.com';	

  } else if (htype == 'tc.hfip.gfsenkf') {
//    value='http://ruc.noaa.gov/hfip/gfsenkf';	
    value='http://www.esrl.noaa.gov/psd/forecasts/gfsenkf/';	



// nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn navy sat

  } else if (htype == 'nrl.sat.troplant') {
      value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=atlantic&SECTOR=tropics&AGE=Latest&SIZE=Full&PRODUCT=ir&PATH=pacific/western/tropics/ir_color&ANIM_TYPE=Instant&DISPLAY=Single&TITLE=Region/Sector';

  } else if (htype == 'nrl.sat.tropepac') {
      value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=pacific&SECTOR=eastern&AGE=Latest&SIZE=Full&PRODUCT=ir_color&PATH=pacific/eastern/tropics/ir_color&buttonPressed=Animate&ANIM_TYPE=Instant';
  } else if (htype == 'nrl.sat.tropwpac') {
      value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=pacific&SECTOR=western/tropics&AGE=Latest&SIZE=Full&PRODUCT=ir_color&PATH=/pacific/western/tropics/ir_color&ANIM_TYPE=Instant&DISPLAY=Single&TITLE=Region/Sector';

  } else if (htype == 'usn.sat.nmfc-jtwc') {
      value='http://metocph.nmci.navy.mil/animator.php';

// nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn ncar

  } else if (htype == 'ncar.tcgp') {
      value='http://www.ral.ucar.edu/hurricanes/realtime/current/';



// ccccccccccccccccccccccccccccccccccccccccccccccccccc cira 

  } else if (htype == 'cira.tc') {
      value='http://rammb.cira.colostate.edu/products/tc_realtime/index.asp';

  } else if (htype == 'cira.tc.vigh') {
      value='http://euler.atmos.colostate.edu/~vigh/guidance/index.htm';

  } else if (htype == 'cira.ramsdis') {
    value='http://rammb.cira.colostate.edu/ramsdis/online/tropical.asp';

  } else if (htype == 'cira.tcfa') {
      value='http://rammb.cira.colostate.edu/projects/gparm/';

  } else if (htype == 'cira.prw') {
      value='http://amsu.cira.colostate.edu/tpw/';

// sssssssssssssssssssssssssssssssssssssssssssssssss nesdis ssd

  } else if (htype == 'ssd.troplant.vis') {
      value='http://www.ssd.noaa.gov/goes/east/tatl/loop-vis.html';

  } else if (htype == 'ssd.troplant.ir') {
      value='http://www.ssd.noaa.gov/goes/east/tatl/loop-avn.html';

  } else if (htype == 'ssd.tropepac.vis') {
      value='http://www.ssd.noaa.gov/goes/west/tpac/loop-vis.html';

  } else if (htype == 'ssd.tropepac.ir') {
      value='http://www.ssd.noaa.gov/goes/west/tpac/loop-avn.html';

// hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh hrd

  } else if (htype == 'hrd.hwind') {
      value='http://www.aoml.noaa.gov/hrd/data_sub/wind2008.html';

//rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr google.earth recon

  } else if (htype == 'troplant.recon') {
      value='http://tropicalatlantic.com/recon/#gerecon';

//fffffffffffffffffffffffffffffffffffffffffff gsd fim model

  } else if (htype == 'gsd.fim8.wxmap') {
      value='http://fim.noaa.gov/fim244';

  } else if (htype == 'gsd.fim9.wxmap') {
      value='http://fim.noaa.gov/fim244TACC';

  } else if (htype == 'ecmwf.72.wpac') {
    value='http://www.ecmwf.int/products/forecasts/d/charts/medium/deterministic/msl_uv850_z500!Wind%20850%20and%20mslp!72!Asia!pop!od!oper!public_plots!/';	

  } else if (htype == 'ecmwf.72.na') {
    value='http://www.ecmwf.int/products/forecasts/d/charts/medium/deterministic/msl_uv850_z500!Wind%20850%20and%20mslp!72!North%20America!pop!od!oper!public_plots!/';	

  } else if (htype == 'ecmwf.obs') {
    value='http://www.ecmwf.int/products/forecasts/d/charts/monitoring/coverage/dcover/';

  } else if (htype == 'fnmoc.obs') {
    value='http://usgodae2.fnmoc.navy.mil/cvrg/index_java_script.html';

  } else if (htype == 'ecmwf.tc') {
    value='https://www.ecmwf.int/en/forecasts/charts/tcyclone/'

  } else if (htype == 'ecmwf.tc.tigge') {
      value='ftp://tigge:tigge@tigge-ldm.ecmwf.int/cxml/';

  } else if (htype == 'fsu.xt-tc') {
    value='http://moe.met.fsu.edu/cyclonephase/';

  } else if (htype == 'mo.clm') {
    value=clmroot+'/' + 'monthly/wx.clm.mo.htm';
  } else if (htype == 'cur.clm') {
    value=clmroot+'/' + 'wx.clm.cur'+'.'+ aor + '.htm';
  } else if (htype == 'cpc.mjo.anim') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/ir_anim_monthly.shtml';
  } else if (htype == 'cpc.mjo.disc') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjoupdate.pdf';
  } else if (htype == 'cpc.mjo.fcst') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjo_chi.shtml';

  } else if (htype == 'area') {
    value=mainpage+'/' + model + '.' + area + '.' + dtg + '.htm';
  } else if (htype == 'arealoop') {
    value=mainpage+'/web_' + model + '/' + dtg + '/' + model + '.movie.' + plot + '.' + area + '.htm';
  } else if (htype == 'areatau0') {
    value=mainpage+'/web_' + model + '/' + dtg + '/' + model + '.' + plot + '.000.' + area + '.htm';
  } else if (htype == 'areaallmap') {
    value=mainpage+'/web_' + model + '/' + dtg + '/' + model + '.allmap.' + tau + '.' + area + '.htm';
  } else if (htype == 'areasst') {
    value=mainpage+'/web_' + model + '/' + dtg + '/' + 'ngp.sst.000.' + area + '.htm';
  } else if (htype == 'areacur') {
    value=mainpage+'/web_' + model + '.' + area + '.htm';
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
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmswv.GIF';
  } else if (htype == 'cimssvort' && area == 'tropwpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmsvor.GIF';
  } else if (htype == 'cimssshr' && area == 'tropwpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmsshr.GIF';

  } else if (htype == 'cimssup' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9wvir.GIF';
  } else if (htype == 'cimssvort' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9vor.GIF';
  } else if (htype == 'cimssshr' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9shr.GIF';

  } else if (htype == 'cimssup' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8wvir.GIF';
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8wvir.GIF';
  } else if (htype == 'cimssvort' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8vor4.GIF';
  } else if (htype == 'cimssshr' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8shr.GIF';

  } else if (htype == 'cimssup' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5wv.GIF';
  } else if (htype == 'cimssvort' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5vor.GIF';
  } else if (htype == 'cimssshr' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5shr.GIF';

  } else if (htype == 'cimssup' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmswvs3.GIF';
  } else if (htype == 'cimssvort' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsvore.GIF';
  } else if (htype == 'cimssshr' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsshSE.GIF';

  } else if (htype == 'nhc.home') {
    value='http://www.nhc.noaa.gov/';

  } else if (htype == 'prwloop') {
     // new jq value=mainpage+'/' + "prw2.htm#" + area ;
     value=mainpage+'/' + "prwloop.php?area=" + area ;
     value=mainpage+'/' + "prw2.htm#" + area ;


  } else if (htype == 'nhc.tafb.epac') {
      value='http://www.nhc.noaa.gov/index.shtml?epac';

  } else if (htype == 'jtwc.home') {
    value='http://metocph.nmci.navy.mil/jtwc.php';
    value='http://www.usno.navy.mil/JTWC';

  } else if (htype == 'jtwc.tdo.ref') {
    value='https://pzal.npmoc.navy.mil/training/tdo/top21/TDOPAGE21.html';
    value='http://metocph.nmci.navy.mil/jtwc/pubref/reference.html';	

  } else if (htype == 'fnmoc.tc') {
    value='https://www.fnmoc.navy.mil/tcweb/cgi-bin/tc_home.cgi';

  } else if (htype == 'jma.tc') {
    value='http://www.jma.go.jp/en/typh/';

  } else if (htype == 'fnmoc.tc.trk') {
    value='https://www.fnmoc.navy.mil/tc_tracks/html/index.html';

  } else if (htype == 'gts.tc.trk') {
    value='http://weather.noaa.gov/pub/data/raw/fx/';

  } else if (htype == 'fnmoc.qs') {
    value='https://www.fnmoc.navy.mil/CGI/scat.cgi/plot=scat/parentime=current/';

  } else if (htype == 'nesdis.qs') {
    value='http://manati.orbit.nesdis.noaa.gov/quikscat/';

  } else if (htype == 'cpc.ocn.mjo') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/enso.shtml';

  } else if (htype == 'cpc.tc') {
    value='http://www.cpc.ncep.noaa.gov/products/Epac_hurr/';

  } else if (htype == 'cpc.enso') {
      value='http://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ensoyears.shtml';

  } else if (htype == 'nrl.tc') {
      value='http://www.nrlmry.navy.mil/tc_pages/tc_home.html';
      value='http://www.nrlmry.navy.mil/TC.html';

  } else if (htype == 'nrl.tcww3') {
     value=mainpage+'/' + "tcww3.php";

  } else if (htype == 'nrl.sat.tropics.wpac') {
    value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=pacific&SECTOR=western&AGE=Latest&SIZE=Full&PRODUCT=ir_color&PATH=pacific/western/tropics/ir_color&buttonPressed=Animate&ANIM_TYPE=Instant';

  } else if (htype == 'nrl.sat.tropics.lant') {
    value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=atlantic&SECTOR=tropics&AGE=Latest&SIZE=Full&PRODUCT=ir&PATH=pacific/western/tropics/ir_color&ANIM_TYPE=Instant&DISPLAY=Single&TITLE=Region/Sector';

  } else if (htype == 'nrl.sat.tropics.epac') {
    value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=pacific&SECTOR=eastern&AGE=Latest&SIZE=Full&PRODUCT=ir_color&PATH=pacific/eastern/tropics/ir_color&buttonPressed=Animate&ANIM_TYPE=Instant';

  } else if (htype == 'ascat.25') {
    value='http://www.knmi.nl/scatterometer/ascat_osi_25_prod/ascat_app.cgi';

  } else if (htype == 'cpc.global.monsoons') {
    value='http://www.cpc.ncep.noaa.gov/products/Global_Monsoons/Global-Monsoon.shtml';

  } else if (htype == 'cira.rammb.tc') {
    value='http://rammb.cira.colostate.edu/products/tc_realtime/index.asp';

  } else if (htype == 'cira.rammb.tcfa') {
    value='http://rammb.cira.colostate.edu/projects/gparm/';

  } else if (htype == 'cimss.tpw.lant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/tpw/mainTPW.html';
    value='http://cimss.ssec.wisc.edu/tropic/real-time/tpw2/global2/main.html';
    value='http://cimss.ssec.wisc.edu/tropic/real-time/tpw2/natl/main.html';
    value='http://tropic.ssec.wisc.edu/real-time/mimic-tpw/natl/main.html';

  } else if (htype == 'cimss.tc') {
    value='http://cimss.ssec.wisc.edu/tropic2/';

  } else if (htype == 'cira.tpw') {
    value='http://amsu.cira.colostate.edu/tpw/';

  } else if (htype == 'ukmo.tc.eps') {
// very old    value='http://skate.nhc.noaa.gov/%7Ejht/ukmet/';

  } else {
    value=mainpage+'/' + model + '.' + area + '.' + dtg + '.htm';
  }

  return(value)

}

function swaphtm() 

{
  if(htype == 'main') {
    value='.';
  } else if (htype == 'wxmap.home.old') {
    value=mainpage+'/' + 'wx.old.' + dtg + '.htm';
  } else if (htype == 'wxmap.archive') {
    value=mainpage+'/' + 'wxmap.web.archive.htm';
  } else if (htype == 'wxmap.fnmoc') {
    value='https://www.fnmoc.navy.mil/wxmap_cgi/index.html';
  } else if (htype == 'wxmap.cola') {
    value='http://wxmaps.org/pix/forecasts.html';	
  } else if (htype == 'wxmap.pzal') {
    value='https://pzal.nmci.navy.mil/wxmap/';	

  } else if (htype == 'ncep.model.veri') {
    value='http://www.emc.ncep.noaa.gov/gmb/STATS/STATS.html';	

  } else if (htype == 'ncep.obs.conv') {
    value='http://www.emc.ncep.noaa.gov/gmb/gdas/convention/index.html';

  } else if (htype == 'ncep.obs.sat') {
    value='http://www.emc.ncep.noaa.gov/gmb/gdas/radiance/su/opr/index.html';	

  } else if (htype == 'ncep.obs.suru') {
    value='http://www.emc.ncep.noaa.gov/gmb/ssaha/';	

// interactive interface to forecast performance + maps including ECMWF
  } else if (htype == 'ncep.emc.stat.maps') {
    value='http://www.emc.ncep.noaa.gov/gmb/STATS_vsdb/';	

// base page with links to obs counts + stats
  } else if (htype == 'ukmo.obs') {
    value='http://www.metoffice.gov.uk/research/nwp/observations/index.html';	

  } else if (htype == 'tc.model.veri.stat') {
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.veri.stat.' + yyyy_basin + '.htm';	
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.veri.stat.' + yyyy_basin + '.htm';	

  } else if (htype == 'tc.model.veri.trk') {
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.trk.' + yyyy_basin + '.htm';	
    value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.trk.' + yyyy_basin + '.htm';	

  } else if (htype == 'tc.act.llmap') {
      value='http://wxmap.net/mike/tc/sitrep/' + yyyy_basin + '/tc.act.climo.llmap.' + yyyy_basin + '.htm';	
      value='http://ruc.noaa.gov/hfip/tcact/cur' + '/tc.act.climo.llmap.' + yyyy_basin + '.htm';	
      value= baseurl + '/hfip/tcact/cur' + '/tc.act.climo.llmap.' + yyyy_basin + '.htm';	
      value='http://tcact.wxmap2.com/cur/llmap.htm'

  } else if (htype == 'tc.act.spec') {
      value='tc/sitrep/cur' + '/tc.act.climo.spec.' + yyyy_basin + '.htm';	
      value='http://ruc.noaa.gov/hfip/tcact/cur' + '/tc.act.climo.spec.' + yyyy_basin + '.htm';	
      value= baseurl+ '/hfip/tcact/cur' + '/tc.act.climo.spec.' + yyyy_basin + '.htm';	
      value='http://tcact.wxmap2.com/cur/spec.htm'

  } else if (htype == 'tc.act.ts') {
      value='tc/sitrep/cur' + '/tc.act.climo.ts.' + yyyy_basin + '.htm';	
      value='http://ruc.noaa.gov/hfip/tcact/cur' + '/tc.act.climo.ts.' + yyyy_basin + '.htm';	
      value= baseurl + '/hfip/tcact/cur' + '/tc.act.climo.ts.' + yyyy_basin + '.htm';	
      value='http://tcact.wxmap2.com/cur/ts.htm'

  } else if (htype == 'cires.tcgen.fcst') {
    value='http://cires.colorado.edu/~rpaul/genesis/tcgenforecast.html';	

  } else if (htype == 'atcf.carq') {
    value='http://www.nrlmry.navy.mil/atcf_web/index1.html';	
    value='http://www.nrlmry.navy.mil/atcf_web/docs/current_storms/?C=M;O=D';  // need login passwd
    value='http://www.nrlmry.navy.mil/atcf_web/docs/carqs/' + dtgcur.substr(0,4);	

  } else if (htype == 'fnmoc.tc.posit') {
    value='https://www.fnmoc.navy.mil/tc_tracks/html/index.html';	

  } else if (htype == 'ecmwf.72.wpac') {
    value='http://www.ecmwf.int/products/forecasts/d/charts/medium/deterministic/msl_uv850_z500!Wind%20850%20and%20mslp!72!Asia!pop!od!oper!public_plots!/';	

  } else if (htype == 'ecmwf.72.na') {
    value='http://www.ecmwf.int/products/forecasts/d/charts/medium/deterministic/msl_uv850_z500!Wind%20850%20and%20mslp!72!North%20America!pop!od!oper!public_plots!/';	

  } else if (htype == 'ecmwf.obs') {
    value='http://www.ecmwf.int/products/forecasts/d/charts/monitoring/coverage/dcover/';

  } else if (htype == 'fnmoc.obs') {
    value='https://www.fnmoc.navy.mil/PUBLIC/QC/CVRG/index_java_script.html';

  } else if (htype == 'ecmwf.tc') {
    value='http://www.ecmwf.int/products/forecasts/d/tccurrent';

  } else if (htype == 'fsu.xt-tc') {
    value='http://moe.met.fsu.edu/cyclonephase/';

  } else if (htype == 'mo.clm') {
    value=clmroot+'/' + 'monthly/wx.clm.mo.htm';
  } else if (htype == 'cur.clm') {
    value=clmroot+'/' + 'wx.clm.cur'+'.'+ aor + '.htm';
  } else if (htype == 'cpc.mjo.anim') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/ir_anim_monthly.shtml';
  } else if (htype == 'cpc.mjo.disc') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjoupdate.pdf';
  } else if (htype == 'cpc.mjo.fcst') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjo_chi.shtml';

  } else if (htype == 'area') {
    value=mainpage+'/' + model + '.' + area + '.' + dtg + '.htm';
  } else if (htype == 'arealoop') {
    value=mainpage+'/web_' + model + '/' + dtg + '/' + model + '.movie.' + plot + '.' + area + '.htm';
  } else if (htype == 'areatau0') {
    value=mainpage+'/web_' + model + '/' + dtg + '/' + model + '.' + plot + '.000.' + area + '.htm';
  } else if (htype == 'areaallmap') {
    value=mainpage+'/web_' + model + '/' + dtg + '/' + model + '.allmap.' + tau + '.' + area + '.htm';
  } else if (htype == 'areasst') {
    value=mainpage+'/web_' + model + '/' + dtg + '/' + 'ngp.sst.000.' + area + '.htm';
  } else if (htype == 'areacur') {
    value=mainpage+'/web_' + model + '.' + area + '.htm';
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
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmswv.GIF';
  } else if (htype == 'cimssvort' && area == 'tropwpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmsvor.GIF';
  } else if (htype == 'cimssshr' && area == 'tropwpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmsshr.GIF';

  } else if (htype == 'cimssup' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9wvir.GIF';
  } else if (htype == 'cimssvort' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9vor.GIF';
  } else if (htype == 'cimssshr' && area == 'tropepac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9shr.GIF';

  } else if (htype == 'cimssup' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8wvir.GIF';
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8wvir.GIF';
  } else if (htype == 'cimssvort' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8vor4.GIF';
  } else if (htype == 'cimssshr' && area == 'troplant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8shr.GIF';

  } else if (htype == 'cimssup' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5wv.GIF';
  } else if (htype == 'cimssvort' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5vor.GIF';
  } else if (htype == 'cimssshr' && area == 'tropsio') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5shr.GIF';

  } else if (htype == 'cimssup' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmswvs3.GIF';
  } else if (htype == 'cimssvort' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsvore.GIF';
  } else if (htype == 'cimssshr' && area == 'tropswpac') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsshSE.GIF';

  } else if (htype == 'nhc.home') {
    value='http://www.nhc.noaa.gov/';

  } else if (htype == 'prwloop') {
     value=mainpage+'/' + "prwloop.php?area=" + area ;
     value=mainpage+'/' + "prw2.htm#" + area ;


  } else if (htype == 'nhc.tafb.epac') {
    value='http://www.nhc.noaa.gov/tafb-pac.shtml';

  } else if (htype == 'jtwc.home') {
    value='http://metocph.nmci.navy.mil/jtwc.php';
    value='http://www.usno.navy.mil/JTWC';
    value='https://metoc.ndbc.noaa.gov/JTWC';
    value='http://www.metoc.navy.mil/jtwc/jtwc.html';

  } else if (htype == 'jtwc.tdo.ref') {
    value='https://pzal.npmoc.navy.mil/training/tdo/top21/TDOPAGE21.html';
    value='http://metocph.nmci.navy.mil/jtwc/pubref/reference.html';	

  } else if (htype == 'fnmoc.tc') {
    value='https://www.fnmoc.navy.mil/tcweb/cgi-bin/tc_home.cgi';

  } else if (htype == 'jma.tc') {
    value='http://www.jma.go.jp/en/typh/';

  } else if (htype == 'fnmoc.tc.trk') {
    value='https://www.fnmoc.navy.mil/tc_tracks/html/index.html';

  } else if (htype == 'gts.tc.trk') {
    value='http://weather.noaa.gov/pub/data/raw/fx/';

  } else if (htype == 'fnmoc.qs') {
    value='https://www.fnmoc.navy.mil/CGI/scat.cgi/plot=scat/parentime=current/';

  } else if (htype == 'nesdis.qs') {
    value='http://manati.orbit.nesdis.noaa.gov/quikscat/';

  } else if (htype == 'cpc.ocn.mjo') {
    value='http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/enso.shtml';

  } else if (htype == 'cpc.tc') {
    value='http://www.cpc.ncep.noaa.gov/products/Epac_hurr/';

  } else if (htype == 'cpc.enso') {
    value='http://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ensoyears.shtml';

  } else if (htype == 'nrl.tc') {
    value='http://www.nrlmry.navy.mil/tc_pages/tc_home.html';
    value='http://www.nrlmry.navy.mil/TC.html';


  } else if (htype == 'nrl.tcww3') {
     value=mainpage+'/' + "tcww3.php";

  } else if (htype == 'nrl.sat.tropics.wpac') {
    value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=pacific&SECTOR=western&AGE=Latest&SIZE=Full&PRODUCT=ir_color&PATH=pacific/western/tropics/ir_color&buttonPressed=Animate&ANIM_TYPE=Instant';

  } else if (htype == 'nrl.sat.tropics.lant') {
    value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=atlantic&SECTOR=tropics&AGE=Latest&SIZE=Full&PRODUCT=ir&PATH=pacific/western/tropics/ir_color&ANIM_TYPE=Instant&DISPLAY=Single&TITLE=Region/Sector';

  } else if (htype == 'nrl.sat.tropics.epac') {
    value='http://www.nrlmry.navy.mil/tropics-bin/tropics.cgi?REGION=pacific&SECTOR=eastern&AGE=Latest&SIZE=Full&PRODUCT=ir_color&PATH=pacific/eastern/tropics/ir_color&buttonPressed=Animate&ANIM_TYPE=Instant';

  } else if (htype == 'ascat.25') {
    value='http://www.knmi.nl/scatterometer/ascat_osi_25_prod/ascat_app.cgi';

  } else if (htype == 'cpc.global.monsoons') {
    value='http://www.cpc.ncep.noaa.gov/products/Global_Monsoons/Global-Monsoon.shtml';

  } else if (htype == 'cira.rammb.tc') {
    value='http://rammb.cira.colostate.edu/products/tc_realtime/index.asp';

  } else if (htype == 'cira.rammb.tcfa') {
    value='http://rammb.cira.colostate.edu/projects/gparm/';

  } else if (htype == 'cimss.tpw.lant') {
    value='http://cimss.ssec.wisc.edu/tropic/real-time/tpw/mainTPW.html';
    value='http://cimss.ssec.wisc.edu/tropic/real-time/tpw2/global2/main.html';
    value='http://cimss.ssec.wisc.edu/tropic/real-time/tpw2/natl/main.html';
    value='http://tropic.ssec.wisc.edu/real-time/mimic-tpw/natl/main.html';

  } else if (htype == 'cimss.tc') {
    value='http://cimss.ssec.wisc.edu/tropic2/';

  } else if (htype == 'cira.tpw') {
    value='http://amsu.cira.colostate.edu/tpw/';

  } else if (htype == 'ukmo.tc.eps') {
    value='http://skate.nhc.noaa.gov/%7Ejht/ukmet/';

  } else {
    value=mainpage+'/' + model + '.' + area + '.' + dtg + '.htm';
    //alert(value);
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

}

//http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5wv.html
