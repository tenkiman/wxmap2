from PyNIO import nio
import numpy as np
import sys

import mf
from dateutils import dateshift, daterange, splitdate
from datetime import datetime
from spharm import Spharmt, regrid

def getmean(diff,coslats):
   meancoslats = coslats.mean()
   return (coslats*diff).mean()/meancoslats


verb=0
dotest=1
if(not(dotest)):
   dtg1 = sys.argv[1]
   dtg2 = sys.argv[2]
   fhr = int(sys.argv[3])
   var = sys.argv[4]
   try:
      level = int(sys.argv[5])
   except:
      level = None

else:
   dtg1='2009092500'
   dtg2='2009092800'

   var='Z'
   level=500
   fhrs=[120]

   var='U'
   level=200
   fhrs=[72,120]
   fhrs=[72]


FimNioVars= ['CP_4_SFC',
             'CP_4_SFC_acc120h',
             'DPT_4_HYBL',
             'FRICV_4_SFC',
             'GH_4_CBL',
             'GH_4_CTL',
             'GH_4_HYBL',
             'GH_4_ISBL',
             'LGSP_4_SFC_acc120h',
             'LHTFL_4_SFC',
             'MMSP_4_MSL',
             'NLRS_4_SFC',
             'NSWRS_4_SFC',
             'PVV_4_HYBL',
             'PW_4_SFC',
             'P_4_HYBL',
             'RH_4_HYBL',
             'RH_4_ISBL',
             'SHTFL_4_SFC',
             'TP_4_SFC',
             'TP_4_SFC_acc120h',
             'T_4_HYBL',
             'T_4_ISBL',
             'T_4_SFC',
             'UW_4_HYBL',
             'UW_4_ISBL',
             'VW_4_HYBL',
             'VW_4_ISBL',
             'WEASD_4_SFC',
             'lat_4',
             'lon_4',
             'lv_HYBL0',
             'lv_HYBL4',
             'lv_ISBL3']


ddtg=12
use_gsiv = False
ntrunc = None
#ntrunc=40
latbound = 20
latboundx = 80

if var == 'U':
    varname_enkf = 'U_GRD_4_ISBL_10'
    varname_gfs  = 'UGRD_P0_L100_GLL0'
    varname_fim  = 'UW_4_ISBL'
    varnamec     = 'U_GRD_3_ISBL_51'
elif var == 'V':
    varname_enkf = 'V_GRD_4_ISBL_10'
    varname_gfs  = 'VGRD_P0_L100_GLL0'
    varname_fim  = 'UW_4_ISBL'
    varname_fim  = 'VW_4_ISBL'
    varnamec     = 'V_GRD_3_ISBL_51'
elif var == 'Z':
    varname_enkf = 'HGT_4_ISBL_10'
    varname_gfs  = 'HGT_P0_L100_GLL0'
    varnamec     = 'HGT_3_ISBL_51'
    varname_fim  = 'GH_4_ISBL'
    
elif var == 'T':
    varname_enkf = 'TMP_4_ISBL_10'
    varname_gfs = 'TMP_P0_L100_GLL0'
    varname_fim = 'T_4_ISBL'
    varnamec = 'TMP_3_ISBL_51'
elif var == 'P':
    varname_enkf = 'PRMSL_4_MSL_10'
    varname_gfs = 'PRMSL_P0_L101_GLL0'
    varnamec = 'PRMSL_3_MSL_51'

    
fimnh_ac={}
fimtr_ac={}
fimsh_ac={}
fimnh_rms={}
fimtr_rms={}
fimsh_rms={}

fimxnh_ac={}
fimxtr_ac={}
fimxsh_ac={}
fimxnh_rms={}
fimxtr_rms={}
fimxsh_rms={}

gsinh_ac={}
gsitr_ac={}
gsish_ac={}
gsinh_rms={}
gsitr_rms={}
gsish_rms={}

spharmhd = None; spharm1d = None

def DicAppend(dic,fhr,val):

   try:
      dic[fhr].append(val)
   except:
      dic[fhr]=[]
      dic[fhr].append(val)

   return(dic)

   

dtgs=mf.dtgrange(dtg1,dtg2,ddtg)

for dtg in dtgs:
   
   for fhr in fhrs:
      
       dtgv = dateshift(dtg,fhr)

       julday=mf.Dtg2JulianDay(dtg)
       juldayv=mf.Dtg2JulianDay(dtgv)

       yy=dtg[2:4]
       hhmm=dtg[8:10]+'00'
       yyv=dtgv[2:4]
       hhmmv=dtgv[8:10]+'00'
       
       
       enkff = '/lfs1/projects/fim/whitaker/gfsenkf_t190/%s/enkf.t%sz.pgrbf%02i' % (dtg,dtg[8:10],fhr)
       enkfa = '/lfs1/projects/fim/whitaker/gfsenkf_t190/%s/enkf.t%sz.pgrbanl'%(dtgv,dtg[8:10])

       #gsif  = '/lfs1/projects/fim/whitaker/gfs.save/%s/gfs.t%sz.pgrb2f%s' % (dtg,dtg[8:10],repr(fhr))
       #gsia  = '/lfs1/projects/fim/whitaker/gfs.save/%s/gfs.t%sz.pgrb2f00' % (dtgv,dtgv[8:10])

       gsif  = '/public/data/grids/gfs/0p5deg/grib2/%s%s%s%04d'%(yy,julday,hhmm,fhr)
       gsia  = '/public/data/grids/gfs/0p5deg/grib2/%s%s%s%04d'%(yy,juldayv,hhmmv,0)
       
       fimf  = '/lfs1/projects/rtfim/FIM/FIMrun/fim_8_64_240_%s00/post_C/fim/NAT/grib1/%s%s%s%04d'%(dtg,yy,julday,hhmm,fhr)
       fima  = '/lfs1/projects/rtfim/FIM/FIMrun/fim_8_64_240_%s00/post_C/fim/NAT/grib1/%s%s%s%04d'%(dtgv,yy,juldayv,hhmmv,0)

       fimfx  = '/lfs1/projects/rtfim/FIMX/FIMrun/fim_8_64_240_%s00/post_C/fim/NAT/grib1/%s%s%s%04d'%(dtg,yy,julday,hhmm,fhr)
       fimax  = '/lfs1/projects/rtfim/FIMX/FIMrun/fim_8_64_240_%s00/post_C/fim/NAT/grib1/%s%s%s%04d'%(dtgv,yy,juldayv,hhmmv,0)

       varname_enkf=varname_fim
       
       climo = nio.open_file("//lfs0/projects/fim/cmean/cmean_1d.1959"+dtgv[4:8]+".grb")
    
       init_times = climo.variables['initial_time5_encoded'][:].tolist()
       ntimec = init_times.index(float('1959'+dtgv[4:10]))
       lats1 = climo.variables['lat_3'][:]
       lons1 = climo.variables['lon_3'][:]
       nlats1=len(lats1); nlons1=len(lons1)

       if spharm1d is None:
          spharm1d = Spharmt(nlons1,nlats1)

       if level is not None:
           try:
               levdim = climo.variables[varnamec].dimensions[1]
               climolevels = climo.variables[levdim][:].tolist()
               nlevc = climolevels.index(level)
               climodat = climo.variables[varnamec][ntimec,nlevc,:,:]
               doclimo=1
           except:
               doclimo=0
               
       else:
           try:
               nlevc = None
               climodat = climo.variables[varnamec][ntimec,:,:]
               doclimo=1
           except:
               doclimo=0
           
       
       #fimx_verif=nio.open_file(fimax+'.grib')

       try:
          fim_fcst = nio.open_file(fimf+'.grib')
          fimx_fcst=nio.open_file(fimfx+'.grib')
       except:
          continue

    
       lats = fim_fcst.variables['lat_4'][:]
       lons = fim_fcst.variables['lon_4'][:]
       nlats = len(lats); nlons = len(lons)
       if spharmhd is None:
          spharmhd = Spharmt(nlons,nlats)

       coslats = np.cos((np.pi/180.)*lats1)
       coslatshd = np.cos((np.pi/180.)*lats)
       coslats = coslats[:,np.newaxis]*np.ones((nlats1,nlons1))
       coslatshd = coslatshd[:,np.newaxis]*np.ones((nlats,nlons))
       latnh = lats1.tolist().index(latbound)
       latnh1 = lats1.tolist().index(latboundx)
       latsh = lats1.tolist().index(-latbound)
       latsh1 = lats1.tolist().index(-latboundx)
       coslatsnh = coslats[latnh1:latnh+1,:]
       coslatssh = coslats[latsh:latsh1+1,:]
       coslatstr = coslats[latnh:latsh+1,:]
       
       try:
          fim_verif = nio.open_file(fima+'.grib')
          fimx_verif = nio.open_file(fimax+'.grib')
          gsi_fcst = nio.open_file(gsif+'.grib')
          gsi_verif = nio.open_file(gsia+'.grib')
       except:
          continue
       
       if level is not None:
           #try:
           if 1:
               levdim = fim_fcst.variables[varname_fim].dimensions[0]
               levels = fim_fcst.variables[levdim][:].tolist()
               nlevf_fim = levels.index(level)
               levdim = fim_verif.variables[varname_fim].dimensions[0]
               levels = fim_verif.variables[levdim][:].tolist()
               nleva_fim = levels.index(level)
               levdim = gsi_fcst.variables[varname_gfs].dimensions[0]
               levels = (0.01*gsi_fcst.variables[levdim][:]).tolist()
               nlevf_gsi = levels.index(level)
               levdim = gsi_verif.variables[varname_gfs].dimensions[0]
               levels = (0.01*gsi_verif.variables[levdim][:]).tolist()
               nleva_gsi = levels.index(level)
               
               fimf_dat = fim_fcst.variables[varname_fim][nlevf_fim,:,:]
               fimv_dat = fim_verif.variables[varname_fim][nleva_fim,:,:]

               fimxf_dat = fimx_fcst.variables[varname_fim][nlevf_fim,:,:]
               fimxv_dat = fimx_verif.variables[varname_fim][nleva_fim,:,:]

               gsif_dat = gsi_fcst.variables[varname_gfs][nlevf_gsi,:,:]
               gsiv_dat = gsi_verif.variables[varname_gfs][nleva_gsi,:,:]
               
           #except:
           #    continue
           if(verb):
               print nlevf_fim,fimf_dat.min(), fimf_dat.max()
               print nleva_fim,fimv_dat.min(), fimv_dat.max()
               print nlevf_fim,fimxf_dat.min(), fimxf_dat.max()
               print nleva_fim,fimxv_dat.min(), fimxv_dat.max()
               print nlevf_gsi,gsif_dat.min(), gsif_dat.max()
               print nleva_gsi,gsiv_dat.min(), gsiv_dat.max()
       else:
           fimf_dat  = fim_fcst.variables[varname_fim][:,:]
           fimv_dat  = fim_verif.variables[varname_fim][:,:]
           fimxf_dat = fimx_fcst.variables[varname_fim][:,:]
           fimxv_dat = fimx_verif.variables[varname_fim][:,:]
           gsif_dat  = gsi_fcst.variables[varname_gfs][:,:]
           gsiv_dat  = gsi_verif.variables[varname_gfs][:,:]
       if use_gsiv:
           fimv_dat = gsiv_dat
           
       #rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
       #
       # regrid -- coslat weight the winds
       #

       if varname_fim.startswith('U') or varname_fim.startswith('V'):
           fimf_dat = regrid(spharmhd, spharm1d, fimf_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
           fimv_dat = regrid(spharmhd, spharm1d, fimv_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
           fimxf_dat = regrid(spharmhd, spharm1d, fimxf_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
           fimxv_dat = regrid(spharmhd, spharm1d, fimxv_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
           gsif_dat = regrid(spharmhd, spharm1d, gsif_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
           gsiv_dat = regrid(spharmhd, spharm1d, gsiv_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
       else:
           fimf_dat = regrid(spharmhd, spharm1d, fimf_dat, ntrunc=ntrunc, smooth=None)
           fimv_dat = regrid(spharmhd, spharm1d, fimv_dat, ntrunc=ntrunc, smooth=None)
           fimxf_dat = regrid(spharmhd, spharm1d, fimxf_dat, ntrunc=ntrunc, smooth=None)
           fimxv_dat = regrid(spharmhd, spharm1d, fimxv_dat, ntrunc=ntrunc, smooth=None)
           gsif_dat = regrid(spharmhd, spharm1d, gsif_dat, ntrunc=ntrunc, smooth=None)
           gsiv_dat = regrid(spharmhd, spharm1d, gsiv_dat, ntrunc=ntrunc, smooth=None)

       fim_fcst.close(); fim_verif.close()
       fimx_fcst.close(); fimx_verif.close()
       gsi_fcst.close(); gsi_verif.close()

       fim_err = fimf_dat - fimv_dat
       if(doclimo):
           fim_cov = (fimf_dat-climodat)*(fimv_dat-climodat)
           fim_fvar = (fimf_dat-climodat)**2
           fim_vvar = (fimv_dat-climodat)**2
           
       fim_mse = fim_err**2

       fimx_err = fimxf_dat - fimxv_dat
       if(doclimo):
           fimx_cov = (fimxf_dat-climodat)*(fimxv_dat-climodat)
           fimx_fvar = (fimxf_dat-climodat)**2
           fimx_vvar = (fimxv_dat-climodat)**2
       fimx_mse = fimx_err**2

       gsif_err = gsif_dat - gsiv_dat
       gsif_mse = gsif_err**2
       if(doclimo):
           gsi_cov = (gsif_dat-climodat)*(gsiv_dat-climodat)
           gsi_fvar = (gsif_dat-climodat)**2
           gsi_vvar = (gsiv_dat-climodat)**2

       fim_rmsnh = np.sqrt(getmean(fim_mse[latnh1:latnh+1,:],coslatsnh))
       fim_rmssh = np.sqrt(getmean(fim_mse[latsh:latsh1+1,:],coslatssh))
       fim_rmstr = np.sqrt(getmean(fim_mse[latnh:latsh+1,:],coslatstr))

       fimx_rmsnh = np.sqrt(getmean(fimx_mse[latnh1:latnh+1,:],coslatsnh))
       fimx_rmssh = np.sqrt(getmean(fimx_mse[latsh:latsh1+1,:],coslatssh))
       fimx_rmstr = np.sqrt(getmean(fimx_mse[latnh:latsh+1,:],coslatstr))
       
       gsi_rmsnh  = np.sqrt(getmean(gsif_mse[latnh1:latnh+1,:],coslatsnh))
       gsi_rmssh  = np.sqrt(getmean(gsif_mse[latsh:latsh1+1,:],coslatssh))
       gsi_rmstr  = np.sqrt(getmean(gsif_mse[latnh:latsh+1,:],coslatstr))

       if(doclimo):
           fim_acnh=getmean(fim_cov[latnh1:latnh+1,:],coslatsnh)/(np.sqrt(getmean(fim_fvar[latnh1:latnh+1,:],coslatsnh))*np.sqrt(getmean(fim_vvar[latnh1:latnh+1,:],coslatsnh)))
           fim_acsh=getmean(fim_cov[latsh:latsh1+1,:],coslatssh)/(np.sqrt(getmean(fim_fvar[latsh:latsh1+1,:],coslatssh))*np.sqrt(getmean(fim_vvar[latsh:latsh1+1,:],coslatssh)))
           fim_actr=getmean(fim_cov[latnh:latsh+1,:],coslatstr)/(np.sqrt(getmean(fim_fvar[latnh:latsh+1,:],coslatstr))*np.sqrt(getmean(fim_vvar[latnh:latsh+1,:],coslatstr)))

           fimx_acnh=getmean(fimx_cov[latnh1:latnh+1,:],coslatsnh)/(np.sqrt(getmean(fimx_fvar[latnh1:latnh+1,:],coslatsnh))*np.sqrt(getmean(fimx_vvar[latnh1:latnh+1,:],coslatsnh)))
           fimx_acsh=getmean(fimx_cov[latsh:latsh1+1,:],coslatssh)/(np.sqrt(getmean(fimx_fvar[latsh:latsh1+1,:],coslatssh))*np.sqrt(getmean(fimx_vvar[latsh:latsh1+1,:],coslatssh)))
           fimx_actr=getmean(fimx_cov[latnh:latsh+1,:],coslatstr)/(np.sqrt(getmean(fimx_fvar[latnh:latsh+1,:],coslatstr))*np.sqrt(getmean(fimx_vvar[latnh:latsh+1,:],coslatstr)))

           gsi_acnh=getmean(gsi_cov[latnh1:latnh+1,:],coslatsnh)/(np.sqrt(getmean(gsi_fvar[latnh1:latnh+1,:],coslatsnh))*np.sqrt(getmean(gsi_vvar[latnh1:latnh+1,:],coslatsnh)))
           gsi_acsh=getmean(gsi_cov[latsh:latsh1+1,:],coslatssh)/(np.sqrt(getmean(gsi_fvar[latsh:latsh1+1,:],coslatssh))*np.sqrt(getmean(gsi_vvar[latsh:latsh1+1,:],coslatssh)))
           gsi_actr=getmean(gsi_cov[latnh:latsh+1,:],coslatstr)/(np.sqrt(getmean(gsi_fvar[latnh:latsh+1,:],coslatstr))*np.sqrt(getmean(gsi_vvar[latnh:latsh+1,:],coslatstr)))

       print 'DDDDDDDDDDDDDD dtg: ',dtg,' fhr: ',fhr,'dtgv: ',dtgv
       if(doclimo):
           print "fim    ac: %6.3f %6.3f %6.3f "%(fim_acnh,fim_actr,fim_acsh)
           print "fimx   ac: %6.3f %6.3f %6.3f "%(fimx_acnh,fimx_actr,fimx_acsh)
           print "gfs    ac: %6.3f %6.3f %6.3f "%(gsi_acnh,gsi_actr,gsi_acsh)
           
       print "fim   rms: %6.3f %6.3f %6.3f "%(fim_rmsnh,fim_rmstr,fim_rmssh)
       print "fimx  rms: %6.3f %6.3f %6.3f "%(fimx_rmsnh,fimx_rmstr,fimx_rmssh)
       print "gfs   rms: %6.3f %6.3f %6.3f "%(gsi_rmsnh,gsi_rmstr,gsi_rmssh)


       if(doclimo):
           fimnh_ac=DicAppend(fimnh_ac,fhr,fim_acnh)
           fimtr_ac=DicAppend(fimtr_ac,fhr,fim_actr)
           fimsh_ac=DicAppend(fimsh_ac,fhr,fim_acsh)
       
           fimxnh_ac=DicAppend(fimxnh_ac,fhr,fimx_acnh)
           fimxtr_ac=DicAppend(fimxtr_ac,fhr,fimx_actr)
           fimxsh_ac=DicAppend(fimxsh_ac,fhr,fimx_acsh)
           
           gsinh_ac=DicAppend(gsinh_ac,fhr,gsi_acnh)
           gsitr_ac=DicAppend(gsitr_ac,fhr,gsi_actr)
           gsish_ac=DicAppend(gsish_ac,fhr,gsi_acsh)

       fimnh_rms=DicAppend(fimnh_rms,fhr,fim_rmsnh)
       fimtr_rms=DicAppend(fimtr_rms,fhr,fim_rmstr)
       fimsh_rms=DicAppend(fimsh_rms,fhr,fim_rmssh)
       
       fimxnh_rms=DicAppend(fimxnh_rms,fhr,fimx_rmsnh)
       fimxtr_rms=DicAppend(fimxtr_rms,fhr,fimx_rmstr)
       fimxsh_rms=DicAppend(fimxsh_rms,fhr,fimx_rmssh)
       
       gsinh_rms=DicAppend(gsinh_rms,fhr,gsi_rmsnh)
       gsitr_rms=DicAppend(gsitr_rms,fhr,gsi_rmstr)
       gsish_rms=DicAppend(gsish_rms,fhr,gsi_rmssh)


for fhr in fhrs:

    if(doclimo):
        fimnh_ac[fhr] = np.array(fimnh_ac[fhr])
        fimsh_ac[fhr] = np.array(fimsh_ac[fhr])
        fimtr_ac[fhr] = np.array(fimtr_ac[fhr])
        
        fimxnh_ac[fhr] = np.array(fimxnh_ac[fhr])
        fimxsh_ac[fhr] = np.array(fimxsh_ac[fhr])
        fimxtr_ac[fhr] = np.array(fimxtr_ac[fhr])
   
        gsinh_ac[fhr] = np.array(gsinh_ac[fhr])
        gsish_ac[fhr] = np.array(gsish_ac[fhr])
        gsitr_ac[fhr] = np.array(gsitr_ac[fhr])
        
    fimnh_rms[fhr] = np.array(fimnh_rms[fhr])
    fimsh_rms[fhr] = np.array(fimsh_rms[fhr])
    fimtr_rms[fhr] = np.array(fimtr_rms[fhr])
    
    fimxnh_rms[fhr] = np.array(fimxnh_rms[fhr])
    fimxsh_rms[fhr] = np.array(fimxsh_rms[fhr])
    fimxtr_rms[fhr] = np.array(fimxtr_rms[fhr])
    
    gsinh_rms[fhr] = np.array(gsinh_rms[fhr])
    gsish_rms[fhr] = np.array(gsish_rms[fhr])
    gsitr_rms[fhr] = np.array(gsitr_rms[fhr])
    
    
    print 
    print 'SSSSSSSSSSSSSS fhr:',fhr,' summary stats for dtg1:',dtg1,' to dtg2: ',dtg2
    if(doclimo):
        print "fim  nh,tr,sh  ac: %6.3f %6.3f %6.3f "%(fimnh_ac[fhr].mean(),fimtr_ac[fhr].mean(),fimsh_ac[fhr].mean()),   ' N: ',len(fimnh_ac[fhr])
        print "fimx nh,tr,sh  ac: %6.3f %6.3f %6.3f "%(fimxnh_ac[fhr].mean(),fimxtr_ac[fhr].mean(),fimxsh_ac[fhr].mean()),   ' N: ',len(fimxnh_ac[fhr])
        print "gfs  nh,tr,sh  ac: %6.3f %6.3f %6.3f "%(gsinh_ac[fhr].mean(),gsitr_ac[fhr].mean(),gsish_ac[fhr].mean()),      ' N: ',len(gsinh_ac[fhr])
        print
        
    print "fim  nh,tr,sh rms: %6.3f %6.3f %6.3f "%(fimnh_rms[fhr].mean(),fimtr_rms[fhr].mean(),fimsh_rms[fhr].mean()),' N: ',len(fimnh_rms[fhr])
    print "fimx nh,tr,sh rms: %6.3f %6.3f %6.3f "%(fimxnh_rms[fhr].mean(),fimxtr_rms[fhr].mean(),fimxsh_rms[fhr].mean()),' N: ',len(fimxnh_rms[fhr])
    print "gfs  nh,tr,sh rms: %6.3f %6.3f %6.3f "%(gsinh_rms[fhr].mean(),gsitr_rms[fhr].mean(),gsish_rms[fhr].mean()),   ' N: ',len(gsinh_rms[fhr])

