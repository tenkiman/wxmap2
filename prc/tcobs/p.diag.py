#!/usr/bin/env python

from M import *
MF=MFutils()

tc13e="""
2009082800 13E.2009 025 1007  13.2   96.5W ---- ---- 285.6  11.1   0  FL: NT DB CQ NW  LF: 0.00  TDO: ___  C:  13.2   
2009082806 13E.2009 025 1007  13.3   97.7W ---- ---- 280.1  11.4   0  FL: NT DB CQ NW  LF: 0.00  TDO: ___  C:  13.4   
2009082812 13E.2009 025 1007  13.4   98.9W ---- ---- 274.9  11.7   0  FL: NT DB CQ NW  LF: 0.00  TDO: ___  C:  13.6   
2009082818 13E.2009 030 1007  13.6  100.1W ---- ---- 277.3  11.8   0  FL: NT DB CQ WN  LF: 0.00  TDO: ___  C:  13.6   
2009082900 13E.2009 035 1005  13.7  101.0W    5 ---- 278.4  10.3   1  FL: TC TS CQ WN  LF: 0.00  TDO: KEF  C:  13.7   
2009082906 13E.2009 045 1000  13.9  101.9W   30 ---- 279.7   8.9   2  FL: TC TS CQ WN  LF: 0.00  TDO: ESB  C:  13.9   
2009082912 13E.2009 065  990  14.2  102.9W   40   21 285.2   9.6   3  FL: TC HU CQ WN  LF: 0.00  TDO: ESB  C:  14.1   
2009082918 13E.2009 090  970  14.8  103.8W   50   25 296.1  10.2   4  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  C:  14.8   
2009083000 13E.2009 090  970  15.4  104.7W   50   25 304.6  10.6   5  FL: TC HU CQ WN  LF: 0.00  TDO: JLB  C:  15.5   
2009083006 13E.2009 105  957  15.8  105.5W   57   27 301.4   9.6   6  FL: TC HU CQ WN  LF: 0.00  TDO: DPB  C:  15.8   
2009083012 13E.2009 120  945  16.0  106.0W   57   27 295.6   6.9   7  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  C:  16.0   
2009083018 13E.2009 120  945  16.3  106.6W   57   27 295.3   5.8   8  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  C:  16.3   
2009083100 13E.2009 125  940  16.7  107.0W   57   27 306.1   5.9   9  FL: TC HU CQ WN  LF: 0.00  TDO: MJB  C:  16.7   
2009083106 13E.2009 125  940  17.2  107.6W   63   32 313.2   6.6  10  FL: TC HU CQ WN  LF: 0.00  TDO: DPB  C:  17.2   
2009083112 13E.2009 125  940  17.7  108.1W   67   37 313.6   7.3  11  FL: TC HU CQ WN  LF: 0.00  TDO: JSD  C:  17.7   
2009083118 13E.2009 130  936  18.1  108.9W  100   61 306.0   7.7  12  FL: TC HU CQ WN  LF: 0.00  TDO: JSD  C:  18.1   
2009090100 13E.2009 135  931  18.9  109.3W  102   61 316.5   8.3  13  FL: TC HU CQ WN  LF: 0.00  TDO: MJB  C:  18.9   
2009090106 13E.2009 135  931  19.8  109.8W  102   61 333.4   9.5  14  FL: TC HU CQ WN  LF: 0.00  TDO: DPB  C:  19.8   
2009090112 13E.2009 130  933  20.6  110.5W  102   61 326.4  10.2  15  FL: TC HU CQ WN  LF: 0.00  TDO: WAL  C:  20.6   
2009090118 13E.2009 115  948  21.5  111.0W  107   52 326.6  10.2  16  FL: TC HU CQ WN  LF: 0.00  TDO: JLB  C:  21.5   
2009090200 13E.2009 100  960  22.3  111.3W  107   52 336.3   9.3  17  FL: TC HU CQ WN  LF: 0.00  TDO: TBK  C:  22.6   
2009090206 13E.2009 095  965  23.4  111.7W   92   50 341.2  10.0  18  FL: TC HU CQ WN  LF: 0.00  TDO: RJB  C:  23.4   
2009090212 13E.2009 090  970  24.7  112.1W   92   50 343.0  12.5  19  FL: TC HU CQ WN  LF: 0.27  TDO: TCT  C:  24.7   
2009090218 13E.2009 080  975  25.9  112.4W   92   50 345.7  12.9  20  FL: TC HU CQ WN  LF: 0.32  TDO: JLB  C:  25.9   
2009090300 13E.2009 065  983  26.7  112.4W   90   48 352.3  10.1  21  FL: TC HU CQ WN  LF: 0.75  TDO: CRA  C:  26.7   
2009090306 13E.2009 050  997  27.4  112.3W   75   25   3.4   7.5  22  FL: TC TS CQ WN  LF: 0.57  TDO: RJB  C:  27.5   
2009090312 13E.2009 045  999  27.6  112.3W   67 ----   5.6   4.5  23  FL: TC TS CQ WN  LF: 0.57  TDO: TCT  C:  27.8   
2009090318 13E.2009 040 1002  27.8  112.1W   30 ----  23.9   2.2  24  FL: TC TS CQ WN  LF: 0.02  TDO: TCT  C:  27.8   
2009090400 13E.2009 035 1004  27.7  111.9W   26 ----  74.2   1.8  25  FL: TC TS CQ WN  LF: 0.16  TDO: DPB  C:  27.6   
2009090406 13E.2009 035 1005  27.5  111.7W   26 ---- 130.3   2.3  26  FL: TC TS CQ WN  LF: 0.00  TDO: JLB  C:  27.5   
2009090412 13E.2009 025 1008  27.7  111.6W ---- ----  90.0   1.3  27  FL: TC TD CQ WN  LF: 0.00  TDO: MJB  C:  27.7   
2009090418 13E.2009 025 1006  27.4  112.2W ---- ---- 257.3   2.3  28  FL: TC TD CQ WN  LF: 0.16  TDO: JSD  C:  27.4
"""

tcdtgs="""
     BLAS 2010062000 03E.2010 050  995  16.9  110.9W   60   15 286.6   7.0  11  FL: TC TS CQ WN  LF: 0.00  TDO: JPC  
    CELIA 2010062000 04E.2010 050  997  12.2   98.3W   45    5 252.5   6.7   3  FL: TC TS CQ WN  LF: 0.00  TDO: ALC  
     BLAS 2010062006 03E.2010 045  997  17.2  111.8W   45 ---- 290.2   8.7  12  FL: TC TS CQ WN  LF: 0.00  TDO: ALC  
    CELIA 2010062006 04E.2010 055  994  12.1   99.0W   45    5 257.6   7.0   4  FL: TC TS CQ WN  LF: 0.00  TDO: ALC  
     BLAS 2010062012 03E.2010 040 1001  17.5  113.0W   47 ---- 286.7  10.5  13  FL: TC TS CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062012 04E.2010 055  994  11.8   99.5W   45    5 251.2   6.2   5  FL: TC TS CQ WN  LF: 0.00  TDO: ___  
_________ 2010062012 95E.2010 020 1009   8.0   88.0W ---- ---- 270.0   9.9   0  FL: NT LO NC NW  LF: 0.00  TDO: ___  
     BLAS 2010062018 03E.2010 030 1006  17.8  114.3W ---- ---- 284.7  11.8  14  FL: TC TD CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062018 04E.2010 065  989  11.6  100.0W   57   30 249.6   5.7   6  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
   INVEST 2010062018 95E.2010 020 1009   7.8   89.0W ---- ---- 270.0   9.9   0  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
     BLAS 2010062100 03E.2010 030 1007  17.9  115.5W ---- ---- 279.5  12.1  15  FL: TC TD CQ WN  LF: 0.00  TDO: HSM  
    CELIA 2010062100 04E.2010 070  986  11.6  100.6W   57   30 259.5   5.5   7  FL: TC HU CQ WN  LF: 0.00  TDO: SRS  
   INVEST 2010062100 95E.2010 020 1009   7.9   89.9W ---- ---- 273.0   9.4   0  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
     BLAS 2010062106 03E.2010 030 1007  18.0  116.6W ---- ---- 275.2  11.0  16  FL: TC TD CQ WN  LF: 0.00  TDO: ALC  
    CELIA 2010062106 04E.2010 070  986  11.7  101.3W   55   30 274.5   6.4   8  FL: TC HU CQ WN  LF: 0.00  TDO: ALC  
     BLAS 2010062112 03E.2010 030 1007  17.8  117.9W ---- ---- 267.5  11.4  17  FL: TC TD CQ WN  LF: 0.00  TDO: ESB  
    CELIA 2010062112 04E.2010 070  986  11.5  102.0W   55   30 270.0   6.9   9  FL: TC HU CQ WN  LF: 0.00  TDO: DPB  
_________ 2010062112 95E.2010 020 1009   9.0   90.6W ---- ---- 296.8   6.6   0  FL: NT LO NC NW  LF: 0.00  TDO: ___  
     BLAS 2010062118 03E.2010 025 1008  17.5  119.3W ---- ---- 261.2  13.0  18  FL: TC TD CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062118 04E.2010 075  979  11.6  102.8W   60   32 273.9   7.4  10  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  
   INVEST 2010062118 95E.2010 025 1008   9.3   91.2W ---- ---- 296.9   6.6   0  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
    CELIA 2010062200 04E.2010 090  970  11.7  103.6W   75   37 277.3   7.9  11  FL: TC HU CQ WN  LF: 0.00  TDO: DPR  
   INVEST 2010062200 95E.2010 025 1008   9.7   91.7W ---- ---- 298.9   6.2   0  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
    CELIA 2010062206 04E.2010 090  970  11.5  104.3W   75   37 266.1   7.4  12  FL: TC HU CQ WN  LF: 0.00  TDO: MAD  
   INVEST 2010062206 95E.2010 025 1008   9.7   92.1W ---- ---- 286.9   5.2   0  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
    CELIA 2010062212 04E.2010 090  970  11.7  105.0W   75   37 274.2   6.9  13  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  
   INVEST 2010062212 95E.2010 025 1008  10.0   92.2W ---- ---- 300.1   4.0   0  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
    CELIA 2010062218 04E.2010 085  972  11.7  105.9W   77   37 273.7   7.9  14  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  
   INVEST 2010062218 05E.2010 025 1008  10.2   92.5W ---- ---- 304.1   3.6   0  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
   INVEST 2010062218 95E.2010 025 1008  10.2   92.5W ---- ---- 304.1   3.6   0  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
    CELIA 2010062300 04E.2010 080  977  11.7  106.7W   77   37 270.0   8.3  15  FL: TC HU CQ WN  LF: 0.00  TDO: MAD  
     FIVE 2010062300 05E.2010 030 1006  10.8   93.0W ---- ---- 315.5   5.6   0  FL: TC TD CQ WN  LF: 0.00  TDO: MAD  
    CELIA 2010062306 04E.2010 075  980  11.8  107.5W   71   36 273.7   7.8  16  FL: TC HU CQ WN  LF: 0.00  TDO:  MA  
     FIVE 2010062306 05E.2010 035 1005  11.3   93.7W   22 ---- 313.0   8.1   1  FL: TC TS CQ WN  LF: 0.00  TDO:  MA  
    CELIA 2010062312 04E.2010 085  974  12.1  108.6W   86   43 282.1   9.5  17  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    DARBY 2010062312 05E.2010 045 1000  11.7   94.6W   40 ---- 295.6   9.2   2  FL: TC TS CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062318 04E.2010 100  963  12.2  109.8W   96   48 280.1  11.4  18  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    DARBY 2010062318 05E.2010 055  995  11.9   95.6W   52   20 287.9   9.8   3  FL: TC TS CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062400 04E.2010 090  971  12.2  111.1W   90   43 274.7  12.3  19  FL: TC HU CQ WN  LF: 0.00  TDO: TBK  
    DARBY 2010062400 05E.2010 055  995  12.2   96.6W   52   20 284.3  10.1   4  FL: TC TS CQ WN  LF: 0.00  TDO: JLB  
    CELIA 2010062406 04E.2010 095  967  12.3  112.2W   92   45 274.9  11.8  20  FL: TC HU CQ WN  LF: 0.00  TDO: SRS  
    DARBY 2010062406 05E.2010 060  994  12.5   97.5W   37   17 287.9   9.8   5  FL: TC TS CQ WN  LF: 0.00  TDO: RJB  
    CELIA 2010062412 04E.2010 100  963  12.3  113.3W   97   50 272.7  10.8  21  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    DARBY 2010062412 05E.2010 065  990  12.7   98.3W   37   17 286.8   8.7   6  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062418 04E.2010 115  948  12.6  114.3W   91   47 278.3  10.4  22  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    DARBY 2010062418 05E.2010 070  980  12.8   99.0W   45   25 281.6   7.5   7  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062500 04E.2010 135  932  12.9  115.4W  101   57 286.3  10.7  23  FL: TC HU CQ WN  LF: 0.00  TDO: ESB  
    DARBY 2010062500 05E.2010 080  978  13.1   99.7W   45   25 286.3   7.1   8  FL: TC HU CQ WN  LF: 0.00  TDO: LAA  
    CELIA 2010062506 04E.2010 140  926  13.2  116.5W  101   57 288.1  11.3  24  FL: TC HU CQ WN  LF: 0.00  TDO: ALC  
    DARBY 2010062506 05E.2010 090  967  13.2  100.4W   52   30 286.3   7.1   9  FL: TC HU CQ WN  LF: 0.00  TDO: RJB  
    CELIA 2010062512 04E.2010 130  935  13.6  117.6W  101   57 288.1  11.3  25  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  
    DARBY 2010062512 05E.2010 100  966  13.4  100.9W   52   30 284.4   6.0  10  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  
    CELIA 2010062518 04E.2010 115  948  14.0  118.5W   96   45 292.4  10.5  26  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  
    DARBY 2010062518 05E.2010 105  963  13.6  101.3W   45   32 294.6   4.8  11  FL: TC HU CQ WN  LF: 0.00  TDO: TCT  
      ONE 2010062600 01L.2010 030 1004  16.6   83.9W ---- ---- 290.4   7.2   0  FL: TC TD CQ WN  LF: 0.00  TDO: MJB  
    CELIA 2010062600 04E.2010 105  957  14.6  119.3W   96   45 301.2   9.6  27  FL: TC HU CQ WN  LF: 0.00  TDO: MJB  
    DARBY 2010062600 05E.2010 100  964  13.7  101.8W   47   32 288.9   4.6  12  FL: TC HU CQ WN  LF: 0.00  TDO: TBK  
      ONE 2010062600 93L.2010 030 1004  16.6   83.9W ---- ---- 290.4   7.2   0  FL: TC TD CQ NW  LF: 0.00  TDO: ___  
    CELIA 2010062606 04E.2010 090  971  15.1  120.3W   96   45 302.3  10.3  28  FL: TC HU CQ WN  LF: 0.00  TDO:  MA  
    DARBY 2010062606 05E.2010 100  964  13.5  102.4W   35   21 264.7   5.4  13  FL: TC HU CQ WN  LF: 0.00  TDO:  MA  
    CELIA 2010062612 04E.2010 085  974  15.4  121.1W   96   45 294.7   9.6  29  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    DARBY 2010062612 05E.2010 095  967  13.4  102.5W   35   21 246.2   3.7  14  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062618 04E.2010 070  987  15.6  121.9W   91   42 288.0   8.1  30  FL: TC HU CQ WN  LF: 0.00  TDO: VEL  
    DARBY 2010062618 05E.2010 080  978  13.5  102.7W   35   21 270.0   2.4  15  FL: TC HU CQ WN  LF: 0.00  TDO: ___  
    CELIA 2010062700 04E.2010 055  994  15.8  122.6W   80   20 285.5   7.5  31  FL: TC TS CQ WN  LF: 0.00  TDO: MJB  
    DARBY 2010062700 05E.2010 060  992  13.5  102.9W   30   17 270.0   1.9  16  FL: TC TS CQ WN  LF: 0.00  TDO: TBK  
    CELIA 2010062706 04E.2010 050  997  15.9  123.2W   52    7 285.5   7.5  32  FL: TC TS CQ WN  LF: 0.00  TDO: MAD  
    DARBY 2010062706 05E.2010 050  997  13.5  103.1W   30   17 270.0   1.9  17  FL: TC TS CQ WN  LF: 0.00  TDO: MFA  
    CELIA 2010062712 04E.2010 045 1000  15.8  123.5W   52 ---- 275.9   4.8  33  FL: TC TS CQ WN  LF: 0.00  TDO: TCT  
    DARBY 2010062712 05E.2010 045  999  13.7  103.1W   30 ---- 315.8   1.4  18  FL: TC TS CQ WN  LF: 0.00  TDO: TCT  
    CELIA 2010062718 04E.2010 035 1004  15.7  123.9W   30 ---- 262.6   3.9  34  FL: TC TS CQ WN  LF: 0.00  TDO: TCT  
    DARBY 2010062718 05E.2010 040 1002  13.6  102.4W   30 ----  81.6   3.4  19  FL: TC TS CQ WN  LF: 0.00  TDO: TCT  
    CELIA 2010062800 04E.2010 035 1004  15.5  124.1W   40 ---- 242.6   3.3  35  FL: TC TS CQ WN  LF: 0.00  TDO: RJP  
    DARBY 2010062800 05E.2010 040 1002  13.8  102.2W   30 ----  75.6   4.0  20  FL: TC TS CQ WN  LF: 0.00  TDO: RJP  
    CELIA 2010062806 04E.2010 035 1005  15.3  124.2W   50 ---- 215.9   2.5  36  FL: TC TS CQ WN  LF: 0.00  TDO: HSM  
    DARBY 2010062806 05E.2010 040 1004  14.2  101.3W   30 ----  68.4   6.8  21  FL: TC TS CQ WN  LF: 0.00  TDO: HSM  
    CELIA 2010062812 04E.2010 035 1005  15.2  124.1W   40 ---- 180.0   1.5  37  FL: TC TS CQ WN  LF: 0.00  TDO: MFA  
    DARBY 2010062812 05E.2010 030 1003  14.1  100.1W ---- ----  81.6  10.3  22  FL: TC TD CQ WN  LF: 0.00  TDO: MJB  
    CELIA 2010062818 04E.2010 030 1006  15.1  123.9W ---- ---- 136.0   2.1  38  FL: TC TD CQ WN  LF: 0.00  TDO: ESB  
    DARBY 2010062818 05E.2010 030 1004  14.3   98.9W ---- ----  87.5  11.6  23  FL: TC TD CQ WN  LF: 0.00  TDO: ESB  
    CELIA 2010062900 04E.2010 030 1006  15.2  123.6W ---- ----  90.0   2.4  39  FL: TC TD CQ WN  LF: 0.00  TDO: TBK  
    DARBY 2010062900 05E.2010 025 1005  14.6   97.7W ---- ----  77.9  11.9  24  FL: NT LO CQ NW  LF: 0.00  TDO: ___  
"""

posits={}

dotclist=0

if(dotclist):
    tcs=tc13e.split('\n')
    for tc in tcs:
        if(len(tc) > 0):
            tt=tc.split()
            dtg=tt[0]
            lat=tt[4]
            clon=tt[5]
            rlat=float(lat)
            rlon=float(clon.split('W')[0])
            rlon=360.0-rlon
            print dtg,lat,clon,rlat,rlon
            posits[dtg]=(rlat,rlon)

    dtgs=posits.keys()
    dtgs.sort()

    odir='../../dat/tc/obs/gfsenkf_cira_irwd_diag/'

            
dotcdtg=1

if(dotcdtg):

    dtgs=[]
    stmids={}
    
    tcdtgs=tcdtgs.split('\n')
    for tc in tcdtgs:
        if(len(tc) > 0):
            tt=tc.split()
            dtg=tt[1]
            stmid=tt[2].split('.')[0]
            lat=tt[5]
            clon=tt[6]
            rlat=float(lat)
            rlon=float(clon.split('W')[0])
            rlon=360.0-rlon
            print dtg,lat,clon,rlat,rlon,stmid
            posits[dtg,stmid]=(rlat,rlon)
            MF.loadDictList(stmids,dtg,stmid)

            dtgs.append(dtg)

    dtgs=MF.uniq(dtgs)

    odir='../../dat/tc/obs/gfsenkf_cira_irwd_diag/'
    odir='../../dat/tc/obs/201006/gfsenkf_control_diag/'
    mf.ChkDir(odir,'mk')


vars=['u','v','ps']

#dtgs=['2010062512']
dtgs = mf.dtg_dtgopt_prc( '2010062000.2010062900')
for dtg in dtgs:

    for stmid in stmids[dtg]:
        
        (rlat,rlon)=posits[dtg,stmid]
        print 'dddddddddddddddddd ',dtg,rlat,rlon,stmid
        if(int(dtg) > 2009090100 and dotclist): continue
        MF.WriteString2File(dtg,'dates.dat',verb=1)

        for var in vars:
            opath="%s/obs.%s.%s.%s.txt"%(odir,var,dtg,stmid)
            cmd='p.x %f %f 850.0 20.0 200.0 %s 0 > %s'%(rlon,rlat,var,opath)
            MF.runcmd(cmd)
