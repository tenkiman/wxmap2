
Cuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
C         
C         ukmo style stencil -- no central point         
C
C         V30 of bogus
C
Cuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu

      data ntcobs/14/
      data ntcobs_mid/8/
      data ntcobs_inner/4/

      data sdeg/
     $     1.5, 1.5, 1.5, 1.5,
     $     3.0, 3.0, 3.0, 3.0,
     $     6.0, 6.0, 6.0, 6.0, 6.0, 6.0,
     $     16*0.0/

      data sang/
     $      45.0, 135.0, 225.0, 315.0,
     $      -20.0, -110.0, -200.0, -290.0,
     $      60.0, 120.0, 180.0, 240.0, 300.0, 360.0,
     $     16*0.0/


Cnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn         
C         
C  fnmoc style stencil -- WITH central point
C
C         V10,V20,V21,V31 of bogus
C
Cnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn         

      data ntcobs/13/
      data ntcobs_mid/9/
      data ntcobs_inner/5/

      data ukmobg/.false./
