#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class Cgd6CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
        }

        self.defaults={
            'model':'cgd6',
        }

        self.options={
            'resopt':     ['L',1,0,'low-res grid resolution -- cgd6 is model from archive'],
            'override':   ['O',0,1,'override'],
            'verb':       ['V',0,1,'verb=1 is verbose'],
            'ropt':       ['N','','norun',' norun is norun'],
            'tauopt':     ['t:',None,'a','set taus as tau1,tau2,...'],
            'dowget':     ['W',0,1,'do wget to get .tar from cmc'],
            'dols':       ['l',0,1,'do ls like l2.py'],
            
        }

        self.purpose='''
purpose -- dearchive & process cmc gdps global grids to w2flds'''
        self.examples='''
%s 2009050100
'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='cmc.gcd6-sfc-corr')
CL=Cgd6CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- M2 object
#
dmodelType='w2flds'
m=setModel2(model)

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=12)

for dtg in dtgs:

    fm=m.DataPath(dtg,dtype=dmodelType,dowgribinv=1,override=override,doDATage=1)
    fm.MakeFdb2(override=override)

    #fd=fm.GetDataStatus(dtg)

    fm.ls()
    continue

    fd.getEtau(dtg)
    
    endtau=fd.etau
    cmptau=fd.dslatestCompleteTauBackward 
    isdone=(endtau == cmptau and dtg[8:10] == '00')
    
    if(dols):
        print ' dtg:  ',dtg,' isdone:  ',isdone,' Maxtau: %5d'%(endtau),' Completed tau: %5d'%(cmptau)
        continue

MF.dTimer(tag='cmc.gcd6-sfc-corr')
