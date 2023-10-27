#!/usr/bin/env python
from WxMAP2 import *
w2=W2()

from tcbase import *
from TCtrk import TcPrBasin,tcgenModels,tcgenW3DatDir,tcgenW3Dir,tcgenModelLabel,getBasinOptFromStmids,tcgenBasins,getGentaus

# -- kaze/kishou location of tcgen.pypdb

if(w2.onTaifuu or w2.onKishou or w2.onTenki):
    ttcgbdir="/w21/dat/tc/tcgen"

ttcgbdir=TcGenDatDir
anlSCdir="%s/anlSC"%(ttcgbdir)
MF.ChkDir(anlSCdir,'mk')

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class gaGenScSummary(MFbase):
    

    def __init__(self,
                 undef=1e20,
                 undef999=-999.,
                 gsdir='/ptmp',
                 verb=0):
        
        self.undef=undef
        self.gsdir=gsdir
        self.gspath="%s/sum.gs"%(self.gsdir)
        self.pngpath="%s/sum.png"%(self.gsdir)
        
    def getGenScs(self):
        
        models=['GFS','ECMWF']
        basins=['WPAC D+2','WPAC D+5','LANT D+3']
        genScs={
            'GFS':[(70,90),(90,300),(50,700)],
            'ECMWF':[(90,50),(60,10),(70,400)],
                }
        
        genScs={}
        genScsSum={}
        
        models=[]
        basins=[]
        cardfiles=glob.glob('%s/sC*txt'%(self.gsdir))
        igenScs={}
        
        
        for cardfile in cardfiles:
            cards=open(cardfile).readlines()
            tt=cards[0].split()

            model=tt[0]
            basin=tt[1]
            year=int(tt[2])
            tau=int(tt[3])
            
            if(tau == 60): day=2
            if(tau == 132): day=5
            basin="%s.14-D+%d"%(basin.upper(),day)
            genP=float(tt[4])
            scP=float(tt[5])
            nGTs=int(tt[6])
            
            models.append(model)
            basins.append(basin)
            igenScs[model,basin]=(genP,scP,nGTs)
        
        models=mf.uniq(models)
        basins=mf.uniq(basins)

        basins=['WPAC.14-D+2','WPAC.14-D+5','EPAC.14-D+2','EPAC.14-D+5','LANT.14-D+2','LANT.14-D+5']

        for model in models:
            mgenP=0.0
            mscP=0.0
            nGT=0
            for basin in basins:
                (genP,scP,nGTs)=igenScs[model,basin]
                mgenP=mgenP+genP*nGTs
                mscP=mscP+scP*nGTs
                nGT=nGT+nGTs
                
                MF.appendDictList(genScs,model,igenScs[model,basin])
                
            mgenP=mgenP/nGT
            mscP=mscP/nGT
            
            print 'MeanGen: ',model,mgenP
            print 'MeanSC1: ',model,mscP
            
            genScsSum[model]=(mgenP,mscP)


            for basin in basins:
                mgenP=0.0
                mscP=0.0
                nGT=0
                for model in models:
                    (genP,scP,nGTs)=igenScs[model,basin]
                    mgenP=mgenP+genP*nGTs
                    mscP=mscP+scP*nGTs
                    nGT=nGT+nGTs
                    
                mgenP=mgenP/nGT
                mscP=mscP/nGT
                
                print 'MeanGen: ',model,mgenP
                print 'MeanSC1: ',model,mscP
                
                genScsSum[basin]=(mgenP,mscP)
                
            
        models=['gfs2','fim8','rtfim9','ecm2','navg','ukm2','cmc2']
        
        for model in models:
            omodel=tcgenModelLabel[model]
            print 'GGGG',model,omodel,genScs[model]
        
        return(models,basins,genScs,genScsSum)
        

    def pBox(self,xb,xe,yb,ye,plcol,prcol,xtitle=None,ytitle=None):
        
        lcol=1
        lthk=5
        lsty=1
        
        xoff=0.10
        
        gsbox=''
        
        
        gsbox=gsbox+"""
'set line %d'
'draw polyf %f %f %f %f %f %f %f %f'
"""%(plcol,xb,yb,xe,ye,xb,ye,xb,yb)

        gsbox=gsbox+"""
'set line %d'
'draw polyf %f %f %f %f %f %f %f %f'
"""%(prcol,xb,yb,xe,yb,xe,ye,xb,yb)

        gsbox=gsbox+"""
'set line %d %d %d'
"""%(lcol,lsty,lthk)
        
        gsbox=gsbox+"""
'draw rec %f %f %f %f'
'draw line %f %f %f %f'
"""%(xb,yb,xe,ye,xb,yb,xe,ye)
        
        if(xtitle != None):
            xs=xb-xoff
            ys=(yb+ye)*0.5
            gstitle="""
'set string 1 r 6 0'
'draw string %f %f %s'
"""%(xs,ys,xtitle)
            
            gsbox=gsbox+gstitle
            
        if(ytitle != None):
            xs=(xb+xe)*0.5 
            ys=ye + xoff
            gstitle="""
'set string 1 bl 6 45'
'draw string %f %f %s'
"""%(xs,ys,ytitle)
            
            gsbox=gsbox+gstitle
            
        return(gsbox)
        
    def getLcol(self,val,vals,cols):
        
        if(val < vals[0]): 
            col=cols[0]
            return(col)
        if(val >= vals[-1]):
            col=cols[-1]
            return(col)
        
        for i in range(0,len(vals)-1):
            if(val >= vals[i] and val < vals[i+1]):
                col=cols[i+1]
                return(col)
        
    def getRcol(self,val,vals,cols):
        
        if(val < vals[0]): 
            col=cols[0]
            return(col)
        if(val >= vals[-1]):
            col=cols[-1]
            return(col)
        
        for i in range(0,len(vals)-1):
            if(val >= vals[i] and val < vals[i+1]):
                col=cols[i+1]
                return(col)
            
    def putShades(self,vals,cols):
        
        gs=''
        ncols=len(cols)
        for n in range(0,ncols):
            i=n+1
            if(n == 0):
                ip1=i+1
                gs=gs+"""
_shdinfo.%d='Number of levels = %d'
_shdinfo.%d='%d <= %5.0f'"""%(i,ncols,i+1,cols[0],vals[0])
            elif(n == ncols-1):
                gs=gs+"""
_shdinfo.%d='%d %5.0f >'"""%(i+1,cols[n],vals[-1])
            else:
                gs=gs+"""
_shdinfo.%d='%d %5.0f %5.0f'"""%(i+1,cols[n],vals[n-1],vals[n])
                
        print gs
        return(gs)
        
        
    def plotSum(self,models,basins,genScs,genScsSum):

        
        xsize=1440
        ysize=int(xsize*(3.0/4.0))
        
        xstart=4.0
        ystart=6.5
        
        nrow=2
        ncol=6
        boxwidth=0.65
        
        xstart=xstart-boxwidth
        
        gridctl=w2.GradsGslibDir+'/dum.ctl'


        Lvals=[  60.,  70.0,   80.,   90.,   100.]
        Lcols=[31,  32,     33,    35,    57,    59  ]

        Lvals=[  60., 70., 80.,   85.,  90.,   100.]
        Lcols=[31,   33,   35, 37,  73,   77 ,     79]

        Lgsshades=self.putShades(Lvals,Lcols)

        Rvals=[  0.,  50.,   70.,  100.,  150.,  200.,  300.,   500. ]
        Rcols=[49,   47,   45,   43,   41,    21,    23,     25,  29  ]
        Rgsshades=self.putShades(Rvals,Rcols)
        
        
        gshead="""
function main(args)
rc=gsfallow(on)
rc=const()
rc=jaecol2()
'set grads off'
'set timelab on'
'open %s'
'set cmin 1000'
'd abs(lat)'
'c'

"""%(
       gridctl,
     )
        
        gs=gshead

        xmin=999
        xmax=-999
        ymin=999
        ymax=-999
        
        nM=len(models)
        
        for j in range(0,nM):
            model=models[j]
            ye=ystart-j*boxwidth
            yb=ye-boxwidth
            genSc=genScs[model]
            if(yb < ymin): ymin=yb
            if(ye > ymax): ymax=ye

            nG=len(genSc)  # mean is at end


            for i in range(0,nG):
                (pgen,psc,nGT)=genSc[i]
                ytitle=None
                if(j == 0): ytitle=basins[i]
                xtitle=None
                if(i == 0): xtitle=tcgenModelLabel[model]
        
                xb=xstart+i*boxwidth
                xe=xb+boxwidth   
                if(xb < xmin): xmin=xb
                if(xe > xmax): xmax=xe
                
                plcol=self.getLcol(pgen,Lvals,Lcols)
                prcol=self.getRcol(psc,Rvals,Rcols)
                
                gsbox=self.pBox(xb, xe, yb, ye, plcol, prcol,xtitle=xtitle,ytitle=ytitle)
                gs=gs+gsbox

                if(i == nG-1):
                    xtitle=None
                    ytitle=None
                    if(j == 0): ytitle='Model Mean'
                    (pgen,psc)=genScsSum[model]
                    plcol=self.getLcol(pgen,Lvals,Lcols)
                    prcol=self.getRcol(psc,Rvals,Rcols)
                    xb=xb+boxwidth+0.25
                    xe=xb+boxwidth
                    gsbox=self.pBox(xb, xe, yb, ye, plcol, prcol,xtitle=xtitle,ytitle=ytitle)
                    gs=gs+gsbox



        for i in range(0,nG):

            ye=ystart-nM*boxwidth-0.25
            yb=ye-boxwidth
            genSc=genScs[model]
            if(yb < ymin): ymin=yb
            if(ye > ymax): ymax=ye
            
            ytitle=None
            xtitle=None
            if(i == 0): xtitle='Basin Mean'
   
            basin=basins[i]
            xb=xstart+i*boxwidth
            xe=xb+boxwidth   
            if(xb < xmin): xmin=xb
            if(xe > xmax): xmax=xe
            
            (pgen,psc)=genScsSum[basin]
            plcol=self.getLcol(pgen,Lvals,Lcols)
            prcol=self.getRcol(psc,Rvals,Rcols)
            gsbox=self.pBox(xb, xe, yb, ye, plcol, prcol,xtitle=xtitle,ytitle=ytitle)
            gs=gs+gsbox


        xmidR=(xmin+xmax)*0.5
        ymidR=ymin-0.75
        
        xmidL=xmax+0.75+boxwidth
        ymidL=(ymin+ymax)*0.5

        gstail="""
                
t1='2014 Model Genesis Forecast v False Alarm Rate '
t2='GEN: %% storms correctly forecast  v FAR: %% of GEN cases with SC1'
t3='3 shots at the foul line to forecast GEN'
t3scl=0.75
rc=toptle3(t1,t2,t3,t3scl)
        
%s
        
#function cbarns (sf,vert,xmid,ymid,sfstr,force,lab,labstr,bgcolor)
rc=cbarns(0.65,0,%f,%f,'',y,y,'GEN[%%]','')
%s

rc=cbarns(0.65,1,%f,%f,'',y,y,'FAR[%%]','')
        
        
#'gxyat -v -x %%d -y %%d %%s'
'printim -x %d -y %d %s'

'q pos'
'quit'
return        
        """%(Lgsshades,xmidR,ymidR,
             Rgsshades,xmidL,ymidL,
             xsize,ysize,self.pngpath)
                
        gs=gs+gstail
        
        
        print gs
        ropt=''
        MF.WriteString2File(gs,self.gspath)
        cmd="%s -lc %s"%(xgrads,self.gspath)
        mf.runcmd(cmd,ropt)
        
        

class AdgenCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv is None): argv=sys.argv

        self.argv=argv
        self.argopts={
#            1:['year',  'run dtgs'],
#            2:['modelopt',    'model|model1,model2|all|allgen'],
        }

        self.defaults={
            'doupdate':0,
            'BMoverride':0,
        }

        self.options={
            'override':      ['O',0,1,'override'],
            'trkoverride':   ['o',0,1,'override in dotrk'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'dogenPlot':     ['G',0,1,'plot genesis points and SC1s'],
            'onlySC1':       ['s',0,1,'calc pr stats for SC1 maps only'],
            'quiet':         ['q',1,0,' run GA in NOT quiet mode'],
            'diag':          ['d',0,1,' extra diagnostics'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doplot':        ['P',1,0,'do NOT make plots'],
            'anlTag':        ['T:','misc','a','tag for the spuricane .pyp'],
            'gentauOpt':     ['t:','all','a','gentauOpt -- fc tau for genesis'],
            'basinopt':      ['b:','all','a',' basin with gen adecks'],
            'filtOpt':       ['f:',None,'a','minsTDd,maxcpsB,mincpsVTl,mincpsVTu SC1s'],
            'anlType':       ['A:','sum','a','anlType - sum |'],
            'zoomOpt':       ['Z:',None,'a','setup subarea zoom box lat1:lat2:lon1;lon2:ylint:xlint'],
            'dochkIfRunning':['c',1,0,'do NOT using MF.chkIfJobIsRunning'],
        }

        self.purpose='''-- analyze spuricane SC'''
        self.examples='''%s 201405.12 gfs2,ecm2 -b lant -T 2014 -t 132'''

argv=sys.argv
CL=AdgenCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

MF.sTimer('all')
gGS=gaGenScSummary()

(models,basins,genScs,genScsSum)=gGS.getGenScs()

gGS.plotSum(models,basins,genScs,genScsSum)

MF.dTimer('all')
sys.exit()

