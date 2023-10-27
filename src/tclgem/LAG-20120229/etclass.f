      subroutine etclass(mft,isst,it150,iepos,itgrd,iv500,iv300,ishdc,
     +                   iv20c,cyt,cmagt,igoes,imiss,rmiss,ioper,stype)
c     The routine uses a discrimant analysis to determine the storm type
c     (tropical, subtropical, extratropical)
c
c     Passed variables
      dimension isst(0:mft),it150(0:mft),iepos(0:mft),itgrd(0:mft)
      dimension iv500(0:mft),iv300(0:mft),ishdc(0:mft),iv20c(0:mft)
      dimension cyt(-2:mft),cmagt(-2:mft)
      dimension igoes(0:mft)
c
      character *4 stype(0:mft)
c
c     Local variables
      parameter (mvda=50,mgda=10,mftl=20)
      dimension dfcoef(0:mvda,mgda,0:mftl)
      dimension dfinp(0:mvda)
      dimension dfval(mgda)
      character *256 fncol
      character *256 coef_location
c
c     Set default to not available
      do k=0,mft
         stype(k) = ' N/A'
      enddo
c
c     Open and read the discriminant analysis coefficients
      lucof = 26
      if (ioper .eq. 1) then
c        get SHIPS_COEF env variable
         call getenv( "SHIPS_COEF",coef_location )
         fncol=trim( coef_location )//'etclass.dat'
      else
         fncol='etclass.dat'
      endif
c
      open(file=fncol,unit=lucof,form='formatted',
     +     status='old',err=900) 
c    
c     Read the header line
      read(lucof,*,err=900,end=900) it1,it2,idelt,nvar,ngrp
c
c     Read the coefficients
      do k=0,mft
      do j=0,nvar
         read(lucof,*,err=900,end=900) idum1,(dfcoef(j,m,k),m=1,ngrp)
      enddo
      enddo
c
c     Start the main time loop
      do k=0,mft
         nmissing = 0
c
c        Assemble input data
c    
c        0 Constant term
         dfinp(0) = 1.0
c
c        1 SST
         if (isst(k) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp( 1) = 0.1*float(isst(k))
         endif
c
c        2 T150
         if (it150(k) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp( 2) = 0.1*float(it150(k))
         endif
c
c        3 EPOS
         if (iepos(k) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp( 3) = 0.1*float(iepos(k))
         endif
c
c        4 TGRD
         if (itgrd(k) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp( 4) = 1.0*float(itgrd(k))
         endif
c
c        5 V500
         if (iv500(k) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp( 5) = 0.1*float(iv500(k))
         endif
c
c        6 V300
         if (iv300(k) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp( 6) = 0.1*float(iv300(k))
         endif
c
c        7 SHDC
         if (ishdc(k) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp( 7) = 0.1*float(ishdc(k))
         endif
c
c        8 V20C
         if (iv20c(k) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp( 8) = 0.1*float(ishdc(k))
         endif
c
c        9 CY
         if (cyt(k) .ge. rmiss) then
            nmissing = nmissing + 1
         else
            dfinp( 9) = cyt(k)
         endif
c
c        10 CY
         if (cmagt(k) .ge. rmiss) then
            nmissing = nmissing + 1
         else
            dfinp(10) = cmagt(k)
         endif
c
c        11 PC10
         if (igoes(5) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp(11) = 1.0*float(igoes(5))
         endif
c
c        12 EYET
         if (igoes(12) .eq. imiss) then
            nmissing = nmissing + 1
         else
            dfinp(12) = 0.1*float(igoes(12))
         endif
c
         if (nmissing .eq. 0) then
c           Calculate discriminant function values for each group
            do m=1,ngrp
               dfval(m) = dfcoef(0,m,k)
               do j=1,nvar
                  dfval(m) = dfval(m) + dfinp(j)*dfcoef(j,m,k)
               enddo
            enddo
         else
            do m=1,ngrp
               dfval(m) = rmiss
            enddo
         endif
c
         if (nmissing .eq. 0) then
c           Choose storm type based on largest discriminant value
            stype(k) = 'TROP'
            dfmax    = dfval(1)
            if (dfval(2) .gt. dfmax) then
               stype(k) = 'SUBT'
               dfmax    = dfval(2)
            endif
c
            if (dfval(3) .gt. dfmax) then
               stype(k) = 'EXTP'
               dfmax    = dfval(3)
            endif
         endif
c
c        write(6,*) k*6,dfval(1),dfval(2),dfval(3),stype(k)
      enddo
c
c     Normal return
      close(lucof)
      return
c
c     Error processing
  900 continue
      close(lucof)
      return
c
      end
