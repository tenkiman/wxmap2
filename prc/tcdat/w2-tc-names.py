#!/usr/bin/env python

from tcbase import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class RsyncCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['tyear',    'tyear -- must set '],
            }

        self.defaults={
            'doupdate':0,
            }

        self.options={
            'source':           ['s:',None,'a','source opt'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'do9Xnames':        ['9',0,1,'verb=1 is verbose'],
            'dojtwc_nhctest':   ['n',0,1,' allow jtwc to set names in CPAC and EPAC'],

            }

        self.purpose='''
generate hash for TC names using JTWC ATCF tables'''
        self.examples='''
%s  2001                   # single years
%s  2001.2003              # three years
%s  cur                    # current year
%s  2004 -n                # allow jtwc to set names in CPAC and EPAC)
%s  2000 -s neumann        # allow jtwc to set names in CPAC and EPAC)'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=RsyncCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


try:
    (yyyy1,yyyy2)=tyear.split('.')
    tyears=range(int(yyyy1),int(yyyy2)+1)
    
except:
    
    if(tyear == 'cur' or tyear == 'ops'):
        tyear=curdtg[0:4]
        tyearp1=int(tyear)+1
        do9Xnames=1
        tyears=[tyear,tyearp1]
    else:
        tyears=[int(tyear)]

if(tyear == 'null'):
    print 'EEE invalid year in command line ....'
    sys.exit()



# set years to two years to cover shem overlap
#
cyear=curdtg[0:4]
curyyyy=curdtg[0:4]

(shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)
curmm=curdtg[4:6]
if( (tyear == curyyyy) and shemoverlap):
    tyears=[yyyy1,yyyy2]

#
# do previous year to catch overlap of storms crossing year
#
elif( (tyear == curyyyy) and (int(curmm) == 1)):
    yyyym1=int(tyear)-1
    yyyym1=str(yyyym1)
    tyears=[yyyym1,tyear]


ndir=w2.TcNamesDatDir
mf.ChkDir(ndir,'mk')


for tyear in tyears:

    #
    # 20070828 -- neumann bdecks/storms*
    #

    if(tyear <= 2000):
        tcnmaskneumann="%s/storms.*.table"%(w2.TcStormsNeumannDir)
    else:
        tcnmaskneumann=''

    #
    # only do 9X names if shem
    #
    
    #if( (int(tyear) > int(cyear)) or
    #    (int(tyear) == int(cyear))
    #   ): do9Xnames=1

    icyear=int(cyear)
    ityear=tyear
    tyear=str(tyear)

    tcnpath="%s/storm.table"%(w2.TcStormsJtwcDir)

    docurjtwc=1
    tcnmaskjtwccur="%s/storms.jtwc*"%(w2.TcStormsJtwcDir)
    tcnmaskjtwccur="%s/storms.*txt"%(w2.TcStormsJtwcDir)
    tcnmaskjtwc="%s/storm.table"%(w2.TcStormsJtwcDir)

    #
    # find latest and greatest storms.jt* from jtwc
    #

    jtstorms=glob.glob("%s/storms.jt*"%(w2.TcStormsJtwcDir))

    youngest=9999999999
    for jtstorm in jtstorms:
        if(not(mf.find(jtstorm,'.zip'))):
            curage=MF.PathModifyTimeCurdiff(jtstorm)*(-1/24.0)
            if(curage < youngest):
                youngest=curage
                youngestjtstorm=jtstorm
                
            if(verb): print 'jjjjjjjjj ',jtstorm,curage

    tcnmaskjtwccur=youngestjtstorm
            
    alljtstorms=glob.glob("%s/storms.jt*"%(w2.TcStormsJtwcDir))
    for alljtstorm in alljtstorms:
        if(verb): print 'aaaaaa ',alljtstorm,youngestjtstorm
        if(alljtstorm != youngestjtstorm):
            print 'cat ',alljtstorm,youngestjtstorm
            cmd="cat %s >> %s"%(alljtstorm,youngestjtstorm)
    

    # -- new standard is storms_list.txt
    if(ityear >= 2004):
        tcnmasknhc="%s/storm.table"%(w2.TcStormsNhcDir)
    else:
        tcnmasknhc="%s/storm.table.archive"%(w2.TcStormsNhcDir)

    docurnhc=1
    if(cyear == tyear or ityear >= icyear or docurnhc):
        tcnmasknhccur="%s/storms.*txt"%(w2.TcStormsNhcDir)
        tcnmasknhccur="%s/storm_list.txt"%(w2.TcStormsNhcDir)
        docurnhc=1
        
    ls=[]
    if(docurnhc):
        ls=glob.glob(tcnmasknhccur)
    ls=ls+glob.glob(tcnmasknhc)

    cardsnhc=[]
    
    #
    # NHC cards
    #

    if(ls):
        for l in ls:
            try:
                cardsnew=open(l).readlines()
            except:
                cardsnew=[]

            cardsnhc=cardsnhc+cardsnew

            
    #
    # filter out non-nhc storms from  NHC cards
    #

    cardsnhc2=[]
    for card in cardsnhc:
        tt=card.split(',')
        if(len(tt) <= 2): continue
        stmname=tt[0].strip()
        basin=tt[1].strip()
        basinid=tt[2].strip()
        stmnum=int(tt[7])
        stmyear=int(tt[8])
        jtwctest=(basinid == 'W' or basinid == 'A' or basinid == 'B' or basinid == 'P' or basinid == 'S')
        #
        # special case for SLANT storm katarina in 2004...
        #
        if(basin == 'SL' and basinid == 'S'):  jtwctest=0
        dojtwctest=1
        if(dojtwctest):
            if(not(jtwctest)):
                cardsnhc2.append(card)
            else:
                print "WWWWWWWWWWWWWWW jtwc storm in nhc tables: ",stmname,basinid,stmnum,stmyear


    cardsnhc=copy.deepcopy(cardsnhc2)


    #
    # use "final" names if tyear != cyear
    #
    if(tyear < cyear):
        dojtwc_nhctest=1

    #
    # JTWC cards
    #

    cardsjtwc=[]

    ls=[]
    if(docurjtwc):
        ls=glob.glob(tcnmaskjtwccur)
    ls=ls+glob.glob(tcnmaskjtwc)

    if(ls):
        for l in ls:
            try:
                cardsnew=open(l).readlines()
            except:
                cardsnew=[]
            cardsjtwc=cardsjtwc+cardsnew

    #
    # Neumann cards
    #

    cardsneumann=[]

    if(tcnmaskneumann != ''):
        ls=glob.glob(tcnmaskneumann)
        if(ls):
            for l in ls:
                try:
                    cardsnew=open(l).readlines()
                except:
                    cardsnew=[]
                cardsneumann=cardsneumann+cardsnew
    else:
        cardsneumann=''
            


    if(dojtwc_nhctest):
        cardsjtwc2=[]
        
        for card in cardsjtwc:
            
            tt=card.split(',')
            if(len(tt) <= 2): continue
            stmname=tt[0].strip()
            basin=tt[1].strip()
            basinid=tt[2].strip()
            nhctest=(basinid == 'L' or basinid == 'E' or basinid == 'C')

            if(not(nhctest)):
                cardsjtwc2.append(card)

        cardsjtwc=cardsjtwc2


    if(source == 'neumann'):
        cards=cardsneumann
    else:
        cards=cardsjtwc+cardsnhc

    tchash={}
    stmnums={}

    for card in cards:
        tt=card.split(',')
        #print 'ccc',card[0:-1]
        if(len(tt) <= 2): continue
        stmname=tt[0].strip()
        basin=tt[1].strip()
        basinid=tt[2].strip()
        stmnum=tt[7].strip()
        yyyy=tt[8].strip()
        #
        # reset basinid for slant storms:
        #
        if(basin == 'SL'): basinid='T'

        stmid=stmnum+basinid

        #
        # only for IO and shem
        #
        if(do9Xnames):
            try:
                ntest=(
                    int(stmid[0]) < 5 or
                    (
                    (int(stmid[0]) == 9)
                    #and
                    #(basinid == 'P' or basinid == 'S' or basinid == 'A' or basinid == 'B')
                    )
                    )
            except:
                ntest=0
        else:
            try:
                ntest=(int(stmid[0]) < 5 )
            except:
                ntest=0


        #if(yyyy == tyear):
        #    print 'qqqq ',stmid,card[:-1]

        if(yyyy == tyear and ntest ):
            ###print stmnum,basinid,card[:-1],stmname
            tchash[stmnum,basinid]="        (\'%s\',\'%s\'): \'%s\',"%(yyyy,stmid,stmname)
            try:
                stmnums[basinid].append(stmnum)
            except:
                stmnums[basinid]=[]
                stmnums[basinid].append(stmnum)
            ###print yyyy,stmid,stmname,basin,basinid,stmnum

    #
    # output sorted by basin, send to one-file-per-year in ~/dat/tc/names
    #

    sh=Hemi3toBasins['SHS']
    nh=Hemi3toBasins['NHS']

    if(source == 'neumann'):
        
        namespath="%s/TCnamesNeumann%s.py"%(ndir,tyear)
        o=open(namespath,'w')

        statspath="%s/TCstatsNeumann%s.py"%(ndir,tyear)
        o=open(namespath,'w')


    elif(source == 'ops'):
        
        namespath="%s/TCnamesOps%s.py"%(ndir,tyear)
        o=open(namespath,'w')

        statspath="%s/TCstatsOps%s.py"%(ndir,tyear)
        o=open(namespath,'w')


    else:
        
        namespath="%s/TCnames%s.py"%(ndir,tyear)
        o=open(namespath,'w')

        statspath="%s/TCstats%s.py"%(ndir,tyear)
        o=open(namespath,'w')

    cards="""
tcnames={
    """
    o.writelines(cards)

    ab=sh+nh
    for b in ab:

        try:
            c=mf.uniq(stmnums[b])
            c.sort()
            stmnums[b]=c
        except:
            pass

    for b in ab:
        try:
            bname=Basin1toBasinNameShort[b]
            card="# basin - %s : %s"%(b,bname)
            o.writelines(card+'\n')
            if(verb): print card
            for s in stmnums[b]:
                o.writelines(tchash[s,b]+'\n')
                if(verb): print tchash[s,b]
        except:
            pass

    cards="""
}
    """
    o.writelines(cards)
    o.close()

    tcnames=GetTCnamesHash(tyear,source=source)
    

    pycardsnhs=[]
    basinopt='NHS'
    (tcs,tcstats,allhtml,alljs,obstmid)=TCsByBasin(tyear,basinopt,
                                                      pycardsnhs,rptopt=0,tchash=tcnames,bstmid='null',source=source)
    pycardsshs=[]
    basinopt='SHS'
    (tcs,tcstats,allhtml,alljs,obstmid)=TCsByBasin(tyear,basinopt,
                                                      pycardsshs,rptopt=0,tchash=tcnames,bstmid='null',source=source)

    pycards=pycardsshs+pycardsnhs

    #for pycard in pycards:
    #    print pycard

    o=open(statspath,'w')
    W=o.writelines

    ocard="tcstats={\n"
    W(ocard)

    for pycard in pycards:
        ocard=pycard+'\n'
        W(ocard)

    ocard="}\n"
    W(ocard)


    o.close()

    if(verb):
        print "NNNNN: %s"%(namespath)
        print "SSSSS: %s"%(statspath)



sys.exit()
