c23456789012345678901234567890123456789012345678901234567890123456789012    
c
      Subroutine rapidga_2011(perri,shdcri,d200ri,potri,
     +            rhlori,sbtri,pcri,rhcri,sname,atcfid,ismon,isday,
     +            isyr,istime,lush)
c
c     Subroutine rapidga_rerun.f
c     Last Updated: May 10, 2011 
c     Author: John Kaplan
c     Purpose: This subroutine is used to compute the 2011 operational
c              Atlantic RI index. The 2011 RI index provides estimates 
c              of the probability of RI for the 25,30,35 kt and 40 kt RI 
c              thresholds based upon the discriminant version of the 
c              RI index only. 
c
c     2011 RI index changes:  
c               
c     1) Model : The RII was re-derived using the updated 1995-2010 SHIPS
c                    data base.
c
c     2) Print out:  The predictors are now printed out in the order of
c                    their average weight for all 4 RI thresholds
c    
c     Subroutine inputs: perri,shdcri,d200ri,potri,rhlori,
c                        sbtri,pcri,rhcri,sname,ismon,isday,isyr,
c                        istime, and lush
c
c     Subroutine  ouputs: scale,prbscl,pratsc
c
c     Notes:  This subroutine assumes that missing input values 
c            are > 900. (e.g., perri=999. if missing). Also, 
c            missing output values will be coded as 999.
c             
c      
c     perri : 12 h intensity change observed for the preceding 12 h (kt)
c     shdcri: 850-200 mb vertical shear (kt) computed from 0-500 km radius 
c             after the vortex has been removed and averaged from T=0 to T=24 h   
c     d200ri: 200 mb divergence (10**-7s-1) from 0-1000 km averaged from 
c             T=0 to T=24 h
c     potri : Potential intensity (kt) averaged from T=0 to T=24 h.
c             The MPI that is used when computing the potential intensity 
c             is determined using Joe Cione's inner-core cooled SST (number 3). 
c             This MPI also accounts for storm speed based upon the algorithm 
c             developed by Schwerdt et al. (1979) and is capped at 165 kt.              
c     rhlori: 850-700 mb relative humidity (%) from 200-800 km radius   
c             averaged from T=0 to T=24 h
c     sbtri : std. dev. of the 50-200 km GOES channel 4 brightness 
c             temperatures at t=0 h
c     pcri  : % area from 50-200 radius with GOES channel 4 brightness 
c             temperatures <-30 C at t=0 h
c     rhcri : Reynolds heat content (kj/cm2) averaged from t=0 to t=24 h
c     sname : Storm name (A10)
c     atcfid: ATCF storm ID (A8)
c     ismon : Month of forecast (I2)
c     Isday : Day of month of forecast (I2)
c     Isyr  : Year of forecast (I2)
c     istime: Time of day of forecast (UTC) (I2)
c     lush  : Output unit number of SHIPS log file 
c     scale : The magnitude of the computed scaled RI index (Range: 0-7).
c     prbscl: The probability of RI (%) computed based upon the magnitude
c             of the scaled RI index (scale).
c     pratsc: The ratio of the probabilty of RI (prbscl) and the dependent sample mean
c             probability of RI (clrisc)
c     Rvar  : Array containing the predictor magnitudes of each of the RI predictors.
c     sclvar: Array containing the scaled magnitudes of each RI predictor.
c     sclvrd: Array containing the scaled discriminant magnitudes of each RI predictor.
c     rmnval: Array containg the min. value at which RI occured for each RI predictor
c     rmxval: Array containg the max. value at which RI occured for each RI predictor
c     avgval: The mean value at which RI occurred for each RI predictor
c     sclav : The binned magnitudes of the scaled RI index
c     prbri : The magnitudes of the RI probabilites for each of the binned scaled RI
c             values found in the array sclavg.
c     sclavd: The binned magnitudes of the scaled RI index
c     prbrid: The magnitudes of the RI probabilites for each of the binned scaled RI
c             values found in the array sclavg.
c     Nindx = number of RI index thresholds computed
c     Nthrss= number of RI predictors
c     Mwrite= The index number used to print out the scaled and weighted values on
c             the log sheet
c     rvarsrt: array containg sorted RI variables
c     labsrt : Character array containing RI predictor labels
c     labdatsrt: Character array containing truncated predictor labels
c     totwgt: Array containing weights of each of the predictors for all RI thresholds
c     totalwgt: Array containing sum of the weights of each predictor for all 4 RI thresholds
c
      Parameter   (Nx=4)
      Parameter   (Nindx=4)
      Parameter   (Nthrss=8)
      Dimension   Rvar(Nthrss), sclvar(Nindx,Nthrss)
      Dimension   Rvarsrt(Nindx,Nthrss)
      Dimension   Sclvrd(Nindx,Nthrss)
      Dimension   Ratsc(nindx),Ratscd(nindx),prscld(nindx)
      Dimension   Rmnval(Nindx,Nthrss), Rmxval(Nindx,Nthrss)
      Dimension   Avgval(Nindx,Nthrss)
      Dimension   Sclav(Nindx,0:NX),  Prbri(Nindx,0:Nx)
      Dimension   Sclavd(Nindx,0:NX), Prbrid(Nindx,0:Nx)
      Dimension   Scale(Nindx), Scaled(Nindx), Suscld(Nindx)
      Dimension   Suscl(nindx), sumwgt(nindx), prscl(nindx)
      Dimension   dwgt(Nindx,Nthrss), Clrisc(Nindx)
      Dimension   totwgt(nindx,Nthrss)
      Dimension   totalwgt(nthrss)
      Dimension   Ithrs(Nindx)
c
      Character*6 Labdat(Nthrss)
      Character*6 Labdatsrt(nindx,nthrss), labdattmp
      character*24 thlabs(nthrss)      
      Character*24 labsrt(nindx,nthrss)
      Character*24 Labtmp
      Character*8 atcfid
      Character*10 sname
c
      Logical Flag(nindx), newper, operational
c
      Data sclmax /1.0/, Sclmin/0.0/
      Data ithrs /25,30,35,40/
c
      DATA (rmnval(1, j), j = 1, nthrss)
     *  /-21.0, 25.1,  3.2, 56.0,-45.0, 17.0,  3.2,  0.0/
      DATA (rmxval(1, j), j = 1, nthrss)
     *  /169.0,130.7, 35.1, 88.0, 30.0,100.0, 35.1,132.0/
      DATA (avgval(1, j), j = 1, nthrss)
     *  / 47.4, 81.2, 10.4, 72.9,  8.1, 76.4, 14.0, 54.0/
      DATA (rmnval(2, j), j = 1, nthrss)
     *  /-21.0, 33.8,  3.2, 56.0,-45.0, 17.0,  3.2,  0.0/
      DATA (rmxval(2, j), j = 1, nthrss)
     *  /165.0,126.5, 26.2, 85.0, 30.0,100.0, 34.1,130.0/
      DATA (avgval(2, j), j = 1, nthrss)
     *  / 48.1, 80.7, 10.0, 73.0,  8.6, 78.7, 13.0, 54.4/
      DATA (rmnval(3, j), j = 1, nthrss)
     *  /-21.0, 35.4,  3.3, 57.0,-45.0, 30.0,  3.2,  3.0/
      DATA (rmxval(3, j), j = 1, nthrss)
     *  /125.0,121.4, 20.3, 84.0, 25.0,100.0, 27.5,130.0/
      DATA (avgval(3, j), j = 1, nthrss)
     *  / 47.7, 80.2,  9.2, 73.0,  9.3, 82.1, 12.1, 57.5/
      DATA (rmnval(4, j), j = 1, nthrss)
     *  /-21.0, 49.4,  3.3, 57.0,-45.0, 38.0,  3.2, 10.0/
      DATA (rmxval(4, j), j = 1, nthrss)
     *  /125.0,121.4, 20.3, 82.0, 25.0,100.0, 26.0,130.0/
      DATA (avgval(4, j), j = 1, nthrss)
     *  / 48.0, 79.6,  9.1, 73.3,  9.2, 84.1, 11.4, 61.0/
      DATA (dwgt(1, j), j = 1, nthrss)
     *  / 2.28, 2.15, 2.43, 0.57, 3.11, 0.63, 1.55,-0.08/
      DATA (dwgt(2, j), j = 1, nthrss)
     *  / 2.09, 1.10, 1.90, 0.58, 3.27, 0.44, 2.08,-0.03/
      DATA (dwgt(3, j), j = 1, nthrss)
     *  / 1.56, 0.63, 1.86, 0.16, 2.98,-0.11, 2.14, 0.60/
      DATA (dwgt(4, j), j = 1, nthrss)
     *  / 0.92,-1.17, 2.17, 0.67, 2.17,-0.47, 2.32, 1.05/
      DATA (sclav (1, j), j = 0, nx)
     *  / 0.00,   2.13,   4.47,   4.99,   5.55/
      DATA (prbri (1, j), j = 0, nx)
     *  / 0.00,   4.60,  21.80,  34.59,  49.72/
      DATA (sclavd (1, j), j = 0, nx)
     *  / 0.00,   3.90,   7.56,   8.21,   8.88/
      DATA (prbrid (1, j), j = 0, nx)
     *  / 0.00,   4.39,  24.15,  41.82,  52.63/
      DATA (sclav (2, j), j = 0, nx)
     *  / 0.00,   1.70,   4.50,   5.02,   5.56/
      DATA (prbri (2, j), j = 0, nx)
     *  / 0.00,   2.80,  16.57,  28.30,  36.59/
      DATA (sclavd (2, j), j = 0, nx)
     *  / 0.00,   2.74,   6.76,   7.45,   8.18/
      DATA (prbrid (2, j), j = 0, nx)
     *  / 0.00,   2.76,  16.48,  27.15,  48.39/
      DATA (sclav (3, j), j = 0, nx)
     *  / 0.00,   1.08,   4.59,   5.12,   5.69/
      DATA (prbri (3, j), j = 0, nx)
     *  / 0.00,   1.55,  11.36,  24.49,  26.32/
      DATA (sclavd (3, j), j = 0, nx)
     *  / 0.00,   1.51,   5.90,   6.57,   7.29/
      DATA (prbrid (3, j), j = 0, nx)
     *  / 0.00,   1.53,  11.58,  21.82,  38.46/
      DATA (sclav (4, j), j = 0, nx)
     *  / 0.00,   0.63,   4.51,   5.07,   5.65/
      DATA (prbri (4, j), j = 0, nx)
     *  / 0.00,   1.02,   9.58,  18.66,  22.22/
      DATA (sclavd (4, j), j = 0, nx)
     *  / 0.00,   0.75,   4.75,   5.46,   6.19/
      DATA (prbrid (4, j), j = 0, nx)
     *  / 0.00,   0.98,  10.04,  25.00,  40.68/
c
       Data clrisc/12.8,8.4,5.0,3.4/ 
       Data newper/.false./, operational/.false./
       Data Thlabs /'D200 (10**7s-1)         ','POT = MPI-VMAX (KT)',
     +             '850-200 MB SHEAR (KT) ','850-700 MB REL HUM (%)',
     +             '12 HR PERSISTENCE (KT)', '% area w/pixels <-30 C', 
     +             'STD DEV OF IR BR TEMP ','Heat content (KJ/cm2)'/
c    
      Data Labdat /'d200','potint','shdc','rhl','deltv6',
     +   'pxcnt','btstd','rhcn'/

c
      Rvar(1) = d200ri
      Rvar(2) = potri
      Rvar(3) = shdcri
      Rvar(4) = rhlori
      Rvar(5) = Perri
      Rvar(6) = pcri
      Rvar(7) = sbtri
      Rvar(8) = rhcri
c
      Do 250 M=1,nindx
          Do 200 N=1,nthrss
               If(Rvar(N).lt.900)then
                   If(Labdat(N).eq.'deltv6' .and. newper)then
                       If(Rvar(N) .LE. Avgval(M,N))then
                          Sclvar(M,N) = 1 -  
     +                  ((Avgval(M,N)- Rvar(N))/
     +                  (avgval(M,N) - rmnval(M,N)))
                       Else
                          Sclvar(M,N) = 1 -  
     +                  ((Rvar(N) - Avgval(M,N))/
     +                  (rmxval(M,N) - avgval(M,N)))  
                       endif
                   Elseif(labdat(N).eq.'shdc'.or. 
     +                    labdat(n).eq.'btstd')then
                        Sclvar(M,N) =  (Rmxval(M,N)  - Rvar(N))/
     +                              (Rmxval(M,N) - Rmnval(M,N)) 
                   Elseif(Labdat(N).eq.'d200'.or.labdat(N).eq.
     +                   'potint'.or.labdat(N).eq.'rhl'.or.
     +                   labdat(N).eq.'pxcnt'.or.
     +                   labdat(N).eq.'deltv6'.or.
     +                   labdat(N).eq.'rhcn')then
                          If(labdat(N).eq.'deltv6' .and. 
     +                        newper)go to 200
                          Sclvar(M,N)=(Rvar(N) - Rmnval(M,N))/
     +                            (Rmxval(M,N) - Rmnval(M,N))
                   Endif   
               Else
                   Sclvar(M,N) = 999.
               Endif
  200     Continue
  250 Continue
        Do 350 M=1,nindx
            Flag(M)  = .false.
            Scale(M) =  0.0
            Scaled(M)=  0.0
            Do 290 NN=1,nthrss
                If(Sclvar(M,NN).gt.900)then
                     Flag(m) = .true.
                     go to 350
                Endif
  290       Continue
             Do 300 NN=1,nthrss
                 If(Sclvar(M,NN).Gt.sclmax)then
                     Sclvar(M,NN) = Sclmax
                 Elseif(sclvar(M,NN).lt.sclmin)then
                     Scale(M) = 0.
                     Scaled(M)= 0.
                     Sclvar(M,NN) = Sclmin
                     Go to 350
                 Endif
                 Scale(m)  = Scale(m)  + Sclvar(M,NN)
                 Scaled(m) = Scaled(m) + Sclvar(M,NN)*dwgt(M,NN)
  300        Continue      
  350  Continue
       Do 540 M=1,nindx
       If(.not.flag(m))then
           Do 500 n=0,nx-1
               If(Scale(M).Ge.Sclav(M,nx))then
                 prscl(M) = prbri(M,nx-1) + ( (prbri(M,nx) - 
     +	         prbri(M,nx-1))/(Sclav(M,nx) - Sclav(M,nx-1))*
     +                     (Scale(M) - Sclav(M,nx-1)) )                
               Elseif(Scale(m).ge.sclav(m,n) .and.
     +                scale(m).lt.sclav(m,n+1))then
                   If(n.gt.0)then                    
                         Prscl(M)= Prbri(M,n) + 
     +                          ( (Prbri(M,n+1) - Prbri(M,n))/ 
     +     (sclav(m,n+1) - Sclav(m,n))*(Scale(M)-Sclav(m,n)) )
                   Elseif(n.eq.0)then
                         Prscl(M) = prbri(M,1)
                   Endif
               Endif
  500      Continue                 
           If(prscl(M).gt.100.)prscl(M)=100.
                  ratsc(m) = prscl(M)/clrisc(M)
           Do 525 n=0,nx-1
               If(Scaled(M) .Ge. Sclavd(m,nx))then
                  prscld(M) = prbrid(M,nx-1) + ( (prbrid(M,nx) - 
     +            prbrid(M,nx-1))/
     +                 (Sclavd(M,nx) - Sclavd(M,nx-1))*
     +                 (Scaled(M) - Sclavd(M,nx-1)) )                
               Elseif(Scaled(M) .ge. sclavd(m,n) .and.
     +                scaled(M).lt.sclavd(m,n+1))then
                  If(N.gt.0)then
                           Prscld(M) = Prbrid(m,n) + 
     +      	           ((Prbrid(m,n+1) - Prbrid(m,n))/ 
     +    (sclavd(m,n+1) - Sclavd(m,n))*(Scaled(M)-Sclavd(m,n)) )
                  Elseif(N.eq.0)then
                      prscld(M) = Prbrid(M,1)
                  Endif
               Endif
  525     Continue                 
           If(prscld(M).gt.100.)prscld(M)=100.
                  ratscd(M) = prscld(M)/clrisc(M)
         Else
            Scale(M)  = 999.
            Prscl(M)  = 999.
            ratsc(M)  = 999.
            Scaled(M) = 999.
            Prscld(M) = 999.
            ratscd(M) = 999.
         Endif
  540  Continue
c 
c      Calculate relative weights of the discrminant predictors
c
       Do 545 M=1,nindx
       Sumwgt(M) = 0.0
       Do 541 K=1,nthrss       
           sumwgt(M) = sumwgt(M) + dwgt(M,K)
  541  Continue          
  545  Continue
c
       Do 565 M=1,nindx
        suscld(M) = 0.0
        Lcount    = 0 
         Do 560 L=1,nthrss
            If(sclvar(M,L).Lt.sclmin 
     +            .and. .not.flag(m)) Sclvar(M,L)=sclmin
            If(sclvar(M,L).gt.sclmax
     +            .and. .not.flag(m)) Sclvar(M,L)=sclmax
            If(sclvar(M,L).lt.900)then
                Lcount   = Lcount + 1                       
                If(operational)then
                  sclvrd(M,L) = Float(nthrss)*dwgt(m,L)/sumwgt(M)
     +                         *sclvar(M,L)
                else
                  sclvrd(M,L) =  sclvar(M,L)*dwgt(M,L)
                Endif
                suscld(M) = suscld(M) + sclvrd(M,L)
            Else
               sclvrd(M,L)  = 999.
            Endif     
  560    continue
c
         If(Lcount.lt.nthrss)suscld(M) = 999.
         If(scaled(M).eq.0)suscld(M)=0.0
  565  Continue
       
c
      write(lush,575) atcfid,sname,ismon,isday,isyr,istime
  575 format(/,'   ** 2011 ATLANTIC RI INDEX',1x,a8,1x,a10,
     +       1x,i2.2,'/',i2.2,'/',i2.2,2x,i2.2,' UTC **')
c
c            Check to insure that probri25 > probri30 >probri35 > probri40)
c            and correct probabilities based on the 
c            climatological rate of RI
c
      Do 580 N=1,nindx-1
         If(prscld(N).lt.prscld(N+1))then
            prscld(N)   = prscld(N)   + (clrisc(N)-clrisc(N+1))
            prscld(N+1) = prscld(N+1) - (clrisc(N)-clrisc(N+1))
         Endif   
  580 continue
c 
      Do 585 N=1,nindx-1
        If(prscld(N+1) .gt. prscld(N)) then
            prscld(N+1)=prscld(N)
        Endif
  585 Continue
c 
      Do 590 N=1,nindx
        If(.not.flag(N))then
          If(prscld(N).gt.100)prscld(N)=100.
          If(prscld(N).lt.0)prscld(N)  =0.0
        Endif
  590 continue
c
c         Sort weights for printing purposes
c       go to 688
c
      Do 625 JJ=1,nthrss
          totalwgt(JJ) = 0.
          Do 600 II=1,nindx
              totalwgt(JJ) = totalwgt(JJ) + 
     +                      abs(dwgt(II,JJ))
  600     continue
  625 Continue   
c
      Do 650 m=1,nindx
         Do 640 kk=1,nthrss
             rvarsrt(m,kk)   = rvar(kk)
             labsrt(m,kk)    = thlabs(kk)
             labdatsrt(m,kk) = labdat(kk)
             totwgt(m,kk)    = totalwgt(kk)
  640    continue
  650 continue
c
        Do 675 m=1,nindx
            Do 670 J=1,nthrss-1
                    K = nthrss - J
               Do 660 L=1,K
                 If(totwgt(m,L).lt.totwgt(m,L+1))then   
                     tottmp      = totwgt(m,L)
                     wgttmp      = dwgt(M,L)
                     rmntmp      = rmnval(M,L)
                     rmxtmp      = rmxval(M,L)
                     scltmp      = sclvar(M,L)
                     sclvrdtmp   = sclvrd(M,L)
                     labtmp      = labsrt(M,L)
                    labdattmp    = labdatsrt(M,L)
                     vartmp      = rvarsrt(M,L)
                     totwgt(m,L)  = totwgt(m,L+1)
                     dwgt(m,L)   = dwgt(m,L+1)
                    rmnval(m,L)  = rmnval(m,L+1)
                    rmxval(m,L)  = rmxval(m,L+1)
                    sclvar(m,L)  = sclvar(M,L+1)
                    sclvrd(m,L)  = sclvrd(M,L+1)
                    labsrt(M,L)  = labsrt(M,L+1)
                    rvarsrt(M,L) = rvarsrt(M,L+1)
                  labdatsrt(M,L) = labdatsrt(M,L+1)
                     totwgt(m,L+1) = tottmp
                     dwgt(m,L+1) = wgttmp
                     rmnval(m,L+1)= rmntmp
                     rmxval(m,L+1)= rmxtmp
                     sclvar(m,L+1)= scltmp
                     sclvrd(m,L+1)= sclvrdtmp
                     labsrt(m,L+1) = labtmp
                     rvarsrt(m,L+1)= vartmp
                     totwgt(m,L+1)  = tottmp
                    labdatsrt(m,L+1) = labdattmp                    
                 endif
  660          continue
  670       continue
  675   continue
c
  
      mwrite = 2
      Do 800 M=1,nindx
      If( M.eq.1 )then
c         write(lush,691) ithrs(mwrite)
  691     format(11x,'( ',i2,
     +         ' KT OR MORE MAX WIND INCREASE IN NEXT 24 HR)')
          write(lush,*)
c 
             Do 699 NN=1,nthrss
                 If(Labdatsrt(mwrite,NN).eq.'shdc'.or.
     +              Labdatsrt(mwrite,NN).eq.'btstd')then
                    Write(lush,698)labsrt(mwrite,NN),
     +              rvarsrt(mwrite,NN),
     +              rmxval(Mwrite,NN),rmnval(Mwrite,NN),
     +             sclvar(Mwrite,NN),sclvrd(Mwrite,NN)
                 Else                  
                     Write(lush,698)labsrt(mwrite,NN),
     +                rvarsrt(mwrite,NN),
     +               rmnval(Mwrite,NN),rmxval(Mwrite,NN),
     +               sclvar(Mwrite,NN),sclvrd(Mwrite,NN)
                 Endif
  698            Format(1x,A22,':',F6.1,' Range:',F5.1,
     +        ' to ',F5.1,' Scaled/Wgted Val:',F5.1,'/',F5.1)
  699        Continue
      Endif         
c
      If(M.eq.1)then       
              write(lush,*)
             iprobt = nint(prscld(m))
             if (iprobt .gt. 95 .and. iprobt .lt. 900) iprobt = 95
             write(lush,680) ithrs(M),iprobt,ratscd(m),
     +	                     clrisc(m)
c               
      Else
c
             iprobt = nint(prscld(m))
             if (iprobt .gt. 95 .and. iprobt .lt. 900) iprobt = 95
             write(lush,680) ithrs(M),iprobt,ratscd(m),
     +	                     clrisc(m)
  680        Format(1x,'Prob of RI for',I3,' kt RI threshold= ',
     + i5,'% is ',F5.1,' times the sample mean(',F4.1,'%)')
      Endif
c
  800  Continue

c     Open file for write (RI Probs) for p25, p30, p35 and p40
c     added by CAS (NOAA/NHC) 5/18/2011

       ip25 = nint( prscld(1) )
       ip30 = nint( prscld(2) )
       ip35 = nint( prscld(3) )
       ip40 = nint( prscld(4) )

       open(29, file="rivalues.dat", action="write", status="replace")
       write(29,*) ip25, ip30, ip35, ip40
       close(29)
c
       return
       end
c
