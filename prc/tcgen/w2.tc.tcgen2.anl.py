#!/usr/bin/env python
from M import *
MFd=MFutils()

diag=1
if(diag): MFd.sTimer('load')
from tcbase import *
#from tcbase import TcData,TcBasin,IsTc,IsNN,Is9X,IsValidStmid,Rlatlon2Clatlon,gc_dist,AdeckBaseDir,MakeStmList,TcGenBasin2Area,getMd2tag,makeTcgenJsInventory
#from tcbase import getTyphoonCat,getSaffirSimpsonCat
#from tcbase import makeAdeckGens,makeAdeckGensTctrk,AdeckGen,AdeckGenTctrk
from TCtrk import TcPrBasin,tcgenModels,getBasinLatLonsPrecise,tcgenW3DatDir,tcgenW3Dir,tcgenModelLabel,getBasinOptFromStmids,tcgenBasins,getGentaus
from M2 import setModel2
from FM import wjetmodels
if(diag): MFd.dTimer('load')
from FM import FimRunModel2

from w2base import w2Colors

w2c=w2Colors()
jaecols=w2c.JaeCols
w2cols=w2c.W2Colors

#from TCtrk import TmTrkGen,TmTrkGenSimple,getFctrkGstdGtcBtcs,tcgenBasins,getGenDtgsByStorm,getBasinOptFromStmids,getGentaus

from VT import SumStats,SumStatsPlot

class TcStdStats(SumStats):

    def __init__(self,
                 taids,
                 tstmids,
                 ostats,
                 ):


        self.taids=taids
        self.vstmids=tstmids
        self.models=taids
        self.ostats=ostats

        self.initAidStorms()
        




class TcgenStats(SumStats):

    def __init__(self,
                 taids,
                 tstmids,
                 ostats,
                 ):


        self.taids=taids
        self.vstmids=tstmids
        self.models=taids
        self.ostats=ostats

        self.initAidStorms()
        

class TcgenStatsPlot(SumStatsPlot):

    def __init__(self,ss,
                 ptype,
                 basin,
                 ):

        pdir='/tmp'
        pdir='%s/tcgen'%(w2.HfipProducts)
        pname='%s.%s'%(ptype,basin)
        self.ss=ss
        self.ptype=ptype
        
        self.ppaths=[
            '%s/%s.png'%(pdir,pname),
            '%s/%s.eps'%(pdir,pname),
            '%s/%s.txt'%(pdir,pname),
            ]

        self.pvartagopt=None


    def basin2basinTitle(self,basin):

        if(self.basin == 'wpac'): self.basintitle='WestPAC'
        if(self.basin == 'epac'): self.basintitle='EastPAC'
        if(self.basin == 'lant'): self.basintitle='atLANTic'

    def setPlottitles(self,
                      toptitle1=None,
                      toptitle2=None,
                      ):

        models=self.ss.models

        # main title
        #
        if(toptitle1 == None):
            t1='please add using -1 command line option....'
        else:
            t1=toptitle1

        if(toptitle2 != None):
            t1=t1+'\n'+toptitle2

        # subtitle
        #

        if(hasattr(self.ss,'vstmids')):
            ovstmids=self.reducestmids(self.ss.vstmids)
        else:
            ovstmids=[]

        ns=len(ovstmids)
        nsmax=20
        t2b="Storms[N] [%d]: "%(ns)

        if(ns > nsmax):
            n1b=0
            n1e=nsmax/2
            n2b=ns-nsmax/2
            n2e=ns-1

            for n in range(n1b,n1e):
                ovstmid=ovstmids[n]
                t2b="%s %s"%(t2b,ovstmid)

            t2b="%s ..."%(t2b)

            for n in range(n2b,n2e):
                ovstmid=ovstmids[n]
                t2b="%s %s"%(t2b,ovstmid)

        else:
            for n in range(0,ns):
                ovstmid=ovstmids[n]
                if(n%20 == 0 and n != 0): t2b=t2b+'\n'
                t2b="%s %s"%(t2b,ovstmid)

        t2=t2b

        self.basin2basinTitle(basin)
        
        if(self.ptype == 'pr'):
            ylab='mean precip [mm/day]'
            t1='Areal-Mean Precip Rate [mm/day] in: %s'%(self.basintitle)
        elif(self.ptype == 'std'):
            ylab='sTDd [day]'
            t1="""Mean Scaled TD days (sTDd) [day] in: %s basin AKA 'Spuricanes'"""%(self.basintitle)
        elif(self.ptype == 'rc2t'):
            ylab="""Ratio Conv/Total Precip [%]"""
            t1="Ratio Conv/Total Precip [%%] in: %s basin"%(self.basintitle)

        self.ptitles=(t1,t2,ylab)

    def setControls(self):
        
        if(self.ptype == 'pr'):
            ptype1='pr'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,10.0,1.0],lgndloc)
        elif(self.ptype == 'rc2t'):
            ptype1='rc2t'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,130.0,10.0],lgndloc)
        elif(self.ptype == 'std'):
            ptype1='rc2t'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,6.0,1.0],lgndloc)
        else:
            print 'EEE invalid plot ptype in PlotsumStat: ',ptype
            sys.exit()
        self.controls=controls

    # -- plot method
    #


class TcStdStatsPlot(TcgenStatsPlot):

    def cformatVal(self,val1,val2,nc,diffv1v2=0,countonly=0,fformat='4.0f'):
        cval1=''
        if(val1 != ''):
            if(countonly):
                cval1="%d"%(nc)
            else:
                cval1="%4.1f[%d]"%(val1,nc)
        return(cval1)


class TcGenStatsHtml(MFhtml):
    
    def model2title(self,model):
        
        title=tcgenModelLabel[model]
        
        return(title)
            

    def __init__(self,basin,year,stmids,models,
                 ofg,oob,ourl,odtg,
                 veribystm,veribymodel,
                 gentau,
                 doobs=0,
                 verb=0):

        self.doobs=doobs
        self.verb=verb
        self.name='tcgen'
        self.titlename='TCgen'
        self.basin=basin
        self.year=year
        self.gentau=gentau
        
        self.pagename='TCgen%s'%(basin.upper())
        self.pagetitle="%s %d h"%(self.pagename,self.gentau)

        self.stmids=stmids
        self.models=models

        self.weburldir="%s"%(self.name)
        self.webdir="%s/%s"%(webdir,self.weburldir)
        self.htmlfile="stats.tcgen.%s.%s.t%03d.htm"%(self.basin,self.year,self.gentau)
        self.htmlurl="%s/%s/%s"%(self.weburlbase,self.weburldir,self.htmlfile)
        self.htmlpath="%s/%s"%(self.webdir,self.htmlfile)

        nmodels=len(models)
        for n in range(0,len(models)):
            if(n == 0):
                modeltitle=self.model2title(models[n])
                if(nmodels > 1): modeltitle=modeltitle+','
            elif(n > 0): modeltitle="%s %s"%(modeltitle,self.model2title(models[n]))
            if(n != nmodels-1 and n > 0): modeltitle=modeltitle+','

        self.modeltitle=modeltitle

        self.ofg=ofg
        self.oob=oob
        self.ourl=ourl
        self.odtg=odtg

        self.initTCs()


    def initTCs(self):

        def getbcol(tccat):

            if(tccat == 'td'): bcol=jaecols[31]; fcol=w2cols['black']
            elif(tccat == 'ts'): bcol=jaecols[21]; fcol=w2cols['black']
            elif(tccat == 'hu1'): bcol=jaecols[23]; fcol=w2cols['black']
            elif(tccat == 'hu2'): bcol=jaecols[24]; fcol=w2cols['black']
            elif(tccat == 'hu3'): bcol=jaecols[25]; fcol=w2cols['black']
            elif(tccat == 'hu4'): bcol=jaecols[28]; fcol=w2cols['white']
            elif(tccat == 'hu5'): bcol=jaecols[29]; fcol=w2cols['white']
            else: fcol=w2cols['black']; fcol=w2cols['white']
            
            return(bcol,fcol)
            

            
        self.stmCstyle={}
        self.stmLabel={}
        self.tD=TcData()

#' TY', 'ALEX        ', 85, 11.199999999999999, 18.199999999999999, 276.89999999999998, '2010062018', '2010070200', 5.7000000000000002, 10.5, 4.0999999999999996, 5.25)
        for stmid in self.stmids:
            tcstat=self.tD.getStmStats(stmid)

            try: tcvmax=tcstat[2]
            except: tcvmax=-999
            
            tccat='---'
            if(tcvmax > 0): tccat=getTyphoonCat(tcvmax) ; tccat=getSaffirSimpsonCat(tcvmax)

            ltccat=tccat.lower()
            
            if(len(tccat) == 2): tccat='&nbsp '+tccat
            
            (stm3id,stmname)=self.tD.getStmName3id(stmid)
            (bcol,fcol)=getbcol(ltccat)
            self.stmCstyle[stmid]='''style="background-color: %s; color: %s"'''%(bcol,fcol)
            self.stmLabel[stmid]="%s [%s  %03d kt] %s"%(stmid,tccat,tcvmax,stmname)


    def setTitleLocal(self):

        htmltitle='''
<td>
<table border=0 cellpadding=0 cellspacing=0 width=800 class='title'  >
<tr>
<col width=800>
<td>
%s Stats :: <b>Gentau: <font color=blue>%s</font> [h]</b> Basin: <font color=blue>%s</font> Year: <font color=blue>%s</font> Models: <font color=red>%s</font> 
</td>
</tr>
</table>
</td>
</tr>
</table>

'''%(self.titlename,self.gentau,self.basin.upper(),self.year,self.modeltitle)
        
        self.html='''%s
%s
'''%(self.html,htmltitle)

        

    def setplotTable(self):

        def getFGcstyle(ofg):

            tt=ofg.split('/')
            ncase=int(tt[0])
            std=tt[1]
            try: std=float(std)
            except: std=-999

            if(std < 0.0 and ncase >= 0):     bcol=w2cols['grey1']; fcol=w2cols['black']  ; strength=0
            elif(std >= 0.0 and std <= 0.7):  bcol=w2cols['grey3']; fcol=w2cols['white']  ; strength=1
            elif(std >  0.7 and std <= 3.0):  bcol=w2cols['olive']; fcol=w2cols['white']  ; strength=2
            elif(std > 3.0  and std <= 6.0):  bcol=w2cols['green']; fcol=w2cols['white']  ; strength=3
            elif(std > 6.0):                  bcol=w2cols['indigo']; fcol=w2cols['white'] ; strength=4
            
            if(ncase == -1):                  bcol=w2cols['red']; fcol=w2cols['white'] ; strength=5
            cstyle='''style="background-color: %s; color: %s"'''%(bcol,fcol)
            return(cstyle,bcol,fcol,strength)

        def getVeriStmcstyle(std):

            if(std < 0.0):                    bcol=w2cols['grey1']; fcol=w2cols['black']  ; strength=0
            elif(std >= 0.0 and std <= 25.0):  bcol=w2cols['yellow']; fcol=w2cols['black']  ; strength=1
            elif(std >  25.0 and std <= 75.0):  bcol=w2cols['yellowgreen']; fcol=w2cols['black'] ; strength=2
            elif(std >  75.0  and std <=100.0):  bcol=w2cols['green']; fcol=w2cols['white']  ; strength=3

            cstyle='''style="background-color: %s; color: %s"'''%(bcol,fcol)
            return(cstyle,bcol,fcol,strength)

        def getOBcstyle(ofg):

            tt=ofg.split('/')
            ndtg=int(tt[0])
            if(ndtg == 0):                  bcol=w2cols['grey4']; fcol=w2cols['white']
            elif(ndtg >=1 and ndtg <=2) :  bcol=w2cols['yellow']; fcol=w2cols['black']
            elif(ndtg == 3):               bcol=w2cols['yellowgreen']; fcol=w2cols['black']
            elif(ndtg > 3):                bcol=w2cols['darkred']; fcol=w2cols['white']

            cstyle='''style="background-color: %s; color: %s"'''%(bcol,fcol)
            return(cstyle)

            
        self.html='''%s\n<table class="stats" cellspacing="0"><tr>'''%(self.html)

        cstyle='''style="text-align: center"'''
        htm='''<td class="hed" %s >%s</td>'''%(cstyle,'Storm')
        self.html='''%s\n%s'''%(self.html,htm)
        for model in self.models:
            htm='''<td class="hedval60" >%s</td>'''%(self.model2title(model))
            self.html='''%s\n%s'''%(self.html,htm)
            if(self.doobs):
                htm='''<td class="hedval60" >OBS</td>'''
                self.html='''%s\n%s'''%(self.html,htm)

        self.html='''%s\n</tr>'''%(self.html)

        for stmid in self.stmids:

            try:     cstyle=self.stmCstyle[stmid]
            except:  cstyle=''
            
            htm='''<td class="field" %s >%s</td>'''%(cstyle,self.stmLabel[stmid])
            self.html='''%s\n%s'''%(self.html,htm)

            for model in self.models:
                
                (fgcstyle,bcol,fcol,fgstrength)=getFGcstyle(self.ofg[model,stmid])
                obcstyle=getOBcstyle(self.oob[model,stmid])
                fgcval=self.ofg[model,stmid]
                curl=self.ourl[model,stmid]
                tdtgs=str(self.odtg[model,stmid])
                if(curl != None):
                    if(fgstrength == 1):
                        fgcval='''<a class="linkText" style="font-weight: normal" href="%s" title="%s" >%s</a>'''%(curl,tdtgs,fgcval)
                    else:
                        fgcval='''<a class="linkText" href="%s" title="%s" >%s</a>'''%(curl,fgcval,fgcval)

#<td>
#<input type='button' class='databutton'
#onMouseOver="className='databuttonOVER';"
#onMouseOut="className='databutton';"
#value='TCdiag.file' name=taub
#onClick="javascript:popUp('test.txt');">
#</td>

                htmfg='''<td class="val60" %s >%s</td>'''%(fgcstyle,fgcval)
                if(self.doobs):
                    htmob='''<td class="val60" %s >%s</td>'''%(obcstyle,self.oob[model,stmid])
                    self.html='''%s\n %s\n %s\n'''%(self.html,htmfg,htmob)
                else:
                    self.html='''%s\n %s\n '''%(self.html,htmfg)

            try:
                fval=veribystm[stmid]
                cval="% 3.0f"%(fval)
            except:
                cval='----'
                fval=-999.0

            
            (fgcstyle,bcol,fcol,fgstrength)=getVeriStmcstyle(fval)

                
            htmfg='''<td class="val60" %s >%s</td>'''%(fgcstyle,cval)
            self.html='''%s\n %s\n'''%(self.html,htmfg)
            
            self.html='''%s\n</tr>'''%(self.html)

        htm='''<td class="hedval60" >%s</td>'''%('bottomline by model')
        self.html='''%s\n%s'''%(self.html,htm)

        for model in self.models:
            (fgcstyle,bcol,fcol,fgstrength)=getFGcstyle(self.ofg[model,stmid])
            fgcval=self.ofg[model,stmid]
            curl=self.ourl[model,stmid]
            tdtgs=str(self.odtg[model,stmid])
            try:
                fval=veribymodel[model]
                cval="%3.0f"%(fval)
            except:
                fval=-999.0
                cval='----'
                
            (fgcstyle,bcol,fcol,fgstrength)=getVeriStmcstyle(fval)
            htmfg='''<td class="val60" %s >%s</td>'''%(fgcstyle,cval)
            if(self.doobs): 
                htmob='''<td class="val60" %s >----</td>'''%(fgcstyle)
                self.html='''%s\n %s\n %s\n'''%(self.html,htmfg,htmob)
            else:
                self.html='''%s\n %s\n'''%(self.html,htmfg)
                
        

        self.html='''%s\n</table>'''%(self.html)


    def doHtml(self):

        self.initTopLine()
        self.initHead(cssdir='css',
                      jsdir='js',
                      cssfile='wxmain.css',
                      icondir='.')
        
        if(self.verb): self.printStats()
        self.setTitleLocal()
        self.setplotTable()
        self.initTail()
        self.writeHtml(verb=1)



    def doPyp(self,verb=1):

        del self.tD
        del self.tG
        try: del self.tGtrk
        except: None
        if(verb): print 'III writing html pyp: ',self.pyppathHtml
        self.putPyp(pyppath=self.pyppathHtml,verb=verb)
            

        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class AdgenCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            2:['modelopt',    'model'],
            }

        self.defaults={
            'doupdate':0,
            }

        self.options={
            'override':     ['O',0,1,'override'],
            'verb':         ['V',0,1,'verb=1 is verbose'],
            'ropt':         ['N','','norun',' norun is norun'],
            'diag':         ['d',0,1,' diag prints'],
            'ptype':        ['p:','pr','a','ptype = pr|std|rc2t'],
            'gentauOpt':    ['t:','all','a','gentauOpt -- fc tau for genesis'],
            'basinopt':     ['b:','epac','a',' basin with gen adecks'],
            'toptitle1':    ['1:',None,'a','toplabel1'],
            'toptitle2':    ['2:',None,'a','toplabel2'],
            'dogenstats':   ['g',0,1,'dogenstats = 1 genesis stats'],
            'genStatOpts':  ['G:',None,'a','set opts on genesis stats'],
            'dostats':      ['s',0,1,'dostats = 1 stats'],
            'stmopt':       ['S:',None,'a','stmopt'],
            }

        self.purpose='''
purpose -- analyze tcgen '''
        self.examples='''
%s test
'''

gaopt='-g 1200x900'
tcgenPhp='http://ruc.noaa.gov/hfip/tcgen/tcgen.php'

from TCtrk import tcgenW3Dir as webdir
webdir=w2.HfipProducts

#tcgenW3DatDir='/dat3/tc/hfip'
# -- kaze/kishou location of tcgen.pypdb
ttcgbdir="%s/../w21/dat/tc/tcgen"%(w2.HfipProducts)

# -- local  
#
if(w2.onTaifuu or w2.onKishou):
    ttcgbdir="/w21/dat/tc/tcgen"

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

argv=sys.argv
CL=AdgenCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

gentaus=getGentaus(gentauOpt)

alltag="ALLDONE %s %s %s"%(dtgopt,modelopt,stmopt)
MF.sTimer(tag=alltag)

if(dogenstats):

    def sumList(list):
        if(list == None):
            sum=None
        else:
            sum=0.0
            for l in list:
                sum=sum+float(l)
        return(sum)

    def makeuRl(list,model,stmid,basin,gentau):
        if(list == None): return(list)
        if(len(list) == 0):
            return(None)
        elif(len(list) == 1):
            gdtg=list[0]
        elif(len(list) == 2):
            gdtg=list[1]
        elif(len(list) == 3):
            gdtg=list[1]
        else:
            gdtg=list[len(list)/2]
        url='''%s?dtg=%s&basin=%s&pmode=veri&model=%s&tau=%03d&bseason=%s'''%(tcgenPhp,gdtg,basin,model,gentau,basin)
        return(url)

    def getFG(fstds,model,stmid,gentau,fdtgs,do24hScale=1):
        
        fg=[]
        for dtg in fdtgs:
            ff=fstds[model,stmid,gentau,dtg]
            if(ff[0] > 0.):
                ffo=ff[0]
                if(do24hScale): 
                    ffo=ff[0]
                    fflife=ff[-1]
                    if(fflife > 24.0):
                        fscl=24.0/fflife
                        ffo=ffo*fscl
                fg.append(ffo)
                
        if(len(fg) == 0): fg=None
        return(fg)
        
    def getNruns(fstds,model,stmid,gentau,fdtgs):
        
        nr=0
        for dtg in fdtgs:
            ff=fstds[model,stmid,gentau,dtg]
            if(ff[0] > 0. or ff[0] == -99.0):
                nr=nr+1
        return(nr)
        

    # -- get gen stat opts
    #
    doobs=0
    if(genStatOpts != None):
        tt=genStatOpts.split(':')
        doobs=int(tt[0])
        
        
    MF.sTimer('stats')

    imask="%s/verigen.*.txt"%(ttcgbdir)
    ipath="%s/verigen.%s.%s.%s.txt"%(ttcgbdir,modelopt,stmopt,gentauOpt)
    
    print 'iiii',ipath
    
    ipaths=glob.glob(imask)
    
    if(ipath in ipaths):
        cards=open(ipath)
    else:
        print """EEE can't find %s in:"""%(ipath,ipaths)
        sys.exit()
        
    tmodels=[]
    tstmids=[]
    tstmdtgs={}
    
    #n;tt 0 rtfim9
    #n;tt 1 01L.2013
    #n;tt 2 2013060500
    #n;tt 3 108
    #n;tt 4 O:
    #n;tt 5 1.4
    #n;tt 6 25
    #n;tt 7 23.3
    #n;tt 8 271.2
    #n;tt 9 NA
    #NA rtfim9   01L.2013 2013060500 108 O:  1.4   25  23.3 271.2 NA    
    
    
    
    #n;tt 0 rtfim9
    #n;tt 1 01L.2013
    #n;tt 2 2013060500
    #n;tt 3 132
    #n;tt 4 O:
    #n;tt 5 1.4
    #n;tt 6 25
    #n;tt 7 23.3
    #n;tt 8 271.2
    #n;tt 9 FAILED
    #FAILED rtfim9   01L.2013 2013060500 132 O:  1.4   25  23.3 271.2 FAILED    
    
    
    #n;tt 0 rtfim9
    #n;tt 1 01L.2013
    #n;tt 2 2013060600
    #n;tt 3 000
    #n;tt 4 O:
    #n;tt 5 0.3
    #n;tt 6 35
    #n;tt 7 25.6
    #n;tt 8 273.5
    #n;tt 9 M:
    #n;tt 10 0.7
    #n;tt 11 35
    #n;tt 12 25.4
    #n;tt 13 273.1
    #n;tt 14 FGT
    #n;tt 15 000
    #n;tt 16 6.0
    #rtfim9   01L.2013 2013060600 060 O:  3.1   35  25.6 273.5 M:  2.4   32  23.4 272.2 FGT 060  60.0    
    
    fstds={}
    ostds={}
    
    
    for card in cards:
        if(verb): print card[:-1]
        tt=card.split()
        #for n in range(0,len(tt)):
        #    print 'n;tt',n,tt[n]
            
        model=tt[0]
        stmid=tt[1]
        dtg=tt[3]

        n=4
        gentau=int(tt[n]) ; n=n+2
        ostd=float(tt[n]) ; n=n+1
        ovmax=float(tt[n]) ; n=n+1
        olat=float(tt[n]) ; n=n+1
        olon=float(tt[n]) ; n=n+1
        olife=24    
        
        if(tt[n] == 'NA'):
            fstd=-1.0
            fvmax=-999
            flat=-99.
            flon=-999.
            ftype='NA'
            flife=-999.
            
        elif(tt[n] == 'FAILED'):
            fstd=-99.
            fvmax=-999
            flat=-99.
            flon=-999.
            ftype='NA'
            flife=-999.
            
        else:
            n=n+1
            fstd=float(tt[n]) ; n=n+1
            fvmax=float(tt[n]) ; n=n+1
            flat=float(tt[n]) ; n=n+1
            flon=float(tt[n]) ; n=n+1
            ftype=tt[n] ; n=n+2
            flife=float(tt[n]) ; n=n+1
            
        tstmids.append(stmid)
        tmodels.append(model)
        MF.appendDictList(tstmdtgs,stmid,dtg)
        ostds[model,stmid,gentau,dtg]=[ostd,ovmax,olat,olon,olife]
        fstds[model,stmid,gentau,dtg]=[fstd,fvmax,flat,flon,flife]
        
    MF.uniqDictList(tstmdtgs)
    
    tmodels=mf.uniq(tmodels)
    tstmids=mf.uniq(tstmids)
    
    basins=getBasinOptFromStmids(tstmids)
    

    for gentau in gentaus:

        veribystm={}
        veribymodel={}
        
        ofg={}
        oob={}
        ourl={}
        odtg={}

        nModelRuns={}
        nModelRunsByStm={}
        
        for stmid in tstmdtgs:
            nModelRunsByStm[stmid]=0

        for model in tmodels:

            nModelRuns[model]=0
            for stmid in tstmids:

                fdtgs=tstmdtgs[stmid]

                fr=getNruns(fstds, model, stmid, gentau, fdtgs)
                fg=getFG(fstds, model, stmid, gentau, fdtgs)
                ob=getFG(ostds, model, stmid, gentau, fdtgs)
                fgsum=sumList(fg)
                obsum=sumList(ob)
                nfg=0
                ofgsum='----'
                if(fgsum != None and fr > 0): nfg=len(fg) ; ofgsum="%4.1f"%(fgsum)
                if(fr == 0): nfg=-1 ; ofgfsum="NoRn"

                if(nfg != -1): 
                    nModelRuns[model]=nModelRuns[model]+1
                    nModelRunsByStm[stmid]=nModelRunsByStm[stmid]+1
                
                nob=0
                oobsum='----'
                if(obsum != None): nob=len(ob) ; oobsum="%4.1f"%(obsum)

                url=makeuRl(fdtgs,model,stmid,basins[0],gentau)
                
                odtg[model,stmid]=fdtgs
                ourl[model,stmid]=url
                ofg[model,stmid]="%1d/%s"%(nfg,ofgsum)
                oob[model,stmid]="%1d/%s"%(nob,oobsum)

                
                if(nob >= 2 and nfg >= 1):
                    MF.loadDictList(veribystm,stmid,1)
                    MF.loadDictList(veribymodel,model,1)

                if(verb): print 'AAA ',model,stmid,gentau,' fg: ',nfg,ofgsum,' ob: ',nob,oobsum,' url: ',url  #,fg,ob


        for k in veribystm.keys():
            veribystm[k]=MF.sumList(veribystm[k])
            nmodels=nModelRunsByStm[k]
            if(nmodels == 0): nmodels=len(tmodels)
            veribystm[k]=(veribystm[k]/nmodels)*100.0
        
        for k in veribymodel.keys():
            veribymodel[k]=MF.sumList(veribymodel[k])
            veribymodel[k]=(veribymodel[k]/nModelRuns[k])*100.0
            
        year=tstmids[-1].split('.')[1]
        hTG=TcGenStatsHtml(basins[0],year,tstmids,tmodels,
                           ofg,oob,ourl,odtg,
                           veribystm,veribymodel,
                           gentau,
                           doobs=doobs,
                           verb=verb)
        hTG.doHtml()

        
        print 'SSSSSSSSSSSSS ',veribystm
        print 'MMMMMMMMMMMMM ',veribymodel

    MF.dTimer(tag=alltag)
    sys.exit()




if(dostats):

    ttS=TmTrkGenSimple()

    MF.sTimer('stats')

    MF.sTimer('numpy')
    import numpy.ma as ma
    MF.dTimer('numpy')

    undef=-999.

    MF.sTimer('gettgcards')
    dsname='tcgcards'
    tgD=DSs.getDataSet(key=dsname)
    if(not(hasattr(tgD,'tcgcards'))):
        tcgcards={}
    else:
        tcgcards=tgD.tcgcards

    #print tcgcards.keys()
    MF.dTimer('gettgcards')


    prs={}
    rc2ts={}
    stds={}
    stmids={}

    ostats={}
    ostmids=[]
    
    idtgs=[]
    imodels=[]
    ibasins=[]
    igentaus=[]


    for gentau in gentaus:

        for model in models:

            for basin in basins:

                for dtg in tdtgs:

                    try:
                        rc=tcgcards[model,dtg,basin,gentau]
                    except:
                        continue

                    idtgs.append(dtg)
                    imodels.append(model)
                    ibasins.append(basin)
                    igentaus.append(gentau)

                    if(rc != None):
                        if(len(rc) == 16):
                            (opr,oprc,orc2t,
                             actStmids,
                             actHitGtcs,genHitGtcs,genGtcs,
                             nGenTc,nGenHit,
                             pr,prc,rc2t,
                             nNo,genNOGtcs,sumStdd,
                             cards,
                             )=rc
                            
                        elif(len(rc) == 15):
                            (opr,oprc,orc2t,
                             actStmids,
                             actHitGtcs,genHitGtcs,genGtcs,
                             nGenTc,nGenHit,
                             pr,prc,rc2t,
                             nNo,sumStdd,
                             cards,
                             )=rc

                        
                    if(diag):
                        print "DDDDDDDDDDDD   %7s %s %-4s %03d  opr: %s"%(model,basin,dtg,gentau,opr)
                        
        
                    kk=(model,basin,gentau)
                    MF.appendDictList(prs,kk,pr)
                    MF.appendDictList(rc2ts,kk,rc2t)
                    MF.appendDictList(stds,kk,sumStdd)

                    for astmid in actStmids:
                        MF.appendDictList(stmids,kk,astmid)
            

    idtgs=MF.uniq(idtgs)
    imodels=MF.uniq(imodels)
    ibasins=MF.uniq(ibasins)
    igentaus=MF.uniq(igentaus)


    MF.dTimer('stats')

    for model in imodels:
        for basin in ibasins:
            for gentau in gentaus:
                prs[model,basin,gentau]=ma.array(prs[model,basin,gentau])
                rc2ts[model,basin,gentau]=ma.array(rc2ts[model,basin,gentau])
                stds[model,basin,gentau]=ma.array(stds[model,basin,gentau])
                ostmids=stmids[model,basin,gentau]
                ostmids=MF.uniq(ostmids)
                stmids[model,basin,gentau]=ostmids


    for model in imodels:
        for basin in ibasins:
            for gentau in gentaus:
                p=ma.masked_equal(prs[model,basin,gentau],-999.)
                r=ma.masked_equal(rc2ts[model,basin,gentau],-999.)
                s=ma.masked_equal(stds[model,basin,gentau],-999.)

                np=ma.count(p)
                nr=ma.count(r)
                ns=ma.count(s)

                ostats[model,gentau,'pr']=(p.mean(),np)

                if(nr != 0):
                    ostats[model,gentau,'rc2t']=(r.mean()*100.0,nr)
                else:
                    ostats[model,gentau,'rc2t']=(undef,nr)
                
                ostats[model,gentau,'std']=(s.mean(),ns)
                
                print model,basin,gentau,' pr: ',p.mean(),p.max(),p.min(),' n: ',np,' c2t: ',r.mean(),' std: ',s.mean(),s.max(),s.min()


    omodels=[]
    for model in imodels:
        for basin in ibasins:
            for gentau in gentaus:
                (val,n)=ostats[model,gentau,ptype]
                if(val != undef): omodels.append(model)


    #models=MF.uniq(omodels)

    tstmids=[]
    for model in models:
        tstmids=tstmids+stmids[model,basin,gentau]
    tstmids=MF.uniq(tstmids)

    ss=TcStdStats(models,tstmids,ostats)
    print ss.ostats
    print ss.vstmids

    statkey=ptype
    sdicts=[]
    ndicts=[]

    for n in range(0,len(models)):
        model=models[n]
        sdict={}
        ndict={}

        for gentau in gentaus:
            sdict[gentau]=ostats[model,gentau,statkey][0]
            ndict[gentau]=ostats[model,gentau,statkey][1]

        sdicts.append((sdict,sdict))
        ndicts.append(ndict)



    if(ptype == 'std'):
        pss=TcStdStatsPlot(ss,statkey,basin)
    else:
        pss=TcgenStatsPlot(ss,statkey,basin)
    if(verb): pss.ls()

    do1stplot=0
    do2ndplot=1

    pss.basin=basin
    pss.setPlottitles(toptitle1,toptitle2)
    pss.setControls()
    pss.simpleplot(ss.models,sdicts,ndicts,ss.labaids,ss.colaids,
                   ilmarker=ss.markaids,
                   do1stplot=do1stplot,
                   do2ndplot=do2ndplot,
                   dopng=1,
                   doshow=1)


    sys.exit()

