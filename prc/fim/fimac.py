from PyNIO import nio
import numpy as np
import sys
from dateutils import dateshift, daterange, splitdate
from datetime import datetime
from spharm import Spharmt, regrid

def getmean(diff,coslats):
   meancoslats = coslats.mean()
   return (coslats*diff).mean()/meancoslats

date1 = sys.argv[1]
date2 = sys.argv[2]
fhr = int(sys.argv[3])
var = sys.argv[4]
try:
    level = int(sys.argv[5])
except:
    level = None
model = sys.argv[6]
if model == 'fim':
    fim = True
else:
    fim = False
use_gsiv = False
ntrunc = None
latbound = 20
latboundx = 80

if var == 'U':
    if fim:
        varname = 'UW_4_ISBL'
    else:
        varname = 'U_GRD_4_ISBL_10'
    varnamec = 'U_GRD_3_ISBL_51'
elif var == 'V':
    if fim:
        varname = 'VW_4_ISBL'
    else:
        varname = 'V_GRD_4_ISBL_10'
    varnamec = 'V_GRD_3_ISBL_51'
elif var == 'Z':
    if fim:
        varname = 'GH_4_ISBL'
    else:
        varname = 'HGT_4_ISBL_10'
    varnamec = 'HGT_3_ISBL_51'
elif var == 'T':
    if fim:
        varname = 'T_4_ISBL'
    else:
        varname = 'TMP_4_ISBL_10'
    varnamec = 'TMP_3_ISBL_51'
elif var == 'P':
    if fim:
        varname = 'MMSP_4_MSL'
    else:
        varname = 'PRMSL_4_MSL_10'
    varnamec = 'PRMSL_3_MSL_51'
print date1, date2, var, level, fhr, model
enkfnh_ac=[]
enkftr_ac=[]
enkfsh_ac=[]
gsinh_ac=[]
gsitr_ac=[]
gsish_ac=[]
enkfnh_rms=[]
enkftr_rms=[]
enkfsh_rms=[]
gsinh_rms=[]
gsitr_rms=[]
gsish_rms=[]
spharmhd = None; spharm1d = None
for date in daterange(date1,date2,24):
    datev = dateshift(date,fhr)
    if date > '2009081200': 
        procs='848'
    else:
        procs='1200'
    if fim:
        yyyy,mm,dd,hh = splitdate(date)
        jday = (datetime(yyyy,mm,dd)-datetime(yyyy,1,1)).days+1
        if date >= '2009082800':
            rev = 'r762'
        elif date >= '2009082500':
            rev = 'r740'
        else:
            rev = 'r706'
        datapath = "/scratch/01033/harrop/FIM_EM.%s/FIMrun/" % rev
        enkff = datapath+'fim_9_64_%s_%s00/post_EM/fim/NAT/grib1/%s%03i00000%03i' % (procs,date,date[2:4],jday,fhr) 
        datapath = "/scratch/01033/harrop/FIM.%s/FIMrun/" % rev
        gsif= datapath+'/fim_9_64_%s_%s00/post_C/fim/NAT/grib1/%s%03i00000%03i' % (procs,date,date[2:4],jday,fhr) 
        yyyy,mm,dd,hh = splitdate(datev)
        jday = (datetime(yyyy,mm,dd)-datetime(yyyy,1,1)).days+1
        if datev > '2009081200': 
            procs='848'
        else:
            procs='1200'
        if datev >= '2009082800':
            rev = 'r762'
        elif datev >= '2009082500':
            rev = 'r740'
        else:
            rev = 'r706'
        datapath = "/scratch/01033/harrop/FIM_EM.%s/FIMrun/" % rev
        enkfa = datapath+'fim_9_64_%s_%s00/post_EM/fim/NAT/grib1/%s%03i00000%03i' % (procs,datev,datev[2:4],jday,0) 
        datapath = "/scratch/01033/harrop/FIM.%s/FIMrun/" % rev
        gsia= datapath+'fim_9_64_%s_%s00/post_C/fim/NAT/grib1/%s%03i00000%03i' % (procs,datev,datev[2:4],jday,0) 
    else:
        enkff = '/scratch/01217/whitaker/gfsenkf_200907/%s/enkf.t%sz.pgrbf%02i' % (date,date[8:10],fhr)
        gsif  = '/scratch/01217/whitaker/gfs/%s/gfs.t%sz.pgrbf%s' % (date,date[8:10],repr(fhr))
        #enkfa = '/scratch/01217/whitaker/gfsenkf_200907/%s/pgrbensmeananl_%s' % (datev,datev)
        enkfa = '/scratch/01217/whitaker/gfsenkf_200907/%s/pgrbanl_%s_ensmean' % (datev,datev)
        gsia  = '/scratch/01217/whitaker/gfs/%s/gfs.t%sz.pgrbanl' % (datev,datev[8:10])
    climo = nio.open_file("/work/01217/whitaker/cmean/cmean_1d.1959"+datev[4:8]+".grb")
    init_times = climo.variables['initial_time5_encoded'][:].tolist()
    ntimec = init_times.index(float('1959'+datev[4:10]))
    lats1 = climo.variables['lat_3'][:]
    lons1 = climo.variables['lon_3'][:]
    nlats1=len(lats1); nlons1=len(lons1)
    if spharm1d is None:
       spharm1d = Spharmt(nlons1,nlats1)
    if level is not None:
        levdim = climo.variables[varnamec].dimensions[1]
        climolevels = climo.variables[levdim][:].tolist()
        nlevc = climolevels.index(level)
        climodat = climo.variables[varnamec][ntimec,nlevc,:,:]
    else:
        nlevc = None
        climodat = climo.variables[varnamec][ntimec,:,:]
    try:
        enkf_fcst = nio.open_file(enkff+'.grib')
    except:
        continue
    lats = enkf_fcst.variables['lat_4'][:]
    lons = enkf_fcst.variables['lon_4'][:]
    nlats = len(lats); nlons = len(lons)
    if spharmhd is None:
       spharmhd = Spharmt(nlons,nlats)
    #climodat = 1.e30*np.ones((nlats,nlons),np.float32)
    ## convert from 1 by 1 to 0.5 x 0.5 grid.
    #climodat[0:nlats:2,0:nlons:2] = climodat1by1[:,:]
    #climodat[1:nlats-1:2,0:nlons:2] = 0.5*(climodat1by1[:-1,:]+climodat1by1[1:,:])
    #climodat[:,1:nlons-1:2] = \
    #0.5*(climodat[:,0:-2:2]+climodat[:,2::2])
    #climodat[:,nlons-1] =  0.5*(climodat[:,0]+climodat[:,nlons-2])
    #from mpl_toolkits.basemap import Basemap
    #import matplotlib.pyplot as plt
    ##map = Basemap(llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=lons[-1])
    #map = Basemap(projection='npstere',boundinglat=20,lon+_0=270)
    #map.drawcoastlines()
    #x,y = map(*np.meshgrid(lons,lats))
    #CS = map.contourf(x,y,climodat,20,extend='both')
    #plt.colorbar(CS,orientation='horizontal')
    #plt.show()
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
        enkf_verif = nio.open_file(enkfa+'.grib')
        gsi_fcst = nio.open_file(gsif+'.grib')
        gsi_verif = nio.open_file(gsia+'.grib')
    except:
        continue
    if level is not None:
        try:
            levdim = enkf_fcst.variables[varname].dimensions[0]
            levels = enkf_fcst.variables[levdim][:].tolist()
            nlevf_enkf = levels.index(level)
            levdim = enkf_verif.variables[varname].dimensions[0]
            levels = enkf_verif.variables[levdim][:].tolist()
            nleva_enkf = levels.index(level)
            levdim = gsi_fcst.variables[varname].dimensions[0]
            levels = gsi_fcst.variables[levdim][:].tolist()
            nlevf_gsi = levels.index(level)
            levdim = gsi_verif.variables[varname].dimensions[0]
            levels = gsi_verif.variables[levdim][:].tolist()
            nleva_gsi = levels.index(level)
            enkff_dat = enkf_fcst.variables[varname][nlevf_enkf,:,:]
            gsif_dat = gsi_fcst.variables[varname][nlevf_gsi,:,:]
            enkfv_dat = enkf_verif.variables[varname][nleva_enkf,:,:]
            gsiv_dat = gsi_verif.variables[varname][nleva_gsi,:,:]
        except:
            continue
        #print nlevf_enkf,enkff_dat.min(), enkff_dat.max()
        #print nleva_enkf,enkfv_dat.min(), enkfv_dat.max()
        #print nlevf_gsi,gsif_dat.min(), gsif_dat.max()
        #print nleva_gsi,gsiv_dat.min(), gsiv_dat.max()
    else:
        enkff_dat = enkf_fcst.variables[varname][:,:]
        gsif_dat = gsi_fcst.variables[varname][:,:]
        enkfv_dat = enkf_verif.variables[varname][:,:]
        gsiv_dat = gsi_verif.variables[varname][:,:]
    if use_gsiv:
        enkfv_dat = gsiv_dat
    if varname.startswith('U') or varname.startswith('V'):
        enkff_dat = regrid(spharmhd, spharm1d, enkff_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
        enkfv_dat = regrid(spharmhd, spharm1d, enkfv_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
        gsif_dat = regrid(spharmhd, spharm1d, gsif_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
        gsiv_dat = regrid(spharmhd, spharm1d, gsiv_dat*coslatshd, ntrunc=ntrunc, smooth=None)/coslats
    else:
        enkff_dat = regrid(spharmhd, spharm1d, enkff_dat, ntrunc=ntrunc, smooth=None)
        enkfv_dat = regrid(spharmhd, spharm1d, enkfv_dat, ntrunc=ntrunc, smooth=None)
        gsif_dat = regrid(spharmhd, spharm1d, gsif_dat, ntrunc=ntrunc, smooth=None)
        gsiv_dat = regrid(spharmhd, spharm1d, gsiv_dat, ntrunc=ntrunc, smooth=None)

    enkf_fcst.close(); enkf_verif.close()
    gsi_fcst.close(); gsi_verif.close()

    #from mpl_toolkits.basemap import Basemap
    #import matplotlib.pyplot as plt
    #map = Basemap(projection='npstere',boundinglat=20,lon_0=270)
    #plt.figure()
    #map.drawcoastlines()
    #x,y = map(*np.meshgrid(lons1,lats1))
    #levels = np.arange(-100,100.1,10.)
    #CS = map.contourf(x,y,enkff_dat-climodat,levels,cmap=plt.cm.RdBu_r,extend='both')
    #plt.colorbar(CS,orientation='horizontal')
    #plt.title('enkf')

    #plt.figure()
    #CS = map.contourf(x,y,gsif_dat-climodat,levels,cmap=plt.cm.RdBu_r,extend='both')
    #map.drawcoastlines()
    #plt.colorbar(CS,orientation='horizontal')
    #plt.title('gsi')

    #plt.figure()
    #CS = map.contourf(x,y,enkfv_dat-climodat,levels,cmap=plt.cm.RdBu_r,extend='both')
    #map.drawcoastlines()
    #plt.colorbar(CS,orientation='horizontal')
    #plt.title('enkf verif')

    #plt.figure()
    #CS = map.contourf(x,y,gsiv_dat-climodat,levels,cmap=plt.cm.RdBu_r,extend='both')
    #map.drawcoastlines()
    #plt.colorbar(CS,orientation='horizontal')
    #plt.title('gsi verif')

    #plt.show()
    #raise SystemExit

    enkf_err = enkff_dat - enkfv_dat
    gsif_err = gsif_dat - gsiv_dat
    enkf_mse = enkf_err**2
    gsif_mse = gsif_err**2
    enkf_cov = (enkff_dat-climodat)*(enkfv_dat-climodat)
    enkf_fvar = (enkff_dat-climodat)**2
    enkf_vvar = (enkfv_dat-climodat)**2
    gsi_cov = (gsif_dat-climodat)*(gsiv_dat-climodat)
    gsi_fvar = (gsif_dat-climodat)**2
    gsi_vvar = (gsiv_dat-climodat)**2
    #from mpl_toolkits.basemap import Basemap
    #import matplotlib.pyplot as plt
    #fig = plt.figure(figsize=(8,10))
    #map =\
    #Basemap(llcrnrlat=-latbound,urcrnrlat=latbound,llcrnrlon=lons[0],urcrnrlon=lons[-1],projection='merc',lat_0=20)
    #plt.subplot(4,1,1)
    #map.drawcoastlines()
    #x,y = map(*np.meshgrid(lons,lats))
    #levs = np.arange(-16,16.1,2)
    #CS = map.contourf(x,y,enkff_dat-climodat,levs,cmap=plt.cm.RdBu_r,extend='both')
    #plt.title('EnKF')
    #plt.subplot(4,1,2)
    #map.drawcoastlines()
    #CS = map.contourf(x,y,gsif_dat-climodat,levs,cmap=plt.cm.RdBu_r,extend='both')
    #plt.title('GSI')
    #plt.subplot(4,1,3)
    #map.drawcoastlines()
    #CS = map.contourf(x,y,enkfv_dat-climodat,levs,cmap=plt.cm.RdBu_r,extend='both')
    #plt.title('EnKF Analysis')
    #plt.subplot(4,1,4)
    #map.drawcoastlines()
    #CS = map.contourf(x,y,gsiv_dat-climodat,levs,cmap=plt.cm.RdBu_r,extend='both')
    #plt.title('GSI Analysis')
    #fig.colorbar(CS,orientation='horizontal')
    #plt.show()
    #raise SystemExit
    enkf_rmsnh = np.sqrt(getmean(enkf_mse[latnh1:latnh+1,:],coslatsnh))
    enkf_rmssh = np.sqrt(getmean(enkf_mse[latsh:latsh1+1,:],coslatssh))
    enkf_rmstr = np.sqrt(getmean(enkf_mse[latnh:latsh+1,:],coslatstr))
    gsi_rmsnh  = np.sqrt(getmean(gsif_mse[latnh1:latnh+1,:],coslatsnh))
    gsi_rmssh  = np.sqrt(getmean(gsif_mse[latsh:latsh1+1,:],coslatssh))
    gsi_rmstr  = np.sqrt(getmean(gsif_mse[latnh:latsh+1,:],coslatstr))
    enkf_acnh =\
    getmean(enkf_cov[latnh1:latnh+1,:],coslatsnh)/(np.sqrt(getmean(enkf_fvar[latnh1:latnh+1,:],coslatsnh))*np.sqrt(getmean(enkf_vvar[latnh1:latnh+1,:],coslatsnh)))
    enkf_acsh =\
    getmean(enkf_cov[latsh:latsh1+1,:],coslatssh)/(np.sqrt(getmean(enkf_fvar[latsh:latsh1+1,:],coslatssh))*np.sqrt(getmean(enkf_vvar[latsh:latsh1+1,:],coslatssh)))
    enkf_actr =\
    getmean(enkf_cov[latnh:latsh+1,:],coslatstr)/(np.sqrt(getmean(enkf_fvar[latnh:latsh+1,:],coslatstr))*np.sqrt(getmean(enkf_vvar[latnh:latsh+1,:],coslatstr)))
    gsi_acnh =\
    getmean(gsi_cov[latnh1:latnh+1,:],coslatsnh)/(np.sqrt(getmean(gsi_fvar[latnh1:latnh+1,:],coslatsnh))*np.sqrt(getmean(gsi_vvar[latnh1:latnh+1,:],coslatsnh)))
    gsi_acsh =\
    getmean(gsi_cov[latsh:latsh1+1,:],coslatssh)/(np.sqrt(getmean(gsi_fvar[latsh:latsh1+1,:],coslatssh))*np.sqrt(getmean(gsi_vvar[latsh:latsh1+1,:],coslatssh)))
    gsi_actr =\
    getmean(gsi_cov[latnh:latsh+1,:],coslatstr)/(np.sqrt(getmean(gsi_fvar[latnh:latsh+1,:],coslatstr))*np.sqrt(getmean(gsi_vvar[latnh:latsh+1,:],coslatstr)))
    #print date,enkf_rmsnh,enkf_rmstr,enkf_rmssh,gsi_rmsnh,gsi_rmstr,gsi_rmssh
    print date,enkf_acnh,enkf_actr,enkf_acsh,gsi_acnh,gsi_actr,gsi_acsh,enkf_rmsnh,enkf_rmstr,enkf_rmssh,gsi_rmsnh,gsi_rmstr,gsi_rmssh
    enkfnh_ac.append(enkf_acnh); enkftr_ac.append(enkf_actr)
    enkfsh_ac.append(enkf_acsh)
    gsinh_ac.append(gsi_acnh); gsitr_ac.append(gsi_actr)
    gsish_ac.append(gsi_acsh)
    enkfnh_rms.append(enkf_rmsnh); enkftr_rms.append(enkf_rmstr)
    enkfsh_rms.append(enkf_rmssh)
    gsinh_rms.append(gsi_rmsnh); gsitr_rms.append(gsi_rmstr)
    gsish_rms.append(gsi_rmssh)
enkfnh_ac = np.array(enkfnh_ac)
enkfsh_ac = np.array(enkfsh_ac)
enkftr_ac = np.array(enkftr_ac)
gsinh_ac = np.array(gsinh_ac)
gsish_ac = np.array(gsish_ac)
gsitr_ac = np.array(gsitr_ac)
enkfnh_rms = np.array(enkfnh_rms)
enkfsh_rms = np.array(enkfsh_rms)
enkftr_rms = np.array(enkftr_rms)
gsinh_rms = np.array(gsinh_rms)
gsish_rms = np.array(gsish_rms)
gsitr_rms = np.array(gsitr_rms)
print len(enkfnh_ac),\
enkfnh_ac.mean(),enkftr_ac.mean(),enkfsh_ac.mean(),gsinh_ac.mean(),gsitr_ac.mean(),gsish_ac.mean()
print len(enkfnh_rms),\
enkfnh_rms.mean(),enkftr_rms.mean(),enkfsh_rms.mean(),gsinh_rms.mean(),gsitr_rms.mean(),gsish_rms.mean()

