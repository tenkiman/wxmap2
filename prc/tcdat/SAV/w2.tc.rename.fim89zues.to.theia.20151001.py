#!/usr/bin/env python

from tcbase import *

byear=2016
source='tmtrkN'
renameAids={
    'fm8z':'fm8t',
    'f8hz':'f8ht',
    'fm9z':'fm9t',
    'f9hz':'f9ht',
    }

ad2rename='adecks.fimzeus.2.rename.txt'
adecks=MF.ReadFile2List(ad2rename)
#adecks=[]
if(len(adecks) > 0):
    for adeck in adecks:
        ncards=[]
        nadeck=adeck[:-1]
        oadeck="%s-OLD"%(nadeck)
        cards=MF.ReadFile2List(nadeck)
        for card in cards:
            ncard=None
            for caid in renameAids.keys():
                if(mf.find(card,caid)):
                    ncard=card.replace(caid,renameAids[caid])
                if(mf.find(card,caid.upper())):
                    ncard=card.replace(caid.upper(),renameAids[caid].upper())

            if(ncard != None):
                ncards.append(ncard)
            else:
                ncards.append(card)

        print 'OOOOOOOOOOOOOOOOOOO',oadeck
        print 'NNNNNNNNNNNNNNNNNNN',nadeck
        MF.WriteList2Path(cards,oadeck)
        MF.WriteList2Path(ncards,nadeck)

            

        


else:
    tdir="%s/%s/%s"%(TcAdecksAtcfFormDir,byear,source)

    adecks2rename=[]
    adecks=glob.glob("%s/a*dat"%(tdir))
    adecks.sort()

    for adeck in adecks:
        cards=MF.ReadFile2List(adeck)
        gotit=0
        for card in cards:
            tt=card.split(',')
            aid=tt[4].strip()
            for caid in renameAids.keys():
                #print 'adfasdf',aid,caid.upper()
                if(aid == caid or aid == caid.upper()):
                    adecks2rename.append(adeck)
                    gotit=1
                    #print 'gggffffffffffffffffffffffffffffffffffffffffffffffffffffffff',aid,caid,adeck
                if(gotit): break

            if(gotit): break

    adecks2rename=mf.uniq(adecks2rename)

    for adeck in adecks2rename:
        print adeck
        

    # run and cat > ad2rename
                
            
            
