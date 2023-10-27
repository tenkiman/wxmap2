c23456789012345678901234567890123456789012345678901234567890123456789012    
c
      Subroutine rapidga_2010(perri,shdcri,d200ri,potri,
     +            rhlori,sbtri,pcri,rhcri,sname,atcfid,ismon,isday,
     +            isyr,istime,lush)
c
c     Subroutine rapidga_rerun.f
c     Last Updated: April 16, 2010 
c     Author: John Kaplan
c     Purpose: This subroutine is used to compute the 2010 operational
c              Atlantic RI index. The 2010 RI index provides estimates 
c              of the probability of RI for the 25,30,35 kt and 40 kt RI 
c              thresholds based upon the discriminant version of the 
c              RI index only. 
c
c     2010 RI index changes:  
c               
c     1) Model : The RII was re-derived using the updated 1995-2009 SHIPS
c                    data base.
c                The model was derived for the 40 kt RI threshold for the
c                first time this year. 
c     2) Print out: The probability of RI for the 40 kt threshold will
c                   be provided for the first time this year. Previously,
c                   only the probabilities for the 25, 30, and 35 kt thresholds
c                   were provided. 
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
c     Mwrite= The index number used to print out the scaled and weighted values on
c             the log sheet
c
      Parameter   (Nx=4)
      Parameter   (Nindx=4)
      Parameter   (Nthrss=8)
      Dimension   Rvar(Nthrss), sclvar(Nindx,Nthrss)
      Dimension   Sclvrd(Nindx,Nthrss)
      Dimension   Ratsc(nindx),Ratscd(nindx),prscld(nindx)
      Dimension   Rmnval(Nindx,Nthrss), Rmxval(Nindx,Nthrss)
      Dimension   Avgval(Nindx,Nthrss)
      Dimension   Sclav(Nindx,0:NX),  Prbri(Nindx,0:Nx)
      Dimension   Sclavd(Nindx,0:NX), Prbrid(Nindx,0:Nx)
      Dimension   Scale(Nindx), Scaled(Nindx), Suscld(Nindx)
      Dimension   Suscl(nindx), sumwgt(nindx), prscl(nindx)
      Dimension   dwgt(Nindx,Nthrss), Clrisc(Nindx)
      Dimension   Ithrs(Nindx)
c
      Character*6 Labdat(Nthrss)
      Character*8 atcfid
      Character*10 sname
      character*24 thlabs(nthrss)      
c
      Logical Flag(nindx), newper, operational
c
      Data sclmax /1.0/, Sclmin/0.0/
      Data ithrs /25,30,35,40/
      Data (rmnval(1,J),J=1,nthrss)/-45.0,3.2,-21.0,25.1,56.0,17.0,
     +  3.2,0.0/
      Data (rmnval(2,J),J=1,nthrss)/-45.0,3.2,-21.0,33.5,56.0,17.0,
     +  3.2,0.0/
      Data (rmnval(3,J),J=1,nthrss)/-45.0,3.3,-21.0,35.4,58.0,38.0,
     +  3.2,6.0/
      Data (rmnval(4,J),J=1,nthrss)/-45.0,3.3,-21.0,49.4,58.0,38.0,
     +  3.2,10.0/
      Data (rmxval(1,J),J=1,nthrss)/30.0,35.1,149.0,130.7,88.0,100.0,
     +  35.1,132.0/
      Data (rmxval(2,J),J=1,nthrss)/30.0,26.2,140.0,126.5,85.0,100.0,
     +  30.6,130.0/        
      Data (rmxval(3,J),J=1,nthrss)/25.0,20.3,125.0,121.4,84.0,100.0,
     +  26.1,130.0/
      Data (rmxval(4,J),J=1,nthrss)/25.0,20.3,125.0,121.4,82.0,100.0,
     +  26.0,130.0/
      Data (avgval(1,J),J=1,nthrss)/7.9,10.6,47.0,80.6,73.4,76.9,
     +  13.6,54.9/
      Data (avgval(2,J),J=1,nthrss)/8.5,10.3,48.2,80.1,73.6,79.2,
     +  12.6,55.8/
      Data (avgval(3,J),J=1,nthrss)/9.1,9.5,48.3,80.6,73.6,82.9,
     +  11.9,60.4/
      Data (avgval(4,J),J=1,nthrss)/9.0,9.4,49.3,80.1,73.6,84.5,
     +  11.1,64.1/
      Data (sclav(1,J),J=0,nx)/0.0,2.15,4.54,5.05,5.62/
      Data (sclav(2,J),J=0,nx)/0.0,1.66,4.56,5.08,5.64/
      Data (sclav(3,J),J=0,nx)/0.0,0.89,4.57,5.14,5.68/
      Data (sclav(4,J),J=0,nx)/0.0,0.69,4.62,5.19,5.79/
      Data (prbri(1,J),J=0,nx)/0.0,4.38,23.03,35.96,50.31/
      Data (prbri(2,J),J=0,nx)/0.0,2.65,17.04,29.61,37.86/
      Data (prbri(3,J),J=0,nx)/0.0,1.48,11.72,27.35,28.85/
      Data (prbri(4,J),J=0,nx)/0.0,1.0,11.06,18.85,30.77/
      Data (sclavd(1,J),J=0,nx)/0.0,3.97,7.80,8.51,9.24/
      Data (sclavd(2,J),J=0,nx)/0.0,2.59,6.62,7.31,8.11/
      Data (sclavd(3,J),J=0,nx)/0.0,1.18,5.55,6.22,6.93/
      Data (sclavd(4,J),J=0,nx)/0.0,0.71,4.81,5.65,6.52/        
      Data (prbrid(1,J),J=0,nx)/0.0,4.24,24.48,41.41,53.29/
      Data (prbrid(2,J),J=0,nx)/0.0,2.62,17.91,27.46,46.90/
      Data (prbrid(3,J),J=0,nx)/0.0,1.46,12.70,22.07,40.00/
      Data (prbrid(4,J),J=0,nx)/0.0,0.99,9.58,24.21,44.44/
      Data (dwgt(1,J),J=1,nthrss)/2.88,2.35,2.19,2.19,0.83,0.52,
     + 2.05,-0.03/
      Data (dwgt(2,J),J=1,nthrss)/3.01,1.70,2.06,1.00,0.85,0.17,
     + 2.37,0.11/
      Data (dwgt(3,J),J=1,nthrss)/2.58,1.57,2.00,0.69,0.03,-0.17,
     + 2.12,0.75/
      Data (dwgt(4,J),J=1,nthrss)/2.04,1.87,1.79,-0.98,0.07,-0.41,
     + 2.55,1.35/
c
      Data clrisc/12.6,8.1,4.8,3.4/ 
c
      Data newper/.false./, operational/.true./
      Data Thlabs /'12 HR PERSISTENCE (KT)','850-200 MB SHEAR (KT) ',
     +            'D200 (10**7s-1)         ','POT = MPI-VMAX (KT)',
     +            '850-700 MB REL HUM (%)','% area w/pixels <-30 C',
     +           'STD DEV OF IR BR TEMP ','Heat content (KJ/cm2)'/
      Data Labdat /'deltv6','shdc','d200','potint','rhl',
     +   'pxcnt','btstd','rhcn'/
c
      Rvar(1) = Perri
      Rvar(2) = shdcri
      Rvar(3) = d200ri
      Rvar(4) = potri
      Rvar(5) = rhlori
      Rvar(6) = pcri
      Rvar(7) = sbtri
      Rvar(8) = rhcri
c      write(40,*)'rvar(1)=',rvar(1),'rvar(2)=',rvar(2),'rvar(3)=',
c     +   rvar(3),'rvar(4)=',rvar(4),'rvar(5)=',rvar(5),'rvar(6)=',
c     +   rvar(6),'rvar(7)=',rvar(7),'rvar(8)=',rvar(8)  
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
       Do 555 M=1,nindx
       Sumwgt(M) = 0.0
       Do 550 K=1,nthrss       
           sumwgt(M) = sumwgt(M) + dwgt(M,K)
  550  Continue          
  555  Continue
c
       Do 565 M=1,nindx
        suscld(M) = 0.0
        Lcount    = 0 
         Do 560 L=1,nthrss
            If(sclvar(M,L).Lt.0)Sclvar(M,L)=0.0
            If(sclvar(M,L).lt.900)then
                Lcount   = Lcount + 1                       
                If(operational)then
                  sclvrd(M,L) = Float(nthrss)*dwgt(m,L)/sumwgt(M)
     +                         *sclvar(M,L)
                else
                  sclvrd(M,L) = sclvar(M,L)*dwgt(M,L)
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
  575 format(/,'   ** 2010 ATLANTIC RI INDEX',1x,a8,1x,a10,
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
  580  continue
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
      mwrite = 2
      Do 800 M=1,nindx
      If( M.eq.1 )then
          write(lush,591) ithrs(mwrite)
  591     format(11x,'( ',i2,
     +         ' KT OR MORE MAX WIND INCREASE IN NEXT 24 HR)')
c 
          Write(lush,*)
             Do 599 NN=1,nthrss
                 If(Labdat(NN).eq.'shdc'.or.Labdat(NN).eq.'btstd')then
                    Write(lush,598)thlabs(NN),rvar(NN),
     +                  rmxval(Mwrite,NN),rmnval(Mwrite,NN),
     +                  sclvar(Mwrite,NN),sclvrd(Mwrite,NN)
                 Else                  
                     Write(lush,598)thlabs(NN),rvar(NN),
     +               rmnval(Mwrite,NN),rmxval(Mwrite,NN),
     +               sclvar(Mwrite,NN),sclvrd(Mwrite,NN)
                 Endif
  598            Format(1x,A22,':',F6.1,' Range:',F5.1,
     +        ' to ',F5.1,' Scaled/Wgted Val:',F5.1,'/',F5.1)
  599        Continue
      Endif         
c
c              write(lush,*)
c              Write(lush,645)scale(m),nint(prscl(m)),ratsc(m),
c     +          clrisc(m)
c  645         Format(1x,'Scaled RI index=  ',F6.2,' Prob of RI=',
c     +        I4,'% is ',F5.1, ' times the sample mean(',f4.1,'%)')
      If(M.eq.1)then       
              write(lush,*)
c              write(lush,660)suscld(m),nint(prscld(m)),ratscd(m),
c     +	     clrisc(m)
c
             iprobt = nint(prscld(m))
             if (iprobt .gt. 95 .and. iprobt .lt. 900) iprobt = 95
             write(lush,680) ithrs(M),iprobt,ratscd(m),
     +	                     clrisc(m)
c               
c  660        Format(1x,'Discrim RI index= ',F6.2,' Prob of RI=',I4,
c     + '% is ',F5.1,' times the sample mean(',F4.1,'%)')
c
      Else
c            If(M.eq.2)then
c              write(lush,*)
c            Endif
c
             iprobt = nint(prscld(m))
             if (iprobt .gt. 95 .and. iprobt .lt. 900) iprobt = 95
             write(lush,680) ithrs(M),iprobt,ratscd(m),
     +	                     clrisc(m)
  680        Format(1x,'Prob of RI for',I3,' kt RI threshold= ',
     + i5,'% is ',F5.1,' times the sample mean(',F4.1,'%)')
c    + F5.1,'% is ',F5.1,' times the sample mean(',F4.1,'%)')
      Endif
c
  800  Continue
c  
c
       return
       end
c
