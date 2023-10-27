import mf

def modtitle(tau,model,bdtg,t1top=None,t2top=None,res=1.0):

    #if(t1top != None):
    #    self.toptitle(t1top,t2top,1.0,1,1)
    
    tres="`2%3.1f0`3.`0 Fields`0"%(res)
    
    if(model == 'gfs' and t1top != None):
        gcmd="draw string 0.2 8.30 NCEP GFS (T382(N286)L64)  %s run %s `3t`0 = %3d h"%(bdtg,tres,tau)
        
    elif(model == 'fim8' and t1top != None):
        gcmd="draw string 0.2 8.30 ESRL FIM (G8(30km)L64)  %s run %s `3t`0 = 'ttau' h"%(bdtg,tres,tau)
    else:
        gcmd=''
    
            
    return(gcmd)


def dtitle(t1):

    gcmd="""
set line 0
draw recf 0.05 0.05 10.95 0.35
set strsiz 0.15 0.18
set string 3 l _cthkt
#
# bottom title verify time + product desc
#
draw string 0.2 0.46 Verify: mydate()
set string 3 r _cthkt
set strsiz 0.12
draw string 10.80 0.46 t1

set strsiz 0.15 0.18

draw recf 0.05 8.15 10.95 8.50

set string 2 l _cthkt

rc=modtitle()

return"""





