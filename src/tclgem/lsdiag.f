      program lsdiag                                                     
c     This program performs diagnostic calculations using                
c     large-scale analyses in packed form.                               
c                                                                        
c     Modified    Apr 2005 - 6 hour data increment                       
c     Modified 20 Apr 2006 - for 2006 season                             
c     Modified 26 Aug 2006 - Legacy svn routines removed                 
c              13 Sep 2006 - Experimental shear and related calculation a
c              16 Sep 2006 - New storm-relative D200 calculation         
c                     2008 - lcmod calculations added                    
c              25 Mar 2009 - U200C,V200C output added                    
c              02 Apr 2010 - RH bias correction for reanalsysis fields ad
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
c                                                                        
C.DUP lsdiag,prima                                                       
      common /primv/ u,v,z,t,r                                           
      dimension u(ixmx,iymx,ipmx),v(ixmx,iymx,ipmx),z(ixmx,iymx,ipmx)    
      dimension t(ixmx,iymx,ipmx),r(ixmx,iymx,ipmx)                      
c                                                                        
C.DUP lsdiag,index                                                       
      common /indexa/ indexp,indexv                                      
      common /indexn/ indexvn                                            
      parameter (nvar=5)                                                 
      dimension indexp(ipmx),indexv(nvar)                                
      character *1 indexvn(nvar)                                         
c     Specify allowable variable names on data input file                
      data indexvn /'U','V','Z','T','R'/                                 
c                                                                        
C.DUP lsdiag,latlon                                                      
       common /latlon/  RLATMN,RLATMX,RLONMN,RLONMX,DLAT,DLON,           
     +                  RLATD,RLOND                                      
       dimension rlatd(iymx),rlond(ixmx)                                 
       common /ilatlon/ NLAT1,NLON1                                      
c                                                                        
C.DUP lsdiag,plevs                                                       
      common /plevs/ plev,plevr                                          
      dimension plev(ipmx),plevr(ipmx)                                   
C.DUP lsdiag,plevsd                                                      
      DATA PLEV  / 1070.,1000., 950.,925.,900.,850.,700.,500.,           
     +                    400., 350.,300.,250.,200.,150.,100.,70.,50.,   
     +                     25.,  10.,  5.,  1./                          
      DATA PLEVR / 1013.,1000.,1000.,925.,850.,850.,700.,500.,           
     +                    400., 400.,300.,250.,200.,150.,100.,70.,50.,   
     +                     25.,  10.,  5.,  1./                          
c                                                                        
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
c                                                                        
C.DUP lsdiag,rawdfn                                                      
      common /rawdf/ rawdfn                                              
      character *40 rawdfn                                               
c                                                                        
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
C.DUP lsdiag,unnumd                                                      
      data lulog,luinp,luout,lurawd /21,22,23,24/                        
c                                                                        
c     Local variables                                                    
      character *20 logname,inname,outname                               
c                                                                        
c     ********************                                               
c                                                                        
c     Specify log file name                                              
      logname = 'lsdiag.log'                                             
c                                                                        
c     Specify input file name                                            
      inname  = 'lsdiag.inp'                                             
c                                                                        
c     Specify data output file name                                      
      outname = 'lsdiag.dat'                                             
c                                                                        
c     Open the log file                                                  
      open(unit=lulog,file=logname,status='replace',form='formatted')    
      write(lulog,300)                                                   
  300 format(' LSDIAG BEGINS, LOG FILE OPENED')                          
c                                                                        
c     Open the data input and output files                               
      open(unit=luinp,file=inname,status='old',form='formatted')         
      open(unit=luout,file=outname,status='replace',form='formatted')    
c                                                                        
c     Calculate constants                                                
      call pncal                                                         
c                                                                        
c     Calculate vertical shear from aviation model fields                
c      call ascal                                                        
c                                                                        
c     Calculate SHIPS variables (2005-2006 version with 5-day input files
c                                                              6 hr data)
      call sv6cal                                                        
c                                                                        
c     Calculate time averages of specified variables                     
c     call tavg                                                          
c                                                                        
      stop                                                               
      END                                                                
      subroutine aunpack(ierr)                                           
c     This routine unpacks the data file and puts the variables          
c     in three-dimensional arrays. If there is a problem opening         
c     or reading the data file, ierr=1, otherwise ierr=0.                
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,prima                                                       
      common /primv/ u,v,z,t,r                                           
      dimension u(ixmx,iymx,ipmx),v(ixmx,iymx,ipmx),z(ixmx,iymx,ipmx)    
      dimension t(ixmx,iymx,ipmx),r(ixmx,iymx,ipmx)                      
c                                                                        
C.DUP lsdiag,index                                                       
      common /indexa/ indexp,indexv                                      
      common /indexn/ indexvn                                            
      parameter (nvar=5)                                                 
      dimension indexp(ipmx),indexv(nvar)                                
      character *1 indexvn(nvar)                                         
C.DUP lsdiag,latlon                                                      
       common /latlon/  RLATMN,RLATMX,RLONMN,RLONMX,DLAT,DLON,           
     +                  RLATD,RLOND                                      
       dimension rlatd(iymx),rlond(ixmx)                                 
       common /ilatlon/ NLAT1,NLON1                                      
C.DUP lsdiag,rawdfn                                                      
      common /rawdf/ rawdfn                                              
      character *40 rawdfn                                               
C.DUP lsdiag,plevs                                                       
      common /plevs/ plev,plevr                                          
      dimension plev(ipmx),plevr(ipmx)                                   
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
c     Local variables                                                    
      parameter(imax=10000)                                              
c                                                                        
      dimension tra(imax)                                                
      character *2 code(imax)                                            
      character *1 type                                                  
      character *10 vlabel                                               
c                                                                        
c     ********************                                               
c                                                                        
c     Open data input file                                               
      open(unit=lurawd,file=rawdfn,status='old',form='formatted',        
     +     err=900)                                                      
c                                                                        
      write(lulog,300) rawdfn                                            
  300 format(/,' Begin unpacking rawd file: ',a40)                       
c                                                                        
c     Initialize all index variables to zero                             
      do 10 i=1,ipmx                                                     
         indexp(i) = 0                                                   
   10 continue                                                           
c                                                                        
      do 15 i=1,nvar                                                     
         indexv(i) = 0                                                   
   15 continue                                                           
c                                                                        
C     READ MAIN HEADER ON PACKED DATA FILE                               
      READ(lurawd,100) WX,DAYX,UTCX,RLATMN,RLATMX,RLONMN,RLONMX,         
     +                 DLAT,DLON                                         
  100 FORMAT(1X,F3.0,F7.0,F5.0,4F8.3,2F4.1)                              
C                                                                        
C     FOR WEST PACIFIC RAWD FILES, SWITCH RLONMN AND RLONMX              
C     TO ACCOUNT FOR DEG EAST LONGITUDE                                  
      IF (rawdfn(1:2) .EQ. 'WP') THEN                                    
         RLMIN = RLONMN                                                  
         RLMAX = RLONMX                                                  
         RLONMN = -RLMAX                                                 
         RLONMX = -RLMIN                                                 
      ENDIF                                                              
C                                                                        
C     WRITE HEADER INFORMATION                                           
      WRITE(LULOG,200) DAYX,UTCX                                         
  200 FORMAT(/,' DATA DATE AND TIME: ',F7.0,1X,F5.0)                     
C                                                                        
      WRITE(LULOG,205) RLATMN,RLATMX,RLONMN,RLONMX                       
  205 FORMAT(/,' MIN,MAX LAT: ',F6.1,1X,F6.1,                            
     +       '   MIN,MAX LON: ',F6.1,1X,F6.1)                            
C                                                                        
      WRITE(LULOG,210) DLAT,DLON                                         
  210 FORMAT(/,' DLAT,DLON= ',F4.1,1X,F4.1)                              
C                                                                        
C     CALCULATE LAT AND LON POINTS                                       
      EPSIL=0.001                                                        
      NLATI = IFIX((RLATMX-RLATMN)/DLAT + EPSIL)                         
      NLONI = IFIX((RLONMX-RLONMN)/DLON + EPSIL)                         
      IPTS  = (NLATI+1)*(NLONI+1)                                        
      NLAT1 = NLATI + 1                                                  
      NLON1 = NLONI + 1                                                  
C                                                                        
C     UNPACK THE DATA                                                    
      NROW = 1 + (IPTS-1)/36                                             
c                                                                        
  500 CONTINUE                                                           
         READ(lurawd,105,ERR=900,END=600) TYPE,PTEM,BSUB,SMPY            
  105    FORMAT(1X,A1,1X,F6.1,2(1X,G15.9))                               
c                                                                        
C        DETERMINE THE PRESSURE LEVEL                                    
         DO 25 I=1,ipmx                                                  
            IF (PTEM .EQ. PLEV(I)) GO TO 1000                            
   25    CONTINUE                                                        
C                                                                        
         WRITE(lulog,960) PTEM                                           
  960    FORMAT(2X,'PRESSURE= ',E11.4,' NOT FOUND IN PLEV ARRAY')        
         STOP                                                            
c                                                                        
 1000    CONTINUE                                                        
         indexp(i) = 1                                                   
         lnow      = i                                                   
c                                                                        
C        READ IN PACKED DATA                                             
         DO 30 N=1,NROW                                                  
            IS = 1 + (N-1)*36                                            
            IE = IS+35                                                   
            READ(lurawd,110,END=902,ERR=902) (CODE(I),I=IS,IE)           
  110       FORMAT(36(A2))                                               
   30    CONTINUE                                                        
c                                                                        
C        UNPACK THE DATA AND PUT IT IN THE PROPER ARRAY                  
         DO 35 I=1,IPTS                                                  
            IX     = IDECOD(CODE(I))                                     
            TRA(I) = IX * SMPY - BSUB                                    
   35    CONTINUE                                                        
C                                                                        
         if (type .eq. 'U') then                                         
            indexv(1) = 1                                                
            DO 40 I = 0,NLATI                                            
            DO 40 J = 0,NLONI                                            
               IJ = (J+1) + I*(NLONI+1)                                  
               u(J+1,I+1,LNOW) = TRA(IJ)                                 
   40       CONTINUE                                                     
         elseif (type .eq. 'V') then                                     
            indexv(2) = 1                                                
            DO 45 I = 0,NLATI                                            
            DO 45 J = 0,NLONI                                            
               IJ = (J+1) + I*(NLONI+1)                                  
               v(J+1,I+1,LNOW) = TRA(IJ)                                 
   45       CONTINUE                                                     
         elseif (type .eq. 'Z') then                                     
            indexv(3) = 1                                                
            DO 50 I = 0,NLATI                                            
            DO 50 J = 0,NLONI                                            
               IJ = (J+1) + I*(NLONI+1)                                  
               z(J+1,I+1,LNOW) = TRA(IJ)                                 
   50       CONTINUE                                                     
         elseif (type .eq. 'T') then                                     
            indexv(4) = 1                                                
            DO 55 I = 0,NLATI                                            
            DO 55 J = 0,NLONI                                            
               IJ = (J+1) + I*(NLONI+1)                                  
               t(J+1,I+1,LNOW) = TRA(IJ)                                 
   55       CONTINUE                                                     
         elseif (type .eq. 'R') then                                     
            indexv(5) = 1                                                
            DO 60 I = 0,NLATI                                            
            DO 60 J = 0,NLONI                                            
               IJ = (J+1) + I*(NLONI+1)                                  
               r(J+1,I+1,LNOW) = TRA(IJ)                                 
   60       CONTINUE                                                     
         else                                                            
            write(lulog,970) type                                        
  970       format(/,' Unrecognized variable type: ',a1)                 
c           stop                                                         
         endif                                                           
      go to 500                                                          
  600 continue                                                           
c                                                                        
c     Calculate latitude (deg) and longitudes (deg W neg.)               
c     the of grid points                                                 
      do 65 j=1,nlat1                                                    
         rlatd(j) = rlatmn + dlat*float(j-1)                             
   65 continue                                                           
c                                                                        
      do 70 i=1,nlon1                                                    
         rlond(i) = -(rlonmx - dlon*float(i-1))                          
   70 continue                                                           
c                                                                        
c     List pressure levels and variable types found on rawd file         
      write(lulog,305)                                                   
  305 format(/,                                                          
     +' Pressure levels (mb) and variables found on rawd file:')         
      do 75 i=1,ipmx                                                     
         if (indexp(i) .eq. 1) then                                      
            write(lulog,310) plevr(i)                                    
  310       format(1x,f6.1)                                              
         endif                                                           
   75 continue                                                           
c                                                                        
      vlabel = '         '                                               
      ii = 0                                                             
      do 80 i=1,nvar                                                     
         if (indexv(i) .eq. 1) then                                      
            ii = ii+1                                                    
            ii2 = 2*ii                                                   
            vlabel(ii2:ii2) = indexvn(i)                                 
         endif                                                           
   80 continue                                                           
      write(lulog,315) vlabel                                            
  315 format(1x,a10)                                                     
c                                                                        
c     Close the rawd file and set the error flag                         
      close(lurawd)                                                      
      ierr=0                                                             
      return                                                             
c                                                                        
  900 write(lulog,950) rawdfn                                            
  950 format(/,' Error opening rawd file: ',a40)                         
      close(lurawd)                                                      
      ierr=1                                                             
      return                                                             
c                                                                        
  902 write(lulog,952) rawdfn                                            
  952 format(/,' Error reading rawd file: ',a40)                         
      close(lurawd)                                                      
      ierr=1                                                             
      return                                                             
c                                                                        
      end                                                                
c     integer function idecod (code)                                     
c                                                                        
c     parameter (base = 32)                                              
c     character*(*) code                                                 
c     character dgtb*(base-1)                                            
c     parameter (dgtb = '123456789ABCDEFGHIJKLMNOPQRSTUV')               
c                                                                        
c     idecod = index (dgtb,code(1:1)) * base                             
c    1  + index (dgtb,code(2:2))                                         
c                                                                        
c     return                                                             
c     END                                                                
      integer function idecod (code)                                     
c     hp version                                                         
c                                                                        
      character*(*) code                                                 
      character dgtb*(31)                                                
      parameter (dgtb = '123456789ABCDEFGHIJKLMNOPQRSTUV')               
c                                                                        
      idecod = index (dgtb,code(1:1)) * 32                               
     1  + index (dgtb,code(2:2))                                         
c                                                                        
      return                                                             
      END                                                                
      subroutine ascal                                                   
c     This routine calculates the vertical shear from the Aviation       
c     model fields for each case in the input file.                      
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,index                                                       
      common /indexa/ indexp,indexv                                      
      common /indexn/ indexvn                                            
      parameter (nvar=5)                                                 
      dimension indexp(ipmx),indexv(nvar)                                
      character *1 indexvn(nvar)                                         
C.DUP lsdiag,rawdfn                                                      
      common /rawdf/ rawdfn                                              
      character *40 rawdfn                                               
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
c     Local common                                                       
      character *72 hline,tline,iline(12)                                
c                                                                        
      dimension islat(-2:7),islon(-2:7)                                  
c                                                                        
c     ********************                                               
c                                                                        
c     Generic rawd file name for Aviation files                          
      rawdfn = 'AF0000_Z0000_PACK.DAT'                                   
c                                                                        
c     Start the case by case loop                                        
      nrawd=0                                                            
 2001 continue                                                           
c                                                                        
C        READ BEST TRACK FILE FOR CASE SELECTION                         
         READ(LUINP,100,ERR=751,END=2000) HLINE                          
  100    FORMAT(A72)                                                     
c                                                                        
         GO TO 5100                                                      
  751       WRITE(LULOG,*) ' ERROR READING INPUT FILE (LUINP)'           
            STOP                                                         
 5100    CONTINUE                                                        
C                                                                        
         iline(1) = hline                                                
         DO 10 I=2,12                                                    
            READ(LUINP,100,ERR=751,END=752) ILINE(I)                     
            GO TO 5200                                                   
  752          WRITE(LULOG,*) ' UNEXPECTED END ON INPUT FILE (LUINP)'    
               STOP                                                      
 5200       CONTINUE                                                     
   10    CONTINUE                                                        
C                                                                        
         nrawd = nrawd + 1                                               
         WRITE(6,200) NRAWD,HLINE                                        
  200    FORMAT(/,' START CASE',I4,' FIRST LINE OF LUINP HEADER:',/,A72) 
C                                                                        
C        READ STORM POSITIONS OFF OF ILINE FROM LUINP FILE               
         READ(ILINE(3),105) (ISLAT(K),K=-2,6)                            
         READ(ILINE(4),105) (ISLON(K),K=-2,6)                            
  105    FORMAT(9(1X,I4))                                                
C                                                                        
c        Calculate vertical shear if necessary                           
         do 15 k=0,6                                                     
            if (islat(k) .lt. 9000 .and. islon(k) .lt. 9000) then        
               slat =      float(islat(k))/10.0                          
               slon = -1.0*float(islon(k))/10.0                          
c                                                                        
c              Create Aviation file name                                 
               k12 = k*12                                                
               write(rawdfn(3:4),405) k12                                
  400          format(i2)                                                
c                                                                        
               rawdfn(5:6) = HLINE(7:8)                                  
               rawdfn(9:10) = HLINE(9:10)                                
c                                                                        
               read(hline(11:12),400) iday                               
               read(hline(14:15),400) itime                              
               if (itime .eq. 12) iday = iday+50                         
               write(rawdfn(11:12),405) iday                             
  405          format(i2.2)                                              
c                                                                        
c              Unpack the rawd file                                      
               call aunpack(ierr)                                        
c                                                                        
               if (ierr .ne. 0) then                                     
                  write(6,205)                                           
  205             format(' Error opening or reading data input file')    
                  stop                                                   
               endif                                                     
c                                                                        
c              Calculate the vertical shear                              
               ps1 = 850.0                                               
               ps2 = 200.0                                               
               radkt = 600.0                                             
               minpts = 8                                                
               call vshear(ps1,ps2,slon,slat,radkt,minpts,shear,sheard)  
c                                                                        
               ishear = ifix(0.49 + 10.0*shear)                          
c                                                                        
               tline = iline(5)                                          
               ks = 12 + 5*k                                             
               ke = ks + 3                                               
               write(tline(ks:ke),410) ishear                            
  410          format(i4)                                                
               iline(5) = tline                                          
            endif                                                        
   15    continue                                                        
c                                                                        
         do 30 i=1,12                                                    
            write(luout,100) iline(i)                                    
   30    continue                                                        
c                                                                        
C     DO NEXT CASE                                                       
      GO TO 2001                                                         
C                                                                        
 2000 CONTINUE                                                           
C                                                                        
      WRITE(LULOG,350) NRAWD                                             
  350 FORMAT(/,' NORMAL COMPLETION OF LSDIAG, ',I4,' CASES PROCESSED')   
C                                                                        
      RETURN                                                             
      END                                                                
      subroutine tavg                                                    
c     This routine finds the time average of various variables           
c     from the files listed in lsdiag.in                                 
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,rawdfn                                                      
      common /rawdf/ rawdfn                                              
      character *40 rawdfn                                               
C.DUP lsdiag,plevh                                                       
      parameter (nplevh=10)                                              
      common /plevhs/ up,vp,zp,tp,rp,tbarp,plevh                         
      dimension up(nplevh),vp(nplevh),zp(nplevh)                         
      dimension tp(nplevh),rp(nplevh)                                    
      dimension tbarp(nplevh)                                            
      dimension plevh(nplevh)                                            
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
c     Other variables                                                    
      dimension upavg(nplevh),vpavg(nplevh),tpavg(nplevh),               
     +          zpavg(nplevh),rpavg(nplevh)                              
c                                                                        
      dimension tppavg(nplevh),deltp(nplevh)                             
      parameter (mxd=300)                                                
      dimension pps(mxd),tts(mxd),tvs(mxd)                               
c     ********************                                               
c                                                                        
c     Generic rawd file name for the input rawd files                    
      rawdfn = 'BACK00_X0000_PACK.DAT'                                   
c                                                                        
c     Specify center lat,lon for sounding                                
      clat = 12.0                                                        
      clon = -40.0                                                       
c                                                                        
      clat = 13.0                                                        
      clon = -40.0                                                       
c                                                                        
c     Set istavg=1 to average sounding over circular area of radius radk 
c      or istavg=2 to avarage sounding over rectangular area +/- xradk,yr
      istavg=2                                                           
c                                                                        
      radk = 666.0                                                       
      xradk=1085.0                                                       
      yradk=555.6                                                        
c                                                                        
      write(luout,203) clat,clon                                         
  203 format(/,' Center of area average, lat,lon: ',                     
     +           f5.1,1x,f6.1)                                           
c                                                                        
      if (istavg .eq. 1) then                                            
         write(luout,201) radk                                           
  201    format(/,' Radius of area=',f6.1,' km')                         
      else                                                               
         write(luout,202) xradk,yradk                                    
  202    format(/,' Rectangular area +/- x=',f6.1,' km  ',               
     +                               '+/- y=',f6.1,' km  ')              
      endif                                                              
c                                                                        
c     Initialize average variables to zero                               
      do 5 i=1,nplevh                                                    
         upavg(i) = 0.0                                                  
         vpavg(i) = 0.0                                                  
         tpavg(i) = 0.0                                                  
	 zpavg(i) = 0.0                                                         
         rpavg(i) = 0.0                                                  
    5 continue                                                           
c                                                                        
c     Start the case by case loop                                        
      nrawd=0                                                            
 2001 continue                                                           
c                                                                        
C        READ FILE FOR CASE SELECTION                                    
         READ(LUINP,100,ERR=751,END=2000) rawdfn                         
  100    FORMAT(A40)                                                     
c                                                                        
         GO TO 5100                                                      
  751       WRITE(LULOG,*) ' ERROR READING INPUT FILE (LUINP)'           
            STOP                                                         
 5100    CONTINUE                                                        
C                                                                        
         nrawd = nrawd + 1                                               
         WRITE(6,200)     NRAWD,rawdfn                                   
         WRITE(LUOUT,200) NRAWD,rawdfn                                   
  200    FORMAT(/,' START CASE',I4,' FILE: ',A40)                        
C                                                                        
c        Unpack the rawd file                                            
         call aunpack(ierr)                                              
c                                                                        
         if (ierr .ne. 0) then                                           
            write(6,205)                                                 
  205       format(' Error opening or reading data input file')          
            nrawd = nrawd-1                                              
            go to 2001                                                   
         endif                                                           
c                                                                        
c        Calculate vertical soundings                                    
         if (istavg .eq. 1) then                                         
            call vsound(clon,clat,radk)                                  
         else                                                            
            call vcsound(clon,clat,xradk,yradk)                          
         endif                                                           
c                                                                        
         if (rawdfn(1:4) .eq. 'BACK') then                               
c           Convert virtual temperature to temperature                   
            do 8 i=1,nplevh                                              
               if (rp(i) .le. 100.0) then                                
                  call virti(tp(i),plevh(i),rp(i),tt)                    
                  tp(i) = tt                                             
               endif                                                     
    8       continue                                                     
        endif                                                            
c                                                                        
c        Convert deviation heights to total heights                      
	 do 9 i=1,nplevh                                                        
	    ptemp = plevh(i)                                                    
	    call stndz(ptemp,ztemp,ttemp,thtemp)                                
	    zp(i) = zp(i) + ztemp                                               
    9    continue                                                        
c                                                                        
c        Add current case for time average                               
         do 10 i=1,nplevh                                                
            upavg(i) = upavg(i) + up(i)                                  
            vpavg(i) = vpavg(i) + vp(i)                                  
            tpavg(i) = tpavg(i) + tp(i)                                  
            zpavg(i) = zpavg(i) + zp(i)                                  
            rpavg(i) = rpavg(i) + rp(i)                                  
   10    continue                                                        
c                                                                        
c        Write current sounding to the output file                       
         write(luout,210) (up(i),i=1,nplevh)                             
         write(luout,215) (vp(i),i=1,nplevh)                             
         write(luout,220) (tp(i),i=1,nplevh)                             
         write(luout,224) (zp(i),i=1,nplevh)                             
         write(luout,222) (rp(i),i=1,nplevh)                             
         write(luout,225) (plevh(i),i=1,nplevh)                          
  210    format(' U ',10(f6.1))                                          
  215    format(' V ',10(f6.1))                                          
  220    format(' T ',10(f6.1))                                          
  221    format(' TP',10(f6.1))                                          
  223    format(' DT',10(f6.1))                                          
  224    format(' Z ',10(f6.0))                                          
  222    format(' R ',10(f6.1))                                          
  225    format(' P ',10(f6.1))                                          
c                                                                        
C     Do next case                                                       
      go to 2001                                                         
C                                                                        
 2000 continue                                                           
c                                                                        
c     Calculate time averages                                            
      rnrawd = float(nrawd)                                              
      if (nrawd .le. 0) rnrawd = 1.0                                     
c                                                                        
      do 20 i=1,nplevh                                                   
         upavg(i) = upavg(i)/rnrawd                                      
         vpavg(i) = vpavg(i)/rnrawd                                      
         tpavg(i) = tpavg(i)/rnrawd                                      
         zpavg(i) = zpavg(i)/rnrawd                                      
         rpavg(i) = rpavg(i)/rnrawd                                      
   20 continue                                                           
c                                                                        
c     Calculate surface pressure and temperature                         
      z1 = zpavg(1)                                                      
      z2 = zpavg(2)                                                      
      p1 = plevh(1)*100.0                                                
      p2 = plevh(2)*100.0                                                
      t1 = tpavg(1) + 273.15                                             
      t2 = tpavg(2) + 273.15                                             
      call pstcal(z1,z2,t1,t2,p1,psfc,tsfc)                              
c                                                                        
c     Calculate lifted parcel temperature from sfc to 100 mb             
      p1000 = 1000.0e+2                                                  
      t1000 = tpavg(1)+273.13                                            
      r1000 = rpavg(1)                                                   
      dpp   = 10.0e+2                                                    
      ptop  = 100.0e+2                                                   
      iadj  = 1                                                          
c                                                                        
      if (nrawd .gt. 0) then                                             
          if (psfc .lt. p1000) then                                      
             call parsub(p1000,t1000,r1000,dpp,ptop,iadj,mxd,            
     +                   psat,pps,tts,tvs,npp)                           
c                                                                        
          else                                                           
             call parsub(psfc,tsfc,r1000,dpp,ptop,iadj,mxd,              
     +                   psat,pps,tts,tvs,npp)                           
          endif                                                          
      endif                                                              
c                                                                        
      do kk=1,nplevh                                                     
         do ii=1,npp                                                     
            if (pps(ii) .eq. 100.0*plevh(kk)) then                       
               tppavg(kk) = tts(ii)-273.15                               
            endif                                                        
         enddo                                                           
         deltp(kk) = tppavg(kk) - tpavg(kk)                              
      enddo                                                              
c                                                                        
c     Sum up the temperature differences from level 1 to npmax           
      npmax = 8                                                          
      dptot = plevh(1)-plevh(npmax)                                      
      dttp  = 0.0                                                        
      do kk=1,npmax                                                      
         if (kk .eq. 1) then                                             
            wtt = 0.5*(plevh(      1)-plevh(     2))/dptot               
         elseif (kk .eq. npmax) then                                     
            wtt = 0.5*(plevh(npmax-1)-plevh(npmax))/dptot                
         else                                                            
            wtt = 0.5*(plevh(   kk-1)-plevh(  kk+1))/dptot               
         endif                                                           
c                                                                        
         dttp = dttp + wtt*(tppavg(kk) - tpavg(kk))                      
      enddo                                                              
c                                                                        
      delu  = upavg(8)  - upavg(2)                                       
      delt  = tppavg(8) - tpavg(8)                                       
c                                                                        
      write(luout,230) nrawd                                             
  230 format(//,' Time averaged variables, no. cases= ',i4)              
      write(luout,210) (upavg(i),i=1,nplevh)                             
      write(luout,215) (vpavg(i),i=1,nplevh)                             
      write(luout,220) (tpavg(i),i=1,nplevh)                             
      write(luout,221) (tppavg(i),i=1,nplevh)                            
      write(luout,223) (deltp(i),i=1,nplevh)                             
      write(luout,224) (zpavg(i),i=1,nplevh)                             
      write(luout,222) (rpavg(i),i=1,nplevh)                             
      write(luout,225) (plevh(i),i=1,nplevh)                             
C                                                                        
      write(luout,227) upavg(2),upavg(8),delu,rpavg(1),delt,tsfc-273.15, 
     +                 tpavg(8),psfc/100.0,psat/100.0,dttp,              
     +                 nrawd,rawdfn(5:12)                                
  227 format(/,'u2=',f4.0,' u8=',f4.0,' du=',f5.1,                       
     +       ' rh1=',f3.0,' dT=',f4.1,                                   
     +       ' Ts=',f4.1,' T8=',f5.1,' Ps=',f6.1,' Pl=',f5.0,            
     +       ' S=',f4.1,1x,i2,1x,a8)                                     
c                                                                        
      WRITE(LULOG,350) NRAWD                                             
  350 FORMAT(/,' NORMAL COMPLETION OF LSDIAG, ',I4,' CASES PROCESSED')   
C                                                                        
      RETURN                                                             
      END                                                                
      subroutine sv6cal                                                  
c     This routine calculates the variables needed for                   
c     the SHIPS intensity forecast model (2005-2006 version)             
c     for each case in the input file.                                   
c                                                                        
c     This version uses the input file with 5-day forecasts.             
c                                                                        
c     The lsdiag input file includes data at 6 hour intervals            
c     rather than 12 hour intervals for this version                     
c                                                                        
      parameter (itmax=20)                                               
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,rawdfn                                                      
      common /rawdf/ rawdfn                                              
      character *40 rawdfn                                               
C.DUP lsdiag,plevh                                                       
      parameter (nplevh=10)                                              
      common /plevhs/ up,vp,zp,tp,rp,tbarp,plevh                         
      dimension up(nplevh),vp(nplevh),zp(nplevh)                         
      dimension tp(nplevh),rp(nplevh)                                    
      dimension tbarp(nplevh)                                            
      dimension plevh(nplevh)                                            
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
c     Local variables                                                    
      dimension islat(-2:itmax),islon(-2:itmax)                          
      dimension  slat(-2:itmax), slon(-2:itmax)                          
c                                                                        
      dimension iu200(0:itmax),it200(0:itmax)                            
      dimension iu200c(0:itmax),iv200c(0:itmax)                          
      dimension it150(0:itmax),it250(0:itmax)                            
      dimension ishrd(0:itmax),ishrs(0:itmax)                            
      dimension ishtd(0:itmax),ishts(0:itmax)                            
      dimension ishrg(0:itmax)                                           
      dimension ishxu(0:itmax),ishxl(0:itmax)                            
      dimension ivorb(0:itmax),idivb(0:itmax),irefc(0:itmax)             
      dimension ipefc(0:itmax)                                           
      dimension irhlo(0:itmax),irhhi(0:itmax),irhmd(0:itmax)             
      dimension ipslv(0:itmax)                                           
      dimension iz000(0:itmax),it000(0:itmax),ir000(0:itmax)             
c                                                                        
      dimension ie000(0:itmax)                                           
      dimension iepos(0:itmax),ieneg(0:itmax)                            
      dimension iepss(0:itmax),ienss(0:itmax)                            
c                                                                        
      dimension fxy(ixmx,iymx)                                           
c                                                                        
      character *4 sname,tlabel                                          
      character *130 hline,tline,iline(60)                               
c                                                                        
c     Variables for vertical profiles                                    
      parameter (nvp=10)                                                 
c                                                                        
      dimension pvp(nvp),uvp(nvp),vvp(nvp),tvp(nvp),rvp(nvp)             
      dimension qvp(nvp)                                                 
      dimension wvp(nvp),wt1(nvp),wt2(nvp),tevp(nvp),tevps(nvp)          
      dimension zvp(nvp)                                                 
c                                                                        
c     Vertical profile arrays for Kerry Emanuel MPI code and lcmod       
      dimension pkmpi(nvp+1),tkmpi(nvp+1),qkmpi(nvp+1),rkmpi(nvp+1)      
      dimension irsst(-2:itmax),rsst(-2:itmax)                           
      dimension ivkmpi(0:itmax),ipkmpi(0:itmax)                          
c                                                                        
c     Variables for tracker and vortex removal code                      
      dimension uxyp(ixmx,iymx,nvp),vxyp(ixmx,iymx,nvp)                  
      dimension txyp(ixmx,iymx,nvp),rxyp(ixmx,iymx,nvp)                  
      dimension zxyp(ixmx,iymx,nvp)                                      
c                                                                        
      dimension itlat(0:itmax),itlon(0:itmax)                            
      dimension ishdc(0:itmax),isddc(0:itmax),ishgc(0:itmax)             
      dimension it15c(0:itmax),it20c(0:itmax),it25c(0:itmax)             
      dimension iepoc(0:itmax),idivc(0:itmax)                            
c                                                                        
      dimension irtcc(0:itmax),irtxc(0:itmax)                            
      dimension itwac(0:itmax),itwxc(0:itmax),itwbc(0:itmax)             
      dimension ipsfc(0:itmax),ipsfcc(0:itmax)                           
c                                                                        
      dimension ivvavg(0:itmax),ivmflux(0:itmax)                         
      dimension ivvavc(0:itmax)                                          
      parameter (mrcf=100,mtcf=16)                                       
      dimension rcf(0:mrcf),thetacf(0:mtcf)                              
      dimension stheta(0:mtcf),ctheta(0:mtcf)                            
      dimension uraa(0:mrcf),vtaa(0:mrcf)                                
c                                                                        
      dimension zcrt(0:mrcf,0:mtcf),tcrt(0:mrcf,0:mtcf)                  
      dimension zraa(0:mrcf),traa(0:mrcf)                                
c                                                                        
c     Variables for proxy GOES data                                      
      dimension pgoes(16)                                                
      dimension ipgoes(0:itmax)                                          
c     ********************                                               
c                                                                        
c     Set iatype=0 to use analyses to calculate predictors,              
c      or iatype=1 to use forecasts for predictors                       
      iatype=1                                                           
c                                                                        
c     If iatype=0, set last year (yyyy) to use re-analysis files         
      iray = 2000                                                        
c     iray = 1000                                                        
c                                                                        
c     If iatype=0, set ibcrh=1 to apply the bias correction to the       
c        RH from the reanalysis fields                                   
      ibcrh=0                                                            
c                                                                        
c     Specify time interval between data points                          
      idelt=6                                                            
      delt = float(idelt)                                                
c                                                                        
c     Specify radii (km) for vertical profile variables                  
c     (These define averaging area for shear and other predictors)       
      radinn = 200.0                                                     
      radout = 800.0                                                     
c                                                                        
c     Specify radius (km) for averaging tangential wind vortex tracking  
      radtwa=600.0                                                       
c                                                                        
c     Specify inner and outer radii (km) for azimuthal average           
c     after filtering and vortex removal                                 
      radinnc =   0.0                                                    
      radoutc = 500.0                                                    
c                                                                        
c     Specify radius (km) for area average relative vorticity            
      radvor = 1000.0                                                    
c                                                                        
c     Specify radius (km) for area average divergence                    
      raddiv = 1000.0                                                    
c                                                                        
c     Specify radius (km) for radially averaging eddy momentum fluxes    
      radrefc = 600.0                                                    
c                                                                        
c     Specify radius (km) for radially averaging planetary momentum fluxe
      radpefc = 600.0                                                    
c                                                                        
c     Specify minimum points for area average calculations               
      minpts=5                                                           
c                                                                        
c     Specify vertical pressure levels (mb) for analysis                 
      pvp( 1) =  100.0                                                   
      pvp( 2) =  150.0                                                   
      pvp( 3) =  200.0                                                   
      pvp( 4) =  250.0                                                   
      pvp( 5) =  300.0                                                   
      pvp( 6) =  400.0                                                   
      pvp( 7) =  500.0                                                   
      pvp( 8) =  700.0                                                   
      pvp( 9) =  850.0                                                   
      pvp(10) = 1000.0                                                   
c                                                                        
c     Specify indices of pressures in pvp array                          
      i100 = 1                                                           
      i150 = 2                                                           
      i200 = 3                                                           
      i250 = 4                                                           
      i300 = 5                                                           
      i400 = 6                                                           
      i500 = 7                                                           
      i700 = 8                                                           
      i850 = 9                                                           
      i000 = 10                                                          
c                                                                        
c     Set imxshr=1 to include max shear variables                        
      imxshr=0                                                           
c                                                                        
c     Calculate deep layer mean weights for each pressure level          
      dpvp = pvp(nvp)-pvp(1)                                             
c                                                                        
      wvp(  1) = 0.5*(pvp(  2)-pvp(    1))/dpvp                          
      wvp(nvp) = 0.5*(pvp(nvp)-pvp(nvp-1))/dpvp                          
c                                                                        
      do 5 n=2,nvp-1                                                     
	 wvp(n) = ( 0.5*(pvp(n+1)-pvp(n-1)) )/dpvp                              
    5 continue                                                           
c                                                                        
c     Variables for center finding and vortex removal arrays             
      nrcf = 24                                                          
      drcf = 50.0                                                        
      do k=0,nrcf                                                        
         rcf(k) = drcf*float(k)                                          
      enddo                                                              
c                                                                        
      ntcf = 7                                                           
      dthetacf = 360.0/float(ntcf+1)                                     
      do m=0,ntcf                                                        
         thetacf(m) = dthetacf*float(m)                                  
         ctheta(m) = cos(dtr*thetacf(m))                                 
         stheta(m) = sin(dtr*thetacf(m))                                 
      enddo                                                              
c                                                                        
c     Start the case by case loop                                        
      nrawd=0                                                            
      nskip=0                                                            
 2001 continue                                                           
c                                                                        
c        Read header line for this case                                  
         read(luinp,100,err=751,end=2000) hline                          
  100    format(a130)                                                    
c                                                                        
c        Extract storm name and date information from header line        
         read(hline,102) sname,imyear,immon,imday,imtime,ihvmax          
  102    format(1x,a4,1x,3(i2),1x,i2,1x,i4)                              
c                                                                        
         write(lulog,748) sname,imyear,immon,imday,imtime                
  748    format(/,' HEADER: ',a4,1x,3(i2.2),1x,i2.2)                     
c                                                                        
         if (imyear .lt. 50) then                                        
            imyear4 = 2000 + imyear                                      
         else                                                            
            imyear4 = 1900 + imyear                                      
         endif                                                           
c                                                                        
         go to 5100                                                      
  751       write(lulog,*) ' Error reading input file (luinp)'           
            stop                                                         
 5100    continue                                                        
C                                                                        
         iline(1) = hline                                                
c                                                                        
         do k=-2,itmax                                                   
            irsst(k) = 9999                                              
         enddo                                                           
         idelvm = 9999                                                   
c                                                                        
c        Read the rest of the data lines for this case                   
c        and look for the LAT and LON lines.                             
         lcount=2                                                        
 5200    continue                                                        
            read(luinp,100,err=751,end=751) tline                        
            iline(lcount) = tline                                        
c                                                                        
            if (tline(117:120) .eq. 'LAT ') then                         
               read(tline,105) (islat(k),k=-2,itmax)                     
  105          format(23(1x,i4))                                         
            endif                                                        
C                                                                        
            if (tline(117:120) .eq. 'LON ') then                         
               read(tline,105) (islon(k),k=-2,itmax)                     
            endif                                                        
c                                                                        
            if (tline(117:120) .eq. 'RSST') then                         
               read(tline,105) (irsst(k),k=-2,itmax)                     
            endif                                                        
c                                                                        
            if (tline(117:120) .eq. 'DELV') then                         
               read(tline,105) idelvm                                    
            endif                                                        
c                                                                        
            if (tline(117:120) .eq. 'LAST') go to 5201                   
c                                                                        
            lcount=lcount+1                                              
            go to 5200                                                   
 5201    continue                                                        
c                                                                        
         nrawd = nrawd + 1                                               
         write(6,200) nrawd,hline                                        
  200    format(/,' START CASE',I4,' FIRST LINE OF LUINP HEADER:',/,A80) 
C                                                                        
         do 15 k=-2,itmax                                                
            slat(k) =      float(islat(k))/10.0                          
            slon(k) = -1.0*float(islon(k))/10.0                          
c                                                                        
            if (irsst(k) .lt. 9000) then                                 
               rsst(k) = 0.1*float(irsst(k))                             
            else                                                         
               rsst(k) = 9999.                                           
            endif                                                        
   15    continue                                                        
c                                                                        
c        Initialize synoptic variables to missing                        
         do 20 kt=0,itmax                                                
            iu200(kt) = 9999                                             
            iu200c(kt)= 9999                                             
            iv200c(kt)= 9999                                             
            it150(kt) = 9999                                             
            it200(kt) = 9999                                             
            it250(kt) = 9999                                             
            it000(kt) = 9999                                             
            iz000(kt) = 9999                                             
            ir000(kt) = 9999                                             
            ie000(kt) = 9999                                             
            iepos(kt) = 9999                                             
            ieneg(kt) = 9999                                             
            iepss(kt) = 9999                                             
            ienss(kt) = 9999                                             
            ishrd(kt) = 9999                                             
            ishtd(kt) = 9999                                             
            ishrs(kt) = 9999                                             
            ishts(kt) = 9999                                             
	    ishrg(kt) = 9999                                                    
	    ishxu(kt) = 9999                                                    
	    ishxl(kt) = 9999                                                    
            ivorb(kt) = 9999                                             
            idivb(kt) = 9999                                             
            irefc(kt) = 9999                                             
            ipefc(kt) = 9999                                             
	    irhlo(kt) = 9999                                                    
	    irhhi(kt) = 9999                                                    
	    irhmd(kt) = 9999                                                    
	    ipslv(kt) = 9999                                                    
c                                                                        
            itlat(kt) = 9999                                             
            itlon(kt) = 9999                                             
            itwac(kt) = 9999                                             
            itwbc(kt) = 9999                                             
            itwxc(kt) = 9999                                             
            irtcc(kt) = 9999                                             
            irtxc(kt) = 9999                                             
            ipsfc(kt) = 9999                                             
            ipsfcc(kt)= 9999                                             
c                                                                        
            ishdc(kt) = 9999                                             
            isddc(kt) = 9999                                             
            ishgc(kt) = 9999                                             
            it15c(kt) = 9999                                             
            it20c(kt) = 9999                                             
            it25c(kt) = 9999                                             
            iepoc(kt) = 9999                                             
            idivc(kt) = 9999                                             
c                                                                        
            ivkmpi(kt) = 9999                                            
            ipkmpi(kt) = 9999                                            
c                                                                        
            ivvavg(kt) = 9999                                            
            ivvavc(kt) = 9999                                            
            ivmflux(kt)= 9999                                            
   20    continue                                                        
c                                                                        
         ilost=0                                                         
         tlast=-6.0                                                      
c                                                                        
c        Start time loop                                                 
         do 99 kt=0,itmax                                                
            tnow = 6.0*float(kt)                                         
c                                                                        
c           Check for missing track positions                            
            if (slat(kt) .gt. 900.0) go to 99                            
c                                                                        
c           Construct rawd file                                          
            if (iatype .eq. 0) then                                      
c              Use analyses (re-analysis or operational) for predictors  
c                                                                        
               ktime = kt*idelt                                          
c                                                                        
c              Calculate date information for next analysis file         
	       call tadd(imyear,immon,imday,imtime,ktime,                       
     +                   iayear,iamon,iaday,iatime)                      
c                                                                        
               if (imyear4 .le. iray) then                               
                  rawdfn = 'R00055_X0000_PACK.DAT'                       
               else                                                      
                  rawdfn = 'A00055_X0000_PACK.DAT'                       
               endif                                                     
c                                                                        
               if (iatime .eq. 6 .or. iatime .eq. 18) then               
                   rawdfn(8:8) = 'Y'                                     
               endif                                                     
c                                                                        
               write(rawdfn(5:6),115) iayear                             
  115          format(i2.2)                                              
c                                                                        
               write(rawdfn(9:10),115) iamon                             
c                                                                        
               if (iatime .ge. 12) then                                  
                  iadayt = iaday + 50                                    
               else                                                      
                  iadayt = iaday                                         
               endif                                                     
               write(rawdfn(11:12),115) iadayt                           
	    else                                                                
c              Use forecast fields for the predictors. Try the           
c              forecast initialized at the time of this case.            
c              If that is not available, try a  6-hour old forecast.     
c                                                                        
               if (kt .eq. 0) then                                       
	          ilaghr = 0                                                    
	          ityear = imyear                                               
	          itmon  = immon                                                
	          itday  = imday                                                
	          ittime = imtime                                               
               endif                                                     
c                                                                        
 3001          continue                                                  
               rawdfn = 'A00055_X0000_PACK.DAT'                          
c                                                                        
               if (ittime .eq. 6 .or. ittime .eq. 18) then               
                   rawdfn(8:8) = 'Y'                                     
               endif                                                     
c                                                                        
               ktime = ilaghr + kt*idelt                                 
c                                                                        
               write(rawdfn(2:4),110) ktime                              
  110          format(i3.3)                                              
c                                                                        
               write(rawdfn(5:6),115) ityear                             
c                                                                        
               write(rawdfn(9:10),115) itmon                             
c                                                                        
               if (ittime .ge. 12) then                                  
                  itdayt = itday + 50                                    
               else                                                      
                  itdayt = itday                                         
               endif                                                     
               write(rawdfn(11:12),115) itdayt                           
c                                                                        
               if (kt .eq. 0) then                                       
c                 Check to see if first file is available. If not,       
c                 look for an earlier model run                          
		  call aunpack(ierr)                                                   
		  if (ierr .eq. 0) go to 3002                                          
c                                                                        
		  ilaghr = ilaghr + 6                                                  
c                                                                        
c                 Set the limit on how far back to look for previous mode
		  if (ilaghr .gt. 6) go to 3002                                        
c                                                                        
                  call tadd(imyear,immon,imday,imtime,-ilaghr,           
     +                      ityear,itmon,itday,ittime)                   
		  go to 3001                                                           
               endif                                                     
            endif                                                        
c                                                                        
 3002       continue                                                     
c                                                                        
c           Unpack the current rawd file                                 
            call aunpack(ierr)                                           
c                                                                        
            if (ierr .eq. 1 .and. kt .eq. 0) then                        
c              If first data file is missing, skip entire case           
               write(lulog,300)                                          
  300          format(' First data file must exist, skip case')          
               nskip=nskip+1                                             
               go to 2001                                                
            endif                                                        
c                                                                        
            if (ierr .eq. 1) then                                        
c              If subsequent data files are missing, skip                
c              calculation only for individual time periods              
               go to 99                                                  
            endif                                                        
c                                                                        
c           Initialize grid parameters at the current                    
c           storm location                                               
            call xyracal(slon(kt),slat(kt))                              
c                                                                        
c           Calculate x,y components of storm motion (m/s)               
            if (slat(kt-2) .lt. 900.0 .and.                              
     +          slat(kt  ) .lt. 900.0) then                              
               t2lat = slat(kt)                                          
               t2lon = slon(kt)                                          
               t1lat = slat(kt-2)                                        
               t1lon = slon(kt-2)                                        
               deltc = 2.0*delt                                          
	       icok = 1                                                         
            else                                                         
	       if (slat(kt+2) .lt. 900.0 .and.                                  
     +             slat(kt  ) .lt. 900.0 .and.                           
     +             kt+2       .le. itmax) then                           
                  t2lat = slat(kt+2)                                     
                  t2lon = slon(kt+2)                                     
                  t1lat = slat(kt)                                       
                  t1lon = slon(kt)                                       
                  deltc = 2.0*delt                                       
		  icok = 1                                                             
	       elseif (slat(kt+1) .lt. 900.0 .and.                              
     +                 slat(kt  ) .lt. 900.0 .and.                       
     +                 kt+1       .le. itmax) then                       
                  t2lat = slat(kt+1)                                     
                  t2lon = slon(kt+1)                                     
                  t1lat = slat(kt)                                       
                  t1lon = slon(kt)                                       
                  deltc = 1.0*delt                                       
		  icok = 1                                                             
               else                                                      
                  t2lat = slat(kt)                                       
                  t2lon = slon(kt)                                       
                  t1lat = slat(kt)                                       
                  t1lon = slon(kt)                                       
                  deltc = 1.0*delt                                       
		  icok = 0                                                             
               endif                                                     
            endif                                                        
c                                                                        
            call lltoxy(olons,olats,colat,t1lon,t1lat,temx1,temy1)       
            call lltoxy(olons,olats,colat,t2lon,t2lat,temx2,temy2)       
c                                                                        
            cx = 1000.0*(temx2-temx1)/(deltc*3600.0)                     
            cy = 1000.0*(temy2-temy1)/(deltc*3600.0)                     
c                                                                        
            if (kt .eq. 0) then                                          
               cx0 = cx                                                  
               cy0 = cy                                                  
            endif                                                        
c                                                                        
c           Get vertical profiles of required variables                  
            do 40 n=1,nvp                                                
               ptem=pvp(n)                                               
	       call varget('U',ptem,fxy,1,iexist)                               
               call fcopy(fxy,uxyp(1,1,n))                               
	       call aavg(fxy,radinn,radout,minpts,1,ierr,uvp(n))                
c                                                                        
	       call varget('V',ptem,fxy,1,iexist)                               
               call fcopy(fxy,vxyp(1,1,n))                               
	       call aavg(fxy,radinn,radout,minpts,1,ierr,vvp(n))                
c                                                                        
	       call varget('T',ptem,fxy,1,iexist)                               
               call fcopy(fxy,txyp(1,1,n))                               
	       call aavg(fxy,radinn,radout,minpts,1,ierr,tvp(n))                
c                                                                        
	       call varget('Z',ptem,fxy,1,iexist)                               
               call fcopy(fxy,zxyp(1,1,n))                               
	       call aavg(fxy,radinn,radout,minpts,1,ierr,zvp(n))                
c                                                                        
               if (ptem .ge. 300.0) then                                 
	          call varget('R',ptem,fxy,1,iexist)                            
c                                                                        
                  if (iatype .eq. 0 .and. ibcrh   .eq. 1                 
     +                              .and. imyear4 .le. iray) then        
c                    Apply bias correction to RH                         
                     call rhbc(fxy,ptem)                                 
                  endif                                                  
c                                                                        
                  call fcopy(fxy,rxyp(1,1,n))                            
	          call aavg(fxy,radinn,radout,minpts,1,ierr,rvp(n))             
               else                                                      
		  rvp(n) = 999.9                                                       
                  do j=1,ny                                              
                  do i=1,nx                                              
                     rxyp(i,j,n) = 999.9                                 
                  enddo                                                  
                  enddo                                                  
               endif                                                     
   40       continue                                                     
c                                                                        
c           Calculate thetae profile                                     
            do n=1,nvp                                                   
               tkel = tvp(n)                                             
               pmb  = pvp(n)                                             
               rh   = rvp(n)                                             
               if (rh .le. 0.0 .or. rh .gt. 99.9) rh = 50.0              
               call thetae(tkel,pmb,rh,plcl,tlcl,wmr,tevp(n))            
               qvp(n) = wmr                                              
               rvp(n) = rh                                               
c                                                                        
               rhs= 100.0                                                
               call thetae(tkel,pmb,rhs,plcl,tlcl,wmr,tevps(n))          
            enddo                                                        
c                                                                        
c           Save annular average u at 200 mb (in knots)                  
            iu200(kt) = ifix(10.0*1.944*uvp(i200))                       
c                                                                        
c           Save annular average T at 150,200 and 250 mb (in deg C)      
            it150(kt) = ifix( 10.0*(tvp(i150)-273.15) )                  
            it200(kt) = ifix( 10.0*(tvp(i200)-273.15) )                  
            it250(kt) = ifix( 10.0*(tvp(i250)-273.15) )                  
c                                                                        
c           Save annular average T,RH and Z at 1000 mb (in deg C)        
            it000(kt) = ifix( 10.0*(tvp(i000)-273.15) )                  
            ir000(kt) = ifix(rvp(i000))                                  
            iz000(kt) = ifix(zvp(i000))                                  
c                                                                        
c           Calculate and save sea level pressure                        
            call psext(tvp(i000),zvp(i000),psfc)                         
            ipsfc(kt) = ifix(10.0*(psfc-1000.0))                         
c                                                                        
c           Save annular average low-level RH                            
            irhlo(kt) = ifix( (rvp(i700)+rvp(i850))/2.0 )                
c                                                                        
c           Save annular average mid-level RH                            
            irhmd(kt) = ifix( (rvp(i500)+rvp(i700))/2.0 )                
c                                                                        
c           Save annular average high-level RH                           
            irhhi(kt) = ifix( (rvp(i300)+rvp(i400)+rvp(i500))/3.0 )      
c                                                                        
c           Save annular average thetae at 1000 mb                       
            ie000(kt) = ifix( 10.0*tevp(i000) )                          
c                                                                        
c           Calculate and save the thetae positive area                  
            epos = 0.0                                                   
            eneg = 0.0                                                   
            epss = 0.0                                                   
            enss = 0.0                                                   
            do n=1,nvp                                                   
               delte = tevp(i000) - tevp(n)                              
               deltes= tevp(i000) - tevps(n)                             
               if (delte  .gt. 0.0) epos = epos + wvp(n)*delte           
               if (delte  .lt. 0.0) eneg = eneg + wvp(n)*abs(delte)      
               if (deltes .gt. 0.0) epss = epss + wvp(n)*deltes          
               if (deltes .lt. 0.0) enss = enss + wvp(n)*abs(deltes)     
            enddo                                                        
            iepos(kt) = ifix( 10.0*epos )                                
            ieneg(kt) = ifix( 10.0*eneg )                                
            iepss(kt) = ifix( 10.0*epss )                                
            ienss(kt) = ifix( 10.0*enss )                                
c                                                                        
c           Calculate and save the 850-200 mb vertical shear             
            shearx = uvp(i200)-uvp(i850)                                 
            sheary = vvp(i200)-vvp(i850)                                 
	    call ctorh(shearx,sheary,shrd,shtd)                                 
            ishrd(kt) = ifix(10.0*1.944*shrd)                            
            ishtd(kt) = ifix(shtd)                                       
c                                                                        
c           Calculate and save the 850-500 mb vertical shear             
            shearx = uvp(i500)-uvp(i850)                                 
            sheary = vvp(i500)-vvp(i850)                                 
	    call ctorh(shearx,sheary,shrs,shts)                                 
            ishrs(kt) = ifix(10.0*1.944*shrs)                            
            ishts(kt) = ifix(shts)                                       
c                                                                        
c           Calculate and save the generalized shear parameter           
	    call gshear(uvp,vvp,wvp,nvp,shrg)                                   
	    ishrg(kt) = ifix(10.0*1.944*shrg)                                   
c                                                                        
c           Calculate and save the maximum shear in the                  
c           upper and lower part of the sounding                         
	    call xshear(uvp,vvp,pvp,nvp,i150,i500,shxu)                         
	    ishxu(kt) = ifix(10.0*1.944*shxu)                                   
c                                                                        
	    call xshear(uvp,vvp,pvp,nvp,i500,i000,shxl)                         
	    ishxl(kt) = ifix(10.0*1.944*shxl)                                   
c                                                                        
            ipsprt=1                                                     
            if (kt .eq. 0) then                                          
c              Calculate and save the steering pressure level            
               alpha = 0.4                                               
               if (icok .eq. 1) then                                     
                  call splcal(pvp,uvp,vvp,cx,cy,alpha,nvp,wt1,wt2,       
     +                        ubard,vbard,pbard,ubars,vbars,pbars)       
c                                                                        
                  if (ipsprt .eq. 1) then                                
		     write(lulog,749) alpha,cx,cy,ubard,vbard,pbard,                   
     +                                            ubars,vbars,pbars      
  749                format(/,' Steering pressure level output',         
     +                      /,' alpha=',f5.1,' cx,cy: ',2(f5.1,1x),      
     +                      /,' ub,vb,pb: ',3(f6.1,1x),                  
     +                      /,' us,vs,ps: ',3(f6.1,1x),                  
     +                     //,'  p     u     v     wd     ws     ws/wd', 
     +                        '  T     RH    ThE    ThEs')               
c                                                                        
		     do ll=1,nvp                                                       
                        tvptem = tvp(ll)-273.15                          
			write(lulog,750) pvp(ll),uvp(ll),vvp(ll),                             
     +                                   wt1(ll),wt2(ll),wt2(ll)/wt1(ll) 
     +                                  ,tvptem,rvp(ll),tevp(ll),        
     +                                                   tevps(ll)       
  750                   format(1x,f5.0,1x,f5.1,1x,f5.1,1x,               
     +                         f6.3,1x,f6.3,1x,f6.2,1x,f5.1,1x,f5.1,     
     +                         1x,f5.1,1x,f5.1)                          
                     enddo                                               
		  endif                                                                
               else                                                      
                  pbars = 525.0                                          
               endif                                                     
               ipslv(kt) = ifix(pbars)                                   
            endif                                                        
c                                                                        
c           Calculate area average 850 mb vorticity                      
            ptem = 850.0                                                 
            call voravg(ptem,slon(kt),slat(kt),radvor,vorbar,ierr)       
c                                                                        
            if (ierr .eq. 0) then                                        
               ivorb(kt) = ifix( (1.0e+7)*vorbar )                       
            else                                                         
               ivorb(kt) = 9999                                          
            endif                                                        
c                                                                        
c           Calculate area average 200 mb divergence                     
            ptem = 200.0                                                 
            call divavg(ptem,slon(kt),slat(kt),raddiv,divbar,ierr)       
c                                                                        
            if (ierr .eq. 0) then                                        
               idivb(kt) = ifix( (1.0e+7)*divbar )                       
            else                                                         
               idivb(kt) = 9999                                          
            endif                                                        
c                                                                        
c           Calculate relative eddy flux convergence of angular          
c           momentum                                                     
            ptem = 200.0                                                 
            call refcal(ptem,slon(kt),slat(kt),cx,cy,radrefc,refc)       
            irefc(kt) = ifix(refc)                                       
c                                                                        
c           Calculate planetary eddy flux convergence of angular         
c           momentum                                                     
            ptem = 200.0                                                 
            radpefc=1000.0                                               
            call pefcal(ptem,slon(kt),slat(kt),radpefc,pefc)             
            ipefc(kt) = ifix(pefc)                                       
c                                                                        
c           Calculate Kery Emanual MPI                                   
            sstkmpi = rsst(kt)                                           
            pskmpi  = psfc                                               
c                                                                        
c           Reverse order of P-level for KMPI routine                    
            do n=1,nvp                                                   
               nn = nvp - (n-1)                                          
               pkmpi(n) = pvp(nn)                                        
               tkmpi(n) = tvp(nn) - 273.15                               
               qkmpi(n) = qvp(nn)                                        
               rkmpi(n) = rvp(nn)                                        
            enddo                                                        
c                                                                        
            ikflag=0                                                     
            if (sstkmpi .lt. 35.0) then                                  
               call pcmin(sstkmpi,pskmpi,pkmpi,tkmpi,qkmpi,nvp,nvp,      
     +                    pmpi,vmpi,ikflag)                              
            endif                                                        
c                                                                        
            if (ikflag .eq. 1) then                                      
               ivkmpi(kt) = ifix(vmpi*1.944 + 0.5)                       
               ipkmpi(kt) = ifix(pmpi+0.5)                               
            else                                                         
               ivkmpi(kt) = 9999                                         
               ipkmpi(kt) = 9999                                         
            endif                                                        
c                                                                        
            if (kt .eq. 900) then                                        
               write(6,*) 'sst,psfc= ',sstkmpi,pskmpi                    
               do n=1,nvp                                                
                  write(6,821) pkmpi(n),tkmpi(n),qkmpi(n),rkmpi(n)       
  821             format(' p,t,q,rh: ',4(f7.1,1x))                       
               enddo                                                     
c              write(6,*) 'pmpi,vmpi: ',ipkmpi(kt),ivkmpi(kt)            
            endif                                                        
c                                                                        
c           Calculate convective mass flux from entraining parcel        
c           cloud model                                                  
                                                                         
            do n=1,nvp                                                   
               pkmpi(n) = pvp(n)                                         
               tkmpi(n) = tvp(n) - 273.15                                
               rkmpi(n) = rvp(n)                                         
            enddo                                                        
c                                                                        
            if (sstkmpi .lt. 35.0) then                                  
               nepx = nvp + 1                                            
               pkmpi(nepx) = psfc                                        
               tkmpi(nepx) = sstkmpi                                     
               rkmpi(nepx) = rkmpi(nvp)                                  
            else                                                         
               nepx = nvp                                                
            endif                                                        
c                                                                        
c           do n=1,nepx                                                  
c              write(6,333) pkmpi(n),tkmpi(n),rkmpi(n)                   
c 333          format('P,T,RH: ',3(f7.1,1x))                             
c           enddo                                                        
c                                                                        
            upx       = 15.0                                             
            zpx       = 0.0                                              
            radx      = 500.0                                            
c           radx      = 1000.0                                           
            cex       = 0.10                                             
            alphax    = 1.0/600.0                                        
            iicex     = 1                                                
            icweightx = 1                                                
            iprtx     = 0                                                
            call lcmod(pkmpi,tkmpi,rkmpi,nepx,upx,zpx,radx,              
     +                 cex,alphax,iicex,icweightx,iprtx,                 
     +                 vvavg,vmflux)                                     
c                                                                        
            if (vvavg .lt. 50.0) then                                    
               ivvavg(kt) = ifix(0.5 + 100.0*vvavg)                      
            else                                                         
               ivvavg(kt) = 9999                                         
            endif                                                        
c                                                                        
            if (vmflux .lt. 50.0) then                                   
               ivmflux(kt) = ifix(0.5 + 100.0*vmflux)                    
            else                                                         
               ivmflux(kt) = 9999                                        
            endif                                                        
c                                                                        
            if (kt .eq. 0) then                                          
               write(lulog,822) sstkmpi,pskmpi,                          
     +                          ipkmpi(kt),ivkmpi(kt),ihvmax,            
     +                          vvavg,slat(kt),slon(kt)                  
  822          format(/,'SST= ',f6.1,' PSFC=',f6.1,                      
     +                  ' PMPI=',i4,' VMPI=',i4,' VMAX=',i4,             
     +                  ' VVAV=',f7.1,' LAT=',f5.1,' LON=',f6.1)         
            endif                                                        
c                                                                        
c           ++ Start new code for vortex removal and adjusted predictors 
c                                                                        
c           Specify radius (km) for storm-relative avg divergence        
            raddivc = 1000.0                                             
            indxdivc = ifix(0.0001 + raddivc/drcf)                       
                                                                         
c           First guess location for vortex search                       
            if (kt .eq. 0) then                                          
               slatcf0 = slat(kt)                                        
               sloncf0 = slon(kt)                                        
            else                                                         
               slatcf0 = slatcf                                          
               sloncf0 = sloncf                                          
            endif                                                        
c                                                                        
            call lltoxy(olons,olats,colat,sloncf0,slatcf0,xcf0,ycf0)     
c                                                                        
c           Find 850 mb circulation center                               
            call cfindxy(uxyp(1,1,i850),vxyp(1,1,i850),rcf,thetacf,      
     +                   mrcf,mtcf,nrcf,ntcf,                            
     +                   radtwa,xcf0,ycf0,xcf,ycf,twa,rwa)               
c                                                                        
            call xytoll(olons,olats,colat,xcf,ycf,sloncf,slatcf)         
c                                                                        
            itlat(kt) = ifix( 10.0*slatcf)                               
            itlon(kt) = ifix(-10.0*sloncf)                               
c                                                                        
c           Check for lost vortex                                        
            rdist=sqrt( (xcf-xcf0)**2 + (ycf-ycf0)**2 )                  
            spdkt = (60.0/111.1)*rdist/(tnow-tlast)                      
            tlast = tnow                                                 
c                                                                        
            call spdlim(slatcf0,spdmax)                                  
c                                                                        
            if (ilost .eq. 0) then                                       
               if (spdkt .gt. spdmax) ilost=1                            
               if (twa   .lt.    1.0) ilost=1                            
            endif                                                        
c                                                                        
            if (ilost .eq. 0) then                                       
               itwac(kt) = ifix( 10.0*twa)                               
            else                                                         
               itwac(kt) = 9999                                          
            endif                                                        
c                                                                        
c           write(6,871) kt*6,slat(kt),slon(kt),                         
c    +                   slatcf0,sloncf0,slatcf,sloncf,twa,rwa,          
c    +                   spdkt,spdmax,ilost                              
c 871       format('t=',i3,' blat,blon: ',f6.2,1x,f7.2,                  
c    +                     ' lat0,lon0: ',f6.2,1x,f7.2,                  
c    +                     ' lat,lon: '  ,f6.2,1x,f7.2,                  
c    +             ' t,rwa: ',f6.1,1x,f6.1,                              
c    +             ' s,sm,ilost: ',f5.1,1x,f5.1,1x,i1)                   
c                                                                        
            if (ilost .eq. 0) then                                       
c              Filter thermodynamic variables and                        
c              remove vortex from wind field                             
c                                                                        
               fradlf = 400.0                                            
               irmflag = 1                                               
c                                                                        
               do ll=1,nvp                                               
                  call lfilter(txyp(1,1,ll),xcf,ycf,fradlf)              
                  call lfilter(rxyp(1,1,ll),xcf,ycf,fradlf)              
                  call lfilter(zxyp(1,1,ll),xcf,ycf,fradlf)              
c                                                                        
                  call vremove(uxyp(1,1,ll),vxyp(1,1,ll),rcf,thetacf,    
     +                         xcf,ycf,mrcf,mtcf,nrcf,ntcf,              
     +                                           uraa,vtaa,irmflag)      
c                                                                        
                  if (ll .eq. i200) then                                 
c                    Calculate storm-relative 200 mb area average diverge
                     divc = 2.0*uraa(indxdivc)/(1000.0*raddivc)          
                     idivc(kt) = ifix(divc*1.0e+7)                       
                  endif                                                  
c                                                                        
                  if (ll .eq. i850) then                                 
c                    Calculate maximum and average cyclonic tangential wi
c                                                                        
c                    Find last radial point where vtaa .ge. 1 starting at
                     do kk=4,nrcf                                        
                        nrlast = kk                                      
                        if (vtaa(kk) .lt. 1.0) then                      
                           nrlast = kk-1                                 
                           go to 1125                                    
                        endif                                            
                     enddo                                               
 1125                continue                                            
                     rtlast = rcf(nrlast)                                
c                                                                        
                     vtmax = -1000.0                                     
                     rtmax =  1000.0                                     
                     vtavg =  0.0                                        
                     do kk=0,nrlast                                      
                        vtavg = vtavg + vtaa(kk)                         
                        if (vtaa(kk) .gt. vtmax) then                    
                           vtmax = vtaa(kk)                              
                           rtmax = rcf(kk)                               
                        endif                                            
                     enddo                                               
                     vtavg = vtavg/(float(nrlast+1))                     
c                                                                        
                     irtcc(kt) = ifix(rtlast)                            
                     irtxc(kt) = ifix(rtmax)                             
                     itwxc(kt) = ifix(vtmax*10.0)                        
                     itwbc(kt) = ifix(vtavg*10.0)                        
                  endif                                                  
c                                                                        
c                 do kk=0,nrcf                                           
c                    write(6,873) tnow,pvp(ll),rcf(kk),uraa(kk),vtaa(kk) 
c 873                format(f5.0,1x,f5.0,1x,f5.0,1x,f6.1,1x,f6.1)        
c                 enddo                                                  
c                                                                        
               enddo                                                     
            endif                                                        
c                                                                        
c           Calculate surface pressure at edge of tangential wind area   
            dxtemp = xgk(2,1)-xgk(1,1)                                   
            dytemp = ygk(1,2)-ygk(1,1)                                   
            x1temp = xgk(1,1)                                            
            y1temp = ygk(1,1)                                            
c                                                                        
            if (ilost .eq. 0) then                                       
               xcftemp = xcf                                             
               ycftemp = ycf                                             
               nrlastt = nrlast                                          
            else                                                         
               xcftemp = 0.0                                             
               ycftemp = 0.0                                             
               nrlastt = 16                                              
            endif                                                        
c                                                                        
            do j=0,ntcf                                                  
            do i=0,nrcf                                                  
               xtemp = xcftemp + rcf(i)*ctheta(j)                        
               ytemp = ycftemp + rcf(i)*stheta(j)                        
c                                                                        
               call lintcf(zxyp(1,1,i000),x1temp,dxtemp,                 
     +                                    y1temp,dytemp,                 
     +                     ixmx,iymx,nx,ny,                              
     +                     xtemp,ytemp,zcrt(i,j))                        
               call lintcf(txyp(1,1,i000),x1temp,dxtemp,                 
     +                                    y1temp,dytemp,                 
     +                     ixmx,iymx,nx,ny,                              
     +                     xtemp,ytemp,tcrt(i,j))                        
            enddo                                                        
            enddo                                                        
c                                                                        
            call azavgcf(zcrt,zraa,mrcf,mtcf,nrcf,ntcf)                  
            call azavgcf(tcrt,traa,mrcf,mtcf,nrcf,ntcf)                  
c                                                                        
c           do i=0,nrcf                                                  
c              write(6,*) kt,rcf(i),zraa(i),traa(i)                      
c           enddo                                                        
c                                                                        
            z00 = zraa(nrlastt)                                          
            t00 = traa(nrlastt)                                          
            call psext(t00,z00,psfc)                                     
            ipsfcc(kt) = ifix(10.0*(psfc-1000.0))                        
c           ipsfcc(kt) = ifix(psfc+0.5)                                  
c                                                                        
c           write(6,889) z00,t00,ipsfcc(kt),ipsfc(kt),nrlastt            
c 889       format('z00,t00,psfcc,psfc,nrlastt: ',                       
c    +             2(f7.1,1x),i4,1x,i4,1x,i2)                            
c                                                                        
c           Azimuthally average u,v,t,r,z                                
c                                                                        
            do ll=1,nvp                                                  
	       call aavg(uxyp(1,1,ll),radinnc,radoutc,minpts,1,                 
     +                                          ierr,uvp(ll))            
	       call aavg(vxyp(1,1,ll),radinnc,radoutc,minpts,1,                 
     +                                          ierr,vvp(ll))            
	       call aavg(txyp(1,1,ll),radinnc,radoutc,minpts,1,                 
     +                                          ierr,tvp(ll))            
	       call aavg(zxyp(1,1,ll),radinnc,radoutc,minpts,1,                 
     +                                          ierr,zvp(ll))            
               if (pvp(ll) .ge. 300.0) then                              
	          call aavg(rxyp(1,1,ll),radinnc,radoutc,minpts,1,              
     +                                             ierr,rvp(ll))         
               else                                                      
		  rvp(ll) = 999.9                                                      
               endif                                                     
c              write(6,875) pvp(ll),uvp(ll),vvp(ll),tvp(ll),rvp(ll)      
c 875          format('p,u,v,t,r: ',5(f7.1,1x))                          
            enddo                                                        
c                                                                        
c           Calculate and save the 850-500 mb vertical shear             
            shearx = uvp(i200)-uvp(i850)                                 
            sheary = vvp(i200)-vvp(i850)                                 
	    call ctorh(shearx,sheary,shdc,sddc)                                 
            ishdc(kt) = ifix(10.0*1.944*shdc)                            
            isddc(kt) = ifix(sddc)                                       
c                                                                        
c           Calculate and save the generalized shear parameter           
	    call gshear(uvp,vvp,wvp,nvp,shgc)                                   
	    ishgc(kt) = ifix(10.0*1.944*shgc)                                   
c                                                                        
c           Calculate convective mass flux from entraining parcel        
c           cloud model with corrected T/RH profiles                     
            do n=1,nvp                                                   
               pkmpi(n) = pvp(n)                                         
               tkmpi(n) = tvp(n) - 273.15                                
               rkmpi(n) = rvp(n)                                         
            enddo                                                        
c                                                                        
            if (sstkmpi .lt. 35.0) then                                  
               nepx = nvp + 1                                            
               pkmpi(nepx) = psfc                                        
               tkmpi(nepx) = sstkmpi                                     
               rkmpi(nepx) = rkmpi(nvp)                                  
            else                                                         
               nepx = nvp                                                
            endif                                                        
c                                                                        
            call lcmod(pkmpi,tkmpi,rkmpi,nepx,upx,zpx,radx,              
     +                 cex,alphax,iicex,icweightx,iprtx,                 
     +                 vvavg,vmflux)                                     
c                                                                        
            if (vvavg .lt. 50.0) then                                    
               ivvavc(kt) = ifix(0.5 + 100.0*vvavg)                      
            else                                                         
               ivvavc(kt) = 9999                                         
            endif                                                        
c                                                                        
c           Save annular average T at 150,200 and 250 mb (in deg C)      
            it15c(kt) = ifix( 10.0*(tvp(i150)-273.15) )                  
            it20c(kt) = ifix( 10.0*(tvp(i200)-273.15) )                  
            it25c(kt) = ifix( 10.0*(tvp(i250)-273.15) )                  
c                                                                        
c           Save u200c and v200c                                         
            iu200c(kt) = ifix(10.0*1.944*uvp(i200))                      
            iv200c(kt) = ifix(10.0*1.944*vvp(i200))                      
c                                                                        
c           Calculate thetae profile                                     
            do n=1,nvp                                                   
               tkel = tvp(n)                                             
               pmb  = pvp(n)                                             
               rh   = rvp(n)                                             
               if (rh .le. 0.0 .or. rh .gt. 99.9) rh = 50.0              
               call thetae(tkel,pmb,rh,plcl,tlcl,wmr,tevp(n))            
               rhs= 100.0                                                
               call thetae(tkel,pmb,rhs,plcl,tlcl,wmr,tevps(n))          
            enddo                                                        
c                                                                        
c           Calculate and save the thetae positive area                  
            epos = 0.0                                                   
            eneg = 0.0                                                   
            epss = 0.0                                                   
            enss = 0.0                                                   
            do n=1,nvp                                                   
               delte = tevp(i000) - tevp(n)                              
               deltes= tevp(i000) - tevps(n)                             
               if (delte  .gt. 0.0) epos = epos + wvp(n)*delte           
               if (delte  .lt. 0.0) eneg = eneg + wvp(n)*abs(delte)      
               if (deltes .gt. 0.0) epss = epss + wvp(n)*deltes          
               if (deltes .lt. 0.0) enss = enss + wvp(n)*abs(deltes)     
            enddo                                                        
            iepoc(kt) = ifix( 10.0*epos )                                
c                                                                        
c           ++ End new code for vortex removal and adjusted predictors   
   99    continue                                                        
c                                                                        
c        ++ Start code to calculate proxy GOES predictors                
c           for use when GOES data                                       
c        is missing.                                                     
         imiss=9999                                                      
         rmiss=9999.                                                     
c                                                                        
         if (islat(0) .ne. imiss) then                                   
            glat = 0.1*float(islat(0))                                   
         else                                                            
            glat = rmiss                                                 
         endif                                                           
c                                                                        
         if (islon(0) .ne. imiss) then                                   
            glon = -0.1*float(islon(0))                                  
         else                                                            
            glon = rmiss                                                 
         endif                                                           
         if (glon .lt. 0.0) glon = glon + 360.0                          
c                                                                        
         grsst = rsst(0)                                                 
         gvmax  = float(ihvmax)                                          
c                                                                        
         if (ishdc(0) .ne. imiss) then                                   
            gshdc = 0.1*float(ishdc(0))                                  
         else                                                            
            gshdc = rmiss                                                
         endif                                                           
c                                                                        
         if (idelvm .ne. imiss) then                                     
            gdelv = float(idelvm)                                        
         else                                                            
            gdelv = 0.0                                                  
         endif                                                           
c                                                                        
         if (it200(0) .ne. imiss) then                                   
            gt200 = 0.1*it200(0)                                         
         else                                                            
            gt200 = rmiss                                                
         endif                                                           
c                                                                        
         if (idivb(0) .ne. imiss) then                                   
            gd200 = idivb(0)                                             
         else                                                            
            gd200 = rmiss                                                
         endif                                                           
c                                                                        
         gspd = 1.944*sqrt(cx0*cx0 + cy0*cy0)                            
c                                                                        
         call bassel(glat,glon,ibasin)                                   
         call ir00param(ibasin,glat,grsst,gvmax,gshdc,gdelv,gt200,       
     +                  gd200,gspd,rmiss,pgoes,ierr)                     
c                                                                        
         if (ierr .ne. 0) then                                           
            do i=0,itmax                                                 
               ipgoes(i) = imiss                                         
            enddo                                                        
         else                                                            
            ipgoes(0) = 0                                                
            do i=1,16                                                    
               ipgoes(i) = ifix(pgoes(i))                                
            enddo                                                        
            do i=17,itmax                                                
               ipgoes(i) = imiss                                         
            enddo                                                        
         endif                                                           
c                                                                        
         write(6,817) glat,glon,grsst,gvmax,gshdc,gdelv,gt200,gd200,     
     +                gspd,ibasin                                        
  817    format('ginput ',9(f7.1),1x,i2)                                 
c                                                                        
c        ++ End code to calculate proxy GOES predictors                  
c                                                                        
c        Write input lines to output file (except the last line)         
         do 16 i=1,lcount-1                                              
            write(luout,100) iline(i)                                    
   16    continue                                                        
c                                                                        
c        Set iskip=1 to skip all but a few variables                     
         iskip=0                                                         
c                                                                        
c        Write out synoptic variables for this case                      
         if (iskip .eq. 0) then                                          
            write(luout,210) (iu200(k),k=0,itmax)                        
  210       format(10x,21(1x,i4),1x,'U200')                              
            write(luout,208) (iu200c(k),k=0,itmax)                       
  208       format(10x,21(1x,i4),1x,'U20C')                              
            write(luout,209) (iv200c(k),k=0,itmax)                       
  209       format(10x,21(1x,i4),1x,'V20C')                              
            write(luout,212) (ie000(k),k=0,itmax)                        
  212       format(10x,21(1x,i4),1x,'E000')                              
            write(luout,213) (iepos(k),k=0,itmax)                        
  213       format(10x,21(1x,i4),1x,'EPOS')                              
            write(luout,214) (ieneg(k),k=0,itmax)                        
  214       format(10x,21(1x,i4),1x,'ENEG')                              
            write(luout,215) (iepss(k),k=0,itmax)                        
  215       format(10x,21(1x,i4),1x,'EPSS')                              
            write(luout,216) (ienss(k),k=0,itmax)                        
  216       format(10x,21(1x,i4),1x,'ENSS')                              
            write(luout,217) (irhlo(k),k=0,itmax)                        
  217       format(10x,21(1x,i4),1x,'RHLO')                              
            write(luout,218) (irhmd(k),k=0,itmax)                        
  218       format(10x,21(1x,i4),1x,'RHMD')                              
            write(luout,219) (irhhi(k),k=0,itmax)                        
  219       format(10x,21(1x,i4),1x,'RHHI')                              
c                                                                        
            write(luout,231) (ipslv(k),k=0,itmax)                        
  231       format(10x,21(1x,i4),1x,'PSLV')                              
            write(luout,232) (ivorb(k),k=0,itmax)                        
  232       format(10x,21(1x,i4),1x,'Z850')                              
            write(luout,233) (idivb(k),k=0,itmax)                        
  233       format(10x,21(1x,i4),1x,'D200')                              
c                                                                        
            tlabel='REFC'                                                
            write(luout,236) (irefc(k),k=0,itmax),tlabel                 
            tlabel='PEFC'                                                
            write(luout,236) (ipefc(k),k=0,itmax),tlabel                 
c                                                                        
            tlabel='T000'                                                
            write(luout,236) (it000(k),k=0,itmax),tlabel                 
            tlabel='R000'                                                
            write(luout,236) (ir000(k),k=0,itmax),tlabel                 
            tlabel='Z000'                                                
            write(luout,236) (iz000(k),k=0,itmax),tlabel                 
c                                                                        
            write(luout,239) (itlat(k),k=0,itmax)                        
  239       format(10x,21(1x,i4),1x,'TLAT')                              
            write(luout,240) (itlon(k),k=0,itmax)                        
  240       format(10x,21(1x,i4),1x,'TLON')                              
            write(luout,241) (itwac(k),k=0,itmax)                        
  241       format(10x,21(1x,i4),1x,'TWAC')                              
c           write(luout,260) (itwbc(k),k=0,itmax)                        
c 260       format(10x,21(1x,i4),1x,'TWBC')                              
            write(luout,261) (itwxc(k),k=0,itmax)                        
  261       format(10x,21(1x,i4),1x,'TWXC')                              
c           write(luout,262) (irtcc(k),k=0,itmax)                        
c 262       format(10x,21(1x,i4),1x,'RTCC')                              
c           write(luout,263) (irtxc(k),k=0,itmax)                        
c 263       format(10x,21(1x,i4),1x,'RTXC')                              
            write(luout,264) (ipsfcc(k),k=0,itmax)                       
  264       format(10x,21(1x,i4),1x,'PENC')                              
            write(luout,242) (ishdc(k),k=0,itmax)                        
  242       format(10x,21(1x,i4),1x,'SHDC')                              
            write(luout,243) (isddc(k),k=0,itmax)                        
  243       format(10x,21(1x,i4),1x,'SDDC')                              
            write(luout,244) (ishgc(k),k=0,itmax)                        
  244       format(10x,21(1x,i4),1x,'SHGC')                              
c           write(luout,245) (it15c(k),k=0,itmax)                        
c 245       format(10x,21(1x,i4),1x,'T15C')                              
c           write(luout,246) (it20c(k),k=0,itmax)                        
c 246       format(10x,21(1x,i4),1x,'T20C')                              
c           write(luout,247) (it25c(k),k=0,itmax)                        
c 247       format(10x,21(1x,i4),1x,'T25C')                              
c           write(luout,248) (iepoc(k),k=0,itmax)                        
c 248       format(10x,21(1x,i4),1x,'EPOC')                              
            write(luout,249) (idivc(k),k=0,itmax)                        
  249       format(10x,21(1x,i4),1x,'DIVC')                              
c                                                                        
         endif                                                           
c                                                                        
         write(luout,311) (it150(k),k=0,itmax)                           
  311    format(10x,21(1x,i4),1x,'T150')                                 
         write(luout,312) (it200(k),k=0,itmax)                           
  312    format(10x,21(1x,i4),1x,'T200')                                 
         write(luout,313) (it250(k),k=0,itmax)                           
  313    format(10x,21(1x,i4),1x,'T250')                                 
         write(luout,220) (ishrd(k),k=0,itmax)                           
  220    format(10x,21(1x,i4),1x,'SHRD')                                 
         write(luout,222) (ishtd(k),k=0,itmax)                           
  222    format(10x,21(1x,i4),1x,'SHTD')                                 
         write(luout,225) (ishrs(k),k=0,itmax)                           
  225    format(10x,21(1x,i4),1x,'SHRS')                                 
         write(luout,227) (ishts(k),k=0,itmax)                           
  227    format(10x,21(1x,i4),1x,'SHTS')                                 
         write(luout,228) (ishrg(k),k=0,itmax)                           
  228    format(10x,21(1x,i4),1x,'SHRG')                                 
c                                                                        
         if (imxshr .eq. 1) then                                         
            write(luout,229) (ishxu(k),k=0,itmax)                        
  229       format(10x,21(1x,i4),1x,'SHXU')                              
            write(luout,230) (ishxl(k),k=0,itmax)                        
  230       format(10x,21(1x,i4),1x,'SHXL')                              
         endif                                                           
c                                                                        
         tlabel='PENV'                                                   
         write(luout,236) (ipsfc(k),k=0,itmax),tlabel                    
  236    format(10x,21(1x,i4),1x,a4)                                     
c                                                                        
         tlabel='VMPI'                                                   
         write(luout,236) (ivkmpi(k),k=0,itmax),tlabel                   
c        tlabel='PMPI'                                                   
c        write(luout,236) (ipkmpi(k),k=0,itmax),tlabel                   
c                                                                        
         tlabel='VVAV'                                                   
         write(luout,236) (ivvavg(k),k=0,itmax),tlabel                   
         tlabel='VMFX'                                                   
         write(luout,236) (ivmflux(k),k=0,itmax),tlabel                  
         tlabel='VVAC'                                                   
         write(luout,236) (ivvavc(k),k=0,itmax),tlabel                   
c                                                                        
         tlabel='IRXX'                                                   
         write(luout,236) (ipgoes(k),k=0,itmax),tlabel                   
c                                                                        
c        Write out last line                                             
         write(luout,100) iline(lcount)                                  
c                                                                        
C        Do next case                                                    
      go to 2001                                                         
C                                                                        
 2000 continue                                                           
C                                                                        
      WRITE(LULOG,350) nrawd,nskip                                       
      WRITE(6,350) nrawd,nskip                                           
  350 FORMAT(/,' NORMAL COMPLETION OF LSDIAG, ',I4,' CASES PROCESSED ',  
     +                                          I4,' SKIPPED')           
C                                                                        
      return                                                             
      END                                                                
      subroutine psext(t00,z00,psfc)                                     
c     This routine calculates the surface pressure in hPa                
c     by extrapolating from the 1000 mb height surface.                  
c                                                                        
c     Input: t00 = temperature (K) at 1000 mb                            
c            z00 = height deviation (m) of 1000 mb from the height of the
c                  standard atmosphere.                                  
c                                                                        
      gamma = 0.0065                                                     
      aa    = 9.81/(287.0*gamma)                                         
      p00 = 1000.0                                                       
      call stndz(p00,zb00,tb00,thb00)                                    
      z00t= zb00+z00                                                     
      t11 = t00 + gamma*z00t                                             
c                                                                        
      psfc= p00*( (t11/t00)**aa )                                        
c                                                                        
      return                                                             
      END                                                                
      subroutine ssfcal(slon,slat,ssx,ssy,ssize,shear,refc,pefc)         
c     This routine calculates the storm motion vector (ssx,ssy),         
c     storm size (ssize), vertical shear along the storm track           
c     (shear), and the relative (refc) and planetary (pefc) eddy         
c     flux convergence of angular momentum.                              
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,index                                                       
      common /indexa/ indexp,indexv                                      
      common /indexn/ indexvn                                            
      parameter (nvar=5)                                                 
      dimension indexp(ipmx),indexv(nvar)                                
      character *1 indexvn(nvar)                                         
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
c     Other variables                                                    
      dimension  slat(-2:7), slon(-2:7)                                  
      dimension shear(0:6)                                               
c                                                                        
c     f(x,y) variables                                                   
      dimension u200(ixmx,iymx),v200(ixmx,iymx)                          
      dimension u850(ixmx,iymx),v850(ixmx,iymx)                          
c                                                                        
      dimension us200(ixmx,iymx),vs200(ixmx,iymx)                        
      dimension us850(ixmx,iymx),vs850(ixmx,iymx)                        
c                                                                        
      dimension ur850(ixmx,iymx),vt850(ixmx,iymx)                        
      dimension ur200(ixmx,iymx),vt200(ixmx,iymx)                        
c                                                                        
      dimension ur850cb(ixmx,iymx),vt850cb(ixmx,iymx)                    
      dimension ur200cb(ixmx,iymx),vt200cb(ixmx,iymx)                    
c                                                                        
      dimension u850b(ixmx,iymx),v850b(ixmx,iymx)                        
      dimension u200b(ixmx,iymx),v200b(ixmx,iymx)                        
c                                                                        
c     f(r,a) variables                                                   
      dimension ur850p(irmx,iamx),vt850p(irmx,iamx)                      
      dimension ur200p(irmx,iamx),vt200p(irmx,iamx)                      
c                                                                        
      dimension f(irmx,iamx),t1ra(irmx,iamx),t2ra(irmx,iamx)             
c                                                                        
c     f(r) variables                                                     
      dimension ur850b(irmx),vt850b(irmx)                                
      dimension ur200b(irmx),vt200b(irmx)                                
c                                                                        
      dimension fb(irmx),pefc(irmx),refc(irmx)                           
      dimension t1r(irmx),t2r(irmx)                                      
c                                                                        
c     ********************                                               
c                                                                        
c     ++ Shear calculation parameters ++                                 
c                                                                        
c     Specify radius (km) for shear calculation                          
      radshr = 600.0                                                     
c                                                                        
c     Specify minimum points for shear calculation                       
      minpts = 10                                                        
c                                                                        
c     ++ Size calculation parameters ++                                  
      rsmin = 395.0                                                      
      rsmax = 805.0                                                      
      vnorm = 5.0                                                        
c                                                                        
c     ++ End parameter specification                                     
c                                                                        
      slat0 = slat(0)                                                    
      slon0 = slon(0)                                                    
c                                                                        
c     Calculate grid information relative to initial storm position      
      call xyracal(slon0,slat0)                                          
c                                                                        
c     Calculate x,y components of storm motion                           
      IF (SLAT(-1) .LT. 900.0 .AND. SLAT(0) .LT. 900.0) THEN             
         T2LAT = SLAT(0)                                                 
         T2LON = SLON(0)                                                 
         T1LAT = SLAT(-1)                                                
         T1LON = SLON(-1)                                                
      ELSEIF (SLAT(0) .LT. 900.0 .AND. SLAT(1) .LT. 900.0) THEN          
         T2LAT = SLAT(1)                                                 
         T2LON = SLON(1)                                                 
         T1LAT = SLAT(0)                                                 
         T1LON = SLON(0)                                                 
      ELSE                                                               
         WRITE(LULOG,904)                                                
  904    FORMAT(/,' NOT ENOUGH VALID TRACK POINTS FOR STORM SPEED')      
         STOP                                                            
      ENDIF                                                              
C                                                                        
      call lltoxy(olons,olats,colat,t1lon,t1lat,temx1,temy1)             
      call lltoxy(olons,olats,colat,t2lon,t2lat,temx2,temy2)             
c                                                                        
      ssx = 1000.0*(temx2-temx1)/(12.0*3600.0)                           
      ssy = 1000.0*(temy2-temy1)/(12.0*3600.0)                           
c                                                                        
c     Calculate Coriolis parameter at all of the polar grid points       
      do 9 j=1,ntheta                                                    
      do 9 i=1,nrad                                                      
         xtemp = xra(i,j)                                                
         ytemp = yra(i,j)                                                
         call xytoll(olons,olats,colat,xtemp,ytemp,tlon,tlat)            
         f(i,j) = 2.0*erot*sin(dtr*tlat)                                 
    9 continue                                                           
c                                                                        
c     Get 200 and 850 winds                                              
      call varget('U',200.0,u200,1,iexist)                               
      call varget('V',200.0,v200,1,iexist)                               
      call varget('U',850.0,u850,1,iexist)                               
      call varget('V',850.0,v850,1,iexist)                               
c                                                                        
c     Calculate radial and tangential winds at 850,200                   
      call uvtort(u200,v200,ur200,vt200)                                 
      call uvtort(u850,v850,ur850,vt850)                                 
c                                                                        
c     Interpolate 850,200 mb radial,tangential wind to polar grid        
      call ctop(ur200,ur200p)                                            
      call ctop(vt200,vt200p)                                            
      call ctop(ur850,ur850p)                                            
      call ctop(vt850,vt850p)                                            
c                                                                        
c     Azimuthally average polar grid winds                               
      call azavg(ur200p,ur200b,0)                                        
      call azavg(vt200p,vt200b,0)                                        
      call azavg(ur850p,ur850b,0)                                        
      call azavg(vt850p,vt850b,0)                                        
c                                                                        
c     Azimuthally average Coriolis parameter                             
      call azavg(f,fb,1)                                                 
c                                                                        
c     Calculate storm size                                               
      anorm = 0.0                                                        
      aram  = 0.0                                                        
      do 20 i=1,nrad                                                     
         if (radk(i) .gt. rsmin .and. radk(i) .lt. rsmax) then           
            aram  = aram + vt850b(i)*radk(i)*radk(i)                     
            anorm = anorm + vnorm*radk(i)*radk(i)                        
         endif                                                           
   20 continue                                                           
      if (anorm .gt. 0.0) then                                           
         ssize = aram/anorm                                              
      else                                                               
         ssize=0.0                                                       
      endif                                                              
c                                                                        
      write(lulog,301) ssize                                             
  301 format(/,' Size= ',f6.2)                                           
c                                                                        
c     Calculate planetary eddy flux momentum convergence                 
c     in units of m/s/day                                                
      do 22 j=1,ntheta                                                   
      do 22 i=1,nrad                                                     
         t1ra(i,j) = -(ur200p(i,j)-ur200b(i))*(f(i,j)-fb(i))             
   22 continue                                                           
      call azavg(t1ra,pefc,0)                                            
c                                                                        
      do 23 i=1,nrad                                                     
         pefc(i) = pefc(i)*24.0*3600.0                                   
   23 continue                                                           
c                                                                        
c     Calculate relative eddy flux momentum convergence                  
c                                                                        
c     Calculate -U'V' in storm relative coordinates                      
      do 26 j=1,ntheta                                                   
         ctheta = cos(dtr*thetad(j))                                     
         stheta = sin(dtr*thetad(j))                                     
         ssrad = ssx*ctheta + ssy*stheta                                 
         sstan =-ssx*stheta + ssy*ctheta                                 
         do 28 i=1,nrad                                                  
            t1ra(i,j) = -(ur200p(i,j) - (ssrad + ur200b(i)))*            
     +                   (vt200p(i,j) - (sstan + vt200b(i)))             
   28    continue                                                        
   26 continue                                                           
c                                                                        
c     Azimuthally average -U'V'                                          
      call azavg(t1ra,t1r,0)                                             
c                                                                        
c     Take radial derivative of averaged -U'V'.                          
      call ddrcal(t1r,t2r)                                               
c                                                                        
c     Calculate relative flux convergence in m/s/day                     
      refc(1) = 24.*3600.*t2r(1)                                         
      do 29 i=2,nrad                                                     
         refc(i) = 24.*3600.*(2.*t1r(i)/(1000.*radk(i)) + t2r(i))        
   29 continue                                                           
c                                                                        
      write(lulog,302)                                                   
  302 format(/,'  r(km) ur850b vt850b ur200b vt200b   refc  pefc')       
      do 15 i=1,nrad                                                     
         write(lulog,304) radk(i),ur850b(i),vt850b(i),                   
     +                            ur200b(i),vt200b(i),                   
     +                    refc(i),pefc(i)                                
  304    format(1x,f7.1,6(f6.1,1x))                                      
   15 continue                                                           
c                                                                        
c     Interpolate azimuthally averaged radial,tangential                 
c     wind back to Cartesian grid.                                       
      call patoc(ur200b,ur200cb)                                         
      call patoc(vt200b,vt200cb)                                         
      call patoc(ur850b,ur850cb)                                         
      call patoc(vt850b,vt850cb)                                         
c                                                                        
c     Convert radial and tangetial winds to Cartesian components         
      call rttouv(ur200cb,vt200cb,u200b,v200b)                           
      call rttouv(ur850cb,vt850cb,u850b,v850b)                           
c                                                                        
c     Subtract azimuthally averaged flow from u,v                        
      do 25 j=1,ny                                                       
      do 25 i=1,nx                                                       
         us200(i,j) = u200(i,j)-u200b(i,j)                               
         vs200(i,j) = v200(i,j)-v200b(i,j)                               
         us850(i,j) = u850(i,j)-u850b(i,j)                               
         vs850(i,j) = v850(i,j)-v850b(i,j)                               
   25 continue                                                           
c                                                                        
c     Calculate vertical shear                                           
      do 30 k=0,6                                                        
c        Calculate grid information                                      
         slatt =  slat(k)                                                
         slont =  slon(k)                                                
         if (slatt .gt. 900.0 .or. slont .gt. 900.0) then                
            ua200  = 999.9                                               
            va200  = 999.9                                               
            ua850  = 999.9                                               
            va850  = 999.9                                               
            shrtem = 999.9                                               
            go to 1030                                                   
         endif                                                           
c                                                                        
         if (k .gt. 0) call xyracal(slont,slatt)                         
c                                                                        
c        Horizontally average 850,200 mb winds                           
         call havg(us200,radshr,minpts,0,ierr1,ua200)                    
         call havg(vs200,radshr,minpts,0,ierr2,va200)                    
         call havg(us850,radshr,minpts,0,ierr3,ua850)                    
         call havg(vs850,radshr,minpts,0,ierr4,va850)                    
c                                                                        
c        Check for missing data                                          
         ierrs = ierr1 + ierr2 + ierr3 + ierr4                           
         if (ierrs .gt. 0) then                                          
            ua200  = 999.9                                               
            va200  = 999.9                                               
            ua850  = 999.9                                               
            va850  = 999.9                                               
            shrtem = 999.9                                               
            go to 1030                                                   
         endif                                                           
c                                                                        
c        Convert average winds to kts                                    
         ua200 = 1.944*ua200                                             
         va200 = 1.944*va200                                             
         ua850 = 1.944*ua850                                             
         va850 = 1.944*va850                                             
c                                                                        
         shrtem = sqrt( (ua200-ua850)**2 + (va200-va850)**2 )            
 1030    continue                                                        
c                                                                        
         shear(k) = shrtem                                               
         ttime = 12.0*float(k)                                           
c                                                                        
         write(lulog,303) ttime,slatt,slont                              
  303    format(/' time,lat,lon: ',3(f6.1,1x))                           
c                                                                        
         write(lulog,300) ua850,va850,ua200,va200,shrtem                 
  300    format(' u850,v850,u200,v200,shr: ',5(f6.1,1x))                 
   30 continue                                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine pncal                                                   
c     This routine specifies physical and numerical constants            
c                                                                        
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
c                                                                        
      pi = 3.14159265                                                    
      dtr = pi/180.0                                                     
c                                                                        
      dtk = 111.1                                                        
c                                                                        
      erad = 6371.0                                                      
      erot = 7.292E-5                                                    
c                                                                        
      return                                                             
      END                                                                
      subroutine refcal(ptem,rlon,rlat,cx,cy,radmax,refc)                
c     This routine calculates the relative eddy                          
c     flux convergence (m/s/day). The refc is calculated                 
c     in storm relative coordinates, and is radially                     
c     averaged.                                                          
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
c     Local variables                                                    
      dimension u(ixmx,iymx),v(ixmx,iymx),ur(ixmx,iymx),vt(ixmx,iymx)    
      dimension vtp(irmx,iamx),urp(irmx,iamx)                            
      dimension upvp(irmx,iamx)                                          
      dimension urpb(irmx),vtpb(irmx)                                    
      dimension upvpb(irmx),dupvpb(irmx),rrefc(irmx)                     
c                                                                        
      ierr=0                                                             
c                                                                        
c     Get u and v                                                        
      ifatal=0                                                           
      call varget('U',ptem,u,ifatal,iexu)                                
      call varget('V',ptem,v,ifatal,iexv)                                
c                                                                        
      if (iexu .ne. 1 .or. iexv .ne. 1) then                             
         ierr=1                                                          
         refc = 0.0                                                      
         return                                                          
      endif                                                              
c                                                                        
c     Convert u and v to storm relative coordinates                      
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
         u(i,j) = u(i,j) - cx                                            
         v(i,j) = v(i,j) - cy                                            
   10 continue                                                           
c                                                                        
c     Calculate radial and tangential winds                              
      call xyracal(rlon,rlat)                                            
      call uvtort(u,v,ur,vt)                                             
c                                                                        
c     Interpolate radial and tangential winds to polar grid              
      call ctop(ur,urp)                                                  
      call ctop(vt,vtp)                                                  
c                                                                        
c     Azimuthally average ur and vt                                      
      call azavg(urp,urpb,0)                                             
      call azavg(vtp,vtpb,0)                                             
c                                                                        
c     Calculate U'V'                                                     
      do 20 j=1,ntheta                                                   
      do 20 i=1,nrad                                                     
         upvp(i,j) = (urp(i,j) - urpb(i))*                               
     +               (vtp(i,j) - vtpb(i))                                
   20 continue                                                           
c                                                                        
c     Azimuthally average U'V'                                           
      call azavg(upvp,upvpb,0)                                           
c                                                                        
c     Take radial derivative of averaged U'V'.                           
      call ddrcal(upvpb,dupvpb)                                          
c                                                                        
c     Calculate relative flux convergence in m/s/day                     
      cf = -24.0*3600.0                                                  
      rrefc(1) = cf*dupvpb(1)                                            
      do 30 i=2,nrad                                                     
         rrefc(i) = cf*(2.*upvpb(i)/(1000.*radk(i)) + dupvpb(i))         
   30 continue                                                           
c                                                                        
      refc = 0.0                                                         
      icount = 0                                                         
      do 40 i=2,nrad                                                     
         if (radk(i) .gt. radmax) go to 2040                             
         refc = refc + rrefc(i)                                          
         icount = icount + 1                                             
   40 continue                                                           
c                                                                        
 2040 continue                                                           
      if (icount .ge. 1) then                                            
         refc = refc/float(icount)                                       
      else                                                               
         refc = 0.0                                                      
      endif                                                              
c                                                                        
      return                                                             
      END                                                                
      subroutine pefcal(ptem,rlon,rlat,radmax,pefc)                      
c     This routine calculates the planetary eddy                         
c     flux convergence (m/s/day). The pefc is radially averaged.         
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
c                                                                        
c     Local variables                                                    
      dimension u(ixmx,iymx),v(ixmx,iymx),ur(ixmx,iymx),vt(ixmx,iymx)    
      dimension urp(irmx,iamx)                                           
      dimension urpb(irmx)                                               
c                                                                        
c     Local variables for Coriolis calculation                           
      dimension f(irmx,iamx),fb(irmx)                                    
      dimension t1ra(irmx,iamx),t1r(irmx)                                
c                                                                        
      ierr=0                                                             
c                                                                        
c     Get u and v                                                        
      ifatal=0                                                           
      call varget('U',ptem,u,ifatal,iexu)                                
      call varget('V',ptem,v,ifatal,iexv)                                
c                                                                        
      if (iexu .ne. 1 .or. iexv .ne. 1) then                             
         ierr=1                                                          
         pefc = 0.0                                                      
         return                                                          
      endif                                                              
c                                                                        
c     Calculate radial and tangential winds                              
      call xyracal(rlon,rlat)                                            
      call uvtort(u,v,ur,vt)                                             
c                                                                        
c     Interpolate radial winds to polar grid                             
      call ctop(ur,urp)                                                  
c                                                                        
c     Azimuthally average ur                                             
      call azavg(urp,urpb,0)                                             
c                                                                        
c     Calculate Coriolis parameter at all of the polar grid points       
      do j=1,ntheta                                                      
      do i=1,nrad                                                        
         xtemp = xra(i,j)                                                
         ytemp = yra(i,j)                                                
         call xytoll(olons,olats,colat,xtemp,ytemp,tlon,tlat)            
         f(i,j) = 2.0*erot*sin(dtr*tlat)                                 
      enddo                                                              
      enddo                                                              
c                                                                        
c     Azimuthally average Coriolis parameter                             
      call azavg(f,fb,1)                                                 
c                                                                        
c     Calculate planetary eddy flux momentum convergence                 
c     in units of m/s/day                                                
      do j=1,ntheta                                                      
      do i=1,nrad                                                        
         t1ra(i,j) = -(urp(i,j)-urpb(i))*(f(i,j)-fb(i))                  
      enddo                                                              
      enddo                                                              
      call azavg(t1ra,t1r,0)                                             
c                                                                        
      do i=1,nrad                                                        
         t1r(i) = t1r(i)*24.0*3600.0                                     
      enddo                                                              
c                                                                        
      pefc = 0.0                                                         
      icount = 0                                                         
      do i=2,nrad                                                        
         if (radk(i) .gt. radmax) go to 2040                             
         pefc = pefc + t1r(i)                                            
         icount = icount + 1                                             
      enddo                                                              
c                                                                        
 2040 continue                                                           
      if (icount .ge. 1) then                                            
         pefc = pefc/float(icount)                                       
      else                                                               
         pefc = 0.0                                                      
      endif                                                              
c                                                                        
      return                                                             
      END                                                                
      subroutine divavg(ptem,rlon,rlat,radtem,divbar,ierr)               
c     This routine calculates the area averaged                          
c     divergence at level ptem by azimuthally averaging                  
c     the radial wind.                                                   
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
c                                                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
c     Local variables                                                    
      dimension u(ixmx,iymx),v(ixmx,iymx),ur(ixmx,iymx),vt(ixmx,iymx)    
      dimension urp(irmx,iamx),urpb(irmx)                                
c                                                                        
      ierr=0                                                             
c                                                                        
c     Get u and v                                                        
      ifatal=0                                                           
      call varget('U',ptem,u,ifatal,iexu)                                
      call varget('V',ptem,v,ifatal,iexv)                                
c                                                                        
      if (iexu .ne. 1 .or. iexv .ne. 1) then                             
         ierr=1                                                          
         divbar=0.0                                                      
         return                                                          
      endif                                                              
c                                                                        
c     Calculate radial and tangential winds                              
      call xyracal(rlon,rlat)                                            
      call uvtort(u,v,ur,vt)                                             
c                                                                        
c     Interpolate radial wind to polar grid                              
      call ctop(ur,urp)                                                  
c                                                                        
c     Azimuthally average vtp                                            
      call azavg(urp,urpb,0)                                             
c                                                                        
c     Find radial grid point closest to requested radius                 
      irad = 0                                                           
      do 10 i=3,nrad                                                     
         if (radk(i) .gt. radtem) then                                   
            irad = i-1                                                   
            go to 1000                                                   
         endif                                                           
   10 continue                                                           
c                                                                        
 1000 continue                                                           
      if (irad .le. 0) then                                              
         ierr=1                                                          
         divbar=0.0                                                      
         return                                                          
      endif                                                              
c                                                                        
      divbar = 2.0*urpb(irad)/(1000.0*radk(irad))                        
c                                                                        
      return                                                             
      END                                                                
      subroutine voravg(ptem,rlon,rlat,radtem,vorbar,ierr)               
c     This routine calculates the area averaged relative                 
c     vorticity at level ptem by azimuthally averaging                   
c     the tangential wind.                                               
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
c                                                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
c     Local variables                                                    
      dimension u(ixmx,iymx),v(ixmx,iymx),ur(ixmx,iymx),vt(ixmx,iymx)    
      dimension vtp(irmx,iamx),vtpb(irmx)                                
c                                                                        
      ierr=0                                                             
c                                                                        
c     Get u and v                                                        
      ifatal=0                                                           
      call varget('U',ptem,u,ifatal,iexu)                                
      call varget('V',ptem,v,ifatal,iexv)                                
c                                                                        
      if (iexu .ne. 1 .or. iexv .ne. 1) then                             
         ierr=1                                                          
         vorbar=0.0                                                      
         return                                                          
      endif                                                              
c                                                                        
c     Calculate radial and tangential winds                              
      call xyracal(rlon,rlat)                                            
      call uvtort(u,v,ur,vt)                                             
c                                                                        
c     Interpolate tangential wind to polar grid                          
      call ctop(vt,vtp)                                                  
c                                                                        
c     Azimuthally average vtp                                            
      call azavg(vtp,vtpb,0)                                             
c                                                                        
c     Find radial grid point closest to requested radius                 
      irad = 0                                                           
      do 10 i=3,nrad                                                     
         if (radk(i) .gt. radtem) then                                   
            irad = i-1                                                   
            go to 1000                                                   
         endif                                                           
   10 continue                                                           
c                                                                        
 1000 continue                                                           
      if (irad .le. 0) then                                              
         ierr=1                                                          
         vorbar=0.0                                                      
         return                                                          
      endif                                                              
c                                                                        
      vorbar = 2.0*vtpb(irad)/(1000.0*radk(irad))                        
c                                                                        
      return                                                             
      END                                                                
      subroutine defcal(ptem,defxy,ierr)                                 
c     This routine calculates the horizontal deformation at pressure     
c     level ptem. The grid is defined by the last call to xyracal.       
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
      dimension defxy(ixmx,iymx)                                         
c                                                                        
c     Local variables                                                    
      dimension uxy(ixmx,iymx),vxy(ixmx,iymx)                            
      dimension dudx(ixmx,iymx),dudy(ixmx,iymx)                          
      dimension dvdx(ixmx,iymx),dvdy(ixmx,iymx)                          
c                                                                        
c     Get u and v                                                        
      call varget('U',ptem,uxy,0,iexu)                                   
      call varget('V',ptem,vxy,0,iexv)                                   
      if (iexu .ne. 1 .or. iexv .ne. 1) then                             
	 ierr = 1                                                               
	 return                                                                 
      endif                                                              
c                                                                        
c     calculate required derivatives                                     
      call dxcal(uxy,dudx)                                               
      call dycal(uxy,dudy)                                               
      call dxcal(vxy,dvdx)                                               
      call dycal(vxy,dvdy)                                               
c                                                                        
c     Calculate the magnitude of the horizontal deformation vector       
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
	 defxy(i,j) = sqrt( (dudy(i,j)+dvdx(i,j))**2 +                          
     +                      (dudx(i,j)-dvdy(i,j))**2 )                   
   10 continue                                                           
c                                                                        
      ierr = 0                                                           
c                                                                        
      return                                                             
      end                                                                
      subroutine dxcal(f,dfdx)                                           
c     This routine calculates the x derivative of f using centered       
c     differences, and one-sided differences on the boundaries.          
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
      dimension f(ixmx,iymx),dfdx(ixmx,iymx)                             
c                                                                        
c     Calculate dx in meters                                             
      dx = 1000.0*(xgk(2,1) - xgk(1,1))                                  
      tdx = 2.0*dx                                                       
c                                                                        
c     Calculate centered differences                                     
      do 10 j=1,ny                                                       
      do 10 i=2,nx-1                                                     
	 dfdx(i,j) = (f(i+1,j) - f(i-1,j))/tdx                                  
   10 continue                                                           
c                                                                        
c     Calculate one-sided differences                                    
      do 20 j=1,ny                                                       
	 dfdx( 1,j) = (f( 2,j) - f(   1,j))/dx                                  
	 dfdx(nx,j) = (f(nx,j) - f(nx-1,j))/dx                                  
   20 continue                                                           
c                                                                        
      return                                                             
      end                                                                
      subroutine dycal(f,dfdy)                                           
c     This routine calculates the y derivative of f using centered       
c     differences, and one-sided differences on the boundaries.          
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
      dimension f(ixmx,iymx),dfdy(ixmx,iymx)                             
c                                                                        
c     Calculate dy in meters                                             
      dy = 1000.0*(ygk(1,2) - ygk(1,1))                                  
      tdy = 2.0*dy                                                       
c                                                                        
c     Calculate centered differences                                     
      do 10 i=1,nx                                                       
      do 10 j=2,ny-1                                                     
	 dfdy(i,j) = (f(i,j+1) - f(i,j-1))/tdy                                  
   10 continue                                                           
c                                                                        
c     Calculate one-sided differences                                    
      do 20 i=1,nx                                                       
	 dfdy(i, 1) = (f(i, 2) - f(i,   1))/dy                                  
	 dfdy(i,ny) = (f(i,ny) - f(i,ny-1))/dy                                  
   20 continue                                                           
c                                                                        
      return                                                             
      end                                                                
      subroutine gshear(uvp,vvp,wvp,nvp,shrg)                            
c     This routine calculates a generalized shear parameter, which       
c     includes contributes from nvp pressure levels                      
c                                                                        
      dimension uvp(nvp),vvp(nvp),wvp(nvp)                               
c                                                                        
c     Calculate the vertically averaged wind                             
      ubar = 0.0                                                         
      vbar = 0.0                                                         
      do 10 n=1,nvp                                                      
	 ubar = ubar + wvp(n)*uvp(n)                                            
	 vbar = vbar + wvp(n)*vvp(n)                                            
   10 continue                                                           
c                                                                        
c     Calculate generarlized shear                                       
      shrg = 0.0                                                         
      do 20 n=1,nvp                                                      
         shrg = shrg + wvp(n)*sqrt( (uvp(n)-ubar)**2 +                   
     +                              (vvp(n)-vbar)**2 )                   
   20 continue                                                           
c                                                                        
c     Add factor to make generalized shear equal to two level shear      
c     for linear shear profiles                                          
      shrg = 4.0*shrg                                                    
c                                                                        
c     do 30 n=1,nvp                                                      
c        write(6,100) n,uvp(n),vvp(n),wvp(n),ubar,vbar,shrg              
c 100    format(1x,'n,u,v,w,ub,vb,sg: ',i2,6(f6.2,1x))                   
c  30 continue                                                           
c                                                                        
      return                                                             
      end                                                                
      subroutine xshear(uvp,vvp,pvp,nvp,i1,i2,shrx)                      
c     This routine calculates the maximum shear in the layer             
c     pvp(i1) to pvp(i2). The max shear magnitude is normalized          
c     to the 850 to 200 mb layer.                                        
c                                                                        
      dimension uvp(nvp),vvp(nvp),pvp(nvp)                               
c                                                                        
c     Check input                                                        
      if (i2 .gt. i1) then                                               
	 n1 = i1                                                                
	 n2 = i2                                                                
      elseif (i2 .lt. i1) then                                           
	 n1 = i2                                                                
	 n2 = i1                                                                
      else                                                               
	 shrx = 999.9                                                           
	 return                                                                 
      endif                                                              
c                                                                        
      if (n1 .gt. nvp .or. n2 .gt. nvp) then                             
	 shrx = 999.9                                                           
	 return                                                                 
      endif                                                              
c                                                                        
      if (n1 .lt. 1 .or. n2 .lt. 1) then                                 
	 shrx = 999.9                                                           
	 return                                                                 
      endif                                                              
c                                                                        
c     Calculate the vertically averaged wind                             
      shrx = -999.9                                                      
      dpn  = (850.0-200.0)                                               
      do 10 n=n1,n2-1                                                    
	 du = (uvp(n+1)-uvp(n))                                                 
	 dv = (vvp(n+1)-vvp(n))                                                 
	 dp = (pvp(n+1)-pvp(n))                                                 
	 shrt = sqrt(du*du + dv*dv)*dpn/dp                                      
c                                                                        
	 if (shrt .gt. shrx) shrx = shrt                                        
   10 continue                                                           
c                                                                        
      return                                                             
      end                                                                
      subroutine vshear(ps1,ps2,rlon,rlat,radkt,minpts,shear,sheard)     
c     This routine calculates the magnitude (shear) and direction        
c     (sheard) of the vertical shear between pressure                    
c     levels ps1,ps2 (mb).  The horizontal velocities are first averaged 
c     over a circle of radius radkt (km), centered at rlon,rlat. The     
c     shear is set to 999.9 if there are less than minpts included       
c     in the horizontal average. The direction of the shear is in        
c     degrees clockwise from north.                                      
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,prima                                                       
      common /primv/ u,v,z,t,r                                           
      dimension u(ixmx,iymx,ipmx),v(ixmx,iymx,ipmx),z(ixmx,iymx,ipmx)    
      dimension t(ixmx,iymx,ipmx),r(ixmx,iymx,ipmx)                      
c                                                                        
C.DUP lsdiag,index                                                       
      common /indexa/ indexp,indexv                                      
      common /indexn/ indexvn                                            
      parameter (nvar=5)                                                 
      dimension indexp(ipmx),indexv(nvar)                                
      character *1 indexvn(nvar)                                         
C.DUP lsdiag,latlon                                                      
       common /latlon/  RLATMN,RLATMX,RLONMN,RLONMX,DLAT,DLON,           
     +                  RLATD,RLOND                                      
       dimension rlatd(iymx),rlond(ixmx)                                 
       common /ilatlon/ NLAT1,NLON1                                      
C.DUP lsdiag,plevs                                                       
      common /plevs/ plev,plevr                                          
      dimension plev(ipmx),plevr(ipmx)                                   
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
c     Local variables                                                    
      dimension rad(ixmx,iymx)                                           
c                                                                        
c     Find indicies of required pressure levels                          
      ips1 = 0                                                           
      ips2 = 0                                                           
      do 10 k=1,ipmx                                                     
         if (plevr(k) .eq. ps1) ips1=k                                   
         if (plevr(k) .eq. ps2) ips2=k                                   
   10 continue                                                           
c                                                                        
      if (ips1 .eq. 0 .or. ips2 .eq. 0) then                             
         write(lulog,900) ps1,ps2                                        
  900    format(/,' Pressure level not found in routine vshear',         
     +            ' ps1,ps2: ' ,f6.1,1x,f6.1)                            
         stop                                                            
      endif                                                              
c                                                                        
      if (indexp(ips1) .eq. 0 .or. indexp(ips2) .eq. 0) then             
         write(lulog,902) ips1,ips2                                      
  902    format(/,' Pressure level not available on data file',          
     +            ' ps1,ps2: ',f6.1,1x,f6.1)                             
         stop                                                            
      endif                                                              
c                                                                        
      if (indexv(1) .eq. 0 .or. indexv(2) .eq. 0) then                   
         write(lulog,904)                                                
  904    format(/,' Wind data not available for shear calculation.')     
         stop                                                            
      endif                                                              
c                                                                        
c     Calculate the radius of each grid point                            
      call xyracal(rlon,rlat)                                            
c                                                                        
c     Apply horizontal average to wind components                        
      ubar1=0.0                                                          
      ubar2=0.0                                                          
      vbar1=0.0                                                          
      vbar2=0.0                                                          
      nbar =0                                                            
      do 20 j=1,nlat1                                                    
      do 20 i=1,nlon1                                                    
         if (rgk(i,j) .le. radkt) then                                   
            ubar1 = ubar1 + u(i,j,ips1)                                  
            ubar2 = ubar2 + u(i,j,ips2)                                  
            vbar1 = vbar1 + v(i,j,ips1)                                  
            vbar2 = vbar2 + v(i,j,ips2)                                  
            nbar = nbar + 1                                              
         endif                                                           
   20 continue                                                           
c                                                                        
      if (nbar .lt. minpts) then                                         
         write(lulog,800) nbar,minpts                                    
  800    format(/,' Not enough data points for shear calculation.',      
     +            ' nbar,minpts: ',i4,1x,i4)                             
         shear = 999.9                                                   
         return                                                          
      endif                                                              
c                                                                        
      rnbar = float(nbar)                                                
      ubar1 = ubar1/rnbar                                                
      ubar2 = ubar2/rnbar                                                
      vbar1 = vbar1/rnbar                                                
      vbar2 = vbar2/rnbar                                                
c                                                                        
      shearx = ubar2 - ubar1                                             
      sheary = vbar2 - vbar1                                             
      call ctorh(shearx,sheary,shear,sheard)                             
c                                                                        
c     Convert shear to knots                                             
      shear = 1.944*shear                                                
c                                                                        
      return                                                             
      END                                                                
      subroutine xyracal(olon,olat)                                      
c     This routine calculates the x and y coordinates and radius         
c     in km and azimuth in deg relative to the origin olon,olat          
c     (olon is deg W negative, olat is deg N positive)                   
c     at all of the Cartesian grid points.                               
c     Then, the radii and azimuths of a polar coordinate system          
c     centered at olon,olat are calculated. Finally, the array pmask     
c     is calculated which contains 0.0 or 1.0 if the polar grid point    
c     is outside or inside of the Cartesian grid.                        
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,latlon                                                      
       common /latlon/  RLATMN,RLATMX,RLONMN,RLONMX,DLAT,DLON,           
     +                  RLATD,RLOND                                      
       dimension rlatd(iymx),rlond(ixmx)                                 
       common /ilatlon/ NLAT1,NLON1                                      
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
c     *************************                                          
c                                                                        
c     Save lat,lon of origin                                             
      olons = olon                                                       
      olats = olat                                                       
      colat = cos(dtr*olat)                                              
c                                                                        
c     Determine number of x,y grid points                                
      nx = nlon1                                                         
      ny = nlat1                                                         
c                                                                        
c     Calculate x,y,r and azimuth of the Cartesian grid                  
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
         tlon = rlond(i)                                                 
         tlat = rlatd(j)                                                 
         call lltoxy(olon,olat,colat,tlon,tlat,xtem,ytem)                
         xgk(i,j) = xtem                                                 
         ygk(i,j) = ytem                                                 
   10 continue                                                           
c                                                                        
      do 15 j=1,ny                                                       
      do 15 i=1,nx                                                       
         rgk(i,j) = sqrt(xgk(i,j)**2 + ygk(i,j)**2)                      
         if (rgk(i,j) .gt. 0.0) then                                     
            agd(i,j) =  ( acos(xgk(i,j)/rgk(i,j)) )/dtr                  
         else                                                            
            agd(i,j) = 0.0                                               
         endif                                                           
   15 continue                                                           
c                                                                        
      xmax = xgk(nx,1)                                                   
      xmin = xgk(1,1)                                                    
      ymax = ygk(1,ny)                                                   
      ymin = ygk(1,1)                                                    
c                                                                        
c     Calculate azimuthal coordinates                                    
      ntheta = iamx                                                      
      dtheta = 360.0/float(ntheta)                                       
      do 20 j=1,ntheta                                                   
         thetad(j) = dtheta*float(j-1)                                   
   20 continue                                                           
c                                                                        
c     Specify radial interval in km                                      
      drad = 100.0                                                       
c                                                                        
c     Find maximum radius value on Cartesian grid                        
      radmax = -1000.0                                                   
      do 25 j=1,ny                                                       
      do 25 i=1,nx                                                       
         if (rgk(i,j) .gt. radmax) radmax=rgk(i,j)                       
   25 continue                                                           
c                                                                        
c     Calculate radial coordinates                                       
      nrad = 2 + ifix(radmax/drad)                                       
      if (nrad .gt. irmx) then                                           
         write(lulog,900) nrad,irmx                                      
  900    format(/,' nrad too big in routine xyracal, increase irmx.',    
     +          /,' nrad,irmx: ',i5,1x,i5)                               
         stop                                                            
      endif                                                              
c                                                                        
      do 30 i=1,nrad                                                     
         radk(i) = drad*float(i-1)                                       
   30 continue                                                           
c                                                                        
c     Calculate x,y values at polar grid points                          
      do 35 j=1,ntheta                                                   
      do 35 i=1,nrad                                                     
         xra(i,j) = radk(i)*cos(dtr*thetad(j))                           
         yra(i,j) = radk(i)*sin(dtr*thetad(j))                           
   35 continue                                                           
c                                                                        
c     Calculate polar coordinate mask                                    
      do 40 j=1,ntheta                                                   
      do 40 i=1,nrad                                                     
         xtem = xra(i,j)                                                 
         ytem = yra(i,j)                                                 
         pmask(i,j) = 1.0                                                
         if (xtem .ge. xmax .or. xtem .le. xmin) pmask(i,j)=0.0          
         if (ytem .ge. ymax .or. ytem .le. ymin) pmask(i,j)=0.0          
   40 continue                                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine lltoxy(olon,olat,colat,tlon,tlat,xtem,ytem)             
c     This routine calculates the x,y coordinates (xtem,ytem) of the     
c     point with longitude and latitude tlon,tlat relative to a          
c     coordinate system with origin at olon,olat.  In the current        
c     version, a simple tangent plane approximation is used for the      
c     transformation.                                                    
c                                                                        
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
c                                                                        
      xtem = dtk*(tlon-olon)*colat                                       
      ytem = dtk*(tlat-olat)                                             
c                                                                        
      return                                                             
      END                                                                
      subroutine xytoll(olon,olat,colat,xtem,ytem,tlon,tlat)             
c     This routine calculates the longitude and latitude tlon,tlat       
c     of the point with x,y coordinates xtem,tem                         
c     relative to a coordinate system with origin at                     
c     olon,olat.  In the current version, a simple tangent plane         
c     approximation is used for the transformation.                      
c                                                                        
C.DUP lsdiag,pncons                                                      
      common /pncons/ pi,dtr,dtk,erad,erot                               
c                                                                        
      tlon = olon + xtem/(dtk*colat)                                     
      tlat = olat + ytem/(dtk)                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine uvtort(u,v,ur,vt)                                       
c     This routine calculates the radial (ur) and tangential (vt)        
c     winds at the Cartesian grid points from the Cartesian              
c     velocity components u,v.                                           
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
c     Other variables                                                    
      dimension u(ixmx,iymx),v(ixmx,iymx),ur(ixmx,iymx),vt(ixmx,iymx)    
c                                                                        
c     ********************                                               
c                                                                        
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
         radtem = amax1(0.1,rgk(i,j))                                    
         ctem = xgk(i,j)/radtem                                          
         stem = ygk(i,j)/radtem                                          
         ur(i,j) =  ctem*u(i,j) + stem*v(i,j)                            
         vt(i,j) = -stem*u(i,j) + ctem*v(i,j)                            
   10 continue                                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine rttouv(ur,vt,u,v)                                       
c     This routine calculates the Cartesian velocity components u,v      
c     from the radial (ur) and tangential (vt) winds at the              
c     Cartesian grid points.                                             
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
c     Other variables                                                    
      dimension u(ixmx,iymx),v(ixmx,iymx),ur(ixmx,iymx),vt(ixmx,iymx)    
c                                                                        
c     ********************                                               
c                                                                        
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
         radtem = amax1(0.1,rgk(i,j))                                    
         ctem = xgk(i,j)/radtem                                          
         stem = ygk(i,j)/radtem                                          
         u(i,j) =  ctem*ur(i,j) - stem*vt(i,j)                           
         v(i,j) =  stem*ur(i,j) + ctem*vt(i,j)                           
   10 continue                                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine varget(vtype,press,fxy,ifatal,iexist)                   
c     This routine gets the variable vtype at pressure level press       
c     and puts it in the array fxy.                                      
c                                                                        
c     If ifatal=1 then execution is terminated if the requested          
c                 field is not available.                                
c     If ifatal=0 then iexist is set to 1 (0) if the requested           
c                 field exists (does not exist). Execution is not        
c                 terminated if ifatal=0.                                
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,prima                                                       
      common /primv/ u,v,z,t,r                                           
      dimension u(ixmx,iymx,ipmx),v(ixmx,iymx,ipmx),z(ixmx,iymx,ipmx)    
      dimension t(ixmx,iymx,ipmx),r(ixmx,iymx,ipmx)                      
C.DUP lsdiag,index                                                       
      common /indexa/ indexp,indexv                                      
      common /indexn/ indexvn                                            
      parameter (nvar=5)                                                 
      dimension indexp(ipmx),indexv(nvar)                                
      character *1 indexvn(nvar)                                         
C.DUP lsdiag,latlon                                                      
       common /latlon/  RLATMN,RLATMX,RLONMN,RLONMX,DLAT,DLON,           
     +                  RLATD,RLOND                                      
       dimension rlatd(iymx),rlond(ixmx)                                 
       common /ilatlon/ NLAT1,NLON1                                      
C.DUP lsdiag,plevs                                                       
      common /plevs/ plev,plevr                                          
      dimension plev(ipmx),plevr(ipmx)                                   
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
c     Other variables                                                    
      character *1 vtype                                                 
      dimension fxy(ixmx,iymx)                                           
c                                                                        
c     ********************                                               
c                                                                        
c     Search for variable type                                           
      do 10 n=1,nvar                                                     
         if (indexvn(n) .eq. vtype) then                                 
            idv = n                                                      
            go to 1000                                                   
         endif                                                           
   10 continue                                                           
c                                                                        
      write(lulog,900) vtype                                             
  900 format(/,' Unrecognized variable type: ',a1,' in routine varget.') 
      stop                                                               
 1000 continue                                                           
c                                                                        
c     Check to make sure variable is available                           
      if (indexv(idv) .eq. 0) then                                       
         if (ifatal .eq. 1) then                                         
            write(lulog,902) vtype                                       
  902       format(/,' Variable ',a1,                                    
     +               ' not available on data input file.',               
     +             /,' Processing halted in routine varget.')            
            stop                                                         
         else                                                            
            write(lulog,802) vtype                                       
  802       format(/,' Variable ',a1,                                    
     +               ' not available on data input file.')               
            iexist=0                                                     
            return                                                       
         endif                                                           
      endif                                                              
c                                                                        
c     Search for pressure level                                          
      do 15 k=1,ipmx                                                     
         if (plevr(k) .eq. press) then                                   
            idp = k                                                      
            if (indexp(k) .eq. 0) go to 1495                             
            go to 1500                                                   
         endif                                                           
 1495    continue                                                        
   15 continue                                                           
c                                                                        
      write(lulog,904) press                                             
  904 format(/,' Pressure level: ',e11.4,                                
     +         ' not found in routine varget.')                          
      if (ifatal .eq. 1) then                                            
         stop                                                            
      else                                                               
         iexist=0                                                        
         return                                                          
      endif                                                              
c                                                                        
 1500 continue                                                           
      iexist=1                                                           
c                                                                        
c     Extract variable                                                   
      if (idv .eq. 1) then                                               
         do 20 j=1,nlat1                                                 
         do 20 i=1,nlon1                                                 
            fxy(i,j) = u(i,j,idp)                                        
   20    continue                                                        
      elseif (idv .eq. 2) then                                           
         do 25 j=1,nlat1                                                 
         do 25 i=1,nlon1                                                 
            fxy(i,j) = v(i,j,idp)                                        
   25    continue                                                        
      elseif (idv .eq. 3) then                                           
         do 30 j=1,nlat1                                                 
         do 30 i=1,nlon1                                                 
            fxy(i,j) = z(i,j,idp)                                        
   30    continue                                                        
      elseif (idv .eq. 4) then                                           
         do 35 j=1,nlat1                                                 
         do 35 i=1,nlon1                                                 
            fxy(i,j) = t(i,j,idp)                                        
   35    continue                                                        
      elseif (idv .eq. 5) then                                           
         do 40 j=1,nlat1                                                 
         do 40 i=1,nlon1                                                 
            fxy(i,j) = r(i,j,idp)                                        
   40    continue                                                        
      else                                                               
         write(lulog,908) idv                                            
  908    format(/,' Illegal variable number ',i2,' in routine varget.')  
         stop                                                            
      endif                                                              
c                                                                        
      return                                                             
      END                                                                
      subroutine ctop(fxy,fra)                                           
c     This routine linearly interpolates the function fxy on             
c     the Cartesian grid to the function fra on the polar grid.          
c     fra is set to zero for points on the polar grid outside            
c     of the Cartesian grid.                                             
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,latlon                                                      
       common /latlon/  RLATMN,RLATMX,RLONMN,RLONMX,DLAT,DLON,           
     +                  RLATD,RLOND                                      
       dimension rlatd(iymx),rlond(ixmx)                                 
       common /ilatlon/ NLAT1,NLON1                                      
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
c     Other variables                                                    
      dimension fxy(ixmx,iymx),fra(irmx,iamx)                            
c                                                                        
      nlonck = nlon1-1                                                   
      nlatck = nlat1-1                                                   
c                                                                        
      do 10 j=1,ntheta                                                   
      do 10 i=1,nrad                                                     
         if (pmask(i,j) .lt. 0.5) then                                   
            fra(i,j) = 0.0                                               
         else                                                            
            xtem = xra(i,j)                                              
            ytem = yra(i,j)                                              
            call xytoll(olons,olats,colat,xtem,ytem,tlon,tlat)           
c                                                                        
c           Calculate x,y indices of the point closet to, and to the     
c           lower left of the current polar coordinate grid point.       
            idx = 1 + ifix( (tlon-rlond(1))/dlon )                       
            idy = 1 + ifix( (tlat-rlatd(1))/dlat )                       
c                                                                        
c           Check bounds of x,y indices                                  
            if (idx .lt. 1 .or. idx .gt. nlonck) then                    
               write(lulog,900) idx                                      
  900          format(/,' idx=',i4,' out of bounds in routine ctop.')    
               stop                                                      
            endif                                                        
c                                                                        
            if (idy .lt. 1 .or. idy .gt. nlatck) then                    
               write(lulog,902) idy                                      
  902          format(/,' idy=',i4,' out of bounds in routine ctop.')    
               stop                                                      
            endif                                                        
c                                                                        
            x11 = xgk(idx  ,idy  )                                       
            x21 = xgk(idx+1,idy  )                                       
            x12 = xgk(idx  ,idy+1)                                       
            x22 = xgk(idx+1,idy+1)                                       
c                                                                        
            y11 = ygk(idx  ,idy  )                                       
            y21 = ygk(idx+1,idy  )                                       
            y12 = ygk(idx  ,idy+1)                                       
            y22 = ygk(idx+1,idy+1)                                       
c                                                                        
            f11 = fxy(idx  ,idy  )                                       
            f21 = fxy(idx+1,idy  )                                       
            f12 = fxy(idx  ,idy+1)                                       
            f22 = fxy(idx+1,idy+1)                                       
c                                                                        
c           Normalize x,y of polar grid point                            
            xnorm = (xtem-x11)/(x21-x11)                                 
            ynorm = (ytem-y11)/(y12-y11)                                 
c                                                                        
            a = f11                                                      
            b = f21 - f11                                                
            c = f12 - f11                                                
            d = f11 + f22 - (f21 + f12)                                  
c                                                                        
            fra(i,j) = a + b*xnorm + c*ynorm + d*xnorm*ynorm             
         endif                                                           
   10 continue                                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine aavg(fxy,radinn,radout,minpts,ifatal,ierr,fxybar)       
c     This routine horizontally averages fxy over an annular             
c     region with r between radinn and radout.  The center of the circle 
c     is determined by the last call to routine xyracal.                 
c     minpts is the minimum number of points allowed in the              
c     circular area. If ifatal=1, execution stops if there is            
c     not enough points for the calculation. If ifatal=0, execution      
c     continues, but ierr is set to 1 if there are not enough points.    
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
      dimension fxy(ixmx,iymx)                                           
c                                                                        
      fxybar= 0.0                                                        
      nbar  = 0                                                          
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
         if (rgk(i,j) .le. radout .and. rgk(i,j) .ge. radinn) then       
            fxybar = fxybar + fxy(i,j)                                   
            nbar = nbar + 1                                              
         endif                                                           
   10 continue                                                           
c                                                                        
      if (nbar .lt. minpts) then                                         
         write(lulog,900) nbar,minpts                                    
  900    format(/,' Not enough data points for aavg calculation.',       
     +            ' nbar,minpts: ',i4,1x,i4)                             
         if (ifatal .eq. 1) then                                         
            stop                                                         
         else                                                            
            ierr=1                                                       
            return                                                       
         endif                                                           
      endif                                                              
c                                                                        
      fxybar = fxybar/float(nbar)                                        
      ierr=0                                                             
c                                                                        
      return                                                             
      END                                                                
      subroutine havg(fxy,radtem,minpts,ifatal,ierr,fxybar)              
c     This routine horizontally averages fxy over a circular             
c     region with radius radtem.  The center of the circle               
c     is determined by the last call to routine xyracal.                 
c     minpts is the minimum number of points allowed in the              
c     circular area. If ifatal=1, execution stops if there is            
c     not enough points for the calculation. If ifatal=0, execution      
c     continues, but ierr is set to 1 if there are not enough points.    
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
      dimension fxy(ixmx,iymx)                                           
c                                                                        
      fxybar= 0.0                                                        
      nbar  = 0                                                          
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
         if (rgk(i,j) .le. radtem) then                                  
            fxybar = fxybar + fxy(i,j)                                   
            nbar = nbar + 1                                              
         endif                                                           
   10 continue                                                           
c                                                                        
      if (nbar .lt. minpts) then                                         
         write(lulog,900) nbar,minpts                                    
  900    format(/,' Not enough data points for havg calculation.',       
     +            ' nbar,minpts: ',i4,1x,i4)                             
         if (ifatal .eq. 1) then                                         
            stop                                                         
         else                                                            
            ierr=1                                                       
            return                                                       
         endif                                                           
      endif                                                              
c                                                                        
      fxybar = fxybar/float(nbar)                                        
      ierr=0                                                             
c                                                                        
      return                                                             
      END                                                                
      subroutine hcavg(fxy,xtem,ytem,minpts,ifatal,ierr,fxybar)          
c     This routine horizontally averages fxy over a rectangular          
c     region from -xtem,ytem to +xtem,ytem.  The center of the rectangle 
c     is determined by the last call to routine xyracal.                 
c     minpts is the minimum number of points allowed in the              
c     rectangular area. If ifatal=1, execution stops if there is         
c     not enough points for the calculation. If ifatal=0, execution      
c     continues, but ierr is set to 1 if there are not enough points.    
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
      dimension fxy(ixmx,iymx)                                           
c                                                                        
      fxybar= 0.0                                                        
      nbar  = 0                                                          
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
         if (xgk(i,j) .le. xtem .and. xgk(i,j) .ge. -xtem .and.          
     +       ygk(i,j) .le. ytem .and. ygk(i,j) .ge. -ytem ) then         
            fxybar = fxybar + fxy(i,j)                                   
            nbar = nbar + 1                                              
         endif                                                           
   10 continue                                                           
c                                                                        
      if (nbar .lt. minpts) then                                         
         write(lulog,900) nbar,minpts                                    
  900    format(/,' Not enough data points for hcavg calculation.',      
     +            ' nbar,minpts: ',i4,1x,i4)                             
         if (ifatal .eq. 1) then                                         
            stop                                                         
         else                                                            
            ierr=1                                                       
            return                                                       
         endif                                                           
      endif                                                              
c                                                                        
      fxybar = fxybar/float(nbar)                                        
      ierr=0                                                             
c                                                                        
      return                                                             
      END                                                                
      subroutine azavg(fra,fr,iorz)                                      
c     This routine azimuthally averages fra on the polar grid.           
c     If iorz=0 then fr is set to zero at the origin.                    
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
      dimension fra(irmx,iamx),fr(irmx)                                  
c                                                                        
      do 10 i=1,nrad                                                     
         jcount = 0                                                      
         ftemp  = 0.0                                                    
         do 20 j=1,ntheta                                                
            if (pmask(i,j) .gt. 0.5) then                                
               ftemp = ftemp + fra(i,j)                                  
               jcount = jcount + 1                                       
            endif                                                        
   20    continue                                                        
         if (jcount .gt. 0) then                                         
            fr(i) = ftemp/float(jcount)                                  
         else                                                            
            fr(i) = 0.0                                                  
         endif                                                           
   10 continue                                                           
c                                                                        
      if (iorz .eq. 0) fr(1)=0.0                                         
c                                                                        
      return                                                             
      END                                                                
      subroutine patoc(fr,fxy)                                           
c     This routine linearly interpolates the azimuthally averaged        
c     function fr on the polar grid to fxy on the Cartesian grid.        
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
      dimension fr(irmx),fxy(ixmx,iymx)                                  
c                                                                        
      do 10 j=1,ny                                                       
      do 10 i=1,nx                                                       
         radtem = rgk(i,j)                                               
c                                                                        
c        Find index of radial point closest to, but                      
c        less than current Cartesian grid point                          
         idr = 1 + ifix(radtem/drad)                                     
c                                                                        
c        Scale the radial distance                                       
         rnorm = (radtem-radk(idr))/drad                                 
c                                                                        
c        Perform linear interpolation                                    
         fxy(i,j) = fr(idr) + (fr(idr+1)-fr(idr))*rnorm                  
   10 continue                                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine ddrcal(fr,dfdr)                                         
c     This routine calculates the radial derivative of fr                
c     using centered derivatives.                                        
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
      dimension fr(irmx),dfdr(irmx)                                      
c                                                                        
c     ********************                                               
c                                                                        
      drm  = 1000.0*drad                                                 
      drm2 = 2.0*drm                                                     
c                                                                        
c     Interior points                                                    
      do 10 i=3,nrad-1                                                   
         dfdr(i) = (fr(i+1)-fr(i-1))/drm2                                
   10 continue                                                           
c                                                                        
c     End points                                                         
      dfdr(1)    = 0.0                                                   
      dfdr(2)    = (fr(   3)-fr(     2))/drm                             
      dfdr(nrad) = (fr(nrad)-fr(nrad-1))/drm                             
c                                                                        
      return                                                             
      END                                                                
      subroutine vsound(rlon,rlat,sradk)                                 
c     This routine horizontally averages variables at                    
c     specified pressure levels and puts the results pressure            
c     arrays. The average is over a circular area of radius sradk        
c     (km) centered at rlon,rlat.                                        
c                                                                        
c     If a variable is not available on the data input                   
c     file, the value is set to 999.9                                    
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,plevh                                                       
      parameter (nplevh=10)                                              
      common /plevhs/ up,vp,zp,tp,rp,tbarp,plevh                         
      dimension up(nplevh),vp(nplevh),zp(nplevh)                         
      dimension tp(nplevh),rp(nplevh)                                    
      dimension tbarp(nplevh)                                            
      dimension plevh(nplevh)                                            
C.DUP lsdiag,plevhd                                                      
      data plevh /1000.0, 850.0, 700.0, 500.0, 400.0,                    
     +             300.0, 250.0, 200.0, 150.0, 100.0/                    
      data tbarp /287.43,278.68,268.57,251.92,241.44,                    
     +            228.58,220.79,216.65,216.65,216.65/                    
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
      dimension fxy(ixmx,iymx)                                           
c                                                                        
c     Specify minimum number of points for the horizontal average        
      minpts=1                                                           
c                                                                        
c     Set itsub=1 to subtract standard atmosphere temperatures           
c                 from observed temperatures or                          
c         itsub=2 to convert from Kelvin to Celsius.                     
c                                                                        
      itsub=2                                                            
c                                                                        
c     Initialize grid variables                                          
      call xyracal(rlon,rlat)                                            
c                                                                        
c     Start pressure level loop                                          
      do 10 k=1,nplevh                                                   
         ptem  = plevh(k)                                                
c                                                                        
         call varget('U',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1) then                                         
             call havg(fxy,sradk,minpts,1,ierr,fbar)                     
             up(k) = 1.944*fbar                                          
         else                                                            
             up(k) = 999.9                                               
         endif                                                           
c                                                                        
         call varget('V',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1) then                                         
             call havg(fxy,sradk,minpts,1,ierr,fbar)                     
             vp(k) = 1.944*fbar                                          
         else                                                            
             vp(k) = 999.9                                               
         endif                                                           
c                                                                        
         call varget('Z',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1) then                                         
             call havg(fxy,sradk,minpts,1,ierr,fbar)                     
             zp(k) = fbar                                                
         else                                                            
             zp(k) = 999.9                                               
         endif                                                           
c                                                                        
         call varget('T',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1) then                                         
             call havg(fxy,sradk,minpts,1,ierr,fbar)                     
             if (itsub .eq. 1) then                                      
                tp(k) = fbar - tbarp(k)                                  
             elseif (itsub .eq. 2) then                                  
                tp(k) = fbar - 273.15                                    
             else                                                        
                tp(k) = fbar                                             
             endif                                                       
         else                                                            
             tp(k) = 999.9                                               
         endif                                                           
c                                                                        
         call varget('R',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1 .and. ptem .gt. 275.0) then                   
             call havg(fxy,sradk,minpts,1,ierr,fbar)                     
             rp(k) = fbar                                                
         else                                                            
             rp(k) = 999.9                                               
         endif                                                           
   10 continue                                                           
c                                                                        
      write(lulog,300)                                                   
  300 format(/,'    P      U      V      Z      T      RH')              
      do 15 k=1,nplevh                                                   
         write(lulog,302) plevh(k),up(k),vp(k),zp(k),tp(k),rp(k)         
  302    format(1x,6(f6.1,1x))                                           
   15 continue                                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine vcsound(rlon,rlat,xradk,yradk)                          
c     This routine horizontally averages variables at                    
c     specified pressure levels and puts the results pressure            
c     arrays. The average is over a rectangulare area (+/-xradk,+/-yradk)
c     (km) centered at rlon,rlat.                                        
c                                                                        
c     If a variable is not available on the data input                   
c     file, the value is set to 999.9                                    
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,plevh                                                       
      parameter (nplevh=10)                                              
      common /plevhs/ up,vp,zp,tp,rp,tbarp,plevh                         
      dimension up(nplevh),vp(nplevh),zp(nplevh)                         
      dimension tp(nplevh),rp(nplevh)                                    
      dimension tbarp(nplevh)                                            
      dimension plevh(nplevh)                                            
C.DUP lsdiag,unnum                                                       
      common /unitno/ lulog,luinp,luout,lurawd                           
c                                                                        
      dimension fxy(ixmx,iymx)                                           
c                                                                        
c     Specify minimum number of points for the horizontal average        
      minpts=1                                                           
c                                                                        
c     Set itsub=1 to subtract standard atmosphere temperatures           
c                 from observed temperatures or                          
c         itsub=2 to convert from Kelvin to Celsius.                     
c                                                                        
      itsub=2                                                            
c                                                                        
c     Initialize grid variables                                          
      call xyracal(rlon,rlat)                                            
c                                                                        
c     Start pressure level loop                                          
      do 10 k=1,nplevh                                                   
         ptem  = plevh(k)                                                
c                                                                        
         call varget('U',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1) then                                         
             call hcavg(fxy,xradk,yradk,minpts,1,ierr,fbar)              
             up(k) = 1.944*fbar                                          
         else                                                            
             up(k) = 999.9                                               
         endif                                                           
c                                                                        
         call varget('V',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1) then                                         
             call hcavg(fxy,xradk,yradk,minpts,1,ierr,fbar)              
             vp(k) = 1.944*fbar                                          
         else                                                            
             vp(k) = 999.9                                               
         endif                                                           
c                                                                        
         call varget('Z',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1) then                                         
             call hcavg(fxy,xradk,yradk,minpts,1,ierr,fbar)              
             zp(k) = fbar                                                
         else                                                            
             zp(k) = 999.9                                               
         endif                                                           
c                                                                        
         call varget('T',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1) then                                         
             call hcavg(fxy,xradk,yradk,minpts,1,ierr,fbar)              
             if (itsub .eq. 1) then                                      
                tp(k) = fbar - tbarp(k)                                  
             elseif (itsub .eq. 2) then                                  
                tp(k) = fbar - 273.15                                    
             else                                                        
                tp(k) = fbar                                             
             endif                                                       
         else                                                            
             tp(k) = 999.9                                               
         endif                                                           
c                                                                        
         call varget('R',ptem,fxy,0,iexist)                              
         if (iexist .eq. 1 .and. ptem .gt. 275.0) then                   
             call hcavg(fxy,xradk,yradk,minpts,1,ierr,fbar)              
             rp(k) = fbar                                                
         else                                                            
             rp(k) = 999.9                                               
         endif                                                           
   10 continue                                                           
c                                                                        
      write(lulog,300)                                                   
  300 format(/,'    P      U      V      Z      T      RH')              
      do 15 k=1,nplevh                                                   
         write(lulog,302) plevh(k),up(k),vp(k),zp(k),tp(k),rp(k)         
  302    format(1x,6(f6.1,1x))                                           
   15 continue                                                           
c                                                                        
      return                                                             
      END                                                                
      subroutine tadd(iyr,imon,iday,itime,ihra,iyra,imona,idaya,itimea)  
c     This routine calculates the year,month,day,time                    
c     (iyra,imona,idaya,itimea) that are ihra hours after                
c     the input year,month,day,time (iyr,imon,iday,itime).               
c                                                                        
c     ihra can not exceed the number of hours in 9 months.               
c                                                                        
c     If ihra is negative, the year,month,day,time that are abs(ihra)    
c     before the input year,month,day,time are calculated.               
c                                                                        
c     The Julian day utilities jday and jdayi are called                 
c     by this routine.                                                   
c                                                                        
      iyra  = iyr                                                        
      imona = imon                                                       
      idaya = iday                                                       
c                                                                        
      if (ihra .lt. 0) go to 1000                                        
c                                                                        
c     ** Start calculation for positive ihra **                          
c                                                                        
c     Add the hours to the input time                                    
      itimea = itime+ihra                                                
c                                                                        
      if (itimea .lt. 24) return                                         
c                                                                        
c     Calculate the number of extra days in the itimea variable          
c     and subtract them from itimea                                      
      idayex = itimea/24                                                 
      itimea = itimea - idayex*24                                        
c                                                                        
c     Calculate Julian day of input date                                 
c     and add extra days to it                                           
      call jday(imon,iday,iyr,jdate)                                     
      jdate = jdate + idayex                                             
c                                                                        
c     Check to see if year has changed                                   
      call jday(12,31,iyr,jmax)                                          
c                                                                        
      if (jdate .gt. jmax) then                                          
         iyra = iyr+1                                                    
         jdate  = jdate-jmax                                             
      else                                                               
         iyra = iyr                                                      
      endif                                                              
c                                                                        
c     Calculate month and day corresponding to the                       
c     increased jdate                                                    
      call jdayi(jdate,iyra,imona,idaya)                                 
c                                                                        
      return                                                             
c                                                                        
 1000 continue                                                           
c     ** Start calculation for negative ihra **                          
c     Add the hours to the input time                                    
      itimea = itime+ihra                                                
c                                                                        
      if (itimea .ge. 0) return                                          
c                                                                        
c     Calculate adjusted time                                            
      idayex = -1 + itimea/24                                            
      itimea = itimea - idayex*24                                        
      if (itimea .eq. 24) then                                           
	 itimea=0                                                               
	 idayex = idayex + 1                                                    
      endif                                                              
c                                                                        
c     Calculate Julian day of input date                                 
c     and subtract extra days from it                                    
      call jday(imon,iday,iyr,jdate)                                     
      jdate = jdate + idayex                                             
c                                                                        
c     Check to see if year has changed                                   
      if (jdate .lt. 1) then                                             
	 iyra  = iyra-1                                                         
	 jdate = jdate + 365                                                    
	 if (mod(iyr-1,4) .eq. 0) jdate = jdate + 1                             
      endif                                                              
c                                                                        
c     Calculate month and day corresponding to the                       
c     decreased jdate                                                    
      call jdayi(jdate,iyra,imona,idaya)                                 
c                                                                        
      return                                                             
      end                                                                
      subroutine jday(imon,iday,iyear,julday)                            
c     This routine calculates the Julian day (julday) from               
c     the month (imon), day (iday), and year (iyear). The                
c     appropriate correction is made for leap year.                      
c                                                                        
      dimension ndmon(12)                                                
c                                                                        
c     Specify the number of days in each month                           
      ndmon(1)  = 31                                                     
      ndmon(2)  = 28                                                     
      ndmon(3)  = 31                                                     
      ndmon(4)  = 30                                                     
      ndmon(5)  = 31                                                     
      ndmon(6)  = 30                                                     
      ndmon(7)  = 31                                                     
      ndmon(8)  = 31                                                     
      ndmon(9)  = 30                                                     
      ndmon(10) = 31                                                     
      ndmon(11) = 30                                                     
      ndmon(12) = 31                                                     
c                                                                        
c     Correct for leap year                                              
      if (mod(iyear,4) .eq. 0) ndmon(2)=29                               
c                                                                        
c     Check for illegal input                                            
      if (imon .lt. 1 .or. imon .gt. 12) then                            
         julday=-1                                                       
         return                                                          
      endif                                                              
c                                                                        
      if (iday .lt. 1 .or. iday .gt. ndmon(imon)) then                   
         julday=-1                                                       
         return                                                          
      endif                                                              
c                                                                        
c     Calculate the Julian day                                           
      julday = iday                                                      
      if (imon .gt. 1) then                                              
         do 10 i=2,imon                                                  
            julday = julday + ndmon(i-1)                                 
   10    continue                                                        
      endif                                                              
c                                                                        
      return                                                             
      end                                                                
      subroutine jdayi(julday,iyear,imon,iday)                           
c     This routine calculates the month (imon) and day (iday)            
c     from the Julian day (julday) and year (iyear).                     
c     The appropriate correction is made for leap year.                  
c                                                                        
      dimension ndmon(12),nsum(13)                                       
c                                                                        
c     Specify the number of days in each month                           
      ndmon(1)  = 31                                                     
      ndmon(2)  = 28                                                     
      ndmon(3)  = 31                                                     
      ndmon(4)  = 30                                                     
      ndmon(5)  = 31                                                     
      ndmon(6)  = 30                                                     
      ndmon(7)  = 31                                                     
      ndmon(8)  = 31                                                     
      ndmon(9)  = 30                                                     
      ndmon(10) = 31                                                     
      ndmon(11) = 30                                                     
      ndmon(12) = 31                                                     
c                                                                        
c     Correct for leap year                                              
      if (mod(iyear,4) .eq. 0) ndmon(2)=29                               
c                                                                        
c     Check for illegal input                                            
      if (mod(iyear,4) .eq. 0) then                                      
         mxjul = 366                                                     
      else                                                               
         mxjul = 365                                                     
      endif                                                              
c                                                                        
      if (julday .lt. 1 .or. julday .gt. mxjul) then                     
         imon = -1                                                       
         iday = -1                                                       
         return                                                          
      endif                                                              
c                                                                        
c     Calculate the month and day                                        
      nsum(1) = 0                                                        
      do 10 i=1,12                                                       
         nsum(i+1) = nsum(i) + ndmon(i)                                  
   10 continue                                                           
c                                                                        
      do 20 i=2,13                                                       
         if (julday .le. nsum(i)) then                                   
            imon = i-1                                                   
            go to 1000                                                   
         endif                                                           
   20 continue                                                           
 1000 continue                                                           
c                                                                        
      iday = julday - nsum(imon)                                         
c                                                                        
      return                                                             
      end                                                                
      subroutine fcopy(fxy,fxyc)                                         
c     This routine copies the 2-D array fxy to fxyc                      
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c                                                                        
      dimension fxy(ixmx,iymx),fxyc(ixmx,iymx)                           
c                                                                        
      do j=1,ny                                                          
      do i=1,nx                                                          
         fxyc(i,j) = fxy(i,j)                                            
      enddo                                                              
      enddo                                                              
c                                                                        
      return                                                             
      end                                                                
                                                                         
c     ** cfindxy code marker (Start) **                                  
c                                                                        
c     This group of routines is for finding the circulation center       
c     and removing the storm influence from various fields.              
c                                                                        
c     Routines include                                                   
c       lfilter                                                          
c       cfindxy                                                          
c       lltxycf                                                          
c       xytllcf                                                          
c       lintcf                                                           
c       azavgcf                                                          
c       rdavgcf                                                          
c       rdavgcf                                                          
c       vremove                                                          
c       ctor                                                             
c       rtoc                                                             
c                                                                        
      subroutine lfilter(fxy,sxc,syc,frad)                               
c     This routine applies a Laplacian filter to all points within       
c     a distance frad (km) to the point sxc, syc                         
c                                                                        
c     ++ common start in lsplot code ++                                  
c     common /xyrai/ nx,ny                                               
c     common /xyrar/ xgk,ygk                                             
c                                                                        
c     parameter (ixmx=26,iymx=21)                                        
c     dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
c     ++ common end in lsplot code ++                                    
c                                                                        
c     ++ common start in lsdiag code ++                                  
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c     ++ common end in lsdiag code ++                                    
c                                                                        
      dimension fxy(ixmx,iymx)                                           
      dimension mask(ixmx,iymx)                                          
c                                                                        
      do j=1,ny                                                          
      do i=1,nx                                                          
         mask(i,j) = 0                                                   
      enddo                                                              
      enddo                                                              
c                                                                        
c     Find maximum search indices                                        
      dx = xgk(2,1)-xgk(1,1)                                             
      dy = ygk(1,2)-ygk(1,1)                                             
      kx = 1 + ifix(frad/dx)                                             
      ky = 1 + ifix(frad/dx)                                             
c                                                                        
      kxo = 1 + ifix( 0.5 + (sxc-xgk(1,1))/dx )                          
      kyo = 1 + ifix( 0.5 + (syc-ygk(1,1))/dy )                          
c                                                                        
      i1 = kxo - kx                                                      
      i2 = kxo + kx                                                      
c                                                                        
      j1 = kyo - ky                                                      
      j2 = kyo + ky                                                      
c                                                                        
      if (i1 .lt.    2) i1 = 2                                           
      if (i2 .gt. nx-1) i2 = nx-1                                        
c                                                                        
      if (j1 .lt.    2) j1 = 2                                           
      if (j2 .gt. ny-1) j2 = ny-1                                        
c                                                                        
      do j=j1,j2                                                         
      do i=i1,i2                                                         
         rad = sqrt( (xgk(i,j)-sxc)**2 + (ygk(i,j)-syc)**2 )             
         if (rad .le. frad) mask(i,j) = 1                                
      enddo                                                              
      enddo                                                              
c                                                                        
c     do j=ny,1,-1                                                       
c        write(6,800) (mask(i,j),i=1,nx)                                 
c 800    format(26(i2))                                                  
c     enddo                                                              
c                                                                        
c     Perform relaxation for Laplacian filter solution                   
      nit=20                                                             
c                                                                        
      r2 = (dy/dx)**2                                                    
c                                                                        
      yfac = 0.5/(r2+1.0)                                                
      xfac = r2*yfac                                                     
c                                                                        
      do 99 n=1,nit                                                      
         do j=j1,j2                                                      
         do i=i1,i2                                                      
            if (mask(i,j) .eq. 1) then                                   
               fxy(i,j) = xfac*(fxy(i+1,j)+fxy(i-1,j)) +                 
     +                    yfac*(fxy(i,j+1)+fxy(i,j-1))                   
            endif                                                        
         enddo                                                           
         enddo                                                           
   99 continue                                                           
c                                                                        
      return                                                             
      end                                                                
      subroutine cfindxy(uxy,vxy,rcf,thetacf,                            
     +                   mrcf,mtcf,nrcf,ntcf,                            
     +                   radtwa,x0,y0,xcen,ycen,twa,rwa)                 
c                                                                        
c     This routine finds the coordinates of the center location          
c     (xcen,ycen) in km that maximizes the mean tangential wind averaged 
c     from 0 to radtwm (km), given the first guess coordinates (x0,y0)   
c     and the horizontal wind components uxy,vxy. The average tangential 
c     wind relative to the center location (twa) is also calculated.     
c                                                                        
c     Input:   uxy,vxy - horizontal wind components as a function of x,y 
c              rcf(0:mrcf) - radius array for storm-rel coord's          
c              thetacf(0:mtcf) - azimuth array for storm-rel coord's     
c              mrcf,mtcf - max dimensions of r,theta arrays              
c              nrcf,ntcf - working dimensions of r,theta arrays          
c              radtwa    - Maximum radius for radially averaged          
c                          tangential wind (km)                          
c              x0,y0     - first guess coordinates of center             
c                                                                        
c    Output:   xcen,ycen - coordinates of storm center (km)              
c              twa,rwa   - azimutally and radially averaged tangential   
c                          and radial winds relative to (xcen,ycen)      
c                                                                        
c    Note:     The x,y coordinates of uxy,vxy are passed through common  
c                                                                        
c     ++ common start in lsplot code ++                                  
c     common /xyrai/ nx,ny                                               
c     common /xyrar/ xgk,ygk                                             
c                                                                        
c     parameter (ixmx=26,iymx=21)                                        
c     dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
c     ++ common end in lsplot code ++                                    
c                                                                        
c     ++ common start in lsdiag code ++                                  
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c     ++ common end in lsdiag code ++                                    
c                                                                        
c     ++ Passed variables                                                
      dimension uxy(ixmx,iymx),vxy(ixmx,iymx)                            
      dimension rcf(0:mrcf),thetacf(0:mtcf)                              
c                                                                        
c     ++ Temporary cylindrical grid variables                            
      parameter (irxcf=100,itxcf=32)                                     
      dimension  xrt(0:irxcf,0:itxcf), yrt(0:irxcf,0:itxcf)              
      dimension ucrt(0:irxcf,0:itxcf),vcrt(0:irxcf,0:itxcf)              
      dimension urrt(0:irxcf,0:itxcf),vtrt(0:irxcf,0:itxcf)              
      dimension urr(0:irxcf),vtr(0:irxcf)                                
      dimension stheta(0:itxcf),ctheta(0:itxcf)                          
c                                                                        
c     Specify number of interations                                      
      niter=8                                                            
c                                                                        
c     Specify initial dx,dy (km) for the search                          
      dxy = 100.0                                                        
c                                                                        
c     Specify the fraction to reduce dx,dy after each iteration          
      dxyrf = 0.6                                                        
c                                                                        
c     Specify the number of points on either side of the first guess lat/
c     for the search                                                     
      nsearch = 2                                                        
c                                                                        
c     Calculate needed geometric info                                    
      dtr = 3.14159/180.0                                                
      dx  = xgk(2,1)-xgk(1,1)                                            
      dy  = ygk(1,2)-ygk(1,1)                                            
      x1  = xgk(1,1)                                                     
      y1  = ygk(1,1)                                                     
c                                                                        
      do j=0,ntcf                                                        
         stheta(j) = sin(dtr*thetacf(j))                                 
         ctheta(j) = cos(dtr*thetacf(j))                                 
      enddo                                                              
c                                                                        
c     First guess center                                                 
      xcen = x0                                                          
      ycen = y0                                                          
      xcent= x0                                                          
      ycent= y0                                                          
      twa  = -1.0e10                                                     
c                                                                        
c     ++ Start iteration                                                 
      do 99 n=1,niter                                                    
c                                                                        
         do jj=-nsearch,nsearch                                          
         do ii=-nsearch,nsearch                                          
c                                                                        
c           Calculate x,y coordinates of center-relative r,theta grid poi
c                                                                        
            xcenij = xcen + dxy*float(ii)                                
            ycenij = ycen + dxy*float(jj)                                
c                                                                        
            do j=0,ntcf                                                  
            do i=0,nrcf                                                  
               xrt(i,j) = xcenij + rcf(i)*ctheta(j)                      
               yrt(i,j) = ycenij + rcf(i)*stheta(j)                      
            enddo                                                        
            enddo                                                        
c                                                                        
c           Interpolate u,v from x,y to r,t                              
            do j=0,ntcf                                                  
            do i=0,nrcf                                                  
               call lintcf(uxy,x1,dx,y1,dy,ixmx,iymx,nx,ny,              
     +                     xrt(i,j),yrt(i,j),ucrt(i,j))                  
               call lintcf(vxy,x1,dx,y1,dy,ixmx,iymx,nx,ny,              
     +                     xrt(i,j),yrt(i,j),vcrt(i,j))                  
            enddo                                                        
            enddo                                                        
c                                                                        
c           Convert Cartesian u,v to radial and tangential winds         
            do j=0,ntcf                                                  
            do i=0,nrcf                                                  
               urrt(i,j) = ucrt(i,j)*ctheta(j) + vcrt(i,j)*stheta(j)     
               vtrt(i,j) = vcrt(i,j)*ctheta(j) - ucrt(i,j)*stheta(j)     
            enddo                                                        
            enddo                                                        
c                                                                        
c           ++ Debug code                                                
c           if (ii .eq. 0 .and. jj .eq. 0) then                          
c              do jk=10,6,-1                                             
c                 if (jk .eq. 10) write(6,849) (ik,ik=8,12)              
c 849             format(/,'uxy',/,4x,20(1x,i4,1x))                      
c                                                                        
c                 write(6,850) jk,(uxy(ik,jk),ik=8,12)                   
c 850             format(1x,i2,1x,20(f5.1,1x))                           
c              enddo                                                     
c                                                                        
c              do jk=10,6,-1                                             
c                 if (jk .eq. 10) write(6,851) (ik,ik=8,12)              
c 851             format(/,'vxy',/,4x,20(1x,i4,1x))                      
c                                                                        
c                 write(6,850) jk,(vxy(ik,jk),ik=8,12)                   
c              enddo                                                     
c                                                                        
c              do jk=0,ntcf                                              
c                 if (jk .eq. 0) write(6,852) (ik,ik=0,10)               
c 852             format(/,'ucrt',/,4x,20(1x,i4,1x))                     
c                                                                        
c                 write(6,850) jk,(ucrt(ik,jk),ik=0,10)                  
c              enddo                                                     
c                                                                        
c              do jk=0,ntcf                                              
c                 if (jk .eq. 0) write(6,853) (ik,ik=0,10)               
c 853             format(/,'vcrt',/,4x,20(1x,i4,1x))                     
c                                                                        
c                 write(6,850) jk,(vcrt(ik,jk),ik=0,10)                  
c              enddo                                                     
c           endif                                                        
c                                                                        
c           Azimuthally average ur,vt                                    
            call azavgcf(urrt,urr,mrcf,mtcf,nrcf,ntcf)                   
            call azavgcf(vtrt,vtr,mrcf,mtcf,nrcf,ntcf)                   
c                                                                        
c           do k=0,nrcf                                                  
c              write(6,704) rcf(k),urr(k),vtr(k)                         
c 704          format('r,ur,vt: ',3(f6.1,1x))                            
c           enddo                                                        
c                                                                        
c           Radially average ur,vt                                       
            call rdavgcf(urr,rcf,radtwa,ubar,mrcf,nrcf)                  
            call rdavgcf(vtr,rcf,radtwa,vbar,mrcf,nrcf)                  
c                                                                        
            if (vbar .gt. twa) then                                      
               xcent = xcenij                                            
               ycent = ycenij                                            
               twa   = vbar                                              
               rwa   = ubar                                              
            endif                                                        
         enddo                                                           
         enddo                                                           
c                                                                        
         xcen = xcent                                                    
         ycen = ycent                                                    
c                                                                        
c        write(6,605) n,dxy,xcen,ycen,twa,rwa                            
c 605    format('n,dxy: ',i2,1x,f6.2,' xc,yc: ',f6.1,1x,f6.1,            
c    +          ' twa,ura: ',f6.2,1x,f6.2)                               
c                                                                        
         dxy = dxy*dxyrf                                                 
c                                                                        
   99 continue                                                           
c                                                                        
c      do k=0,nrcf                                                       
c         write(6,704) rcf(k),urr(k),vtr(k)                              
c 704     format('r,ur,vt: ',3(f6.1,1x))                                 
c     enddo                                                              
c                                                                        
      return                                                             
      end                                                                
      subroutine lltxycf(olat,olon,colat,dtk,rlat,rlon,x,y)              
c     This routine calculates the x,y coordinates of the                 
c     point (rlon,rlat) where the origin is at olon,olat and             
c     colat=cos(olat). All lat/lons are in deg N/E and x,y               
c     are in km, and dtk is the deg lat to km conversion factor.         
c     All parameters except x,y are input parameters.                    
c                                                                        
      x = dtk*(rlon-olon)*colat                                          
      y = dtk*(rlat-olat)                                                
c                                                                        
      return                                                             
      end                                                                
      subroutine xytllcf(olat,olon,colat,dtk,x,y,rlat,rlon)              
c     This routine calculates the lat,lon coordinates of the             
c     point (x,y) where the origin is at olon,olat and                   
c     colat=cos(olat). All lat/lons are in deg N/E and x,y               
c     are in km, and dtk is the deg lat to km conversion factor.         
c     All parameters except rlat,rlon are input parameters.              
c                                                                        
      rlon = olon + x/(dtk*colat)                                        
      rlat = olat + y/(dtk      )                                        
c                                                                        
      return                                                             
      end                                                                
      subroutine lintcf(fxy,x1,dx,y1,dy,mx,my,nx,ny,xi,yi,fxyii)         
c     This routine bi-linearly interpolates fxy to the point             
c     (xi,yi) to give fxyii.                                             
c                                                                        
c     Input:   fxy(mx,my) - array to be interpolated                     
c              dx,dy      - spacing of evenly spaced x,y points          
c              x1,y1      - x,y coorindates of lower-left point          
c              mx,my      - max dimensions of fxy                        
c              nx,ny      - working dimensions of fxy                    
c              xi,yi      - coordinates of point to be interpolated      
c                                                                        
c     Output:  fxyii      - value of interpolated function at (xi,yi)    
c                                                                        
      dimension fxy(mx,my)                                               
c                                                                        
c     Find the indices of the lower-left point of the c                  
c     grid box containing the point (xi,yi)                              
      i0 = 1 + ifix( (xi-x1)/dx )                                        
      j0 = 1 + ifix( (yi-y1)/dy )                                        
c                                                                        
c     Check index bounds                                                 
      if (i0 .lt.    1) i0=   1                                          
      if (i0 .gt. nx-1) i0=nx-1                                          
      if (j0 .lt.    1) j0=   1                                          
      if (j0 .gt. ny-1) j0=ny-1                                          
c                                                                        
      i1 = i0+1                                                          
      j1 = j0+1                                                          
c                                                                        
c     Calculate normalized x,y distances                                 
      xn = ( (xi-x1) - dx*float(i0-1) )/dx                               
      yn = ( (yi-y1) - dy*float(j0-1) )/dx                               
c                                                                        
      if (xn .lt. 0.0) xn = 0.0                                          
      if (xn .gt. 1.0) xn = 1.0                                          
      if (yn .lt. 0.0) yn = 0.0                                          
      if (yn .gt. 1.0) yn = 1.0                                          
c                                                                        
c     Calculate coefficients for interpolation function                  
      f00 = fxy(i0,j0)                                                   
      f10 = fxy(i1,j0)                                                   
      f01 = fxy(i0,j1)                                                   
      f11 = fxy(i1,j1)                                                   
c                                                                        
      a = f00                                                            
      b = f10-f00                                                        
      c = f01-f00                                                        
      d = f00+f11-f10-f01                                                
c                                                                        
      fxyii = a + b*xn + c*yn + d*xn*yn                                  
c                                                                        
      return                                                             
      end                                                                
      subroutine azavgcf(frt,fr,mr,mt,nr,nt)                             
c     This routine performs and azimuthal average of frt to give ft      
      dimension frt(0:mr,0:mt),fr(0:mr)                                  
c                                                                        
      cf = 1.0/float(nt+1)                                               
c                                                                        
      do i=0,nr                                                          
         fr(i) = frt(i,0)                                                
         do j=1,nt                                                       
            fr(i) = fr(i) + frt(i,j)                                     
         enddo                                                           
c                                                                        
         fr(i) = cf*fr(i)                                                
      enddo                                                              
c                                                                        
      return                                                             
      end                                                                
      subroutine rdavgcf(fr,rr,radmax,fbar,mr,nr)                        
c     This routine radially averages fr from r=0 to r=radmax             
c                                                                        
      dimension fr(0:mr),rr(0:mr)                                        
c                                                                        
      count = 0.0                                                        
      fbar  = 0.0                                                        
      do i=0,nr                                                          
         if (rr(i) .gt. radmax) go to 1000                               
         count = count + 1.0                                             
         fbar  = fbar  + fr(i)                                           
      enddo                                                              
c                                                                        
 1000 continue                                                           
c                                                                        
      if (count .ge. 1.0) then                                           
         fbar = fbar/count                                               
      else                                                               
         fbar = 0.0                                                      
      endif                                                              
c                                                                        
      return                                                             
      end                                                                
      subroutine vremove(uxy,vxy,rcf,thetacf,xcen,ycen,                  
     +                   mrcf,mtcf,nrcf,ntcf,uraa,vtaa,irflag)           
c                                                                        
c     This routine calculates the azimuthally averaged radial            
c     and tangential winds (uraa and vtaa) relative to the point         
c     (xcen,ycen) from the Cartesian wind components uxy,vxy.            
c                                                                        
c     If irflag=1, then the symmetric winds are removed from uxy,vxy     
c     in regions of cyclonic rotation.                                   
c                                                                        
c     ++ common start in lsplot code ++                                  
c     common /xyrai/ nx,ny                                               
c     common /xyrar/ xgk,ygk                                             
c                                                                        
c     parameter (ixmx=26,iymx=21)                                        
c     dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
c     ++ common end in lsplot code ++                                    
c                                                                        
c     ++ common start in lsdiag code ++                                  
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,xyra                                                        
      common /xyra/ xgk,ygk,rgk,agk,xmin,xmax,ymin,ymax,                 
     +              olons,olats,colat                                    
      dimension xgk(ixmx,iymx),ygk(ixmx,iymx)                            
      dimension rgk(ixmx,iymx),agd(ixmx,iymx)                            
      common /ixyra/ nx,ny                                               
      common /raxy/ radk,thetad,xra,yra,pmask,drad,dtheta                
      dimension radk(irmx),thetad(iamx)                                  
      dimension xra(irmx,iamx),yra(irmx,iamx)                            
      dimension pmask(irmx,iamx)                                         
      common /iraxy/ nrad,ntheta                                         
c     ++ common end in lsdiag code ++                                    
c                                                                        
c     ++ Passed variables                                                
      dimension uxy(ixmx,iymx),vxy(ixmx,iymx)                            
      dimension rcf(0:mrcf),thetacf(0:mtcf)                              
      dimension uraa(0:mrcf),vtaa(0:mrcf)                                
c                                                                        
c     ++ Temporary cylindrical grid variables                            
      parameter (irxcf=100,itxcf=32)                                     
      dimension  xrt(0:irxcf,0:itxcf), yrt(0:irxcf,0:itxcf)              
      dimension ucrt(0:irxcf,0:itxcf),vcrt(0:irxcf,0:itxcf)              
      dimension urrt(0:irxcf,0:itxcf),vtrt(0:irxcf,0:itxcf)              
      dimension urr(0:irxcf),vtr(0:irxcf)                                
      dimension stheta(0:itxcf),ctheta(0:itxcf)                          
c                                                                        
c     Specify minimum radius (km) for vortex removal                     
      rminvr = 301.0                                                     
c                                                                        
c     Calculate needed geometric info                                    
      dtr = 3.14159/180.0                                                
      dx  = xgk(2,1)-xgk(1,1)                                            
      dy  = ygk(1,2)-ygk(1,1)                                            
      x1  = xgk(1,1)                                                     
      y1  = ygk(1,1)                                                     
      dr  = rcf(2)-rcf(1)                                                
c                                                                        
      do j=0,ntcf                                                        
         stheta(j) = sin(dtr*thetacf(j))                                 
         ctheta(j) = cos(dtr*thetacf(j))                                 
      enddo                                                              
c                                                                        
c     ++ Find symmetric average ++                                       
c                                                                        
c     Find x,y coordinates of storm-centered radial grid points          
      do j=0,ntcf                                                        
      do i=0,nrcf                                                        
         xrt(i,j) = xcen + rcf(i)*ctheta(j)                              
         yrt(i,j) = ycen + rcf(i)*stheta(j)                              
      enddo                                                              
      enddo                                                              
c                                                                        
c     Interpolate u,v from x,y to r,t                                    
      do j=0,ntcf                                                        
      do i=0,nrcf                                                        
         call lintcf(uxy,x1,dx,y1,dy,ixmx,iymx,nx,ny,                    
     +               xrt(i,j),yrt(i,j),ucrt(i,j))                        
         call lintcf(vxy,x1,dx,y1,dy,ixmx,iymx,nx,ny,                    
     +               xrt(i,j),yrt(i,j),vcrt(i,j))                        
      enddo                                                              
      enddo                                                              
c                                                                        
c     Convert Cartesian u,v to radial and tangential winds               
      do j=0,ntcf                                                        
      do i=0,nrcf                                                        
         urrt(i,j) = ucrt(i,j)*ctheta(j) + vcrt(i,j)*stheta(j)           
         vtrt(i,j) = vcrt(i,j)*ctheta(j) - ucrt(i,j)*stheta(j)           
      enddo                                                              
      enddo                                                              
c                                                                        
c     Azimuthally average ur,vt                                          
      call azavgcf(urrt,urr,mrcf,mtcf,nrcf,ntcf)                         
      call azavgcf(vtrt,vtr,mrcf,mtcf,nrcf,ntcf)                         
c                                                                        
      uraa(0) = 0.0                                                      
      vtaa(0) = 0.0                                                      
      do k=1,nrcf                                                        
         uraa(k) = urr(k)                                                
         vtaa(k) = vtr(k)                                                
      enddo                                                              
c                                                                        
      if (irflag .ne. 1) return                                          
c                                                                        
c     ++ Vortex removal ++                                               
c                                                                        
c     Find the first radius beyond minimum where tangential wind         
c     becomes negative                                                   
      kstart = ifix(rminvr/dr)                                           
      kend   = nrcf                                                      
c                                                                        
      do k=kstart+1,nrcf                                                 
         if (vtr(k) .lt. 0.0) then                                       
c           write(6,*) 'k,vtr(k)',k,vtr(k)                               
            kend = k-1                                                   
            go to 1000                                                   
         endif                                                           
      enddo                                                              
 1000 continue                                                           
c                                                                        
      rend = rcf(kend)                                                   
      vend = vtr(kend)                                                   
      uend = urr(kend)                                                   
c                                                                        
      if (kend .lt. nrcf) then                                           
c        Set symmetric wind outside rend to zero                         
         do k=kend+1,nrcf                                                
            vtr(k) = 0.0                                                 
            urr(k) = 0.0                                                 
         enddo                                                           
      endif                                                              
c                                                                        
      if (abs(vend) .gt. 1.0 .or. abs(uend) .gt. 1.0) then               
c        Taper the last three points of symmetric circulation            
         vtr(kend  ) = 0.1*vtr(kend  )                                   
         urr(kend  ) = 0.1*urr(kend  )                                   
c                                                                        
         vtr(kend-1) = 0.4*vtr(kend-1)                                   
         urr(kend-1) = 0.4*urr(kend-1)                                   
c                                                                        
         vtr(kend-2) = 0.7*vtr(kend-2)                                   
         urr(kend-2) = 0.7*urr(kend-2)                                   
      endif                                                              
c                                                                        
c     do k=0,nrcf                                                        
c        write(61,800) rcf(k),uraa(k),urr(k),vtaa(k),vtr(k)              
c 800    format(5(f6.1,1x))                                              
c     enddo                                                              
c                                                                        
c     Determine maximum range of x,y points for vortex removal           
      xp = xcen + rend                                                   
      xm = xcen - rend                                                   
      yp = ycen + rend                                                   
      ym = ycen - rend                                                   
c                                                                        
      im = 1 + ifix( (xm-x1)/dx )                                        
      ip = 2 + ifix( (xp-x1)/dx )                                        
      jm = 1 + ifix( (ym-y1)/dy )                                        
      jp = 2 + ifix( (yp-y1)/dy )                                        
c                                                                        
      if (im .lt.  1) im =  1                                            
      if (ip .gt. nx) ip = nx                                            
      if (jm .lt.  1) jm =  1                                            
      if (jp .gt. ny) jp = ny                                            
c                                                                        
c     Set ipert=1 to put vortex only into uxy,vxy instead of subtracting 
      ipert=0                                                            
      if (ipert .eq. 1) then                                             
         do j=1,ny                                                       
         do i=1,nx                                                       
            uxy(i,j) = 0.0                                               
            vxy(i,j) = 0.0                                               
         enddo                                                           
         enddo                                                           
      endif                                                              
c                                                                        
c     Loop through all x,y points that may need vortex removal           
      do j=jm,jp                                                         
      do i=im,ip                                                         
c                                                                        
c        Calculate storm-relative r,theta for this x,y point             
         xrel = xgk(i,j)-xcen                                            
         yrel = ygk(i,j)-ycen                                            
c                                                                        
         call ctor(xrel,yrel,rrel,thetarel)                              
         if (rrel .gt. rend) go to 2000                                  
c                                                                        
c        Linearly interpolate vortex radial and tangetial wind           
c        to model x,y grid point                                         
         i1 = ifix(rrel/dr)                                              
         if (i1 .ge. nrcf-1) i1=nrcf-1                                   
         i2 = i1+1                                                       
         rnorm = (rrel - dr*float(i1))/dr                                
         w1 = (1-rnorm)                                                  
         w2 = rnorm                                                      
c                                                                        
         urel = w1*urr(i1) + w2*urr(i2)                                  
         vrel = w1*vtr(i1) + w2*vtr(i2)                                  
c                                                                        
c        write(6,915) xrel,yrel,rrel,thetarel,rnorm,urel,vrel,           
c    +                vtr(i1),vtr(i2)                                    
c 915    format('x,y,r,t,rnorm,urel,vrel,vt1,vt2: ',10(f7.1,1x))         
c                                                                        
c        Convert urel,vrel to Cartesian coordinates                      
         sinth = sin(dtr*thetarel)                                       
         costh = cos(dtr*thetarel)                                       
         ucrel = urel*costh - vrel*sinth                                 
         vcrel = vrel*costh + urel*sinth                                 
c                                                                        
c        Subtract vortex                                                 
         if (ipert .eq. 1) then                                          
            uxy(i,j) = ucrel                                             
            vxy(i,j) = vcrel                                             
         else                                                            
            uxy(i,j) = uxy(i,j)-ucrel                                    
            vxy(i,j) = vxy(i,j)-vcrel                                    
         endif                                                           
c                                                                        
 2000    continue                                                        
c                                                                        
      enddo                                                              
      enddo                                                              
c                                                                        
      return                                                             
      end                                                                
      subroutine ctor(x,y,r,theta)                                       
c     This routine converts from Cartesion coordinates                   
c     to radial coordinates, where theta is in                           
c     degrees measured counter-clockwise from                            
c     the +x-axis.                                                       
c                                                                        
      r = sqrt(x*x + y*y)                                                
c                                                                        
      if (r .le. 0.0) then                                               
         theta = 0.0                                                     
         return                                                          
      endif                                                              
c                                                                        
      rtd = 57.296                                                       
      theta = rtd*acos(x/r)                                              
      if (y .lt. 0.0) theta = 360.0 - theta                              
c                                                                        
      return                                                             
      end                                                                
      subroutine rtoc(r,theta,x,y)                                       
c     This routine converts from radial coordinates                      
c     to Cartesian coordinates, where theta is in                        
c     degrees measured counter-clockwise from                            
c     the +x-axis.                                                       
c                                                                        
      rtd = 57.296                                                       
      x = r*cos(theta/rtd)                                               
      y = r*sin(theta/rtd)                                               
c                                                                        
      return                                                             
      end                                                                
      subroutine spdlim(rlat,spdmax)                                     
c     This routine estimates the maximum expected translational          
c     speed (kt) of an Atlantic or east Pacific tropical cyclone         
c     at a given latitude.                                               
c                                                                        
      alat = abs(rlat)                                                   
c                                                                        
      if    (alat  .lt. 25.0) then                                       
         spdmax = 30.0                                                   
      elseif (alat .ge. 25.0 .and. alat .lt. 40.0) then                  
         spdmax = 30.0 + (alat-25.0)*2.0                                 
      else                                                               
         spdmax = 60.0                                                   
      endif                                                              
c                                                                        
      return                                                             
      end                                                                
c     ** cfindxy code marker (end) **                                    
c                                                                        
      subroutine rhbc(rh,ptem)                                           
c     This routine applies a bias correction the relative humidity       
c     variable from GFS reanalysis fields to make them comparable        
c     to those from the operational GFS analyses.                        
c                                                                        
c                                                                        
C.DUP lsdiag,primd                                                       
      parameter(ixmx=121,iymx=91,ipmx=21)                                
      parameter(irmx=300,iamx=24)                                        
C.DUP lsdiag,latlon                                                      
       common /latlon/  RLATMN,RLATMX,RLONMN,RLONMX,DLAT,DLON,           
     +                  RLATD,RLOND                                      
       dimension rlatd(iymx),rlond(ixmx)                                 
       common /ilatlon/ NLAT1,NLON1                                      
C.DUP lsdiag,plevh                                                       
      parameter (nplevh=10)                                              
      common /plevhs/ up,vp,zp,tp,rp,tbarp,plevh                         
      dimension up(nplevh),vp(nplevh),zp(nplevh)                         
      dimension tp(nplevh),rp(nplevh)                                    
      dimension tbarp(nplevh)                                            
      dimension plevh(nplevh)                                            
c                                                                        
      dimension rh(ixmx,iymx)                                            
c                                                                        
c     Local variables                                                    
      dimension a0(nplevh),a1(nplevh),a2(nplevh)                         
c                                                                        
c     Coefficients for the RH bias correction functions (quadratic polyno
      data a0 /1.3886,6.0946,1.7537,4.1882,9.1137,13.624,                
     +                                    0.0,0.0,0.0,0.0/               
      data a1 /1.1992,1.5182,1.6303,1.1531,0.9546,0.6662,                
     +                                    1.0,1.0,1.0,1.0/               
      data a2 /-.0037,-.0072,-.0084,-.0045,-.0025,-.0004,                
     +                                    0.0,0.0,0.0,0.0/               
c                                                                        
c     Find the pressure level                                            
      eps = 0.0001                                                       
      do k=1,nplevh                                                      
         if (abs(ptem-plevh(k)) .lt. eps) then                           
            kplev = k                                                    
            go to 1000                                                   
         endif                                                           
      enddo                                                              
c                                                                        
c     Pressure level not found, skip bias correction                     
      return                                                             
c                                                                        
 1000 continue                                                           
c                                                                        
      b0 = a0(kplev)                                                     
      b1 = a1(kplev)                                                     
      b2 = a2(kplev)                                                     
c                                                                        
      do j=1,nlat1                                                       
      do i=1,nlon1                                                       
         rhx = rh(i,j)                                                   
         rh(i,j) = b0 + b1*rhx + b2*rhx*rhx                              
      enddo                                                              
      enddo                                                              
c                                                                        
      return                                                             
      end                                                                
      subroutine splcal(plev,u,v,cx,cy,alpha,ml,
     +                  dw,w,ubard,vbard,pbard,ubar,vbar,pbar)

c     This routine calculates the weights w to determine the vertically
c     averaged horizontal wind that is as close as possible to
c     the storm motion cx,cy. The weights are used to determine the
c     pressure of the steering level.
c
c     Input:
c       plev        - 1-D array containing the pressure levels (mb)
c       u,v         - The enviromental wind at the levels plev
c       cx,cy       - The components of the storm motion vector
c       alpha       - The coefficient for contraining the steering
c                     weights so that they are not "too far" from
c                     the mass weighted average weights
c       ml          - The number of pressure levels
c
c     Output:
c       dw          - The weights for a mass-weighted average
c       w           - The weights for the optimal steering
c       ubard,vbard - The mass-weighted average horizontal wind
c       ubar,vbar   - The optimally weighted horizontal mean
c       pbard       - The mass-weighted pressure
c       pbar        - The optimally weighted pressure
c
      dimension plev(ml),u(ml),v(ml),dw(ml),w(ml)
c
c     Local variables
      parameter (np=12,mp=2)
c
      dimension a(np,np),b(np,mp)
c
c     Set ipen=1 for penalty in terms of (W-M) or 
c         ipen=2 for penalty in terms of (W/M-1)
      ipen=2
c
c     Make sure np is large enough
      if (ml .gt. np) then
         write(6,100)
  100    format(/,' np too small in routine wcal')
         stop
      endif
c
      n=ml-1
c
c     Calculate deep-layer mean weights
      call dlmw(plev,dw,ml)
c
c     Calculate column matrix on the RHS of the linear system for w
      uk = u(ml)
      vk = v(ml)
      dk= dw(ml)
c
      if (ipen .eq. 1) then
         do 10 k=1,n
            b(k,1) = (cx-uk)*(u(k)-uk) + (cy-vk)*(v(k)-vk) +
     +               alpha*(1.0 + dw(k) - dk)
   10    continue
      else
         do 11 k=1,n
            b(k,1) = (cx-uk)*(u(k)-uk) + (cy-vk)*(v(k)-vk) +
     +               alpha*(1.0/(dk*dk) + 1.0/dw(k) - 1.0/dk)
   11    continue
      endif
c
c     Calculate w coefficient matrix
      if (ipen .eq. 1) then
         do 15 j=1,n
         do 15 i=1,n
            if (i .eq. j) then
               ac = 2.0
            else
               ac = 1.0
            endif
c
            a(i,j) = (u(i)-uk)*(u(j)-uk) +
     +               (v(i)-vk)*(v(j)-vk) + ac*alpha
   15    continue
      else
         do 16 j=1,n
         do 16 i=1,n
            if (i .eq. j) then
               ac = (1.0/dk)**2 + (1.0/dw(j))**2
            else
               ac = (1.0/dk)**2
            endif
c
            a(i,j) = (u(i)-uk)*(u(j)-uk) +
     +               (v(i)-vk)*(v(j)-vk) + ac*alpha
   16    continue
      endif
c
c     Calculate optimal weights
      call gaussj(a,n,np,b,1,mp)
c
      do 30 i=1,n
         w(i) = b(i,1)
   30 continue
c
      w(ml) = 1.0
      do 40 i=1,n
         w(ml) = w(ml) - w(i)
   40 continue
c
c     Calculate vertically weighted variables
      ubard = 0.0
      vbard = 0.0
      ubar  = 0.0
      vbar  = 0.0
      pbard = 0.0
      pbar  = 0.0
      do 50 k=1,ml
         ubard = ubard + dw(k)*u(k)
         vbard = vbard + dw(k)*v(k)
         pbard = pbard + dw(k)*plev(k)
         ubar  = ubar  +  w(k)*u(k)
         vbar  = vbar  +  w(k)*v(k)
         pbar  = pbar  +  w(k)*plev(k)
   50 continue
c
      return
      end
      subroutine dlmw(plev,dw,ml)
      dimension plev(ml),dw(ml)
c
      if (ml .eq. 1) then
         dw(1) = 1.0
         return
      endif
c
      pdeep = plev(ml) - plev(1)
c
      dw( 1) = 0.5*(plev(2)-plev(1))/pdeep
      dw(ml) = 0.5*(plev(ml)-plev(ml-1))/pdeep
c
      if (ml .eq. 2) return
c
      do 10 k=2,ml-1
         dw(k) = 0.5*(plev(k+1)-plev(k-1))/pdeep
   10 continue
c
      return
      end
      SUBROUTINE GAUSSJ(A,N,NP,B,M,MP)
      PARAMETER (NMAX=50)
      DIMENSION A(NP,NP),B(NP,MP),IPIV(NMAX),INDXR(NMAX),INDXC(NMAX)
      DO 11 J=1,N
        IPIV(J)=0
11    CONTINUE
      DO 22 I=1,N
        BIG=0.
        DO 13 J=1,N
          IF(IPIV(J).NE.1)THEN
            DO 12 K=1,N
              IF (IPIV(K).EQ.0) THEN
                IF (ABS(A(J,K)).GE.BIG)THEN
                  BIG=ABS(A(J,K))
                  IROW=J
                  ICOL=K
                ENDIF
              ELSE IF (IPIV(K).GT.1) THEN
                PAUSE 'Singular matrix'
              ENDIF
12          CONTINUE
          ENDIF
13      CONTINUE
        IPIV(ICOL)=IPIV(ICOL)+1
        IF (IROW.NE.ICOL) THEN
          DO 14 L=1,N
            DUM=A(IROW,L)
            A(IROW,L)=A(ICOL,L)
            A(ICOL,L)=DUM
14        CONTINUE
          DO 15 L=1,M
            DUM=B(IROW,L)
            B(IROW,L)=B(ICOL,L)
            B(ICOL,L)=DUM
15        CONTINUE
        ENDIF
        INDXR(I)=IROW
        INDXC(I)=ICOL
        IF (A(ICOL,ICOL).EQ.0.) PAUSE 'Singular matrix.'
        PIVINV=1./A(ICOL,ICOL)
        A(ICOL,ICOL)=1.
        DO 16 L=1,N
          A(ICOL,L)=A(ICOL,L)*PIVINV
16      CONTINUE
        DO 17 L=1,M
          B(ICOL,L)=B(ICOL,L)*PIVINV
17      CONTINUE
        DO 21 LL=1,N
          IF(LL.NE.ICOL)THEN
            DUM=A(LL,ICOL)
            A(LL,ICOL)=0.
            DO 18 L=1,N
              A(LL,L)=A(LL,L)-A(ICOL,L)*DUM
18          CONTINUE
            DO 19 L=1,M
              B(LL,L)=B(LL,L)-B(ICOL,L)*DUM
19          CONTINUE
          ENDIF
21      CONTINUE
22    CONTINUE
      DO 24 L=N,1,-1
        IF(INDXR(L).NE.INDXC(L))THEN
          DO 23 K=1,N
            DUM=A(K,INDXR(L))
            A(K,INDXR(L))=A(K,INDXC(L))
            A(K,INDXC(L))=DUM
23        CONTINUE
        ENDIF
24    CONTINUE
      RETURN
      END
       SUBROUTINE PCMIN(SST,PSL,P,T,R,NA,N,PMIN,VMAX,IFL)
C
C   Revised on 9/24/2005 to fix convergence problems at high pressure
C
C   ***   This routine calculates the maximum wind speed           ***
C   ***             and mimimum central pressure                   ***
C   ***    achievable in tropical cyclones, given a sounding       ***
C   ***             and a sea surface temperature.                 ***
C
C  INPUT:   SST: Sea surface temperature in C
C
C           PSL: Sea level pressure (mb)
C
C           P,T,R: One-dimensional arrays of dimension NA
C             containing pressure (mb), temperature (C),
C             and mixing ratio (g/kg). The arrays MUST be
C             arranged so that the lowest index corresponds
C             to the lowest model level, with increasing index
C             corresponding to decreasing pressure. The temperature
C             sounding should extend to at least the tropopause and 
C             preferably to the lower stratosphere, however the
C             mixing ratios are not important above the boundary
C             layer. Missing mixing ratios can be replaced by zeros.
C
C           NA: The dimension of P,T and R
C
C           N:  The actual number of points in the sounding
C                (N is less than or equal to NA)
C
C  OUTPUT:  PMIN is the minimum central pressure, in mb
C
C           VMAX is the maximum surface wind speed, in m/s
C                  (reduced to reflect surface drag)
C
C           IFL is a flag: A value of 1 means OK; a value of 0
C              indicates no convergence (hypercane); a value of 2
C              means that the CAPE routine failed.
C
C-----------------------------------------------------------------------------
	REAL T(NA), P(NA), R(NA)
C
C   ***   Adjustable constant: Ratio of C_k to C_D    ***
C
	CKCD=0.9
C
C   ***   Adjustable constant for buoyancy of displaced parcels:  ***
C   ***    0=Reversible ascent;  1=Pseudo-adiabatic ascent        ***
C
      SIG=0.0
C
C   ***  Adjustable switch: if IDISS = 0, no dissipative heating is   ***
C   ***     allowed; otherwise, it is                                 ***
C
	IDISS=1
C
C   ***  Exponent, b, in assumed profile of azimuthal velocity in eye,   ***
C   ***   V=V_m(r/r_m)^b. Used only in calculation of central pressure   ***
C
	b=2.0
C
C   *** Set level from which parcels lifted   ***
C
	NK=1
C
C   *** Factor to reduce gradient wind to 10 m wind
C
	VREDUC=0.8
C
C   ***   Normalize certain quantities   ***
C
	SSTK=SST+273.15
	ES0=6.112*EXP(17.67*SST/(243.5+SST))
	DO 40 I=1,N
	 R(I)=R(I)*0.001
	 T(I)=T(I)+273.15
   40	CONTINUE
C
C   ***   Default values   ***
C
      VMAX=0.0
	PMIN=PSL 
	IFL=1
C
	NP=0
	PM=950.0
C
C   ***   Find environmental CAPE *** 
C
      TP=T(NK)
      RP=R(NK)
      PP=P(NK)
      CALL CAPE(TP,RP,PP,T,R,P,NA,N,SIG,CAPEA,TOA,IFLAG)
      IF(IFLAG.NE.1)IFL=2
C
C   ***   Begin iteration to find mimimum pressure   ***
C
  100 CONTINUE
C
C   ***  Find CAPE at radius of maximum winds   ***
C
      TP=T(NK)
      PP=MIN(PM,1000.0)
      RP=0.622*R(NK)*PSL/(PP*(0.622+R(NK))-R(NK)*PSL)
      CALL CAPE(TP,RP,PP,T,R,P,NA,N,SIG,CAPEM,TOM,IFLAG) 
      IF(IFLAG.NE.1)IFL=2
      RAT=SSTK/TOM
      IF(IDISS.EQ.0)RAT=1.0
C
C  ***  Find saturation CAPE at radius of maximum winds   ***
C
      TP=SSTK
      PP=MIN(PM,1000.0)
      RP=0.622*ES0/(PP-ES0)
      CALL CAPE(TP,RP,PP,T,R,P,NA,N,SIG,CAPEMS,TOMS,IFLAG)
      IF(IFLAG.NE.1)IFL=2
C
C  ***  Initial estimate of minimum pressure   ***
C
      RS0=RP
      TV1=T(1)*(1.+R(1)/0.622)/(1.+R(1))
	TVAV=0.5*(TV1+SSTK*(1.+RS0/0.622)/(1.+RS0))
C	CAT=0.5*CKCD*RAT*(CAPEMS-CAPEM)
	CAT=CAPEM-CAPEA+0.5*CKCD*RAT*(CAPEMS-CAPEM)
	CAT=MAX(CAT,0.0)
	PNEW=PSL*EXP(-CAT/(287.04*TVAV))
C
C   ***  Test for convergence   ***
C
	IF(ABS(PNEW-PM).GT.0.2)THEN
	 PM=PNEW
	 NP=NP+1
	 IF(NP.GT.1000.OR.PM.LT.400.0)THEN
	  PMIN=PSL
	  IFL=0
	  GOTO 900
	 END IF
	 GOTO 100
	ELSE
	 CATFAC=0.5*(1.+1./b)
C	 CAT=CKCD*RAT*CATFAC*(CAPEMS-CAPEM)
	 CAT=CAPEM-CAPEA+CKCD*RAT*CATFAC*(CAPEMS-CAPEM)
	 CAT=MAX(CAT,0.0)
	 PMIN=PSL*EXP(-CAT/(287.04*TVAV))
	END IF
  900	CONTINUE
	FAC=MAX(0.0,(CAPEMS-CAPEM))
	VMAX=VREDUC*SQRT(CKCD*RAT*FAC)
C
C   ***  Renormalize sounding arrays   ***
C	
	DO 910 I=1,N
	 R(I)=R(I)*1000.0
	 T(I)=T(I)-273.15
  910	CONTINUE
C
	RETURN
	END
C        
      SUBROUTINE CAPE(TP,RP,PP,T,R,P,ND,N,SIG,CAPED,TOB,IFLAG)
C
C     This routine calculates the CAPE of a parcel with pressure PP (mb), 
C       temperature TP (K) and mixing ratio RP (gm/gm) given a sounding
C       of temperature (T in K) and mixing ratio (R in gm/gm) as a function
C       of pressure (P in mb). ND is the dimension of the arrays T,R and P,
C       while N is the actual number of points in the sounding. CAPED is
C       the calculated value of CAPE and TOB is the temperature at the
C       level of neutral buoyancy.  IFLAG is a flag
C       integer. If IFLAG = 1, routine is successful; if it is 0, routine did
C       not run owing to improper sounding (e.g.no water vapor at parcel level).
C       IFLAG=2 indicates that routine did not converge.                 
C
      REAL T(ND),R(ND),P(ND),TVRDIF(100)   
      REAL NA
C
C   ***   Default values   ***
C      
      CAPED=0.0
      TOB=T(1)
      IFLAG=1
C
C   ***   Check that sounding is suitable    ***
C
      IF(RP.LT.1.0E-6.OR.TP.LT.200.0)THEN
       IFLAG=0
       RETURN
      END IF            
C
C   ***   Assign values of thermodynamic constants     ***
C
      CPD=1005.7
      CPV=1870.0
C      CL=4190.0
      CL=2500.0
      CPVMCL=CPV-CL
      RV=461.5
      RD=287.04
      EPS=RD/RV
      ALV0=2.501E6
C
C   ***  Define various parcel quantities, including reversible   ***
C   ***                       entropy, S.                         ***
C                           
      TPC=TP-273.15
      ESP=6.112*EXP(17.67*TPC/(243.5+TPC))
      EVP=RP*PP/(EPS+RP)
      RH=EVP/ESP
	RH=MIN(RH,1.0)
      ALV=ALV0-CPVMCL*TPC
      S=(CPD+RP*CL)*LOG(TP)-RD*LOG(PP-EVP)+
     1   ALV*RP/TP-RP*RV*LOG(RH)            
C
C   ***  Find lifted condensation pressure, PLCL   ***
C     
	CHI=TP/(1669.0-122.0*RH-TP)
	PLCL=PP*(RH**CHI)
C
C   ***  Begin updraft loop   ***
C
	NCMAX=0
	DO J=1,N
	 TVRDIF(J)=0.0
	END DO
C
	JMIN=1E6
	DO 200 J=1,N
C
C    ***   Don't bother lifting parcel above 60 mb and skip sections of sounding below parcel level  ***
C
      IF(P(J).LT.59.0.OR.P(J).GE.PP)GOTO 200
C
	JMIN=MIN(JMIN,J)
C
C    ***  Parcel quantities below lifted condensation level   ***
C	 
	 IF(P(J).GE.PLCL)THEN
	  TG=TP*(P(J)/PP)**(RD/CPD)
	  RG=RP
C
C   ***   Calculate buoyancy   ***
C  
	  TLVR=TG*(1.+RG/EPS)/(1.+RG)
	  TVRDIF(J)=TLVR-T(J)*(1.+R(J)/EPS)/(1.+R(J))
	 ELSE
C
C   ***  Parcel quantities above lifted condensation level  ***
C	 
	  TG=T(J)          
	  TJC=T(J)-273.15 
	  ES=6.112*EXP(17.67*TJC/(243.5+TJC)) 
	  RG=EPS*ES/(P(J)-ES)
C
C   ***  Iteratively calculate lifted parcel temperature and mixing   ***
C   ***                ratio for reversible ascent                    ***
C
	  NC=0
  120	  CONTINUE
	  NC=NC+1
C
C   ***  Calculate estimates of the rates of change of the entropy    ***
C   ***           with temperature at constant pressure               ***
C  
	  ALV=ALV0-CPVMCL*(TG-273.15)
	  SL=(CPD+RP*CL+ALV*ALV*RG/(RV*TG*TG))/TG
	  EM=RG*P(J)/(EPS+RG)
	  SG=(CPD+RP*CL)*LOG(TG)-RD*LOG(P(J)-EM)+
     1      ALV*RG/TG
	  IF(NC.LT.3)THEN
	   AP=0.3
	  ELSE
	   AP=1.0
	  END IF
	  TGNEW=TG+AP*(S-SG)/SL  
C
C   ***   Test for convergence   ***
C
	  IF(ABS(TGNEW-TG).GT.0.001)THEN
	   TG=TGNEW
	   TC=TG-273.15
	   ENEW=6.112*EXP(17.67*TC/(243.5+TC))
C
C   ***   Bail out if things get out of hand   ***
C
	   IF(NC.GT.500.OR.ENEW.GT.(P(J)-1.0))THEN
            IFLAG=2
            RETURN
	   END IF
	   RG=EPS*ENEW/(P(J)-ENEW)           
	   GOTO 120
	  END IF
	  NCMAX=MAX(NC,NCMAX)
C
C   *** Calculate buoyancy   ***
C
        RMEAN=SIG*RG+(1.-SIG)*RP
	  TLVR=TG*(1.+RG/EPS)/(1.+RMEAN)
	  TVRDIF(J)=TLVR-T(J)*(1.+R(J)/EPS)/(1.+R(J))
	 END IF
  200	CONTINUE
C
C  ***  Begin loop to find NA, PA, and CAPE from reversible ascent ***
C
	NA=0.0
	PA=0.0
C
C   ***  Find maximum level of positive buoyancy, INB    ***
C
	INB=1
	DO 550 J=N,JMIN,-1
	 IF(TVRDIF(J).GT.0.0)INB=MAX(INB,J)
  550	CONTINUE
	IF(INB.EQ.1)RETURN
C
C   ***  Find positive and negative areas and CAPE  ***
C
	IF(INB.GT.1)THEN
	 DO 600 J=JMIN+1,INB
	  PFAC=RD*(TVRDIF(J)+TVRDIF(J-1))*(P(J-1)-P(J))/(P(J)+P(J-1))
	  PA=PA+MAX(PFAC,0.0)
	  NA=NA-MIN(PFAC,0.0)
  600	 CONTINUE
C
C   ***   Find area between parcel pressure and first level above it ***
C
	PMA=(PP+P(JMIN)) 
	PFAC=RD*(PP-P(JMIN))/PMA
	PA=PA+PFAC*MAX(TVRDIF(JMIN),0.0)
	NA=NA-PFAC*MIN(TVRDIF(JMIN),0.0)
C
C   ***   Find residual positive area above INB and TO  ***
C
       PAT=0.0
       TOB=T(INB)
       IF(INB.LT.N)THEN
        PINB=(P(INB+1)*TVRDIF(INB)-P(INB)*TVRDIF(INB+1))/
     1   (TVRDIF(INB)-TVRDIF(INB+1))
        PAT=RD*TVRDIF(INB)*(P(INB)-PINB)/(P(INB)+PINB)
	  TOB=(T(INB)*(PINB-P(INB+1))+T(INB+1)*(P(INB)-PINB))/
     1    (P(INB)-P(INB+1))
       END IF
C
C   ***   Find CAPE  ***
C            
	 CAPED=PA+PAT-NA
	 CAPED=MAX(CAPED,0.0)
	END IF
C
	RETURN
	END
      subroutine lcmod(pepx,tcepx,rhepx,nepx,upx,zpx,radx,
     +                 cex,alphax,iicex,icweightx,iprtx,
     +                 vvavg,vmflux)
c
c     This is a program for a 1-dimensional Lagragian cloud model.
c
c     Input variables:
c       pepx(nepx):  Pressure levels (hPa) of environmental sounding 
c                    ordered from lowest to highest pressure
c       tcepx(nepx): Temperature (deg C) at pepx levels
c       rhepx(nepx): Relative humidity (%) at pepx levels
c       nepx:        No. of pepx levels
c       upx:         Initial parcel vertical velocity (m/s)
c       zpx:         Initial parcel height (m)
c       radx:        Inital parcel radius (m)
c       cex:         Entrainment coefficient (n.d.)
c       alphax:      Precipitation removal coefficient (1/sec)
c       iicex:       Flag for including (=1) or neglecting (=0) ice phase
c       icweightx:   Flag for including (=1) or neglecity condensate weight
c                    on buoyancy
c       iprtx:       Flag for printing output (set to 0 to supress all printing
c                    by lcmod routine except fatal errors.
c       
c     Output:
c       vmflux: Vertically averaged convective mass flux per unit area.
c        
c     Arrays for input variables
      dimension pepx(nepx),tcepx(nepx),rhepx(nepx)
c
c     Arrays for saturation vapor pressure functions
      parameter (mxt=500)      
      dimension evt(0:mxt+1), eit(0:mxt+1)
      dimension tvp(0:mxt+1),tvpc(0:mxt+1)
      dimension  et(0:mxt+1),et1(0:mxt+1),et2(0:mxt+1)
c
c     Vapor pressure variables
      common /vpr/ tvpmx,tvpmn,dt,tvp,tvpc,evt,eit,et,et1,et2
      common /vpi/ nvp
c
c     Reference state variables
      common /ref/ tref,paref,eref,rhoaref,rhocref,rhovref,daref
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Arrays for enivornmental sounding versus P
      parameter (mel=800)
      dimension tkep(mel),rhep(mel),ppep(mel),tvkep(mel)
      common /envts/ tkep,rhep,ppep,tvkep,nep
c
c     Arrays for environmental sounding versus z
      parameter (mz=1000)
      dimension zze(mz),tze(mz),tvze(mz),pze(mz),rhze(mz)
      dimension wze(mz),wsze(mz),eze(mz),esze(mz),sze(mz)
      common /envz/ zze,tze,tvze,pze,rhze,wze,wsze,eze,esze,sze,nez
c
c     Arrays for evenly spaced output grid
      parameter (mto=10000,mzo=1000)
      dimension tto(mto),zto(mto),pto(mto),rhoto(mto),uto(mto),rto(mto)
      dimension tpto(mto),teto(mto),tvpto(mto),tveto(mto)
      dimension wvpto(mto),wspto(mto),wveto(mto),wcpto(mto)
      common /tov/ tto,zto,pto,rhoto,uto,rto,tpto,teto,tvpto,tveto,
     +             wvpto,wspto,wveto,wcpto
c
      dimension tzo(mto),zzo(mto),pzo(mto),rhozo(mto),uzo(mto),rzo(mto)
      dimension tpzo(mto),tezo(mto),tvpzo(mto),tvezo(mto)
      dimension wvpzo(mto),wspzo(mto),wvezo(mto),wcpzo(mto)
      common /zov/ tzo,zzo,pzo,rhozo,uzo,rzo,tpzo,tezo,tvpzo,tvezo,
     +             wvpzo,wspzo,wvezo,wcpzo
c
c     Physical factor flags
      common /pflag/ iice,icweight
c
c     Unit numbers
      data lulog,ludat /6,10/
c
c     ++ Parameter specification ++
c
c     Initialize time (t0), parcel height (m), vertical velocity (m/s)
c     and radius (m)
      tsec   = 0.0
      zp     = zpx
      up     = upx
      rp     = radx
c
c     Specify the time step (sec) and the number of time steps
      dtsec  =  5.0
      nts    =  500
c
c     Set iupos=1 to stop model integration when vertical velocity
c         becomes negative
      iupos=1
c
c     Specify the time step interval for printing output
      ntsp = 1 
c
c     Specify the time step label interval for printing output
      ntsl= 50
c
c     Set iice=1 to include the ice phase
      iice = iicex
c
c     Set icweight=1 to include the effect of condensate weight on buoyancy
      icweight = icweightx 
c
c     Specify the height increment max height (m) for the evenly 
c     spaced output and calculation grid
      dzo   = 100.0
      dzmax = 15000.0
c
c     ++ Model set-up ++
c     Initialize physical and numerical constants
      call pncint
c
c     Over-ride alpha and ce with the values from the routine 
c     calling arguments
      ce = cex
      alpha = alphax
c
c     Initialize saturation vapor pressure tables
      call svptab
c
c     ++ Environmental sounding initialization and unit conversion ++
      nep = nepx
      do i=1,nep
         ppep(i) = 100.0*pepx(i)
         tkep(i) = tcepx(i) + tck
         rhep(i) = rhepx(i)
      enddo
c
c     Interpolate environmental sounding to function of z
      call septoz(iprtx,dzmax)
c
c     Initialize all  time accumulation array variables to zero
      do i=1,mto
         tto(i) = 0.0
         zto(i) = 0.0
         pto(i) = 0.0
         rhoto(i) = 0.0
         uto(i)   = 0.0
         rto(i)   = 0.0
         tpto(i)  = 0.0
         teto(i)  = 0.0
         tvpto(i) = 0.0
         tveto(i) = 0.0
         wvpto(i) = 0.0
         wspto(i) = 0.0
         wveto(i) = 0.0
         wcpto(i) = 0.0
      enddo
c
c     ** Start parcel initialization ***
c
c     Get environmental p,t,tv,w and s at tsec=0
      call tdenv(zp,pe,te,tve,wve,se,lulog)
      wce = 0.0
      we  = wve + wce
c
c     Initialize parcel pressure (pp0), water mixing ratio (wp0), 
c     and entropy mixing ratio (sp0)
      pp = pe
      wp = wve
      sp = se
c
c     Specify first guess parcel T and water vapor pressure
c     for TD diagnostic routine
      tfg1 = te
      tfg2 = te
      pvfg= wp*pp/(wp + ra/rv)
c
c     Diagnose parcel temp, water vapor and condensate mixing ratios,
c     water vapor pressure and total parcel density
      call tddiag(pp,sp,wp,tfg1,tfg2,pvfg, t1,t2,tp,wvp,wcp,pvp,rhop)
      call tvcal1(tp,pp,wvp,tvpar)
c
c     Save t1 and t2 for the next time step
      tfg1 = t1
      tfg2 = t2
c
c     Calculate saturation mixing ratio of the parcel
      call escal(tp,es,des,d2es,rl)
      wsp = ra*es/(rv*(pp-es))
c
c     Calculate initial parcel mass
      pmass = rhop*(4.0/3.0)*pi*(rp**3)
c
c     Print initial parcel values
      ilab = 1
      if (iprtx .ne. 0) then
         call pprint(lulog,ilab,tsec,zp,pp,rhop,up,pmass,rp,
     +               t1,t2,tp,te,tvpar,tve,wvp,wsp,wve,wcp,wce,sp,se)
      endif
c
c     Save initial parcel and environmental variables
      nsave = 1
      call vsave(nsave,tsec,zp,pp,rhop,up,rp,tp,te,tvpar,tve,
     +           wvp,wsp,wve,wcp)
c
c     ** End Parcel Initialization ***
c
c     ** Begin time integration section **
c
c     Calculate time step factors for Adams-Bashforth time integration
      dtth = 1.5*dtsec
      dtoh = 0.5*dtsec
c
      do 99 i=1,nts
         tsec = tsec + dtsec
c
c        Calculate time tendency of prognostic variables
         call ttcal(tvpar,tve,wvp,wcp,we,up,rp,pmass,sp,se,
     +              upt1,pmasst1,wpt1,spt1,zpt1)
c
c        write(6,830) i,upt1,pmasst1,wpt1,spt1,zpt1
c 830    format('i,ut,pmt,wt,st,st ',i4,5(e11.4))
c
         if (i .eq. 1) then
c           Forward time step
            up    = up    + dtsec*upt1
            pmass = pmass + dtsec*pmasst1
            wp    = wp    + dtsec*wpt1
            sp    = sp    + dtsec*spt1
            zp    = zp    + dtsec*zpt1
         else
c           Adams-Bashforth time step
            up    = up    + dtth*upt1    - dtoh*upt0
            pmass = pmass + dtth*pmasst1 - dtoh*pmasst0
            wp    = wp    + dtth*wpt1    - dtoh*wpt0
            sp    = sp    + dtth*spt1    - dtoh*spt0
            zp    = zp    + dtth*zpt1    - dtoh*zpt0
         endif
c
c        Check for negative vertical velocity
         if (iupos .eq. 1) then
            if (up .lt. 0.0) then
               if (iprtx .ne. 0) then
                  write(lulog,860) zp
  860             format(/,' Vertical velocity negative, ',
     +                     ' Max parcel height reached ',f7.0,' m')
               endif
               go to 7000
            endif
         endif
c
         if (zp .ge. zze(nez)) then
            if (iprtx .ne. 0) then
               write(lulog,861) zp/1000.0
  861          format(/,' Parcel height above model top, z=',f6.2,'km')
            endif
            go to 7000
         endif
c
c        Save tendencies for the next time step
         upt0    = upt1
         pmasst0 = pmasst1
         wpt0    = wpt1
         spt0    = spt1
         zpt0    = zpt1

c        Update diagnostic variables
c
c        Get environmental p,t,tv,w and s at new z
         call tdenv(zp,pe,te,tve,wve,se,lulog)
         wce = 0.0
         we  = wve + wce
c
c        Set parcel pressure equal to environment pressure
         pp  = pe
c
c        Specify first guess parcel T and water vapor pressure
c        for TD diagnostic routine
         tfg = tp
         pvfg= wp*pp/(wp + ra/rv)
c
c        Diagnose parcel temp, water vapor and condensate mixing ratios,
c        water vapor pressure and total parcel density
         call tddiag(pp,sp,wp,tfg1,tfg2,pvfg, t1,t2,tp,wvp,wcp,pvp,rhop)
         call tvcal1(tp,pp,wvp,tvpar)
c
c        Save t1 and t2 for the next time step
         tfg1 = t1
         tfg2 = t2
c
c        write(6,831) i,t1,t2,tp,wvp,wcp,pvp,rhop
c 831    format('i,t1,t2,tp,wvp,wcp,pvp,rhop ',i3,1x,7(e11.4,1x))
c
c        Calculate saturation mixing ratio of the parcel
         call escal(tp,es,des,d2es,rl)
         wsp = ra*es/(rv*(pp-es))
c
c        Diagnose parcel radius from the mass
         rp = ( 3.0*pmass/(4.0*pi*rhop) )**(1.0/3.0)
c
         if (mod(i,ntsp) .eq. 0) then
            if (mod(i,ntsl) .eq. 0) then
               ilab = 1
            else
               ilab = 0
            endif
c
            if (iprtx .ne. 0) then
            call pprint(lulog,ilab,tsec,zp,pp,rhop,up,pmass,rp,
     +                  t1,t2,tp,te,tvpar,tve,wvp,wsp,wve,wcp,wce,sp,se)
            endif
c
         endif
c
c        Save initial parcel and environmental variables
         nsave = i+1
         call vsave(nsave,tsec,zp,pp,rhop,up,rp,tp,te,tvpar,tve,
     +              wvp,wsp,wve,wcp)
c
   99 continue
c
 7000 continue
c     Write output variables on evenly spaced vertical grid
      call vezdat(ludat,nts+1,dzo,dzmax,nzo,iprtx)
c
c     Calculate average vertical mass flux
      call avmf(nzo,zzo,uzo,rhozo,tpzo,tezo,vvavg,vmflux,cape,cin)
c
      if (iprtx .ne. 0) then
         write(lulog,310) vvavg,vmflux,cape,cin
  310    format('vvavg=',f6.2,' vmflux=',f6.2, ' cape=',f7.1,
     +          ' cin=',f6.1)
      endif
c
      return 
      end
      subroutine pncint
c     This routine initializes needed physical and 
c     numerical constants. MKS units are used
c
c     Reference state variables
      common /ref/ tref,paref,eref,rhoaref,rhocref,rhovref,daref
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Physical factor flags
      common /pflag/ iice,icweight
c
c     PI
      pi = 3.14159265
c
c     Gravitational constant
      g = 9.81
c
c     Dry air properties
      ra = 287.01
      cpa= 1005.7
      cva= 718.7
c
c     Water vapor properties
      rv = 462.5
      cpv= 1875.0
      cvv= 1412.5
c
c     Conversion from Centigrade to Kelvin
      tck = 273.15
c
c     Temperature parameters for liquid to ice transition zone
      if (iice .eq. 1) then
         tf =  -7.5+tck
         dtf=   2.5
      else
         tf = -200.0+tck
         dtf=   2.5
      endif
c
c     Entrainment coefficient (nd)
      ce = 0.1
c 
c     Drag coefficient (nd)
      cd = 0.0 
c
c     Precipitation coefficient (1/sec)
      alpha = 1.0/600.0
c
      return
      end
      subroutine svptab
c     This routine calculates tables of the saturation vapor 
c     pressure (hPa) as a function of temperature in Kelvin (tvp). 
c     The vapor pressure over water and ice (evt, eit) are first 
c     calculated using polynomials from Flatau (1993) and 
c     then for a combined water-ice mixture (et) using the
c     method from Ooyama (1990). The 1st and 2nd derivative of 
c     et wrt tvp are then calculated using finite difference
c     formulas. 
c
c     Reference state variables
      common /ref/ tref,paref,eref,rhoaref,rhocref,rhovref,daref
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Arrays for saturation vapor pressure functions
      parameter (mxt=500)      
      dimension evt(0:mxt+1),eit(0:mxt+1)
      dimension  tvp(0:mxt+1),tvpc(0:mxt+1)
      dimension  et(0:mxt+1),et1(0:mxt+1),et2(0:mxt+1)
c
      common /vpr/ tvpmx,tvpmn,dt,tvp,tvpc,evt,eit,et,et1,et2
      common /vpi/ nvp
c
c     Latent heat array
      dimension rlt(0:mxt+1)
      common /dvp/ rlt
c
c     Arrays for polynomial coefficients
      dimension a(0:6),b(0:6)
c
c     Arrays for temperatures weights for water-air mixing
      dimension ww(0:mxt+1),wi(0:mxt+1),dwwdt(0:mxt+1)
      dimension enum(0:mxt+1)
c     
c     Array for E smoothing
      dimension evf(0:mxt+1)
c
c     Specify the start, ending and increment of 
c     temperature (K) for the vp tables
c
      tvpmn = -120.0+tck
      tvpmx =  50.0+tck
      dt    = 0.5
      dt2   = 2.0*dt
      dts   = dt*dt
      nvp   = 1 + ifix( 1.0e-4 + (tvpmx-tvpmn)/dt )
c
c     Set nfilt to number of times to smooth et(n)
      nfilt=1
c
      do n=0,nvp+1
         tvp(n) = tvpmn + dt*float(n-1)
         tvpc(n)= tvp(n)-tck
      enddo
c
c     Calculate water and ice weights as function of T
      do n=0,nvp+1
         tn = (tvp(n)-tf)/dtf
         ww(n) = 0.5*(1.0+tanh(tn))
         wi(n) = 1.0-ww(n)
c
         dwwdt(n) = (1.0-(tanh(tn))**2)/(2.0*dtf)
      enddo
c
c     Specify polynomial coefficients for calculation
c     of evt and eit.
      a(0) = 6.11176750
      a(1) = 0.443986062
      a(2) = 0.143053301e-01
      a(3) = 0.265027242e-03
      a(4) = 0.302246994e-05
      a(5) = 0.203886313e-07
      a(6) = 0.638780966e-10
c
      b(0) = 6.10952665
      b(1) = 0.501948366
      b(2) = 0.186288989e-01
      b(3) = 0.403488906e-03
      b(4) = 0.539797852e-05
      b(5) = 0.420713632e-07
      b(6) = 0.147271071e-09
c
c     Speficy reference state T and P
      tref = 273.15
      paref = 1.0e+5
c
c     Calculate ev and ei at the reference state
      evref = 0.0
      eiref = 0.0
      trefc = tref - tck
c
      do k=0,6
         ttk = trefc**k
         evref = evref + a(k)*ttk
         eiref = eiref + b(k)*ttk
      enddo
c
      evref = 100.0*evref
      eiref = 100.0*eiref
c     
c     Calculate evt and eit from polynomial series
c
c     Specify minimum T value (C) for utilizing tables.
c     Asympototic exponential forms are used for colder T.
c     Also, specify the width of the blending zone (tblend).
      ttmin = -50.0
      tblend=  1.0
c
      do n=0,nvp+1
         tt = (tvpc(n))
c
         evt(n) = 0.0
         eit(n) = 0.0
c       
c        Asymptotic form
         evt2 = 1459.9*exp(.1083*tt)  
c        eit2 = 1464.2*exp(.1182*tt)
c        tti = -50.0-tt
c        if (tti .ge. 0.0) then
c           eit2 = 3.942*exp(-.106*(tti)**1.09)
c        else
c           eit2 = 3.942*exp( .106*(-tti)**1.09)
c        endif
c
         ttk = tt + tck
         eit2 = 3.942*exp(6127.6*(1.0/223.15 - 1.0/ttk))
c
c        General form
         evt1 = 0.0
         eit1 = 0.0
         do k=0,6
            ttk = tt**k
            evt1 = evt1 + a(k)*ttk
            eit1 = eit1 + b(k)*ttk
         enddo
c
c        Convert to hPa
         evt1 = 100.0*evt1
         eit1 = 100.0*eit1
c
         w1 = 0.5*(1.0 + tanh( (tt-ttmin)/tblend ))
         w2 = 1.0 - w1
c
c        write(6,*) tt,w1,w2,evt1,evt2,eit1,eit2
c
         evt(n) = w1*evt1 + w2*evt2
         eit(n) = w1*eit1 + w2*eit2
      enddo
c
c     Initialize water-ice vp with water vp
      do n=0,nvp+1
         et(n) = evt(n)
      enddo
c
c     Specify index of temperature array to begin
c     integration for water-ice mixture vp calculation
      nts = nvp-10
c
      ts  = tvp(nts)
      evs = evt(nts)
      eis = eit(nts)
c
c     Analytic part of e(t) calculation
      do n=nts,0,-1
         et(n) = alog(evref) + (ts/tvp(n))*alog(evs/evref)
     +           + ww(n)*alog(evt(n)/evref) 
     +           - ww(nts)*(ts/tvp(n))*alog(evs/evref)
     +           + wi(n)*alog(eit(n)/eiref)
     +           - wi(nts)*(ts/tvp(n))*alog(eis/eiref)
      enddo
c
c     Calculate the integral term in the e(t) calculation
      etm = 0.0
      enum(nts) = 0.0
      do n=nts-1,0,-1
         dtm  = tvp(n)-tvp(n+1)
         tm1  = tvp(n+1)*dwwdt(n+1)*(alog(eit(n+1)/eiref)
     +                              -alog(evt(n+1)/evref))
         tm2  = tvp(n  )*dwwdt(n  )*(alog(eit(n  )/eiref)
     +                              -alog(evt(n  )/evref))
         etm  = dtm*0.5*(tm1+tm2)
         enum(n) = enum(n+1) + etm
      enddo
c
c     Add integral term to analytic term
      do n=nts,0,-1
          et(n) = et(n) + enum(n)/tvp(n)
      enddo
c
c     Take exponential to find evt
      do n=nts,0,-1
         et(n) = exp(et(n))
      enddo
c

      if (nfilt .gt. 0) then
         do k=1,nfilt
            evf(  0) = et(  0)
            evf(nts) = et(nts)
c
            do n=1,nts-1
               evf(n) = 0.25*et(n-1) + 0.5*et(n) + 0.25*et(n+1)
            enddo
c
            do n=1,nts-1
               et(n) = evf(n)
            enddo
         enddo
c
      endif
c
      et1(0)     = 0.0
      et2(0)     = 0.0
      et1(nvp+1) = 0.0
      et2(nvp+1) = 0.0
c
c     Calculate first and second derivative of et
      do n=1,nvp
         et1(n) = (et(n+1)-et(n-1))/dt2
         et2(n) = (et(n+1)+et(n-1)-2.0*et(n))/dts
      enddo
c
c     Calculate latent heat of water-ice mixture
c     from C-C equation
      rlt(0)     = 0.0
      rlt(nvp+1) = 0.0
      do n=1,nvp
         rlt(n) = et1(n)*rv*tvp(n)*tvp(n)/et(n)
      enddo
c
      iprint = 0
      if (iprint .eq. 1) then
         write(6,801)
  801    format('       T      Wv      Ev         Ei          E     ',
     +          ' dE/dT     d2E/dT2     L')
c
         do n=1,nvp
            write(6,800) n,tvpc(n),ww(n),evt(n),eit(n),
     +                   et(n),et1(n),et2(n),rlt(n)
  800       format(1x,i4,f6.1,1x,f4.2,1x,e10.4,1x,e10.4,4(1x,e10.4))
         enddo
      endif
c
c     Specify the rest of the reference state variables
      eref    = evref
      rhoaref = paref/(ra*tref)
      rhocref = 0.0
      rhovref = eref/(rv*tref)
c
      call escal(tref,es,des,d2es,rl)
      daref = rl/tref
c
      return
      end
      subroutine tvcal(t,p,rh,tv)
c     This routine calculates the virtual temperature tv (K)
c     given the temperature t (K), pressure p (Pa), and relative
c     humidity rh (%)
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
      call escal(t,es,des,d2es,rl)
      ws = ra*es/(rv*(p-es))
      w  = ws*rh/100.0
      c1 = (rv-ra)/ra
      v1 = w/(1.0+w)
      tv = t*(1.0 + c1*v1)
c
      return
      end
      subroutine tvcal1(t,p,w,tv)
c     This routine calculates the virtual temperature tv (K)
c     given the temperature t (K), pressure p (Pa), and
c     water vapor mixing ratio wv (kg/kg)
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
      c1 = (rv-ra)/ra
      v1 = w/(1.0+w)
      tv = t*(1.0 + c1*v1)
c
      return
      end
      subroutine escal(t,es,des,d2es,rl)
c     This routine calculates the saturation vapor
c     pressure (es in Pa) from the temperature (t in K) by
c     interpolating from a pre-calculated table. 
c
c     The first (des) and second (d2es) derivatives of es wrt to temperature
c     and the latent heat (rl) are also calcualted. 
c
c     Arrays for saturation vapor pressure functions
      parameter (mxt=500)      
      dimension evt(0:mxt+1), eit(0:mxt+1)
      dimension tvp(0:mxt+1),tvpc(0:mxt+1)
      dimension  et(0:mxt+1),et1(0:mxt+1),et2(0:mxt+1)
c
c     Latent heat array
      common /dvp/ rlt
      dimension rlt(0:mxt+1)
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Vapor pressure variables
      common /vpr/ tvpmx,tvpmn,dt,tvp,tvpc,evt,eit,et,et1,et2
      common /vpi/ nvp
c
      if     (t .ge. tvpmx) then
         es   = et(0)
         des  = et1(0)
         d2es = et2(0)
         rl   = rlt(0)
      elseif (t .le. tvpmn) then
         es  = et(nvp)
         des = et1(nvp)
         d2es= et2(nvp)
         rl  = rlt(nvp)
      else
c        Find index closest to but less than tt
         id1 = ifix( (t-tvpmn)/dt )
         id2 = id1 + 1
c
         e1 = et(id1)
         e2 = et(id2)
         f1 = et1(id1)
         f2 = et1(id2)
         g1 = et2(id1)
         g2 = et2(id2)
         r1 = rlt(id1)
         r2 = rlt(id2)
c
         w2 = (t-tvp(id1))/dt
         w1 = 1.0 - w2
c
         es   = w1*e1 + w2*e2         
         des  = w1*f1 + w2*f2
         d2es = w1*g1 + w2*g2
         rl   = w1*r1 + w2*r2
      endif
c
      return
      end
      subroutine scal(p,t,w, sa,sm,s,wc)
c     This routine calculates the dry air and moisture mass-specific 
c     entropies (sa and sm) and the total air entropy mixing ratio (s)
c     given the total pressure p, temperature t and total water mixing ratio (w).
c     The mixing ratio of the condensed water is also calculated if
c     the air is saturated. MKS units are used for all variables. 
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Reference state variables
      common /ref/ tref,paref,eref,rhoaref,rhocref,rhovref,daref
c
c     Calculate the saturation vapor pressure (e)
      call escal(t,es,des,d2es,rl)
c
c     Calculate the vapor pressure from the total mixing ratio
      pv = w*p/(w + ra/rv)
c
      if (pv .le. es) then
c        The air is unsaturated
         wc = 0.0
         pa = p - pv
         rhoa = pa/(ra*t)
         rhov = pv/(rv*t)
         rhom = rhov
c
         sa = cva*alog(t/tref) - ra*alog(rhoa/rhoaref)
         sm = cvv*alog(t/tref) - rv*alog(rhov/rhovref) + daref
      else
c        The air is saturated
         pa = p - es
         rhoa = pa/(ra*t)
         rhov = es/(rv*t) 
         rhom = w*rhoa
c
         ws   = rhov/rhoa
         wc   = w - ws
c
         sa = cva*alog(t/tref) - ra*alog(rhoa/rhoaref)
         sm = cvv*alog(t/tref) - rv*alog(rhov/rhovref) + daref -
     +        (rl/t)*(1.0-(rhov/rhom))
c
      endif
c
      s = (sa*rhoa + sm*rhom)/rhoa
c
c      write(6,*) t,p,pv,rhoa,rhom
      return
      end
      subroutine scal1(p,t,w, sa1,sa2,sm1,sm2,s1,s2,wc)
c     This routine calculates the dry air and moisture mass-specific 
c     entropies (sa and sm) and the total air entropy mixing ratio (s)
c     given the total pressure p, temperature t and total water mixing ratio (w).
c     The mixing ratio of the condensed water is also calculated if
c     the air is saturated. MKS units are used for all variables. 
c
c     In this version both sm1,sm2 and s1,s2 are returned (the unsaturated 
c     and saturated versions of sm and s) for testing purposes.
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Reference state variables
      common /ref/ tref,paref,eref,rhoaref,rhocref,rhovref,daref
c
c     Calculate the saturation vapor pressure (e)
      call escal(t,es,des,d2es,rl)
c
c     Calculate the vapor pressure from the total mixing ratio
      pv = w*p/(w + ra/rv)
c
c     Unsaturated case
         wc = 0.0
         pa = p - pv
         rhoa = pa/(ra*t)
         rhov = pv/(rv*t)
         rhom = rhov
c
         sa1 = cva*alog(t/tref) - ra*alog(rhoa/rhoaref)
         sm1 = cvv*alog(t/tref) - rv*alog(rhov/rhovref) + daref
         s1 = (sa1*rhoa + sm1*rhom)/rhoa
c
c     Saturated case
         pa = p - es
         rhoa = pa/(ra*t)
         rhov = es/(rv*t) 
         rhom = w*rhoa
c
         ws   = rhov/rhoa
         wc   = w - ws
c
         sa2 = cva*alog(t/tref) - ra*alog(rhoa/rhoaref)
         sm2 = cvv*alog(t/tref) - rv*alog(rhov/rhovref) + daref -
     +        (rl/t)*(1.0-(rhov/rhom))
         s2 = (sa2*rhoa + sm2*rhom)/rhoa
c
      return
      end
      subroutine septoz(iprtx,dzmax)
c     This routine converts the environmental sounding
c     from a function of P to a function of z, and calcualtes
c     needed environmental moisture variables.
c
c     Arrays for enivornmental sounding versus P
      parameter (mel=800)
      dimension tkep(mel),rhep(mel),ppep(mel),tvkep(mel)
      common /envts/ tkep,rhep,ppep,tvkep,nep
c
c     Arrays for environmental sounding versus z
      parameter (mz=1000)
      dimension zze(mz),tze(mz),tvze(mz),pze(mz),rhze(mz)
      dimension wze(mz),wsze(mz),eze(mz),esze(mz),sze(mz)
      common /envz/ zze,tze,tvze,pze,rhze,wze,wsze,eze,esze,sze,nez
c
      dimension rlze(mz)
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Local variables
      dimension zp(mel),saze(mz),smze(mz)
c
c     Specify min and max z values (meters)
      zb = 0.0
c     zt = 16.0e+3
      zt = dzmax + 500.0
      dz = 0.5e+3
      nez = 1 + ifix(0.0001 + (zt-zb)/dz)
c
      do k=1,nez
         zze(k) = zb + dz*float(k-1)
      enddo
c
c     Calculate Tv at pressure levels
      do n=1,nep
         call tvcal(tkep(n),ppep(n),rhep(n),tvkep(n))
      enddo
c
c     Calculate the height of the environmental pressure levels
      zp(nep) = 0.0
      do n=nep-1,1,-1
         p2 = ppep(n   )
         p1 = ppep(n+1 )
         tv2 = tvkep(n  )
         tv1 = tvkep(n+1) 
         if (tv1 .eq. tv2) tv1 = tv1 + 0.001
c
         zp(n) = zp(n+1) + (ra/g)*(tv2-tv1)*alog(p1/p2)/alog(tv2/tv1)
      enddo
c
      if (iprtx .ne. 0) then
         do n=1,nep
            write(6,301) ppep(n),zp(n),tkep(n)-tck,tvkep(n)-tck,rhep(n)
  301       format(1x,'P=',f7.0,' Z=',f7.0,' T=',f6.1,' Tv=',f6.1,
     +                ' RH',f6.1)
         enddo
      endif
c
c     Calculate T and P as a function of height
      do 99 k=1,nez
c
c        Find the environmental pressure levels above and below the 
c        current height level
         do n=1,nep-1
            if (zze(k) .lt. zp(n) .and. zze(k) .ge. zp(n+1)) then
               tv1 = tvkep(n+1)
               tv2 = tvkep(n  )
               t1 = tkep(n+1)
               t2 = tkep(n  )
               p1 = ppep(n+1)
               p2 = ppep(n  )
               z1 = zp(n+1)
               z2 = zp(n  )
               r1 = rhep(n+1)
               r2 = rhep(n  )
c
               if (tv1 .eq. tv2) tv1 = tv1 + 0.001
c
               go to 1000
            endif
         enddo
c
         write(6,900) zze(k)
  900    format(' z=',f8.1,' out of z domain in routine septoz')
         stop
c
 1000    continue
c
         gammav= (tv2-tv1)/(z2-z1)
         gammat= (t2 - t1)/(z2-z1)
         gammar= (r2 - r1)/(z2-z1)
         aa    = -g/(ra*gammav)
c
         tvze(k) = tv1 + gammav*(zze(k)-z1)
         tze(k)  = t1  + gammat*(zze(k)-z1)
         rhze(k) = r1  + gammar*(zze(k)-z1)
         pze(k)  = p1*(tvze(k)/tv1)**aa
c
         call escal(tze(k),esze(k),des,d2es,rl)
         wsze(k) = ra*esze(k)/(rv*(pze(k)-esze(k)))
         wze(k)  = wsze(k)*rhze(k)/100.0
         eze(k)  = wze(k)*pze(k)/(wze(k) + ra/rv)
         rlze(k) = rl
c
         call scal(pze(k),tze(k),wze(k),sa,sm,sze(k),wc)
         saze(k) = sa
         smze(k) = sm
c
   99 continue 
c
      if (iprtx .ne. 0) then
      write(6,299) 
  299 format('  Z      T      Tv      P       RH     ws      w      e',
     +       '    Sa      Sm      S       L')
      do k=nez,1,-1
         write(6,300) zze(k)/1000.0,tze(k)-tck,tvze(k)-tck,
     +                pze(k)/100.0,rhze(k),wsze(k)*1000.,wze(k)*1000.,
     +                eze(k)/100.0,saze(k),smze(k),sze(k),rlze(k)
c  300    format( 'Z=',f6.1,' T= ',f6.1,' Tv=',f6.1,
c     +          ' P=',f6.1,' RH=',f6.1,' ws=',f6.2,1x,
c     +          ' w=',f6.2,' e=',f6.2,' sa=',f6.1,' sm=',f6.1,
c     +          ' s=',f6.1,' L=',e10.3)
  300    format(5(f6.1,1x),3(f6.2,1x),3(f7.1,1x),e10.3)
      enddo
      endif
c 
      return
      end
      subroutine tdenv(z,pe,te,tve,we,se,lulog)
c     This routine calculates the thermodynamic properties 
c     of the parcel environment at level z. It is assumed that
c     the parcel environment is unsaturated.  
c
c     Reference state variables
      common /ref/ tref,paref,eref,rhoaref,rhocref,rhovref,daref
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Arrays for environmental sounding versus z
      parameter (mz=1000)
      dimension zze(mz),tze(mz),tvze(mz),pze(mz),rhze(mz)
      dimension wze(mz),wsze(mz),eze(mz),esze(mz),sze(mz)
      common /envz/ zze,tze,tvze,pze,rhze,wze,wsze,eze,esze,sze,nez
c
c     Find height level closest to z
      do k=1,nez-1
         if (z .ge. zze(k) .and. z .le. zze(k+1)) then
            p1  = pze(k)
            p2  = pze(k+1)
            t1  = tze(k) 
            t2  = tze(k+1)
            tv1 = tvze(k)
            tv2 = tvze(k+1)
            r1  = rhze(k)
            r2  = rhze(k+1)
            e1  = eze(k)
            e2  = eze(k+1)
            w1  = wze(k)
            w2  = wze(k+1)
            z1  = zze(k)
            z2  = zze(k+1)
            se1 = sze(k)
            se2 = sze(k+1)
c
            go to 1000
         endif
      enddo
c
      write(lulog,900) z
  900 format(/,'z outside of model domain, z=',f8.1)
      stop
c
 1000 continue
c
      a1 = (z2-z)/(z2-z1)
      a2 = (z-z1)/(z2-z1)
c
      pe = a1*p1 + a2*p2
      te = a1*t1 + a2*t2
      tve= a1*tv1+ a2*tv2
      we = a1*w1 + a2*w2
      se = a1*se1+ a2*se2
c
      return
      end
      subroutine tddiag(p,s,w,tfg1,tfg2,pvfg, t1,t2,t,wv,wc,pv,rho)
c     The routine diagnoses the temperature t, water vapor mixing
c     ratio (wv), water vapor condensate (wc) mixing ration, water vapor pressure
c     (pv) and total air density (rho), given the total pressure (p), entropy
c     mixing ratio (s), and total water mixing ratio (w).
c
c     First guess temperatures for t1 and t2 (tfg1 and tfg2) and 
c     water vapor pressure (pvfg) need to be provided.
c   
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Specify the number of iterations
      nit = 10
c
c     Find T1
      wv1 = w
      wc1 = 0.0
c
      pv1 = wv1*p/(wv1 + ra/rv)
      pa = p - pv1
c
      t1 = tfg1
      do 98 i=1,nit
         rhoa   = pa/(ra*t1) 
         call t1froms(s,w,rhoa, t1)
   98 continue
c 
c     Find T2
c
      t2 = tfg2
      do 99 i=1,nit
         call escal(t2,es,des,d2es,rl)
         pv2 = es
         pa  = p - pv2
         rhoa = pa/(ra*t2)
         wv2 = es/(rv*t2*rhoa)
         wc2 = w - wv2
         tstart = t2
c
         call t2froms(s,w,rhoa,tstart, t2)
c        write(6,*) 'i98,tstart,t2 ',i,tstart,t2
   99 continue
c 
      if (t1 .ge. t2) then
c     if (t1 .ge. 0) then
         t  = t1
         wv = wv1
         wc = wc1
         pv = pv1
      else
         t  = t2
         wv = wv2
         wc = wc2
         pv = pv2
      endif
c
c     Calculate final value of total air density
      pa     = p - pv
      rhoa   = pa/(ra*t) 
      rhov   = wv*rhoa
      rhoc   = wc*rhoa
      rho    = rhoa + rhov + rhoc
c
c     call scal1(p,t1,w, sa11,sa12,sm11,sm12,s11,s12,wc1)
c     call scal1(p,t2,w, sa21,sa22,sm21,sm22,s21,s22,wc2)
c
c     write(6,800) t1,t2,rhoa,rhov,rhoc,rho,pv
c 800 format('t1,t2,rhoa,rhov,rhoc,rho,pv: ',
c    +       f7.2,1x,f7.2,1x,4(e11.4,1x),1x,f6.1)
c
c     write(6,801) sa11,sm11,s11,sa12,sm12,s12,wc1,
c    +             sa21,sm21,s21,sa22,sm22,s22,wc2
c 801 format('sa11,sm11,s11,sa12,sm12,s12,wc1: ',7(e11.4,1x),/,
c    +       'sa21,sm21,s21,sa22,sm22,s22,wc2: ',7(e11.4,1x))
c
      return
      end
      subroutine t1froms(s,w,rhoa, t1)
c     This routine calculates the temperature t1 from the 
c     entropy density s, total water mixing ratio w and dry 
c     air density rhoa assuming unsaturated air, following 
c     Ooyama (1990).
c
c     Reference state variables
      common /ref/ tref,paref,eref,rhoaref,rhocref,rhovref,daref
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
      eta = w*rhoa
c
c     Calculate t1 from the analytic formula
      fnum = s + ra*alog(rhoa/rhoaref) + w*rv*alog(eta/rhovref) - 
     +       w*daref
      fden = cva + w*cvv
      t1   = tref*exp(fnum/fden)
c
      return
      end
      subroutine t2froms(s,w,rhoa,tstart, t2)
c     This routine calculates the temperature t from the 
c     entropy density s, total water mixing ratio w and dry 
c     air density rhoa using an iterative procedure. The input
c     variable tstart is the first guess for the iteration.
c     The formulation follows Ooyama (1990).
c
c     Reference state variables
      common /ref/ tref,paref,eref,rhoaref,rhocref,rhovref,daref
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
      eta = w*rhoa
c
c     Calculate t2 using an iterative procedure
      t2 = tstart
      nit = 10
      do 99 i=1,nit
         t = t2
         sa  = cva*alog(t/tref) - ra*alog(rhoa/rhoaref)
c
         call escal(t,es,des,d2es,rl)
         etas = es/(rv*t)
c
         sm1 = cvv*alog(t/tref) 
         sm2 = -rv*alog(etas/rhovref)
         sm3 = daref
         sm4 = (etas-eta)*(rl/t)/eta
         sm = sm1 + sm2 + sm3 + sm4
c
         dsadt = cva/t
c
         dsm1 = cpv/t
         dsm2 = (rv/es)*des*((t/es)*des-2.0)
         dsm3 = d2es*((1.0/eta) - (rv*t)/es)
         dsmdt = dsm1 + dsm2 + dsm3
c
c        siter = sa + w*sm
c        write(6,750) i,t,sa,sm,siter,s
c 750    format('i,t,sa,sm,siter,s ',i2,1x,f6.2,4(e11.4))
c
         f = sa + w*sm - s
         dfdt = dsadt + w*dsmdt
c
c        write(6,748) t,etas,eta,rl,f,dfdt
c 748    format('  t,etas,eta,rl,f,dfdt:  ',3x,6(e12.5))
c        write(6,749) i,t,sm1,sm2,sm3,sm4,sm
c 749    format('i,t,sm1,2,3,4,sm: ',i2,1x,6(e12.5))
 
         t2 = t - f/dfdt
   99 continue
c
      return
      end
      subroutine pprint(lulog,ilab,tsec,zp,pp,rhop,up,pmass,rp,
     +                  t1,t2,tp,te,tvp,tve,wvp,wsp,wve,wcp,wce,sp,se)
c
c     This routine prints the parcel and environmental variables
c     at a single time
c
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Unit conversions for printing
      ppw = pp/100.0
c
      t1w  = t1 -tck
      t2w  = t2 -tck
      tpw  = tp -tck
      tew  = te -tck
      tvpw = tvp-tck
      tvew = tve-tck
c
      wvpw = wvp*1000.0
      wvew = wve*1000.0
      wcpw = wcp*1000.0
      wcew = wce*1000.0
c
      wspw = wsp*1000.0
c
      if (ilab .eq. 1) then
         write(lulog,100) 
  100    format(/,'   t       z     P     rhop    u      M         Rp',
     +            '     T1     T2     Tp     Te    Tvp    Tve',
     +            '    wvp    wsp    wve    wcp    wce     Sp     Se')
      endif
c
      write(lulog,300) tsec,zp,ppw,rhop,up,pmass,rp,
     +                 t1w,t2w,tpw,tew,tvpw,tvew,
     +                 wvpw,wspw,wvew,wcpw,wcew,sp,se
  300 format(f6.1,1x,f6.0,1x,f6.1,1x,f6.2,1x,f6.1,1x,e10.3,1x,f6.1,1x,
     +       6(f6.1,1x),
     +       5(f6.1,1x),2(f6.1,1x))
c
      return
      end
      subroutine ttcal(tvp,tve,wvp,wcp,we,up,rp,pmass,sp,se,
     +                 upt,pmasst,wpt,spt,zpt)
c
c     This routine calculates the time tendency of the 5 prognostic variables
c     of the cloud model:
c
c     upt:    Vertical velocity tendency
c     pmasst: Parcel total mass tendency
c     wpt:    Parcel total water mixing ratio
c     dpt:    Parcel entropy mixing ratio tendency
c     zpt:    Parcel height tendency
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Physical factor flags
      common /pflag/ iice,icweight
c
c     ++ Preliminary calculations
      if (rp .le. 0.0) then
         ri = 0.0
      else
         ri = 1.0/rp
      endif
c
      etfac = abs(up)*ce*ri
c
c     ++ upt calculation
      f1 = (tvp-tve)/tve
c
      if (icweight .eq. 1) then
         f2 = wcp/(1.0+wvp)
      else
         f2 = 0.0
      endif
c
      upt    = g*( (f1-f2)/(1.0+f2) ) - (ce+cd)*up*up*ri
c
c     ++ pmasst calculation
      pmasst = etfac*pmass
c
c     ++ wpt calculation
      wp     = wvp+wcp
      wpt    = etfac*(we-wp) - alpha*wcp
c
c     ++ spt calculation
      spt = etfac*(se-sp)
c
c     ++ zpt calculation
      zpt = up
c
c     write(6,*) 'upt,pmasst,wpt,spt,zpt',upt,pmasst,wpt,spt,zpt
      return
      end
      subroutine vsave(nsave,tsec,zp,pp,rhop,up,rp,tp,te,tvp,tve,
     +                 wvp,wsp,wve,wcp)
c     This routine saves the primary parcel and environmental variables
c     as a function of time for later interpolation to an evenly spaced
c     vertical grid. 
c
c     Arrays for evenly spaced output grid
      parameter (mto=10000,mzo=1000)
      dimension tto(mto),zto(mto),pto(mto),rhoto(mto),uto(mto),rto(mto)
      dimension tpto(mto),teto(mto),tvpto(mto),tveto(mto)
      dimension wvpto(mto),wspto(mto),wveto(mto),wcpto(mto)
      common /tov/ tto,zto,pto,rhoto,uto,rto,tpto,teto,tvpto,tveto,
     +             wvpto,wspto,wveto,wcpto
c
      n = nsave
c
      tto(n)   = tsec
      zto(n)   = zp
      pto(n)   = pp
      rhoto(n) = rhop
      uto(n)   = up
      rto(n)   = rp
      tpto(n)  = tp
      teto(n)  = te
      tvpto(n) = tvp
      tveto(n) = tve
      wvpto(n) = wvp
      wspto(n) = wsp
      wveto(n) = wve
      wcpto(n) = wcp
c
      return
      end
      subroutine vezdat(ludat,ntmax,dzo,dzmax,nzo,iprtx)
c     This routine prints the primary variables as a function of z
c     on an evenly spaced grid.
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
c     Arrays for evenly spaced output grid
      parameter (mto=10000,mzo=1000)
      dimension tto(mto),zto(mto),pto(mto),rhoto(mto),uto(mto),rto(mto)
      dimension tpto(mto),teto(mto),tvpto(mto),tveto(mto)
      dimension wvpto(mto),wspto(mto),wveto(mto),wcpto(mto)
      common /tov/ tto,zto,pto,rhoto,uto,rto,tpto,teto,tvpto,tveto,
     +             wvpto,wspto,wveto,wcpto
c
      dimension tzo(mto),zzo(mto),pzo(mto),rhozo(mto),uzo(mto),rzo(mto)
      dimension tpzo(mto),tezo(mto),tvpzo(mto),tvezo(mto)
      dimension wvpzo(mto),wspzo(mto),wvezo(mto),wcpzo(mto)
      common /zov/ tzo,zzo,pzo,rhozo,uzo,rzo,tpzo,tezo,tvpzo,tvezo,
     +             wvpzo,wspzo,wvezo,wcpzo
c
c     Local variables
      dimension tdezo(mto),tdpzo(mto)
c
c     Calculate output z points
      nzo = 1 + ifix(0.001 + dzmax/dzo)
      do k=1,nzo
         zzo(k) = dzo*float(k-1)
      enddo
c
c     Initialize output variables to missing
      vmiss = 0.0
      do k=1,nzo
         tzo(k)   = vmiss
         pzo(k)   = vmiss
         rhozo(k) = vmiss
         uzo(k)   = vmiss
         rzo(k)   = vmiss
         tpzo(k)  = vmiss
         tezo(k)  = vmiss
         tvpzo(k) = vmiss
         tvezo(k) = vmiss
         wvpzo(k) = vmiss
         wspzo(k) = vmiss
         wvezo(k) = vmiss
         wcpzo(k) = vmiss
      enddo
c
c     Interpolate time values to z values
      do k=1,nzo
         z = zzo(k)
c
         call ttoz(uto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) uzo(k) = fz
c
         call ttoz(pto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) pzo(k) = fz
c
         call ttoz(tpto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) tpzo(k) = fz - tck
c
         call ttoz(teto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) tezo(k) = fz - tck
c
         call ttoz(tvpto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) tvpzo(k) = fz - tck
c
         call ttoz(tveto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) tvezo(k) = fz - tck
c
         call ttoz(rto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) rzo(k) = fz
c
         call ttoz(rhoto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) rhozo(k) = fz
c
         call ttoz(wvpto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) wvpzo(k) = fz
c
         call ttoz(wveto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) wvezo(k) = fz
c
         call ttoz(wcpto,zto,ntmax,z,fz,ierr)
         if (ierr .eq. 0) wcpzo(k) = fz
c
      enddo
c
c     Calculate dewpoint temperature of environment
      do k=1,nzo
         ttmp = tezo(k)+tck
         ptmp = pzo(k)
         wtmp = wvezo(k)
c
         call tdcal(ptmp,ttmp,wtmp,tdtmp)
c
         tdezo(k) = tdtmp-273.15
      enddo
c
c     Calculate dewpoint temperature of parcel
      do k=1,nzo
         ttmp = tpzo(k)+tck
         ptmp = pzo(k)
         wtmp = wvpzo(k)
c
         call tdcal(ptmp,ttmp,wtmp,tdtmp)
c
         tdpzo(k) = tdtmp-273.15
      enddo
c
      if (iprtx .ne. 0) then
c        Open the output file
         open(file='lcmod.dat',unit=ludat,form='formatted',
     +        status='replace')
c
c        Write output file 
         write(ludat,100)
  100    format('  z       P     RHOp    u     Rp    ',
     +          ' Tp     Te     Tvp    Tve    Tdp    Tde   wvp    wve',
     +           '    wcp')
c
         do k=nzo,1,-1
            write(ludat,110) zzo(k)/1000.0,pzo(k)/100.0,rhozo(k),uzo(k),
     +                       rzo(k),tpzo(k),tezo(k),tvpzo(k),tvezo(k),
     +                     tdpzo(k),tdezo(k),wvpzo(k)*1000.0,
     +                     wvezo(k)*1000.0,wcpzo(k)*1000.0
  110       format(f6.2,1x,f6.1,1x,f6.3,1x,8(f6.1,1x),3(f6.2,1x))
         enddo
c
         close(ludat)
      endif
c
      return
      end
      subroutine ttoz(ft,zt,ntmax,z,fz,ierr)
c     This routine finds a function value (fz) at the given value of
c     z by linearly interpolating between the points in the function ft.
c     The two values to interpolate from are determined from the 
c     z as a function of t (zt). 
c     
c     If z is outside of the range of zt,
c     fz is set to zero and ierr=1. 
c     
      dimension ft(ntmax),zt(ntmax)
c
c     Search for the interval of ft in which z lies. 
      do k=1,ntmax-1
         if (z .ge. zt(k) .and. z .le. zt(k+1)) then
            k1 = k
            k2 = k+1
            go to 2000
         endif
      enddo
c
c     If you get to here the z value was outside the range of zt.
      ierr = 1
      return
c
 2000 continue
      ierr = 0
c
      z1 = zt(k1)
      z2 = zt(k2)
      f1 = ft(k1)
      f2 = ft(k2)
      if (z1 .eq. z2) then
         fz = f1
      else
         w1 = (z2-z)/(z2-z1)
         w2 = (z-z1)/(z2-z1)
         fz = w1*f1 + w2*f2
      endif
c      
      return
      end
      subroutine avmf(nzo,zzo,uzo,rhozo,tvp,tve,vvavg,vmflux,cape,cin)
c     This routine calculates the vertically averaged vertical mass flux. 
c     The average vertical velocity (vvavg), CAPE and CIN are also calculated. 
c
      dimension zzo(nzo),uzo(nzo),rhozo(nzo)
      dimension tvp(nzo),tve(nzo)
c
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
      vmflux = 0.0
      vvavg  = 0.0
      do i=1,nzo
         vmflux = vmflux + rhozo(i)*uzo(i)
         vvavg  = vvavg  +          uzo(i)
      enddo
c
      if (nzo .ne. 0) then
         vmflux = vmflux/float(nzo)
         vvavg  = vvavg/float(nzo)
      endif
c
      cape = 0.0
      cin  = 0.0
      dz   = zzo(2)-zzo(1)
c
      icape=0
      icin =0
c
      do i=2,nzo
         bterm = g*(tvp(i)-tve(i))/(tve(i)+tck)
c
         if (bterm .gt. 0.0 .and. icape .eq. 0) icape = 1
         if (bterm .lt. 0.0 .and. icin  .eq. 0) icin  = 1
c
         if (icape .eq. 1) then
            cape = cape + dz*bterm 
         endif
c
         if (icin .eq. 1) then
            cin = cin + dz*abs(bterm)
         endif
c
         if (bterm .lt. 0.0 .and. icape .eq. 1) icape= -1
         if (bterm .gt. 0.0 .and. icin  .eq. 1) icin = -1
c
c        write(6,*) 'z,dt: ',zzo(i),tvp(i)-tve(i)
      enddo
c
      return
      end
      subroutine tdcal(p,t,w,td)
c     This routine calculated the dew point temperature (td in K)
c     given the pressure (p in Pa), temperature (t in K) and
c     mixing ratio (w in kg/kg).
c
c     Physical and numerical constants
      common /pncon/ pi,g,ra,cpa,cva,rv,cpv,cvv,tck,tf,dtf,ce,cd,alpha
c
      dt = 0.05
      tmin = -100.0+tck
      td   = tmin
c
      do i=-1,2000
         t1 = t-dt*float(i)
         t2 = t1-dt
c        if (t1 .le. tmin) return
c
         call escal(t1,es,des,d2es,rl)
         ws1 = ra*es/(rv*(p-es))
c
         call escal(t2,es,des,d2es,rl)
         ws2 = ra*es/(rv*(p-es))
c
         if (ws1 .ge. w .and. ws2 .lt. w) then
            td = t1
            return
         endif
      enddo
c
      return
      end
      subroutine ir00param(ibasin,lat,rsst,vmax,shdc,delv,t200,
     +                     d200,tspd,rmiss,goes00,ierr)
c      
c-----------------------------------------------------------------------      
c     This is a subroutine of the SHIPS model.
c
c     This program calculates the GOES parameters currently used in
c     SHIPS from various synoptic predictors.  This is for use when
c     GOES satellite imagery is not available.
c
c
c     Inputs: ibasin - 1 for Atlantic, 2 for E. Pacific
c             lat    - Storm latitude (deg N) at t=0h
c             rsst   - Reynold's SST (deg C) at t=0h
c             vmax   - Maximum winds (kt) at t=0h
c             shdc   - 850-200 mb corrected shear magnitude (kt) at t=0h
c             delv   - Intensity change (kt) from t=-12h to 0h
c             t200   - 200 to 800km area average 200mb temperature (deg C) at t=0h
c             d200   - 200mb divergence for r=0-1000km (sec-1*10^7) at t=0h
c             tspd   - Storm translational speed (kt) at t=0h
c             rmiss  - default value for missing data (currently 9999.)
c
c     Output: 
c             goes00  - Array containing the 16 goes00 parameters (1-16)
c             ierr    - error flag =0 for normal completion
c                                  =1 one or more predictors missing  
c
c     Created April 2009 by A. Schumacher, CIRA/CSU
c    
c----------------------------------------------------------------------- 
c
c     Number of predictors
      parameter    (nvar=9)
c
c     Input predictors
      real         lat,rsst,vmax,shdc,delv,t200,d200,tspd 
      dimension    pvar(nvar)
c
c     Output GOES parameters
      real         goes00(16)     
c
c     Atlantic arrays
      dimension    mna(nvar)	! Predictor means
      dimension    sda(nvar)	! Predictor standard deviations
      dimension    cfa01(nvar)	! Normalized predictor coefficients, goes00(1)
      dimension    cfa02(nvar)	! Normalized predictor coefficients, goes00(2)
      dimension    cfa03(nvar)	! Normalized predictor coefficients, goes00(3)
      dimension    cfa04(nvar)	! Normalized predictor coefficients, goes00(4)
      dimension    cfa05(nvar)	! Normalized predictor coefficients, goes00(5)
      dimension    cfa06(nvar)	! Normalized predictor coefficients, goes00(6)
      dimension    cfa07(nvar)	! Normalized predictor coefficients, goes00(7)
      dimension    cfa08(nvar)	! Normalized predictor coefficients, goes00(8)
      dimension    cfa09(nvar)	! Normalized predictor coefficients, goes00(9)
      dimension    cfa10(nvar)	! Normalized predictor coefficients, goes00(10)
      dimension    cfa11(nvar)	! Normalized predictor coefficients, goes00(11)
      dimension    cfa12(nvar)	! Normalized predictor coefficients, goes00(12)
      dimension    cfa13(nvar)	! Normalized predictor coefficients, goes00(13)
      dimension    cfa14(nvar)	! Normalized predictor coefficients, goes00(14)
      dimension    cfa15(nvar)	! Normalized predictor coefficients, goes00(15)
      dimension    cfa16(nvar)	! Normalized predictor coefficients, goes00(16)
c 
c     E Pacific arrays           
      dimension    mnp(nvar)	! Predictor means
      dimension    sdp(nvar)	! Predictor standard deviations
      dimension    cfp01(nvar)	! Normalized predictor coefficients, goes00(1)
      dimension    cfp02(nvar)	! Normalized predictor coefficients, goes00(2)
      dimension    cfp03(nvar)	! Normalized predictor coefficients, goes00(3)
      dimension    cfp04(nvar)	! Normalized predictor coefficients, goes00(4)
      dimension    cfp05(nvar)	! Normalized predictor coefficients, goes00(5)
      dimension    cfp06(nvar)	! Normalized predictor coefficients, goes00(6)
      dimension    cfp07(nvar)	! Normalized predictor coefficients, goes00(7)
      dimension    cfp08(nvar)	! Normalized predictor coefficients, goes00(8)
      dimension    cfp09(nvar)	! Normalized predictor coefficients, goes00(9)
      dimension    cfp10(nvar)	! Normalized predictor coefficients, goes00(10)
      dimension    cfp11(nvar)	! Normalized predictor coefficients, goes00(11)
      dimension    cfp12(nvar)	! Normalized predictor coefficients, goes00(12)
      dimension    cfp13(nvar)	! Normalized predictor coefficients, goes00(13)
      dimension    cfp14(nvar)	! Normalized predictor coefficients, goes00(14)
      dimension    cfp15(nvar)	! Normalized predictor coefficients, goes00(15)
      dimension    cfp16(nvar)	! Normalized predictor coefficients, goes00(16)
c     
c
c----------------------------------------------------------------------- 
c     ATLANTIC BASIN: 
c----------------------------------------------------------------------- 
c     Predictor means and standard deviations
c                 LAT  RSST  VMAX  SHDC  DELV  T200  D200  TSPD  VMAX^2
      data mna / 24.9, 27.4, 59.4, 17.3,  2.6,-53.2, 24.5,  5.5, 4206.4/
      data sda /  8.3,  2.0, 26.1, 10.4,  9.3,  1.7, 33.3,  3.2, 3870.0/
  
c     Model for goes00( 1):
      data mna01 /-35.9/
      data sda01 / 22.7/
      data cfa01 / 0.28,-0.09,-1.51, 0.18,-0.10,-0.04,-0.08,-0.10, 1.05/
c     Variance explained by model:  56.65%
  
c     Model for goes00( 2):
      data mna02 / 15.6/
      data sda02 /  6.8/
      data cfa02 / 0.10, 0.16,-0.51, 0.13,-0.02,-0.09, 0.02,-0.02, 0.06/
c     Variance explained by model:  26.02%
  
c     Model for goes00( 3):
      data mna03 /-27.3/
      data sda03 / 18.3/
      data cfa03 / 0.22,-0.08,-1.12, 0.15,-0.06,-0.10,-0.17,-0.09, 0.61/
c     Variance explained by model:  61.16%
  
c     Model for goes00( 4):
      data mna04 / 20.8/
      data sda04 /  7.1/
      data cfa04 / 0.05, 0.29,-0.18, 0.22, 0.02,-0.14, 0.04, 0.04,-0.30/
c     Variance explained by model:  32.18%
  
c     Model for goes00( 5):
      data mna05 / 71.3/
      data sda05 / 28.1/
      data cfa05 /-0.21, 0.03, 1.57,-0.25, 0.06, 0.05, 0.09, 0.10,-1.12/
c     Variance explained by model:  54.36%
  
c     Model for goes00( 6):
      data mna06 / 64.9/
      data sda06 / 29.3/
      data cfa06 /-0.21, 0.07, 1.49,-0.23, 0.07, 0.04, 0.08, 0.11,-0.99/
c     Variance explained by model:  56.80%
  
c     Model for goes00( 7):
      data mna07 / 58.3/
      data sda07 / 29.8/
      data cfa07 /-0.20, 0.10, 1.36,-0.19, 0.07, 0.03, 0.08, 0.11,-0.83/
c     Variance explained by model:  58.63%
  
c     Model for goes00( 8):
      data mna08 / 50.8/
      data sda08 / 29.7/
      data cfa08 /-0.20, 0.14, 1.19,-0.15, 0.07, 0.02, 0.08, 0.11,-0.64/
c     Variance explained by model:  59.82%
  
c     Model for goes00( 9):
      data mna09 / 40.2/
      data sda09 / 28.7/
      data cfa09 /-0.20, 0.18, 0.87,-0.09, 0.08, 0.04, 0.07, 0.10,-0.31/
c     Variance explained by model:  59.13%
  
c     Model for goes00(10):
      data mna10 / 25.1/
      data sda10 / 24.5/
      data cfa10 /-0.24, 0.17, 0.32,-0.01, 0.10, 0.09, 0.07, 0.05, 0.17/
c     Variance explained by model:  53.59%
  
c     Model for goes00(11):
      data mna11 /-33.9/
      data sda11 / 31.8/
      data cfa11 / 0.30,-0.10,-1.81, 0.12,-0.07,-0.02,-0.05,-0.12, 1.73/
c     Variance explained by model:  31.23%
  
c     Model for goes00(12):
      data mna12 /-38.0/
      data sda12 / 30.7/
      data cfa12 / 0.31,-0.11,-1.73, 0.13,-0.08,-0.01,-0.06,-0.11, 1.56/
c     Variance explained by model:  34.24%
  
c     Model for goes00(13):
      data mna13 / 15.2/
      data sda13 / 11.1/
      data cfa13 /-0.09, 0.05, 0.59,-0.05, 0.01,-0.01, 0.03, 0.05,-0.75/
c     Variance explained by model:   5.55%
  
c     Model for goes00(14):
      data mna14 /-47.0/
      data sda14 / 25.6/
      data cfa14 / 0.28,-0.09,-1.53, 0.19,-0.10,-0.01,-0.05,-0.08, 1.11/
c     Variance explained by model:  50.15%
  
c     Model for goes00(15):
      data mna15 /-39.1/
      data sda15 / 25.4/
      data cfa15 / 0.29,-0.08,-1.52, 0.18,-0.10,-0.02,-0.05,-0.10, 1.08/
c     Variance explained by model:  53.30%
  
c     Model for goes00(16):
      data mna16 / 57.9/
      data sda16 / 36.0/
      data cfa16 / 0.22,-0.07,-1.13, 0.09,-0.06, 0.06,-0.01,-0.06, 1.14/
c     Variance explained by model:  12.48%
c
c-----------------------------------------------------------------------
c     EAST PACIFIC BASIN:
c-----------------------------------------------------------------------
c     Predictor means and standard deviations
c                 LAT  RSST  VMAX  SHDC  DELV  T200  D200  TSPD  VMAX^2
      data mnp / 16.8, 27.1, 55.2, 13.4,  0.7,-52.2, 20.2,  4.5, 3768.2/
      data sdp /  3.7,  1.9, 26.9,  8.2, 10.9,  0.9, 30.8,  2.0, 3758.7/
  
c     Model for goes00( 1):
      data mnp01 /-37.4/
      data sdp01 / 24.9/
      data cfp01 / 0.15,-0.34,-1.50, 0.10,-0.16,-0.03,-0.09,-0.08, 1.12/
c     Variance explained by model:  67.75%
  
c     Model for goes00( 2):
      data mnp02 / 13.4/
      data sdp02 /  6.3/
      data cfp02 / 0.00, 0.25, 0.07, 0.02,-0.16,-0.10,-0.03,-0.02,-0.31/
c     Variance explained by model:  13.15%
  
c     Model for goes00( 3):
      data mnp03 /-26.0/
      data sdp03 / 20.6/
      data cfp03 / 0.15,-0.31,-1.07, 0.06,-0.18,-0.08,-0.18,-0.10, 0.73/
c     Variance explained by model:  66.21%
  
c     Model for goes00( 4):
      data mnp04 / 17.4/
      data sdp04 /  6.6/
      data cfp04 /-0.03, 0.35, 0.41, 0.12,-0.11,-0.12, 0.01,-0.01,-0.60/
c     Variance explained by model:  19.31%
  
c     Model for goes00( 5):
      data mnp05 / 71.0/
      data sdp05 / 32.2/
      data cfp05 /-0.14, 0.32, 1.50,-0.15, 0.11, 0.04, 0.10, 0.07,-1.11/
c     Variance explained by model:  65.13%
  
c     Model for goes00( 6):
      data mnp06 / 64.1/
      data sdp06 / 33.2/
      data cfp06 /-0.14, 0.31, 1.37,-0.11, 0.15, 0.03, 0.11, 0.07,-0.96/
c     Variance explained by model:  66.90%
  
c     Model for goes00( 7):
      data mnp07 / 57.1/
      data sdp07 / 33.1/
      data cfp07 /-0.14, 0.30, 1.22,-0.08, 0.18, 0.03, 0.11, 0.08,-0.80/
c     Variance explained by model:  67.21%
  
c     Model for goes00( 8):
      data mnp08 / 49.4/
      data sdp08 / 32.0/
      data cfp08 /-0.14, 0.30, 1.05,-0.05, 0.20, 0.03, 0.12, 0.09,-0.62/
c     Variance explained by model:  65.95%
  
c     Model for goes00( 9):
      data mnp09 / 39.2/
      data sdp09 / 29.5/
      data cfp09 /-0.13, 0.29, 0.79,-0.01, 0.21, 0.04, 0.12, 0.09,-0.38/
c     Variance explained by model:  61.35%
  
c     Model for goes00(10):
      data mnp10 / 25.3/
      data sdp10 / 24.2/
      data cfp10 /-0.11, 0.26, 0.47, 0.04, 0.23, 0.05, 0.13, 0.10,-0.15/
c     Variance explained by model:  49.45%
  
c     Model for goes00(11):
      data mnp11 /-38.9/
      data sdp11 / 32.9/
      data cfp11 / 0.13,-0.34,-1.88, 0.09,-0.11,-0.01,-0.04,-0.06, 1.79/
c     Variance explained by model:  46.79%
  
c     Model for goes00(12):
      data mnp12 /-42.4/
      data sdp12 / 32.0/
      data cfp12 / 0.13,-0.34,-1.80, 0.10,-0.12, 0.01,-0.05,-0.06, 1.63/
c     Variance explained by model:  50.13%
  
c     Model for goes00(13):
      data mnp13 / 14.9/
      data sdp13 / 10.4/
      data cfp13 / 0.00, 0.17, 0.64,-0.05,-0.03, 0.00, 0.00, 0.00,-0.81/
c     Variance explained by model:   7.52%
  
c     Model for goes00(14):
      data mnp14 /-49.3/
      data sdp14 / 28.4/
      data cfp14 / 0.13,-0.35,-1.58, 0.13,-0.13, 0.00,-0.05,-0.06, 1.20/
c     Variance explained by model:  63.61%
  
c     Model for goes00(15):
      data mnp15 /-41.9/
      data sdp15 / 27.5/
      data cfp15 / 0.14,-0.33,-1.53, 0.11,-0.16,-0.01,-0.06,-0.07, 1.14/
c     Variance explained by model:  65.83%
  
c     Model for goes00(16):
      data mnp16 / 53.3/
      data sdp16 / 33.4/
      data cfp16 / 0.09,-0.25,-1.27, 0.10,-0.04, 0.06, 0.02,-0.02, 1.22/
c     Variance explained by model:  20.70%
c
c     Scale factors for GOES predictors
      dimension sfac(16)
      data sfac /10.0,10.0,10.0,10.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
     +           10.0,10.0, 1.0,10.0,10.0, 1.0/ 
c     
c     Max/Min caps - constrains predicted parameters to reasonable
c     values based on parameter properties and observed max/min
      dimension cmax(16)
      data cmax / 30.0, 45.0, 30.0, 45.0,100.0,100.0,100.0,100.0,
     +           100.0,100.0, 30.0, 30.0, 30.0, 30.0, 30.0,120.0 /
      dimension cmin(16)
      data cmin /-90.0,  0.0,-90.0,  0.0,  0.0,  0.0,  0.0,  0.0,
     +             0.0,  0.0,-90.0,-90.0,  0.0,-90.0,-90.0, 20.0 /
c
c-----------------------------------------------------------------------
c
      ierr = 0
c
      pvar(1) = lat
      pvar(2) = rsst
      pvar(3) = vmax
      pvar(4) = shdc
      pvar(5) = delv
      pvar(6) = t200
      pvar(7) = d200
      pvar(8) = tspd
      pvar(9) = vmax*vmax
c
      do i=1,nvar
         if (pvar(i) .eq. rmiss) goto 9800
      enddo
      
      sumv01 = 0.0
      sumv02 = 0.0
      sumv03 = 0.0
      sumv04 = 0.0
      sumv05 = 0.0
      sumv06 = 0.0
      sumv07 = 0.0
      sumv08 = 0.0
      sumv09 = 0.0
      sumv10 = 0.0
      sumv11 = 0.0
      sumv12 = 0.0
      sumv13 = 0.0
      sumv14 = 0.0
      sumv15 = 0.0
      sumv16 = 0.0
      
      if (ibasin .eq. 1) then
         do i=1,nvar
	    sumv01 = sumv01 + cfa01(i)*((pvar(i) - mna(i))/sda(i))
	    sumv02 = sumv02 + cfa02(i)*((pvar(i) - mna(i))/sda(i))
	    sumv03 = sumv03 + cfa03(i)*((pvar(i) - mna(i))/sda(i))
	    sumv04 = sumv04 + cfa04(i)*((pvar(i) - mna(i))/sda(i))
	    sumv05 = sumv05 + cfa05(i)*((pvar(i) - mna(i))/sda(i))
	    sumv06 = sumv06 + cfa06(i)*((pvar(i) - mna(i))/sda(i))
	    sumv07 = sumv07 + cfa07(i)*((pvar(i) - mna(i))/sda(i))
	    sumv08 = sumv08 + cfa08(i)*((pvar(i) - mna(i))/sda(i))
	    sumv09 = sumv09 + cfa09(i)*((pvar(i) - mna(i))/sda(i))
	    sumv10 = sumv10 + cfa10(i)*((pvar(i) - mna(i))/sda(i))
	    sumv11 = sumv11 + cfa11(i)*((pvar(i) - mna(i))/sda(i))
	    sumv12 = sumv12 + cfa12(i)*((pvar(i) - mna(i))/sda(i))
	    sumv13 = sumv13 + cfa13(i)*((pvar(i) - mna(i))/sda(i))
	    sumv14 = sumv14 + cfa14(i)*((pvar(i) - mna(i))/sda(i))
	    sumv15 = sumv15 + cfa15(i)*((pvar(i) - mna(i))/sda(i))
	    sumv16 = sumv16 + cfa16(i)*((pvar(i) - mna(i))/sda(i))
	 enddo
	 goes00(1)  = mna01 + (sumv01*sda01)
	 goes00(2)  = mna02 + (sumv02*sda02)
	 goes00(3)  = mna03 + (sumv03*sda03)
	 goes00(4)  = mna04 + (sumv04*sda04)
	 goes00(5)  = mna05 + (sumv05*sda05)
	 goes00(6)  = mna06 + (sumv06*sda06)
	 goes00(7)  = mna07 + (sumv07*sda07)
	 goes00(8)  = mna08 + (sumv08*sda08)
	 goes00(9)  = mna09 + (sumv09*sda09)
	 goes00(10) = mna10 + (sumv10*sda10)
	 goes00(11) = mna11 + (sumv11*sda11)
	 goes00(12) = mna12 + (sumv12*sda12)
	 goes00(13) = mna13 + (sumv13*sda13)
	 goes00(14) = mna14 + (sumv14*sda14)
	 goes00(15) = mna15 + (sumv15*sda15)
	 goes00(16) = mna16 + (sumv16*sda16)
      elseif (ibasin .eq. 2) then
         do i=1,nvar
	    sumv01 = sumv01 + cfp01(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv02 = sumv02 + cfp02(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv03 = sumv03 + cfp03(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv04 = sumv04 + cfp04(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv05 = sumv05 + cfp05(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv06 = sumv06 + cfp06(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv07 = sumv07 + cfp07(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv08 = sumv08 + cfp08(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv09 = sumv09 + cfp09(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv10 = sumv10 + cfp10(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv11 = sumv11 + cfp11(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv12 = sumv12 + cfp12(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv13 = sumv13 + cfp13(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv14 = sumv14 + cfp14(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv15 = sumv15 + cfp15(i)*((pvar(i) - mnp(i))/sdp(i))
	    sumv16 = sumv16 + cfp16(i)*((pvar(i) - mnp(i))/sdp(i))
	 enddo
	 goes00(1)  = mnp01 + (sumv01*sdp01)
	 goes00(2)  = mnp02 + (sumv02*sdp02)
	 goes00(3)  = mnp03 + (sumv03*sdp03)
	 goes00(4)  = mnp04 + (sumv04*sdp04)
	 goes00(5)  = mnp05 + (sumv05*sdp05)
	 goes00(6)  = mnp06 + (sumv06*sdp06)
	 goes00(7)  = mnp07 + (sumv07*sdp07)
	 goes00(8)  = mnp08 + (sumv08*sdp08)
	 goes00(9)  = mnp09 + (sumv09*sdp09)
	 goes00(10) = mnp10 + (sumv10*sdp10)
	 goes00(11) = mnp11 + (sumv11*sdp11)
	 goes00(12) = mnp12 + (sumv12*sdp12)
	 goes00(13) = mnp13 + (sumv13*sdp13)
	 goes00(14) = mnp14 + (sumv14*sdp14)
	 goes00(15) = mnp15 + (sumv15*sdp15)
	 goes00(16) = mnp16 + (sumv16*sdp16)
      else
         goto 9800
      endif	 
c
c
c     Apply max/min caps to parameters
c
      do i=1,16
         if (goes00(i) .lt. cmin(i)) goes00(i) = cmin(i)
	 if (goes00(i) .gt. cmax(i)) goes00(i) = cmax(i)
      enddo
c
c     Apply scale factors
      do i=1,16
         goes00(i) = goes00(i)*sfac(i)
      enddo
c
      return

c     Error processing
 9800 ierr = 1
      do i=1,16
         goes00(i) = rmiss
      enddo
    
      return     
c
      end
      subroutine bassel(rlat,rlon,ibasin)
c     This routine determines which basin a given 
c     lat/lon point is in
c
c     Input: 
c       rlat - latitude deg N
c       rlon - longitude deg E (0-360 convention)
c 
c     Output
c       ibasin = 1 for Atlantic
c              = 2 for east Pacific
c              = 3 for west Pacific
c              = 4 for south Pacific
c              = 5 for Indian Ocean 
c
      ibasin = 1
      if     (rlat                      .ge.  0.0) then
      if     (rlat                      .le.  8.0) then
        if (rlon .lt.  285.0) ibasin=2
      elseif (rlat .gt.  8.0 .and. rlat .le. 15.0) then
        if (rlon .lt.  275.0) ibasin=2
      elseif (rlat .gt. 15.0 .and. rlat .le. 17.5) then
        if (rlon .lt.  270.0) ibasin=2
      elseif (rlat .gt. 17.5                     ) then
         if (rlon .lt.  260.0) ibasin=2
      endif
      endif
c
      if ((rlon .lt. 180.0) .and. (rlat .ge. 0.0))  ibasin=3
c
      if ((rlon .lt. 280.0) .and. (rlat .lt. 0.0))  ibasin=4
c
      if (rlon .lt. 100.0) ibasin=5
      
      return
      end
      subroutine virt(t,p,rh,tv)
c     This routine calculates the virtual temperature
c     given the temperature, pressure and relative humidity
c           input:  t  = temperature (C)
c                   p  = pressure (mb)
c                   rh = relative humidity (%)
c           output: tv = virtual temperature (C)
c
c     Check input
      if (t .lt. -273.15 .or. p .gt. 1050. .or. p .lt. 10.0
     +                   .or. rh .gt. 100.0 .or. rh .lt. 0.) then
         tv = 0.0
         return
      endif
c
c     Specify constants
      tcon  = 273.15
      epsil = 0.622
c
c     Convert input to mks units
      tk = t + tcon
      pp = 100.0*p
      rhr = rh/100.0
c
c     Calculate saturation vapor pressure
      call teten(tk,es)
c
c     Calculate vapor pressure
      ws = es*epsil/(pp-es)
      w  = rhr*ws
      e  = w*pp/(w+epsil)
c
c     Calculate virtual temperature and convert back to Celsius
      tv = tk/( 1.0 -(e/pp)*(1.0-epsil) )
      tv = tv - tcon
c
      return
      end
      subroutine virti(tv,p,rh,t)
c     This routine calculates the temperature
c     given the virtual temperature, pressure and relative humidity.
c     A simple iteration method is used for the calculation.
c           input:  tv = virtual temperature (C)
c                   p  = pressure (mb)
c                   rh = relative humidity (%)
c           output: t  = virtual temperature (C)
c
c     Check input
      if (tv .lt. -273.15 .or. p .gt. 1050. .or. p .lt. 10.0
     +                    .or. rh .gt. 100.0 .or. rh .lt. 0.) then
         tv = 0.0
         return
      endif
c
c     Specify constants
      tcon  = 273.15
      epsil = 0.622
c
c     Convert input to mks units
      tvk = tv + tcon
      pp = 100.0*p
      rhr = rh/100.0
c
c     Make first guess for the temperature
      tk = tvk
c
c     Iterate to fine the actual temperature
      nit = 5
      do 10 i=1,nit
c        Calculate saturation vapor pressure
         call teten(tk,es)
c
c        Calculate vapor pressure
         ws = es*epsil/(pp-es)
         w  = rhr*ws
         e  = w*pp/(w+epsil)
c
c        Calculate temperature 
         tk = tvk*( 1.0 -(e/pp)*(1.0-epsil) )
c        write(6,*) '    ',i,tk
   10 continue
c
c     Convert temperature to Celsius
      t = tk - tcon
c
      return
      end
      subroutine teten(tk,es)
c     This routine calculates the saturation vapor pressure using
c     Teten's formula
c          input:  tk = temperature (K)
c          output: es = saturation vapor pressure (Pa)
c
c     Check for valid temperature
      if (tk .lt. 40.0) then
         es = 0.0
         return
      endif
c
      c1 = 610.78
      c2 = 17.269
      c3 = 35.86 
c
      es = c1*exp( c2*(tk-273.16)/(tk-35.86) )
c
      return
      end
      subroutine parsub(pb,tb,rhb,dp,pmin,iadj,mxd,psat,pp,tp,tvp,npp)
c     This program calculates temperature/pressure profiles
c     for parcels lifted under various assumptions. The thermodynamic
c     formulation described by Ooyama (1990) is used for
c     the calculations. The ice phase is not included in the calculations.
c 
c     Input: 
c            pb     = boundary layer pressure (Pa)
c            tb     = boundary layer temperature (K)
c            rhb    = boundary layer relative humidity (%)
c            dp     = Pressure increment for profile (Pa)
c            pmin   = Minimum pressure of profile (Pa)
c            iadj   = 0 to carry liquid water
c                   = 1 to remove liquid water as it condenses
c            mxd    = Maximum dimension of the pp,tp,tvp arrays
c
c     Output: 
c            psat   = Pressure (Pa) where parcel first becomes saturated
c            pp     = Pressure profile (Pa)
c            tp     = Temperature profile (K)
c            tvp    = Virtual temperature profile
c            npp    = No. of points in pressure profile
c
      dimension pp(mxd),tp(mxd),tvp(mxd)
c
      common /gc/ ra,rv,cpa,cpv,cva,cvv,cck
      common /rs/ t0,p0,z0,e0,etas0,cl0
      common /sc/ a,d0,d1,d2
c
c     Specify number of iterations for the pressure loop
      nit = 10
c
c     Specify gas constants and conversion from C to K (mks units)
      ra  = 287.0
      rv  = 462.5
      cpa = 1005.7
      cpv = 1875.0
      cva = cpa - ra
      cvv = cpv - rv
      cck = 273.15
      eps = ra/rv
c
c     Specify constants for saturation vapor pressure equation
      a  = 611.2
      d0 = 17.67
      d1 = 273.15
      d2 = 29.65
c
c     Specify reference state temperature and dry air pressure
      t0 = 273.15
      p0 = 1000.0e+2
c
c     Calculate dry air density of the reference state
      z0 = p0/(ra*t0)
c
c     Calculate saturation vapor pressure and density of reference state
      call esat(t0,e0,de0,d2e0)
      etas0 = e0/(rv*t0)
c
c     Calculate lambda of the reference state
      cl0 = rv*t0*de0/e0
c
c     Set initial value of condensate to zero
      etac = 0.0
c
c     Calculate saturation vapor pressure and saturation
c     vapor density of parcel
      call esat(tb,eb,deb,d2eb)
      etasb = eb/(rv*tb)
c
c     Calculate actual vapor density and vapor pressure of parcel
      etavb = rhb*etasb/100.0
      pvb   = etavb*rv*tb
c
c     Calculate dry air pressure and density of the parcel
      pab = pb - pvb
      zb  = pab/(ra*tb)
c
c     Calculate initial mixing ratio and saturation mixing ratio
      wb  = etavb/zb
      wsb = etasb/zb
c
c     Calculate initial condensate mixing ratio
      wc = etac/zb
c
c     Calculate dry air entropy
      call sacal(tb,zb,sab)
c
c     Calculate moisture entropy (saturated and unsaturated)
      call smcal(tb,etavb,sm1b,sm2b)
c
c     Calculate entropy density
      sg1b = zb*sab + etavb*sm1b
      sg2b = zb*sab + etavb*sm2b
c
      sb = sg1b/zb
c
c     Start the pressure loop
c
c     Initialize variables with those from the boundary layer
c     before starting the pressure loop
      pv = pvb
      t  = tb
      s  = sb
      w  = wb
c
      pp(1)  = pb
      tp(1)  = tb
      tvp(1) = tb*(1.0 + wb/eps)/(1.0 + wc + wb)
c
      psat = -100.0
      i    = 2
c
c     Start pressure loop with pressure to the nearest 10 mb. 
      p = 1000.0*float(ifix( (pb-1.0)/1000.0 ) )
c
 2000 continue
c
         pp(i) = p
c
c        Start iteration
         n   = 0
c
 1000    continue
            pa = p - pv
            z  = pa/(ra*t)
            eta = w*z
c
            call tcal(t,z,eta,s,t1,t2)
            t = t1
            if (t2 .gt. t1) t=t2
c
            call esat(t,e,des,d2es)
            etas = e/(rv*t)
            etac = eta - etas
            if (etac .lt. 0.0) etac=0.0
            etav = eta - etac
c
            ws = etas/z
            wc = etac/z
c
            wv = (w - wc)
c
            pv   = etav*rv*t
            rh   = etav/etas
c
            n = n+1
         if (n .lt. nit) go to 1000
c
c        Check for saturation pressure
         if (psat .lt. 0.0 .and. rh .gt. .999) psat = p
c
         if (iadj .eq. 1) then
c           Remove condensate as it forms
c           and adjust mixing ratio and entropy density accordingly
            if (etac .gt. 0.0) then
               etac = 0.0
               eta  = etas + etac
               w    = eta/z
c
               call sacal(t,z,sa)
               call smcal(t,eta,sm1,sm2)
c
c              Calculate entropy density
               sg = z*sa + eta*sm2
               s  = sg/z
            endif
         endif
c
c        Calculate virtual temperature
         tv = t*(1.0 + wv/eps)/(1.0 + wc + wv)
c
         tp(i)  = t
         tvp(i) = tv
c
         i = i+1
         p = p - dp
      if (p .ge. pmin .and. i .le. mxd) go to 2000
c
      npp = i-1
c
      return
      end
      subroutine esat(t,e,de,d2e)
c     This routine calculates the saturation vapor pressure
c     (e) in Pa and its first and second derivatives, given
c     the temperature (T) in K using eqn. (10) from Bolton
c     (1980), except that T is input in K rather than C.
c
      common /sc/ a,d0,d1,d2
c
      if (t .le. d2) then
         e   = 0.0
         de  = 0.0
         d2e = 0.0
      else
         e = a*exp(d0*(t-d1)/(t-d2))
         de  = e*d0*(d1-d2)/( (t-d2)*(t-d2) )
         d2e = de*de/e -2.0*de/(t-d2)
      endif
c
      return
      end
      subroutine sacal(t,z,sa)
c     This routine calculates the dry air entropy (sa) given
c     the temperature (K) and dry air density z (kg/m3).
c
      common /gc/ ra,rv,cpa,cpv,cva,cvv,cck
      common /rs/ t0,p0,z0,e0,etas0,cl0
c
      sa = cva*alog(t/t0) - ra*alog(z/z0)
c
      return
      end
      subroutine smcal(t,eta,sm1,sm2)
c     This routine calculates the entropy of the water substance
c     (sm1 and sm2) given the temperature (K) and moisture density
c     (kg/m3). sm1 is valid for unsaturated air and sm2 is valid
c     for saturated air.
c
      common /gc/ ra,rv,cpa,cpv,cva,cvv,cck
      common /rs/ t0,p0,z0,e0,etas0,cl0
c
      sm1 = cvv*alog(t/t0) - rv*alog(eta/etas0) + cl0
c
      call esat(t,e,de,d2e)
      etas = e/(rv*t)
c
      sm2 = cvv*alog(t/t0) - rv*t*de/e + cl0 - rv*alog(etas/etas0) +
     +      de/eta
c
      return
      end
      subroutine tcal(t,z,eta,s,t1,t2)
c     This routine inverts the definition of the entropy density
c     using Newton-Raphson iteration.
c
c     The necessary input is as follows:
c         t   = first guess temperature
c         z   = dry air density
c         eta = mass density of total moisture
c         s   = entropy density
c
c     There are two temperature outputs. The greater of the two
c     is the proper temperature. If t2 > t1 then the air is
c     saturated. If t1 > t2 then the air is not saturated.
c
      common /gc/ ra,rv,cpa,cpv,cva,cvv,cck
c
c     Specify the number of iterations
      nit = 10
c
c     Initialize t1 and t2 and counter
      t1 = t
      t2 = t
      n  = 0
c     
c     Start iteration
 1000 continue
c
c        Calculations for t1
         call sacal(t1,z,sa)
         call smcal(t1,eta,sm1,sm2)
c
         f = sa + eta*sm1/z - s
c
         dsadt1 = cva/t1
         dsmdt1 = cvv/t1
c
         dfdt1 = dsadt1 + eta*dsmdt1/z
c
         t1 = t1 - f/dfdt1
c
c        Calculations for t2
         call sacal(t2,z,sa)
         call smcal(t2,eta,sm1,sm2)
c
         f = sa + eta*sm2/z - s
c
         call esat(t2,e,de,d2e)
c
         dsadt2 = cva/t2
         dsmdt2 = cpv/t2  - (rv*de/e)*(2.0 - t2*de/e) +
     +            d2e*(1.0/eta - rv*t2/e)
c
         dfdt2 = dsadt2 + eta*dsmdt2/z
c
         t2 = t2 - f/dfdt2
c
         n  = n + 1
c
c         write(6,*) '     n,t1,t2',n,t1,t2
      if (n .lt. nit) go to 1000
c
      return
      end
      subroutine pstcal(z1,z2,t1,t2,p1,ps,ts)
c     This routine calculates the surface pressure (psfc) 
c     from thermodynamic variables near the surface.
c
c     level 1 = level closest to the surface (usually 1000 mb)
c     level 2 = next level up (usually 850 or 925 mb)
c
c     input: p1 = pressure (Pa) 
c            zi = geopotential height (m) (i=1,2)
c            ti = temperature (K)         (i=1,2)
c     
c     output: ps = surface pressure (Pa)
c             ts = surface temperature (K)
c
c     Specify physical constants (mks units)
      rd = 287.0
      g  = 9.81
c    
c     Calculate the lapse rate
      gamma = -(t2-t1)/(z2-z1)
c
      if (gamma .gt. 0.0) then
c        Assume constant lapse rate atmosphere
         ps = p1*( (t1/(t1-gamma*z1))**(g/(rd*gamma)) )
         ts = t1 + gamma*z1
      else
c        Assume isothermal atmosphere
         ps = p1*exp(g*z1/(rd*t1))
         ts = t1
      endif
c
      return
      end
      subroutine stndz(p,z,t,theta)
c     This routine calculates the standard height z (m) from the
c     pressure p (mb). The temperature t (K) and potential temperature
c     theta (K) at p are also calculated.
C
      g   = 9.80665
      r   = 287.05
      cp  = 1004.0
      b   = 0.0065
      p0  = 1013.25
      t0  = 288.15
      p00 = 1000.0
      p1  = 226.32
      t1  = 216.65
      z1  = 11000.0
      cap = r/cp
      a   = r*b/g
C
      z2  = 20000.0
      b2  = -0.0010
      p2  = 54.75
      t2  = t1
      a2  = r*b2/g
C
      if     (p .ge. p1) then
         z = (t0/b)*(1.0 - (p/p0)**a)
         t = t0 - b*z
      elseif (p .lt. p1 .and. p .ge. p2) then
         z = z1 + (r*t1/g)*alog(p1/p)
         t = t1
      else
	 z = z2 + (t2/b2)*(1.0 - (p/p2)**a2)
	 t = t2 - b2*(z-z2)
      endif
C
      theta = t*( (p00/p)**cap )
c
      return
      end
      subroutine thetae(tk,p,rh,pl,tl,w,te)
c     This routine calculates the equivalent potential temperature
c     using the formula described in Bolton (1980) MWR
c     
c     Input: tk  - Temperature (K)
c            p   - Total pressure (hPa)
c            rh  - Relative humidity (%)
c       
c     Output: tl - Temperature (K) of the LCL
c             pl - Pressure (hPa) of the LCL
c             te - Thetae (K) 
c             w  - Mixing ratio (g/Kg)
c
c     Note: If any input values is outside the normal 
c           atmospheric range, all output variables are set to -999.
c
c     Check input
      if (tk .lt. 100. .or. tk .gt.  350.) go to 900
      if (p  .le.   0  .or.  p .gt. 1200.) go to 900
      if (rh .le.   0. .or. rh .gt.  100.) go to 900
c
      ctk = 273.15
      t   = tk - ctk
c
      es = 6.112*exp( 17.67*t/(t+243.5) )
      ws = 622.0*es/(p-es)
      w  = ws*rh/100.0
c
      tl = 55.0 + 1.0/( 1.0/(tk-55.0) - alog(rh/100.0)/2840. )
      pl = p*(tl/tk)**(1.0/0.2854)
c
      aa = .2854*(1.0 - .00028*w) 
      bb = ( (3.376/tl) - .00254 )*w*(1.+.00081*w)
      te = (tk*(1000.0/p)**aa)*exp(bb)
c
      return
c
  900 continue
      pl = -999.
      tl = -999.
      te = -999.
c
      return
      end
      subroutine ctorh(x,y,r,theta)
c     This routine converts from Cartesion coordinates
c     to radial coordinates, where theta is in
c     degrees measured clockwise from
c     the +y-axis (standard meteorological heading).
c
      r = sqrt(x*x + y*y)
c
      if (r .le. 0.0) then
         theta = 0.0
         return
      endif
c
      rtd = 57.296
      theta = rtd*acos(x/r)
      if (y .lt. 0.0) theta = 360.0 - theta
c
c     Convert theta to heading
      theta = 90.0 - theta
      if (theta .lt. 0.0) theta = theta + 360.0
c
      return
      end
      subroutine rhtoc(r,thetah,x,y)
c     This routine converts from radial coordinates
c     to Cartesian coordinates, where theta is in
c     degrees measured lockwise from
c     the +y-axis (standard meteorological heading).
c
c     Convert theta from heading to standard definition
      theta = 90.0 - thetah
      if (theta .lt. 0.0) theta = theta + 360.0
c
      rtd = 57.296
      x = r*cos(theta/rtd)
      y = r*sin(theta/rtd)
c
      return
      end
