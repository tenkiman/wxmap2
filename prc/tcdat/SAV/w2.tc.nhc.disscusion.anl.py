#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

byear=2015
byear=2003
eyear=2016

years=mf.yyyyrange(byear, eyear)
basins=['al','ep','cp']
#basins=['al']

nDisc={}
nHwrf={}
hwrfMentions={}
nEcmwf={}
ecmwfMentions={}
nGfs={}
gfsMentions={}
nGfdl={}
gfdlMentions={}

pMentions={}

for year in years:
    sdir="%s/%s"%(w2.TcDisNhcDir,year)
    for basin in basins:
        discS=glob.glob("%s/*%s*"%(sdir,basin))
        nDisc[basin,year]=len(discS)
        nHwrf[basin,year]=0
        nEcmwf[basin,year]=0
        nGfs[basin,year]=0
        nGfdl[basin,year]=0

        for d in discS:
            
            (ddir,dfile)=os.path.split(d)
            
            cards=open(d).readlines()
            
            for card in cards:
                if 'hwrf' in card.lower():
                    MF.append2KeyDictList(hwrfMentions, basin,year,d)
                    nHwrf[basin,year]=nHwrf[basin,year]+1
                    break
                
            for card in cards:
                if 'ecmwf' in card.lower():
                    MF.append2KeyDictList(ecmwfMentions, basin,year,d)
                    nEcmwf[basin,year]=nEcmwf[basin,year]+1
                    break
                
            for card in cards:
                if 'gfs' in card.lower():
                    MF.append2KeyDictList(gfsMentions, basin,year,d)
                    nGfs[basin,year]=nGfs[basin,year]+1
                    break

            for card in cards:
                if 'gfdl' in card.lower():
                    MF.append2KeyDictList(gfdlMentions, basin,year,d)
                    nGfdl[basin,year]=nGfdl[basin,year]+1
                    break
                
                
print 'All:   ',nDisc
print 'Hwrf:  ',nHwrf
print 'Ecmwf: ',nEcmwf
print 'Gfs:   ',nGfs
print 'Gfdl:  ',nGfdl


for year in years:
    for basin in basins:
        nT=nDisc[basin,year]
        nH=nHwrf[basin,year]
        nE=nEcmwf[basin,year]
        nG=nGfs[basin,year]
        nL=nGfdl[basin,year]
        
        print 'yyybbb',year,basin,nT
        if(nT > 0):
            pH=mf.nint((float(nH)/float(nT))*100.0)
            pE=mf.nint((float(nE)/float(nT))*100.0)
            pG=mf.nint((float(nG)/float(nT))*100.0)
            pL=mf.nint((float(nL)/float(nT))*100.0)
        else:
            pH=pE=pG=pL=999
        
        pMentions[basin,year]=(pH,pE,pG,pL)
        
        print 'NNN',basin,year,nT,nH,nE,nG,nL
        print 'PPP',basin,year,'H:',pH,' E: ',pE,' GFS: ',pE,' GFDL: ',pL
        
for basin in basins:
    print '% mentions in: ',basin
    print "      HWRF  ECMWF  GFS  GFDL"
    for year in years:
        (pH,pE,pG,pL)=pMentions[basin,year]
        print "%s   %3d    %3d  %3d   %3d"%(year,pH,pE,pG,pL)
        
sys.exit()
hwrfType={}
for d in hwrfMentions['al'][year]:
    cmd="less %s"%(d)
    mf.runcmd(cmd)
    htype=raw_input("type of use? ")
    MF.append2KeyDictList(hwrfType, 'al', year,(htype,d))
    print 'hhh',htype
    
            
    
    
