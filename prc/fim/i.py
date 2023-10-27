import os,sys,time
import getopt,glob
import cPickle as pickle

import mf
import w2
import FM

sRootG='/scratch/01033/harrop/FIM'
sRootE='/scratch/01033/harrop/FIM_ens'
tRoot='/scratch/01233/mfiorino/fim9'

fimver=None
expoptGfs='g9gfs'
expoptEnkf='g9enkf'
fimtypeGfs='C'
fimtypeEnkf='EM'


glvl='9'
nlvl='64'
npes1='1200'
npes2='1200'

dtg='20090873100'


sRootG='/mnt/lfs0/projects/fim/bao/FIMX1/FIMrun/qsubfim_28959'
sRootE='/mnt/lfs0/projects/fim/bao/FIMX1/FIMrun/qsubfim_8169'
tRoot='/mnt/lfs0/projects/fim/bao/dat'


fimver=None
expoptGfs='rtfim'
expoptEnkf='rtfimx'
glvl='8'
nlvl='64'
npes1='240'
npes2='240'
fimtypeGfs='C'
fimtypeEnkf='C'



sRootG='/lfs0/projects/rtfim/FIM'
sRootE='/lfs0/projects/rtfim/FIMX'
tRoot='/lfs0/projects/fim/fiorino/rtfim'


fimver=None
expoptGfs='rtfim'
expoptEnkf='rtfimx'
glvl='8'
nlvl='64'
npes1='240'
npes2='240'
fimtypeGfs='C'
fimtypeEnkf='C'

dtg='2009080600'


FG=FM.FimRun(dtg,fimver,glvl,nlvl,npes1,expoptGfs,sRootG,tRoot,fimtypeGfs)
FE=FM.FimRun(dtg,fimver,glvl,nlvl,npes2,expoptEnkf,sRootE,tRoot,fimtypeEnkf)

#p1=FM.PlotMaps(FG,None,window=1)
#p2=FM.PlotMaps(FE,None,window=1)

#xgrads=os.getenv('xgrads')
xgrads='grads'
gaopt="rungrads %s %s"%(FG.ctlpath,FE.ctlpath)
cmd="%s -lc \"%s\""%(xgrads,gaopt)
print cmd
os.system(cmd)

## sRoot='/lfs0/projects/rtfim/FIM'
## sRootx='/lfs0/projects/rtfim/FIMX1'
## tRoot='/lfs0/projects/fim/fiorino/rtfim'
## fimver=None
## expopt='rtfim'
## expoptx='rtfimx'

## glvl='8'
## nlvl='64'
## npes='240'
## dtg='2009062912'
## dtg='2009070400'
## dtg='2009071512'

## RF=FM.FimRun(dtg,fimver,glvl,nlvl,npes,expopt,sRoot,tRoot)
## RFx=FM.FimRun(dtg,fimver,glvl,nlvl,npes,expoptx,sRootx,tRoot)

## p1=FM.PlotMaps(RF,None,window=1)
## p2=FM.PlotMaps(RFx,None,window=1)




