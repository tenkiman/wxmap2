from WxMAP2 import *
w2=W2()

class MfTrkAreaNhem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=0.0,
                 latN=80.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)


class MfTrkAreaShem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=0.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)


class MfTrkAreaGlobal(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=60.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)


#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded methods


def getCtlpathTaus(sbdir,model,dtg,maxtau=168):
    
    def getNfields(wgribs,verb=1):

        nfields={}

        for wgrib in wgribs:
            (dir,file)=os.path.split(wgrib)
            tt=file.split('.')
            tau=tt[len(tt)-3][1:]
            nf=len(open(wgrib).readlines())
            nfields[int(tau)]=nf

        return(nfields)


    def gettaus(gribs,verb=0):

        datpaths={}
        taus=[]
        gribver=None
        gribtype=None

        for grib in gribs:
            (dir,file)=os.path.split(grib)
            tt=file.split('.')
            tau=tt[len(tt)-2][1:]
            gribtype=tt[len(tt)-1]
            gribver=gribtype[-1:]
            siz=MF.GetPathSiz(grib)
            if(siz > 0):
                tau=int(tau)
                taus.append(tau)
                datpaths[tau]=grib
                if(verb): print file,tau,gribtype,gribver

        taus=MF.uniq(taus)

        return(taus,gribtype,gribver,datpaths)

    # -- hard wire for 2011073000 test
    #
    sdir="%s/%s/%s"%(sbdir,model,dtg)
    ctlpath='%s/%s.w2flds.%s.ctl'%(sdir,model,dtg)
    print 'sss ',sdir
    gribs=glob.glob("%s/*.grb?"%(sdir))
    wgribs=glob.glob("%s/%s*.wgrib?.txt"%(sdir,model))
    (taus,gribtype,gribver,datpaths)=gettaus(gribs)
    nfields=getNfields(wgribs)


    return(ctlpath,taus,nfields)


