#!/usr/bin/env python

from tcbase import *
import FM
import w2

from TCdiag import *

class TcDiagHtml(MFhtml):

    def __init__(self,tG=None,tGtrk=None,verb=0):

        self.tG=tG
        self.tGtrk=tGtrk

        self.verb=verb
        self.name='tcdiag'
        self.pagename='TCdiag'

        self.rctG=1
        if(not(hasattr(tG,'year'))):
            self.rctG=0
            return

        self.year=self.tG.year
        self.dtg=self.tG.dtg
        self.model=self.tG.model.lower()
        self.umodel=self.tG.model.upper()
        self.stmid=self.tG.stmid.lower()
        self.basename=self.tG.basename
        if(hasattr(tG,'aidtrk')): self.aidtrk=self.tG.aidtrk

        self.trkploturl=self.tGtrk.trkploturl

        if(hasattr(tG,'webdir')):
            self.webdir=self.tG.webdir
        else:
            print 'EEE(TcDiagHtml) webdir not set in tG object'
            sys.exit()

        self.weburldir="%s/%s/%s/%s"%(self.name,self.year,self.dtg,self.model)
        self.webdir="%s/%s"%(self.webdir,self.weburldir)

        self.htmlfile="%s.%s.%s.htm"%(self.model,self.dtg,self.stmid)
        self.htmlurl="%s/%s/%s"%(self.weburlbase,self.weburldir,self.htmlfile)
        self.htmlpath="%s/%s"%(self.webdir,self.htmlfile)

        self.pagetitle="%s :: %s %s  %s"%(self.basename,self.dtg,self.model,self.stmid)

        self.databutton='''
<input type='button' class='databutton'
onMouseOver="className='databuttonOVER';"
onMouseOut="className='databutton';"
value='%s.file' name=taub
onClick="javascript:popUp('test.txt');">
'''%(self.basename)
        
        self.trkbutton='''
<input type='button' class='databutton'
onMouseOver="className='databuttonOVER';"
onMouseOut="className='databutton';"
value='%s.TRKplot' name=taub
onClick="url='%s',poptastic(url);">
'''%(self.basename,self.trkploturl)
        
        self.htmldiag={}

        self.taus=self.tG.taus
        # -- check if taus reduced because of going to far poleward
        #
        if( hasattr(tG,'stmTaus') and (len(self.taus) > len(tG.stmTaus)) ):
            self.taus=tG.stmTaus

        self.diagKeys=self.tG.diagKeys
        self.diagVals=self.tG.diagVals
        self.diagTypes=self.tG.diagTypes
        self.diaguRls=self.tG.diaguRls
        self.diagFilenames=self.tG.diagFilenames
        self.pyppathHtml=self.tG.pyppathHtml

        self.initTCs()


        datatrkhtm='''
<table border=0 cellpadding=0 cellspacing=0 width=1000 style='table-layout:fixed' >
<col width=100>
<col width=100>
<col width=800>
<tr>
<td>
%s
</td>
<td>
%s
</td>
 '''%(self.databutton,self.trkbutton)
        
        self.htmltitle='''
 %s <td>
<table border=0 cellpadding=0 cellspacing=0 width=800 class='title'  >
<tr>
<col width=800>
<td>
&nbsp;&nbsp;
 Model: <font color=blue>%s</font> Dtg: <font color=blue>%s</font>
 TC: <font color=red>%s [%s]</font>  TCVmax: <font color=red>%d</font>
<a href="%s" rel="lightbox" title="trkplot" >TRKplot</a>
</td>
</tr>
</table>
</td>
</tr>
</table>

'''%(datatrkhtm,modelOname[self.model],self.dtg,self.stmid.upper(),self.stmname,int(self.tcvmax),self.trkploturl)
        


        
    def doHtml(self):

        self.initTopLine()
        self.initHead()
        if(self.verb): self.printStats()
        self.setTitleLocal()
        self.setplotTable()
        self.initTail()
        self.writeHtml()


    def setTitleLocal(self,htmltitle=None):

        if(htmltitle == None): htmltitle=self.htmltitle

        self.html='''%s
%s
'''%(self.html,htmltitle)



    def doPyp(self,verb=0):

        del self.tD
        del self.tG
        try: del self.tGtrk
        except: None
        if(verb or self.verb): print 'III writing html pyp: ',self.pyppathHtml
        self.putPyp(pyppath=self.pyppathHtml,verb=verb)
            

    def setplotTable(self):

        self.html='''%s\n<table class="stats" cellspacing="0"><tr>'''%(self.html)

        dkeys=self.diagKeys

        for dkey in dkeys:

            self.htmldiag[dkey]=''

            cstyle=''
            if(mf.find(dkey,'TIME')):  cstyle='''style="background-color: #B0C4DE; color: #000000"'''


            #if(self.diagFilenames[dkey] != 'None'):
            #    curl="../%s.htm"%(self.diagFilenames[dkey])
            #    cval=dkey
            #    cval='''<a href="%s" >%s</a>'''%(curl,cval)
            #else:
            #    cval=dkey

            if(not(mf.find(dkey,'TIME'))):
                curl="../%s.htm"%(self.diagFilenames[dkey])
                cval=dkey
                cval='''<a class="linkTextb" href="%s" >%s</a>'''%(curl,cval)
            else:
                cstyle='''style="background-color: #B0C4DE; color: #000000"'''
                cval=dkey

            htm='''<td class="field" %s >%s</td>'''%(cstyle,cval)
            self.html='''%s\n%s'''%(self.html,htm)
            self.htmldiag[dkey]=self.htmldiag[dkey]+htm
            
            for tau in self.taus:
                
                cval=self.diagVals[tau][dkey]
                if(float(cval) == -9999.): cval=' 9999'

                # -- in case a bad number gets to this point
                #
                if(len(cval) > 5):  cval='9999'

                ctype=self.diagTypes[tau][dkey]
                if(self.diaguRls[tau][dkey] != 'None'):
                    curl=self.diaguRls[tau][dkey]
                    curl="../../../%s"%(curl)
                    ###cval='''<a href="javascript:poptastic('%s');">%s</a>'''%(curl,cval)
                    cval='''<a class="linkText" href="%s" rel="lightbox" title="%s" >%s</a>'''%(curl,cval,cval)

                cstyle=''
                if(ctype == 'storm'):                           cstyle='''style="background-color: #FFB6C1; color: #000000"'''
                if(ctype == 'custom'):                          cstyle='''style="background-color: #FFFFF0; color: #000000"'''
                if(ctype == 'sounding'):                        cstyle='''style="background-color: #87CEFA; color: #000000"'''
                if(mf.find(self.diagVals[tau][dkey],'9999')):   cstyle='''style="background-color: #888; color: #fff"'''
                if(mf.find(dkey,'TIME')):                       cstyle='''style="background-color: #B0C4DE; color: #000000"'''

                htm='''<td class="val" %s >%s</td>'''%(cstyle,cval)
                self.html='''%s\n%s'''%(self.html,htm)

            self.html='''%s\n</tr>'''%(self.html)

        self.html='''%s\n</table>'''%(self.html)


    def printStats(self):


        for tau in self.taus:
            for dkey in self.diagKeys:
                print tau,dkey,self.diagVals[tau][dkey],self.diaguRls[tau][dkey]
        



        
class TcDiagHtmlVars(TcDiagHtml):


    def __init__(self,tG=None,verb=0):


        self.tG=tG

        self.verb=verb
        self.name='tcdiag'
        self.pagename='TCdiagVars'
        
        self.year=self.tG.year
        self.dtg=self.tG.dtg
        self.model=self.tG.model.lower()
        self.umodel=self.tG.model.upper()
        self.basename=self.tG.basename
        self.stmid=self.tG.stmid

        self.weburldir="%s/%s/%s"%(self.name,self.year,self.dtg)
        if(hasattr(tG,'webdir')):
            self.webdir=self.tG.webdir
        else:
            print 'EEE(TcDiagHtmlVars) webdir not set in tG object'
            sys.exit()
            
        self.webdir="%s/%s"%(self.webdir,self.weburldir)

        self.htmldiag={}

        self.inittGhPyps()



    def inittGhPyps(self,verb=0):


        vkeys=[]
        vtaus=[]
        vmodels=[]
        vmodelurls={}

        vvals={}
        vurls={}
        vctypes={}

        htmlpyps=glob.glob("%s/*/*htm*pyp"%(self.webdir))

        n=0
        for pyp in htmlpyps:
            (dir,file)=os.path.split(pyp)
            tgH=self.getPyp(pyppath=pyp)
            ss=file.split('.')
            stmid="%s.%s"%(ss[1],ss[2])
            if(stmid == self.stmid):
                n=n+1
                model=dir.split('/')[len(dir.split('/'))-1]
                vmodels.append(model)
                try:
                    vmodelurls[model]=tgH.htmlfile
                except:
                    print 'WWWW unable to read pyp: ',pyp
                    continue

                if(n == 1):
                    vkeys=tgH.diagKeys
                    vfilenames=tgH.diagFilenames
                    
                if(len(tgH.taus) > len(vtaus)): vtaus=tgH.taus

                vvals[model]=tgH.diagVals
                vurls[model]=tgH.diaguRls
                vctypes[model]=tgH.diagTypes


                if(verb):
                    for kk in kks:
                        print kk,tgH.diagFilenames[kk]
                        for tau in tgH.taus:
                            print tgH.diagVals[tau][kk],tgH.diaguRls[tau][kk]


        # -- no diags for stmid
        #
        if(len(vkeys) == 0):
            self.vkeys=vkeys
            return(0)
        
        if(verb):
            print '     vkeys: ',vkeys
            print '     vtaus: ',vtaus
            print '   vmodels: ',vmodels
            print 'vfilenames: ',vfilenames
            for vmodel in vmodels:
                print 'vvvvv ',vmodel,vvals[model].keys(),vurls[model].keys()


        self.vkeys=vkeys
        self.vmodels=vmodels
        self.vtaus=vtaus
        self.vfilenames=vfilenames
        self.vvals=vvals
        self.vurls=vurls
        self.vmodelurls=vmodelurls
        self.vctypes=vctypes
        


    def doHtml(self):

        rc=1
        if(len(self.vkeys) == 0):
            rc=0
            return(rc)
        
        for vkey in self.vkeys:

            if(mf.find(vkey,'TIME')): continue
            self.pagetitle="%s %s"%(vkey,self.dtg)
            self.htmltitle="%s for models at dtg:<font color=blue>%s</font> TC: <font color=red>%s</font>"%(vkey,self.dtg,self.stmid)
            self.htmlfile="%s.htm"%(self.vfilenames[vkey])
            self.htmlpath="%s/%s"%(self.webdir,self.htmlfile)
            self.htmlurl="%s/%s/%s"%(self.weburlbase,self.weburldir,self.htmlfile)

            self.initTopLine()
            self.initHead(bdir='../..')
            self.setTitle()
            self.setplotTable(vkey)
            self.initTail()
            self.writeHtml(verb=1)

        return(rc)



    def setplotTable(self,tvkey):

        self.html='''%s\n<table class="stats" cellspacing="0"><tr>'''%(self.html)

        for vkey in self.vkeys:

            if( not(mf.find(vkey,'TIME') or vkey == tvkey) ):continue


            if(mf.find(vkey,'TIME')):
                
                cstyle=''
                if(mf.find(vkey,'TIME')):  cstyle='''style="background-color: #B0C4DE; color: #000000"'''
                htm='''<td class="field" %s >%s</td>'''%(cstyle,vkey)
                self.html='''%s\n%s'''%(self.html,htm)
                    
                for vtau in self.vtaus:
                    cval=vtau
                    cstyle=''
                    cstyle='''style="background-color: #B0C4DE; color: #000000"'''
                    htm='''<td class="val" %s >%s</td>'''%(cstyle,cval)
                    self.html='''%s\n%s'''%(self.html,htm)

                self.html='''%s\n</tr>'''%(self.html)


            else:

                
                for vmodel in self.vmodels:

                    cstyle=''
                    
                    curl="%s/%s"%(vmodel,self.vmodelurls[vmodel])
                    cval=vmodel.upper()

                    curltrk="../../%s/%s/%s/trkplt.%s.%s.png"%(self.year,self.dtg,vmodel,self.stmid,vmodel)
                    cvaltrk='TRK'

                    cval='''<a class="linkTextb" href="%s" >%s</a>&nbsp;<a class="linkTextb" href="%s" rel="lightbox" >%s</a>'''%(curl,cval,curltrk,cvaltrk)

                    htm='''<td class="field" %s >%s</td>'''%(cstyle,cval)
                    self.html='''%s\n%s'''%(self.html,htm)
                    
                    for vtau in self.vtaus:

                        try:
                            cval=self.vvals[vmodel][vtau][tvkey]
                        except:
                            cval='9999'

                        # -- in case a bad number gets to this point
                        #
                        if(len(cval) > 5):  cval='9999'
                            
                        try:
                            curl=self.vurls[vmodel][vtau][tvkey]
                        except:
                            curl='None'

                        try:
                            ctype=self.vctypes[vmodel][vtau][tvkey]
                        except:
                            ctype='None'

                        if(curl != 'None'):
                            curl="../../%s"%(curl)
                            cval='''<a class="linkText" href="%s" rel="lightbox" title="%s" >%s</a>'''%(curl,cval,cval)

                        cstyle=''
                        if(ctype == 'storm'):                           cstyle='''style="background-color: #FFB6C1; color: #000000"'''
                        if(ctype == 'custom'):                          cstyle='''style="background-color: #FFFFF0; color: #000000"'''
                        if(ctype == 'sounding'):                        cstyle='''style="background-color: #87CEFA; color: #000000"'''
                        if(mf.find(cval,'9999')):                       cstyle='''style="background-color: #888; color: #fff"'''
                        #if(mf.find(tvkey,'TIME')):                       cstyle='''style="background-color: #B0C4DE; color: #000000"'''

                        htm='''<td class="val" %s >%s</td>'''%(cstyle,cval)
                        self.html='''%s\n%s'''%(self.html,htm)

                    self.html='''%s\n</tr>'''%(self.html)


        self.html='''%s\n</table>'''%(self.html)



        
class phpInv(MFbase):

    def PrintHash(self,hash,name='hash',verb=0):

        cards=[]
        kk=hash.keys()
        kk.sort()
        nh=len(hash)

        if(verb):
            print kk
            print nh
            
        if(isinstance(kk[0],tuple)):   nk=len(kk[0])
        else:                          nk=1

        
        card="%s %d %d"%(name,nk,nh)
        cards.append(card)

        for k in kk:
            card=''
            if(isinstance(k,tuple)):
                for n in k:
                    card=card+' '+n
            else:
                card=card+' '+k

            card=card+' : '
            for n in hash[k]:
                card=card+' '+n
            cards.append(card)

        return(cards)


    def uNiqHash(self,hash):
        tt={}
        for kk in hash.keys():
            dd=hash[kk]
            dd=mf.uniq(dd)
            tt[kk]=dd
        return(tt)



class TcdiagInv(phpInv):



    def __init__(self,tG,
                 dtgopt=None,
                 ndayback=25,
                 verb=1):

        MF.sTimer(tag='inv.tcdiag')

        if(dtgopt == None):
            bdtg="cur12-d%d"%(ndayback)
            tdtgopt="%s.cur12"%(bdtg)
            tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

        elif(not(mf.find(dtgopt,'cur'))):
            edtg=mf.dtg_command_prc(dtgopt)
            bdtg=mf.dtginc(edtg,-24*ndayback)
            tdtgopt="%s.%s"%(bdtg,edtg)
            tdtgs=mf.dtg_dtgopt_prc(tdtgopt)
            
        elif(len(dtgopt.split('.')) > 1):
            tdtgs=mf.dtg_dtgopt_prc(dtgopt)
            
        else:
            print 'EEE invalid dtgopt: ',dtgopt,' in TcdiagInv'

        webdir=tG.webdir
        tD=TcData()

        webdir="%s/%s"%(webdir,tG.basename.lower())
        MF.ChangeDir(webdir)

        stmsDtg={}
        allstmsDtg={}
        dtgsStm={}
        dtgsModel={}
        modelsDtgStm={}

        for dtg in tdtgs:

            year=dtg[0:4]

            hmask="%s/%s/*/*.htm"%(year,dtg)

            htmls=glob.glob(hmask)

            if(len(htmls) == 0):
                print 'WWW no htmls in webdir: ',webdir,' for dtg: ',dtg

            for html in htmls:
                (dir,file)=os.path.split(html)
                (base,ext)=os.path.splitext(file)
                tt=file.split('.')
                model=tt[0]
                dtg=tt[1]
                stm3id=tt[2]
                stmyear=tt[3]
                stm="%s.%s"%(stm3id,stmyear)
                stm=stm.upper()
                if(verb): print 'FFF model: ',model,dtg,stm
                # -- dtg <- model
                MF.appendDictList(dtgsModel,model,dtg)
                # -- stm <- dtg
                MF.appendDictList(stmsDtg,dtg,stm)
                # -- dtg <- stm
                MF.appendDictList(dtgsStm,stm,dtg)
                # -- models <- dtg,basin
                MF.append2TupleKeyDictList(modelsDtgStm,dtg,stm,model)


            if(len(htmls) > 0):
                allstmsDtg[dtg]=tD.getStmidDtg(dtg)
                if(verb): print 'FFF allstms: ',dtg,allstmsDtg[dtg]
              
        stmsDtg=self.uNiqHash(stmsDtg)
        dtgsStm=self.uNiqHash(dtgsStm)
        dtgsModel=self.uNiqHash(dtgsModel)
        modelsDtgStm=self.uNiqHash(modelsDtgStm)

        cards=[]
        cards=cards+self.PrintHash(stmsDtg)
        cards=cards+self.PrintHash(allstmsDtg)
        cards=cards+self.PrintHash(dtgsStm)
        cards=cards+self.PrintHash(dtgsModel)
        cards=cards+self.PrintHash(modelsDtgStm)

        invpath="%s/inv.hfip.tcdiag.txt"%(webdir)
        rc=MF.WriteList2File(cards,invpath,1)

        MF.dTimer(tag='inv.tcdiag')


        

class TcTrkPlot(DataSet):


    def __init__(self,tG,stmid,zoomfact=None,verb=1,otau=48,override=0):

        doplot=1
        if(not(hasattr(tG,'ga'))): doplot=0

        self.year=tG.year
        self.dtg=tG.dtg
        self.model=tG.model
        self.pltdir=tG.pltdir

        self.stmid=stmid
        self.verb=verb
        self.aidtrk=tG.aidtrk
        self.aidtaus=tG.aidtaus
        self.zoomfact=zoomfact
        self.otau=otau

        self.pltfile="trkplt.%s.%s.png"%(self.stmid,self.model)
        self.pltpath="%s/%s"%(self.pltdir,self.pltfile)
        self.trkplotpath=self.pltpath
        self.trkploturl="../../../%s/%s/%s/%s"%(self.year,self.dtg,self.model,self.pltfile)
        
        if(doplot):
            self.ga=tG.ga
            self.ge=tG.ge
        else:
            return
            
        self.ge.pareaxl=0.50
        self.ge.pareaxr=9.75
        self.ge.pareayb=0.25
        self.ge.pareayt=8.25
        self.ge.setParea()


        if(not(override) and MF.ChkPath(self.trkplotpath)):
            print 'III trkplotpath: ',self.trkplotpath,' already there and override=0...'
            return

        self.curgxout=self.ga.getGxout()
        self.setInitialGA()

        # -- get TC info and best track
        #
        tD=TcData()
        self.bts=tD.getBtcs4Stmid(stmid,dtg=self.dtg)
        (self.stm3id,self.stmname)=tD.getStmName3id(stmid)

        self.PlotTrk()


    def setInitialGA(self):

        ga=self.ga
        ge=self.ge
        (alats,alons,refaid,reftau,reftrk)=GetOpsRefTrk(self.dtg,self.stmid,override=0,verb=0)

        self.alats=alats
        self.alons=alons
        self.refaid=refaid
        self.reftau=reftau
        self.reftrk=reftrk
        
        (lat1,lat2,lon1,lon2)=LatLonOpsPlotBounds(alats,alons,verb=verb)

        if(zoomfact != None):

            zoom=float(zoomfact)

            dlon=30.0/zoom
            dlat=20.0/zoom
            dint=2.5

            rlat=self.aidtrk[self.otau][0]
            rlon=self.aidtrk[self.otau][1]
            if(rlat == None):
                vdtg=mf.dtginc(self.dtg,self.otau)
                try:
                    bt=self.bts[vdtg]
                except:
                    bt=self.bts[self.dtg]
                rlat=bt[0]
                rlon=bt[1]

            lat1=rlat-dlat*0.65
            lat1=int(lat1/dint+1)*dint
            lat2=lat1+dlat

            lon1=rlon-dlon*0.35
            lon1=int(lon1/dint+1)*dint
            lon2=lon1+dlon


            print 'zzzzzzzzzzzzz ',rlat,rlon
            print 'ddddddddddddd ',lat1,lat2,lon1,lon2


        ge.lat1=lat1
        ge.lat2=lat2
        ge.lon1=lon1
        ge.lon2=lon2

        ge.mapdset='mres'
        #ge.xlint=xlint
        #ge.ylint=ylint
        ge.clear()
        ge.mapcol=0
        ge.setMap()
        ge.grid='off'
        ge.setGrid()
        ge.setLatLon()
        ge.setXylint()
        ge.setParea()
        ge.setPlotScale()
        

    def PlotTrk(self,doalltaus=1,otau=48,etau=120,dtau=12):
        
        ga=self.ga
        ge=self.ge

        self.etau=etau
        self.dtau=dtau
        self.otau=otau

        mktaus=[0,24,48,72,120]
        mkcols={0:1,24:1,48:1,72:2,120:2}

        ftlcol=modelTrkPlotProps[self.model][0]
        modeltitle=modelOname[self.model]
        
        (btau,etau,dtau)=(0,etau,dtau)
        itaus=range(btau,etau+1,dtau)

        taus=[]
        for itau in itaus:
            for ttau in self.aidtaus:
                if(itau == ttau):
                    taus.append(itau)
        

        pbt=ga.gp.plotTcBt
        pbt.set(self.bts,self.dtg,nhbak=72,nhfor=etau)
        
        bm=ga.gp.basemap2
        bm.draw()
        ge.setPlotScale()

        pbt.dline(times=pbt.otimesbak,lcol=7,lthk=10)
        pbt.dwxsym(times=pbt.otimesbak)
        pbt.legend(ge,times=pbt.otimesbak,ystart=7.9)

        pft=ga.gp.plotTcFt
        pft.set(self.aidtrk,lcol=ftlcol,doland=1)
        
        if(ftlcol == -2):
            pft.dline(lcol=15)
            try:     vmcol=pft.lineprop[otau][0]
            except:  None

            if(vmcol != 75):
                pft.dmark(times=[otau],mkcol=vmcol,mksiz=0.20)
                pft.dmark(times=[otau],mksiz=0.05)
            else:
                pft.dmark(times=[otau])
        else:
            pft.dline(times=taus,lsty=3)
            pft.dmark(times=taus,mksiz=0.050)
            for mktau in mktaus:
                if(mktau in taus):
                    pft.dmark(times=[mktau],mksiz=0.100)
                    pft.dmark(times=[mktau],mkcol=0,mksiz=0.070)
                    pft.dmark(times=[mktau],mkcol=mkcols[mktau],mksiz=0.040)

                    
    

        ttl=ga.gp.title
        ttl.set(scale=0.85)
        t1='%s TC: %s[%s] V`bmax`n: %3dkt bdtg: %s'%(modeltitle,self.stmid,self.stmname,int(self.bts[self.dtg][2]),self.dtg)
        t2='TCDiag track plot'
        ttl.top(t1,t2)

        ga('q pos')

        ge.pngmethod='gxyat'
        ge.makePng(self.pltpath,verb=1)



def getTausFromTauopt(tauopt):

    if(mf.find(tauopt,',')):
        tt=tauopt.split(',')
        taus=[]
        for t1 in tt:
            t1=int(t1)
            taus.append(t1)
    else:
        taus=[int(tauopt)]

    return(taus)
        


def cycleByDtgsModels(CL,dtgs,models,stmopt):

    # -- check for when doing a single
    if((len(dtgs) == 1 and len(models) == 1) or CL.doinventory):
        dtg=dtgs[0]
        model=models[0]
        return(dtg,model)

    if(CL.dohtmlvars): models=['gfs2']

    for dtg in dtgs:
        
        for model in models:

            cmd="%s %s %s"%(CL.pypath,dtg,model)
            for o,a in CL.opts:
                cmd="%s %s %s"%(cmd,o,a)
                        
            mf.runcmd(cmd,ropt)

    sys.exit()

    

def doAllPrc(CL,dohtml=0):
    
    cmd1="%s %s %s -P -W"%(CL.pypath,CL.dtgopt,CL.modelopt)
    for o,a in CL.opts:
        if(o != '-A' and o != '-N'and o != '-n'):
            cmd1="%s %s %s"%(cmd1,o,a)
    mf.runcmd(cmd1,CL.ropt)

    if(dohtml):
        cmd2="%s %s %s -H"%(CL.pypath,CL.dtgopt,CL.modelopt)
        mf.runcmd(cmd2,ropt)

    cmd2a="%s %s %s -D"%(CL.pypath,CL.dtgopt,CL.modelopt)
    mf.runcmd(cmd2a,ropt)

    cmd3="%s %s %s -I"%(CL.pypath,CL.dtgopt,CL.modelopt)
    for o,a in CL.opts:
        if(o != '-A' and o != '-N' and o != '-O'):
            cmd3="%s %s %s"%(cmd3,o,a)
    mf.runcmd(cmd3,CL.ropt)

    sys.exit()



class MyCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            2:['modelopt',    'model|model1,model2|all|allgen'],
            }

        self.defaults={
            'doupdate':0,
            'doga':1,
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'quiet':['q',0,1,' run GA in quiet mode'],
            'ropt':['N','','norun',' norun is norun'],
            'dowindow':['w',0,1,'1 - dowindow in GA.setGA()'],
            'dowebserver':['W',0,1,'1 - dowebserver=1 write to webserver for plotonly '],
            'doxv':['X',0,1,'1 - xv the plot'],
            'doplot':['P',0,1,'1 - make diag plots'],
            'doDiagPlotsOnly':['p',0,1,'0 - do NOT only do diag plots'],
            'dotarball':['T',0,1,'1 - tarball [and scp to wxmap2.sf.net]'],
            'domandonly':['m',0,1,'DO        reduced levels only (sfc,850,500,200)'],
            'doStndOnly':['s',1,0,'do NOT do SHIPS levels (1000,850,700,500,400,300,250,200,150,100)'],
            'stmopt':['S:',None,'a','stmopt'],
            'getpYp':['Y',0,1,'1 - get from pyp'],
            'doclean':['K',0,1,'clean off files < dtgopt'],
            'dohtmlALL':['H',0,1,'do all html for individual models'],
            'dohtmlvars':['h',0,1,'do htmlvars only'],
            'tauopt':['t:',None,'a','tauopt'],
            'doinventory':['I',0,1,'do html for individual models'],
            'dols':['l',0,1,'do ls of TCs...'],
            'ndayback':['n:',25,'i','ndays back to do inventory from current dtg...'],
            'doTrkPlot':['R',0,1,'doTrkPlot...'],
            'zoomfact':  ['Z:',None,'a','zoomfact'],
            'doALL':['A',0,1,'do all processing for a dtg'],
            'doDiagOnly':['D',0,1,'do only diagfile processing'],
            }

        self.purpose='''
purpose -- generate TC large-scale 'diag' file for lgem/ships/stips intensity models
 '''
        self.examples='''
%s 2010052500 gfs2
'''

#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# errors

def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='all')
MF.sTimer(tag='startup')

#argstr="pyfile 2010052500 gfs2 -P -S 04l"
#argv=argstr.split()

argv=sys.argv
CL=MyCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- switches from w2switches
#
if(not(w2.W2doTCdiag)):
    print 'SSSSSSSSSSSSSS W2doTCdiag=0...bail...'
    sys.exit()

if(doALL): doAllPrc(CL)

gaopt='-g 1024x768'

if(doclean): modelopt='gfs2'
(dtgs,models)=getDtgsModels(CL,dtgopt,modelopt)
(dtg,model)=cycleByDtgsModels(CL,dtgs,models,stmopt)


if(doinventory or dohtmlvars or dohtmlALL): dowebserver=1

if(doclean or dohtmlvars or dohtmlALL or doinventory or dols or getpYp): doga=0

tG=TcDiag(dtg,model,doplot=doplot,
          gaopt=gaopt,
          domandonly=domandonly,
          doStndOnly=doStndOnly,
          doDiagOnly=doDiagOnly,
          dols=dols,
          dowebserver=dowebserver,
          doDiagPlotsOnly=doDiagPlotsOnly,
          doga=doga,verb=verb)

#tG.ge.ls()
#tG.ls()
#sys.exit()

# -- bail if no data
#
if(tG.rcM2 == None):
    print 'WWW(w2.tc.flddiag.py): no data for dtg: ',dtg,' model: ',model
    sys.exit()

# -- tcs
#
tstmids=getStmids(dtg,tG.stmids,tG.adstm2ids,stmopt=stmopt)
if(doclean): tG.cleanDiagFiles(dtg,CL.ropt); sys.exit()

if(dols):
    tstmids=getStmids(dtg,tG.stmids,tG.adstm2ids,stmopt=None)
    print 'current all stmids:'
    tG.lsTC()
    print 'stmids from real-time/post tracker and tcdiag file: ',tstmids
    for tstmid in tstmids:
        rc=tG.setTCtracker(tstmid,quiet=1)
        siz=None
        if(hasattr(tG,'pyppathDataALL')): siz=MF.GetPathSiz(tG.pyppathDataALL)
        if(rc and  siz != None):
            print 'YYY DataALL for: ',tstmid," %-60s"%(tG.pyppathDataALL),' siz: %8d '%(siz),tstmid
        else:
            print 'NNN        for: ',tstmid,' DataAll not yet done...'

    sys.exit()

if(doinventory):
    tGi=TcdiagInv(tG,ndayback=ndayback)
    sys.exit()

if(dohtmlvars or dohtmlALL and dowebserver):
    
    for tstmid in tstmids:

        if(tG.setTCtracker(tstmid,quiet=1) == 0):
            print 'EEE in setTCtracker...'
            continue

        if(not(dohtmlvars)):
            tGd=tG.gettGdpyp()
            tGtrk=TcTrkPlot(tG,tstmid,zoomfact,override=override)
            tGh=TcDiagHtml(tGd,tGtrk)
            tGh.doHtml()

        tGhs=TcDiagHtmlVars(tG,verb=verb)
        tGhs.doHtml()

    sys.exit()

if(tG.rcM2 == None):
    print 'EEE  no data for model: ',model,' dtg: ',dtg
    sys.exit()


MF.dTimer(tag='startup')


# -- get sst for globe
if(not(getpYp) and not(doTrkPlot)):
    MF.sTimer(tag='sst')
    ssT=Oisst(tG.ga,tG.ge,dtg,verb=verb)
    MF.dTimer(tag='sst')


for stmid in tstmids:

    MF.sTimer(tag=stmid)

    print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW               working stmid: ',stmid,'  model: ',model,' dtg: ',dtg

    # -- get trackers -- if none available; bail...
    #
    rc=tG.setTCtracker(stmid)
    if(not(rc)): continue

    # -- initialize the output
    #
    tG.initOutput()

    # -- get pyps for data and html and regen the diag file and html
    #
    doAllOnly=1
    if(dowebserver): doAllOnly=0
    

    if(getpYp):

        # -- just the full diag file
        if(doAllOnly):
            tGd=tG.gettGdAllpyp()
            tGd.aidname=tG.aidname
            tGd.webdir=tG.webdir
            tGd.diagpathWebALL=tG.diagpathWebALL
            tGd.makeDiagFile()
            tGtrk=TcTrkPlot(tG,stmid,zoomfact,override=override)

            if(webserver):
                tGh=TcDiagHtml(tGd,tGtrk)
                tGh.doHtml()


        # -- reduced/plot diag file + html
        else:
            tGd=tG.gettGdpyp()
            tGh=tG.gettGhpyp()
            tGd.makeDiagFile()
            tGtrk=TcTrkPlot(tG,stmid,zoomfact,override=override)
            
            if(webserver):
                tGh=TcDiagHtml(tGd,tGtrk)
                if(tGh.rctG == 0): sys.exit()
                if(not(tGh.doHtml())):  tGh.doPyp()
            
        continue

    
    # -- set the taus
    #
    taus=tG.aidtaus
    if(tauopt != None): taus=getTausFromTauopt(tauopt)
    tG.taus=taus


    # -- get status of data/plots
    #
    tG.getDataStatus(override)

    if(len(tG.tausFinal) > 0):
        taus=tG.tausFinal
        tG.stmTaus=[]
    else:
        # -- taus already done, just make the diagfile and the html
        #
        if(doDiagOnly): continue

        if(tG.tGdprev != None):
            tGd=tG.tGdprev
        if(not(hasattr(tGd,'trkploturl'))):
            tGtrk=TcTrkPlot(tG,stmid,zoomfact)
            tG.trkploturl=tGtrk.trkploturl
            tGd.trkploturl=tGtrk.trkploturl

        if(dowebserver):
            # -- set here rather than using default in M.MFhtml
            tGd.webdir=tG.webdir
            tGh=TcDiagHtml(tGd,tGtrk)
            tGh.doHtml()
            tGh.doPyp()

        MF.dTimer(tag=stmid)

        continue

        
    # -- do trk plot
    #
    if(doTrkPlot):
        tGtrk=TcTrkPlot(tG,stmid,zoomfact,override=doTrkPlot)
        continue


    # -- loop through taus
    #
    for tau in taus:

        MF.sTimer(tag='storm: %03d'%(tau))
        rc=tG.setLatLonTimeByTau(dtg,model,stmid,tau)
        if(rc == 0): continue
        if(rc == -1): break

        dosfc=1
        if(dosfc):
            tG.getPrecip()
            tG.getVort850(dohl=1)
            tG.getDiv200()
            tG.getTang850(dohl=1)
            tG.getShear()
            tG.getSst(dohl=0)
            tG.getPmin()
            tG.getPrw()
            tG.getVmaxRmax4Tcxy2rt(dohl=0)
            tG.getHartCps()
            MF.dTimer(tag='storm: %03d'%(tau))

        dosndng=1
        if(dosndng):
            MF.sTimer(tag='sounding: %03d'%(tau))
            tG.getSoundingData()
            MF.dTimer(tag='sounding: %03d'%(tau))


    if(not(doDiagPlotsOnly)):
        tGd=TcDiagData(tG,verb=verb)
        tGd.makeDiagFile()
        tGd.doPyp()

    if(not(doDiagOnly)):
        tGtrk=TcTrkPlot(tG,stmid,zoomfact,override=override)

        if(dowebserver):
            tGh=TcDiagHtml(tG,tGtrk)
            tGh.doHtml()
            tGh.doPyp()
            tGhs=TcDiagHtmlVars(tG,verb=verb)
            tGhs.doHtml()
    
        
    MF.dTimer(tag=stmid)


MF.dTimer(tag='all')
if(dotarball):
    tG.tarball2Wxmap2(dtg)
    


