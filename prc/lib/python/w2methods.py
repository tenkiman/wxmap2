#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded methods
#

from M import *
MF=MFutils()


def getCurrentPids(pyfile,doArgs=0,verb=0):
    # -- grep ps output and output to log
    #
    cmd='ps -ef | grep python | grep -v root | grep -v keeplive | grep -v grep | grep -v wing | grep -v %s | grep -v defunc | grep -v globus-connect | grep -v jupyter'%(pyfile)
    cards=MF.runcmdLogOutput(cmd,quiet=1)
    cards=cards.split('\n')
    curPidPSs={}
    for card in cards:
        tt=card.split()
        ntt=len(tt)
        if(ntt > 9):
            pid=int(tt[1])
            PS=tt[8:]
            job=PS[0]
            args=''
            if(len(PS) > 1):
                for n in range(1,len(PS)):
                    args="%s %s"%(args,PS[n])
            (jdir,jfile)=os.path.split(job)
            if(doArgs):
                if(verb): print jfile,' args:',args
                curPidPSs[pid]=(jfile,args)
            else:
                curPidPSs[pid]=jfile
            
    return(curPidPSs)
            

def setTausTauopt(tauopt):

    taui=12
    if(tauopt != None):
        try:
            tt=tauopt.split('.')
        except:
            print 'WWW w2methods.SetTaus -- failed to split() return None'
            taus=None
            return(taus)

        if(len(tt) == 1):
            taub=taue=int(tauopt)
                
        elif(len(tt) == 2):
            taub=int(tt[0])
            taue=int(tt[1])

        elif(len(tt) == 3):
            taub=int(tt[0])
            taue=int(tt[1])
            taui=int(tt[2])

        taus=[]

        for tau in range(taub,taue+1,taui):
            taus.append(tau)

    else:
        taus=None

    return(taus)



def listComp(list1,list2,method='pbetter',undef=-999,hasflag=1,verb=0):
    
    nstat1=0
    nstat2=0
    
    nall=0

    if(len(list1) != len(list2)):
        print 'EEE cannot add two lists of unequal length'
        return(listsum)

    
    for n in range(0,len(list1)):
        ll1=list1[n]
        ll2=list2[n]
    
        if(hasflag):
            flag1=ll1[0][0]
            val1=ll1[1]
            flag2=ll2[0][0]
            val2=ll2[1]
        else:
            flag1=1
            flag2=1
            val1=float(ll1)
            val2=float(ll2)
              
        if(flag1 and flag2):
            if(method == 'pbetter'):
                if(val1 < val2):
                    nstat1=nstat1+1
                else:
                    nstat2=nstat2+1
                if(verb):
                    print 'n: ',n,'nstat1/2: ',nstat1,nstat2,' val1/2: ',val1,val2
            else:
                print "EEE w2methods.listComp() invalid method: ",method
                sys.exit()
            nall=nall+1

    if(nall > 0):
        fn=float(nall)
        pstat1=(nstat1/fn)*100.0
        pstat2=(nstat2/fn)*100.0
        
    else:
        pstat1=pstat2=undef

    if(verb): print 'w2methods.listComp() pstat1/2: ',pstat1,pstat2,'n: ',nall
    
    rc=(pstat1,pstat2,nall)
    return(rc)

def SimpleListStats(dlist,verb=0,undef=-77,undef2=1e20,hasflag=1,flagval=None):
    """
    added undef2 which is semi-universal undef -- used in vdVM in processing VdeckS()
"""
    mean=0.0
    amean=0.0
    sigma=0.0
    mean2=0.0
    max=-1e20
    min=1e20
    
    odlist=[]
    n=0
    for ll in dlist:

        if(hasflag):
            flag=ll[0][0]
            val=ll[1]
            # -- if not a float set to undef
            if(type(val) is StringType): val=undef
        else:
            flag=1
            val=float(ll)
            
        # -- flag test
        #
        flagtest=(flag >= 1)
        if(flagval != None): flagtest=(flag == flagval)
        
        if(val == float(undef) or val == undef2): flagtest=0
                
        if(flagtest):
            odlist.append(val)
            mean=mean+val
            mean2=mean2+val*val
            amean=amean+fabs(val)
            if(val > max): max=val
            if(val < min): min=val
            if(verb):
                print 'stats n: ',n,'flag: ',flag,' val: ',val,' flagtest: ',flagtest
            n=n+1

    if(n > 0):
        mean=mean/float(n)
        amean=amean/float(n)
        var=mean2/float(n) - mean*mean
        if(fabs(var) > epsilonm5):
            sigma=sqrt(var)
        else:
            sigma=0.0
    else:
        mean=None
        amean=None
        sigma=None
        mean=amean=sigma=max=min=undef

    odlist.sort()
    if(n <= 1):
        ptl25=median=ptl75=ptl90=undef
    else:
        width=float(n-1)
        ptl25=width*0.25 ; n250=int(ptl25); n251=n250+1 ; d25=ptl25-n250
        ptl50=width*0.50 ; n500=int(ptl50); n501=n500+1 ; d50=ptl50-n500
        ptl75=width*0.75 ; n750=int(ptl75); n751=n750+1 ; d75=ptl75-n750
        ptl90=width*0.90 ; n900=int(ptl90); n901=n900+1 ; d90=ptl90-n900

        ptl25 =odlist[n250]*(1.0-d25) + odlist[n251]*d25
        median=odlist[n500]*(1.0-d50) + odlist[n501]*d50
        ptl75 =odlist[n750]*(1.0-d75) + odlist[n751]*d75
        ptl90 =odlist[n900]*(1.0-d90) + odlist[n901]*d90

        if(verb):
            print '50: ',n500,n501,d50,odlist[n500],odlist[n501],median
            print '25: ',n250,n251,d25,odlist[n250],odlist[n251],ptl25
            print '75: ',n750,n751,d75,odlist[n750],odlist[n751],ptl75
            print '90: ',n900,n901,d90,odlist[n900],odlist[n901],ptl90
    
    
    rc=(mean,amean,sigma,max,min,n,ptl25,median,ptl75,ptl90)
    return(rc)


def addFile2ZipArchive(addPath,arPath,tmpdir=ptmpBaseDir,
                       rmlastfile=1,
                       forceAdd=0,verb=1):

    if(verb): print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    (addDir,addFile)=os.path.split(addPath)

    try:
        aZ=zipfile.ZipFile(arPath,'a')
    except:
        aZ=zipfile.ZipFile(arPath,'w')

    # -- get last archive
    #
    ainfos=aZ.infolist()

    try:
        ainfo=ainfos[-1]
    except:
        # -- first time?
        ainfo=None

    if(verb):
        print ' addPath(addFile2ZipArchive): ',addPath
        print '  arPath(addFile2ZipArchive): ',arPath

    rc=0
    MF.ChkDir(tmpdir,'mk')
    MF.ChangeDir(tmpdir,verb=verb)
    if(ainfo != None):
        lastfile=aZ.extract(ainfo.filename)
        if(verb): print 'lastPath: ',lastfile
        rc=filecmp.cmp(addPath,lastfile)
        if(verb): print '   cmpRc(addFile2ZipArchive): ',rc
        if(rmlastfile):
            os.unlink(lastfile)

    if(rc):
        # -- they are the same
        doadd=0
        if(forceAdd):
            doadd=1
        else:
            return(0)
    else:
        doadd=1

    if(doadd):
        addZfile="%s_%s"%(addFile,mf.dtg('dtg_hms'))
        if(verb): print '    ADD(addFile2ZipArchive): ',addZfile
        aZ.write(addPath,addZfile,zipfile.ZIP_DEFLATED)
        aZ.close()



def cleanZipArchive(zip,dotestzip=1,forceReadChk=0,doreplace=0,ropt='',verb=0,quiet=0):
    
    (dir,file)=os.path.split(zip)
    (base,ext)=os.path.splitext(file)
    
    zipN="%s/%s-SAV.zip"%(dir,base)

    if(MF.ChkPath(zipN)): os.unlink(zipN)

    siz=MF.GetPathSiz(zip)
    sizN=MF.GetPathSiz(zipN)
    if(sizN == None): sizN=-999

    print 'SSS(cleanZipArchive): %100s %12d'%(zip,siz)
    print 'TTT(cleanZipArchive): %100s %12d'%(zipN,sizN)

    AZ=zipfile.ZipFile(zip)
    AZN=zipfile.ZipFile(zipN,'w')
    ainfos=AZ.infolist()
    lainfos=len(ainfos)

    doreadchk=0

    if(dotestzip):
        MF.sTimer('testzip')
        try:
            badfiles=AZ.testzip()
        except:
            badfiles=-999
        if(badfiles != None): doreadchk=1
        print 'BBB(testzip) badfiles: ',badfiles
        MF.dTimer('testzip')


    if(forceReadChk): doreadchk=1
    
    keepfiles={}
    keepfiles[0]=1

    for i in range(1,lainfos):

        tt0=tt1=1
        if(doreadchk):
            try:
                tt0=AZ.read(ainfos[i-1])
            except:
                tt0=None
            
            try:
                tt1=AZ.read(ainfos[i])
            except:
                tt1=None

        if(mf.find(ainfos[i-1].filename,'/')):
            tt0=None
            print 'WWW directory in ofile: ',ainfos[i-1]
            
        as0=ainfos[i-1].file_size
        ac0=ainfos[i-1].CRC

        as1=ainfos[i].file_size
        ac1=ainfos[i].CRC
        keepfiles[i]=1
        if(tt0 == None): keepfiles[i-1]=0
        if(tt1 == None): keepfiles[i]=0
        if(as0 == as1 and ac0 == ac1 and tt0 != None and tt1 != None):
            keepfiles[i]=0

        if(verb): print 'III %5d'%(i),'as0 ac0: %-12d %-12d'%(as0,ac0),\
                  ' as1 ac1: %-12d %-12d'%(as1,ac0),'keepfiles[i]: ',keepfiles[i]

    # -- check if every file uniq; if so don't bother writing
    #
    nkeep=0
    for i in range(0,lainfos):
        if(keepfiles[i]):nkeep=nkeep+1

    if(nkeep == lainfos):
        print 'WWWWW zip file: ',zip,""" uniq don't bother rewriting..."""
        AZ.close()
        AZN.close()
        return(0)
        

    MF.ChangeDir('/tmp')
    redo=0
    for i in range(0,lainfos):

        if(keepfiles[i]):
            iobj=ainfos[i]
            ofile=iobj.filename
            cmd="unzip -o %s %s"%(zip,ofile)
            output=MF.runcmdLog(cmd,ropt,quiet=quiet)
            
            #iok=1
            #for oo in output:
            #    print oo
            #if(mf.find(oo,'inflated')): iok=1
            #if(iok == 0):
            #    continue
            try:
                AZN.write(ofile,ofile,zipfile.ZIP_DEFLATED)
                os.unlink(ofile)
            except:
                print 'EEE writing ofile: ',ofile,'to: ',zipN


    AZ.close()
    AZN.close()

    if(doreplace):
        cmd="mv %s %s"%(zipN,zip)
        mf.runcmd(cmd,ropt)

    siz=MF.GetPathSiz(zip)
    sizN=MF.GetPathSiz(zipN)
    if(sizN == None): sizN=-999

    print 'SSS(cleanZipArchive): %100s %12d    FINAL'%(zip,siz)
    print 'TTT(cleanZipArchive): %100s %12d    FINAL'%(zipN,sizN)


    return(1)
            
    
def add2000(y):
    if(len(y) == 1):
        yyyy=str(2000+int(y))
    elif(len(y) == 2):
        if(int(y) > 25):
            yyyy=str(1900+int(y))
        else:
            yyyy=str(2000+int(y))
            
    else:
        yyyy=y
    return(yyyy)

def renamemodel(ol):

    rol='XXXX'

    if(ol == 'gfsn'): rol='GFS'
    if(ol == 'ecmo'): rol='ECMWF'
    if(ol == 'ukmo'): rol='UKMO'
    if(ol == 'ecmo'): rol='ECMWF'
    if(ol == 'ngps'): rol='NOGAPS'
    if(ol == 'gfdl'): rol='GFDL'
    if(ol == 'ofcl'): rol='OFCL'
    if(ol == 'bcon'): rol='BCON'
    if(ol == 'clip'): rol='CLIPER'
    if(ol == 'egrr'): rol='UKMO'

    return(rol)

def setpvartag(npvartag,pvartagopt=None):

    if(pvartagopt == '00_12z'):
        if(npvartag == 1):
            pvartag='_00z'
        elif(npvartag == 2):
            pvartag='_12z'

    elif(pvartagopt == '00z'):
        pvartag='_00z'

    elif(pvartagopt == '00_12v06_18z'):
        if(npvartag == 1):
            pvartag='_00/12z'
        elif(npvartag == 2):
            pvartag='_06/18z'
    else:
        pvartag=''

    return(pvartag)


def putpvar(pvar,npvartag,pvartag,model,var,lab,cnt,type='fe'):

    lab=lab+'%s'%(pvartag)
    pvar[model,npvartag,type+'var']=var
    pvar[model,npvartag,type+'lab']=lab
    pvar[model,npvartag,type+'cnt']=cnt




def getpvar(pvar,npvartag,model,type='fe'):

    var=pvar[model,npvartag,type+'var']
    lab=pvar[model,npvartag,type+'lab']
    cnt=pvar[model,npvartag,type+'cnt']

    return(var,lab,cnt)



def reducestmids(stmids):

    ostmids=[]
    for stmid in stmids:
        ostmid=stmid.replace('200','')
        ostmids.append(ostmid)

    return(ostmids)


def isundef(val,undef=None):

    if(val == None):
        return(1)
    
    if(undef != None):
        undefs=[undef]
    else:
        undefs=[-999.,999.]
    rc=0
    for undef in undefs:
        if(val == undef): rc=1
    return(rc)


def isundef(val,undef=None):

    if(val == None):
        return(1)
    
    if(undef != None):
        undefs=[undef]
    else:
        undefs=[-999.,999.]
    rc=0
    for undef in undefs:
        if(val == undef): rc=1
    return(rc)


def iszero(val):
    rc=0
    if(fabs(val) == 0): rc=1
    return(rc)


def smooth(x,window_len=10,
           #window='hanning',
           window='flat',
           adjustWindowLen=1):

    import numpy

    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """

    if(x.size < window_len and adjustWindowLen): window_len=x.size-1
    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]

def chkifRunningOnKaze(pyfile,verb=0,quiet=1,dotcops=0):

    def getocards(outchk):
        ocards=[]
        for card in outchk:
            if(mf.find(card,'grep') or mf.find(card,'tcsh') or len(card) == 0 or card[0] == '*'): continue
            else: 
                ocards.append(card)
                
        return(ocards)
    
        
    if(verb): quiet=0
    rc=0
    cmd='''ssh fiorino@wxmap2 "ps -ef | grep ' python '"'''
    outchkW=MF.runcmdLog(cmd,quiet=quiet)
    ocardsW=getocards(outchkW)
    for ocard in ocardsW:
        if(verb): print 'wxmap2: ',ocard
        if(mf.find(ocard,pyfile)): 
            rc=1
            break
    
    if(dotcops):
        cmd='''ssh fiorino@tcops "ps -ef | grep ' python '"'''
        outchkT=MF.runcmdLog(cmd,quiet=quiet)
        ocardsT=getocards(outchkT)

        for ocard in ocardsT:
            if(verb): print ' tcops: ',ocard
            if(mf.find(ocard,pyfile)): 
                rc=1
                break
        
    return(rc)
    

