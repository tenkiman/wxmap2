from const import  *
from mfbase import *
import mf 
#from WxMAP2 import W2
#hfipProducts=W2Base().HfipProducts

import fcntl, new
import __builtin__
from fcntl import LOCK_SH, LOCK_EX, LOCK_UN, LOCK_NB

def _sclose(self):
    shelve.Shelf.close(self)
    fcntl.flock(self.lckfile.fileno(), LOCK_UN)
    self.lckfile.close()

def sopen(filename, flag='c', protocol=None, writeback=False, block=True, lckfilename=None):
    """Open the sheve file, createing a lockfile at filename.lck.  If 
    block is False then a IOError will be raised if the lock cannot
    be acquired"""
    if lckfilename == None:
        lckfilename = filename + ".lck"
    lckfile = __builtin__.open(lckfilename, 'w')

    # Accquire the lock
    if flag == 'r':
        lockflags = LOCK_SH
    else:
        lockflags = LOCK_EX
    if not block:
        lockflags = LOCK_NB
    fcntl.flock(lckfile.fileno(), lockflags)

    # Open the shelf
    shelf = shelve.open(filename, flag, protocol, writeback)

    # Override close 
    shelf.close = new.instancemethod(_sclose, shelf, shelve.Shelf)
    shelf.lckfile = lckfile 

    # And return it
    return shelf

class MFbase():

    def sendEmail(self,to_addr_list,subject,message,
                  passwdFile='/data/amb/users/fiorino/w21/prc/lib/python/passwdMFemail',
                  cc_addr_list=[],
                  from_addr='michael.fiorino@noaa.gov',
                  smtpserver='smtp.gmail.com:587',
                  login='michael.fiorino@noaa.gov',
                  password=None,
                  ):


        import smtplib,base64

        # did base64.b64encode(real password) - put in passwdFile and made it rw by owner only
        # and did NOT include in svn
        #

        password=open(passwdFile).read()
        password=base64.b64decode(password)

        header  = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        if(len(cc_addr_list) > 0): header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject

        message = header + message

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()


    def ls(self,findstr=None,lsopt=None,maxchar=116,varsonly=0,quiet=0):

        methods=[]
        variables=[]
        clss=[]
        nvar=0

        mlen=28

        mformat="MMM: %%-%ds: %%s"%(mlen)
        cformat="CCC: %%-%ds: %%s"%(mlen)
        vformat="VVV(%%3d): %%-%ds: %%s"%(mlen)
        dd=inspect.getmembers(self)

        for d in dd:
            name=d[0]
            if(findstr != None):
                if(not(mf.find(name,findstr))): continue

            if(type(d[1]) is ListType and len(str(d[1])) > maxchar):
                val=str(d[1])[0:maxchar]+' ... '
            elif(type(d[1]) is DictType and len(str(d[1])) > maxchar):
                val=str(d[1])[0:maxchar]+' ... '
            else:
                try:
                    val=str(d[1])
                except:
                    val='undef...'

            if(lsopt != None): val=str(d[1])
            

            if(mf.find(val,'<bound method') or mf.find(val,'<module ')):
                methods.append(mformat%(name[0:mlen],val[0:maxchar]))
            elif(mf.find(val,'instance at')):
                clss.append(cformat%(name[0:mlen],val[0:maxchar]))
            else:
                if(len(val) >= maxchar): val=val[0:maxchar] + '... NOT ListType or DictType'
                variables.append(vformat%(nvar,name[0:mlen],val))
                nvar=nvar+1

        if(not(quiet)):

            if(len(clss) > 0 and not(varsonly)):
                print
                for cls in clss:
                    print cls
                print

            if(len(methods) > 0 and not(varsonly)):
                for method in methods:
                    print method
                print

            for variable in variables:
                print variable


        return(clss,methods,variables)


    def setObjVarsNone(self):

        keepvars=keepclss=None

        if(hasattr(self,'keepObjVars')):
            keepvars=self.keepObjVars

        if(hasattr(self,'keepObjClss')):
            keepclss=self.keepObjClss

        if(keepvars == None and keepclss == None):
            return


        # -- get the classes, methods, vars
        #
        (clss,methods,variables)=self.ls(quiet=1)

        if(keepvars != None):
            for var in variables:
                vvar=var.split()[2].strip()
                if(mf.find(vvar,'__')): continue
                if(not(vvar in keepvars)):
                    try:
                        cmd="self.%s=None"%(vvar)
                        exec(cmd)
                    except:
                        print 'MFbase.setObjVarsNone -- did not None vvar: ',vvar

        if(keepclss != None):
            for cls in clss:
                vcls=cls.split()[1].strip()
                if(mf.find(vcls,'__')): continue
                if(not(vcls in keepclss)):
                    try:
                        cmd="self.%s=None"%(vcls)
                        exec(cmd)
                    except:
                        print 'MFbase.setObjVarsNone -- did not None vcls: ',vcls




    def setPyppath(self,pyppath=None):
        """ method to set the pyppath for getPyp and putPyp"""

        if(pyppath == None and hasattr(self,'pyppath') and self.pyppath == None):
            ppath='/tmp/zy0x1w2.pyp'

        elif(pyppath != None):
            ppath=pyppath

        elif(hasattr(self,'pyppath') and self.pyppath != None):
            ppath=self.pyppath

        else:
            print 'EEE unable to open either pyppath: ',pyppath,' or self.pyppath: ',self.pyppath
            return(None)

        return(ppath)



    def getPyp(self,pyppath=None,unlink=0,verb=0):

        ppath=self.setPyppath(pyppath=pyppath)
        if(ppath == None): return(None)

        if(unlink):
            try:    os.unlink(ppath)
            except:  None

        if(os.path.exists(ppath)):
            if(verb): print "getPyp opening: ",ppath
            PS=open(ppath)
            try:
                FR=pickle.load(PS)
                if(verb): print "hai, getPyp ha, itadakimasu..."
            except:
                if(verb): print "IEE, getPyp ga, komarimashita ne! "
                FR=None
            PS.close()
            return(FR)

        else:
            return(None)


    def putPyp(self,pyp=None,pyppath=None,unlink=0,
               unlinkException=0,
               unlinkBadDump=0,
               verb=1):

        ppath=self.setPyppath(pyppath=pyppath)
        if(ppath == None): return(None)

        if(pyp != None):
            pyppckle=pyp
        else:
            pyppckle=self

        if(unlink):
            try:
                os.unlink(ppath)
            except:
                None

        try:
            PS=open(ppath,'w')
            pickle.dump(pyppckle,PS)
            PS.close()
            siz=os.path.getsize(ppath)
            if(verb):
                print 'III dumping pyp: ',pyppckle
                print 'III     to path: ',ppath,' size: ',siz
        except:
            if(unlinkException):
                print 'WWW killing ppath: ',ppath,' on open/dump exception'
                os.unlink(ppath)
                try:
                    PS=open(ppath,'w')
                    pickle.dump(pyppckle,PS)
                    PS.close()
                except:
                    print """EEEEE unable to pickle.dump: ',ppath,' after unlinkException, kill it anyway...it's baaad, it's baaad..."""
                    os.unlink(ppath)

            else:
                print 'EEEEE unable to pickle.dump: ',ppath,' so unlink it???'
                if(unlinkBadDump): os.unlink(ppath)


    def initCurState(self):

        self.curdtg=mf.dtg()
        self.curphr=mf.dtg('phr')
        self.curyear=self.curdtg[0:4]

        if(not(hasattr(self,'curtime'))):  self.curtime=[]

        self.curtime.append(mf.dtg('dtg.phms'))



    def sTimer(self,tag='notag'):

        if(not(hasattr(self,'stimers'))):    self.stimers={}
        value=timer()
        self.loadDictList(self.stimers,tag,value)

    def dTimer(self,tag='notag'):

        sleep(0.1)
        phms=mf.dtg('dtg.phms')
        if(hasattr(self,'stimers')):
            value=time.time()-self.stimers[tag][-1]
            
        card="TTTTTTTTTTTTTTTTTTTTTTT-------------------timer: %-72s: %6.3f      at: %s"%(tag,value,phms)
        print card
        return(card)

    def sTime(self,tag='notag'):

        if(not(hasattr(self,'stimes'))):    self.stimes={}
        value=timer()
        self.loadDictList(self.stimes,tag,value)


    def dTime(self,tag='notag'):

        if(not(hasattr(self,'curdtimes'))):
            self.curdtimes={}
        else:
            if( type(self.curdtimes) is not(DictType) ): self.curdtimes={}

        value=mf.dtg('dtg.phms')
        self.loadDictList(self.curdtimes,tag,value)

        if(not(hasattr(self,'dtimes'))):   self.dtimes={}
        value=time.time()-self.stimes[tag][-1]
        self.loadDictList(self.dtimes,tag,value)



    def loadDictList(self,dict,key,value):
        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)




class MFutils(MFbase):

    import mf

    calendar='gregorian'

    mname = {
        '01':'January',
        '02':'February',
        '03':'March',
        '04':'April',
        '05':'May',
        '06':'June',
        '07':'July',
        '08':'August',
        '09':'September',
        '10':'October',
        '11':'November',
        '12':'December'
    }

    mday=(0,31,28,31,30,31,30,31,31,30,31,30,31)
    mdayleap=(0,31,29,31,30,31,30,31,31,30,31,30,31)
    aday=(1,32,60,91,121,152,182,213,244,274,305,335)
    adayleap=(1,32,61,92,122,153,183,214,245,275,306,336)

    sec2hr=1/3600.0

    pyppath=None

    def nDayYear(self,yyyy):
        nd=365
        if (int(yyyy)%4 == 0): nd=366
        return(nd)

    def nDayMonth(self,yyyymm):
        yyyy=int(yyyymm[0:4])
        mm=int(yyyymm[4:6])

        leap=0
        if (yyyy%4 == 0): leap=1

        #
        # override leaping if 365 day calendar
        #
        if(self.calendar == '365day'): leap=0

        if(leap):
            return(self.mdayleap[mm])
        else:
            return(self.mday[mm])


    def TimeZoneName(self):

        import time
        tz=time.tzname
        tz=tz[time.daylight]
        return(tz)


    def Dtg2JulianDay(self,dtg):

        import time
        year=int(str(dtg)[0:4])
        month=int(str(dtg)[4:6])
        day=int(str(dtg)[6:8])

        t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        jday=time.gmtime(t)[7]
        jday="%03d"%(int(jday))
        return (jday)

    def YearJulianDay2YMD(self,year,jday):

        from datetime import date,timedelta
        ymd=date(int(str(year)),1,1) + timedelta(int(str(jday))-1)
        ymd=ymd.strftime("%Y%m%d")
        return(ymd)



    def YearJulianDay2Dtg(self,year,jday,chour=None):

        from datetime import date,timedelta
        ijday=int(jday)
        rjdayhr=jday-ijday*1.0
        ymd=date(int(str(year)),1,1) + timedelta(ijday-1)
        if(chour == None):
            chour="%02d"%(int(rjdayhr*24.0+0.5))
        ymd=ymd.strftime("%Y%m%d")
        dtg=ymd+chour
        return(dtg)


    def Dtg2Timei(self,dtg):
        timei=time.strptime(dtg,"%Y%m%d%H")
        return(timei)


    def DeltaTimei(self,timei1,timei2):

        t1=time.mktime(timei1)
        t2=time.mktime(timei2)
        dt=(t1-t2)/3600.0
        return(dt)

    def getGtime4DTG(self,dtg,
                     #localTZ='America/Denver', localTZname='MST', localTZnameDST='MDT',
                     localTZ='US/Eastern', localTZname='EST', localTZnameDST='EDT',
                     local=1,verb=0):
        
        from datetime import datetime
        from dateutil import tz
        from datetime import date
        import calendar
        import pytz
        
        
        def findDay(year,month,day):
            born = date(year, month, day)
            return born.strftime("%a")
        
        
        def is_dst (localTZ,dtg=None):
            
            """Determine whether or not Daylight Savings Time (DST)
            is currently in effect"""
            # -- use dtg
        
            if(dtg != None):
                yy=int(dtg[0:4])
                mm=int(dtg[4:6])
                dd=int(dtg[6:8])
    
                x=datetime(yy,1,1,0,0,0)
                y=datetime(yy,mm,dd,0,0,0)
                timezone = pytz.timezone(localTZ)
                tzy = timezone.localize(y, is_dst=None)
                tzx = timezone.localize(x, is_dst=None)
                xoff=str(tzx)[-6:-3]
                yoff=str(tzy)[-6:-3]
                xoff=int(xoff)
                yoff=int(yoff)
                
                return not(xoff == yoff)
        
            # -- use current
            else:
                x = datetime(datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(localTZ)) # Jan 1 of this year
                y = datetime.now(pytz.timezone(localTZ))
        
                # if DST is in effect, their offsets will be different
                return not (y.utcoffset() == x.utcoffset())
        
    
        utcTZname='UTC'
        
        isDst=is_dst(localTZ,dtg=dtg)
        if(isDst): localTZname=localTZnameDST
        
        from_zone = tz.gettz('utc'.upper())
        to_zone = tz.gettz(localTZ)
        
        if(verb): print 'iii ',isDst,from_zone,to_zone
            
        cdtg=str(dtg)
        
        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])
        ct='%4d-%02d-%02d %02d:%02d:%02d'%(yy,mm,dd,hh,0,0)
        if(verb): print ct
        
        utc = datetime.strptime(ct, '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
    
        # -- get the standard time string for utc and local
        #
        uuu=utc.astimezone(from_zone)
        uu=str(uuu)
    
        mountain = utc.astimezone(to_zone)
        mm=str(mountain)
        
        myy=int(mm[0:4])
        mmm=int(mm[5:7])
        mdd=int(mm[8:10])
        mhh=int(mm[11:13])
        mmn=int(mm[14:16])
        
        uyy=int(uu[0:4])
        umm=int(uu[5:7])
        udd=int(uu[8:10])
        uhh=int(uu[11:13])
        umn=int(uu[14:16])
        
        
        mDDName=findDay(myy,mmm,mdd)
        uDDName=findDay(uyy,umm,udd)
        
        mmName=mountain.strftime('%b').upper()
        ummName=uuu.strftime('%b').upper()
        
        mgtime="%s %02d%02d %s %02d %s"%(mDDName,mhh,mmn,localTZname,mdd,mmName)
        ugtime="%s %02d%02d %s %02d %s"%(uDDName,uhh,umn,utcTZname,udd,ummName)
        if(verb): 
            print 'gggg: ',mgtime
            print 'uggg: ',ugtime
        
        gtime=ugtime
        if(local):
            gtime=mgtime
            
        return(gtime)


    def PathCreateTimeDtgdiff(self,dtg,path):

        # -- handle broken symbolic link -- return -666.66 -- for gfs2 when /public down
        #
        if(os.path.islink(path) and not(os.path.exists(path))): return(-666.66)
         
        if(not(os.path.exists(path))): return(None)
        timei=os.path.getctime(path)
        ctimei=time.gmtime(timei)
        dtimei=self.Dtg2Timei(dtg)
        dt=self.DeltaTimei(ctimei,dtimei)

        return(dt)


    def PathModifyTime(self,path):

        if(not(os.path.exists(path))): return(None,None,None)
        timei=os.path.getmtime(path)
        ltimei=time.localtime(timei)
        gtimei=time.gmtime(timei)
        dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        ldtg=dtimei[0:10]
        gdtg=gdtimei[0:10]
        return(dtimei,ldtg,gdtg)

    def PathCreateTime(self,path):

        if(not(os.path.exists(path))): return(None,None,None)
        timei=os.path.getctime(path)
        ltimei=time.localtime(timei)
        gtimei=time.gmtime(timei)
        dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        ldtg=dtimei[0:10]
        gdtg=gdtimei[0:10]
        return(dtimei,ldtg,gdtg)


    def PathModifyTimei(self,path):

        if(not(os.path.exists(path))): return(None,None)
        timei=os.path.getmtime(path)
        gtimei=time.gmtime(timei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        return(gtimei,gdtimei)


    def PathCreateTimei(self,path):

        if(not(os.path.exists(path))): return(None,None)
        timei=os.path.getctime(path)
        gtimei=time.gmtime(timei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        return(gtimei,gdtimei)


    def PathModifyTimeDtgdiff(self,dtg,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getmtime(path)
        ctimei=time.gmtime(timei)
        dtimei=self.Dtg2Timei(dtg)
        dt=self.DeltaTimei(ctimei,dtimei)+tzoff

        return(dt)

    def getCurTimei(self):

        ctimei=time.gmtime(time.time())
        return(ctimei)


    def PathModifyTimeCurdiff(self,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getmtime(path)
        ptimei=time.gmtime(timei)
        ctimei=time.gmtime(time.time())
        dt=self.DeltaTimei(ptimei,ctimei)+tzoff

        return(dt)

    def PathCreateTimeCurdiff(self,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getctime(path)
        ptimei=time.gmtime(timei)
        ctimei=time.gmtime(time.time())
        dt=self.DeltaTimei(ptimei,ctimei)+tzoff

        return(dt)

    def GetPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=None
        else:
            siz=os.path.getsize(path)

        return(siz)

    def getPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=-999
        else:
            siz=os.path.getsize(path)

        return(siz)

    def getPathNlines(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            nlines=-999
        else:
            nlines=int(check_output(['wc', '-l', path]).split()[0])
            
        return(nlines)
    
    def getPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=-999
        else:
            siz=os.path.getsize(path)

        return(siz)

    def listTxtPath(self,path,ncprint=None):

        if(self.GetPathSiz(path) != None):
            cards=open(path).readlines()
            ncards=len(cards)
            if(ncprint != None):
                ncprint=min(ncprint,ncards)
            else:
                ncprint=ncards
            for n in range(0,ncprint):
                print cards[n][0:-1]



    def GetDirFilesSiz(self,dir,pathopt='exit',mask="*",verb=0):

        if(self.ChkPath(dir,pathopt='noexit',verb=verb) != 1):
            siz=None
        else:
            paths=glob.glob("%s/%s"%(dir,mask))
            siz=0
            for path in paths:
                fsiz=self.GetPathSiz(path)
                if(fsiz != None): siz=siz+fsiz

        return(siz)

    def GetNfilesDir(self,dir,mask="*"):
        files=glob.glob("%s/%s"%(dir,mask))
        return(len(files))

    def ChkDirOld(dir,diropt='verb'):
    
        if(dir == None):
            if(diropt != 'quiet'): print "dir      = None : "
            return(-2)
    
        if not(os.path.isdir(dir)) :
            if(diropt != 'quiet'): print "dir  (not there): ",dir
            if(diropt == 'mk' or diropt == 'mkdir'):
                try:
                    os.system('mkdir -p %s'%(dir))
                except:
                    print 'EEE unable to mkdir: ',dir,' in mf.ChkDir, return -1 ...'
                    return(-1)
                print 'dir     (MADE): ',dir
                return(2)
            else:
                return(0)
        else:
            if(diropt == 'verb'):
                print "dir      (there): ",dir
            return(1)


    def ChkDir(self,ddir,diropt='verb'):
    
        if(ddir == None):
            if(diropt != 'quiet'): print "dir      = None : "
            return(-2)
    
        if not os.path.exists(ddir):
            
            if(diropt != 'quiet'): print "dir  (not there): ",ddir
            if(diropt == 'mk' or diropt == 'mkdir'):
        
                try:
                    os.makedirs(ddir)
                    print 'dir     (MADE): ',ddir
                    return(2)
                    
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise
                        #print 'EEE unable to mkdir: ',dir,' in mf.ChkDir, return -1 ...'
                        #return(-1)
                    else:
                        print "\nBE CAREFUL! Directory %s already exists." % path
        
            else:
                return(0)
            
        else:
            if(diropt == 'verb'):
                print "dir      (there): ",ddir
            return(1)

    def ChangeDir(self,ddir,verb=1,docurtime=0):

        dtgcurtime=''
        if(docurtime):  dtgcurtime=mf.dtg('curtime')

        try:
            os.chdir(ddir)
            if(verb == 1): print 'cd---> ',ddir,dtgcurtime
            return(1)
        except:
            if(verb != -1): print 'WWW(MF.ChangeDir()) unable to cd to: ',ddir
            return(0)


    def ChkPath(self,path,pathopt='noexit',verb=0):

        if(path == None): return(0)

        if not(os.path.exists(path)) :
            if(verb): print "EEE(ChkPath): path: %s NOT there... "%(path)
            if(pathopt == 'exit'):
                print "EEE(ChkPath): Sayoonara..."
                sys.exit()
            else:
                return(0)
        else:
            return(1)


    def is0618Z(self,dtg):

        hh=dtg[8:10]
        rc=0
        if(hh == '06' or hh == '18'): rc=1
        return(rc)

    def is0012Z(self,dtg):

        hh=dtg[8:10]
        rc=0
        if(hh == '00' or hh == '12'): rc=1
        return(rc)

    def isSynopticHour(self,dtg,dtau=6):

        hh=int(dtg[8:10])
        rc=0
        remainder=hh%dtau
        if(remainder == 0): rc=1
        return(rc,remainder)

    def TimeZoneName(self):

        tz=time.tzname
        tz=tz[time.daylight]
        return(tz)

    def dtg(self,opt="default"):

        tzname=" %s "%(self.TimeZoneName())

        if (opt == "curtime" or opt == "curtimeonly" ):
            t=time.localtime(time.time())
        else:
            t=time.gmtime(time.time())

        yr="%04d" % t[0]
        mo="%02d" % t[1]
        dy="%02d" % t[2]
        hr="%02d" % t[3]
        fhr="%02d" % (int(t[3]/6)*6)
        phr=int(t[3])%6
        mn="%02d" % t[4]
        sc="%02d" % t[5]
        fphr=float(phr)*1.0 + float(mn)/60.0;

        if opt == "default":
            dtg=yr + mo + dy + fhr
        elif opt == "phr":
            dtg="%4.2f"%(fphr)
        elif opt == "fphr":
            dtg=fphr
        elif opt == "dtg.hm":
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
        elif opt == "dtg.phm":
            cphr="%02d"%(phr)
            dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn
        elif opt == "dtgmn":
            dtg=yr + mo + dy +  hr + mn
        elif opt == "dtg_ms":
            dtg=yr + mo + dy +  hr + "_%s_%s"%(mn,sc)
        elif opt == "dtg_hms":
            dtg=yr + mo + dy + "_%s_%s_%s"%(hr,mn,sc)
        elif opt == "dtg.hm":
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
        elif opt == "dtg.hms":
            dtg=yr + mo + dy +  " " + hr + ":" + mn + ":" + sc
        elif opt == "dtgcurhr":
            dtg=yr + mo + dy + hr
        elif (opt == "timeonly"):
            dtg=hr+":"+mn+":"+sc+ " UTC "
        elif (opt == "time"):
            dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
        elif (opt == "curtime"):
            dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
        elif (opt == "curtimeonly"):
            dtg=hr+":"+mn+":"+sc+ tzname
        else:
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

        return(dtg)

    def dtg2time(self,dtg):

        cdtg=str(dtg)

        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])

        ct=(yy,mm,dd,hh,0,0,0,0,0)
        time=mktime(ct)
        return(time)

    def dtg2YMDH(self,dtg):

        cdtg=str(dtg)

        yy=cdtg[0:4]
        mm=cdtg[4:6]
        dd=cdtg[6:8]
        hh=cdtg[8:10]

        return(yy,mm,dd,hh)
    
    def dtg2ISODateTime(self,dtg):
        (yy,mm,dd,hh)=self.dtg2YMDH(dtg)
        isodate="%s-%s-%s"%(yy,mm,dd)
        isohour="%02d:00:00"%(int(hh))
        return(isodate,isohour)
        


    def DtgDiff(self,dtg1,dtg2):

        dtg1=str(dtg1)
        dtg2=str(dtg2)

        yyyy1=int(dtg1[0:4])
        yyyy2=int(dtg2[0:4])

        offyear=1981
        if(yyyy1%4==0):
            offyear=1980
        if(yyyy2%4==0):
            offyear=1979

        # override leaping if 365 day calendar
        #
        if(self.calendar == '365day'): offyear=1981

        #
        # 20030828 -- fix crossing year if offsetting
        #

        dyyyy=yyyy2-yyyy1

        if(yyyy1 < offyear or yyyy2 < offyear):
            dtg1off=offyear-int(dtg1[0:4])
            dtg1="%04d"%(offyear)+dtg1[4:10]
            dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

        t1=self.dtg2time(dtg1)
        t2=self.dtg2time(dtg2)
        nhr=(t2-t1)*self.sec2hr

        return(nhr)

    def DiffDtgHms(self,dtghms1,dtghms2):
        """ diff of dtghms2 (2nd arg) - dtghms1"""
        ymd1=dtghms1.split()[0]
        y1=ymd1[0:4]
        #ndy1=self.nDayYear(y1) -- constant length of year
        ndy1=365.0
        jday1=self.Dtg2JulianDay(ymd1)
        (hh1,mm1,ss1)=dtghms1.split()[1].split(':')
        ymdh1=(float(y1)*float(ndy1) + float(jday1))*24.0 + int(hh1)*1.0 + int(mm1)/60.0 + int(ss1)/3600.0
        #print '11111111111 ',y1,ndy1,ymd1,hh1,mm1,ss1,ymdh1

        ymd2=dtghms2.split()[0]
        y2=ymd2[0:4]
        #ndy2=self.nDayYear(y2)
        ndy2=ndy1
        jday2=self.Dtg2JulianDay(ymd2)
        (hh2,mm2,ss2)=dtghms2.split()[1].split(':')
        
        ymdh2=(float(y2)*float(ndy2) + float(jday2))*24.0 + int(hh2)*1.0 + int(mm2)/60.0 + int(ss2)/3600.0
        #print '22222222222 ',y2,ndy2,ymd2,hh2,mm2,ss2,ymdh2
        diff=ymdh2-ymdh1
        #print 'ddddddddddd ',diff

        return(diff)



    def YearRange(self,byear,eyear=None,inc=1):

        def yearinc(year,inc):
            nyear=int(year)+inc
            return(nyear)

        if(eyear == None):
            eyear=byear

        years=[]

        byear=int(byear)
        eyear=int(eyear)

        year=byear

        while(year<=eyear):
            years.append(year)
            year=yearinc(year,inc)

        return(years)


    def makeDtgsString(self,dtgs,msiz=1024,osiz=132,ndtg=10):
        """ clean up list of dtgs"""

        #card=str(dtgs)[0:msiz].replace(', ','').replace("""''""",' ').replace("""['""",'').replace("""']""",'')
        #
        #if(len(card) > osiz):
        #    card=card[0:osiz]
        #    card=card+'...'



        nend=len(dtgs)
        card='N: %4d  dtgs: '%(nend)
        if(nend == 0): return(card)
        if(len(dtgs) >= ndtg): nend=ndtg/2

        for dtg in dtgs[0:nend]:
            card=card+dtg+' '


        if(len(dtgs) >= ndtg):
            card=card+'... '
            for dtg in dtgs[(len(dtgs)-ndtg/2):]:
                card=card+dtg+' '

        return(card)


    def setDirFromHash(self,ss,n):

        sbdir=''
        for sb in ss[0:len(ss)-n]:
            sbdir="%s/%s"%(sbdir,sb)
        sbdir=sbdir.replace('//','/')

        return(sbdir)



#tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
# time
#

    def rhh2hhmm(hh):

        if(hh < 0):
            rhh=abs(hh)
            lt0=1
        else:
            rhh=hh
            lt0=0

        imm=int(rhh*60.0+0.5)
        ihh=imm/60
        imm=imm%60
        if(lt0):
            ohhmm="-%02d:%02d"%(ihh,imm)
        else:
            ohhmm="+%02d:%02d"%(ihh,imm)

        return(ohhmm)


    #uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
    # utilities

    def loadDictList(self,dict,key,value):
        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)


    def uniqDictList(self,tdict):

        kk=tdict.keys()

        for k in kk:
            tlist=tdict[k]
            tlist=mf.uniq(tlist)
            tdict[k]=tlist
            
        return(tdict)

    def uniqDict2List(self,ddict):
    
        kk1=ddict.keys()
        
        for k1 in kk1:
            kk2=ddict[k1].keys()
            
            for k2 in kk2:
                dlist=ddict[k1][k2]
                dlist=mf.uniq(dlist)
                ddict[k1][k2]=dlist

    def uniqDictDict(self,dict):
        """ uniq a dict of dicts"""
        kk=dict.keys()

        for k in kk:
            dict2=dict[k]
            kk2=dict2.keys()
            self.uniqDictList(dict2)
            dict[k]=dict2
            
        return(dict)



    def addList2DictList(self,dict,key,list):
        try:
            dict[key]=dict[key]+list
        except:
            dict[key]=list


    def appendList(self,list,value):

        try:
            list.append(value)
        except:
            list=[]
            list.append(value)

    def appendDictList(self,dict,key,value):

        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)

    def append2KeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1][key2].append(value)

        except:

            try:
                dict[key1][key2]
            except:
                try:
                    dict[key1]
                except:
                    dict[key1]={}

            dict[key1][key2]=[]
            dict[key1][key2].append(value)

    def set2KeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1][key2]=value

        except:

            try:
                dict[key1][key2]
            except:
                try:
                    dict[key1]
                except:
                    dict[key1]={}

            dict[key1][key2]=value


    def append3KeyDictList(self,dict,key1,key2,key3,value):

        try:
            dict[key1][key2][key3]=value
        except:
            try:
                dict[key1][key2]={}
                dict[key1][key2][key3]=value
            except:
                dict[key1]={}
                dict[key1][key2]={}
                dict[key1][key2][key3]=value



    def append2TupleKeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1,key2].append(value)
        except:
            dict[key1,key2]=[]
            dict[key1,key2].append(value)


    def append3TupleKeyDictList(self,dict,key1,key2,key3,value):

        try:
            dict[key1,key2,key3].append(value)

        except:
            dict[key1,key2,key3]=[]
            dict[key1,key2,key3].append(value)



    def DictTr(self,dic):
        dict={}
        kk=dic.keys()
        for k in kk:
            val=dic[k]
            try:
                dict[val].append(k)
            except:
                dict[val]=[]
                dict[val].append(k)

        return(dict)

    def DictAdd(self,dic1,dic2,priority=2):
        dic={}
        kk1=dic1.keys()
        kk2=dic2.keys()
        kk=kk1+kk2
        kk.sort()
        kk=self.uniq(kk)

        for k in kk:

            hk1=dic1.has_key(k)
            hk2=dic2.has_key(k)

            if(hk1 and hk2):
                if(priority == 2):
                    dic[k]=dic2[k]
                else:
                    dic[k]=dic1[k]

            elif(hk1 and not(hk2)):
                dic[k]=dic1[k]
            elif(not(hk1) and hk2):
                dic[k]=dic2[k]
            else:
                print 'EEE DicAdd'
                sys.exit()

        return(dic)


    def uniqDict(self,dict):
        tt={}
        for kk in dict.keys():
            dd=dict[kk]
            dd=self.uniq(dd)
            tt[kk]=dd
        return(tt)

    def Dic2list(self,dic,ne):
        kk=dic.keys()
        kk.sort()

        list=[]
        for k in kk:
            list.append(dic[k][ne])

        return(list)


    def List2Dict(self,dic,list,ne):

        kk=dic.keys()
        kk.sort()

        for i in range(0,len(kk)):
            dic[kk[i]][ne]=list[i]

        return

    def List2String(self,ilist):

        ostring='\n'.join(ilist)
        ostring=ostring+'\n'
        return(ostring)
    
    def setList2String(self,ilist):
                
        lstring=''
        
        for n in range(0,len(ilist)):
            im=ilist[n]
            lstring=lstring+'%s'%(im)
            if(n < len(ilist)-1):
                lstring=lstring+','
            if(n > 0):
                lstring=lstring+' '
        return(lstring)
                

    def PrintDict(self,dict,name='dict'):

        cards=[]
        kk=dict.keys()
        kk.sort()
        nh=len(dict)

        # -- case of empty dict
        #
        if(len(kk) == 0):
            print 'WWW MF.PrintDict dict={} ... return cards=[]'
            return(cards)

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
            for n in dict[k]:
                card=card+' '+str(n)
            cards.append(card)

        return(cards)



    def WriteString2File(self,string,path,verb=0,warnonly=1):

        try:
            c=open(path,'w')
        except:
            print "EEE unable to open (MF.WriteString2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        c.writelines(string)
        c.close()
        return


    def WriteList2File(self,list,path,verb=0,warnonly=1):

        try:
            c=open(path,'w')
        except:
            print "EEE unable to open path(MF.WriteList2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        for card in list:
            rcard=card.rstrip()
            if(verb): print rcard
            rcard=rcard+'\n'
            c.writelines(rcard)
        c.close()
        return


    def WriteList2Path(self,dlist,path,append=0,verb=0,warnonly=1):

        try:
            if(append):
                c=open(path,'a')
            else:
                c=open(path,'w')
        except:
            print "EEE unable to open path(MF.WriteList2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        for card in dlist:
            if(verb): print card
            card=card.rstrip()+'\n'
            c.writelines(card)
        c.close()
        return

    def WriteString2Path(self,string,path,verb=0,warnonly=1):

        self.WriteString2File(string,path,verb=verb)

        return


    def WriteHash2File(self,hash,path,verb=0):

        keys=hash.keys()
        keys.sort()

        O=open(path,'w')
        for key in keys:
            O.writelines(hash[key]+'\n')

        O.close()



    def ReadFile2List(self,path,verb=0):

        try:
            list=open(path,'r').readlines()
        except:
            print "EEE(ReadFile2List) unable to open path: %s"%(path)
            return(None)

        return(list)


    def ReadFile2String(self,path,verb=0):

        string=''
        try:
            list=open(path,'r').readlines()
        except:
            print "EEE(ReadFile2String) unable to open path: %s"%(path)
            return(string)

        for tt in list:
            if(verb): print tt
            string=string+str(tt)
        return(string)


    def WriteCtl(self,ctl,ctlpath,verb=0):

        try:
            c=open(ctlpath,'w')
        except:
            print "EEE unable to open: %s"%(ctlpath)
            sys.exit()

        if(verb): print "CCCC creating .ctl: %s"%(ctlpath)
        c.writelines(ctl)
        c.close()
        return


    def PrintList(self,list,verb=0):

        for card in list:
            print card


    def sumList(self,list):
        if(list == None):
            sum=None
        else:
            sum=0.0
            for l in list:
                sum=sum+float(l)
        return(sum)


    # --- fundamentals
    #

    def uniq(self,list):
        weirdtest='asdasdfasdfasdfasdf'
        #
        # sort before length check for case of two
        #
        list.sort()
        rlist=[]

        if(len(list) > 2):
            test=list[1]
            test=weirdtest
        elif(len(list) == 0):
            return(rlist)
        else:
            test=list[0]

        if(test != weirdtest):
            rlist.append(test)

        for l in list:
            #if(repr(l) != repr(test)):
            if(l != test):
                rlist.append(l)
                test=l
        return(rlist)


    def find(self,mystr,pattern):
        rc=0
        if(mystr.find(pattern) != -1): rc=1
        return(rc)



    def h2hm(self,age):

        fh=int(age)*1.0
        im=int( (age-fh)*60.0+0.5 )
        if(im == 60):
            fh=fh+1.0
            im=0

        cage="%4.0f:%02d"%(fh,im)
        return(cage)


    def min2minsec(self,min):

        fm=int(min)*1.0
        im=int( (min-fm)*60.0+0.5 )
        if(im == 60):
            fm=fm+1.0
            im=0

        cmin="%4.0f:%02d"%(fm,im)
        return(cmin)



    def runcmdLog(self,cmd,ropt='',quiet=0,printCmd='runcmdLog'):

        if(ropt == 'norun'):
            print "CCC(%s): %s"%(printCmd,cmd)
            return([])
        else:
            if(not(quiet)): print "CCC(%s): %s"%(printCmd,cmd)
            p=Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.read()
            lines=output.split('\n')

        return(lines)


    def runcmdLogOutput(self,cmd,ropt='',quiet=0):

        if(ropt == 'norun' or not(quiet)): print "CCC(runcmdLog): %s"%(cmd)

        if(ropt == 'norun'):
            return([])
        else:
            p=Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.read()

        return(output)



    def runcmd(self,command,logpath='straightrun',lsopt=''):

        if(logpath == ''):
            logpath='straightrun'

        if(logpath == 'straightrun' or logpath == 'norun'):
            if(lsopt != 'q'): print "CCC: %s"%command
            if(logpath != 'norun'): os.system(command)
            return

        if(logpath == 'quiet'):

            tt=command.split()
            mycmd=tt[0]
            myarg=''
            if(len(tt) > 1):
                for t1 in tt[1:]:
                    myarg="%s %s"%(myarg,t1)

            #p=Popen([mycmd,myarg], stdout=PIPE)
            #(o,e)=p.communicate()

            rc=os.popen(command).readlines()
            return(rc)

        global LF

        #
        # output to log file (append and add title line)
        #

        if(logpath != 'nologpath'):

            log=getCommandOutput2(command)

            lout="\nTTT: %s  :: CCC: %s\n\n"%(dtg6 ('curtime'),command)
            lout=lout+log

            if(not(os.path.exists(logpath))):
                try:
                    LF=open(logpath,'a')
                    LF.writelines(lout)
                    LF.flush()
                except:
                    print 'EEE(runcmd): unable to open logpath: %s'%(logpath)
                    return
            else:
                try:
                    LF.writelines(lout)
                    LF.flush()
                except:
                    try:
                        LF=open(logpath,'a')
                        LF.writelines(lout)
                        LF.flush()
                    except:
                        LF.writelines(lout)
                        LF.flush()
                        print 'EEE(runcmd): unable to write to logpath: %s'%(logpath)
                        return

        #
        # output to terminal
        #

        else:

            log=getCommandOutput2(command)

            print "CCC(log): %s\n"%command
            print log

        return

    def runcmdRetry(self,cmd,ropt='',nTry=0,nTryMax=3,trySleep=5,
                    errorString='error',printCmd='runcmdRetry'):

        rsyncOK=1
        rc=0
        output=self.runcmdLog(cmd,ropt,printCmd=printCmd)
        for o in output:
            print o
            if(mf.find(o,errorString)): rsyncOK=0

        if(rsyncOK == 0): 
            nTry=1
        elif(rsyncOK):
            rc=1
            return(rc)

        while(nTry <= nTryMax):
            rsyncOK=1
            print
            print "IIIIIIII--------------------------retry cmd:",cmd, "ntry: ",nTry,' nTryMax: ',nTryMax
            print
            time.sleep(trySleep)  

            output=self.runcmdLog(cmd,ropt,printCmd=printCmd)
            for o in output:
                print o
                if(mf.find(o,errorString)): rsyncOK=0

            if(rsyncOK):
                nTry=nTryMax+1
                rc=1
            else:
                nTry=nTry+1
                rc=0

        return(rc)



    def get0012fromDtgs(self,dtgs):

        odtgs=[]
        for dtg in dtgs:
            hh=int(dtg[8:10])
            if(hh == 12 or hh == 0): odtgs.append(dtg)

        return(odtgs)



    def chkIfJobIsRunningOld(self,job,jobopt=None,killjob=1,verb=1,incron=0,nminWait=10,timesleep=5):

        """20120209 -- set killjob=1, if both hit it at the same time, will be stuck"""

        curpid=os.getpid()


        def isRunning(job,jobopt,killjob):

            pids=mf.LsPids()

            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2])
                jobchk=mf.find(prc,job)

                if(jobopt != None):  joboptchk=mf.find(prc,jobopt)
                else:                joboptchk=1

                if(jobchk and joboptchk and cpid != curpid):
                    #if(incron and not(mf.find(prc,'tcsh'))): continue
                    # -- bypass any proc with tcsh -- means in cron(?)
                    ctime=mf.dtg('curtime')
                    if(mf.find(prc,'tcsh') or mf.find(prc,'/bin/sh -c')): continue
                    print 'isRunning...cpid:',cpid,'curpid: ',curpid,'prc: ',prc,'aaaaaaaaaaaaafter tcsh check',killjob
                    rc=rc+1

                    if(killjob):
                        print 'KKKKKKKKKKK killing this job since a previous instance is already running....'
                        cmd="kill %s"%(curpid)
                        mf.runcmd(cmd,'')

            return(rc)

        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(mf.find(osname,'posix'))):
            print 'WWW chkIfJobIsRunning is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        # -- check if *TWO* or more instances running, the first is the current, but that is checked above...
        if(nminWait > 0 and isRunning(job,jobopt,killjob) >= 1):
            nsleep=0
            while(nsleep < (nmaxsleep-1) and isRunning(job,jobopt,killjob) > 1 ):
                print 'SSSleeping in chkIfJobIsRunning nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfJobIsRunning...job:',job,'jobopt:',jobopt,'still running...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

            rc=0

        else:
            rc=isRunning(job,jobopt,killjob)
            if(verb): print 'chkIfJobIsRunning rc: ',rc

        return(rc)


    def whoIsRunningNew(self,job,jobopt=None,killjob=0,rcPid=0):
        """ 
20210624 -- better version of isRunning because of switch to bash from tcsh
looks for all instances of the job first to set the code

"""
        cpidOut=-999
        rc=0

        runPids=mf.findPyPids(job)
        nrunPids=len(runPids)
        
        for runp in runPids:
            print runp
            
        # -- if only one return 0 to not cycle
        #
        if(nrunPids == 1):
            (cpid,opid,prc,ptime)= runPids[0]
            return(0)
        
        if(nrunPids > 1):

            jobchk=1
            (curpid,opid,curprc,ptime)=runPids[-1]

            for (cpid,opid,prc,ptime) in runPids:
            
                if(jobopt != None):
                    try:
                        prcjobopt=prc.split()[2:]
                    except:
                        prcjobopt=None

                    if(prcjobopt != None):
                        prcjoboptS=''
                        for pp in prcjobopt:
                            prcjoboptS='%s %s'%(prcjoboptS,pp)

                        if(joboptchkType == 'find'): 
                            joboptchk=mf.find(prcjoboptS,jobopt)
                        else:
                            joboptchk=(prcjoboptS == jobopt)
                else:
                    joboptchk=1
                    
                print 'jjjjjjjjjjjjjjjj',prc,cpid,curpid
                if(jobchk and joboptchk and cpid != curpid):

                    ctime=mf.dtg('curtime')
                    print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid: ',cpid,' prc: ',prc,'job: ',job,'jobopt: ',jobopt
                    cpidOut=cpid
                    rc=rc+1

                    kropt='quiet'
                    kropt='norun'
                    kropt=''
                    # -- do the killing inside whoIsRunning
                    #
                    if(killjob == 1):
                        print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                        cmd="kill %s"%(curpid)
                        mf.runcmd(cmd,kropt)
                    elif(killjob == -1):
                        print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                        cmd="kill %s"%(cpid)
                        mf.runcmd(cmd,kropt)

        if(rc > 0 and rcPid): rc=cpidOut
        
        return(rc)




    def chkRunning(self,pyfile,setJobopt=None,strictChkIfRunning=0,verb=0,killjob=0,
                   timesleep=5,nminWait=5):
        
        """ big and complete check
"""
    # -- get command line vars, except -N
        pyfileopt=''
        for s in sys.argv[1:]:
            if(s != '-N'):
                pyfileopt='%s %s'%(pyfileopt,s)
    
        jobopt=pyfileopt.split()[0]
        # -- if very sctrict check -- any instance of pyfile
        if(strictChkIfRunning): jobopt=None
        
        if(setJobopt != None): jobopt=setJobopt
        
        if(verb): self.sTimer('chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
        rc=self.chkIfJobIsRunning(pyfile,jobopt=jobopt,killjob=killjob,verb=verb,nminWait=nminWait,
                                  timesleep=timesleep)
        if(verb): self.dTimer('chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
        
        return(rc)



    def chkIfJobIsRunning(self,job,jobopt=None,killjob=1,verb=0,incron=0,
                          nminWait=10,timesleep=5,rcPid=0,
                          # -- two types of joboptchk finding the jobopt string in prc or must be equal to jobopt
                          joboptchkType='find'):

        """20120209 -- set killjob=1, if both hit it at the same time, will be stuck"""

        curpid=os.getpid()

        def isRunning(job,jobopt,killjob,rcPid=0):

            pids=mf.LsPids()
            cpidOut=-999

            pids=mf.uniq(pids)
            pids.sort()

            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2]).strip()

                # -- uninteresting procs
                #
                if(mf.find(prc,'[') and mf.find(prc,']') or mf.find(prc,'/dev/tty') or mf.find(prc,'-tcsh') or mf.find(prc,'-bash') or
                   mf.find(prc,'/usr') or mf.find(prc,'vmhgfs') or
                   mf.find(prc,'sbin') or mf.find(prc,'automount') or mf.find(prc,'crond') or mf.find(prc,'sshd')): continue

                jobchk=mf.find(prc,job)

                if(verb): print 'M.chkIfJobIsRunning() jobchk ',jobchk,'prc:',prc,'job: ',job,jobopt
                if(jobopt != None):

                    # -- 20120326 new/better logic to check if exact job running
                    # -- 20131127 -- even better checks whole cmd line arg
                    #
                    if(jobchk):
                        try:
                            prcjobopt=prc.split()[2:]
                        except:
                            prcjobopt=None

                        if(prcjobopt != None):
                            prcjoboptS=''
                            for pp in prcjobopt:
                                prcjoboptS='%s %s'%(prcjoboptS,pp)

                        if(joboptchkType == 'find'): 
                            joboptchk=mf.find(prcjoboptS,jobopt)
                        else:
                            joboptchk=(prcjoboptS == jobopt)

                else:
                    joboptchk=1
                    

                if(jobchk and joboptchk and cpid != curpid):
                    #if(incron and not(mf.find(prc,'tcsh'))): continue
                    # -- bypass any proc with tcsh -- means in cron(?)
                    ctime=mf.dtg('curtime')
                    if(mf.find(prc,'tcsh') or mf.find(prc,'/bin/sh -c')): continue
                    print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid, prc: ',cpid,prc,' job,jobopt',job,jobopt
                    cpidOut=cpid
                    rc=rc+1

                    if(killjob == 1):
                        print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                        cmd="kill %s"%(curpid)
                        mf.runcmd(cmd,'quiet')
                    elif(killjob == -1):
                        print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                        cmd="kill %s"%(cpid)
                        mf.runcmd(cmd,'quiet')

            if(rc > 0 and rcPid): rc=cpidOut
            return(rc)



        def whoIsRunning(job,jobopt,killjob,rcPid=0):
            """ 
20210624 -- better version of isRunning because of switch to bash from tcsh
looks for all instances of the job first to set the code

"""

            pids=mf.LsPids()
            cpidOut=-999

            pids=mf.uniq(pids)
            pids.sort()
            
            runPids=[]
            # -- rc is the number of jobs
            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2]).strip()
                # -- look for non cron jobs
                if(mf.find(prc,job)):
                    if(mf.find(prc,'cron')): continue
                    runPids.append((prc,cpid))

            nrunPids=len(runPids)
            
            # -- if only one return 0 to not cycle
            #
            if(nrunPids == 1):
                (prc,cpid)= runPids[0]
                return(0)
                
            if(nrunPids > 1):

                jobchk=1
                (curprc,curpid)=runPids[-1]

                for (prc,cpid) in runPids:
                
                    if(jobopt != None):
                        try:
                            prcjobopt=prc.split()[2:]
                        except:
                            prcjobopt=None
    
                        if(prcjobopt != None):
                            prcjoboptS=''
                            for pp in prcjobopt:
                                prcjoboptS='%s %s'%(prcjoboptS,pp)
    
                            if(joboptchkType == 'find'): 
                                joboptchk=mf.find(prcjoboptS,jobopt)
                            else:
                                joboptchk=(prcjoboptS == jobopt)
                    else:
                        joboptchk=1
                        
                
                    if(jobchk and joboptchk and cpid != curpid):

                        ctime=mf.dtg('curtime')
                        print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid: ',cpid,' prc: ',prc,'job: ',job,'jobopt: ',jobopt
                        cpidOut=cpid
                        rc=rc+1
    
                        # -- do the killing inside whoIsRunning
                        #
                        if(killjob == 1):
                            print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                            cmd="kill %s"%(curpid)
                            mf.runcmd(cmd,'quiet')
                        elif(killjob == -1):
                            print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                            cmd="kill %s"%(cpid)
                            mf.runcmd(cmd,'quiet')

            if(rc > 0 and rcPid): rc=cpidOut
            
            return(rc)


        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(mf.find(osname,'posix'))):
            print 'WWW M.chkIfJobIsRunning is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        # -- check if *TWO* or more instances running, the first is the current, but that is checked above...
        #
        rc=whoIsRunning(job,jobopt,killjob,rcPid=rcPid)
        if(verb): print '111111111111111111111111111 rc whoIsRunning: ',rc,'job: ',job,'jobopt: ',jobopt,' killjob: ',killjob
        
        # -- only cycle if not killjob...
        #
        if(nminWait > 0 and not(killjob) and rc >= 1 ):
            nsleep=0
            rc=whoIsRunning(job,jobopt,killjob,rcPid=0)
            if(verb): print '22222222222222222222222222222222222222 rc whoIsRunning: ',rc
            print 'M.chkIfJobIsRunning -- cycling rc: ',rc,' curtime: ',mf.dtg('curtime')
            while(nsleep < (nmaxsleep-1) and rc >= 1 ):
                print 'SSSleeping in chkIfJobIsRunning nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep,' job,jobopt: ',job,jobopt
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfJobIsRunning...job:',job,'jobopt:',jobopt,'still running...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

                rc=isRunning(job,jobopt,killjob,rcPid=0)
                print 'M.chkIfJobIsRunning -- cycling rc: ',rc,' curtime: ',mf.dtg('curtime')

            rc=0


        return(rc)




    def chkIfFileIsOpen(self,path,verb=0,nminWait=10,timesleep=5):

        def isOpen(path,verb=0):

            if(not(self.GetPathSiz(path) > 0)):
                print 'WWW in chkIfFileIsOpen: ',path,' does not exist or is 0 length'
                return(0)

            rc=0
            openpids=[]
            cmd="lsof %s"%(path)
            lines=self.runcmdLog(cmd)
            if(len(lines[0]) > 0):

                if(verb):
                    olines=lines[1:-1]
                    olines=mf.uniq(olines)
                    for line in olines:
                        pid=line.split()[1]
                        openpids.append(pid)
                        print 'chkIfFileIsOpen: ',line

                rc=1

            return(rc,openpids)

        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(mf.find(osname,'posix'))):
            print 'WWW chkIfFileIsOpen is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        if(nminWait > 0 and isOpen(path,verb=verb) ):
            nsleep=0
            while(nsleep < (nmaxsleep-1) and isOpen(path,verb=verb) ):
                print 'SSSleeping in chkIfFileIsOpen nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfFileIsOpen...path: ',path,'still open...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

            rc=0

        else:
            rc=isOpen(path,verb=verb)
            if(verb): print 'chkIfFileIsOpen rc: ',rc

        return(rc)
    
    def loopCmd2(self,cmd,nLoop=5,sLoop=5,ropt='',verb=0):
        rc=mf.runcmd2(cmd,ropt=ropt)
        if(ropt != 'norun' and verb): print '0000-loopCmd2-rc: ',rc
    
        if(rc < 0): 
            print 'EEEE rsync error GGGEEETTTIING INVentory...retry for %d times sleeping %d seconds..'%(nLoop,sLoop)
            for n in range(0,nLoop):
                sleep(sLoop)
                rc=mf.runcmd2(cmd,ropt='')
                if(ropt != 'norun'): print '0000-runcmd2-rc: ',rc
                if(rc >= 0): 
                    return(rc)
        
        if(rc < 0):
            print 'bailing in loopCmd: ',cmd,'nLoop: ',nLoop,' sLoop: ',sLoop
            sys.exit()
        else:
            return(rc)





class DataSet(MFbase):

    from mfbase import ptmpBaseDir
    
    def __init__(self,
                 name='test',
                 version='0.1',
                 dtype='hash',
                 bdir=ptmpBaseDir,
                 unlink=0,
                 verb=0,
                 ):

        self.name=name
        self.version=version
        self.dtype=dtype
        self.bdir=bdir
        self.pyppath="%s/%s.pyp"%(self.bdir,self.name)
        if(unlink):
            try:
                os.unlink(self.pyppath)
            except:
                print 'WWW M.DataSet -- failed to unlink: ',self.pyppath
                
        self.data={}
        self.verb=verb

    def getPyp(self):

        if(self.verb):
            print 'M.DataSet(getPyp): pyppath: ',self.pyppath

        if(os.path.exists(self.pyppath)):
            if(self.verb):  print 'M.DataSet(getPyp): pyppath: ',self.pyppath
            try:
                PS=open(self.pyppath)
                FR=pickle.load(PS)
                PS.close()
                return(FR)
            except:
                print 'WWW M.DataSet.getPyp() error opening: ',self.pyppath,' returning None'
                return(None)

        else:
            return(None)


    def putPyp(self,override=0):


        if(mf.ChkDir(self.bdir,'mk') == -1): sys.exit()

        if(override and os.path.exists(self.pyppath)):
            os.unlink(self.pyppath)
            self.curtime=[]


        if(not(hasattr(self,'curtime'))):
            self.curtime=[]

        self.curtime.append(mf.dtg('dtg.phm'))

        try:
            if(self.verb):  print 'M.DataSet(putPyp): pyppath: ',self.pyppath
            PS=open(self.pyppath,'w')
            pickle.dump(self,PS)
            PS.close()
        except:
            print 'EEEEE unable to pickle.dump: ',self.pyppath
            sys.exit()


    def getData(self):

        return(self.data)



    def putData(self,key,value,verb=1,override=0):

        if(not(hasattr(self,'data'))):
            print 'IIII making data'
            self.data={}

        try:
            haskey=self.data.has_key(key)
        except:
            haskey=0

        try:
            lkey=len(self.data[key])
        except:
            lkey=0


        if(not(haskey) or override or ( lkey != len(value)) ):
            print 'PPPPP adding value to data[key]'
            self.data[key]=value

        else:
            if(verb):  print 'data for key: ',key,' already there'



class DataSets(DataSet):

    from mfbase import ptmpBaseDir

    def __init__(self,bdir=ptmpBaseDir,name='datasets',dtype='model',version='0.1',verb=0,backup=0,unlink=0,
                 unlinkWithRm=0,
                 docp1st=0,
                 doDSsWrite=0,
                 dowriteback=True,
                 doFileLock=0,
                 doMkdir=1,
                 warn=0,
                 chkifopen=0,nminWait=10):

        self.bdir=bdir
        self.name=name
        self.version=version
        self.dtype=dtype
        self.verb=verb
        self.docp1st=docp1st


        if(doDSsWrite and doMkdir):
            if(mf.ChkDir(bdir,'mk') == -1): 
                print 'M.Datasets - cannot mkdir bdir: ',bdir,'bailing...'
                sys.exit()
        else:
            if(not(mf.ChkDir(bdir,'quiet'))):
                print 'M.Datasets - doDSsWrite==0 bdir: ',bdir,'not there, bailing...'
                sys.exit()
                

        path=os.path.join(bdir,name)
        if(os.path.exists(path) and backup):
            cmd="cp %s %s.SAV"%(path,path)
            mf.runcmd(cmd,'')
        elif(os.path.exists(path) and unlink):
            try:
                if(unlinkWithRm):
                    print 'III(M.DataSets rm -v): ',path
                    mf.runcmd("rm -v %s"%(path),'')
                else:
                    # -- use .os to rm...
                    print 'III(M.DataSets unlinking): ',path
                    os.unlink(path)
            except:
                print 'III(M.DataSets unlinking): ',path,' failed because...'


        self.path=path
        self.pathCP=None

        from WxMAP2 import W2adminuSer,W2currentuSer,W2adminuSers

        if(self.docp1st):
            curpid=os.getpid()
            pathCP="%s-%d"%(path,curpid)
            cmd="cp %s %s"%(path,pathCP)
            mf.runcmd(cmd,'')
            path=pathCP
            self.pathCP=pathCP
            print "III M.Dataset.__init__() docp1st from: %s to: %s"%(self.path,self.pathCP) 

        if(chkifopen):
            MF=MFutils()
            rc=MF.chkIfFileIsOpen(path,nminWait=nminWait,verb=verb)

        isDSsThere=os.path.exists(path)

        if(not(isDSsThere) and not(doDSsWrite)):
            if(warn): print 'WWW M.Dataset.__init_() -- path: ',path,' not there do not create shelve...doDSsWrite = 0'
            return

        if( ( (W2currentuSer == W2adminuSer) or (W2currentuSer in W2adminuSers) )  and doDSsWrite):

            if(doFileLock):
                self.db=sopen(path,flag='c',writeback=dowriteback)
            else:
                self.db=shelve.open(path,writeback=dowriteback)

        else:
            self.db=shelve.open(path,'r')

        if(verb): print 'DataSets.dbpath: ',path
        self.dbpath=path

    def putDataSet(self,dataset,key,
                   unlinkException=0,
                   verb=0,
                   doDbSync=0,
                   ):

        if(not(hasattr(dataset,'curdtghms'))):
            dataset.curdtghms=[]

        dataset.curdtghms.append(mf.dtg('dtg.hms'))

        if(not(hasattr(self,'putKeys'))): self.putKeys=[]
        self.putKeys.append(key)

        try:
            self.db[key]=dataset
            if(doDbSync): self.db.sync()
            if(verb): print 'PPP putDataSet    putting key: ',key,'   to: %s/%s  dbsync: %d'%(self.bdir,self.name,doDbSync)
            return(0)
        except:
            if(unlinkException):
                print 'WWW killing ppath: ',self.dbpath,' on open/dump exception in putDataSet'
                os.unlink(self.dbpath)
            print 'PPP EEE(M.putDataSet() error in putting key: ',key,'   to: %s/%s'%(self.bdir,self.name)
            print 'PPP WWW press!'
            return(-1)


    def closeDataSet(self,verb=0,warn=0):
        #self.ls()
        
        if(hasattr(self,'db')):
            #self.db.sync()  -- not needed; done before close in shelve.py
            self.db.close()
            if(verb):
                print 'M.DataSets.closeDataSet() -- success'
        else:
            if(warn):
                print 'M.DataSets.closeDataSet() -- failed'

    def syncDataSet(self):
        if(hasattr(self,'db')):
            self.db.sync()     


    def getDataSet(self,key,override=0,verb=0,warn=1):

        if(override): return(None)

        try:
            self.db.has_key(key)
        except:
            if(warn): print 'EEE bad dataset in DataSets.getDataSet()...return None key: ',key
            return(None)

        if(self.db.has_key(key)):

            # return None if problem getting pyp from db...
            #pyp=self.db[key]
            #return(pyp)
            try:
                pyp=self.db[key]
                if(self.verb or verb): print 'GGG DataSets.getDataSet() getting key: ',key,' in: %s/%s'%(self.bdir,self.name)
            except:
                if(self.verb or verb): print 'EEE DataSets.getDataSet()     got key: ',key,' problem with unpickling in: %s/%s'%(self.bdir,self.name)
                pyp=None
            return(pyp)
        else:
            if(self.verb or verb): print 'GGG  DataSets.getDataSet()  NNNOOO key: ',key,' in: %s/%s'%(self.bdir,self.name)
            return(None)

    def lsKeys(self):

        kk=self.db.keys()
        kk.sort()
        for k in kk:
            print 'key: ',k

    def getKeys(self):

        kk=self.db.keys()
        kk.sort()
        return(kk)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# runGrads

class runGrads(MFutils):


    gradscmd='''grads -Hlc'''


    def __init__(self,files,gsprc='',verb=0,filetype=''):

        if(type(files) != ListType): files=[files]

        print 'files: ',files
        gs="""function main(args)
# prelims:

rc=gsfallow('on')
rc=const()"""

        gaopencmd='open'
        if(filetype == 'xdf'): gaopencmd='xdfopen'
        if(filetype == 'sdf'): gaopencmd='sdfopen'

        for file in files:
            gs="""%s
print 'opening: %s'
'%s %s'
"""%(gs,file,gaopencmd,file)

        gs="""%s
%s
"""%(gs,gsprc)


        gspath='/tmp/runGrads.gs'
        self.WriteString2File(gs,gspath)
        cmd='''%s "%s" -g 1024x768-30'''%(self.gradscmd,gspath)
        os.system(cmd)







#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline

class CmdLine(MFutils):

    def __init__(self,argv=sys.argv):

        self.argv=argv

        self.argopts={
            'dtgopt': 'no default',
            'model': 'no default',
        }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'source':['S:','rtfim','a','source'],
        }

        self.defaults={
            'zy0x1w2':0,
            'zy0x1w2y3':'test'
        }

        self.purpose='''
purpose -- to boldly go, where no man has gone before!'''

        self.examples='''
%s test
'''




    def initDoc(self):

        argdoc="%s "

        optdoc='''
plain args:'''
        for n in range(1,len(self.argopts)+1):
            key=self.argopts[n][0]
            val=self.argopts[n][1]
            argdoc="%s %s"%(argdoc,key)
            optdoc=optdoc+'''
  %-20s - %s'''%(key,val)



        argdoc=argdoc+' ['
        optdoc=optdoc+'''

switches:'''
        kk=self.options.keys()
        kk.sort()
        for k in kk:
            oo=self.options[k]
            argdoc="%s -%s"%(argdoc,oo[0][0])
            optdoc=optdoc+'''
  -%1s :: %s=[%s] %s'''%(oo[0][0],k,oo[1],oo[3])


        argdoc=argdoc+' ]'

        exampledoc="""
Example(s):%s"""%(self.examples)

        purposedoc="""
Purpose:%s"""%(self.purpose)

        self.__doc__="""%s
%s
%s
%s
"""%(argdoc,optdoc,purposedoc,exampledoc)



    def initFlagOpts(self):

        self.flagOpts=''
        vv=self.options.values()
        for v in vv:
            self.flagOpts=self.flagOpts+v[0]


    def initArgOpts(self):

        narg=len(self.argopts)

        if(narg == 0):
            estr="self.istart=%d"%(narg+1)
            exec(estr)
            return

        for n in range(1,narg+1):

            key=self.argopts[n][0]
            val=self.argopts[n][1]

            if(n == 1):
                estr="self.%s=self.argv[%d]"%(key,n)
                exec(estr)
                estr="self.istart=%d"%(n+1)
                exec(estr)
            else:
                exec("if(self.narg > %d): self.%s=self.argv[%d]"%(n-1,key,n))
                exec("self.istart=%d"%(n+1))


    def getFlagOpts(self):

        self.foptions={}
        for o, a in self.opts:
            for k in self.options.keys():
                oo=self.options[k]
                if(o == "-%s"%(oo[0][0])):
                    if(oo[2] == 'a'):
                        self.foptions[k]=a
                    elif(oo[2] == 'i'):
                        self.foptions[k]=int(a)
                    elif(oo[2] == 'f'):
                        self.foptions[k]=float(a)
                    else:
                        self.foptions[k]=oo[2]

        for k in self.options.keys():
            if(not(self.foptions.has_key(k))):
                self.foptions[k]=self.options[k][1]


    def setFlagOpts(self):

        self.estrFlag=''
        for k in self.foptions.keys():
            if(type(self.foptions[k]) == StringType):
                estr="%s='%s'"%(k,self.foptions[k])
            elif(type(self.foptions[k]) == IntType):
                estr="%s=%d"%(k,self.foptions[k])
            elif(type(self.foptions[k]) == FloatType):
                estr="%s=%g"%(k,self.foptions[k])
            elif(self.foptions[k] == None):
                estr="%s=None"%(k)
            else:
                print 'EEE invalid option in ',__class__
                sys.exit()
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrFlag="%s%s\n"""%(self.estrFlag,estr)


    def setArgOpts(self):

        self.estrArg=''
        istart=1
        for n in range(1,len(self.argopts)+1):
            key=self.argopts[n][0]
            try:
                exec("kk=self.%s"%(key))
            except:
                print "!!!!"
                print "!!!!EEE CmdLine.setArgOpts: need to set the plain arg n: ",n,' key: ',key,' !!!!'
                print "!!!!"
                mf.usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                sys.exit()
            estr="%s='%s'"%(key,kk)
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrArg="%s%s\n"""%(self.estrArg,estr)


    def setDefaults(self):

        self.estrDefaults=''
        try:
            self.defaults.keys()
        except:
            return
        for k in self.defaults.keys():
            if(type(self.defaults[k]) == StringType):
                estr="%s='%s'"%(k,self.defaults[k])
            elif(type(self.defaults[k]) == IntType):
                estr="%s=%d"%(k,self.defaults[k])
            elif(type(self.defaults[k]) == FloatType):
                estr="%s=%g"%(k,self.defaults[k])
            elif(self.defaults[k] == None):
                estr="%s=None"%(k)
            else:
                print 'EEE invalid option in ',__class__
                sys.exit()
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrDefaults="%s%s\n"""%(self.estrDefaults,estr)

    def CmdLine(self,blankPlainArgs=0):

        self.blankPlainArgs=blankPlainArgs

        self.initFlagOpts()
        self.initDoc()

        self.curpid=os.getpid()
        self.curdtg=mf.dtg()
        self.curphr=mf.dtg('phr')
        self.curdir=os.getcwd()
        self.curyear=self.curdtg[0:4]
        self.curtime=mf.dtg('curtime')

        (self.tttdtg,self.curphr)=mf.dtg_phr_command_prc(self.curdtg) 

        self.pypath=self.argv[0]
        self.abspypath=os.path.abspath(self.pypath)
        (self.pydir,self.pyfile)=os.path.split(self.abspypath)

        self.estrCur="""curdtg='%s'\ncurphr='%s'\ncuryear='%s'\ncurtime='%s'\ncurdir='%s'\n"""%(self.curdtg,
                                                                                                self.curphr,
                                                                                                self.curyear,
                                                                                                self.curtime,
                                                                                                self.curdir,
                                                                                                )

        self.estrCur="""%s\npydir='%s'\npypath='%s'\npyfile='%s'\n"""%(self.estrCur,self.pydir,self.pypath,self.pyfile)

        gspath=os.path.abspath(self.pypath)
        (base,ext)=os.path.splitext(gspath)
        self.gspath=base+'.gs'

        self.narg=len(self.argv)-1

        if(self.narg >= 1 and not(self.blankPlainArgs)):

            self.initArgOpts()

            try:
                (self.opts, self.args) = getopt.getopt(self.argv[self.istart:], self.flagOpts)

            except getopt.GetoptError, e:
                mf.usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                print
                print "EEE"
                print """EEE invalid getopt opt error: '%s'"""%(e)
                print "EEE"
                print
                sys.exit(2)

            self.getFlagOpts()
            self.setFlagOpts()
            self.setArgOpts()
            self.setDefaults()
            self.estr=self.estrFlag+self.estrDefaults+self.estrArg+self.estrCur



        # -- 20111023 -- tried allowing blank plain args -- need to rewrite the whole section
        #

        elif(self.blankPlainArgs):


            self.initArgOpts()

            try:
                (self.opts, self.args) = getopt.getopt(self.argv[self.istart:], self.flagOpts)

            except getopt.GetoptError:
                mf.usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                print "EEE invalid getopt opt"
                sys.exit(2)


            self.getFlagOpts()
            self.setFlagOpts()
            self.setArgOpts()
            self.setDefaults()
            self.nargsFlag=len(self.opts)

            print '0000000000000000000 ',self.narg,self.nargsFlag
            print '1111111111111111111 ',self.estrArg
            print '2222222222222222222 ',self.opts,self.args
            print '3333333333333333333 ',self.nargsFlag,self.estrFlag,self
            print '4444444444444444444 ',self.estrCur
            print '5555555555555555555 ',self.estrDefaults
            self.estr=self.estrFlag+self.estrDefaults+self.estrArg+self.estrCur


        else:
            mf.usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
            sys.exit(1)


if (__name__ == "__main__"):

#    import base64
    MF=MFutils()
    
#    subject='test from MFutils.py'
#    message="""this is only a test
#if this had been a real emergency, you'd be sayoonara ogenki de!!!
#please reply if you copy, over...
#"""
#    toWhomList=['curtis.alexander@noaa.gov','michael.fiorino@noaa.gov']
#    MF.sendEmail(toWhomList,subject,message)
    #ds=DataSets()
    #ds.ls()
    sys.exit()




