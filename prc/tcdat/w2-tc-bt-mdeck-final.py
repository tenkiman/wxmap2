#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from tcbase import *
import ATCF

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local defs
#
def logparse(cards):
    sizes={}
    if(cards == None):
        return(sizes)
    elif(len(cards) == 0):
        return(sizes)
    
    for card in cards:
        tt=card.split()
        sizes[tt[0]]=int(tt[2])
        
    return(sizes)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class RsyncCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['yyyy',    'tyear -- must set '],
            }

        self.defaults={
            'dosizecheck':0,
            'dodupchk':0,
            }

        self.options={
            'popt':             ['p:',None,'a',' [clean.BT | clean.bt | clean.all]'],
            'source':           ['s:',None,'a','source opt'],
            'dofilt9x':         ['9',1,0,'do NOT dofilt9x'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'writelog':         ['W',0,1,'force writing log of mdeck'],
            'btonly':           ['B',0,1,'set the dtgs from findtc to bdeck only'],
            'doLn':             ['L',1,0,"""do NOT use 'ln -s' use 'cp' instead for filesystem independence"""],
            }

        self.purpose='''
calc merged mdeck from bdeck and adeck'''
        self.examples='''
%s  cur                      # just update
%s  cur  -p clean.all        # kill all ln jtwc.local forms
%s  2005-2011  -p clean.all  # kill all ln jtwc.local forms'''



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=RsyncCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# test if the curdtg is in the shem overlap
#


curyyyy=curdtg[0:4]
(shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)

#
# don't dofilt9x....
#
if(yyyy == 'cur' or yyyy == 'ops'):
    dofilt9x=0
    if(popt == None): popt=''
    yyyy=curdtg[0:4]
    mm=curdtg[4:6]
    writelog=1

try:
    (yyyy1,yyyy2)=yyyy.split('-')
    years=range(int(yyyy1),int(yyyy2)+1)
except:
    if(yyyy == 'all'):
        years=range(2000,2005)
        mm='99'
    else:
        years=[yyyy]
    

#
# set years to two years to cover shem overlap
#

if( (yyyy == curyyyy) and shemoverlap):
    years=[yyyy1,yyyy2]


if(yyyy == curyyyy): mm=curdtg[4:6]
#
# do previous year to catch overlap of storms crossing year
#
elif( (yyyy == curyyyy) and (int(mm) == 1)):
    yyyym1=int(yyyy)-1
    yyyym1=str(yyyym1)
    years=[yyyym1,yyyy]

#
# do the names for shem
#
for year in years:

    btdir=w2.TcBtDatDir+"/%s"%(year)
    bttcs=glob.glob("%s/BtOps*"%(btdir))

    
    tcs=[]
    for bttc in bttcs:
        (dir,file)=os.path.split(bttc)
        tc=file.split('.')[2]
        tc=tc+'.'+file.split('.')[3]
        tcs.append(tc)

    mddir=w2.TcMdecksFinalDir+"/%s"%(year)
    mf.ChkDir(mddir,'mk')

    if(popt == 'clean.all'):
        
        MF.sTimer('clean.all')
        MDfiles=glob.glob("%s/MD.*"%(mddir))
        mdecklocalfiles=glob.glob("%s/mdeck.local.*"%(mddir))
        MdOpsfiles=glob.glob("%s/MdOps.*"%(mddir))
        
        for kfile in MDfiles+mdecklocalfiles+MdOpsfiles:
            if(verb): print "killing ",kfile
            os.unlink(kfile)
        MF.dTimer('clean.all')
        
        #cmd="rm %s/MD.* ; rm %s/mdeck.local.* ; rm %s/MdOps.*"%(mddir,mddir,mddir)
        #mf.runcmd(cmd,ropt)


    addir=w2.TcAdecksFinalDir+"/%s"%(year)

    tcs.sort()

    localmds=[]
    log=[]

    if(writelog):
        logdir="%s/%s"%(w2.TcMdeckLogDir,curdtg)
        mf.ChkDir(logdir,'mk')
        logfile="mdeck.%s.txt"%(mf.dtg('dtg_ms'))
        logpath="%s/%s"%(logdir,logfile)

    for tc in tcs:
        
        stmid=tc.split('.')[1]+'.'+tc.split('.')[0]
        stm3id=tc.split('.')[1]

        b1id=stm3id[2:3]
        b3id=Basin1toBasin3[b1id]

        mdcards=findtc(stmid,dofilt9x,verb=verb,btonly=btonly)
        dtgs=mdcards.keys()
        dtgs.sort()

        admask="adeck.local.jtwc.%s.%s.%s.*.txt"%(b3id,year,stm3id)
        admask="%s/%s"%(addir,admask)
        adpaths=glob.glob(admask)
        adpaths.sort()
        
        if(len(adpaths) == 0):
            if(verb):
                print 'WWWWWWW no adpaths ...',admask
            adpath='zy0x1w2'
        elif(len(adpaths) == 1):
            adpath=adpaths[0]
        else:
            adpath=adpaths[-1]
            print 'WWW--AAA: w2-tc-bt-mdeck-final.py --  too many adpaths... ',adpaths,' using the last one...'

        # get bdecks
        #
        btmask="bt.local.jtwc.%s.%s.%s.*.txt"%(b3id,year,stm3id)
        btmask="%s/%s"%(btdir,btmask)
        btpaths=glob.glob(btmask)
        btpaths.sort()
        
        if(len(btpaths) == 0):
            if(verb):
                print 'WWWWWW no btpaths...',btmask
            btpath='zy0x1w2'
        elif(len(btpaths) == 1):
            btpath=btpaths[0]
        else:
            btpath=btpaths[-1]
            print 'WWW-BBB: w2-tc-bt-mdeck-final.py -- too many btpaths... ',btpaths,btmask,' using the last one...'
            print 'originally: EEE too many btpaths... ',btpaths,btmask,' and sys.exit()'
            
        if(btpath == 'zy0x1w2'): 
            print 'WWW(mdeck.final): NO btpath for stm3id: ',stm3id,' year: ',year
            continue
        
        (dir,file)=os.path.split(btpath)
        tt=file.split('.')
        ltt=len(tt)
        #
        # set bdtg by the dtgs in the mdeck cards NOT the bt because nhc shorts the final best track
        #
        bdtg=tt[ltt-3]
        edtg=tt[ltt-2]

        if(len(dtgs) == 0):
            print 'WWW(mdeck.final): NO dtgs for stm3id: ',stm3id,' year: ',year
            continue

        bdtg=dtgs[0]
        edtg=dtgs[-1]


        #
        # check for multiple b1ids
        #
        maskofileid="%s/mdeck.local.jtwc.%s.%s.%2s?.*.txt"%(mddir,b3id,year,stm3id[0:2])
        omdecks=glob.glob(maskofileid)
        chkdup=0
        #
        # turn off dup chk confusing jt/nhc b decks in cpac
        #
        dodupchk=0
        if(len(omdecks) > 1 and dodupchk):
            print 'WWWWWW(dups) multiple local bdecks... ',stm3id[0:2]
            for omdeck in omdecks:
                (dir,file)=os.path.split(omdeck)
                ff=file.split('.')
                omstmid=ff[5]
                bdtg=ff[6]
                edtg=ff[7]
                b1id=omstmid[2]
                agemdeck=w2.PathModifyTimeDtgdiff(curdtg,omdeck)
                print 'WWWWWW(dups) omstmid: ',omstmid,b1id,bdtg,edtg,' omdeck: ',omdeck,agemdeck

            oages={}
            for omdeck in omdecks:
                timei=os.path.getmtime(omdeck)
                (dir,file)=os.path.split(omdeck)
                tt=file.split('.')
                oages[tt[5]]=timei
            kk=oages.keys()
            kk.sort()
            koldest=kk[0]
            oldest=oages[koldest]
            for k in kk:
                if(oages[k] < oldest):
                    koldest=k
            stmid=koldest
            # --- do nothing just output for diagnostics
            #
            # can't stop 
            #continue
            #sys.exit()
            #for omdeck in omdecks:
            #    os.unlink(omdeck)




        mdofile="mdeck.local.jtwc.%s.%s.%s.%s.%s.txt"%(b3id,year,stm3id,bdtg,edtg)
        mdopath="%s/%s"%(mddir,mdofile)

        #
        # compare age of the local bdeck & adeck and local mdeck
        #

        timei=-999
        if(os.path.exists(btpath)):
            timei=os.path.getctime(btpath)
            ltimei=time.localtime(timei)
            dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
            
        timea=-999
        if(os.path.exists(adpath)):
            timea=os.path.getctime(adpath)
            ltimea=time.localtime(timea)
            dtimea=time.strftime("%Y%m%d%H:%M%S",ltimea)

        timeo=-999
        if(os.path.exists(mdopath)):
            timeo=os.path.getctime(mdopath)
            ltimeo=time.localtime(timeo)
            dtimeo=time.strftime("%Y%m%d%H:%M%S",ltimeo)


        if( ( (timei < timeo) and (timea < timeo) ) and (timeo != -999) ):
        # 20101102 -- bypass and 10l.2010 12l.2010 because adeck has junk -- mod'd w2.tc.bt.adeck.final.py
        #if( ( (timei < timeo) and (timea < timeo) ) and (timeo != -999) or mf.find(mdopath,'12L') ):
            if(verb):
                print "OOOOOOOOOOO mdeck already processed: ",mdopath
                print 'bt:      ',dtimei,btpath
                print 'adpath:  ',dtimea,adpath
                print 'mdopath: ',dtimeo,mdopath
            continue

        #
        # bail if no cards, bad bdeck
        #

        if(not(mdcards)):
            print 'WWWWWWWWWWW no cards in bdeck: ',mdopath,' SaYOOOnara it...'
            cmd="rm %s"%(mdopath)
            mf.runcmd(cmd,ropt)

            continue

        print 'MMMMM working/updating --- ',mdopath
        #
        # blow away old mdeck.local.jtwc*
        #
        omdomask="%s/*.%s.%s.%s.*.txt"%(mddir,b3id,year,stm3id)
        cmd="rm %s"%(omdomask)
        mf.runcmd(cmd,ropt)

        print 'mmmmmmmmmmm ',mdopath
        MF.WriteHash2File(mdcards,mdopath)

        localmds.append(mdopath)
        siz=mf.GetPathSiz(mdopath)
        logcard="%s siz: %8d  dtg: %s time %s"%(mdopath,siz,curdtg,mf.dtg('dtg_ms'))
        log.append(logcard)


    if(len(log) > 0 and writelog):
        MF.WriteList2File(log,logpath,verb=1)


    mddir=w2.TcMdecksFinalDir+"/%s"%(year)
    mf.ChkDir(mddir,diropt='mk')

    #222222222222222222222222222222222222222222222222222222222222222222222
    #
    # ln -s to "final" MD
    #

    for md in localmds:
    
        (idir,ifile)=os.path.split(md)
        lf=len(ifile)

        tt=ifile.split('.')

        b3id=tt[3]
        year=tt[4]
        stmid=tt[5]
        bdtg=tt[6]
        edtg=tt[7]
        
        stmnum=int(stmid[0:2])
        
        #
        # always do MdOps; just base on stmnum
        #

        if( (stmnum <= 50) ):
            begs=['MD','MdOps']
        elif( (stmnum > 50) ):
            begs=['MdOps']
        else:
            begs=['MD']

        for beg in begs:
            ofile="%s.%s.%s.%s.%s.%s.txt"%(beg,b3id,year,stmid,bdtg,edtg)
            #omd="%s/%s"%(mddir,ofile)
            #
            # keep dir out of ln?
            #
            os.chdir(idir)
            if(doLn):
                cmd="ln -f -s %s %s"%(ifile,ofile)
            else:
                cmd="cp %s %s"%(ifile,ofile)
                
            mf.runcmd(cmd,ropt)

sys.exit()
