      SUBROUTINE RHDST(FLAT,FLNG,TLAT,TLNG,DIR,DST)                      
C                                                                        
C  THIS IS A "GHDST" SUBROUTINE; FROM POINT (FLAT,FLNG) TO POINT         
C   (TLAT,TLNG) FINDS THE DIRECTION (DIR) AND DISTANCE (DST) IN N MI.    
C   DIRECTION IS CALCULATED ACCORDING TO RHUMB-LINE DIRECTION.           
C                                                                        
C                                                                        
      DIR=0.                                                             
      DST=0.                                                             
      RNUM = (FLNG-TLNG)*3.1415926535898/180.                            
      TD1 = TAN((45.0+(0.5*TLAT))*3.1415926535898/180.)                  
      TD2 = TAN((45.0+(0.5*FLAT))*3.1415926535898/180.)                  
      RLTD1 = ALOG(TD1)                                                  
      RLTD2 = ALOG(TD2)                                                  
      DENOM = RLTD1-RLTD2                                                
      RMAG = (RNUM*RNUM) + (DENOM*DENOM)                                 
      IF (RMAG.NE.0.0) DIR = ATAN2(RNUM,DENOM)*180./3.1415926535898      
      IF (DIR.LE.0.0) DIR = 360.0+DIR                                    
      DST = 60.0*ABS(FLAT-TLAT)/ABS(COS(DIR*3.1415926535898/180.))       
      ICRS = DIR+0.5                                                     
      IF (ICRS.EQ.90  .OR.  ICRS.EQ.270)                                 
     &DST = 60.0*ABS(FLNG-TLNG)*COS(FLAT*3.1415926535898/180.)           
      DIR=FLOAT(ICRS)                                                    
      ICRS=DST*10.+0.5                                                   
      DST=FLOAT(ICRS)/10.                                                
      RETURN                                                             
      END                                                                
