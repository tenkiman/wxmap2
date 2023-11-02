no *.x because took out of git on mike3
 1022  la src/*/*.x

 1030  cd ../tcgfdltrk/
 1033  cd gettrk_gen_20111014/
 1034  m
 1037  cd ../standalone_gfdl-vortextracker_v3.9a/
 1038  m
 1050  cd tclgem/
 1053  m clean
 1054  m
 1056  cd ../tcgfdltrk/
 1059  cd w3lib/
 1061  m
 1062  cd ../grbindex/
 1063  m
 1066  cd ../tcnavytrk/
 1068  m clean
 1069  m
 1071  m -f Makefile.linux 
 1074  ln -s Makefile.linux Makefile

 1077  cd tcgfdltrk/
 1078  ln -s standalone_gfdl-vortextracker_v3.9a/trk_exec/gettrk.exe gettrk_gen3.x
 1079  cd ..
 1080  la */*.x
-rwxrwxr-x. 1 fiorino fiorino  333728 Nov  2 14:01 tcdiag/lsdiag.x
lrwxrwxrwx. 1 fiorino fiorino      55 Nov  2 14:10 tcgfdltrk/gettrk_gen3.x -> standalone_gfdl-vortextracker_v3.9a/trk_exec/gettrk.exe
-rwxrwxr-x. 1 fiorino fiorino 1142144 Nov  2 14:02 tcgfdltrk/gettrk_genN.x
-rwxrwxr-x. 1 fiorino fiorino   59624 Nov  2 14:07 tcgfdltrk/grbindex.x
-rwxrwxr-x. 1 fiorino fiorino  460048 Nov  2 14:05 tclgem/iships.x
-rwxrwxr-x. 1 fiorino fiorino  208856 Nov  2 14:07 tcnavytrk/ngtrkN.x
