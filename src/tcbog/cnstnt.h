*comdeck cnstnt
      include 'param.h'
c
      parameter (lccn= 400+lm*(12+5*lm)) 
c        
c  ********************************************************************
c
      dimension ccn(lccn)        
      equivalence (c,ccn)     
c
      common/cnstnt/ c(300),itau,ithist,idtg(3),sarray(lm,lm)
     *, carray(lm,lm),evecin(lm,lm),evectr(lm,lm),tmcor(lm,lm)        
     *, eigval(lm),spalm(lm),pmcor(lm),pbcor(lm),tmean(lm)  
     *, asig(lmp1),bsig(lmp1),dasig(lm),dbsig(lm) 
     *, sige(lmp1),dsig(lm),dpres(lm),ptmean,ccpad(100)      
c         
     *, cim(mlmax),eps4(mlmax),thatm(lmm1)   
     *, ocos(jm),weight(jm),asd(lm,lm),cosl(jm),sinl(jm)
     *, mlsort(jtrun,jtrun),msort(mlmax),lsort(mlmax)
c         
c  *******************************************************************
c
      logical forwrd,prnt,nozone,sstclm,updayc,incrup,incwnd     
     *, ecadv,hybrd,skew,tseres,crosc,prftop,dinit,ops,prntij
     *, fluxcl,mombdg,pcmdi,eccld
c         
      character*8 cdtg,ipdtg,idx,cdtgoi,dtgpcm         
      character*10 dtgfnoc
ccc      equivalence (idtg(2),dtgfnoc)
ccc      equivalence (idtg,cdtg) 
c         
c         
c  ********************************************************************
c
      common/dgcons/
c
c  skewt parameters
c
     * tausk,ijskew(100),sklat(100),sklon(100)
c
c  time series parameters (atmosphere)
c
     *, ijts(100),tslat(100),tslon(100),idts1(100),idts2(100)
c
c  cross section parameters
c
     *, taucs,cslat1(20),cslat2(20),cslat3(20),cslat4(20)
     *, cslat5(20),cslon1(20),cslon2(20),cslon3(20),cslon4(20)
     *, cslon5(20),idcs1(20),idcs2(20)
c
c  physics diagnostics
c
     *, tauph,phlat(20),phlon(20),latjs(20),latjn(20)
     *, loniw(20),lonie(20)
c
c  tops profiles (and gridpoint prints if prntij=true)
c
     *, tautop,ijtops(100),toplon(100),toplat(100)
c
c  ********************************************************************
c    
c  input and output file names
c
      common/ffiles/ ifilin,ifilo1,ifilo2,mastops,dgfile,ocards
     *, namlsts,hstdir,pstdir(2)
     *, gaufil,spgeo,uaclim,climof,lsice
     *, lsifil,topfil1,topfil2,topcur,ocnclim,qsfile,crdate
     *, pcmsst,pcmice,fident,pshp12(5)
c
      character*48  ifilin,ifilo1,ifilo2,mastops,dgfile,ocards
     *, namlsts,hstdir,pstdir1,pstdir2,pstdir
     *, gaufil,spgeo,uaclim,climof,lsice
     *, lsifil,topfil1,topfil2,topcur,ocnclim,qsfile,crdate
     *, pcmsst,pcmice,fident,pshp12
      equivalence (pstdir1,pstdir(1)),(pstdir2,pstdir(2))
c
c  ********************************************************************
c
      common/clkcom/ rtime(2,25)
c         
      dimension rjobtm(2),rtfcst(2),rtnm(2),rts2p(2),rtp2s(2),rtget(2)
     *, rtrs(2),rtsr(2),rtfft(2),ftsort(2),rtpres(2),rtcmp3(2),rtdiag(2)
     *, rtimpl(2),rtops(2),rtlsp(2),rtmsta(2),rtlwr(2),rtswr(2),rtpbl(2)
     *, rtshcu(2),rtcuml(2),rtcup(2),rtkern(2),rtlamd(2)
c
      equivalence   
     *  (rtime(1,1),rjobtm),  (rtime(1,2),rtfcst),  (rtime(1,3),rtnm)      
     *, (rtime(1,4),rts2p),   (rtime(1,5),rtp2s),   (rtime(1,6),rtget)     
     *, (rtime(1,7),rtrs),    (rtime(1,8),rtsr),    (rtime(1,9),ftfft)     
     *, (rtime(1,10),ftsort), (rtime(1,11),rtpres), (rtime(1,12),rtcmp3)   
     *, (rtime(1,13),rtdiag), (rtime(1,14),rtimpl), (rtime(1,15),rtops)    
     *, (rtime(1,16),rtlsp),  (rtime(1,17),rtmsta), (rtime(1,18),rtlwr)    
     *, (rtime(1,19),rtswr),  (rtime(1,20),rtpbl),  (rtime(1,21),rtshcu)   
     *, (rtime(1,22),rtcuml), (rtime(1,23),rtcup),  (rtime(1,24),rtkern)   
     *, (rtime(1,25),rtlamd)    
c     
c
c  ********************************************************************
c
