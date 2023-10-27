from M import *

class ClimoFld(MFbase):

    byear=1959
    ctype='cmean'
    ctlfile='cmean_1d.ctl'

    def __init__(self,bdir=None):

        self.ctype=self.ctype
        if(bdir == None):
            print 'EEE cm2.ClimoFld - you must provide a bdir when instantiating...'
            sys.exit()
        self.bdir=bdir
        self.ddir="%s/%s"%(self.bdir,self.ctype)
        self.byear=self.byear
        self.ctlfile=self.ctlfile
        self.ctlpath="%s/%s"%(self.ddir,self.ctlfile)



class ClimoFldWMO(ClimoFld):

    byear=25655
    ctype='era-dailyclim'
    ctlfileUV='all-wind-mean.ctl'
    ctlfileWS='all-windspeed-mean.ctl'
    ctlfileMS='all-mass-mean.ctl'
    gravity=9.80665 

    def __init__(self,bdir=None):

        self.ctype=self.ctype
        if(bdir == None):
            print 'EEE cm2.ClimoFld - you must provide a bdir when instantiating...'
            sys.exit()
        self.bdir=bdir
        self.ddir="%s/%s"%(self.bdir,self.ctype)
        self.byear=self.byear
        self.ctlpathUV="%s/%s"%(self.ddir,self.ctlfileUV)
        self.ctlpathWS="%s/%s"%(self.ddir,self.ctlfileWS)
        self.ctlpathMS="%s/%s"%(self.ddir,self.ctlfileMS)



    

    
        

    
