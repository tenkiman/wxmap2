#base configuration here

W2Center='esrl.kaze'
W2='/data/amb/users/fiorino/w21'


#------------------------------------------ don't need change below
# - from M.py ...
from subprocess import Popen, PIPE, STDOUT
import os,sys,glob,time,getopt,copy,getpass,struct
import inspect
import shelve
import cPickle as pickle
from socket import gethostname
import datetime

from time import time as timer
from time import sleep,mktime
from types import StringType,IntType,FloatType,ListType,DictType,TupleType
from math import atan2,atan,pi,fabs,cos,sin,log,tan,acos,sqrt
import array


class MFbase():

    def find(self,mystr,pattern):
        rc=0
        if(mystr.find(pattern) != -1): rc=1
        return(rc)


    def ls(self,findstr=None,lsopt=None,maxchar=116,varsonly=0):

        methods=[]
        variables=[]
        clss=[]
        nvar=0

        mlen=28

        mformat="MMM: %%-%ds: %%s"%(mlen)
        cformat="CCC: %%-%ds: %%s"%(mlen)
        vformat="VVV(%%3d): %%-%ds: %%s"%(mlen)
        dd=inspect.getmembers(self)
        dd.sort()
        for d in dd:
            name=d[0]
            if(findstr != None):
                if(not(self.find(name,findstr))): continue
                
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
            

            if(self.find(val,'<bound method') or self.find(val,'<module ')):
                methods.append(mformat%(name[0:mlen],val[0:maxchar]))
            elif(self.find(val,'instance at')):
                clss.append(cformat%(name[0:mlen],val[0:maxchar]))
            else:
                variables.append(vformat%(nvar,name[0:mlen],val))
                nvar=nvar+1

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


    def getPyp(self,pyppath=None,unlink=0,verb=0):

        if(pyppath == None and self.pyppath == None):
            ppath='/tmp/zy0x1w2.pyp'
        else:
            if(hasattr(self,'pyppath')):
                ppath=self.pyppath
            elif(pyppath != None):
                ppath=pyppath
            else:
                print 'EEE unable to open either pyppath: ',pyppath,' or self.pyppath: ',self.pyppath
                return

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

        if(pyppath == None and self.pyppath == None):
            ppath='/tmp/zy0x1w2.pyp'
        else:
            if(hasattr(self,'pyppath')):
                ppath=self.pyppath
            elif(pyppath != None):
                ppath=pyppath
            else:
                print 'EEE unable to open either pyppath: ',pyppath,' or self.pyppath: ',self.pyppath
                return

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

        self.curdtg=dtg()
        self.curphr=dtg('phr')
        self.curyear=self.curdtg[0:4]

        if(not(hasattr(self,'curtime'))):  self.curtime=[]

        self.curtime.append(dtg('dtg.phms'))



    def sTimer(self,tag='notag'):

        if(not(hasattr(self,'stimers'))):    self.stimers={}
        value=timer()
        self.loadDictList(self.stimers,tag,value)
        
    def dTimer(self,tag='notag'):
        
        phms=dtg('dtg.phms')
        if(hasattr(self,'stimers')):
            value=time.time()-self.stimers[tag][-1]

        print "TTTTTTTTTTTTTTTTTTTTTTT-------------------timer: %-40s: %6.3f      at: %s"%(tag,value,phms)


    def sTime(self,tag='notag'):

        if(not(hasattr(self,'stimes'))):    self.stimes={}
        value=timer()
        self.loadDictList(self.stimes,tag,value)
        

    def dTime(self,tag='notag'):
        
        if(not(hasattr(self,'curdtimes'))):
            self.curdtimes={}
        else:
            if( type(self.curdtimes) is not(DictType) ): self.curdtimes={}
            
        value=dtg('dtg.phms')
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

    def nDayYear(self,yyyy):
        nd=365
        if (int(yyyy)%4 == 0): nd=366
        return(nd)

    def nDayMonth(self,yyyymm):
        yyyy=string.atoi(yyyymm[0:4])
        mm=string.atoi(yyyymm[4:6])

        leap=0
        if (yyyy%4 == 0): leap=1

        #
        # override leaping if 365 day calendar
        #
        if(calendar == '365day'): leap=0

        if(leap):
            return(mdayleap[mm])
        else:
            return(mday[mm])


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


    def PathCreateTimeDtgdiff(self,dtg,path):

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
        

    def ChkDir(self,dir,diropt='verb'):

        if (not(os.path.isdir(dir))) :
            if(diropt != 'quiet'): print "dir  (not there): ",dir
            if(diropt == 'mk' or diropt == 'mkdir'):
                try:
                    os.system('mkdir -p %s'%(dir))
                except:
                    print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                    return(-1)
                print 'dir     (MADE): ',dir
                return(2)
            else:
                return(0)
        else:
            if(diropt == 'verb'):
                print "dir      (there): ",dir
            return(1)

    def ChangeDir(self,dir,verb=1):

        try:
            os.chdir(dir)
            if(verb == 1): print 'cd---> ',dir
            return(1)
        except:
            if(verb != -1): print 'WWW unable to cd to: ',dir
            return(0)



    def ChkPath(self,path,pathopt='noexit',verb=1):

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
        ndy1=self.nDayYear(y1)
        jday1=self.Dtg2JulianDay(ymd1)
        (hh1,mm1,ss1)=dtghms1.split()[1].split(':')
        ymdh1=(float(y1)*float(ndy1) + float(jday1))*24.0 + int(hh1) + int(mm1)/60.0 + int(ss1)/3600.0
        #print '11111111111 ',ymd1,hh1,mm1,ss1,ymdh1

        ymd2=dtghms2.split()[0]
        y2=ymd2[0:4]
        ndy2=self.nDayYear(y2)
        jday2=self.Dtg2JulianDay(ymd2)
        (hh2,mm2,ss2)=dtghms2.split()[1].split(':')
        ymdh2=(float(y2)*float(ndy2) + float(jday2))*24.0+int(hh2)+int(mm2)/60.0 + int(ss2)/3600.0
        #print '22222222222 ',ymd2,hh2,mm2,ss2,ymdh2
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



        card=''
        nend=len(dtgs)
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
            

    def uniqDictList(self,dict):

        kk=dict.keys()

        for k in kk:
            list=dict[k]
            list=self.uniq(list)
            dict[k]=list


    def uniqDictDict(self,dict):
        """ uniq a dict of dicts"""
        kk=dict.keys()

        for k in kk:
            dict2=dict[k]
            kk2=dict2.keys()
            self.uniqDictList(dict2)
            dict[k]=dict2



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


    def PrintDict(self,dict,name='dict'):

        cards=[]
        kk=dict.keys()
        kk.sort()
        nh=len(dict)

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
            print "EEE unable to open: %s"%(path)
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
            print "EEE unable to open path: %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        for card in list:
            card=card.rstrip()+'\n'
            c.writelines(card)
        c.close()
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



    def runcmdLog(self,cmd,ropt=''):

        if(ropt == 'norun'):
            print "CCC(runcmdLog): %s"%(cmd)
            return([])
        else:
            p=Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.read()
            lines=output.split('\n')

        return(lines)



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



    def get0012fromDtgs(self,dtgs):

        odtgs=[]
        for dtg in dtgs:
            hh=int(dtg[8:10])
            if(hh == 12 or hh == 0): odtgs.append(dtg)

        return(odtgs)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc classes to make .files and tcsh script to run cron

class W2localrc(MFbase):

    def __init__(self):


        self.dotpath='../.w2localrc'
        self.dotfile="""
#setenv NIO_GRIB2_CODETABLES /lfs0/projects/fim/whitaker/lib/python2.5/site-packages/PyNIO/ncarg/grib2_codetables/

echo "setting ld_library_path in .w2localrc"

setenv GALIBD "$W2_GRADS_BDIR/lib"
if ( $?LD_LIBRARY_PATH ) then
   setenv LD_LIBRARY_PATH .:"$LD_LIBRARY_PATH":"$GALIBD":"$W2_BDIRLIB":"$W2_BDIRDB3LIB"
   setenv LD_LIBRARY_PATH .:"$LD_LIBRARY_PATH":"$GALIBD":"$W2_BDIRAPPLIB"
else
   setenv LD_LIBRARY_PATH .:"$W2_BDIRLIB":"$GALIBD":"$W2_BDIRDB3LIB"
endif

exit

#source .w2pgirc
#
# add local paths...
#
#set localpath = ( \
#                ~/prc \
#                /opt/linux/bin \
#		)
#set path = ( \
#		$path \
#		$localpath \
#)
"""



class W2rc(MFbase):

    def __init__(self):


        self.dotpath='../.w2rc'
        self.dotfile='''
setenv W2CENTER '%s'
setenv W2 '%s'
setenv HOSTNAMESHORT `hostname|awk -F. '{ print tolower($1) }'`
setenv HOSTOSLOWER `uname|awk '{ print tolower($1) }'`
setenv HOSTOSUPPER `uname|awk '{ print toupper($1) }'`

setenv W2_BDIR "$W2"
setenv W2_BDIRDAT "$W2/dat"
setenv W2_BDIRAPP "$W2/app"
setenv W2_BDIRBIN "$W2/bin"
setenv W2_BDIRAPPLIB "$W2/app/lib"
#setenv W2_BDIRDB3LIB "$W2/app/lib/db4.8/lib"
#setenv W2_BDIRDB3LIB "$W2/app/db4.8/lib"
setenv W2_BDIRDB5LIB "$W2/app/db5.0/lib"
setenv W2_BDIRLIB "$W2/lib"
setenv W2_BDIRPLT "$W2/plt"
setenv W2_BDIRWEB "$W2/web"
setenv W2_BDIRWEBA "$W2/weba"
setenv W2_BDIREVT "$W2/evt"
setenv W2_BDIRLOG "$W2/log"

setenv W2_SRC_DIR  "$W2_BDIR/src"
setenv W2_PRC_DIR  "$W2_BDIR/prc"
setenv W2_PERL_DIR "$W2_PRC_DIR/lib/perl"
setenv W2_PY_DIR   "$W2_PRC_DIR/lib/python"

setenv W2_GRADS_BDIR "$W2_BDIRAPP/grads"
setenv W2_GRADS1_BDIR "$W2_BDIRAPP/opengrads1.10"
setenv W2_GRADS2_BDIR "$W2_BDIRAPP/opengrads2.0"

# wgrib1 table
#
setenv GRIBTAB "$W2_BDIRLIB/wgrib/w2.wgrib1.var.table.txt"

# ecmwf bufr
#
setenv BUFR_TABLES "$W2_BDIRLIB/bufrtables/"

# gacvs
#
setenv CVS_RSH ssh

# python
#
setenv PYTHONSTARTUP "$W2_BDIR/.pythonrc"
setenv PYTHONPATH "$W2_PRC_DIR/lib/python"

# perl
#
#setenv PERL5LIB "$W2_BDIRAPP/perl/lib/5.8.5"

if ( $?prompt ) then      # if this is an interactive shell...
source .w2alias
endif

# grads
#
setenv GADDIR "$W2_GRADS_BDIR/data"
setenv GASCRP "$W2_GRADS_BDIR/gslib"
setenv GA1UDXT "$W2_GRADS1_BDIR/bin/gex/udxt"
setenv GA2UDXT "$W2_GRADS2_BDIR/bin/gex/udxt"

# library path for pgf77 application that does cliper via python w2.tc.cliper.py
# dependency needs to be removed... couldn't get f2py to build via g95... 

# ************* LOCAL USER PATH
set lpath = ( \\
                "$W2_BDIRBIN" \
                "$W2_GRADS_BDIR/util" \\
                "$W2_GRADS1_BDIR/bin" \\
                "$W2_GRADS2_BDIR/bin" \\
                "$W2_BDIRAPP/python/bin" \\
                "$W2_BDIRAPP/perl/bin" \\
                "$W2_BDIRAPP/bin" \\
#                "/opt/local/bin" \\
                "/opt/CollabNet_Subversion/bin" \\
                "/usr/local/bin" \\
		)


# *************  PROJECT PATHS
set projectpath = ( \\
                    "$W2_BDIR/prc/wxmap2" \\
                    "$W2_BDIR/prc/flddat" \\
		    "$W2_BDIR/prc/tcdat" \\
                    "$W2_BDIR/prc/util" \\
		    )

set path = ( \\
		. \\
		$lpath \\
		$projectpath \\
		$path \\
#		$adminpath \\
)		

if ( -e .w2localrc ) then
   echo "loading local config rc .w2localrc"
   source .w2localrc
endif

if ( $?prompt ) then      # if this is an interactive shell...
fixprompt
endif
'''%(W2Center,W2)


class W2crontcsh(MFbase):

    def __init__(self):


        self.tcshpath='../run.cron.tcsh'
        self.tcshfile='''
#!/usr/bin/env tcsh
#
#       96110100 -- changed this to tcsh after all the mucking around with .cshrc
#
#       set the environment
#
cd %s
source .w2rc 
echo "Executing run.crontab.tcsh"
echo "************************************"
echo "*"
echo "QQQQQ: START $1 at "`date`" on "`hostname`
echo "*"
echo "************************************"
$1
echo "************************************"
echo "*"
echo "QQQQQ:  END $1 at "`date`" on "`hostname`
echo "*"
echo "************************************"
exit'''%(W2)


if (__name__ == "__main__"):

    MF=MFutils()
    rc=W2localrc()
    rc.ls()
    rc=W2rc()
    rc.ls()
    #MF.WriteString2File(rc.dotfile,rc.dotpath
    rc=W2crontcsh()
    rc.ls()

    

        
