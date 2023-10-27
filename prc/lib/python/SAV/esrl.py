def GetDataStatus(status,dtg,model,tdir):

    lastTau=None
    latestTau=None
    latestCompleteTau=None
    earlyTau=None
    gmplastdogribmap=-999
    gmplatestTau=-999
    gmplastTau=-999

    mask="%s/gribmap.status.*.txt"%(tdir)
    gmps=glob.glob(mask)
    gmps.sort()

    gmpAge=0.0
    if(len(gmps) >= 1):
        for gmpspath in gmps:
            age=w2.PathCreateTimeDtgdiff(dtg,gmpspath)
            if(age > gmpAge):
                gmpAge=age
                latestgmpPath=gmpspath

        (dir,file)=os.path.split(latestgmpPath)
        tt=file.split('.')

        gmplastdogribmap=int(tt[3])
        gmplatestTau=int(tt[4])
        gmplastTau=int(tt[5])
    
    itaus=status.keys()
    itaus.sort()

    ages={}
    for itau in itaus:
        ages[itau]=status[itau][0]

    
    oldest=-1e20
    youngest=+1e20

    for itau in itaus:
        if(ages[itau] < youngest):
            youngest=ages[itau]
            earlyTau=itau
            
        if(ages[itau] > oldest):
            oldest=ages[itau]
            latestTau=itau


    if(len(status) >= 1):
        lastTau=itaus[-1]
        latestCompleteTau=lastTau
        
    datataus=w2.Model2DataTaus(model,dtg)

    ndt=len(datataus)
    for n in range(0,ndt):
        datatau=datataus[n]

        goit=0
        for itau in itaus:
            if(datatau == itau):
                goit=1
                latestCompleteTau=datatau

        if(goit == 0):  break


    rc=[lastTau,gmpAge,oldest,latestTau,youngest,earlyTau,gmplastdogribmap,gmplatestTau,gmplastTau,latestCompleteTau]
    #print 'GetDataStatus rc: ',rc

    return(rc)
    
