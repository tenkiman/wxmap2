from M import *
MF=MFutils()

# -- needed for 'noload'




class Aid(MFutils):

    Model2AidCard={
#model
#                 ! adeck name
#                 !      ! adeck type 0 - tcanal calc ; 1 - atcf adecks ; 2 - derived
#                 !      !   ! plus hour to "i" tracks are available +6 h into the future -- for counting cases
#                 !      !   !    ! adeck #
#                 !      !   !    !     ! start syn hour
#                 !      !   !    !     !    ! DdtgModelTracker -- how often run
#                 !      !   !    !     !    !    ! dtaumodel -- how often output
#                 !      !   !    !     !    !    !     ! TauMaxModel
#                 !      !   !    !     !    !    !     !     ! RmBigFeModelTracker 1 = remove; 0 = no; turned off 20070716
#                 !      !   !    !     !    !    !     !     !   !critrad nhc
#                 !      !   !    !     !    !    !     !     !   !    ! critrad jtwc
#                 !      !   !    !     !    !    !     !     !   !    !    ! vmax corr - none | light | moderate | heavy in bctrk.adeck.py
#                 !      !   !    !     !    !    !     !     !   !    !    !        ! matplotlib parms                              
#                 !      !   !    !     !    !    !     !     !   !    !    !        !                                       ! titling              

'fim8'   : "fim8  ! FIM8 ! 1 ! 0  !  50 ! 0  ! 12 !  12 ! 120 ! 0 !  0 !  0 ! light  ! ['FIM8,'orchid','orchid','fim8','-']  ! ESRL FIM G8 (30 km) using GFS GSI",
'ecmt'   : "ecmt  ! ECMT ! 1 ! 0  !  03 ! 0  !  6 !  12 ! 120 ! 0 ! 34 ! 34 ! light  ! ['ECMT','purple','fuchsia','ecmt']    ! ECMWF IFS (det) from TIGGE",
'conw'   : "conw  ! CONW ! 1 ! 0  !  83 ! 0  !  6 !   6 ! 180 ! 0 ! 34 ! 34 ! heavy  ! ['CONW','#51588E','indianred','conw'] ! NCEP GFS (AVNO tracker)",
# rap -- 3-h output
'rapc'   : "rapc  ! RAPC ! 1 ! 0  !  50 ! 0  !  3 !   3 ! 120 ! 0 !  0 !  0 ! light  ! ['RAPC,'orchid','orchid','f8c','-']   ! ESRL RAP -- Cold Start from GFS",
'rpao'   : "rpao  ! RPAO ! 1 ! 0  !  50 ! 0  !  3 !   3 ! 120 ! 0 !  0 !  0 ! light  ! ['RAPC,'orchid','orchid','f8c','-']   ! ESRL RAP -- Conv Obs + AIRS",
'rpco'   : "rpco  ! RPCO ! 1 ! 0  !  50 ! 0  !  3 !   3 ! 120 ! 0 !  0 !  0 ! light  ! ['RAPC,'orchid','orchid','f8c','-']   ! ESRL RAP -- Conv Obs only",

    }


    def __init__(self,model):


        def ttnum2var(tt,n,conv='a'):
            try:
                var=tt[n].strip()
            except:
                var=''
            if(conv == 'i' and var !=''): var=int(var)
            return(var)

        def str2list(ttt):
            ttt=ttt[1:len(ttt)-1]
            ttt=ttt.split(',')
            tt4=[]
            for t4 in ttt:
                tt4.append(t4[1:-1])
            return(tt4)

        card=self.GetModelAidPropCard(model)
        tt=card.split('!')

        i=1

        self.AdeckName=ttnum2var(tt,i) ; i=i+1
        self.AdeckType=ttnum2var(tt,i,'i') ; i=i+1
        self.PlusHour=ttnum2var(tt,i,'i') ; i=i+1
        self.AdeckNum=ttnum2var(tt,i) ; i=i+1

        self.StartSynHourModel=ttnum2var(tt,i,conv='i') ; i=i+1

        self.DdtgModelTracker=ttnum2var(tt,i,'i') ; i=i+1
        self.DtauModel=ttnum2var(tt,i,'i') ; i=i+1

        self.TauMaxModel=ttnum2var(tt,i,'i') ; i=i+1
        self.RmBigFeModelTracker=ttnum2var(tt,i,'i') ; i=i+1
        self.CritRadAdeckParserNhc=ttnum2var(tt,i,'i') ; i=i+1
        self.CritRadAdeckParserJtwc=ttnum2var(tt,i,'i') ; i=i+1
        self.VmaxCorrType=ttnum2var(tt,i); i=i+1

        ttt=ttnum2var(tt,i); i=i+1
        tt4=str2list(ttt)
        tt5=tt[i] ; i=i+1

        self.TrkModeltoBattributes=tt4
        self.ModelNametoModelDesc=tt5

        self.VmaxOnly=0
        self.TrackOnly=0

        self.fcnoload=(-98.8,-988.8,-98.8,-998.8)

    def GetModelAidPropCard(self,model,verb=0):

        try:
            card=self.Model2AidCard[model]
        except:
            if(verb): print 'no aid for model: ',model
            #card="MMMM  ! MMMM ! 1 ! 0  !  50 ! 0  ! 12 !  12 ! 120 ! 0 !  0 !  0 ! heavy  ! ['MMMM,'orchid','orchid','mmm','-']     ! XXXXX"
            # -- default
            card="MMMM  ! MMMM ! 1 ! 0  !  83 ! 0  !  6 !   6 ! 180 ! 0 ! 0 ! 0 ! heavy  ! ['MMMM','#51588E','indianred','mmmm']   ! XXXXX"

        return(card)



AidPropCards={
#       omodel = model if blank
#             ! color
#             !              ! title
#             !              !                                                ! mark -- matplotlib ('d')
#             !              !                                                !    !  vmaxCorrScheme ('global' | 'lame')
#             !              !                                                !    !    ! opt1                    
'rapc'        : "RAPCOLD     ! RAP(12 km) : GFS Cold Start                    ! red     !    !     !    !    !    !",
'rpao'        : "RAP+AIRS    ! RAP(12 km) : Conv + AIRS obs                   ! red           !    !     !    !    !    !",
'rpco'        : "RAP         ! RAP(12 km) : Conv only                         ! green      !    !     !    !    !    !",
'avno'        : "GFS         ! GFS(T584):HybDA                                ! olive    !    !     !    !    !    !",
'tgfs2'       : "GFS         ! GFS(T584):HybDA(local trkr)                    ! olive    !    !     !    !    !    !",
'rf3162g9'    : "GFS         ! GFS(T584):HybDA(local trkr)                    ! olive    !    !     !    !    !    !",
}



class AidProp(MFbase):


    exprs={

# -- nwp2 models -- local trackers

"""%s == 'pwsg'""":
(("PWSG - PanaWxSysGFS [Dx:13kmL64]                         ",None    ,'darkgreen'          ,   ),('NNNN' , 77,0,6,6, )),

"""%s == 'gfsp'""":
(("GFSP - GFS[Dx:13kmL64] using PanaWxSysGFS res/grids                ",None    ,'greenyellow'          ,   ),('NNNN' , 77,0,6,6, )),



"""mf.find(%s,'ecm2')""":
(("ECM2 - ECMWF HRES IFS[Dx:9kmL137] NCEP 1deg    ",None    ,'lightgoldenrodyellow'           ,   ),('NNNN' , 77,0,12,6, )),

"""mf.find(%s,'ecm4')""":
(("ECM4 - ECMWF HRES IFS[Dx:9kmL137] NCEP 0.25deg    ",None    ,'yellow'           ,   ),('NNNN' , 77,0,12,6, )),

"""mf.find(%s,'ecm5')""":
(("ECM5 - ECMWF HRES IFS[Dx:9kmL137] ECMWF 0.25/0.10deg    ",None    ,'yellow'           ,   ),('NNNN' , 77,0,12,6, )),

"""%s == 'ecmn'""":
(("ECMN - ECMWF IFS[det,T1279(16km)L137] NWS 1deg grid     ",None    ,'gold'           ,   ),('NNNN' , 77,0,12,6, )),

"""%s == 'ecmt'""":
(("ECMT - ECMWF HRES IFS[Dx:9KmL137] TIGGE 0.5deg grid ",None    ,'gold'           ,   ),('NNNN' , 77,0,6,6, )),

"""%s == '3ecmt'""":
(("3ECMT - V3.9 of TIM ECMWF HRES IFS[Dx:9KmL137] TIGGE 0.5deg grid ",None    ,'gold'           ,   ),('NNNN' , 77,0,6,6, )),

"""%s == 'gfs2'""":
(("GFS2 - GFS[Dx:13kmL64]                         ",None    ,'greenyellow'          ,   ),('NNNN' , 77,0,6,6, )),

"""%s == 'fv3e'""":
(("FV3E - ESRL FV3 GFS-Phys[Dx:27kmL64]           ",None ,'greenyellow'          ,   ),('NNNN' , 77,0,6,6, )),

"""%s == 'fv3g'""":
(("FV3G - ESRL FV3 Grell-Freitas-Phys[Dx:27kmL64] ",None ,'skyblue'          ,   ),('NNNN' , 77,0,6,6, )),

"""%s == 'fv7e'""":
(("FV7E - ESRL FV3 (C768) GFS-Phys[Dx:13kmL64]           ",None ,'lime' ,      ),('NNNN' , 77,0,6,6, )),

"""%s == 'fv7g'""":
(("FV7G - ESRL FV3 (C768) Grell-Freitas-Phys[Dx:13kmL64]  ",None ,'dodgerblue' ,  ),('NNNN' , 77,0,6,6, )),

"""%s == 'navg' or %s == 'nvgm' or %s == 'tnavg'""":
(("NVGM - NAVGEM [T359(47km)L42]                          ",None    ,'navy  '    ,   ),( )),

"""%s == 'otcm'""":
(("OTCM - One-way influence TC model [200kmL3]           ",None    ,'cornflowerblue'    ,   ),( )),

"""%s == 'ntcm'""":
(("NTCM - Nested two-way interactive TC model [200kmL3]   ",None    ,'green '    ,   ),( )),

"""%s == 'gnav'""":
(("GNAV - USN Global Model = NOGAPS (2007-2011) or NAVGEM  (2011-)      ",None    ,'navy  '    ,   ),( )),

"""%s == 'ngx' or %s == 'nngx'""":
(("NGX - NAVGEM [T359(47km)L42] (ncep tracker)            ",None    ,'royalblue  '    ,   ),( )),

""" %s == 'afum' """:
(("AFUM - USAF ~ UM[Dx:17kmL70] 0.32x0.24 grid (native)                 ",None    ,'mediumpurple    '     ,   ),( )),

""" mf.find(%s,'ukm2')    """:
(("UKMO - UM[Dx:17kmL70] 0.32x0.24 grid (native)                 ",None    ,'purple    '     ,   ),( )),

"""%s == 'cmc2'         """:
(("CMC:GDPS3.0[0.9x0.9(N400)L79]                  ",None    ,'mediumseagreen' ,   ),( )),

"""%s == 'cgd6'         """:
(("CMC:GDPS3.0[0.6x0.6(N400)L79]                  ",None    ,'mediumseagreen' ,   ),( )),

"""%s == 'cgd2'         """:
(("CMC:GDPS7.0[0.24x0.24(N350)L79]                  ",None    ,'mediumvioletred' ,   ),( )),


# -- ecmwf trackers
#        

"""%s == 'erai'  """:
(("ERAI - ERA Interim  [T255(80km)L60]    ",None    ,'indigo'     ,        ),('ERAI' , 77,0,12,6, )),


"""%s == 'emx'  or %s == 'nemx'      """:
(("EMX - ECMWF HRES [To1279(9km)L137] NCEP 0.25 deg grid    ",None    ,'khaki'     ,        ),('EMX' , 77,0,12,6, )),


"""%s == 'edetn'""":
(("EDETN - ECMWF HRES(tigge) withOUT tau continuity     ",None    ,'tan'     ,         ),('EDETN' , 77,0,12,6, )),


"""%s == 'edte'""":
(("EDTE - ECMWF HRES from ECMWF     ",None    ,'goldenrod'     ,         ),('EDTE' , 77,0,12,6, )),

"""%s == 'e41r'""":
(("E41R - ECMWF C41R2 || runs     ",None    ,'tan'     ,         ),('E41R' , 77,0,12,6, )),

"""%s == 'ecmo' or %s == 'emdt'""":
#(("EDET - ECMWF HRES [IFS,det,T1279(16km)L137]     ",None    ,'gold'     ,         ),('EDET' , 77,0,6,6, )),
(("ECMO - ECMWF HRES [9kmL137] (bufr) native res grid ~0.1deg     ",None    ,'gold'     ,         ),('ECMO' , 77,0,6,6, )),

"""%s == 'ecmf'""":
#(("EDET - ECMWF HRES [IFS,det,T1279(16km)L137]     ",None    ,'gold'     ,         ),('EDET' , 77,0,12,6, )),
(("ECMF - ECMWF HRES [9kmL137] (bufr) native res grid ~0.1deg     ",None    ,'gold'     ,         ),('ECMO' , 77,0,12,6, )),

"""%s == 'ecmi'""":
#(("EDET - ECMWF HRES [IFS,det,T1279(16km)L137]     ",None    ,'gold'     ,         ),('EDET' , 77,0,12,6, )),
(("ECMI - 6-h interp ECMWF HRES [9kmL137] (bufr) native res grid ~0.1deg     ",None    ,'gold'     ,         ),('ECMO' , 77,0,12,6, )),

"""%s == 'ecnt' or %s == 'emct'      """:
(("ECMWF EPS[cntrl,T699(16km)L137]                  ",None    ,'yellow  ' ,         ),('NNNN', 77,0,12,6, )),

"""%s == 'erai' """:
(("ERAI - ECMWF ERA-I [N128 79kmL60 CY31R2] grid res: 0.7deg    ",None    ,'lightyellow'     ,         ),('ERAI' , 77,0,12,6, )),

"""%s == 'era5' """:
(("ERA5 - ECMWF ERA5 [T699 27kmL137 CY41R2] grid res: 0.25deg     ",None    ,'goldenrod'     ,         ),('ERA5' , 77,0,12,6, )),

# -- standard adeck aids
#
"""%s == 'jtwc'         """:
(("JTWC - official forecast          ",None     ,'tomato'      ,                   ),( )),

"""%s == 'rjtd'         """:
(("JMA - official forecast          ",None     ,'magenta'      ,                   ),( )),

"""%s == 'ofcl'         """:
(("NHC - official forecast         ",None     ,'tomato    '      ,                 ),( )),

"""%s == 'ofci'         """:
(("NHC(background: +6h interp first guess)     ",None     ,'indianred    ' ,       ),( )),

"""%s == 'jtwi'         """:
(("JTWC(background: +6h interp first guess)    ",None     ,'indianred    ' ,       ),( )),

"""%s == 'avno'""":
(("AVNO - NCEP GFS [13kmL64] IC:NCEP Hybrid            ",None     ,'olive'        ,        ),('AVNO' , 77,0,6,6, )),

"""%s == 'javn'""":
(("JAVN - NCEP GFS - local tracker at JTWC IC:NCEP Hybrid          ",None     ,'greenyellow'        ,        ),('AVNO' , 77,0,6,6, )),


"""%s == 'egrr'         """:
((" UKMO - UM(global;dx~25km) (EGRR - human QC)                   ",None     ,'purple    '  ,         ),( 'EGRR' , 77,0,12,6, )),

"""%s == 'ukm'         """:
((" UKM - UM(global;dx~13km)                   ",None     ,'purple    '  ,         ),( 'EGRR' , 77,0,12,6, )),

"""%s == 'egri'         """:
(("UKMO UM(global;dx~25km) (6h interp)         ",None     ,'purple    '  ,         ),( )),

"""%s == 'jgsm' or %s == 'jgsi'   """:
#(("JMA Global Spectral Model (dx=20km)         ",None     ,'deepskyblue    '    ,         ),( )),
(("JMA Global Spectral Model (dx=20km)         ",None     ,'dodgerblue    '    ,         ),( )),

"""%s == 'jukm'                   """:
(("uKMO - MF tracker                           ",None     ,'violetred '  ,         ),( )),

"""%s == 'ukx' or %s == 'nukx'  """:
(("uKMO - TM trkr                              ",None     ,'violetred'   ,         ),( )),

"""%s[0:4] == 'ngps' or %s[0:4] == 'ngpc' or %s[1:5] == 'ngpc' or %s[0:4] == 'ngp2' or %s[1:5] == 'ngp2' """:
(("NOGAPS [T319(57km)L42]                      ",None     ,'navy  '     ,          ),( )),

"""%s == 'ngpi'         """:
(("NOGAPS (6h interp)                          ",None     ,'navy   ' ,              ),( )),

"""%s == 'nvgi'         """:
(("NAVGEM (6h interp)                          ",None     ,'navy   ' ,              ),( )),

"""%s == 'aemn'    """:
(("AEMN - NCEP:GEFS [34kmL64] Mean of 21 members          ",None     ,'mediumseagreen ' ,      ),( )),

"""%s == 'naemn' or %s == 'faemn'  """:
(("NAEMN -NCEP:GEFS [34kmL64] Mean of 21 members              ",None     ,'mediumseagreen ' ,      ),( )),

"""%s == 'ffgmn' """:
(("FFGMN - mean NCEP GFS EFS(11-20;T254)) + FIM 01-10 (dx=60km)       ",None     ,'greenyellow ' ,      ),( )),

"""%s == 'ffgsp' """:
(("FFGSP - NCEP GFS EFS(11-20;T254)) + FIM 01-10 (dx=60km) spread      ",None     ,'green' ,      ),( )),

"""%s == 'fgomn' """:
(("FGOMN - mean FIM 01-05 (gfs physics)       ",None     ,'yellow ' ,      ),( )),

"""%s == 'fgfmn' """:
(("FGFMN - mean FIM 06-10 GF (Grell-Frietas) convection     ",None     ,'magenta ' ,      ),( )),

""" %s == 'faesp'   """:
(("NAESP - NCEP:GEFS [34kmL64] Mean Spread                        ",None     ,'darkgreen ' ,      ),( )),


"""%s == 'cemn'    """:
(("CEMN - mean CMC GEM EPS (20;dx~66km)EnKF(254)                         ",None     ,'mediumseagreen ' ,      ),('CEMN', 77,0,12,6 )),


"""%s == 'avni'    """:
#(("GFS:GSI(29 km, 0.5deg) 06-h interp          ",None     ,'khaki    '      ,       ),( )),
(("GFS:GSI(29 km, 0.5deg) 06-h interp          ",None     ,'green    '      ,       ),( )),


# -- LGEM


"""%s == 'tecg'    """:
(("LGEM(ECWMF) with TM track            ",None     ,'gold'      ,              ),( )),

"""%s == 'oecg'    """:
(("LGEM(ECMWF) with OFCI track          ",None     ,'yellowgreen'  ,           ),( )),

"""%s == 'becg'    """:
(("LGEM(ECMWF) with BEST track          ",None     ,'yellow'      ,            ),( )),

"""%s == 'tgfg'    """:
(("LGEM(GFS) with TM track              ",None     ,'olive    '      ,         ),( )),

"""%s == 'ogfg'    """:
(("LGEM(GFS) with OFCI track            ",None     ,'greenyellow    '      ,   ),( )),

"""%s == 'bgfg'    """:
(("LGEM(GFS) with BEST track            ",None     ,'darkgreen    '      ,     ),( )),

"""%s == 'tgfg'    """:
(("LGEM(GFS) with TM track              ",None     ,'olive    '      ,         ),( )),

"""%s == 'tfig'    """:
(("LGEM(FIM) with TM track              ",None     ,'garnet    '      ,        ),( )),

"""%s == 'ofig'    """:
(("LGEM(FIM) with OFCI track            ",None     ,'magenta    '      ,       ),( )),

"""%s == 'bfig'    """:
(("LGEM(FIM) with BEST track            ",None     ,'maroon    '      ,        ),( )),

"""%s == 'ecm2g'        """:
(("ECMWF+LGEM (Logistic Growth Eqn Mod) ",None     ,'indigo    ' ,'H',         ),( )),

"""%s == 'gfs2g'        """:
(("GFS+LGEM (Logistic Growth Eqn Mod)   ",None     ,'plum    '   ,'H',         ),( )),

"""%s == 'ukm2g'        """:
(("uKmo+LGEM (Logistic Growth Eqn Mod)  ",None     ,'teal    '   ,'H',         ),( )),

"""%s == 'prdh'    """:
(("GFS:EnKF-GSI(not(TC relocate))       ",None     ,'greenyellow    '      ,   ),( )),

"""%s == 'prdi'    """:
(("GFS:EnKF-GSI(TC relocate)            ",None     ,'darkgreen    '      ,     ),( )),



# -- gfs para exp-2011

"""%s == 'gp3h'         """:
(("GFS(prd12q3h.2011)                  ",None     ,'yellow    '  ,             ),( )),


# -- gfs para 2010-2011 used by hwrf in hfip 2013 retro
"""%s == 'avnh13'         """:
(("GFS2012[27kmL64] IC:NCEP-Hybrid    ",None     ,'yellow    '   ,              ),( )),

"""%s == 'gp3i'         """:
(("GFS(prd12q3i.2011)                 ",None     ,'yellowgreen'  ,              ),( )),

"""%s == 'gfs2010'      """:
(("GFS(T574):GSI(29 km, 0.5deg)       ",None     ,'mediumseagreen ' ,           ),( )),

# -- FIM

"""%s == 'f8ca'         """:
(("FIM 2nd veldfbkg=1 intf= 50        ",'fimretro2517_A'  ,'usafblue' ,         ),( )),

"""%s == 'f8cb'         """:
(("FIM 2nd veldfbkg=1 intf=150        ",'fimretro2517_B'  ,'navy    ',          ),( )),

"""%s == 'f8cc'         """:
(("4th veldfbkg=3 intf =50            ",'fimretro2517_C'  ,'powderblue' ,       ),( )),

"""%s == 'f8cd'         """:
(("4th veldfbkg=3 intf=150            ",'fimretro2517_D'  ,'mediumblue' ,       ),( )),

"""%s == 'f8ce'         """:
(("2nd intf=150 vdboost=3             ",'fimretro2517_E'  ,'gold    '   ,       ),( )),

"""%s == 'f8cf'         """:
(("4th veldfbkg=10 intf=150           ",'fimretro2517_F'  ,'yellow '    ,       ),( )),

"""%s == 'f8cg'         """:
(("4th veldfbkg= 5 intf=150           ",'fimretro2517_G'  ,'khaki   '      ,    ),( )),

"""%s == 'fm8j' or mf.find(%s[0:4],'fm8j')""":
(("FIM8 - JET   FIM G8[30kmL64] 0.5deg tracker ",None     ,'steelblue '      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'fmxj' or mf.find(%s[0:4],'fm8j')""":
(("FIMX - JET   FIM G?[??kmL64] 0.5deg tracker ",None     ,'steelblue '      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'fmxt' or mf.find(%s[0:4],'fm8j')""":
(("FIMX - JET   FIM G?[??kmL64] 0.5deg tracker ",None     ,'steelblue '      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'fm7j' or mf.find(%s[0:4],'fm7j')""":
(("FIM7 - JET   FIM G7[60kmL64] 0.5deg tracker ",None     ,'steelblue '      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'fm8t' or mf.find(%s[0:4],'fm8t')""":
(("FIM8 - THEIA FIM G8[30kmL64] 0.5deg tracker ",None     ,'steelblue '      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'fm7t' or mf.find(%s[0:4],'fm7t')""":
(("FIM7 - THEIA FIM G7[60kmL64] 0.5deg tracker ",None     ,'steelblue '      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'fmgt' or mf.find(%s[0:4],'fmgt')""":
(("FIMG - THEIA FIM G?[??kmL64] 0.5deg tracker ",None     ,'navy'      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'fght' or mf.find(%s[0:4],'fght')""":
(("FIMG - THEIA FIM G?[??kmL64] 0.125deg tracker ",None     ,'tomato'      ,            ),('FIM7' , 77,0,12,6, )),

"""%s == 'f7ss' or mf.find(%s[0:4],'f7ss')""":
(("F7SS - FIM G7[60kmL64] SubSeasonal V2",None     ,'steelblue '      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'f7s3' or mf.find(%s[0:4],'f7s3')""":
(("F7S3 - FIM G7[60kmL64] SubSeasonal V3",None     ,'usafblue '      ,            ),('FIM8' , 77,0,12,6, )),

# --------- hi-res tracker
#
"""%s == 'f7hj' or mf.find(%s[0:4],'f7hj')""":
(("FIM7 - JET   FIM G7[60kmL64] 0.125deg tracker ",None     ,'tomato'      ,            ),('FIM7' , 77,0,12,6, )),

"""%s == 'f7ht' or mf.find(%s[0:4],'f7ht')""":
(("FIM7 - THEIA FIM G7[60kmL64] 0.125deg tracker ",None     ,'tomato'      ,            ),('FIM7' , 77,0,12,6, )),

"""%s == 'f8hj' or mf.find(%s[0:4],'f8hj')""":
(("FIM8 - JET   FIM G8[30kmL64] 0.125deg tracker ",None     ,'tomato'      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'f8ht' or mf.find(%s[0:4],'f8ht')""":
(("FIM8 - THEIA FIM G8[30kmL64] 0.125deg tracker ",None     ,'tomato'      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'fxhj' or mf.find(%s[0:4],'fxhj')""":
(("FIMX - JET   FIM G?[??kmL64] 0.125deg tracker ",None     ,'tomato'      ,            ),('FIM8' , 77,0,12,6, )),


"""%s == 'fm9j' or mf.find(%s[0:4],'fm9j')""":
(("FIM9 - FIM G9[15kmL64] 0.5deg tracker ",None     ,'royalblue '      ,            ),('FIM9' , 77,0,12,6, )),

""" mf.find(%s,'f9hj')""":
(("FIM9 - FIM G9[15kmL64] 0.125deg tracker ",None     ,'darkred '      ,            ),('FIM9' , 77,0,12,6, )),

"""%s == 'f8c' or mf.find(%s[0:5],'fim8') or mf.find(%s[0:4],'jf8c')""":
(("FIM8 - FIM G8[30kmL64] IC:NCEP_Hyrbrid   ",None     ,'mediumblue '      ,            ),('FIM8' , 77,0,12,6, )),

"""%s == 'f7c' or %s == 'fim7'       """:
(("FIM7 - FIM G7[60kmL64]             ",'fim7        ','steelblue    ' ,   ),( )),

"""%s == 'fim7x'        """:
(("FIM:GSI-EnKF(60 km, 0.5deg)             ",'fim7-chem   ','powderblue   ' ,  ),( )),

"""%s == 'f9c' or %s == 'f9cz'       """:
(("FIM - GSI_EnKF(15 km, 0.5deg)             ",'fim9        ','usafblue   ' ,    ),( )),

"""%s == 'rtfim'        """:
(("FIM:GSI-EnKF  [30kmL64]       ",'fim8  ','navy'      ,                      ),( )),

"""%s == 'f8cx'         """:
(("FIMX:GSI-EnKF(30 km, 0.5deg)          ",'fimx          ','usafblue    ' ,   ),( )),

"""%s == 'f8cy' or %s[0:4] == 'fimy' """:
(("FIMY:EnKF TMgen trks  [30kmL64]      ",'fim         ','steelblue'      ,    ),( )),

"""%s == 'jf8cy'        """:
(("FIMY:EnKF TM trkr  [30kmL64]            ",None     ,'royalblue'     ,       ),( )),

"""%s == 'f8cz' or %s == 'rtfimz'    """:
(("FIMZ:GSI : NewPhys  [30kmL64]           ",'fimz'   ,'usafblue'     ,        ),( )),

"""%s == 'f8em'         """:
(("FIM8:Ensemble Mean  [30kmL64]                 ",None     ,'steelblue' ,     ),( )),

"""%s == 'f9em'         """:
(("FIM9:Ensemble Mean  [15kmL64]                 ",None     ,'royalblue ' ,    ),( )),

"""%s == 'fim9' or mf.find(%s[0:5],'hfim9')     """:
(("FIM9 - FIM G9[15kmL64] IC:NCEP_Hybrid      ",None     ,'dodgerblue  '      ,       ),( )),

"""%s == 'fim93'    """:
(("FIM93 - FIM G9[15kmL64] IC:NCEP_Hybrid HFIP2013 model     ",None     ,'dodgerblue  '      ,       ),( )),

"""%s == 'fim94'    """:
(("FIM94 - FIM G9[15kmL64] IC:NCEP_Hybrid HFIP2014 model     ",None     ,'steelblue  '      ,       ),( )),

"""%s == 'fim9ni'    """:
(("FIM9NI - FIM G9[15kmL64] IC:NCEP_Hybrid HFIP2014 model new_interp   ",None     ,'usafblue  '      ,       ),( )),


"""%s == 'fim9eda'      """:
(("FIM9:ESRL GSI(T878)/EnKF(T382) Hybrid       ",None     ,'navy    '      ,   ),( )),

"""%s == 'f0em'         """:
(("FIM:EnKF(10 km, 0.5de g)                    ",None     ,'usafblue '     ,              ),( )),

"""%s == 'fr1094b'                """:
(("FIM 1094B:newphys V1                        ",None     ,'royalblue '     ,              ),( )),

"""%s == 'fr1231'                 """:
(("FIM 1231:newphys V1.1                       ",None     ,'steelblue    '  ,              ),( )),

"""%s == 'fr1273'                 """:
(("FIM 1273:newphys V1.2                       ",None     ,'steelblue    '  ,              ),( )),

"""%s == 'fr1411enkf'             """:
(("FIM1411:EnKF ((30 km, FlxCorr, err N EnKF)   ",None     ,'steelblue    ' ,              ),( )),

"""%s == 'fr1422enkf'             """:
(("FIM1422:EnKF (30 km, FlxCorr)               ",None     ,'mediumblue    ' ,              ),( )),

"""%s == 'fr1422gfs'              """:
(("FIM1422:GSI (30 km, FlxCorr)                ",None     ,'steelblue    ' ,              ),( )),

"""%s == 'fr1422gfsg7'            """:
(("FIM1422:GSI (60 km L64, FlxCorr)            ",None     ,'usafblue    '  ,              ),( )),

"""%s == 'fr1422gfsg7l38'         """:
(("FIM1422:GSI (60 km L38, FlxCorr)            ",None     ,'royalblue    ' ,              ),( )),

"""%s == 'fr925'                  """:
(("FIMR925:GSI(30 km, 0.5deg)                  ",None     ,'mediumblue  '  ,              ),( )),

"""%s == 'fzr1094'                """:
(("FIMZ R1094:GSI(30 km, 0.5deg)               ",None     ,'usafblue    '  ,              ),( )),

"""%s == 'fr1831gfsg8'            """:
(("FIM R1831:GFS G8 control                    ",None     ,'navy    '      ,              ),( )),

"""%s == 'fr1831plm1'             """:
(("FIM R1831:PLM1(vdiff=0.0)                   ",None     ,'usafblue    '  ,              ),( )),

"""%s == 'fr1831plm1vd05'         """:
(("FIM R1831:PLM1(vdiff=0.5)                   ",None     ,'mediumblue  '  ,              ),( )),

"""%s == 'fr1831plm1vd10'         """:
(("FIM R1831:PLM1(vdiff=0.5)                   ",None     ,'royalblue  '   ,              ),( )),

"""%s == 'fzr1163'                """:
(("FIMZ R1163:GSI(30 km, 0.5deg)               ",None     ,'royalblue  '   ,              ),( )),

"""%s == 'fr1174'                 """:
(("FIM R1174:GSI(30 km, 0.5deg)                ",None     ,'steelblue  '   ,              ),( )),

"""%s == 'fr1926'                 """:
(("FIM R1926:GSI(30 km, 0.5deg)                ",None     ,'navy    '      ,              ),( )),

"""%s == 'fr19261d'               """:
(("FIM R1926 (physics every time step vice every four) ",None     ,'mediumblue   '      ,              ),( )),

"""%s == 'fr2159int'              """:
(("FIM R2159(intfc_smooth=200)                 ",None     ,'steelblue    ' ,              ),( )),

"""%s == 'fr2176sig'              """:
(("FIM R2176(pure_sig=.true.)                  ",None     ,'usafblue    '  ,              ),( )),

"""%s == 'fr2093sig'              """:
(("FIM R2093(pure_sig=.true.;physics TENDency every time step)   ",None    ,'dodgerblue  ' ,              ),( )),

"""mf.find(%s,'fr2220g9')         """:
(("FIM G9(15km):EnKF|Hybrid -- hfip 2012 retro                   ",None    ,'dodgerblue '  ,              ),( )),

"""mf.find(%s,'fr2220g8')         """:
(("FIM G8(30km):EnKF|Hybrid -- hfip 2012 retro                   ",None     ,'usafblue '   ,              ),( )),

"""mf.find(%s,'fr2371hyb')        """:
(("FIM G8(30km,EnKF|Hyb):4th diff v=10 m/s - hfip 2012 retro     ",None     ,'powderblue ' ,              ),( )),

"""mf.find(%s,'fr2371vdiff')      """:
(("FIM G8(30km,EnKF|Hyb):4th diff v=30 m/s + upper boost - hfip 2012 retro  ",None  ,'mediumslateblue' ,              ),( )),

"""mf.find(%s,'fr2608g9')         """:
(("FIM G9(15km,4th diff):EnKF|Hybrid -- hfip 2012 retro          ",None     ,'powderblue  ' ,              ),( )),

"""mf.find(%s,'fr2647jpgf')       """:                   
(("FIM G8 Janjic PGF                                             ",None     ,'powderblue '   ,              ),( )),

"""%s == 'fr3162g9ops'       """:
(("FIM G9(15kmL64) IC:GSI -- hfip 2013 retro                     ",None     ,'royalblue  '   ,              ),( )),

"""%s == 'fr3162g9hyb'       """:
(("FIM G9(15kmL64) IC:NCEP Hybrid -- hfip 2013 retro             ",None     ,'navy    '      ,              ),( )),

"""%s == 'fr3162g9'       """:
(("FIM G9(15kmL64) IC:ESRL EnKF|Hybrid -- hfip 2013 retro        ",None     ,'powderblue '   ,              ),( )),

"""%s == 'fr3585v3'       """:
(("FIM G8(30kmL64) control -- 201105 ncep phys        ",None     ,'navy '   ,              ),( )),

"""%s == 'fr3585v4'       """:
(("FIM G8(30kmL64) 202105 ncep phys        ",None     ,'powderblue '   ,              ),( )),


# -- eps models

"""%s == 'gkmn'                   """:
(("GFS(T382) Eps GSI(T878)-EnKF(T382) Mean of 20 bers          ",None     ,'green  '      ,'d',              ),( )),

"""%s == 'rr2em'                   """:
(("GFS(T382) PSD RR2 Eps Mean of 10 members          ",None     ,'green  '      ,'d',              ),( )),

"""%s == 'rr2es'                   """:
(("GFS(T382) PSD RR2 Eps Spread of 10 members          ",None     ,'greenyellow '      ,'d',              ),( )),


"""mf.find(%s[0:4],'ge00')        """:
# 2012 (("GFS(T878) GSI(T878)-EnKF(T382) Control                         ",None     ,'yellowgreen'  ,'d',              ),( )),
# 2013
(("GFS(T1148) GSI(T1148)-EnKF(T574) Control                    ",None     ,'yellowgreen'  ,'d',              ),( )),

"""mf.find(%s [0:4],'fgmn') or mf.find(%s[0:4],'fgsp')  """:
(("01-10 FIM7 (60km) pert: EnKF(T878) Mean of 10 members  "        ,None     ,'usafblue' ,    'd',              ),( )),

"""%s == 'fg2mn' or %s == 'fg2sp' """:
(("12-21 GFS(254)Eps+10-FIM7:EnKF(T554) Mean of 21 members        ",None     ,'navy    '     ,'d',              ),( )),

"""%s[0:4] == 'gkmn' and year == 2011 """:
(("GFS(T574) Eps pert: EnKF(T878) Mean of 20 members              ",None     ,'green  '      ,'d',              ),( )),

"""%s[0:4] == 'gfsk'              """:
(("GFS(T574):EnKF(T574) Control                                   ",None     ,'greenyellow ' ,'d',              ),( )),

"""%s == 'gxmn'         """:
(("GFS(254)Eps:EnKF(T254) Mean of 20 members; Pmin only           ",None     ,'mediumblue  ' ,'d',              ),( )),

"""%s == 'gimn'         """:
(("GFS(254)Eps:EnKF(T254) Mean of 20 members; Pmin+IWRD           ",None     ,'usafblue  ',   'd',              ),( )),

"""%s == 'gkdt'         """:
(("GFS(T574):EnKF Mean:DET                                        ",None     ,'darkgreen  ',  'd',              ),( )),

"""%s == 'gksp'         """:
(("GFS:EnKF EPS Spread                                            ",None     ,'lightgoldenrodyellow' ,'s',      ),( )),

""" mf.find(%s,'eemn')    """:
(("EEMN - ECMWF:EPS [18kmL91] Mean of 50 members       ",None     ,'goldenrod' ,          ),('EEMN' , 77,0,12,6, )),

"""%s == 'edet'""":
#(("EDET - ECMWF HRES [IFS,det,T1279(16km)L137]     ",None    ,'gold'     ,         ),('EDET' , 77,0,12,6, )),
(("EDET - ECMWF HRES [09kmL137]     ",None    ,'gold'     ,         ),('EDET' , 77,0,12,6, )),

""" mf.find(%s,'eesp')         """:
(("EESP - ECMWF:EPS [18kmL91] Mean Spread                         ",None     ,'sienna    '   ,'s'               ),( )),

"""%s == 'nemn'         """:
(("GFS:Eps:GSI Mean of 21 members                             ",None     ,'greenyellow ' ,                  ),( )),

"""%s == 'nesp'         """: #lightgoldenrodyellow
(("GFS(254)Eps:GSI EPS Spread                                     ",None     ,'green'        ,                  ),( )),

"""%s == 'f8mn'         """:
(("FIM(30km):EnKF EPS Mean                                        ",None     ,'purple    '   ,'d' ,             ),( )),

"""%s == 'f8sp'         """:
(("FIM(30km):EnKF EPS Spread                                      ",None     ,'purple    '   ,'s',              ),( )),

"""%s == 'uemn'         """:
(("uKMO MOGREPS mean                                              ",None     ,'plum    '     ,                  ),( )),

"""%s == 'uedet'         """:
(("uKMO MOGREPS deterministic run from 00/12Z XML                ",None     ,'plum    '     ,                  ),( )),

# -- intensity

"""%s == 'ship'         """:
(("SHIPS (Stat Hurr Intensity Pred Sys)           ",None     ,'teal    '    , ),( )),

"""%s == 's5xx'         """:
(("2011 Updated STIPS Consensus=S511 + COTI + CHII (NRL)       ",None     ,'plum   '    , ),( )),


"""%s == 'st11'         """:
(("ST11 - STIPS (Stat Typhoon Intensity Pred Sys) 11 member ensemble      ",None     ,'teal  '      , ),('STIP',77,0,6,6,1 )),

"""%s == 'st5d'         """:
(("ST5D - STIPS (Stat Typhoon Intensity Pred Sys) 5 day   ",None     ,'teal  '      , ),( 'ST5D',77,0,6,6,1 )),


"""%s == 'lgem'         """:
(("LGEM - LGEM (Logistic Growth Eqn Mod)                 ",None     ,'purple   '  , ),( )),

"""%s == 'dshp'         """:
(("DSHP - Decay SHIPS (Logistic Growth Eqn Mod)                 ",None     ,'purple   '  , ),( )),

"""%s == 'lgea'         """:
(("LGEA - LGEM (Logistic Growth Eqn Mod) WPAC-GFS            ",None     ,'plum   '  , ),( )),

"""%s == 'lgen'         """:
(("LGEN - LGEM (Logistic Growth Eqn Mod) WPAC-NAVGEM         ",None     ,'royalblue '  , ),( )),


"""%s == 'ivcn'         """:
(("IVCN (Intensity Variable CON)                 ",None     ,'fuchsia   '  , ),( )),

"""%s == 'icnw'         """:
(("ICNW - Intensity Con Wiskey         ",None     ,'fuchsia   '  , ),( )),
"""%s == 'shf5'         """:
(("SHIFOR 5-d (Intensity CLIPER)                  ",None     ,'purple '     , ),( )),

"""%s == 'chip'         """:
(("CHIPS (MIT intensity)                          ",None     ,'fuchsia  '   , ),( )),


# -- consensus

"""%s == 'tvcn'         """:
#(("Track Variable CoNsensus                               ",None     ,'yellowgreen   '   ,  ),( )),
(("Track Variable CoNsensus                               ",None     ,'navy'   ,  ),( )),

"""%s == 'bcon'         """:
(("Best track CONsensus (conw:wpac;conu|tvcn:epac/lant)   ",None     ,'yellowgreen  '   ,  ),( )),

"""%s == 'conw'         """:
#(("""CONW ("con-whiskey") JTWC best consensus          """,None     ,'yellowgreen '      ,  ),( )),
(("""CONW ("con-whiskey") JTWC best consensus          """,None     ,'navy'      ,  ),( )),


# -- LAME - limited area models

"""%s[0:4] == 'hwrf'    """:
(("HWRF - NCEP HurrWRF LAM (LimitedAreaModel) 27:9:3 km               ",None     ,'mediumaquamarine' , 'd' ,'lame'  ),('HWRF' , 77,0,6,6, ) ),

"""%s[0:4] == 'hnvi'    """:
(("HNVI - NCEP HWRF - no VortexInit 27:9:3 km               ",None     ,'cadetblue' , 'd' ,'lame'  ),('HNVI' , 77,0,6,6, ) ),

"""%s[0:4] == 'lasw'    """:
(("LASW - LaSW ARW LAM (LimitedAreaModel) 18:6:2 km               ",None     ,'cornflowerblue' , 'd' ,'lame'  ),('LASW' , 77,0,6,6, ) ),

"""%s[0:4] == 'hmon'    """:
(("HMON - NCEP HurrMON LAM (LimitedAreaModel) 27:9:3 km               ",None     ,'teal' , 'd' ,'lame'  ),('HMON' , 77,0,6,6, ) ),

"""%s[0:4] == 'hwfi'    """:
(("HWRF LAM (6h interp)                                  ",None     ,'violetred ' , 'd' ,'lame'  ),( )),

"""%s[0:4] == 'gfdl'    """:
(("GFDL LAM (Limited-Area-Model)                         ",None     ,'plum      ' , 'd' ,'lame'  ),( )),

"""%s[0:4] == 'gfdi'    """:
(("GFDL LAM (6h interp)                                  ",None     ,'plum      ' , 'd' ,'lame'  ),( )),

"""%s[0:4] == 'ghmi'    """:
(("GFDL LAM (6h interp + 24-h no intensity offset)           ",None     ,'purple     ' , 'd' ,'lame'  ),( )),


"""%s[0:4] == 'gfdn'    """:
(("GFDN - GFDL LAM (LimitedAreaModel) embedded in NAVGEM                         ",None     ,'plum      ' , 'd' ,'lame'  ),( )),

"""%s[0:4] == 'cotc'    """:
(("COTC - COAMPS TC LAM (LimitedAreaModel) embedded in NAVGEM                     ",None     ,'teal    ' , 'd' ,'lame'  ),( )),

"""%s[0:4] == 'ctcx'    """:
(("CTCX - COAMPS TC LAM (LimitedAreaModel) embedded in GFS vice NAVGEM                     ",None     ,'mediumseagreen    ' , 'd' ,'lame'  ),( )),

"""%s[0:4] == 'h3gp'    """:
(("HWRF 3-km LAM (Limited-Area-Model)                    ",None     ,'fuchsia   ' , 'd' ,'lame'  ),( )),

"""%s[0:4] == 'ahw4'    """:
(("ARW LAM (Limited-Area-Model)                          ",None     ,'wheat     ' , 'd' ,'lame'  ),( )),

"""%s[0:4] == 'uwn8'    """:
(("UWisc LAM (Limited-Area-Model)                        ",None     ,'usafblue  ' , 'd' ,'lame'  ),( )),

# -- cliper
"""%s == 'clp5'         """:
(("CLP5 - NHC 5 d CLIPER                             ",None     ,'sienna  '  , ),( )),

"""%s == 'c120'         """:
(("C120 JTWC 5 d CLIPER                           ",None     ,'chocolate  '  , ),( )),

"""%s == 'clip5'         """:
(("CLIP5 - JTWC/NHC 5 d CLIPER                        ",None     ,'sienna  '  , ),( )),

"""%s == 'clp3'         """:
(("CLP3 - JTWC/NHC 3 d CLIPER LOCAL.py w/ CARQ input             ",None     ,'peru  '  , ),( )),

"""%s == 'clpb'         """:
(("JTWC/NHC 3-d CLIPER LOCAL.py with BEST TRACK      ",None     ,'sienna'  , ),( )),

"""%s == 'clpm'         """:
(("JTWC/NHC 3-d CLIPER LOCAL.py w/ CARQ tau0 motion   ",None     ,'tan'  , ),( )),

"""%s == 'clip'         """:
(("CLIP - JTWC/NHC 3 d CLIPER operational                ",None     ,'chocolate'  , ),( )),
# -- other

"""%s == 'hfip'         """:
(("HFIP Baseline (2006-2008)                             ",None     ,'grey  '  , ),( )),

"""%s == 'hfipj'         """:
(("HFIP JTWC Baseline (2006-2008)                             ",None     ,'grey  '  , ),( )),

"""%s == 'hfip20'       """:
(("20% improvement over HFIP Baseline                   ",None     ,'black  '  , ),( )),

"""%s == 'hfipskill'    """:
(("HFIP Skill Baseline (2006-2008)                       ",None     ,'    '    , ),( )),

"""%s == 'hfipskill20'  """:
(("20%% improvement over HFIP Skill Baseline             ",None     ,'    '    , ),( )),


# -- RAP experiments 

"""%s == 'rapc'         """:
(("RAP(12 km) : GFS Cold Start      ",None , 'red '     ,  ),('NNNN',77,0,3,3, )),

"""%s == 'rpao'         """:
((" RAP(12 km) : Conv + AIRS obs    ",None , 'red '     ,  ),('NNNN',77,0,3,3, )),

"""%s == 'rpco'         """:
(("RAP(12 km) : Conv only           ",None , 'green '   ,  ),('NNNN',77,0,3,3, )),

# -- template
"""                     """:
(("                                                      ",None     ,'    '      ,              ),( )),


# -- WAF Paper

"""mf.find(%s,'tecm500')""":
(("ECMWF GFDL tracker   ",None    ,'yellow'           ,   ),('NNNN' , 77,0,12,6, )),



    }

    # -- option for fitting masks # add additional flag to properly set the start syn hour for 00|06|12 trackers
    #
    exprsP1={
        """mf.find(%s[len(%s)-2:],'00') and %s != 'ge00'  """: ((-2,-2),"%s - 00-h interp  ","%s00",0),
        """mf.find(%s[len(%s)-2:],'06')                   """: ((-2,-2),"%s - 06-h interp  ","%s06",1),
        """mf.find(%s[len(%s)-2:],'12')                   """: ((-2,-2),"%s - 12-h interp  ","%s12",0),
    }

    exprsP2={
        """var=%s; eko=(len(var) == 5 and var[-1] == 'g') """: ((-1,-1),"%s - LGEM",      "%sg",-1),
        """var=%s; eko=(len(var) == 5 and var[0]  == 't') """: ((1,5),  "%s - TIM (GFDL) Tracker","t%s",-1),
        """var=%s; eko=(len(var) == 5 and var[0]  == 'm') """: ((1,5),  "%s - MIKE (ESRL) Tracker","m%s",-1),
        """var=%s; eko=(len(var) == 5 and var[0]  == 'n') """: ((1,5),  "%s - NCEP(TM) Tracker","n%s",-1),
        """var=%s; eko=(len(var) == 7 and var[0]  == 't') """: ((1,5),  "%s - TIM (GFDL) Tracker","t%s",-1),
        """var=%s; eko=(len(var) == 7 and var[0]  == 'm') """: ((1,5),  "%s - MIKE (ESRL) Tracker","m%s",-1),
    }


    def __init__(self,
                 aid,
                 label=None,
                 defcolor='navy',
                 color=None,
                 mark='d',
                 vmaxCorrScheme='global',
                 year=2011,
                 AdeckName='NNNN',
                 AdeckNum=77,
                 StartSynHourModel=0,
                 DdtgModelTracker=6,
                 DtauModel=6,
                 warn=1,
                 ):

        self.aid=aid
        self.oname=aid
        self.label=label
        self.color=color
        self.mark=mark
        self.vmaxCorrScheme=vmaxCorrScheme

        self.warn=warn


        # -- vars from atcf.py may or may not be needed -- in localvdstat2.py to do vda -p ls

        self.AdeckName=AdeckName
        self.AdeckNum=AdeckNum
        self.StartSynHourModel=StartSynHourModel
        self.DdtgModelTracker=DdtgModelTracker
        self.DtauModel=DtauModel

        # -- check if matches a specific aid
        #
        self.getBase(aid)

        # -- first check if post process form
        #    P2 -- mf|tm trkN
        #    p1 -- 00,06,12
        #
        self.getPost(aid,self.exprsP2,doBase=1)
        self.getPost(aid,self.exprsP1,doBase=1)
        
        # -- label override
        if(aid == 'tecm500' or aid == 'tecm5'):
            self.label="ECMWF IFS  -- GFDL tracker 0.25deg"
        elif(aid == 'tera500' or aid == 'tera5'):
            self.label="ECMWF ERA5 -- GFDL tracker 0.25deg"
        elif(aid == 'hwrf' or aid == 'hwrf00'):
            self.label='HWRF'
        elif(aid == 'avno' or aid == 'avno00'):
            self.label= 'GFS'
        elif(aid == 'emdt' or aid == 'emdt00'):
            self.label= 'ECMWF IFS  -- ECMWF tracker 0.10deg'

        if(self.label == None and self.warn):
            print "WWW ATCF.AidProp got Nada for aid: ",aid," using defaults"
            self.color=defcolor
            self.label="WWW AidProp class has no setting for :%s"%(aid)

        if(self.AdeckName == 'NNNN'): self.AdeckName=aid.upper()

        # -- blank out data dics to lighten object
        #	
        self.exprs={}
        self.exprsP1={}
        self.exprsP2={}

        # -- from Aid() class
        #
        if(not(hasattr(self,'VmaxOnly'))): self.VmaxOnly=0 
        self.TrackOnly=0
        self.fcnoload=(-98.8,-988.8,-98.8,-998.8)

    def getChkType(self,k):

        ctype=0
        hasfind=mf.find(k,'find')
        kkor=len(k.split('or'))-1
        kkand=len(k.split('and'))-1
        kkeq=len(k.split('=='))-1
        if((kkeq == 1 or hasfind) and (kkor ==  0 and kkand == 0)): ctype=1
        #print 'kkkkkkkkkkkk kkor',kkor,'hasfind: ',hasfind,'kkand: ',kkand,'kkeq: ',kkeq,'k: ',k,'ctype: ',ctype

        return(ctype)


    def getBase(self,aid):

        self.gotbase=0
        self.gotpost=0	
        eko=0
        kk=self.exprs.keys()
        for n in range(0,len(kk)):
            k=kk[n]

            ko=k.replace('%s',"""'%s'"""%(aid))
            exec("eko=(%s)"%(ko))
            if(eko):
                ff=self.exprs[k][0]
                ff1=self.exprs[k][1]
                lf=len(ff)

                title=ff[0].strip()
                oname=ff[1]

                if(lf >= 3):
                    color=ff[2].strip()

                mark=self.mark
                if(lf >= 4):
                    mark=ff[3].strip()

                vmaxCorrScheme=self.vmaxCorrScheme
                if(lf >= 5):
                    vmaxCorrScheme=ff[4]

                ftitle=title.strip()

                if(oname != None): ftitle="%s - %s"%(oname,title)
                if(oname == None): oname=aid

                self.color=color
                self.label=ftitle
                self.oname=oname
                self.mark=mark
                self.vmaxCorrScheme=vmaxCorrScheme
                self.gotbase=1

                # -- get properties in original atcf.card 
                #
                if(len(ff1) == 5):
                    self.AdeckName=ff1[0]
                    self.AdeckNum=ff1[1]
                    self.StartSynHourModel=ff1[2]
                    self.DdtgModelTracker=ff1[3]
                    self.DtauModel=ff1[4]
                elif(len(ff1) == 6):
                    self.AdeckName=ff1[0]
                    self.AdeckNum=ff1[1]
                    self.StartSynHourModel=ff1[2]
                    self.DdtgModelTracker=ff1[3]
                    self.DtauModel=ff1[4]
                    self.VmaxOnly=ff1[5]


                break


    def getPost(self,aid,exprsP,doBase=1,verb=0):

        # -- if got specific aid bail
        #
        if(self.gotbase and not(doBase)):
            if(verb): print 'gotbase in getPost aid:',aid
            return

        self.gotpost=0
        gotvar=0
        kk=exprsP.keys()

        for n in range(0,len(kk)):
            k=kk[n]
            ko=k.replace('%s',"""'%s'"""%(aid))
            if(ko[0:3] == 'var'):
                exec(ko)
                if(eko):  gotvar=1
            else:
                exec("eko=(%s)"%(ko))

            if(eko):
                self.gotpost=1
                rdL=exprsP[k][0]
                (bL,eL)=rdL
                if(bL < 0):
                    baid=aid[0:len(aid)+bL]
                else:
                    baid=aid[bL:eL]

                # -- get base
                #
                if(doBase):
                    self.getBase(baid)

                # -- get post 
                #
                ff=exprsP[k]

                if(hasattr(self,'label')):
                    if(not(self.label == None)):
                        label=ff[1]%(self.label)
                        label=label.strip()
                        self.label=label
                        

                if(hasattr(self,'oname')):
                    oname=ff[2]%(baid)
                    oname=oname.strip()
                    self.oname=oname
                    if(self.label != None):
                        # -- replace name with   new one
                        self.label=self.label.replace(baid.upper(), self.oname.upper())

                self.gotbase=0

                # -- get post flag...if = 1, then set the StartSynHourModel if DtgModelTracker = 2
                #
                postflag=ff[-1]
                if(postflag == 1):
                    if(hasattr(self,'DdtgModelTracker') and self.DdtgModelTracker == 12):
                        self.StartSynHourModel=6

                return


    def getAidPropCard(self,model,verb=1):

        try:
            card=AidPropCards[model]
        except:
            if(verb): print 'no AidProp for model: ',model,' in ATCF getAidPropCard'
            card="uuuu   ! ! unknown aid  !  !    !     !    !    !    !"
        return(card)



class EaidProperties(MFbase):

    def __init__(self,source):

        if(source == 'gfsenkf'):
            self.modeltitle='GFS(T382) EnKF'
        elif(source == 'ncep'):
            self.modeltitle='GFS(T126) E`aT`n'
        elif(source == 'ecmwf'):
            self.modeltitle='ECMWF(T399) EPS'
        else:
            self.modeltitle='unknown'

class aidDescTechList(MFbase):

    aidDescJtwc={
'ABRF':"""BOM Brisbane""",
'AC00':"""GEFS Control Run""",
'ACEI':"""BoM ACCESS (unified model) vortex tracker (NHC interpolator)""",
'ACES':"""CCESS (unified model) vortex tracker""",
'ADRM':"""BOM Darwin""",
'AEMI':"""GEFS Ensemble Mean (Original Members)(interpolated)""",
'AEMN':"""GEFS Ensemble Mean (Original Members)""",
'AF12':"""MM5 Coarse resolution (Interpolated 12 hours)""",
'AFS5':"""MM5 STIPS intensity output (with OHC)""",
'AFUI':"""AFWA Unified Model (UKMET) (NHC interpolator)""",
'AFUM':"""AFWA Unified Model (UKMET)""",
'AFW1':"""AFWA MM5 45 km resolution, cng to WRF May 2010""",
'AFW2':"""AFWA MM5 (NHC Interpolator)(2nd interpolation)""",
'AFWI':"""AFWA MM5 (NHC Interpolator)""",
'AHN2':"""GFS wind radii aid, second interpolation""",
'AHNI':"""GFS Wind radii aid""",
'AP01':"""GEFS Ensemble Member 1""",
'AP02':"""GEFS Ensemble Member 2""",
'AP03':"""GEFS Ensemble Member 3""",
'AP04':"""GEFS Ensemble Member 4""",
'AP05':"""GEFS Ensemble Member 5""",
'AP06':"""GEFS Ensemble Member 6""",
'AP07':"""GEFS Ensemble Member 7""",
'AP08':"""GEFS Ensemble Member 8""",
'AP09':"""GEFS Ensemble Member 9""",
'AP10':"""GEFS Ensemble Member 10""",
'AP11':"""GEFS Ensemble Member 11""",
'AP12':"""GEFS Ensemble Member 12""",
'AP13':"""GEFS Ensemble Member 13""",
'AP14':"""GEFS Ensemble Member 14""",
'AP15':"""GEFS Ensemble Member 15""",
'AP16':"""GEFS Ensemble Member 16""",
'AP17':"""GEFS Ensemble Member 17""",
'AP18':"""GEFS Ensemble Member 18""",
'AP19':"""GEFS Ensemble Member 19""",
'AP20':"""GEFS Ensemble Member 20""",
'APRF':"""BOM Perth""",
'ARP2':"""MeteoFrance Arpege regional model tracker (Second interpolation)""",
'ARPG':"""MeteoFrance Arpege regional model tracker""",
'ARPI':"""MeteoFrance Arpege regional model tracker (Interpolated)""",
'AVN2':"""NCEP AVN TC vortex tracker (NHC interpolator)(2nd interpolation)""",
'AVNI':"""NCEP AVN TC vortex tracker (NHC interpolator)""",
'AVNO':"""NCEP AVN TC vortex tracker""",
'AVS5':"""GFS STIPS intensity output (with OHC)""",
'BABJ':"""CMA Beijing""",
'BAMD':"""Beta and Advection model, deep (NHC)""",
'BAMM':"""Beta and Advection model, medium (NHC)""",
'BAMS':"""Beta and Advection model, shallow (NHC)""",
'BATS':"""Korean Model""",
'BCGZ':"""CMA Guanzhou""",
'BLND':"""Average of several aids (hybrid)""",
'C01C':"""COAMPS-TC Ensemble Member 1""",
'C02C':"""COAMPS-TC Ensemble Member 2""",
'C03C':"""COAMPS-TC Ensemble Member 3""",
'C04C':"""COAMPS-TC Ensemble Member 4""",
'C05C':"""COAMPS-TC Ensemble Member 5""",
'C06C':"""COAMPS-TC Ensemble Member 6""",
'C07C':"""COAMPS-TC Ensemble Member 7""",
'C08C':"""COAMPS-TC Ensemble Member 8""",
'C09C':"""COAMPS-TC Ensemble Member 9""",
'C10C':"""COAMPS-TC Ensemble Member 10""",
'C120':"""120 Hour CLIPER (Aberson, HRD)""",
'C12N':"""Consensus; AVNI, EGRI, ECMI, GFNI, JGSI, NGPI/NVGI, WBAI""",
'CARQ':"""Combined ARQ Position""",
'CCON':"""Experimental Bias Corrected Consensus (Goerss JHT, 2007)""",
'CCWF':"""Combined Confidence Weighted Forecast""",
'CEMI':"""Canadian model Ensemble Mean (interpolated)""",
'CEMN':"""Canadian model Ensemble Mean """,
'CHII':"""Emanuel's Intensity Program (Interpolated)""",
'CHIP':"""Emanuel's Intensity Program""",
'CLAU':"""Aus/SE Indian Ocean CLIPER (Neumann, 2000)""",
'CLIM':"""Climatology from TYAN78 total data set""",
'CLIP':"""CLIPER""",
'CLP3':"""3-d CLImatology-PERsistance model""",
'CLP5':"""CLImatology-PERsistance model 5-day""",
'CLSI':"""SW Indian Ocean CLIPER (Neumann, 2001)""",
'CLSW':"""SW Pacific Ocean CLIPER (Neumann, 2000)""",
'CMC':"""Canadian Model""",
'CMC2':"""Canadian Model (NHC Interpolator) (2nd interpolation)""",
'CMCI':"""anadian Model (NHC Interpolator)""",
'CMES':"""CON-MESO Intensity Consensus of GFNI, COTI, CTCI, HWFI-July2013""",
'CMSD':"""CON-MESO-Statistical-Dynamical Intensity Consensus of GFNI, COTI, CTCI, HWFI, DSHA, LGEA, LGEM, DSHN - July2013""",
'CNGA':"""ATCF Numerical Model Consensus""",
'CNGE':"""ATCF Numerical Model Consensus""",
'CNGJ':"""ATCF Numerical Model Consensus""",
'CNGN':"""ATCF Numerical Model Consensus""",
'CNRA':"""ATCF Numerical Model Consensus""",
'CNRC':"""ATCF Numerical Model Consensus""",
'CNRG':"""ATCF Numerical Model Consensus""",
'CNRJ':"""ATCF Numerical Model Consensus""",
'COEI':"""COAMPS (Interpolated)""",
'COF2':"""COAMPS-TC Second Interpolated Western Pacific - NAVGEM Driven (Legacy)""",
'COFI':"""COAMPS-TC Interpolated Western Pacific - NAVGEM Driven (Legacy)""",
'COFN':"""COAMPS-TC Western Pacific - NAVGEM Driven (Legacy)""",
'COID':"""COAMPS Indonesia""",
'COIN':"""COAMPS Indian Ocean""",
'COKO':"""COAMPS Korea""",
'CON6':"""ATCF Numerical Model Consensus""",
'CON7':"""ATCF Numerical Model Consensus""",
'CON8':"""ATCF Numerical Model Consensus""",
'CONC':"""Consensus; NGPI, EGRI, JGSI, GFNI, JTYI, AFWI, COWI, WBAI, TCLI, JAVI (temp)""",
'CONG':"""Consensus; NGPI, EGRI, JGSI, JAVI""",
'CONJ':"""JTWC Consensus; NGAI, EGAI, JGAI, GFAI, JTYI, AFWI, COWI, WBAI, TCLI, JAVI""",
'CONR':"""ATCF Numerical Regional Model Consensus""",
'CONT':"""ATCF Numerical Model Consensus""",
'CONU':"""Consensus; NGPI, EGRI, JGSI, GFNI, JTYI, AFWI, COWI""",
'CONW':"""Consensus; AVNI,EGRI,ECMI,GFNI,JGS1,NVGI,CTCI,HWFI,AEMI,JENI""",
'CON_':"""Consensus; NGPI, EGRI, JGSI, GFNI, JTYI""",
'COSH':"""Consensus; NGPI, EGRI, JGSI, JAVI, GFNI, TLAI, LAPI""",
'COT2':"""COAMPS-TC Second Interpolated Western Pacific - GFS Driven (Operational - FNMOC)""",
'COTC':"""COAMPS-TC Western Pacific - NAVGEM Driven (Operational - FNMOC)""",
'COTI':"""COAMPS-TC Interpolated Western Pacific - NAVGEM Driven (Operational - FNMOC)""",
'COW2':"""COAMPS Western Pacific (NHC interpolator)(2nd interpolation)""",
'COWI':"""COAMPS Western Pacific (NHC interpolator)""",
'COWP':"""COAMPS Western Pacific""",
'CSUM':"""CSU-84 statistical model""",
'CTC2':"""COAMPS-TC Second Interpolated Western Pacific - GFS Driven (Experimental)""",
'CTCI':"""COAMPS-TC Interpolated Western Pacific - GFS Driven (Experimental - NRL)""",
'CTCX':"""COAMPS-TC Western Pacific - GFS Driven (Experimental NRL cold starts began 2014014218)""",
'CTIN':"""COAMPS-TC Ensemble Intensity Consensus (Uninterpolated Members)""",
'CTMN':"""COAMPS-TC Ensemble Mean (Uninterpolated Members)""",
'DAVE':"""Weighted average of dynamic aids""",
'DCON':"""LDO Selective Consensus""",
'DEMS':"""IMD New Delhi""",
'DRCL':"""Wind radii cliper (CIRA/NOAA/NRL)""",
'DSHA':"""Decay SHIPS model to predict over land decay rates w/GFS fields""",
'DSHN':"""Decay SHIPS model to predict over land decay rates w/NVGM fields""",
'DSHP':"""Decay SHIPS model to predict over land decay rates""",
'DYAV':"""Average of NGPS,GFDL,UKMO""",
'ECM2':"""ECMWF model (Interpolated 12 hours)""",
'ECM3':"""ECMWF model (Interpolated 18 hours) Capability added 12Aug08 to incrs CONW members""",
'ECM4':"""ECMWF model (Interpolated 24 hours) Capability added 12Aug08 to incrs CONW members""",
'ECME':"""ECMWF control (T254)""",
'ECMF':"""European Center For Medium Range Forecasting""",
'ECMI':"""ECMWF model (Interpolated)""",
'ECMO':"""ECMWF Model [GTS Tracker]""",
'ECO2':"""ECMWF Model Second Interpolated [GTS Tracker]""",
'ECOI':"""ECMWF Model First Interpolated [GTS Tracker]""",
'EEM2':"""ECMWF Model Ensemble Mean EPS (NHC interpolator) (2nd interpolation)""",
'EEM3':"""ECMWF Model Ensemble Mean EPS (NHC interpolator) (3rd interpolation - added 17 May 15)""",
'EEM4':"""ECMWF Model Ensemble Mean EPS (NHC interpolator) (4th interpolation - added 17 May 15)""",
'EEMI':"""ECMWF Model Ensemble Mean EPS (NHC interpolator)""",
'EEMN':"""ECMWF Model Ensemble Mean EPS""",
'EEMO':"""ECMWF Model Ensemble Mean EPS [GTS Tracker]""",
'EGAI':"""Corrected SAFA tracker (interpolated)""",
'EGR2':"""Bracknell (NHC interpolator)(2nd interpolation)""",
'EGRA':"""Corrected SAFA tracker""",
'EGRI':"""Bracknell (NHC interpolator)""",
'EGRR':"""Bracknell""",
'EGRT':"""Bracknell (translated from SAFA)""",
'EGRX':"""Bracknell 120 hr forecast""",
'EMX':"""ECMWF Model (GFS Tracker) parent tracker	   """,
'EMX2':"""ECMWF Model (GFS Tracker) 12-hour interpolation""",
'EMXI':"""ECMWF Model (GFS Tracker) 6-hour interpolation """,
'ETA':"""NCEP ETA Model Tracker""",
'ETAI':"""NCEP ETA Interpolated""",
'FBAF':"""Beta and Advection model, deep FNMOC run""",
'FBAM':"""Beta and Advection model, deep""",
'FI92':"""ESRL FIM9 TC vortex tracker (Second interpolation)""",
'FI9I':"""ESRL FIM9 TC vortex tracker (Interpolated)""",
'FIM9':"""ESRL FIM9 TC vortex tracker""",
'F7SS':"""ESRL FIM7 SubSeasonal TM tracker Version 2""",
'F7S3':"""ESRL FIM7 SubSeasonal TM tracker Version 3""",
'FV3E':"""ESRL FV3 with GFS physics dx~27 km""",
'FV3G':"""ESRL FV3 with Grell-Freitas (GF) physics dx~27 km""",
'FMEE':"""METEO France La Reunion""",
'FUJI':"""JTWC Fuji model (Fujiwhara)""",
'GF32':"""Experimental 1-D Coupled GFDN (NHC interpolator) (2nd interpolation)""",
'GF3C':"""Experimental 1-D Coupled GFDN  """,
'GF3I':"""Experimental 1-D Coupled GFDN (NHC Interpolator) """,
'GF52':"""GFDL v5 model (Interpolated 12 hours)""",
'GF5I':"""GFDL v5 model (Interpolated 06 hours)""",
'GFAI':"""Navy version of GFDL model, corrected SAFA (interpolated)""",
'GFD5':"""GFDL v5 model""",
'GFDE':"""Navy version of GFDL model (extrapolated)""",
'GFDI':"""GFDL extrapolated 6 hrs""",
'GFDK':"""Korean GFDL Model""",
'GFDL':"""GFDL model""",
'GFDN':"""Navy version of GFDL model""",
'GFDO':"""GFDL OFF""",
'GFDT':"""GFDL model with thermodynamic output""",
'GFN2':"""Navy version of GFDL model (NHC interpolator)(2nd interp)""",
'GFNI':"""Navy version of GFDL model (NHC interpolator)""",
'GFS5':"""GFDN STIPS intensity output (with OHC)""",
'GFTI':"""Interpolated GFDL model with thermodynamic output""",
'GHMI':"""GFDL model with Intensity adjustment (Interpolated 06 hours)""",
'GHT2':"""GFDL wind radii aid, second interpolation""",
'GHTI':"""GFDL Wind radii aid""",
'GLAV':"""Average of NGPS,EGRR,JGSM""",
'GPMI':"""GFDL Ensemble mean extrapolated 6 hrs""",
'GUNA':"""NHC Consensus Interpolated (AVNI+GHMI+EGRI/2+NGPI)""",
'GUNS':"""NHC Numerical Model Consensus""",
'HHF2':"""HWRF Wind radii aid, second interpolation""",
'HHFI':"""HWRF Wind radii aid""",
'HPAC':"""Half Persistance And Half Climatology""",
'HRDW':"""HRD Wind Analysis""",
'HWF2':"""HWRF model (Interpolated 12 hours)""",
'HWFI':"""HWRF model (Interpolated 06 hours)""",
'HWMI':"""HWRF Ensemble Mean (Interpolated 06 hours)""",
'HWMN':"""HWRF Ensemble """,
'HWRF':"""HWRF model""",
'J120':"""JTWC 120 hr forecast""",
'JAV2':"""AVN Fiorino vortex tracker (2nd NHC interpolation) """,
'JAVI':"""AVN Fiorino vortex tracker (NHC interpolator)""",
'JAVN':"""FIORINO AVNF Tracker""",
'JEN2':"""Japanese Global Spectral Model ENSEMBLE (2nd interpolation)""",
'JENI':"""Japanese Global Spectral Model ENSEMBLE (Interpolated)""",
'JENS':"""Japanese Global Spectral Model ENSEMBLE""",
'JGAI':"""JGSM (NHC interpolator from SAFA JGSA)""",
'JGS2':"""JGSM (NHC interpolator from ATCF JGSM)(2nd interpolation)""",
'JGS5':"""JGSM STIPS intensity output (with OHC)""",
'JGSA':"""SAFA modified tracker""",
'JGSE':"""JGSM (extrapolated)""",
'JGSI':"""JGSM (NHC interpolator from ATCF JGSM)""",
'JGSM':"""Japanese Global Spectral Model""",
'JGST':"""JGSM (translated from SAFA)""",
'JJG2':"""FIORINO JGSM Tracker, 2nd Interpolation""",
'JJGI':"""FIORINO JGSM Tracker  Interpolated                   """,
'JJGS':"""FIORINO JGSM Tracker""",
'JMRF':"""MRF Fiorino vortex tracker (NHC interpolator)""",
'JNGI':"""FIORINO Interp NGPF Tracker""",
'JNGP':"""FIORINO NOGAPS Tracker""",
'JNV2':"""FIORINO Interp NAVGEM Tracker, 2nd Interpolation""",
'JNVG':"""FIORINO NAVGEM Tracker""",
'JNVI':"""FIORINO Interp NAVGEM Tracker""",
'JT92':"""JTWC92""",
'JTME':"""JTYM (extrapolated)""",
'JTW2':"""JTWC Interpolated Forecast (12 hour)""",
'JTWC':"""JTWC official forecast""",
'JTWI':"""JTWI JTWC Interpolated Track""",
'JTY2':"""JTYM (NHC interpolator)(2nd interpolation)""",
'JTYI':"""JTYM (NHC interpolator)""",
'JTYM':"""Japanese Typhoon Model""",
'JTYT':"""JTYM (translated from SAFA)""",
'JUK2':"""UKMO Fiorino vortex tracker (NHC interpolator)(2nd interpolation)""",
'JUKI':"""UKMO Fiorino vortex tracker (NHC interpolator)""",
'JUKM':"""FIORINO UKMO Tracker""",
'K106':"""KMA T106 Global Model (Low Resolution)""",
'K10I':"""KMA T106 Global Model interpolated (Low Resolution)""",
'K213':"""KMA T213 Global Model (High resolution)""",
'K21I':"""KMA T213 Global Model interpolated (High resolution)""",
'K426':"""KMA T426 Global Model (Low Resolution)""",
'K42I':"""KMA T426 Global Model interpolated (Low Resolution)""",
'KBAI':"""KMA DBAR Barotropic Model interpolated""",
'KBAR':"""KMA DBAR Barotropic Model""",
'KREG':"""KMA RDPS Regional Model""",
'KREI':"""KMA RDPS Regional Model interpolated""",
'LBAR':"""LBAR""",
'LGEA':"""SHIPS Logistic Growth Equation (LGE) forecast w/GFS""",
'LGEM':"""SHIPS Logistic Growth Equation (LGE) forecast model""",
'LGEN':"""SHIPS Logistic Growth Equation (LGE) forecast w/NVGM""",
'MBAF':"""Beta and Advection model, medium FNMOC run""",
'MBAM':"""Beta and Advection model, medium""",
'ME01':"""MEPS 4 km Ensemble Member 1""",
'ME02':"""MEPS 4 km Ensemble Member 2""",
'ME03':"""MEPS 4 km Ensemble Member 3""",
'ME04':"""MEPS 4 km Ensemble Member 4""",
'ME05':"""MEPS 4 km Ensemble Member 5""",
'ME06':"""MEPS 4 km Ensemble Member 6""",
'ME07':"""MEPS 4 km Ensemble Member 7""",
'ME08':"""MEPS 4 km Ensemble Member 8""",
'ME09':"""MEPS 4 km Ensemble Member 9""",
'ME10':"""MEPS 4 km Ensemble Member 10""",
'MEM2':"""MEPS 4 km Ensemble Mean (2nd Interpolation)""",
'MEMI':"""MEPS 4 km Ensemble Mean (Interpolated)""",
'MEMN':"""MEPS 4 km Ensemble Mean (Uninterpolated Members)""",
'MRCL':"""Wind radii cliper (McCadie - Atlantic only)""",
'MRFO':"""NCEP MRF off time""",
'MYOC':"""Forecaster Created Consensus Guidance (any model combination)""",
'N01I':"""NGPS Ensemble Member 1 (Interpolated)""",
'N02I':"""NGPS Ensemble Member 2 (Interpolated)""",
'N03I':"""NGPS Ensemble Member 3 (Interpolated)""",
'N04I':"""NGPS Ensemble Member 4 (Interpolated)""",
'N05I':"""NGPS Ensemble Member 5 (Interpolated)""",
'N06I':"""NGPS Ensemble Member 6 (Interpolated)""",
'N07I':"""NGPS Ensemble Member 7 (Interpolated)""",
'N08I':"""NGPS Ensemble Member 8 (Interpolated)""",
'N09I':"""NGPS Ensemble Member 9 (Interpolated)""",
'N10I':"""NGPS Ensemble Member 10 (Interpolated)""",
'N11I':"""NGPS Ensemble Member 11 (Interpolated)""",
'N12I':"""NGPS Ensemble Member 12 (Interpolated)""",
'N13I':"""NGPS Ensemble Member 13 (Interpolated)""",
'N14I':"""NGPS Ensemble Member 14 (Interpolated)""",
'N15I':"""NGPS Ensemble Member 15 (Interpolated)""",
'N16I':"""NGPS Ensemble Member 16 (Interpolated)""",
'N17I':"""NGPS Ensemble Member 17 (Interpolated)""",
'N18I':"""NGPS Ensemble Member 18 (Interpolated)""",
'N19I':"""NGPS Ensemble Member 19 (Interpolated)""",
'N20I':"""NGPS Ensemble Member 20 (Interpolated)""",
'NCON':"""Numerical Consensus (SAFA)""",
'NEMN':"""NGPS Ensemble Mean (Interpolated Members)""",
'NFFN':"""FMS Nandi""",
'NG01':"""NGPS Ensemble Member 1""",
'NG02':"""NGPS Ensemble Member 2""",
'NG03':"""NGPS Ensemble Member 3""",
'NG04':"""NGPS Ensemble Member 4""",
'NG05':"""NGPS Ensemble Member 5""",
'NG06':"""NGPS Ensemble Member 6""",
'NG07':"""NGPS Ensemble Member 7""",
'NG08':"""NGPS Ensemble Member 8""",
'NG09':"""NGPS Ensemble Member 9""",
'NG10':"""NGPS Ensemble Member 10""",
'NG11':"""NGPS Ensemble Member 11""",
'NG12':"""NGPS Ensemble Member 12""",
'NG13':"""NGPS Ensemble Member 13""",
'NG14':"""NGPS Ensemble Member 14""",
'NG15':"""NGPS Ensemble Member 15""",
'NG16':"""NGPS Ensemble Member 16""",
'NG17':"""NGPS Ensemble Member 17""",
'NG18':"""NGPS Ensemble Member 18""",
'NG19':"""NGPS Ensemble Member 19""",
'NG20':"""NGPS Ensemble Member 20""",
'NGAI':"""Corrected SAFA tracker (Interpolated)""",
'NGM':"""NCEP NGM Model Tracker""",
'NGP2':"""NOGAPS tc vortex tracker (NHC interpolator)(2nd interpolation)""",
'NGPA':"""Corrected SAFA tracker""",
'NGPE':"""NOGAPS tc vortex tracker (extrapolated)""",
'NGPI':"""NOGAPS tc vortex tracker (NHC interpolator)""",
'NGPR':"""NOGAPS tc vortex tracker (ATCF)""",
'NGPS':"""NOGAPS tc vortex tracker""",
'NGPT':"""NOGAPS tc vortex tracker (translated from SAFA)""",
'NGPX':"""NOGAPS 120 hr forecast""",
'NGS5':"""NOGAPS STIPS intensity output (with OHC)""",
'NGSD':"""STIPS - decay version (CIRA/NOAA/NRL) run on NGPI""",
'NRPI':"""NORAPS vortex tracker (Indian)""",
'NRPP':"""NORAPS vortex tracker (Pacific)""",
'NSOF':"""NSOF wind radii""",
'NVG2':"""NAVGEM tc vortex tracker (NHC interpolator)(2nd interpolation)-added 12Dec12""",
'NVGI':"""NAVGEM tc vortex tracker (NHC interpolator)-added 12Dec12""",
'NVGM':"""NAVGEM tc vortex tracker - added 12Dec12""",
'NVS5':"""NAVGEM STIPS intensity output (with OHC)""",
'NWBB':"""METEO France New Caledonia""",
'NWOC':"""JTWC EASTPAC official DoD forecast""",
'NZKL':"""NZ Met Wellington""",
'OFCI':"""NHC/CPHC interpolated official""",
'OFCL':"""NHC/CPHC official""",
'OTCM':"""One-way tropical cyclone model""",
'NTCM':"""Nested Tropical Cyclone Model (two-way interactive)""",
'OTCR':"""One-way tropical cyclone model (ATCF)""",
'P91E':"""UKMET regional""",
'P9UK':"""UKMO""",
'PEST':"""Deterministic forecast from PEST (Weber, ONR)""",
'PTRI':"""La Reunion NWP model (interpolated)""",
'PTRO':"""La Reunion NWP model""",
'R120':"""120 hr JTWC+CLIP blend""",
'RCTP':"""CWB Taiwan""",
'RECR':"""TYAN78, recurver data set""",
'RGAV':"""Average of GFDN,JTYM""",
'RI30':"""SHIPS-RI forecast for 30 kt intensity change in 24 hours - produced when SHIPS-RI probability >= 30%""",
'RJTD':"""JMA Tokyo""",
'RJTZ':"""Japanese Self-Defense Forces (JASDF)""",
'RKSL':"""KMA Forecast""",
'RKTM':"""Korean Model""",
'RPMM':"""PAGASA""",
'RVCN':"""Wind radii model Consensus of GFTI, AHNI, HHFI, EMXI""",
'RYOC':"""Forecaster Created Consensus Guidance (any model combination)""",
'S411':"""STIPS Consensus w/AOML OHC Input (All 10 CONW members + GFNI) (NRL)""",
'S511':"""STIPS Consensus w/NCODA OHC Input (All 10 CONW members + GFNI) (NRL)""",
'S5XX':"""2011 Updated STIPS Consensus=S511 + COTI + CHII (NRL) """,
'S5YY':"""Intensity Consensus - DSHA+DSHN+CTCI+HWFI+GHMI+CHII""",
'SBAF':"""Beta and Advection model, shallow, FNMOC run""",
'SBAM':"""Beta and Advection model, shallow""",
'SCON':"""elective Consensus (SAFA)""",
'SHIP':"""SHIPS""",
'ST10':"""STIPS Consensus (All 10 CONW members) (NRL)""",
'ST11':"""STIPS Consensus (All 10 CONW members + GFNI) (NRL)""",
'ST5D':"""5 Day STIFOR CIRA""",
'ST85':"""STIPS Microwave Enhanced 85 GHz (Univ of AL)""",
'STIC':"""STIPS consensus (STIP,STID,STWP,STWD)""",
'STID':"""STIPS - decay version (CIRA/NOAA/NRL)""",
'STIM':"""STIPS Microwave Enhanced 19/85 GHz(Univ of AL)""",
'STIP':"""STIPS (CIRA/NOAA)""",
'STRT':"""TYAN92, straight mover data set""",
'STWD':"""STIPS - decay version (CIRA/NOAA/NRL) run on CONW""",
'STWP':"""STIPS (CIRA/NOAA/NRL) run on CONW""",
'TAPT':"""JTWC TAPT model (typhoon accel)""",
'TCL2':"""TC LAPS (NHC Interpolator)(2nd interpolation)""",
'TCLI':"""TC LAPS (NHC Interpolator)""",
'TCLP':"""TC LAPS (BOM regional model)""",
'TCON':"""NHC Consensus Track Guidance  (AVNI/2+EGRI/2+NGPI/2+GHMI/2+HWRI/2)""",
'TCS5':"""TC LAPS STIPS intensity output (with OHC)""",
'TLAI':"""BOM Global (NHC Interpolator)""",
'TLAP':"""BOM Global""",
'TM01':"""MEPS 20 km Ensemble Member 1""",
'TM02':"""MEPS 20 km Ensemble Member 2""",
'TM03':"""MEPS 20 km Ensemble Member 3""",
'TM04':"""MEPS 20 km Ensemble Member 4""",
'TM05':"""MEPS 20 km Ensemble Member 5""",
'TM06':"""MEPS 20 km Ensemble Member 6""",
'TM07':"""MEPS 20 km Ensemble Member 7""",
'TM08':"""MEPS 20 km Ensemble Member 8""",
'TM09':"""MEPS 20 km Ensemble Member 9""",
'TM10':"""MEPS 20 km Ensemble Member 10""",
'TMM2':"""MEPS 20 km Ensemble Mean (2nd Interpolation)""",
'TMMI':"""MEPS 20 km Ensemble Mean (Interpolated)""",
'TMMN':"""MEPS 20 km Ensemble Mean (Uninterpolated Members)""",
'TVCN':"""NHC Variable Track Guidance (AVNI/2+EGRI/2+NGPI/2+GHMI/2+HRWRI/2+EMXI/2)""",
'TWRF':""" Taiwan (CWB) WRF, implemented Jun 2012""",
'TWRI':"""Taiwan WRF (Interpoloated 06 hours)""",
'TXLI':"""TX LAPS (NHC Interpolator)""",
'TXLP':"""TX LAPS (BOM TC vort tracker started 1 Dec 04)""",
'UKM':"""UKMET Global Vortex Tracker""",
'UKM2':"""UKMET model (Interpolated 12 hours)""",
'UKMI':"""UKMO""",
'UKX':"""UKMET Model using AVN vortex tracker algorithm""",
'UKXI':"""UKMET AVN tracker interpolated""",
'VHHH':"""Hong Kong Observatory""",
'VTBB':"""Thailand Official Forecast""",
'WANI':"""NPS Experimental Weighted Analog Intensity Forecast """,
'WBA2':"""Harry Weber model interpolated (2nd interpolation)""",
'WBAF':"""Harry Weber model FNMOC Run""",
'WBAI':"""Harry Weber model interpolated""",
'WBAR':"""Harry Weber model""",
'WBS5':"""WBAR STIPS intensity output (with OHC)""",
'WGTD':"""Weighted average of several aids""",
'WRF0':"""AFWA WRF 45 km resolution unbogussed""",
'WRF2':"""AFWA WRF 45 km resolution unbogussed (second interpolation)""",
'WRFI':"""AFWA WRF 45 km resolution unbogussed (first interpolation)""",
'WRNG':"""Warning""",
'XTRP':"""Extrapolation from past 12 hour motion""",
    }

    aidDescNhc={
'A4P2':"""PSU ARW w/Doppler 2011 version (Interpolated 12 hours)""",
'A4PI':"""PSU ARW w/Doppler 2011 version (Interpolated 06 hours)""",
'A4PS':"""PSU ARW w/Doppler 2011 version""",
'AC00':"""GFS Ensemble control member""",
'AEM2':"""GFS Ensemble Mean (Interpolated 12 hours)""",
'AEMI':"""GFS Ensemble Mean (Interpolated 06 hours)""",
'AEMN':"""GFS Ensemble Mean""",
'AHW2':"""SUNY Advanced Hurricane WRF (Interpolated 12 hours)""",
'AHW4':"""SUNY Advanced Hurricane WRF""",
'AHWI':"""SUNY Advanced Hurricane WRF (Interpolated 06 hours)""",
'AMMN':"""GFS New Ensemble Mean""",
'AP01':"""GFS Ensemble +01 member""",
'AP02':"""GFS Ensemble +02 member""",
'AP03':"""GFS Ensemble +03 member""",
'AP04':"""GFS Ensemble +04 member""",
'AP05':"""GFS Ensemble +05 member""",
'AP06':"""GFS Ensemble +06 member""",
'AP07':"""GFS Ensemble +07 member""",
'AP08':"""GFS Ensemble +08 member""",
'AP09':"""GFS Ensemble +09 member""",
'AP10':"""GFS Ensemble +10 member""",
'AP11':"""GFS Ensemble +11 member""",
'AP12':"""GFS Ensemble +12 member""",
'AP13':"""GFS Ensemble +13 member""",
'AP14':"""GFS Ensemble +14 member""",
'AP15':"""GFS Ensemble +15 member""",
'AP16':"""GFS Ensemble +16 member""",
'AP17':"""GFS Ensemble +17 member""",
'AP18':"""GFS Ensemble +18 member""",
'AP19':"""GFS Ensemble +19 member""",
'AP20':"""GFS Ensemble +20 member""",
'AP21':"""GFS Ensemble +21 member""",
'AP22':"""GFS Ensemble +22 member""",
'AP23':"""GFS Ensemble +23 member""",
'AP24':"""GFS Ensemble +24 member""",
'AP25':"""GFS Ensemble +25 member""",
'AP26':"""GFS Ensemble +26 member""",
'AP27':"""GFS Ensemble +27 member""",
'AP28':"""GFS Ensemble +28 member""",
'AP29':"""GFS Ensemble +29 member""",
'AP30':"""GFS Ensemble +30 member""",

'APS2':"""PSU ARW (Interpolated 12 hours)""",
'APSI':"""PSU ARW (Interpolated 06 hours)""",
'APSU':"""PSU ARW""",
'AVN2':"""GFS Model (Interpolated 12 hours)""",
'AVNI':"""GFS Model (Interpolated 06 hours)""",
'AVNO':"""GFS Model""",
'AVX2':"""GFS Model 10-day tracker (Interpolated 12 hours)""",
'AVXI':"""GFS Model 10-day tracker (Interpolated 06 hours)""",
'AVXO':"""GFS Model 10-day tracker""",
'BAMD':"""Beta and Advection model, deep (NHC)""",
'BAMM':"""Beta and Advection model, medium (NHC)""",
'BAMS':"""Beta and Advection model, shallow (NHC)""",
'BCD5':"""Combination of CLP5 and Decay-SHIFOR run on operational inputs""",
'CARQ':"""Combined ARQ Position""",
'CC00':"""Canadian model Ensemble control""",
'CEM2':"""Canadian model Ensemble Mean (Interpolated 12 hours)""",
'CEMI':"""Canadian model Ensemble Mean (Interpolated 06 hours)""",
'CEMN':"""Canadian model Ensemble Mean""",
'CGUN':"""Corrected version of GUNA""",
'CLIP':"""CLImatology-PERsistence model 3-day""",
'CLP3':"""3-day CLImatology-PERsistence model""",
'CLP5':"""CLImatology-PERsistence model 5-day""",
'CMC':"""Canadian model""",
'CMC2':"""Canadian Model (Interpolated 12 hours)""",
'CMCI':"""Canadian model (Interpolated 06 hours)""",
'COA2':"""COAMPS Atlantic grid (Interpolated 12 hours)""",
'COAI':"""COAMPS Atlantic grid (Interpolated 06 hours)""",
'COAL':"""COAMPS Atlantic grid""",
'COCE':"""COAMPS Carib/E Pacific grid""",
'COE2':"""COAMPS Carib/E Pacific grid (Interpolated 12 hours)""",
'COEI':"""COAMPS Carib/E Pacific grid (Interpolated 06 hours)""",
'CONU':"""NHC Multi-Model Consensus (Retired)""",
'COT2':"""NRL COAMPS-TC model (Interpolated 12 hours)""",
'COTC':"""NRL COAMPS-TC model""",
'COTI':"""NRL COAMPS-TC model (Interpolated 06 hours)""",
'CP01':"""Canadian model Ensemble +01 member""",
'CP02':"""Canadian model Ensemble +02 member""",
'CP03':"""Canadian model Ensemble +03 member""",
'CP04':"""Canadian model Ensemble +04 member""",
'CP05':"""Canadian model Ensemble +05 member""",
'CP06':"""Canadian model Ensemble +06 member""",
'CP07':"""Canadian model Ensemble +07 member""",
'CP08':"""Canadian model Ensemble +08 member""",
'CP09':"""Canadian model Ensemble +09 member""",
'CP10':"""Canadian model Ensemble +10 member""",
'CP11':"""Canadian model Ensemble +11 member""",
'CP12':"""Canadian model Ensemble +12 member""",
'CP13':"""Canadian model Ensemble +13 member""",
'CP14':"""Canadian model Ensemble +14 member""",
'CP15':"""Canadian model Ensemble +15 member""",
'CP16':"""Canadian model Ensemble +16 member""",
'CP17':"""Canadian model Ensemble +17 member""",
'CP18':"""Canadian model Ensemble +18 member""",
'CP19':"""Canadian model Ensemble +19 member""",
'CP20':"""Canadian model Ensemble +20 member""",
'CTC2':"""NRL COAMPS-TC expt (Interpolated 12 hours)""",
'CTCI':"""NRL COAMPS-TC expt (Interpolated 06 hours)""",
'CTCX':"""NRL COAMPS-TC model experimental version""",
'DRCI':"""DeMaria Radii CLIPER model (Interpolated)""",
'DRCL':"""DeMaria Radii CLIPER model""",
'DSHP':"""Decay SHIPS model""",
'DSPP':"""Decay SHIPS model parallel (experimental - do not use)""",
'EC00':"""ECMWF model Ensemble control member [NCEP tracker]""",
'ECM':"""ECMWF model""",
'ECM2':"""ECMWF model (Interpolated 12 hours)""",
'ECME':"""ECMWF model Ensemble Control Member [GTS tracker]""",
'ECMI':"""ECMWF model (Interpolated 06 hours)""",
'ECMO':"""ECMWF model [GTS tracker]""",
'ECO2':"""ECMWF model [GTS tracker] (Interpolated 12 hours)""",
'ECOI':"""ECMWF model [GTS tracker] (Interpolated 06 hours)""",
'EE00':"""ECMWF model Ensemble Control Member [GTS tracker]""",
'EE01':"""ECMWF model Ensemble +01 member [GTS tracker]""",
'EE02':"""ECMWF model Ensemble +02 member [GTS tracker]""",
'EE03':"""ECMWF model Ensemble +03 member [GTS tracker]""",
'EE04':"""ECMWF model Ensemble +04 member [GTS tracker]""",
'EE05':"""ECMWF model Ensemble +05 member [GTS tracker]""",
'EE06':"""ECMWF model Ensemble +06 member [GTS tracker]""",
'EE07':"""ECMWF model Ensemble +07 member [GTS tracker]""",
'EE08':"""ECMWF model Ensemble +08 member [GTS tracker]""",
'EE09':"""ECMWF model Ensemble +09 member [GTS tracker]""",
'EE10':"""ECMWF model Ensemble +10 member [GTS tracker]""",
'EE11':"""ECMWF model Ensemble +11 member [GTS tracker]""",
'EE12':"""ECMWF model Ensemble +12 member [GTS tracker]""",
'EE13':"""ECMWF model Ensemble +13 member [GTS tracker]""",
'EE14':"""ECMWF model Ensemble +14 member [GTS tracker]""",
'EE15':"""ECMWF model Ensemble +15 member [GTS tracker]""",
'EE16':"""ECMWF model Ensemble +16 member [GTS tracker]""",
'EE17':"""ECMWF model Ensemble +17 member [GTS tracker]""",
'EE18':"""ECMWF model Ensemble +18 member [GTS tracker]""",
'EE19':"""ECMWF model Ensemble +19 member [GTS tracker]""",
'EE20':"""ECMWF model Ensemble +20 member [GTS tracker]""",
'EE21':"""ECMWF model Ensemble +21 member [GTS tracker]""",
'EE22':"""ECMWF model Ensemble +22 member [GTS tracker]""",
'EE23':"""ECMWF model Ensemble +23 member [GTS tracker]""",
'EE24':"""ECMWF model Ensemble +24 member [GTS tracker]""",
'EE25':"""ECMWF model Ensemble +25 member [GTS tracker]""",
'EE26':"""ECMWF model Ensemble +26 member [GTS tracker]""",
'EE27':"""ECMWF model Ensemble +27 member [GTS tracker]""",
'EE28':"""ECMWF model Ensemble +28 member [GTS tracker]""",
'EE29':"""ECMWF model Ensemble +29 member [GTS tracker]""",
'EE30':"""ECMWF model Ensemble +30 member [GTS tracker]""",
'EE31':"""ECMWF model Ensemble +31 member [GTS tracker]""",
'EE32':"""ECMWF model Ensemble +32 member [GTS tracker]""",
'EE33':"""ECMWF model Ensemble +33 member [GTS tracker]""",
'EE34':"""ECMWF model Ensemble +34 member [GTS tracker]""",
'EE35':"""ECMWF model Ensemble +35 member [GTS tracker]""",
'EE36':"""ECMWF model Ensemble +36 member [GTS tracker]""",
'EE37':"""ECMWF model Ensemble +37 member [GTS tracker]""",
'EE38':"""ECMWF model Ensemble +38 member [GTS tracker]""",
'EE39':"""ECMWF model Ensemble +39 member [GTS tracker]""",
'EE40':"""ECMWF model Ensemble +40 member [GTS tracker]""",
'EE41':"""ECMWF model Ensemble +41 member [GTS tracker]""",
'EE42':"""ECMWF model Ensemble +42 member [GTS tracker]""",
'EE43':"""ECMWF model Ensemble +43 member [GTS tracker]""",
'EE44':"""ECMWF model Ensemble +44 member [GTS tracker]""",
'EE45':"""ECMWF model Ensemble +45 member [GTS tracker]""",
'EE46':"""ECMWF model Ensemble +46 member [GTS tracker]""",
'EE47':"""ECMWF model Ensemble +47 member [GTS tracker]""",
'EE48':"""ECMWF model Ensemble +48 member [GTS tracker]""",
'EE49':"""ECMWF model Ensemble +49 member [GTS tracker]""",
'EE50':"""ECMWF model Ensemble +50 member [GTS tracker]""",
'EEMN':"""ECMWF model Ensemble Mean [NCEP tracker]""",
'EGR2':"""UKMET model GTS (Official - Interpolated 12 hours)""",
'EGRI':"""UKMET model GTS (Official - Interpolated 06 hours)""",
'EGRR':"""UKMET model GTS (Official)""",
'EMN2':"""ECMWF model Ensemble Mean [NCEP tracker] (Interpolated 12 hours)""",
'EMN3':"""ECMWF model Ensemble Mean [NCEP tracker] (Interpolated 18 hours)""",
'EMN4':"""ECMWF model Ensemble Mean [NCEP tracker] (Interpolated 24 hours)""",
'EMNI':"""ECMWF model Ensemble Mean [NCEP tracker] (Interpolated 06 hours)""",
'EMX':"""ECMWF model [NCEP tracker]""",
'EMX2':"""ECMWF model [NCEP tracker] (Interpolated 12 hours)""",
'EMXI':"""ECMWF model [NCEP tracker] (Interpolated 06 hours)""",
'EN01':"""ECMWF model Ensemble +01 member [NCEP tracker]""",
'EN02':"""ECMWF model Ensemble +02 member [NCEP tracker]""",
'EN03':"""ECMWF model Ensemble +03 member [NCEP tracker]""",
'EN04':"""ECMWF model Ensemble +04 member [NCEP tracker]""",
'EN05':"""ECMWF model Ensemble +05 member [NCEP tracker]""",
'EN06':"""ECMWF model Ensemble +06 member [NCEP tracker]""",
'EN07':"""ECMWF model Ensemble +07 member [NCEP tracker]""",
'EN08':"""ECMWF model Ensemble +08 member [NCEP tracker]""",
'EN09':"""ECMWF model Ensemble +09 member [NCEP tracker]""",
'EN10':"""ECMWF model Ensemble +10 member [NCEP tracker]""",
'EN11':"""ECMWF model Ensemble +11 member [NCEP tracker]""",
'EN12':"""ECMWF model Ensemble +12 member [NCEP tracker]""",
'EN13':"""ECMWF model Ensemble +13 member [NCEP tracker]""",
'EN14':"""ECMWF model Ensemble +14 member [NCEP tracker]""",
'EN15':"""ECMWF model Ensemble +15 member [NCEP tracker]""",
'EN16':"""ECMWF model Ensemble +16 member [NCEP tracker]""",
'EN17':"""ECMWF model Ensemble +17 member [NCEP tracker]""",
'EN18':"""ECMWF model Ensemble +18 member [NCEP tracker]""",
'EN19':"""ECMWF model Ensemble +19 member [NCEP tracker]""",
'EN20':"""ECMWF model Ensemble +20 member [NCEP tracker]""",
'EN21':"""ECMWF model Ensemble +21 member [NCEP tracker]""",
'EN22':"""ECMWF model Ensemble +22 member [NCEP tracker]""",
'EN23':"""ECMWF model Ensemble +23 member [NCEP tracker]""",
'EN24':"""ECMWF model Ensemble +24 member [NCEP tracker]""",
'EN25':"""ECMWF model Ensemble +25 member [NCEP tracker]""",
'EP01':"""ECMWF model Ensemble +26 member [NCEP tracker]""",
'EP02':"""ECMWF model Ensemble +27 member [NCEP tracker]""",
'EP03':"""ECMWF model Ensemble +28 member [NCEP tracker]""",
'EP04':"""ECMWF model Ensemble +29 member [NCEP tracker]""",
'EP05':"""ECMWF model Ensemble +30 member [NCEP tracker]""",
'EP06':"""ECMWF model Ensemble +31 member [NCEP tracker]""",
'EP07':"""ECMWF model Ensemble +32 member [NCEP tracker]""",
'EP08':"""ECMWF model Ensemble +33 member [NCEP tracker]""",
'EP09':"""ECMWF model Ensemble +34 member [NCEP tracker]""",
'EP10':"""ECMWF model Ensemble +35 member [NCEP tracker]""",
'EP11':"""ECMWF model Ensemble +36 member [NCEP tracker]""",
'EP12':"""ECMWF model Ensemble +37 member [NCEP tracker]""",
'EP13':"""ECMWF model Ensemble +38 member [NCEP tracker]""",
'EP14':"""ECMWF model Ensemble +39 member [NCEP tracker]""",
'EP15':"""ECMWF model Ensemble +40 member [NCEP tracker]""",
'EP16':"""ECMWF model Ensemble +41 member [NCEP tracker]""",
'EP17':"""ECMWF model Ensemble +42 member [NCEP tracker]""",
'EP18':"""ECMWF model Ensemble +43 member [NCEP tracker]""",
'EP19':"""ECMWF model Ensemble +44 member [NCEP tracker]""",
'EP20':"""ECMWF model Ensemble +45 member [NCEP tracker]""",
'EP21':"""ECMWF model Ensemble +46 member [NCEP tracker]""",
'EP22':"""ECMWF model Ensemble +47 member [NCEP tracker]""",
'EP23':"""ECMWF model Ensemble +48 member [NCEP tracker]""",
'EP24':"""ECMWF model Ensemble +49 member [NCEP tracker]""",
'EP25':"""ECMWF model Ensemble +50 member [NCEP tracker]""",
'FIM2':"""ESRL FIM 2011 version (Interpolated 12 hours)""",
'FIM9':"""ESRL FIM""",
'FIMI':"""ESRL FIM 2011 version (Interpolated 06 hours)""",
'FIMY':"""ESRL FIM 2011 version""",
'FM92':"""ESRL FIM (Interpolated 12 hours)""",
'FM9I':"""ESRL FIM (Interpolated 06 hours)""",
'FSSE':"""FSU Superensemble""",
'G002':"""GFDL Ensemble +00 Control (Interpolated 12 hours)""",
'G00I':"""GFDL Ensemble +00 Control (Interpolated 06 hours)""",
'G012':"""GFDL Ensemble +01 member (unbogussed) (Interpolated 12 hours)""",
'G01I':"""GFDL Ensemble +01 member (unbogussed) (Interpolated 06 hours)""",
'G022':"""GFDL Ensemble +02 member (Interpolated 12 hours)""",
'G02I':"""GFDL Ensemble +02 member (Interpolated 06 hours)""",
'G032':"""GFDL Ensemble +03 member (Interpolated 12 hours)""",
'G03I':"""GFDL Ensemble +03 member (Interpolated 06 hours)""",
'G042':"""GFDL Ensemble +04 member (Interpolated 12 hours)""",
'G04I':"""GFDL Ensemble +04 member (Interpolated 06 hours)""",
'G052':"""GFDL Ensemble +05 member (Interpolated 12 hours)""",
'G05I':"""GFDL Ensemble +05 member (Interpolated 06 hours)""",
'G062':"""GFDL Ensemble +06 member (Interpolated 12 hours)""",
'G06I':"""GFDL Ensemble +06 member (Interpolated 06 hours)""",
'G072':"""GFDL Ensemble +07 member (Interpolated 12 hours)""",
'G07I':"""GFDL Ensemble +07 member (Interpolated 06 hours)""",
'G082':"""GFDL Ensemble +08 member (Interpolated 12 hours)""",
'G08I':"""GFDL Ensemble +08 member (Interpolated 06 hours)""",
'G092':"""GFDL Ensemble +09 member (Interpolated 12 hours)""",
'G09I':"""GFDL Ensemble +09 member (Interpolated 06 hours)""",
'G102':"""GFDL Ensemble +10 member (Interpolated 12 hours)""",
'G10I':"""GFDL Ensemble +10 member (Interpolated 06 hours)""",
'G112':"""GFDL Ensemble +11 member (Interpolated 12 hours)""",
'G11I':"""GFDL Ensemble +11 member (Interpolated 06 hours)""",
'G122':"""GFDL Ensemble +12 member (Interpolated 12 hours)""",
'G12I':"""GFDL Ensemble +12 member (Interpolated 06 hours)""",
'G132':"""GFDL Ensemble +13 member (Interpolated 12 hours)""",
'G13I':"""GFDL Ensemble +13 member (Interpolated 06 hours)""",
'G142':"""GFDL Ensemble +14 member (Interpolated 12 hours)""",
'G14I':"""GFDL Ensemble +14 member (Interpolated 06 hours)""",
'G152':"""GFDL Ensemble +15 member (Interpolated 12 hours)""",
'G15I':"""GFDL Ensemble +15 member (Interpolated 06 hours)""",
'G162':"""GFDL Ensemble +16 member (Interpolated 12 hours)""",
'G16I':"""GFDL Ensemble +16 member (Interpolated 06 hours)""",
'G172':"""GFDL Ensemble +17 member (Interpolated 12 hours)""",
'G17I':"""GFDL Ensemble +17 member (Interpolated 06 hours)""",
'GF52':"""Parallel version of GFDL (Interpolated 12 hours)""",
'GF5I':"""Parallel version of GFDL (Interpolated 06 hours)""",
'GFD2':"""GFDL model (Interpolated 12 hours)""",
'GFD5':"""Parallel version of GFDL""",
'GFDE':"""GFDL w/ ECMWF fields model""",
'GFDI':"""GFDL model (Interpolated 06 hours)""",
'GFDL':"""GFDL model""",
'GFDN':"""Navy GFDL model""",
'GFDT':"""GFDL using [NCEP tracker]""",
'GFE2':"""GFDL w/ ECMWF fields model (Interpolated 12 hours)""",
'GFEI':"""GFDL w/ ECMWF fields model (Interpolated 06 hours)""",
'GFEX':"""Consensus of AVNI and EMXI""",
'GFN2':"""Navy GFDL model (Interpolated 12 hours)""",
'GFNI':"""Navy GFDL model (Interpolated 06 hours)""",
'GFT2':"""GFDL using [NCEP tracker] (Interpolated 12 hours)""",
'GFTI':"""GFDL using [NCEP tracker] (Interpolated 06 hours)""",
'GHM2':"""GFDL 12-h interpolated model using variable intensity offset""",
'GHMI':"""GFDL 06-h interpolated model using variable intensity offset""",
'GP00':"""GFDL Ensemble +00 Control""",
'GP01':"""GFDL Ensemble +01 member (unbogussed)""",
'GP02':"""GFDL Ensemble +02 member""",
'GP03':"""GFDL Ensemble +03 member""",
'GP04':"""GFDL Ensemble +04 member""",
'GP05':"""GFDL Ensemble +05 member""",
'GP06':"""GFDL Ensemble +06 member""",
'GP07':"""GFDL Ensemble +07 member""",
'GP08':"""GFDL Ensemble +08 member""",
'GP09':"""GFDL Ensemble +09 member""",
'GP10':"""GFDL Ensemble +10 member""",
'GP11':"""GFDL Ensemble +11 member""",
'GP12':"""GFDL Ensemble +12 member""",
'GP13':"""GFDL Ensemble +13 member""",
'GP14':"""GFDL Ensemble +14 member""",
'GP15':"""GFDL Ensemble +15 member""",
'GP16':"""GFDL Ensemble +16 member""",
'GP17':"""GFDL Ensemble +17 member""",
'GPM2':"""GFDL Ensemble Mean (Interpolated 12 hours)""",
'GPMI':"""GFDL Ensemble Mean (Interpolated 06 hours)""",
'GPMN':"""GFDL Ensemble Mean""",
'GUNA':"""Consensus of all: AVNI/GHMI/EGRI/NGPI""",
'H3G2':"""NCEP/AOML HWRF 3km (Interpolated 12 hours)""",
'H3GI':"""NCEP/AOML HWRF 3km (Interpolated 06 hours)""",
'H3GP':"""NCEP/AOML HWRF 3km model""",
'HW32':"""HWRF model [2013 version] (Interpolated 12 hours)""",
'HW3F':"""HWRF model [2013 version]""",
'HW3I':"""HWRF model [2013 version] (Interpolated 06 hours)""",
'HWE2':"""HWRF w/ ECMWF fields model (Interpolated 12 hours)""",
'HWEI':"""HWRF w/ ECMWF fields model (Interpolated 06 hours)""",
'HWF2':"""HWRF model (Interpolated 12 hours)""",
'HWFE':"""HWRF w/ ECMWF fields model""",
'HWFI':"""HWRF model (Interpolated 06 hours)""",
'HWM2':"""HWRF Ensemble Mean (Interpolated 12 hours)""",
'HWMI':"""HWRF Ensemble Mean (Interpolated 06 hours)""",
'HWMN':"""HWRF Ensemble Mean""",
'HWRF':"""HWRF model""",
'HMON':"""HMON model""",
'ICON':"""Consensus of all: DSHP/LGEM/GHMI/HWFI (2016 version)""",
'IV15':"""HFIP intensity consensus of >=2: DSHP/LGEM/HWFI/GPMI/CXTI/UW4I (2014 version)""",
'IVCN':"""Consensus of >=2: DSHP/LGEM/GHMI/HWFI/CTCI (2016 version)""",
'IVCR':"""Consensus of >=2: DSHP/LGEM/GHMI/HWFI/RI??+CTCI""",
'IVRI':"""Consensus of 5: DHSP/LGEM/GHMI/HWFI/CTCI+RI40 or RI35 or RI30 or RI25""",
'JGS2':"""Japanese Global Spectral Model (Interpolated 12 hours)""",
'JGSI':"""Japanese Global Spectral Model (Interpolated 06 hours)""",
'JGSM':"""Japanese Global Spectral Model""",
'JTWC':"""JTWC official forecast""",
'JTWI':"""JTWC official forecast (Interpolated 06 hours)""",
'KBMD':"""Beta and Advection model, deep (NHC-NCO PARA)""",
'KBMM':"""Beta and Advection model, medium (NHC-NCO PARA)""",
'KBMS':"""Beta and Advection model, shallow (NHC-NCO PARA)""",
'KCL5':"""CLImatology-PERsistence model 5-day (NHC-NCO PARA)""",
'KCLP':"""CLImatology-PERsistence model 3-day (NHC-NCO PARA)""",
'KDSP':"""Decay SHIPS model (NHC-NCO PARA)""",
'KEG2':"""UKMET model GTS (2014 test - Interpolated 12 hours)""",
'KEGI':"""UKMET model GTS (2014 test - Interpolated 06 hours)""",
'KEGR':"""UKMET model GTS (2014 test)""",
'KLBR':"""LBAR (NHC-NCO PARA)""",
'KLGM':"""SHIPS Logistic Growth Equation (LGE) forecast model (NHC-NCO PARA)""",
'KOCD':"""Combination of CLP5 and Decay-SHIFOR run on operational inputs (NHC-NCO PARA)""",
'KSF5':"""SHIFOR intensity model 5-day (NHC-NCO PARA)""",
'KSFR':"""SHIFOR intensity model 3-day (NHC-NCO PARA)""",
'KSHP':"""SHIPS model (NHC-NCO PARA)""",
'KXTR':"""Extrapolation using past 12-hr motion (NHC-NCO PARA)""",
'LBAR':"""LBAR""",
'LGEM':"""SHIPS Logistic Growth Equation (LGE) forecast model""",
'MRCI':"""McAdie Radii CLIPER model (Interpolated)""",
'MRCL':"""McAdie Radii CLIPER model""",
'MYOC':"""Forecaster Created Consensus Guidance (any model combination)""",
'NAM':"""NAM model""",
'NAM2':"""NAM model (Interpolated 12 hours)""",
'NAMI':"""NAM model (Interpolated 06 hours)""",
'NGP2':"""NOGAPS model (Interpolated 12 hours)""",
'NGPI':"""NOGAPS model (Interpolated 06 hours)""",
'NGPS':"""NOGAPS model""",
'NGX':"""NAVGEM/NOGAPS [GFS tracker]""",
'NGX2':"""NAVGEM/NOGAPS [GFS tracker] (Interpolated 12 hours)""",
'NGXI':"""NAVGEM/NOGAPS [GFS tracker] (Interpolated 06 hours)""",
'NVG2':"""NAVGEM model (Interpolated 12 hours)""",
'NVGI':"""NAVGEM model (Interpolated 06 hours)""",
'NVGM':"""NAVGEM model""",
'OCD5':"""Combination of CLP5 and Decay-SHIFOR run on operational inputs""",
'OFC2':"""NHC official forecast (Interpolated 12 hours)""",
'OFCI':"""NHC official forecast (Interpolated 06 hours)""",
'OFCL':"""NHC official forecast""",
'OFCP':"""NHC provisional forecast""",
'OFP2':"""NHC provisional forecast (Interpolated 12 hours)""",
'OFPI':"""NHC provisional forecast (Interpolated 06 hours)""",
'OHPC':"""WPC official forecast""",
'OOPC':"""OPC official forecast""",
'RI25':"""Rapid Intensity Aid 25kts (24 hr RI Prob)""",
'RI30':"""Rapid Intensity Aid 30kts (24 hr RI Prob)""",
'RI35':"""Rapid Intensity Aid 35kts (24 hr RI Prob)""",
'RI40':"""Rapid Intensity Aid 40kts (24 hr RI Prob)""",
'RYOC':"""Forecaster Created Consensus Guidance (any model combination)""",
'SHF5':"""SHIFOR intensity model 5-day""",
'SHFR':"""SHIFOR intensity model 3-day""",
'SHIP':"""SHIPS model""",
'SHPP':"""SHIPS model parallel (experimental - do not use)""",
'SPC3':"""CSU-CIRA SPICE statistical intensity consensus""",
'TABD':"""Trajectory and Beta Model, deep (NHC)""",
'TABM':"""Trajectory and Beta Model, medium (NHC)""",
'TABS':"""Trajectory and Beta Model, shallow (NHC)""",
'TCCN':"""Corrected version of TCON""",
'TCLP':"""Trajectory CLIPER model 7-day""",
'TCOA':"""Consensus of all: AVNI/EGRI/GHMI/HWFI (2016 version)""",
'TCOE':"""Consensus of all: AVNI/EGRI/GHMI/HWFI (2016 version)""",
'TCON':"""Consensus of all: AVNI/EGRI/GHMI/HWFI (2016 version)""",
'TV15':"""HFIP track consensus of >=2: AVNI/EGRI/HWFI/EMXI/GPMI (2014 version)""",
'TVCA':"""Consensus of >=2: AVNI/EGRI/GHMI/HWFI/EMXI/CTCI (2016 version)""",
'TVCC':"""Corrected version of TVCN""",
'TVCE':"""Consensus of >=2: AVNI/EGRI/GHMI/HWFI/EMXI/CTCI (2016 version)""",
'TVCN':"""Consensus of >=2: AVNI/EGRI/GHMI/HWFI/EMXI/CTCI (2016 version)""",
'TVCX':"""Consensus of >=2: AVNI/EGRI/GHMI/HWFI/EMXIx2/CTCI (2016 version)""",
'TVCY':"""Consensus of >=2: AVNIx2/EGRI/GHMI/HWFI/EMXIx2/CTCI (2016 version)""",
'UE00':"""UKMET MOGREPS-G Ensemble Control Member""",
'UE01':"""UKMET MOGREPS-G Ensemble +01 member""",
'UE02':"""UKMET MOGREPS-G Ensemble +02 member""",
'UE03':"""UKMET MOGREPS-G Ensemble +03 member""",
'UE04':"""UKMET MOGREPS-G Ensemble +04 member""",
'UE05':"""UKMET MOGREPS-G Ensemble +05 member""",
'UE06':"""UKMET MOGREPS-G Ensemble +06 member""",
'UE07':"""UKMET MOGREPS-G Ensemble +07 member""",
'UE08':"""UKMET MOGREPS-G Ensemble +08 member""",
'UE09':"""UKMET MOGREPS-G Ensemble +09 member""",
'UE10':"""UKMET MOGREPS-G Ensemble +10 member""",
'UE11':"""UKMET MOGREPS-G Ensemble +11 member""",
'UE12':"""UKMET MOGREPS-G Ensemble +12 member""",
'UE13':"""UKMET MOGREPS-G Ensemble +13 member""",
'UE14':"""UKMET MOGREPS-G Ensemble +14 member""",
'UE15':"""UKMET MOGREPS-G Ensemble +15 member""",
'UE16':"""UKMET MOGREPS-G Ensemble +16 member""",
'UE17':"""UKMET MOGREPS-G Ensemble +17 member""",
'UE18':"""UKMET MOGREPS-G Ensemble +18 member""",
'UE19':"""UKMET MOGREPS-G Ensemble +19 member""",
'UE20':"""UKMET MOGREPS-G Ensemble +20 member""",
'UE21':"""UKMET MOGREPS-G Ensemble +21 member""",
'UE22':"""UKMET MOGREPS-G Ensemble +22 member""",
'UE23':"""UKMET MOGREPS-G Ensemble +23 member""",
'UE24':"""UKMET MOGREPS-G Ensemble +24 member""",
'UE25':"""UKMET MOGREPS-G Ensemble +25 member""",
'UE26':"""UKMET MOGREPS-G Ensemble +26 member""",
'UE27':"""UKMET MOGREPS-G Ensemble +27 member""",
'UE28':"""UKMET MOGREPS-G Ensemble +28 member""",
'UE29':"""UKMET MOGREPS-G Ensemble +29 member""",
'UE30':"""UKMET MOGREPS-G Ensemble +30 member""",
'UE31':"""UKMET MOGREPS-G Ensemble +31 member""",
'UE32':"""UKMET MOGREPS-G Ensemble +32 member""",
'UE33':"""UKMET MOGREPS-G Ensemble +33 member""",
'UE34':"""UKMET MOGREPS-G Ensemble +34 member""",
'UE35':"""UKMET MOGREPS-G Ensemble +35 member""",
'UE36':"""UKMET MOGREPS-G Ensemble Previous Control member????""",
'UEM2':"""UKMET MOGREPS-G Ensemble Mean (Interpolated 12 hours)""",
'UEMI':"""UKMET MOGREPS-G Ensemble Mean (Interpolated 06 hours)""",
'UEMN':"""UKMET MOGREPS-G Ensemble Mean""",
'UKM':"""UKMET model (Developmental)""",
'UKM2':"""UKMET model (Interpolated 12 hours)""",
'UKMI':"""UKMET model (Interpolated 06 hours)""",
'UKX':"""UKMET [GFS tracker]""",
'UKX2':"""UKMET [GFS tracker] (Interpolated 12 hours)""",
'UKXI':"""UKMET [GFS tracker] (Interpolated 06 hours)""",
'UW42':"""UW-NMS 4km model (Interpolated 12 hours)""",
'UW4I':"""UW-NMS 4km model (Interpolated 06 hours)""",
'UWN2':"""UW-NMS 8km model (Interpolated 12 hours)""",
'UWN4':"""UW-NMS 4km model""",
'UWN8':"""UW-NMS 8km model""",
'UWNI':"""UW-NMS 8km model (Interpolated 06 hours)""",
'WRNG':"""Warning""",
'XTRP':"""Extrapolation using past 12-hr motion""",
    }

    aidDescLocal={
        'RR2MN':"""Psd RR2 Mean Ensemble """,
        'RR200':"""Psd RR2 Ensemble Control """,
        'RR201':"""Psd RR2 Ensemble Member 1""",
        'RR202':"""Psd RR2 Ensemble Member 2""",
        'RR203':"""Psd RR2 Ensemble Member 3""",
        'RR204':"""Psd RR2 Ensemble Member 4""",
        'RR205':"""Psd RR2 Ensemble Member 5""",
        'RR206':"""Psd RR2 Ensemble Member 6""",
        'RR207':"""Psd RR2 Ensemble Member 7""",
        'RR208':"""Psd RR2 Ensemble Member 8""",
        'RR209':"""Psd RR2 Ensemble Member 9""",
        'RR210':"""Psd RR2 Ensemble Member 10""",
        
        # -- direct pull/crack of  wmo-essential
        
        'EMDT':"""ECMWF HRES [GTS Tracker]""",
        'EM01':"""ECMWF model Ensemble +01 member [GTS tracker]""",
        'EM02':"""ECMWF model Ensemble +02 member [GTS tracker]""",
        'EM03':"""ECMWF model Ensemble +03 member [GTS tracker]""",
        'EM04':"""ECMWF model Ensemble +04 member [GTS tracker]""",
        'EM05':"""ECMWF model Ensemble +05 member [GTS tracker]""",
        'EM06':"""ECMWF model Ensemble +06 member [GTS tracker]""",
        'EM07':"""ECMWF model Ensemble +07 member [GTS tracker]""",
        'EM08':"""ECMWF model Ensemble +08 member [GTS tracker]""",
        'EM09':"""ECMWF model Ensemble +09 member [GTS tracker]""",
        'EM10':"""ECMWF model Ensemble +10 member [GTS tracker]""",
        'EM11':"""ECMWF model Ensemble +11 member [GTS tracker]""",
        'EM12':"""ECMWF model Ensemble +12 member [GTS tracker]""",
        'EM13':"""ECMWF model Ensemble +13 member [GTS tracker]""",
        'EM14':"""ECMWF model Ensemble +14 member [GTS tracker]""",
        'EM15':"""ECMWF model Ensemble +15 member [GTS tracker]""",
        'EM16':"""ECMWF model Ensemble +16 member [GTS tracker]""",
        'EM17':"""ECMWF model Ensemble +17 member [GTS tracker]""",
        'EM18':"""ECMWF model Ensemble +18 member [GTS tracker]""",
        'EM19':"""ECMWF model Ensemble +19 member [GTS tracker]""",
        'EM20':"""ECMWF model Ensemble +20 member [GTS tracker]""",
        'EM21':"""ECMWF model Ensemble +21 member [GTS tracker]""",
        'EM22':"""ECMWF model Ensemble +22 member [GTS tracker]""",
        'EM23':"""ECMWF model Ensemble +23 member [GTS tracker]""",
        'EM24':"""ECMWF model Ensemble +24 member [GTS tracker]""",
        'EM25':"""ECMWF model Ensemble +25 member [GTS tracker]""",
        'EM26':"""ECMWF model Ensemble +26 member [GTS tracker]""",
        'EM27':"""ECMWF model Ensemble +27 member [GTS tracker]""",
        'EM28':"""ECMWF model Ensemble +28 member [GTS tracker]""",
        'EM29':"""ECMWF model Ensemble +29 member [GTS tracker]""",
        'EM30':"""ECMWF model Ensemble +30 member [GTS tracker]""",
        'EM31':"""ECMWF model Ensemble +31 member [GTS tracker]""",
        'EM32':"""ECMWF model Ensemble +32 member [GTS tracker]""",
        'EM33':"""ECMWF model Ensemble +33 member [GTS tracker]""",
        'EM34':"""ECMWF model Ensemble +34 member [GTS tracker]""",
        'EM35':"""ECMWF model Ensemble +35 member [GTS tracker]""",
        'EM36':"""ECMWF model Ensemble +36 member [GTS tracker]""",
        'EM37':"""ECMWF model Ensemble +37 member [GTS tracker]""",
        'EM38':"""ECMWF model Ensemble +38 member [GTS tracker]""",
        'EM39':"""ECMWF model Ensemble +39 member [GTS tracker]""",
        'EM40':"""ECMWF model Ensemble +40 member [GTS tracker]""",
        'EM41':"""ECMWF model Ensemble +41 member [GTS tracker]""",
        'EM42':"""ECMWF model Ensemble +42 member [GTS tracker]""",
        'EM43':"""ECMWF model Ensemble +43 member [GTS tracker]""",
        'EM44':"""ECMWF model Ensemble +44 member [GTS tracker]""",
        'EM45':"""ECMWF model Ensemble +45 member [GTS tracker]""",
        'EM46':"""ECMWF model Ensemble +46 member [GTS tracker]""",
        'EM47':"""ECMWF model Ensemble +47 member [GTS tracker]""",
        'EM48':"""ECMWF model Ensemble +48 member [GTS tracker]""",
        'EM49':"""ECMWF model Ensemble +49 member [GTS tracker]""",
        'EM50':"""ECMWF model Ensemble +50 member [GTS tracker]""",
        'EMCN':"""ECMWF model Ensemble Control Member [GTS tracker]""",

        'CEDET':"""Canadian Model from XML""",
        
        'CEP00':"""Canadian model Ensemble Control Run""",
        'CEP01':"""Canadian model Ensemble +01 member""",
        'CEP02':"""Canadian model Ensemble +02 member""",
        'CEP03':"""Canadian model Ensemble +03 member""",
        'CEP04':"""Canadian model Ensemble +04 member""",
        'CEP05':"""Canadian model Ensemble +05 member""",
        'CEP06':"""Canadian model Ensemble +06 member""",
        'CEP07':"""Canadian model Ensemble +07 member""",
        'CEP08':"""Canadian model Ensemble +08 member""",
        'CEP09':"""Canadian model Ensemble +09 member""",
        'CEP10':"""Canadian model Ensemble +10 member""",
        'CEP11':"""Canadian model Ensemble +11 member""",
        'CEP12':"""Canadian model Ensemble +12 member""",
        'CEP13':"""Canadian model Ensemble +13 member""",
        'CEP14':"""Canadian model Ensemble +14 member""",
        'CEP15':"""Canadian model Ensemble +15 member""",
        'CEP16':"""Canadian model Ensemble +16 member""",
        'CEP17':"""Canadian model Ensemble +17 member""",
        'CEP18':"""Canadian model Ensemble +18 member""",
        'CEP19':"""Canadian model Ensemble +19 member""",
        'CEP20':"""Canadian model Ensemble +20 member""",

        'GEDET':"""NCEP AVN TC vortex tracker from XML""",
        'GEP00':"""GEFS Control Run""",
        'GEP01':"""GFS Ensemble +01 member""",
        'GEP02':"""GFS Ensemble +02 member""",
        'GEP03':"""GFS Ensemble +03 member""",
        'GEP04':"""GFS Ensemble +04 member""",
        'GEP05':"""GFS Ensemble +05 member""",
        'GEP06':"""GFS Ensemble +06 member""",
        'GEP07':"""GFS Ensemble +07 member""",
        'GEP08':"""GFS Ensemble +08 member""",
        'GEP09':"""GFS Ensemble +09 member""",
        'GEP10':"""GFS Ensemble +10 member""",
        'GEP11':"""GFS Ensemble +11 member""",
        'GEP12':"""GFS Ensemble +12 member""",
        'GEP13':"""GFS Ensemble +13 member""",
        'GEP14':"""GFS Ensemble +14 member""",
        'GEP15':"""GFS Ensemble +15 member""",
        'GEP16':"""GFS Ensemble +16 member""",
        'GEP17':"""GFS Ensemble +17 member""",
        'GEP18':"""GFS Ensemble +18 member""",
        'GEP19':"""GFS Ensemble +19 member""",
        'GEP20':"""GFS Ensemble +20 member""",

    }

    def __init__(self):
        self.allAids=self.aidDescJtwc.keys()+self.aidDescNhc.keys() + self.aidDescLocal.keys()

    def lsAids(self,mask=None):
        for aid in self.allAids:
            if(mask != None and mf.find(aid,mask.upper())):
                print 'aidmmm: ',aid
                continue
            elif(mask == None):
                print 'aid: ',aid

    def getAidDesc(self,aid,useNHC=1,useJT=0):
        gaid=aid.upper()

        if(len(gaid) == 0):
            return('NO LOAD AID')
        
        if(gaid[0:2] == 'EP' and len(gaid) == 4 and gaid[2:4].isdigit()):
            gaid='EE'+ gaid[2:4]


        if((gaid[0] == 'N' and len(gaid) == 5) or (gaid[1:] == 'EMX' or gaid[1:] == 'CMC' or gaid[1:] == 'NAM') ): 
            gaid=gaid[1:]

        if((gaid[0] == 'U' and len(gaid) == 5) and gaid != 'UEDET'):
            gaid='UE'+gaid[3:]
            
        if((gaid[0] == 'C' and len(gaid) == 5) ):
            gaid='CE'+gaid[2:]

        if((gaid[0] == 'G' and len(gaid) == 5) ):
            gaid='GE'+gaid[2:]


        try:
            descJ=self.aidDescJtwc[gaid]
        except:
            descJ=None

        try:
            descN=self.aidDescNhc[gaid]
        except:
            descN=None

        try:
            descL=self.aidDescLocal[gaid]
        except:
            descL=None



        if(descJ == None and descN == None and descL == None):
            ad=AidProp(gaid.lower(),warn=0)
            descA=ad.label
            if(descA == None): descA='NNOO description available for: %s'%(aid)

        if(useJT and descJ != None): 
            descF=descJ
        elif(useJT and descJ == None and descF != None): descF=dsecN

        if(useNHC and descN != None): 
            descF=descN
        elif(useNHC and descN == None and descJ != None): descF=descJ

        if(descJ == None and descN == None): 

            if(descL != None):
                descF=descL
            else:
                descF=descA

        return(descF)

# -- for mdeck
def PickBestDeck(decks1,decks2,verb=1,decktype='all'):

    curdtg=mf.dtg('dtgcurhr')

    decks1.sort()
    decks2.sort()

    decksall={}
    deckstcs=[]
    decks=[]

    if(len(decks1) > 0):
        for deck in decks1:
            (dir,file)=os.path.split(deck)
            storm=file[1:-4]
            #
            # jtwc is now using letters in the 4 position to indicate an invest that did not go to warning
            #
            if(file[3].isdigit()):
                deckstcs.append(storm)
                decksall[storm,1]=deck


    if(len(decks2) > 0):
        for deck in decks2:
            (dir,file)=os.path.split(deck)
            storm=file[1:-4]
            if(file[3].isdigit()):
                deckstcs.append(storm)
                decksall[storm,2]=deck

    if(len(deckstcs) == 0):
        return(decks)

    deckstcs=mf.uniq(deckstcs)
    deckstcs.sort()

    if(len(deckstcs) >= 1):

        for storm in deckstcs:

            isdummy=isinvest=isstorm=0

            snum=int(storm[2:4])

            cdtg1=cdtg2=None

            if(snum >= 80 and snum <= 89): isdummy=1
            if(snum >= 90 and snum <= 99): isinvest=1
            if(snum >= 1 and snum <= 50): isstorm=1

            #if(isdummy): continue
            try:
                deck1=decksall[storm,1]
            except:
                deck1=sz1=None

            try:
                deck2=decksall[storm,2]
            except:
                deck2=sz2=None

            if(deck1 != None):
                sz1=mf.GetPathSiz(deck1)
                #rc=mf.PathCreateTime(deck1)
                rc=mf.PathModifyTime(deck1)
                cdtg1=rc[2]

            if(deck2 != None):
                sz2=mf.GetPathSiz(deck2)
                #rc=mf.PathCreateTime(deck2)
                rc=mf.PathModifyTime(deck2)
                cdtg2=rc[2]

            if(deck1 != None and deck2 != None):
                tdiff=mf.dtgdiff(cdtg1,cdtg2)
                tdiffc1=mf.dtgdiff(curdtg,cdtg1)
                tdiffc2=mf.dtgdiff(curdtg,cdtg2)
            else:
                tdiff=tdiffc1=tdiffc2=None


            #
            # always go with first(official) deck if active
            #

            if(tdiff == None):
                if(deck1 != None):
                    deck=deck1
                elif(deck2 != None):
                    deck=deck2
            else:
                if(isstorm):
                    deck=deck1
                    #
                    #  if tdiff > 0.0, second deck is newer
                    #
                    if(tdiff > 0.0):
                        if(deck2 != None):
                            deck=deck2
                        elif(deck1 != None):
                            deck=deck1
                    #
                    #  if tdiff > 0.0, second deck is newer
                    #
                    elif(tdiff <= 0.0):
                        if(deck1 != None):
                            deck=deck1
                        elif(deck2 != None):
                            deck=deck2
                elif(isinvest):
                    #
                    #  if tdiff > 0.0, second deck is newer
                    #
                    if(tdiff > 0.0):
                        if(deck2 != None):
                            deck=deck2
                        elif(deck1 != None):
                            deck=deck1
                    #
                    #  if tdiff > 0.0, second deck is newer
                    #
                    elif(tdiff <= 0.0):
                        if(deck1 != None):
                            deck=deck1
                        elif(deck2 != None):
                            deck=deck2


            # go with nhc if equal sizes
            #
            if((sz1 != None and sz2 != None)):
                if(sz1 == sz2):
                    deck=deck1
                elif(sz1 > sz2):
                    deck=deck1
                elif(sz2 > sz1):
                    deck=deck2



            if(verb):
                print
                print 'aaaaaaaaaaaaaaa 111: ',deck1,sz1,curdtg,cdtg1
                print 'aaaaaaaaaaaaaaa 222: ',deck2,sz2,curdtg,cdtg2
                print 'aaaaaaaaaaaaa tdiff: ',tdiff,tdiffc1,tdiffc2
                print 'aaaaaaaaaaaaaaa FFF: ',deck

            decks.append(deck)

    return(decks)


# 20060125
#
# define consensus, make ukm, gfd, eco non req but must have 2 out of three
# make fg4/fv4 req against the optional to show impact

# these con are more op in that the almost always give a con so that a model
# will be penalized if not available, i.e., it has to be there to contribute,
# makes a harder, more demanding test 
#





if (__name__ == "__main__"):

    ad=aidDescTechList()
    ad.lsAids('nam')
    descF=ad.getAidDesc('nam')
    descF=ad.getAidDesc('avno')
    descF=ad.getAidDesc('nap01')
    print 'descF: ',descF
    descF=ad.getAidDesc('ap01')
    print 'descF: ',descF


    sys.exit()
    aids=['emx','fim9','fim900','hwrf','ecm2g']
    #aids=['fim900']
    aids=['fim900','ecm2','tecg2','ecm2g','tecm2','navgg','mgfs2']
    for aid in aids:
        aP=AidProp(aid)
        print 'AAA ',aid,aP.gotbase,aP.gotpost
        aP.ls('label')


    sys.exit()

    aP=AidProp('rapc')
    aP.ls()
    print '0000%s11111'%(aP.label)

    aP=AidProp('emx')
    print '0000%s11111'%(aP.label)

    sys.exit()
