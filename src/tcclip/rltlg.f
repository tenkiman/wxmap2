      SUBROUTINE RLTLG(FLAT,FLNG,TLAT,TLNG,DIR,DST)                      
C                                                                        
C  THIS IS A "GLTLG" SUBROUTINE; FROM POINT (FLAT,FLNG) AND DIR,DST      
C   FINDS THE END POINT (TLAT,TLNG)                                      
C   DIRECTION IS THE RHUMB-LINE DIRECTION.                               
C                                                                        
C                                                                        
      TLAT=0.                                                            
      TLNG=0.                                                            
      ICRS=DIR                                                           
      IF (ICRS.EQ.90.OR.ICRS.EQ.270) GO TO 150                           
      CRPD = DIR*3.1415926535898/180.                                    
      TLAT = FLAT+(DST*COS(CRPD)/60.)                                    
      IF (TLAT.GT.89.0) TLAT = 89.0                                      
      IF (TLAT.LT.-89.0) TLAT = -89.0                                    
      TD1 = TAN((45.0+(0.5*TLAT))*3.1415926535898/180.)                  
      TD2 = TAN((45.0+(0.5*FLAT))*3.1415926535898/180.)                  
      RLTD1 = ALOG(TD1)                                                  
      RLTD2 = ALOG(TD2)                                                  
      DENOM = RLTD1-RLTD2                                                
      TLNG = FLNG-((TAN(CRPD)*DENOM)*180./3.1415926535898)               
      GO TO 100                                                          
150   DLON = DST/(60.0*COS(FLAT*3.1415926535898/180.))                   
      IF (ICRS.EQ.90) TLNG = FLNG - DLON                                 
      IF (ICRS.EQ.270) TLNG = FLNG + DLON                                
      TLAT = FLAT                                                        
100   ICRS=TLAT*10.+0.5                                                  
      TLAT=FLOAT(ICRS)/10.                                               
      ICRS=TLNG*10.+0.5                                                  
      TLNG=FLOAT(ICRS)/10.                                               
      END                                                                
