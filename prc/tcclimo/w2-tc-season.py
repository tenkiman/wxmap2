#!/usr/bin/env python

"""%s

purpose:

  process TCs by seaon/basin

usages:

  %s yearopt basinopt -p prcopt

      yearopt  : cur | Y | YY | YYYY[.YYYY] for single year of range of years
      basinopt : cur | B[.B.B.B] B=L.E.W.C.A.B.I.S.P.T | NHS(n) | SHS(s)
      
  -p  prcopt   : ops.all | ops.veri.data | ops.veri.anal | era40.tracks | ops.track |
               : ops.veri.anal.all |
               : ops.climo |
               : ops.climo.all -- do all climo processing including rsync
               
               : ops.web | ops.web.html  (generate .js and .html for www/tc/sitrep web)
               : ops.web.dev -- dev set in html section below |
               
               : ops.webupload (put web to tenkimap.com) | ops.bt (names, bt, adecks) |
               : ops.webrsync -- rsync to some outside server  

               : ops.adecks (gen wxmap adecks from jt/nhc adecks) |
               : ops.fc.refresh (cp fc tracks)
               
               : ls (list)  

  -C           : do current year only in climo
  -B           : forced run of w2.tc.bt.climo.pl; default is to NOT run

examples:

%s  2004 -p ls
%s  1958.2001 -p py                create TCstats.py -- YYYY.SSS dict of storm stats
%s  2004  SHS -p ops.track
%s  2004  SHS -p ops.veri.anal -r jtwc.mod
"""

from WxMAP2 import *
w2=W2()

import TChtml
from tcbase import *


#
#  defaults
#

dobtclimo=None
curyearonly=None
yearopt=None
basinopt=None
prcopt='ls'
doexternalrsync=0
override=0

ropt=''

verb=0

curdtg=mf.dtg()
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

#
# veriname is always arg #1
#

#
# options using getopt
#

if(narg >= 2):

    yearopt=sys.argv[1]
    basinopt=sys.argv[2]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[3:], "p:v:NCBO")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-p",""): prcopt=a
        if o in ("-v",""): viopt=a
        if o in ("-N",""): ropt='norun'
        if o in ("-C",""): curyearonly=1
        if o in ("-B",""): dobtclimo=1
        if o in ("-O",""): override=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)



#
# set number of nyears back to go for climo
#

NyearsClimo=YearsBackClimo
NyearsClimoTss=YearsBackClimoTss

if(yearopt == 'cur'):
    yearopt=curyear

elif(len(yearopt) <= 2):
    yearopt=add2000(yearopt)


if(basinopt == 'cur'):

    curyy=int(curdtg[0:4])
    curmo=int(curdtg[4:6])
    curda=int(curdtg[6:8])
    basinopt='SHS'
    dtgNHMseason="%d050500"%(curyy)  # 20160104 - change to nhem season > 050500
    dtgSHMseason="%d010500"%(curyy)  # -- 20170105 - change to shem season
    cdtgdiffSHM=mf.dtgdiff(dtgSHMseason,curdtg)
    cdtgdiffNHM=mf.dtgdiff(dtgNHMseason,curdtg)
    if(cdtgdiffNHM > 0): basinopt='NHS'

elif(basinopt == 'cur.shem'):
    (shemoverlap,cy,cyp1)=CurShemOverlap(curdtg)
    basinopt='SHS'
    if(shemoverlap): yearopt=cyp1

elif(basinopt == 'cur.nhem'):
    basinopt='NHS'
    yearopt=curyear


if(not(prcopt) or not(yearopt)):
    print "EEE must set yearopt -p prcopt"
    sys.exit()
    
if( (prcopt == 'ops.veri.data'
     or prcopt == 'ops.veri.anal'
     or prcopt == 'ops.veri.plot'
     or prcopt == 'ops.track' )
   and not(basinopt)):
    print "EEE for -p %s you must set basin -b NHS | SHS (?hemi superbasin)"%(prcopt)
    sys.exit()

if(not(basinopt)):
    print "EEE set basin -b n|NHS or s|SHS"
    sys.exit()



if(basinopt == 'n'): basinopt='NHS'
if(basinopt == 's'): basinopt='SHS'
if(basinopt == 'g'): basinopt='GLB'
basinopt=basinopt.upper()

#
# lists
#

verirulesanal=['jtwc','jtwc.mod','nhc.wind','nhc.pure']
verirulesplot=['jtwc','nhc.pure']
statcomps=['fe','pod','impclp','vmax']

#
# -- 20071031 -- do both ace and stcd
# -- 20131021 -- do stcd, aced and hurricane aced
# -- 20200814 -- change order so that tcace is first
#
tcexprs=['tcace','huace','tcstr']

modelcomps=[
	'ofc.clp','ofc.avn','ofc.ngp','ofc.ukm','ofc.eco',
        'ofc.con','ofc.fv4','ofc.fv5',
	'avn.ngp','avn.eco','avn.ukm','avn.con','avn.fv4',
	'fv4.avn','fv4.ngp','fv4.eco','fv4.ukm','fv4.con',
	'fv4.fv5',
        'fv5.avn','fv5.ngp','fv5.eco','fv5.ukm','fv5.con',
	'ece.eco','ukm.eco','ngp.eco',
        'con.eco','con.ukm',
	]

modelcompsmissedfv5=[
        'fv5.ukm','fv5.con',
	]

unitcomps=['','-M']
if(basinopt == 'NHS' or basinopt == 'SHS'):
    basincomps=Hemi3toSuperBasins[basinopt]
    #basincomps=['NHS','W']
homorules=[None]+modelcomps

pycards=[]
rptopt=0
if(prcopt == 'ls'): rptopt=1

tt=yearopt.split('.')

if(len(tt) > 1):
    yyyy1=int(tt[0])
    yyyy2=int(tt[1])
    years=range(yyyy1,yyyy2+1,1)

else:
    if(yearopt == 'cur'):
        years=[curdtg[0:4]]
    else:
        years=[yearopt]

for year in years:

    year=str(year)

    tcnames=GetTCnamesHash(year)
    tcstats=GetTCstatsHash(year)

    (tcs,tcstats,allhtml,alljs,obstmid)=TCsByBasin(year,basinopt,
                                                      pycards,rptopt,tchash=tcnames)

    yearm1=int(year)-1
    yearp1=int(year)+1
    
    if(basinopt == 'SHS'):
        lhemi='shem'
        yearmb=int(year)-NyearsClimo

        byyyymmtss=[]
        eyyyymmtss=[]
        for ny in NyearsClimoTss:
            yearmbts=int(year)-ny
            byyyymmts="%s07"%(yearmbts)
            eyyyymmts="%s07"%(year)
            byyyymmtss.append(byyyymmts)
            eyyyymmtss.append(eyyyymmts)
            
        verifile="ops.%s.%s"%(year,lhemi)
        bdtg="%s070100"%(yearm1)
        edtg="%s070100"%(year)
        edtgseason=edtg
        opstdir="%s.%s"%(year,lhemi)
        hemi='SHEM'
        
    elif(basinopt == 'NHS'):
        
        lhemi='nhem'
        yearmb=int(yearp1)-NyearsClimo
        
        byyyymmtss=[]
        eyyyymmtss=[]
        for ny in NyearsClimoTss:
            yearmbts=int(year)-ny
            byyyymmts="%s01"%(yearmbts)
            eyyyymmts="%s01"%(yearp1)
            byyyymmtss.append(byyyymmts)
            eyyyymmtss.append(eyyyymmts)
            

        verifile="ops.%s.%s"%(year,lhemi)
        bdtg="%s010100"%(year)
        edtg="%s010100"%(yearp1)
        edtgseason=edtg
        opstdir="%s.%s"%(year,lhemi)
        hemi='NHEM'
        
    elif(prcopt == 'ls'):
        continue
    else:
        print "EEE for -p %s ; must specify basinopt -b NHS | SHS"%(prcopt)
        sys.exit()

    byyyymm=bdtg[0:6]
    eyyyymm=edtg[0:6]
    emmdd=edtg[4:8]
    cemmdd=curdtg[4:8]

    #
    # check if where real-time
    #
    if(int(edtg) > int(curdtg)):
        edtg='cur'
        eyyyymm=curdtg[0:6]
        emmdd=curdtg[4:8]


    TChtml.SetTCHtmlDirsVars(year,hemi,curyear,emmdd,cemmdd,
                             byyyymmtss,eyyyymmtss)

    #aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    #
    #  ops -- whole nine yards
    #
    #aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        
    if(prcopt == 'ops.all' or prcopt == 'ops.veri.anal.all'):


        os.chdir(BaseDirPrcTc)
        opsveriopts=['bt','adecks','climo','veri.data','veri.anal','veri.plot','track','web','webupload']
        ###
        ### 20050412 - turn off webupload, tenkimap root still getting blown away...
        ###
        ##opsveriopts=['bt','climo','veri.data','veri.anal','veri.plot','track','web']

        if(prcopt == 'ops.veri.anal.all'):
            opsveriopts=['veri.anal','veri.plot','track','web','webupload']

        
        for opsveriopt in opsveriopts:
            if(curyearonly and opsveriopt == 'climo'): curyearonlyopt='-C'
            cmd="%s %s %s -p ops.%s %s"%\
                 (pyfile,year,basinopt,opsveriopt,curyearonlyopt)
            mf.runcmd(cmd,ropt)


    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    #  ops bt -- do names, bt mo and adecks
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.adecks'):
        
        os.chdir(BaseDirPrcTcDat)

        #
        # adecks for ofc
        #
        cmd="w2.tc.adeck.2.wxmap.adeck.py  %s -i JTWC -o ofc -s jtwc"%(year)
        mf.runcmd(cmd,ropt)
        cmd="w2.tc.adeck.2.wxmap.adeck.py  %s -i OFCL -o ofc -s nhc"%(year)
        mf.runcmd(cmd,ropt)

        #
        # adecks for con
        #
        cmd="w2.tc.adeck.2.wxmap.adeck.py  %s -i CONW -o con -s jtwc"%(year)
        mf.runcmd(cmd,ropt)
        cmd="w2.tc.adeck.2.wxmap.adeck.py  %s -i CONU -o con -s nhc"%(year)
        mf.runcmd(cmd,ropt)

        #
        # adecks for ofc06 -- ofi -- jtwi
        #
        cmd="w2.tc.adeck.2.wxmap.adeck.py  %s -i JTWI -o ofi -s jtwc"%(year)
        mf.runcmd(cmd,ropt)

        #
        # adecks for ofc06 -- ofi -- jtwi
        #
        cmd="w2.tc.adeck.2.wxmap.adeck.py %s -i OFCI -o ofi -s nhc"%(year)
        mf.runcmd(cmd,ropt)

        #
        # adecks for ofc06 -- ofi -- jtwi
        #
        cmd="w2.tc.adeck.2.wxmap.adeck.py %s -i EGRR -o egr -s jtwc"%(year)
        mf.runcmd(cmd,ropt)

    elif(prcopt == 'ops.bt'):
        
        #
        # names
        #
        os.chdir(BaseDirPrcTcDat)
        cmd="w2-tc-names.py %s"%(year)
        mf.runcmd(cmd,ropt)

        cmd=" w2-tc-bt-bdeck-final.py %s"%(year)
        mf.runcmd(cmd,ropt)

        cmd=" w2-tc-bt-adeck-final.py %s"%(year)
        mf.runcmd(cmd,ropt)



    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    #  ops.fc.refresh -- cp all the fc in the current ops (w1) dir to w2 
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.fc.refresh'):

        sdir=FcCurDir
        tdir=FcOpsDir
        mask="tc.???.%s*.txt"%(year)
        mf.cpfiles(sdir,tdir,mask,ropt)


    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    #  ops climo
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.climo.all'):

        
        MF.sTimer(tag=prcopt)

        overOpt=''
        if(override): overOpt='-O'
        cmd1="%s %s %s -p ops.climo %s"%(pyfile,yearopt,basinopt,overOpt)
        mf.runcmd(cmd1,ropt)

        #
        # cp files; make html 
        #
        if(ropt == ''):
            TChtml.HtmlTCPlotFiles(dtypeopt='climo')
            TChtml.HtmlTCCssJs()
            TChtml.HtmlTCActSpec(NyearsClimo)
            TChtml.HtmlTCActMaps()
            TChtml.HtmlTCActTS()

        if(doexternalrsync):
            cmd2="%s %s %s -p ops.webrsync"%(pyfile,yearopt,basinopt)
            mf.runcmd(cmd2,ropt)

        # -- 20200317 -- now rsync to wxmap2
        #
        if(ropt == ''):
            rc=rsync2Wxmap2('tcact',ropt)


        MF.dTimer(tag=prcopt)
        sys.exit()

    elif(prcopt == 'ops.climo.webonly'):

        #
        # cp files; make html 
        #
        if(ropt == ''):
            #TChtml.HtmlTCPlotFiles(dtypeopt='climo')
            TChtml.HtmlTCCssJs()
            TChtml.HtmlTCActSpec(NyearsClimo)
            TChtml.HtmlTCActMaps()
            TChtml.HtmlTCActTS()

        sys.exit()

    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    #  ops climo
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.climo'):

        pltdir=w2.PltTcOpsClimoDir+"/%s"%(opstdir)
        mf.ChkDir(pltdir,'mk')

        climobasins=ClimoBasinsHemi[basinopt]

       
        NyearsClimom1=NyearsClimo-1
        yearmb=int(year)-NyearsClimom1
        yearp1=int(year)+1

        if(basinopt == 'NHS'):
            if(curyearonly):
                llyears=range(int(year),int(year)+1)
                llyearsall=range(int(year)-NyearsClimom1,int(year)+1)
                llyearsall=llyears
            else:
                llyears=range(int(year)-NyearsClimom1,int(year)+1)
                llyearsall=llyears
        elif(basinopt == 'SHS'):
            if(curyearonly):
                llyears=range(int(year)-1,int(year))
                llyearsall=range(int(year)-NyearsClimo,int(year))
                llyearsall=llyears
            else:
                llyears=range(int(year)-NyearsClimo,int(year))
                llyearsall=llyears
                
        bmm=bdtg[4:6]
        if(edtg == 'cur'):
            emm=edtgseason[4:6]
        else:
            emm=edtg[4:6]
            
        eyyyymmclimo=eyyyymm
        if(edtg == 'cur'): eyyyymmclimo=edtg


        #
        # only do if edtg=cur or forced using -B
        #

        #BBBBBBBBBBBBBBBBBBBBTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT -- depends on BT.*

        os.chdir(w2.PrcDirTcclimoW2)

        # -- 20200302 -- deprecate -- no use make.tc.bt.climo.ll.py .gs
        #
        if(edtg == 'cur' or dobtclimo):
            cmd="w2.tc.bt.mo.climo.pl %s %s"%(byyyymm,eyyyymm)
            mf.runcmd(cmd,ropt)
        
        for llyear in llyears:

            bllyear=llyear
            ellyear=llyear+1
            
            
            bdtgact="%d%s0100"%(bllyear,bmm)
            edtgactplot="%d%s"%(ellyear,edtgseason[4:])

            if(edtg == 'cur' and llyear == int(year)):
                edtgact=curdtg
            else:
                edtgact="%d%s"%(ellyear,edtgseason[4:])
                
            #BBBBBBBBBBBBBBBBBBBBTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT -- depends on BT.*
            ngtrpropt=ropt
            dongtrp=1
            if(not(dongtrp)): ngtrpropt='norun'
            ngtrpdir="%s/ngtrp"%(w2.ptmpBaseDir)
            mf.ChkDir(ngtrpdir,'mk')
            ngtrppath="%s/ngtrp.tcactivity.%s.%s.txt"%(ngtrpdir,bdtgact,edtgact)
            btest=(basinopt == 'SHS' and (int(llyear)+1) == int(curyear))
            #-- 20201003 -- redid the yearly ngtrp after redoing bt.local
            #from 1950-2019 btest=1 print
            #'nnnn',ngtrppath,llyear,curyear,basinopt,btest sys.exit()
            if(not(os.path.exists(ngtrppath)) or
               llyear  == curyear or
               btest or override
               ):
                # -- 202210013 -- big flail getting correct id of lant storms
                # 02L -> 04E and nhc has warnings on both
                # 13E is one of many cases where a non-TC has a warning therefore it's a TC except in the IO and SHEM
                #
                cmd="w2-tc-posit.py %s.%s -n %s -T -S mdeck"%(bdtgact,edtgact,ngtrppath)
                mf.runcmd(cmd,ngtrpropt)

            
            #
            # kill off previous plots
            #
            cmd="rm %s/tc.act.spec.%s.*"%(pltdir,bdtgact)
            mf.runcmd(cmd,ropt)

            cmd="g.tc.activity.pl %s %s %s %s"%(bdtgact,edtgactplot,ngtrppath,pltdir)
            mf.runcmd(cmd,ropt)

        # -- make the lat-lon plots
        #
        # -- blow off the current btclimo data....
        #
        btcurrentDir="%s/climo/current"%(w2.TcDatDir)
        cmd="rm %s/*"%(btcurrentDir)
        mf.runcmd(cmd,ropt)
        
        # -- cycle by basins/years
        #
        for climobasin in climobasins:

            for llyear in llyearsall:
                
                bllyear=llyear
                ellyear=llyear+1
                
                #
                # mf 20050718 -- fix current nhem
                #
                if(basinopt == 'NHS' and (edtg == 'cur') ):
                    ellyear=bllyear
                
                byyyymm="%d%s"%(bllyear,bmm)

                if(edtg == 'cur' and llyear == int(year)):
                    eyyyymmclimo=edtg
                else:
                    eyyyymmclimo="%d%s"%(ellyear,emm)

                bdtgll="%d%s0100"%(bllyear,bmm)
                if(edtg == 'cur'):
                    # mf 2006120 -- logic for cur year and shem...
                    if((basinopt == 'SHS' and (int(curyear) < int(year)))):
                        edtgll="%d%s"%(bllyear,curdtg[4:])
                    elif(llyear == int(year)):
                        edtgll=curdtg
                    else:
                        edtgll="%d%s"%(ellyear,curdtg[4:])
                else:
                    edtgll="%d%s"%(ellyear,edtgseason[4:])


                cmd="rm %s/tc.act.llmap.%s.%s*"%(pltdir,climobasin,bdtgll[0:8])
                mf.runcmd(cmd,ropt)

                flagrl=''
                if(edtgll == curdtg): flagrl='-R'

                for tcexpr in tcexprs:
                    cmd="g.tc.bt.climo.ll.py -y %s.%s -b %s -d %s %s -p %s"%(bdtgll,edtgll,climobasin,pltdir,flagrl,tcexpr)
                    mf.runcmd(cmd,ropt)

            cmd="rm %s/tc.act.mots.%s.*%s*"%(pltdir,climobasin,eyyyymmts)
            mf.runcmd(cmd,ropt)

            for n in range(0,len(byyyymmtss)):

                byyyymmts=byyyymmtss[n]
                eyyyymmts=eyyyymmtss[n]
                for tcexpr in tcexprs:
                    cmd="g.tc.bt.timeseries.mo.py -y %s.%s -b %s -d %s -p %s"%(byyyymmts,eyyyymmts,climobasin,pltdir,tcexpr)
                    mf.runcmd(cmd,ropt)
        
    elif(prcopt == 'ops.climo.tsonly'):

        MF.ChangeDir(w2.PrcDirTcclimoW2)

        pltdir=w2.PltTcOpsClimoDir+"/%s"%(opstdir)
        mf.ChkDir(pltdir,'mk')

        climobasins=ClimoBasinsHemi[basinopt]

        NyearsClimom1=NyearsClimo-1
        yearmb=int(year)-NyearsClimom1
        yearp1=int(year)+1

        if(basinopt == 'NHS'):
            if(curyearonly):
                llyears=range(int(year),int(year)+1)
                llyearsall=range(int(year)-NyearsClimom1,int(year)+1)
                llyearsall=llyears
            else:
                llyears=range(int(year)-NyearsClimom1,int(year)+1)
                llyearsall=llyears
        elif(basinopt == 'SHS'):
            if(curyearonly):
                llyears=range(int(year)-1,int(year))
                llyearsall=range(int(year)-NyearsClimo,int(year))
                llyearsall=llyears
            else:
                llyears=range(int(year)-NyearsClimo,int(year))
                llyearsall=llyears
                
        bmm=bdtg[4:6]
        if(edtg == 'cur'):
            emm=edtgseason[4:6]
        else:
            emm=edtg[4:6]
            
        eyyyymmclimo=eyyyymm
        if(edtg == 'cur'): eyyyymmclimo=edtg


        for climobasin in climobasins:

            for llyear in llyearsall:
                
                bllyear=llyear
                ellyear=llyear+1
                
                #
                # mf 20050718 -- fix current nhem
                #
                if(basinopt == 'NHS' and (edtg == 'cur') ):
                    ellyear=bllyear
                
                byyyymm="%d%s"%(bllyear,bmm)

                if(edtg == 'cur' and llyear == int(year)):
                    eyyyymmclimo=edtg
                else:
                    eyyyymmclimo="%d%s"%(ellyear,emm)

                bdtgll="%d%s0100"%(bllyear,bmm)
                if(edtg == 'cur'):
                    # mf 2006120 -- logic for cur year and shem...
                    if((basinopt == 'SHS' and (int(curyear) < int(year)))):
                        edtgll="%d%s"%(bllyear,curdtg[4:])
                    elif(llyear == int(year)):
                        edtgll=curdtg
                    else:
                        edtgll="%d%s"%(ellyear,curdtg[4:])
                else:
                    edtgll="%d%s"%(ellyear,edtgseason[4:])


                flagrl=''
                if(edtgll == curdtg): flagrl='-R'

            cmd="rm %s/tc.act.mots.%s.*%s*"%(pltdir,climobasin,eyyyymmts)
            mf.runcmd(cmd,ropt)

            for n in range(0,len(byyyymmtss)):

                byyyymmts=byyyymmtss[n]
                eyyyymmts=eyyyymmtss[n]
                for tcexpr in tcexprs:
                    cmd="g.tc.bt.timeseries.mo.py -y %s.%s -b %s -d %s -p %s"%(byyyymmts,eyyyymmts,climobasin,pltdir,tcexpr)
                    mf.runcmd(cmd,ropt)
        
        
        if(ropt == ''):
            TChtml.HtmlTCPlotFiles(dtypeopt='climo')
                                

    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    #  vdecks:  verification data
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.veri.data'):
        

        dobtmo=0
        if(dobtmo):
            os.chdir(BaseDirPrcTcDat)
            #BBBBBBBBBBBBBBBBBBBBTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT -- depends on BT.*
            btmoapp='w2.tc.bt.mo.final.py'
            cmd="%s %s %s"%(btmoapp,byyyymm,eyyyymm)
            mf.runcmd(cmd,ropt)
        
        os.chdir(BaseDirPrcTcVeri)
        veriapp='w2.tc.veri.data.all.py'
        cmd="%s %s -d %s.%s -m ops -p ops -b %s"%(veriapp,verifile,bdtg,edtg,basinopt)
        mf.runcmd(cmd,ropt)
        
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    #  veri anal
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.veri.anal'):
        
        os.chdir(BaseDirPrcTcVeri)
        veriapp='w2.tc.veri.anal.py'
        verifile=None
        verifile="ops.%s.%s"%(year,lhemi)
        verifile="ops.%s.%s"%(year,lhemi)
        filtopt=''
        if(basinopt == 'NHS'): filtopt='-F'

        if(not(verifile)): print "EEE invalid basinopt of -p ops.veri.anal: %s must be S|N"%(basinopt) ; sys.exit()

        poptopt='-popt.0.0.0.0.ropt.1.1.1.1'
        for verirule in verirulesanal:
            for homorule in homorules:
                homoopt=''
                if(homorule): homoopt="-h %s"%(homorule)
                cmd="%s %s -r %s %s %s %s"%(veriapp,verifile,verirule,homoopt,poptopt,filtopt)
                mf.runcmd(cmd,ropt)

    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    # stat plotting
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.veri.plot'):
        
        os.chdir(BaseDirPrcTcVeri)
        veriapp='w2.tc.g.veri.stat.py'
        
        verifile="ops.%s.%s"%(year,lhemi)
        pltdir="%s/%s.%s"%(PltOpsVeriDir,year,lhemi)
        mf.ChkDir(pltdir,'mk')

        #
        # kill off previous plots
        #
        ls=glob.glob("%s/tc.veri.*"%(pltdir))
        for l in ls:
            cmd="rm %s"%(l)
            mf.runcmd(cmd,ropt)

        
        if(not(verifile)): print "EEE invalid basinopt of -p ops.veri.anal: %s must be S|N"%(basinopt) ; sys.exit()
        
        for vericomp in verirulesplot:

            for basincomp in basincomps:

                for modelcomp in modelcomps:

                    homos=['',modelcomp]
                    for homo in homos:
                        homocomp=''
                        if(homo != ''): homocomp="-h %s"%(homo)

                        for unitcomp in unitcomps:

                            for statcomp in statcomps:

                                cmd="%s %s -m %s -r %s %s %s -p %s -b %s -P"%\
                                     (veriapp,verifile,
                                      modelcomp,vericomp,homocomp,
                                      unitcomp,statcomp,basincomp)
                                mf.runcmd(cmd,ropt)

    #
    # track plotting
    #

    elif(prcopt == 'era40.tracks'):

        gsopt='era40'
        gsopt='era40.batch'

        modelopts=['e40','clp']
        if(int(year) >= 1995):
            modelopts=['e40','clp','ifs']
        if(int(year) >= 1998):
            modelopts=['e40','clp','ifs','ngp']

        for tc in tcs:

            tctype=tcstats[tc][0]
            tcname=tcstats[tc][1]
            for modelopt in modelopts:
                cmd="g.tc.pl %s era40.%s %s %s %s name.%s.%s"%(year,year,tc,modelopt,gsopt,tctype,tcname)
                mf.runcmd(cmd,ropt)
                
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    # ops track plotting
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.track'):


        #
        # kill off previous plots
        #
        pltdir="%s/%s.%s"%(PltOpsTrackDir,year,lhemi)
        mf.ChkDir(pltdir,'mk')

        ls=glob.glob("%s/tc.trk.*"%(pltdir))
        for l in ls:
            cmd="rm %s"%(l)
            mf.runcmd(cmd,ropt)


        modelopts=['ofc','avn','clp','ngp','ukm','eco','ece','btk','fv4','fv5']

        for tc in tcs:

            tctype=tcstats[tc][0]
            tcname=tcstats[tc][1]
            tcbasin=tc[2]
            tchemi=Basin1toHemi3[tcbasin]
            print tchemi,tcbasin
            tcverihemi=Hemi1toHemiVeriName[tchemi]
            print 'qqq ',tc,tcbasin,tchemi,tcverihemi

            for modelopt in modelopts:
                cmd="g.tc.py ops.%s.%s -s %s.%s -m %s -P"%(year,tcverihemi,tc,year,modelopt)
                mf.runcmd(cmd,ropt)



        
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    # ops sitrep web -- create
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.web' or prcopt == 'ops.web.html' or prcopt == 'ops.web.dev' ):

        basinopt=basinopt.upper()

        curyear=curdtg[0:4]


        if(prcopt == 'ops.web.dev'):

            TChtml.HtmlTCCssJs()
            TChtml.HtmlTCActSpec()
            TChtml.HtmlTCActMaps()
            TChtml.HtmlTCActTS()

            sys.exit()
            

        if(ropt == 'norun'):
            print 'ops.web: ',year,curyear,hemi,lhemi,emmdd
            sys.exit()

        docp=1

        #
        # option to only cp vice cp + rm
        #
        docponly=1
        docponly=0
        
        if(docponly): docp=0
        
        dohtml=1

        if(prcopt == 'ops.web.html'): docp=0

        
        if(docp):
            TChtml.HtmlTCPlotFiles(dtypeopt='climo')
            
        elif(docponly):
            #
            # mf 20050816 only do climo
            #TChtml.HtmlTCPlotFiles(doclean=0,dtypeopt='climo')
            # all
            TChtml.HtmlTCPlotFiles(dtypeopt='climo',doclean=0)
        


        if(dohtml):
            
            TChtml.HtmlTCCssJs()

            TChtml.HtmlTCActSpec()
            TChtml.HtmlTCActMaps()
            TChtml.HtmlTCActTS()

            #TChtml.HtmlTCTrk()
            #TChtml.HtmlTCVeriStats()
            #TChtml.HtmlKeyVeri()
            #TChtml.HtmlKeyTrack()

    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    # ops sitrep web -- clean and upload
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ops.webupload'):

        server='ftp.tenkimap.com'
        user='tenkimap.com'
        passwd='tcad9494'
        sbdir=BaseDirWWWTcSitrep
        tdir='Documents/tc/sitrep'

        lbdir="%s/%s.%s"%(sbdir,year,lhemi)
        rbdir="tc/sitrep/%s.%s"%(year,lhemi)
        ftpdirs=['.','plt/climo','plt/track','plt/veri','rpt','css','js']
        ftpmask="*"

        ftpmkdirs=['plt','plt/climo','plt/track','plt/veri','rpt','css','js']

        # 111111111111111111111
        #
        # try mkdir the ftp server web tree, this prevents errors on the mdel
        # from blowing away root
        #

    elif(prcopt == 'ops.webrsync' and doexternalrsync):

        #
        # sync to both skate and dogfish
        #
        
        sbdir=BaseDirWWWTcSitrep

        mf.ChangeDir(sbdir)

        server=w2.NhcHttpIntranetServerSkate
        tdir=w2.NhcHttpIntranetDocRootSkate
        tdir="%s/wxmap2/web/tc/sitrep"%(tdir)

        rsyncopt='-alv --delete --timeout=600'
        cmd="rsync -e ssh %s %s/. %s:%s"%(rsyncopt,sbdir,server,tdir)
        mf.runcmd(cmd,ropt)

        if(w2.DoDogfishRsync):
            server=w2.NhcHttpIntranetServerDogfish
            tdir=w2.NhcHttpIntranetDocRootDogfish
            tdir="%s/wxmap2/web/tc/sitrep"%(tdir)
            
            rsyncopt='-alv --delete --timeout=600'
            cmd="rsync -e ssh %s %s/. %s:%s"%(rsyncopt,sbdir,server,tdir)
            mf.runcmd(cmd,ropt)

        sys.exit()


        ftpdirs=['.','plt/climo','plt/track','plt/veri','rpt','css','js']
        ftpmask="*"

        ftpmkdirs=['plt','plt/climo','plt/track','plt/veri','rpt','css','js']

       # 111111111111111111111
        #
        # try mkdir the ftp server web tree, this prevents errors on the mdel
        # from blowing away root
        #

        mf.doFTPsimple(server,lbdir,rbdir,ftpmask,'ftp.mkdir')

        for ftpdir in ftpdirs:
            rdir="%s/%s"%(rbdir,ftpdir)
            ldir="%s/%s"%(lbdir,ftpdir)
            mf.doFTPsimple(server,ldir,rdir,ftpmask,'ftp.mkdir')


        # 222222222222222222222
        #
        # now clean off the tenkimap web
        #
        
        for ftpdir in ftpdirs:

            #
            # 20050314 - don't wipe out root!!!
            #
            
            if(ftpdir == '.'):
                ftpopt='ftp.ls'
            else:
                ftpopt='ftp.rm'
            
            if(ropt == 'norun'):
                ftpopt='ftp.noload'

            rdir="%s/%s"%(rbdir,ftpdir)
            ldir="%s/%s"%(lbdir,ftpdir)

            print 'RRRRRR   rdir: ',rdir
            print 'LLLLLL   ldir: ',ldir
            print 'FFFFFF ftpopt: ',ftpopt
    
            mf.doFTPsimple(server,ldir,rdir,ftpmask,ftpopt)


        # 3333333333333333333333
        #
        #  now upload using wput
        #
        
        os.chdir(sbdir)

        print os.getcwd()
        #
        # mf 20050718 -- new timestamp option
        #
        cmd="wput -N -u -nv %s.%s/ ftp://%s:%s@%s/%s/"%(year,lhemi,user,passwd,server,tdir)
        mf.runcmd(cmd,ropt)

        #
        # mf 20050725 -- force upload of *.htm
        #
        cmd="wput -u -v %s.%s/*.htm ftp://%s:%s@%s/%s/%s.%s/"%(year,lhemi,user,passwd,server,tdir,year,lhemi)
        mf.runcmd(cmd,ropt)

    


    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    #
    # just ls
    #
    #ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    elif(prcopt == 'ls'):
        pass

    else:
        print "EEE invalid prcopt -p %s"%(prcopt)

sys.exit()

