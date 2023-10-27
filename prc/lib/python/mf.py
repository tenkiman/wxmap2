from mfbase import *

#class mfenv:

    #era = {
        #'6hdir':'/dat1/reanal/ecmwf/era40/6h/monitor',
        #'exp':'012.e4',
        #'expnum':'012',
    #}

    #tc = {
        #'dat.jtwc':'/dat/nwp/dat/tc/jtwc',
        #'prcclimo':'/home/fiorino/era/tc/prc/tcclimo',
        #'prc':'/home/fiorino/era/tc/prc/tctrack',
        #'prc.struct':'/home/fiorino/era/tc/prc/tcstruct',
    #}


#from time import *
#from math import *
#from math import atan2

#pi=4.0*atan2(1.0,1.0)
#pi4=pi/4.0
#pi2=pi/2.0
##
## wmo gravity
##
#gravity=9.8065
#deg2rad=pi/180.0
#rad2deg=1.0/deg2rad
#rearth=6371.0
#km2nm=60.0/(2*pi*rearth/360.0)
#nm2km=1.0/km2nm
#knots2ms=1000/(km2nm*3600)
#ms2knots=1/knots2ms
#units='metric'


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

mname3 = {
'01':'Jan',
'02':'Feb',
'03':'Mar',
'04':'Apr',
'05':'May',
'06':'Jun',
'07':'Jul',
'08':'Aug',
'09':'Sep',
'10':'Oct',
'11':'Nov',
'12':'Dec'
}

cname3 = {
'JAN':'01',
'FEB':'02',
'MAR':'03',
'APR':'04',
'MAY':'05',
'JUN':'06',
'JUL':'07',
'AUG':'08',
'SEP':'09',
'OCT':'10',
'NOV':'11',
'DEC':'12'
}



#
#  add 0 for indexing by month vice month-1
#
mday=(0,31,28,31,30,31,30,31,31,30,31,30,31)
mdayleap=(0,31,29,31,30,31,30,31,31,30,31,30,31)
aday=(1,32,60,91,121,152,182,213,244,274,305,335)
adayleap=(1,32,61,92,122,153,183,214,245,275,306,336)


sec2hr=1/3600.0

def ndayyr(yyyy):
    nd=365
    if (int(yyyy)%4 == 0): nd=366
    return(nd)

def ndaymo(yyyymm):
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


def TimeZoneName():

    import time
    tz=time.tzname
    tz=tz[time.daylight]
    return(tz)


def Dtg2JulianDay(dtg):

    import time
    year=int(str(dtg)[0:4])
    month=int(str(dtg)[4:6])
    day=int(str(dtg)[6:8])

    t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
    jday=time.gmtime(t)[7]
    jday="%03d"%(int(jday))
    return (jday)

def YearJulianDay2YMD(year,jday):

    from datetime import date,timedelta
    ymd=date(int(str(year)),1,1) + timedelta(int(str(jday))-1)
    ymd=ymd.strftime("%Y%m%d")
    return(ymd)



def dtg6(opt="default"):

    import time
    tzname=" %s "%(TimeZoneName())

    if (opt == "curtime" or opt == "curtimeonly" ):t=time.localtime(time.time())
    else:t=time.gmtime(time.time())

    yr="%04d" % t[0]
    mo="%02d" % t[1]
    dy="%02d" % t[2]
    hr="%02d" % t[3]
    fhr="%02d" % (int(t[3]/6)*6)
    mn="%02d" % t[4]
    sc="%02d" % t[5]

    if opt == "default":
        dtg=yr + mo + dy + fhr
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif (opt == "timeonly"):
        dtg=hr+":"+mn+":"+sc+ " UTC "
    elif (opt == "time"):
        dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtime"):
        dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
    else:
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

    return(dtg)

def dtg(opt="default"):

    import time
    
    from datetime import datetime
    from dateutil import tz
    
    tzname=" %s "%(TimeZoneName())
    
    from_zone = tz.gettz('UTC')
    to_zone   = tz.gettz('America/Denver')

    if (opt == "curtime" or opt == "curtimeonly" or opt == 'cur_hms'):
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
    elif opt == "cur.hm":
        dtg=yr + mo + dy + " " + hr + ":" + mn
    elif opt == "dtg.phm":
        cphr="%02d"%(phr)
        dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn
    elif opt == "dtg.phms":
        cphr="%02d"%(phr)
        dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn + ":" + sc
    elif opt == "dtgmn":
        dtg=yr + mo + dy +  hr + mn
    elif opt == "dtg_mn":
        dtg=yr + mo + dy +  hr + '_%s'%(mn)
    elif opt == "dtg_ms":
        dtg=yr + mo + dy +  hr + "_%s_%s"%(mn,sc)
    elif opt == "dtg_hms":
        dtg=yr + mo + dy + "_%s_%s_%s"%(hr,mn,sc)
    elif opt == "cur_hms":
        dtg="  ---> CurDT: " + yr + mo + dy + " %s:%s:%s <---"%(hr,mn,sc)
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

def dtg12(opt="default"):
    import time
    tzname=" %s "%(TimeZoneName())

    if (opt == "curtime" or opt == "curtimeonly" ):t=time.localtime(time.time())
    else:t=time.gmtime(time.time())

    yr="%04d" % t[0]
    mo="%02d" % t[1]
    dy="%02d" % t[2]
    hr="%02d" % t[3]
    fhr="%02d" % (int(t[3]/12)*12)
    phr=int(t[3])%12
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


def isRealTime(tdtgs,age=72.0):
    curdtg=dtg()
    alldtgs=tdtgs
    if(type(tdtgs) != ListType): alldtgs=[tdtgs]
    
    rc=1
    for tdtg in alldtgs:
        dtgd=dtgdiff(tdtg,curdtg)
        if(dtgd > age): 
            rc=0
            break
        
    return(rc)
    

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



def yyyymmrange(byyyymm,eyyyymm,inc=1):

    yyyymms=[]

    byyyymm=str(byyyymm)
    eyyyymm=str(eyyyymm)

    yyyymm=byyyymm

    while(yyyymm<=eyyyymm):
        yyyymms.append(yyyymm)
        yyyymm=yyyymminc(yyyymm,inc)


    return(yyyymms)

def yyyyrange(byyyy,eyyyy,inc=1):

    yyyys=[]

    byyyy=str(byyyy)
    eyyyy=str(eyyyy)

    yyyy=byyyy

    while(yyyy<=eyyyy):
        yyyys.append(yyyy)
        yyyy=yyyyinc(yyyy,inc)

    return(yyyys)



def yyyymmdiff(yyyymm1,yyyymm2):

    yyyy1=int(yyyymm1[0:4])
    yyyy2=int(yyyymm2[0:4])
    mm1=int(yyyymm1[4:6])
    mm2=int(yyyymm2[4:6])
    dyyyy=yyyy2-yyyy1
    dmm=mm2-mm1+1

    dyyyymm=(dyyyy*12)+dmm

    return(dyyyymm)


def yyyymminc(yyyymm,inc=1):
    yyyy=int(yyyymm[0:4])
    mm=int(yyyymm[4:6])
    mm=mm+inc
    if mm > 12:
        mm=mm-12
        yyyy=yyyy+1
    if mm < 1:
        mm=mm+12
        yyyy=yyyy-1

    nyyyymm="%04d%02d"%(yyyy,mm)
    return(nyyyymm)

def yyyyinc(yyyy,inc):

    yyyy=int(yyyy)

    nyyyy=yyyy+inc

    nyyyy="%04d"%(nyyyy)
    return(nyyyy)

def IsLeapYear(yyyy):
    rc=0
    if(yyyy%4 == 0 and (yyyy%100 != 0) or (yyyy%400 == 0)):
        rc=1
    return(rc)


def dtginc(idtg,off):

    dtg=str(idtg)
    
    if(len(dtg) == 10):
        yr=int(dtg[0:4])    
        mo=int(dtg[4:6])
        dy=int(dtg[6:8])
        hr=int(dtg[8:10])
    elif(len(dtg) == 11):
        yr=int(dtg[0:5])    
        mo=int(dtg[5:7])
        dy=int(dtg[7:9])
        hr=int(dtg[9:11])
        
    hr=hr+int(off)

    #
    # do leap if going forward in time
    #

    leap=0

    #200201120
    # problem, limit backward offset
    #
    if (IsLeapYear(yr) and off > -120): leap=1

    #
    # turn off leap of 365 day calendar
    #
    if(calendar == '365day'): leap=0

    ndyyr=365+leap

    jdy=dy-1

    ada=aday[mo-1]
    if leap == 1:ada=adayleap[mo-1];
    jdy=jdy+ada

    while hr >= 24:
        hr=hr-24
        jdy=jdy+1

    while hr < 0:
        hr=hr+24
        jdy=jdy-1

    if jdy <= 0:
        yr=yr-1
        leap=0
        if(IsLeapYear(yr)):
            leap=1
            ndyyr=366
            if(calendar == '365day'):
                leap=0
                ndyyr=365
        else:
            ndyyr=365

        jdy=jdy+ndyyr

    if jdy > ndyyr:
        jdy=jdy-ndyyr
        yr=yr+1
        leap=0
        if(IsLeapYear(yr)):
            leap=1
            ndyyr=366
            if(calendar == '365day'):
                leap=0
                ndyyr=365
        else:
            ndyyr=365

    if(calendar == '365day'): leap=0

    i=11
    if leap == 1:
        while(jdy<adayleap[i]):i=i-1
        ndy=jdy-adayleap[i]+1
    else:
        while(jdy<aday[i]):i=i-1
        ndy=jdy-aday[i]+1

    yr="%04d"%yr
    mo="%02d"%(i+1)
    dy="%02d"%ndy
    hr="%02d"%hr

    ndtg=yr+mo+dy+hr

    return(ndtg)

def dtg2time(dtg):


    cdtg=str(dtg)

    try:
        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])

        ct=(yy,mm,dd,hh,0,0,0,0,0)
        time=mktime(ct)
    except:
        print 'mf.dtg2time: invalid dtg: ',dtg,' sayoonara'
        sys.exit()

    return(time)

def dtgmn2time(dtg):

    from time import mktime 

    cdtg=str(dtg)

    yy=int(cdtg[0:4])
    mm=int(cdtg[4:6])
    dd=int(cdtg[6:8])
    hh=int(cdtg[8:10])
    mn=int(cdtg[10:12])

    ct=(yy,mm,dd,hh,mn,0,0,0,0)
    time=mktime(ct)
    return(time)


def dtgdiff(dtg1,dtg2):

    #from time import *

    dtg1=str(dtg1)
    dtg2=str(dtg2)

    yyyy1=int(dtg1[0:4])
    yyyy2=int(dtg2[0:4])

    offyear=1981
    if(yyyy1%4==0):
        offyear=1980
    if(yyyy2%4==0):
        offyear=1979

    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtg1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

    t1=dtg2time(dtg1)
    t2=dtg2time(dtg2)
    nhr=(t2-t1)*sec2hr

    return(nhr)

def dtgmndiff(dtgmn1,dtgmn2):

    #from time import *

    dtgmn1=str(dtgmn1)
    dtgmn2=str(dtgmn2)

    yyyy1=int(dtgmn1[0:4])
    yyyy2=int(dtgmn2[0:4])

    offyear=1981
    if(yyyy1%4==0):
        offyear=1980
    if(yyyy2%4==0):
        offyear=1979

    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtgmn1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtgmn2[4:10]

    t1=dtgmn2time(dtgmn1)
    t2=dtgmn2time(dtgmn2)
    nhr=(t2-t1)*sec2hr

    return(nhr)


def dtgShift0012(dtg,round=1):

    bstart=8
    if(len(dtg) == 11): bstart=9
    
    if(round):
        if(dtg[bstart:] == '06' or dtg[bstart:] == '18'):
            odtg=dtginc(dtg,6)
        else:
            odtg=dtg
    else:
        if(dtg[bstart:] == '06' or dtg[bstart:] == '18'):
            odtg=dtginc(dtg,-6)
        else:
            odtg=dtg

    return(odtg)


def dtgrange(dtg1,dtg2,inc=6):

    verb=0

    inc=int(inc)
    dtg1=str(dtg1)
    dtg2=str(dtg2)

    if(verb): print 'ddd dtgrange',dtg1,dtg2,inc

    if(inc > 0 and dtg2 < dtg1 and inc > 0):
        print "EEE invalid edtg (before bdtg) in mf.dtgrange: dtg1: %s  dtg2: %s"%(dtg1,dtg2)
        sys.exit()

#
# return dtg1 if dtg1=dtg2
#
    if(dtg1 == dtg2):
        dtgs=[dtg1]
        return(dtgs)

#
# pre 1970? problem
#
    dtg1off=0

    yyyy1=int(dtg1[0:4])
    yyyy2=int(dtg2[0:4])

    offyear=1981
    #
    # 20031114 fix problem when begin/end year are the same
    #
    if(yyyy1%4 == 0 and yyyy2%4 == 0):
        offyear=1980
    if(yyyy2%4 == 0 and yyyy1%4 != 0):
        offyear=1979

    if(verb): print 'aaa ',yyyy1,yyyy2,yyyy1%4,yyyy2%4,offyear
    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(verb): print 'bbb ',dtg1,dtg2,yyyy1,yyyy2,offyear
    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtg1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

    t1=dtg2time(dtg1)
    t2=dtg2time(dtg2)


    nhr=(t2-t1)*sec2hr
    dtgs=[]
    dtgo=str(dtg1)

    if(inc > 0):
        ntime=nhr/inc
        if(verb): print 'ddd dtgrange',ntime,nhr,inc
        dtga=dtgo
        dtgs.append(dtga)
        i=1
        while(i<=ntime):
            dtgn=dtginc(dtgo,inc)
            dtga=dtgn
            dtgs.append(dtga)
            dtgo=dtgn
            i=i+1

        if(dtg1off != 0):
            i=0
            for dtg in dtgs:
                yyyy=int(dtg[0:4])-dtg1off
                dtga="%04d%s"%(yyyy,dtg[4:10])
                dtgs[i]=dtga
                i=i+1

    elif(inc <  0):
        dtgo=str(dtg1)
        ntime=abs(nhr/inc)
        if(verb): print 'ddd ------------ dtgrange',ntime,nhr,inc
        dtga=dtgo
        dtgs.append(dtga)
        i=1
        while(i<=ntime):
            dtgn=dtginc(dtgo,inc)
            dtga=dtgn
            dtgs.append(dtga)
            dtgo=dtgn
            i=i+1

        if(dtg1off != 0):
            i=0
            for dtg in dtgs:
                yyyy=int(dtg[0:4])-dtg1off
                dtga="%04d%s"%(yyyy,dtg[4:10])
                dtgs[i]=dtga
                i=i+1

    else:
        dtgs=[-999]

    return(dtgs)

def dtg2ymdh(dtg):

    cdtg=str(dtg)
    if(len(cdtg) == 10):
        yy=cdtg[0:4]
        mm=cdtg[4:6]
        dd=cdtg[6:8]
        hh=cdtg[8:10]
        
    elif(len(cdtg) == 11):
        yy=cdtg[0:5]
        mm=cdtg[5:7]
        dd=cdtg[7:9]
        hh=cdtg[9:11]
        
    else:
        yy=cdtg[0:2]
        mm=cdtg[2:4]
        dd=cdtg[4:6]
        hh=cdtg[6:8]
        yy='19'+yy

    return(yy,mm,dd,hh)

def dtg2vtime(dtg):

    tt=dtg2time(dtg)
    gmt=gmtime(tt)
    #vtime=strftime("%a %HZ %d %b %y",gmt)
    vtime=strftime("%a %d %b %HZ",gmt)
    return(vtime)

def dtg2gtime(dtg):
    try:
        (y,m,d,h)=dtg2ymdh(dtg)
    except:
        return(none)
    mo=mname3[m]
    gtime="%sZ%s%s%s"%(h,d,mo,y)
    return(gtime)

def yyyymm2gtime(yyyymm):
    y=yyyymm[0:4]
    m=yyyymm[4:]
    mo=mname3[m]
    gtime="%s%s"%(mo,y)
    return(gtime)

def gtime2dtg(gtime):
    h=gtime[0:2]
    d=gtime[3:5]
    m=gtime[5:8]
    y=gtime[8:]
    cm=cname3[m]
    dtg=y+cm+d+h
    return(dtg)

def chomp(string):
    ss=string[:-1]
    return ss

def uniq(ulist):
    weirdtest='asdasdfasdfasdfasdf'
    #
    # sort before length check for case of two
    #
    ulist.sort()
    rlist=[]

    if(len(ulist) > 2):
        test=ulist[1]
        test=weirdtest
    elif(len(ulist) == 0):
        return(rlist)
    else:
        test=ulist[0]

    if(test != weirdtest):
        rlist.append(test)

    for l in ulist:
        #if(repr(l) != repr(test)):
        if(l != test):
            rlist.append(l)
            test=l
    return(rlist)


def fopen(file,state='r'):
    from sys import exit
    try:
        fh=open(file,state)
        return(fh)
    except:
        print "unable to open: ",file,"\nsayoonara"
        exit()


def argopt(i):
    import sys
    try:
        if(sys.argv[i]):
            return(1)
    except:
        return(0)


def dtg_dtgopt_prc(dtgopt,ddtg=6):

    ddc=dtgopt.split(',')
    
    if(len(ddc) > 1):
        dtgs=[]
        for dc in ddc:
            if(find(dc,'.') or len(dc) != 10):
                dtgs=dtgs+dtg_dtgopt_prc(dc)
            else:
                dtgs.append(dc)
        return(dtgs)


    dd=dtgopt.split('.')
    if(len(dd) == 1):
        if(len(dtgopt) == 6 and dtgopt.isdigit()):
            bdtg="%s0100"%(dtgopt)
            edtg=dtginc("%s0100"%(yyyymminc(dtgopt,1)),-6)

        else:
            bdtg=dtg_command_prc(dtgopt)
            edtg=bdtg

    if(len(dd) >= 2):

        if(len(dd[0]) == 6 and dd[1].isdigit()):
            bdtg="%s0100"%(dd[0])
        else:
            bdtg=dtg_command_prc(dd[0])
 
        if(len(dd[0]) == 6):
            if(dd[1].isdigit()):
                if(len(dd[1]) == 6):
                    edtg=dtginc("%s0100"%(yyyymminc(dd[1],1)),-6)
                elif(len(dd[1]) == 2 or dd[1] == '6'):
                    edtg=dtginc("%s0100"%(yyyymminc(dd[0],1)),-int(dd[1]))
                    ddtg=int(dd[1])
            else:
                edtg=dtg_command_prc(dd[1])    
        else:
            edtg=dtg_command_prc(dd[1])

    if(len(dd) == 3):
        ddtg=dd[2]

    if(find(dtgopt,'cur12')): ddtg=12

    dtgs=dtgrange(bdtg,edtg,ddtg)

    if(dtgs[0] == '-1'):
        print 'EEE mf.dtg_dtgopt_prc bad dtgopt: ',dtgopt
        sys.exit()

    return(dtgs)


def dtg_command_prc(dtg,quiet=0,curdtg12=0,opsfhr=5.0):

    odtg=dtg
    if(curdtg12):
        curdtg=dtg12()
    else:
        curdtg=dtg6()

    if(dtg == 'cur+12'):
        odtg=dtginc(curdtg,+12)
    elif(dtg == 'cur+6'):
        odtg=dtginc(curdtg,+6)
    elif(dtg == 'cur'):
        odtg=curdtg
    elif(dtg == 'cur12'):
        odtg=dtg12()
    elif(dtg == 'cur-6'):
        odtg=dtginc(curdtg,-6)
    elif(dtg == 'cur-12'):
        odtg=dtginc(curdtg,-12)
    elif(dtg == 'cur-18'):
        odtg=dtginc(curdtg,-18)
    elif(dtg == 'cur-24'):
        odtg=dtginc(curdtg,-24)
    elif(dtg == 'cur-30'):
        odtg=dtginc(curdtg,-30)
    elif(dtg == 'cur-36'):
        odtg=dtginc(curdtg,-36)
    elif(dtg == 'cur-42'):
        odtg=dtginc(curdtg,-42)
    elif(dtg == 'cur-48'):
        odtg=dtginc(curdtg,-48)
    elif(dtg == 'cur-d1'):
        odtg=dtginc(curdtg,-24)

    elif(find(dtg,'cur-')  and not(find(dtg,'cur-d')) ):
        ld=len(dtg)
        nhr=int(dtg[4:ld])
        odtg=dtginc(curdtg,-1*nhr)

    elif(find(dtg,'cur12-')  and not(find(dtg,'cur12-d')) ):
        ld=len(dtg)
        nhr=int(dtg[6:ld])
        odtg=dtginc(dtg12(),-1*nhr)

    elif(find(dtg,'cur+') and not(find(dtg,'cur+d')) ):
        ld=len(dtg)
        nhr=int(dtg[4:ld])
        odtg=dtginc(curdtg,nhr)

    elif(find(dtg,'cur12+') and not(find(dtg,'cur12+d')) ):
        ld=len(dtg)
        nhr=int(dtg[6:ld])
        odtg=dtginc(curdtg,nhr)

#
# -dXXX
#
    elif(find(dtg,'cur-d')):
        ld=len(dtg)
        nday=int(dtg[5:ld])
        odtg=dtginc(curdtg,-1*nday*24)

    elif(find(dtg,'cur12-d')):
        ld=len(dtg)
        nday=int(dtg[7:ld])
        odtg=dtginc(dtg12(),-1*nday*24)

    elif(find(dtg,'cur+d')):
        ld=len(dtg)
        nday=int(dtg[5:ld])
        odtg=dtginc(curdtg,nday*24)

    elif(find(dtg,'cur12+d')):
        ld=len(dtg)
        nday=int(dtg[7:ld])
        odtg=dtginc(curdtg,nday*24)

#
# ops 12 for w2.esrl.nwp2.py
#
    elif(dtg == 'ops12'):
        odtg=dtg12()
        fphr=float(dtg12('fphr'))
        if(fphr <= opsfhr):
            odtg=dtginc(odtg,-12)
    elif(dtg == 'ops12long'):
        opsfhrl=11.0
        odtg=dtg12()
        fphr=float(dtg12('fphr'))
        if(fphr <= opsfhrl):
            odtg=dtginc(odtg,-12)
    elif(dtg == 'ops6'):
        (odtg,phr)=dtg_phr_command_prc('cur')
        fphr=float(phr)
        if(fphr <= opsfhr*0.5):
            odtg=dtginc(odtg,-6)

    if(len(odtg) != 10):
        if(quiet != 0):
            print "EEE odtg ",odtg," fouled len: ",len(odtg)
        odtg=-1

    if(len(dtg.split('.')) > 1):
        odtg=len(dtg.split('.'))

    return(odtg)

def dtg_phr_command_prc(idtg):

    curdtg=dtg()
    curphr=dtg('phr')

    ddtg=-9999

    odtg=dtg_command_prc(idtg)

    if(ddtg != -9999):
        odtg=dtginc(curdtg,ddtg)

    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)
        odtg=-1
        ocurphr=-1
        return(odtg,ocurphr)

    deltadtg=dtgdiff(odtg,curdtg)
    curphr=float(curphr)+float(deltadtg)

    if(curphr >= 0.0 and curphr < 10.0):
        ocurphr="+%3.2f"%(curphr)
    elif(curphr >= 10.0 and curphr < 100.0):
        ocurphr="+%4.2f"%(curphr)
    elif(curphr >= 100.0 and curphr < 1000.0):
        ocurphr="+%5.2f"%(curphr)

    else:
        ocurphr="%7.2f"%(curphr)


    return(odtg,ocurphr)


def dtg_12_command_prc(idtg):

    odtg=idtg
    curdtg=dtg()
    if(idtg == 'cur+12'):
        odtg=dtginc(curdtg,+12)
    elif(idtg == 'cur'):
        odtg=curdtg
    elif(idtg == 'cur-12'):
        odtg=dtginc(curdtg,-12)
    elif(idtg == 'cur-24'):
        odtg=dtginc(curdtg,-24)

    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)

    return(odtg)

def cur2dtg(idtg):

    odtg=idtg

    curdtg=dtg6()

    if(idtg == 'cur+12'): odtg=dtginc(curdtg,+12)
    if(idtg == 'cur+6'): odtg=dtginc(curdtg,+6)
    if(idtg == 'cur'): odtg=curdtg
    if(idtg == 'cur-6'): odtg=dtginc(curdtg,-6)
    if(idtg == 'cur-12'): odtg=dtginc(curdtg,-12)
    if(idtg == 'cur-18'): odtg=dtginc(curdtg,-18)
    if(idtg == 'cur-24'): odtg=dtginc(curdtg,-24)
    if(idtg == 'cur-36'): odtg=dtginc(curdtg,-36)
    if(idtg == 'cur-48'): odtg=dtginc(curdtg,-48)


    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)

    return(odtg)

# --------- python cookbood p.228 -- capture stderr/stdout
#
# -- turn off buffering

## def makeNonBlocking(fd):
##     fl = fcntl.fcntl(fd, FCNTL.F_GETFL)
##     try:
##         fcntl.fcntl(fd, FCNTL.F_SETFL,fl | FCNTL.O_NDELAY)
##     except AttributeError:
##         fcntl.fcntl(fd, FCNTL.F_SETFL,fl | FCNTL.NDELAY)

## def getCommandOutput(command,erropt='stderr'):

##     child = popen2.Popen3(command, 1)
##     child.tochild.close()
##     outfile = child.fromchild
##     outfd = outfile.fileno()
##     errfile = child.childerr
##     errfd = errfile.fileno()

##     makeNonBlocking(outfd)
##     makeNonBlocking(errfd)

##     outdata = errdata = ''
##     outeof = erreof = 0

##     while 1:

##         ready = select.select([outfd,errfd],[],[]) # wait for input

##         if outfd in ready[0]:
##             outchunk = outfile.read()
##             if outchunk == '': outeof = 1
##             outdata = outdata + outchunk

##         if errfd in ready[0]:
##             errchunk = errfile.read()
##             if errchunk == '': erreof = 1
##             errdata = errdata + errchunk

##         if outeof and erreof: break
##         select.select([],[],[],.1) # allow a little time for buffers to fill

##     err = child.wait()

##     if err != 0:

##         if(erropt != 'nostderr'):
##             print "EEE: %s failed with the exit code %d\nEEE: %s" % ( command, err, errdata)

##         return outdata
## #        raise RuntimeError, "%s failed with the exit code %d\n%s" % ( command, err, errdata)

##     return outdata


def getCommandOutput2(command):
    child = os.popen(command)
    data = child.read()
    err= child.close()
    if err:
        raise RuntimeError, '%s failed with the exit code %d\n' % (command,err)
    return data



def runcmd(command,logpath='straightrun',lsopt='',prefix='',postfix=''):

    if(logpath == ''):
        logpath='straightrun'

    oprefix=''
    if(prefix != ''): oprefix="(%s)"%(prefix)
    
    opostfix=''
    if(postfix != ''): opostfix="[%s]"%(postfix)

    if(logpath == 'straightrun' or logpath == 'norun'):

        curtime=dtg('cur_hms')
        occc="CCC"
        if(oprefix != ''): occc="%s(%s)"%(occc,oprefix)
        if(lsopt != 'q'): print "%s: %s %s %s"%(occc,command,curtime,opostfix)
        if(logpath != 'norun'): os.system(command)
        return

    if(logpath == 'quiet'):
        os.system(command)
        return

    global LF

    #
    # output to log file (append and add title line)
    #

    if(logpath != 'nologpath'):

        log=getCommandOutput2(command)

        lout="\nTTT: %s  :: CCC: %s\n\n"%(dtg6('curtime'),command)
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

def runcmd2(command, ropt='', verb=1, lsopt='', prefix='', postfix='', ostdout=1,
            wait=False):

    oprefix=''
    if(prefix != ''): oprefix="(%s)"%(prefix)
    
    opostfix=''
    if(postfix != ''): opostfix="[%s]"%(postfix)

    if(ropt == 'norun'):  
        if(oprefix != ''):  oprefix="%s-NNNrun"%(oprefix)
        else:               oprefix='NNNrun'
        if(opostfix != ''): opostfix="%s-NNN"%(opostfix)
        else:               opostfix='NNN'
    curtime=dtg('cur_hms')
    occc="CCC-222"
    if(oprefix != ''): occc="%s(%s)"%(occc,oprefix)
    ocard="%s: %s %s %s"%(occc,command,curtime,opostfix)
    if(lsopt != 'q'): print ocard
    
    if(ropt == 'norun'): return(0)
    
    import subprocess
    try:
        if (wait):

            p = subprocess.Popen(
                [command], 
                stdout = subprocess.PIPE,
                shell = True)
            p.wait()
        else:
            if(ostdout == 1):
                p = subprocess.Popen(
                    [command], 
                    shell = True, 
                    stdin = None, stdout = PIPE, stderr = PIPE, close_fds = True)
            else:
                p = subprocess.Popen(
                    [command], 
                    shell = True, 
                    stdin = None, stdout = None, stderr = PIPE, close_fds = True)
                
        (result, error) = p.communicate()

        
    except subprocess.CalledProcessError as e:
        sys.stderr.write(
            "common::run_command() : [ERROR]: output = %s, error code = %s\n" 
            % (e.output, e.returncode))
        
        return(-999)


    rc=1
    if(ostdout == 1):
        slines=result.split('\n')

        if(verb): 
            print 'STDOut...'
            for line in slines:
                if(len(line) > 0):  print line

    elines=error.split('\n')
    if(verb and len(elines) > 1): print'STDErr...'
    for line in elines:
        if(verb): 
            if(len(line) > 0):  print line
        if(find(line,'error')): 
            rc=-999

    if(ostdout == 1): rc=(rc,slines)
    
    return (rc)



def PathCreateTime(path):
    import time
    timei=os.path.getctime(path)
    ltimei=time.localtime(timei)
    gtimei=time.gmtime(timei)
    dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
    gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
    ldtg=dtimei[0:10]
    gdtg=gdtimei[0:10]
    return(dtimei,ldtg,gdtg)

def PathModifyTime(path):
    import time
    timei=os.path.getmtime(path)
    ltimei=time.localtime(timei)
    gtimei=time.gmtime(timei)
    dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
    gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
    ldtg=dtimei[0:10]
    gdtg=gdtimei[0:10]
    return(dtimei,ldtg,gdtg)

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

def ChkDir(ddir,diropt='verb'):

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

def ChangeDir(dir,diropt='verb'):

    try:
        os.chdir(dir)
        print 'cd---> ',dir
    except:
        print 'WWW unable to cd to: ',dir

def ChkPath(path,pathopt='noexit',verb=1):

    if not(os.path.exists(path)) :
        if(verb): print "EEE(ChkPath): path: %s NOT there... "%(path)
        if(pathopt == 'exit'):
            print "EEE(ChkPath): Sayoonara..."
            sys.exit()
        else:
            return(0)
    else:
        return(1)

def GetPathSiz(path,pathopt='exit',verb=1):

    if(ChkPath(path,pathopt='noexit') != 1):
        siz=None
    else:
        siz=os.path.getsize(path)

    return(siz)





def LsPids():

    #
    # get executing processes
    #

    processes=os.popen('ps -ef ').readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[1]),int(tt[2]),pname,piddate) )

    return(pids)

def findPyPids(job):

    #
    # get executing processes
    #

    processes=os.popen('ps kstart_time -ef | grep -i %s'%(job)).readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[1]),int(tt[2]),pname,piddate) )
        
    opids=[]
    for pid in pids:
        if(find(pid[2],'python')):
            opids.append(pid)
        

    return(opids)


def LsPids3():

    # get executing processes and three ids (on bsd/mac only?)
    #
    processes=os.popen('ps -ef ').readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[0]),int(tt[1]),int(tt[2]),pname,piddate) )

    return(pids)


def PsTime2Hours(time):
    tt=time.split('-')

    if(len(tt) == 2):
        days=float(tt[0])
        ttime=tt[1].split(':')
    else:
        days=0.0
        ttime=time.split(':')

    hours=float(ttime[0])
    minutes=float(ttime[1])
    seconds=float(ttime[2])

    totaltime=days*24.0 + hours + (minutes+ (seconds/60.0) )/60.0

    return(totaltime)


def LsPidsuSer():

    #
    # get user executing processes
    #
    user=os.getenv('USER')
    processes=os.popen("ps -u %s -o \"pid,ppid,time,comm\""%(user)).readlines()
    pids=[]

    for n in range(1,len(processes)):
        p=processes[n]
        tt=p.split()
        pid=int(tt[0])
        ppid=int(tt[1])
        time=tt[2]
        command=tt[3]
        totaltime=PsTime2Hours(time)
        pids.append( (pid, ppid, totaltime, command) )

    return(pids)

def KillLongRunningProcess(timelimitkill,command2kill):

    upids=LsPidsuSer()
    for upid in upids:
        pid=upid[0]
        totaltime=upid[2]
        command=upid[3]
        if(totaltime >= timelimitkill and command == command2kill):
            print 'KKKKKKKKKKKilling: ',pid,totaltime,command
            os.kill(pid,signal.SIGKILL)






def KillPids(parentpid):

    verb=1

    #
    #  look for children (cpid) of the current parent process (ppid)
    #  put in list of spawned pids (spids)
    #
    #  initialize with input pid from calling parent

    curpid=parentpid

    spids=[]

    pids=LsPids()

    for pid in pids:
        cpid=pid[0]
        ppid=pid[1]
        pname=pid[2]

        if(ppid == curpid):
            spids.append(cpid)
            curpid=cpid
            if(verb): print cpid,ppid,curpid,pname

    #
    #  send kill signal to spids
    #

    nspids=len(spids)
    if(verb): print 'KKKKKKKKKKKK',nspids,spids,parentpid
    for spid in spids:
        try:
            print 'Killing pid: ',spid
            os.kill(spid,signal.SIGKILL)
        except:
            if(verb):
                print "unable to kill spawnd process: ",spid
            else:
                pass

    #
    #  now kill the main process if the one of the spawned 
    #

    try:
        os.kill(curpid,signal.SIGKILL)
    except:
        pass



def CleanReturns(istring):

    olist=[]

    o=istring.split('\n')

    for oo in o:
        if(len(oo) != 0):
            olist.append(oo+'\n')

    return(olist)

#
# calculate age of file using current and motime (h)
#
def PathDmtime(ipath):

    import time
    import os
    ctime=time.time()
    mtime=os.path.getmtime(ipath)
    dmtime=(ctime-float(mtime))/3600.0
    return(dmtime)


def doFTPsimple(server,localdir,remotedir,mask,
                opt='ftp.put',passive='off',doitout=0,quittime=None,
                verb=0):


    ftpopt=''
    if(quittime != None):
        ftpopt="-q %s"%(quittime)

    if(passive == 'off'):
        passopt=''
    elif(passive == 'on'):
        passopt='passive'
    else:
        passopt='passive'

    if(opt == 'ftp.ls' or opt == 'ftp.noload'):
        cmd="""
%s
cd %s
pwd
dir %s
quit
"""%(passopt,remotedir,mask)

    elif(opt == 'local.ls' or opt == 'ftp.noload'):
        cmd="""
%s
lcd %s
pwd
!ls -l %s
quit
"""%(passopt,localdir,mask)

    elif(opt == 'ftp.mkdir'):
        cmd="""
%s
mkdir %s
"""%(passopt,remotedir)

    elif(opt == 'ftp.rm'):
        cmd="""
%s
###verbose
prompt
cd %s
pwd
mdel %s
"""%(passopt,remotedir,mask)

    elif(opt == 'ftp.put' or opt == 'ftp'):

        cmd="""
#passive
verbose
cd %s
lcd %s
bin
prompt
mput %s
"""%(remotedir,localdir,mask)

    elif(opt == 'ftp.put.mk' or opt == 'ftp'):

        cmd="""
#passive
verbose
mkdir %s
cd %s
lcd %s
bin
prompt
mput %s
"""%(remotedir,remotedir,localdir,mask)

    elif(opt == 'ftp.get'):

        cmd="""
#passive
verbose
cd %s
lcd %s
bin
prompt
mget %s
"""%(remotedir,localdir,mask)

    else:
        print 'EEEEEEEEEEE in mf.doFTPsimple invalid opt: ',opt
        sys.exit()


    doit=1
    if(opt == 'ftp.noload'): doit=0

    if(doit and doitout==0):
        ftppopen="ftp %s %s"%(ftpopt,server)
        if(verb): print 'ftppopen: ',ftppopen,' ftp cmd: ',cmd
        o=os.popen(ftppopen,"w")
        o.write(cmd)
        o.close()

    if(doitout):
        if(verb): print "ftp cmd:",cmd
        cmd="""ftp %s %s << EOF
%s
EOF
"""%(ftpopt,server,cmd)
        rc=os.popen(cmd).readlines()
        return(rc)

    #if(opt == 'ftp.ls'): sys.exit()

#
# 20031120 - process __doc__ string (str)
# to add pyfile
#

def usage(str,arg,curdtg=None,curtime=None,curphr=None):
    n=str.count('%s')
    pp=[]
    for n in range(0,n): pp.append(arg)
    pp=tuple(pp)
    print str%(pp)
    if(curdtg!=None and curtime!=None and curphr!=None):
        print "The Current DTG: %s  Phr: %s  Time: %s"%(curdtg,curphr,curtime)
    elif(curdtg!=None and curtime!=None):
        print "The Current DTG: %s  Time: %s"%(curdtg,curtime)


def find(mystr,pattern):
    rc=0
    if(mystr.find(pattern) != -1): rc=1
    return(rc)



def nint(f):
    if(f>=0.0): rc=int(f+0.5)
    if(f<=0.0): rc=int(f-0.5)
    return(rc)


def WriteCtl(ctl,ctlpath,verb=0):

    try:
        c=open(ctlpath,'w')
    except:
        print "EEE unable to open: %s"%(ctlpath)
        sys.exit()

    if(verb): print "CCCC creating .ctl: %s"%(ctlpath)
    c.writelines(ctl)
    c.close()
    return

def WriteList(llist,opath,verb=0,wmode='w'):

    try:
        c=open(opath,wmode)
    except:
        print "EEE unable to open: %s"%(opath)
        sys.exit()

    if(verb): print "CCCC creating list output file: %s"%(opath)
    for card in llist:
        card=card+'\n'
        c.writelines(card)
    c.close()
    return


def PrintCtl(ctl,ctlfile=None):

    if(ctlfile):
        otitle=ctlfile
    else:
        otitle="ctl file"
    print "PPPPPPPPP printing: %s ..................."%(otitle)

    for cc in ctl:
        print cc[:-1]

def PrintCurrency(title,ns=54,amount=-999,quiet=0):
    ntot=str(amount)
    nl=len(ntot)
    if(nl>9):
        n9=nl-9
        n6=nl-6
        n3=nl-3
        format="%%-%ds :: %4s,%3s,%3s,%3s"%(ns-4,ntot[0:n9],ntot[n9:n6],ntot[n6:n3],ntot[n3:])
    elif(nl>6):
        n6=nl-6
        n3=nl-3
        format="%%-%ds :: %8s,%3s,%3s"%(ns-4,ntot[0:n6],ntot[n6:n3],ntot[n3:])
    elif(nl>3):
        n3=nl-3
        format="%%-%ds :: %12s,%3s"%(ns-4,ntot[0:n3],ntot[n3:])
    else:
        format="%%-%ds :: %16s"%(ns-4,ntot)
    card=format%(title)
    if(quiet == 0): print card

    return(card)

def PyVer():
    (pyverMajor,pyverMinor,pyverRel)=sys.version.split()[0].split('.')[0:3]
    fpyver=float("%s.%s%s"%(pyverMajor,pyverMinor,pyverRel))
    return(fpyver)

def Timer(str,stime):
    import time
    dtime=time.time()-stime
    print "ffffffff %-60s time: %5.2f s"%(str,dtime)


#
# function to glob than cp files 
#

def cpfiles(sdir,tdir,mask,ropt=''):

    files=glob.glob("%s/%s"%(sdir,mask))

    for file in files:
        cmd="cp %s %s/."%(file,tdir)
        runcmd(cmd,ropt)


def rmfiles(sdir,mask,ropt='norun'):

    files=glob.glob("%s/%s"%(sdir,mask))

    for file in files:
        cmd="rm %s"%(file)
        runcmd(cmd,ropt)

def h2hm(age):

    fh=int(age)*1.0
    im=int( (age-fh)*60.0+0.5 )
    if(im == 60):
        fh=fh+1.0
        im=0

    cage="%4.0f:%02d"%(fh,im)
    return(cage)


def min2minsec(min):

    fm=int(min)*1.0
    im=int( (min-fm)*60.0+0.5 )
    if(im == 60):
        fm=fm+1.0
        im=0

    cmin="%4.0f:%02d"%(fm,im)
    return(cmin)


if (__name__ == "__main__"):

    upids=LsPidsuSer()
    for upid in upids:
        print 'uuu ',"%5.2f"%(upid[2]),upid
        if(upid[2] > 0.30):
            pid=upid[0]
            totaltime=upid[2]
            command=upid[3]
            print 'lllllllllll ',pid,totaltime,command

    KillLongRunningProcess(12.0,'rsync')



