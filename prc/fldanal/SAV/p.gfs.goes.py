#!/usr/bin/env python

from M import *
import w2

import WxMAP2 as W2



MF=MFutils()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            2:['parea',    'no default'],
            }

        self.defaults={
            'model':'gfs2',
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'ptau':['t:',999,'i','ptau -- fc tau for genesis'],
            'channel':['C:',3,'i','channel to plot'],
            'dvorak':['D',0,1,'use channel 4 and BD curve'],
            'doortho':['S',0,1,'do orthographic projection'],
            'dowind':['W',0,1,'plot 500-300 layer mean wind'],
            }

        self.purpose='''
purpose -- wget mirror gfs stb (sat brightness t) goes images
%s cur
'''
        self.examples='''
%s cur
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='gfs.stb.plot')
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

AA=W2.getW2Area(parea)

if(AA != None):
    AA.ls()
else:
    print 'EEE invalid parea: ',parea
    sys.exit()

if(ptau == 999):
    ptaus=[0]
    ptau=0
else:
    ptaus=[ptau]



sbdir="%s/%s"%(w2.Nwp2DataBdir,w2.Model2CenterModel(model))

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

for dtg in dtgs:

    hh=int(dtg[8:])
    sdir="%s/%s"%(sbdir,dtg)
    gpath="%s/gfs.t%02dz.goessimpgrb2.1p0deg.grib2.ctl"%(sdir,hh)




channel=int(channel)

zoomfactX=0.90
zoomfactY=0.950
zoomfactY=1.0
if(doortho):
    zoomfactX=0.90
    zoomfactY=0.90
    
lutchannel=channel
if(channel == 2): lutchannel=4

lut="GOES-Ch%02d.txt"%(lutchannel)

if(dvorak):
    channel=4
    lutchannel=4
    lut="GOES-Ch%02d-BD.txt"%(lutchannel)

# -- grads script
#

gfspath="/w21/dat/nwp2/w2flds/dat/gfs2/%s/gfs2.w2flds.%s.ctl"%(dtg,dtg)

doprw=1
prwarea='io'

if(doprw):
    gs="""function main(args)

rc=gsfallow(on)
rc=const()

'open %s'
'open %s'

rc=prwarea(%s)

  _blat=-40
  _elat=30
  _blon=20
  _elon=140

print 'bbbb '_blon' '_elon' '_blat' '_elon
if(_blon < 0) ; _blon=360+_blon ; endif
if(_elon < 0) ; _elon=360+_elon ; endif

'set lon '_blon' '_elon
'set lat '_blat' '_elat

"""%(gpath,gfspath,prwarea)

    cmd="cp prwarea.gsf /ptmp/."
    mf.runcmd(cmd)

else:
    gs="""function main(args)

rc=gsfallow(on)
rc=const()

'open %s'
'open %s'

rc=prwarea(%s)

if(_blon < 0) ; _blon=360+_blon ; endif
if(_elon < 0) ; _elon=360+_elon ; endif

'set lon '_blon' '_elon
'set lat '_blat' '_elat


'set lat %4.1f %5.1f'
'set lon %4.1f %5.1f'
'set parea  %6.3f %6.3f %6.3f %6.3f'

"""%(gpath,gfspath,AA.latS,AA.latN,AA.lonW,AA.lonE,
     AA.pareaxl*zoomfactX,AA.pareaxr*zoomfactX,AA.pareayb*zoomfactY,AA.pareayt*zoomfactY)


gspath='/ptmp/g.gfs.goes.gs'
pngpath='/ptmp/gfs.goes.chn%02d.%s.%s.t%03d.png'%(channel,parea,dtg,ptau)

if(doortho):
    pngpath='/ptmp/gfs.goes.chn%02d.%s.%s.t%03d.png'%(channel,'ortho',dtg,ptau)
    gs="""%s

'set lat -90 90'
'set lon 130 310'
'set mproj orthogr'
"""%(gs)

print 'PPPPPPPPPPPPPPPPPPP: ',pngpath


# -- open the text file with the color table for chnl 3 -- h20 vapor
#

cards=open(lut).readlines()


iskip=1
nn=16   # start of user defined grads color 16-255
nmax=240

cvals='set clevs '
rgbcols='set ccols %d'%(nn)

zeroK=273.16

for n in range(0,len(cards),iskip):
    j=len(cards)-n-1
    tt=cards[j].split()
    ndx=tt[0].split(':')[0]
    temp=float(tt[1].split(':')[1]) - zeroK
    red=int(tt[2].split(':')[1])
    green=int(tt[3].split(':')[1])
    blue=int(tt[4].split(':')[1])
    #print card,ndx,temp,red,green,blue
    if(nn>255 or n > nmax): continue
    cvals="%s %5.1f"%(cvals,temp)
    gscmd="""'set rgb %d %d %d %d'"""%(nn,red,green,blue)
    rgbcols="%s %d"%(rgbcols,nn)
    nn=nn+1

    gs=gs+"""%s
"""%(gscmd)

gs=gs+"""
'%s'
"""%(cvals)

if(channel == 2):  tchannel='IR2'
if(channel == 3):  tchannel='W/V'
if(channel == 4):  tchannel='IR4'
if(channel == 4 and dvorak):  tchannel='IR4-BD curve'
vdtg=mf.dtginc(dtg,ptau)

gtime=mf.dtg2gtime(vdtg)

gs=gs+"""'%s'

'set grads off'
'set timelab on'
'set xlint 20'
'set xlint 10'
'set ylint 10'
'set mpdset mres'
'set map 7 1 8'
'set gxout shaded'
'set csmooth on'
'set time %s'
'd sbtch%d - %f'
"""%(rgbcols,gtime,channel,zeroK)

if(dowind):
    gs=gs+"""

'set dfile 2'

nplevs=2
plev2=200
plevs='500 300'
pwghts='250 200'
pwghttot='450'
levb=600
levt=200
_prwsden=5
_cthkbb=10
_cthk=4
_cthkb=4
_bskip=5
_prwbskip=8
bskip=_prwbskip

'u2=const(ua(lev='plev2'),0,-a)'
'v2=u2'

k=1
while(k<=nplevs)
  plev=subwrd(plevs,k)
  pwght=subwrd(pwghts,k)

  'ualev=ua(lev='plev')'
  'valev=va(lev='plev')'

  'u2=u2+ualev*('pwght')'
  'v2=v2+valev*('pwght')'
  'vfact=(0.01*0.622)*'pwght

  k=k+1
endwhile

'u2=(u2*'_ms2kt') / 'pwghttot
'v2=(v2*'_ms2kt') / 'pwghttot

'u2s=re2(u2,1.0)'
'v2s=re2(v2,1.0)'
'm2s=mag(u2,v2)'

'set gxout stream'
'set arrowhead 0.010'
'set strmden '_prwsden
'set cthick '_cthkbb
'set ccolor 0'
'd u2s;v2s'

#'set clevs 10 15 20 35 50 65 100'
#'set rbrange 0 100'

'set cthick '_cthk
'set ccolor 7'

'd u2s;v2s'


'set gxout barb'
'set cthick '_cthkb
'set cthick 10'
'set ccolor 0'
'set digsiz 0.04'


vmin=25
vmax=65

vminn=10
'd skip(u2,'bskip');maskout(v2,m2s-'vminn')'
'set cthick 5'
'set ccolor 3'
'd skip(u2,'bskip');maskout(v2,m2s-'vminn')'

'set cthick '_cthkbb
'set ccolor 0'
'd skip(u2,'bskip');maskout(v2,m2s-'vmin')'

'set cthick 5'
'set ccolor 7'
'd skip(u2,'bskip');maskout(v2,m2s-'vmin')'

'set cthick '_cthkbb
'set ccolor 0'
'd skip(u2,'bskip');maskout(v2,m2s-'vmax')'

'set cthick 6'
'set ccolor 2'
'd skip(u2,'bskip');maskout(v2,m2s-'vmax')'


"""


wtitle=''
if(dowind): wtitle='+ 500-300 mb Winds'

gs=gs+"""

'cbarn2 1.0 1 0.50'
'set map 7 1 5'
'draw map'
t1='GFS %s `3t`0=%d h GOES12 Chnl %d (%s) %s'
t2='valid: %s  1`3.`0 global grid'

rc=toptitle(t1,t2,0.75)

#'gxyat -x 1024 -y 768 -r %s'
'printim %s x1600 y1200 black'

"""%(dtg,ptau,channel,tchannel,wtitle,vdtg,pngpath,pngpath)

MF.WriteString2File(gs,gspath)
cmd='''grads2 -lc "%s"'''%(gspath)
MF.runcmd(cmd)

MF.dTimer(tag='gfs.stb.plot')




