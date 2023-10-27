



def GetTdos(b1id):

    tdos='uKN'
    if(b1id == 'L' or b1id == 'E'):
        tdos=['SRS','LAA','JLB','JLF','RDK','RJP','___',
              'JDP','RTM','TAC','RWF','SHH','KRK',
              'DPB','ESB','HSM','JRR','MMM']

    #
    # jtwc tdo veri
    #
    if(b1id == 'W' or b1id == 'I' or b1id == 'B' or b1id == 'S' or b1id == 'P'):
        tdos=['CAB','JMM','JSB','JSD','RMK','JWL','YOP','___',
              'ADL','BGH','JWF','KAP','MBS','MEK','SGB',
	      'JAM','GPR']

    return(tdos)
        

def TdoColors():
    
    tdocolor={}
    Color2Hex={}
    Color2Hex['black']='#000000'


    Color2Hex['navy']='#000080'
    Color2Hex['royalblue']='#4169E1'
    Color2Hex['steelblue']='#4682B4'
    Color2Hex['usafblue']='#CCCCFF'
    Color2Hex['mediumslateblue']='#7B68EE'
    Color2Hex['mediumblue']='#0000CD'
    
    Color2Hex['yellow']='#FFFF00'
    Color2Hex['gold']='#FFD700'
    Color2Hex['yellowgreen']='#9ACD32'
    Color2Hex['khaki']='#F0E68C'
    Color2Hex['goldenrod']='#DAA520'
    Color2Hex['lightgoldenrodyellow']='#FAFAD2'
    
    Color2Hex['wheat']='#F5DEB3'
    Color2Hex['usafgrey']='#51588E'
    Color2Hex['grey1']='#CCCCCC'
    Color2Hex['grey2']='#999999'
    Color2Hex['grey3']='#666666'
    Color2Hex['grey4']='#333333'
    Color2Hex['grey']='#808080'
    Color2Hex['garnet']='#990000'
    Color2Hex['magenta']='#FF00FF'
    Color2Hex['maroon']='#800000'
    
    Color2Hex['green']='#008000'
    Color2Hex['greenyellow']='#ADFF2F'
    Color2Hex['olive']='#808000'
    Color2Hex['mediumseagreen']='#3CB371'
    
    Color2Hex['red']='#FF0000'
    Color2Hex['tomato']='#FF4637'
    Color2Hex['indianred']='#CD5C5C'
    Color2Hex['darkred']='#8B0000'
    Color2Hex['lightcoral']='#F08080'
    Color2Hex['orange']='#FFA500'
    
    Color2Hex['orchid']='#DA70D6'
    Color2Hex['violet']='#EE82EE'
    Color2Hex['fuchsia']='#FF00FF'
    
    Color2Hex['purple']='#800080'
    Color2Hex['indigo']='#4B0082'
    Color2Hex['plum']='#DDA0DD'
    Color2Hex['violetred']='#D02090'
    Color2Hex['teal']='#008080'
    

#
# NHC S(upreme) HS
#

    tdocolor['JLB']='grey'
    tdocolor['JLF']='gold'
    tdocolor['LAA']='magenta'
    tdocolor['RDK']='green'
    tdocolor['RJP']='garnet'
    tdocolor['SRS']='navy'
#
# NHC pitch hitters
#
    tdocolor['HPC']='usafblue'
    tdocolor['HSM']='darkred'
#
# cphc, misc
#
    tdocolor['JDP']='khaki'
    tdocolor['RTM']='khaki'
    tdocolor['TAC']='khaki'
    tdocolor['RWF']='khaki'
    tdocolor['SHH']='khaki'
    tdocolor['KRK']='khaki'

#
# NHCjunior HS
#
    tdocolor['DPB']='purple'
    tdocolor['ESB']='orange'
    tdocolor['JRR']='indigo'
    tdocolor['MMM']='lightcoral'
    
    tdocolor['all']='wheat'
    

#
# JTWC 2005-2006
#
    tdocolor['JSB']='grey'
    tdocolor['CAB']='gold'
    tdocolor['JWL']='magenta'
    tdocolor['RMK']='usafblue'
    tdocolor['JSD']='green'
    tdocolor['JMM']='navy'
    tdocolor['YOP']='orchid'
    tdocolor['___']='red'
#
# 2007 crew
#
    tdocolor['ADL']='black'
    tdocolor['BGH']='black'
    tdocolor['JWF']='black'
    tdocolor['KAP']='black'
    tdocolor['MBS']='black'
    tdocolor['MEK']='black'
    tdocolor['SJB']='black'


    return(tdocolor,Color2Hex)


def TdoNameTitles():

    tdoname={}
#
# NHC
#
    tdoname['JLB']='Dr. Bevin'
    tdoname['JLF']='Mr. Franklin'
    tdoname['LAA']='Dr. Avila'
    tdoname['RDK']='Dr. Knabb'
    tdoname['RJP']='Dr. Pasch'
    tdoname['SRS']='Mr. Stewart'
    tdoname['MMM']='Ms. Mainelli'
    tdoname['ESB']='Mr. Twister-Blake'
    tdoname['JRR']='Mr. Rhome'
    tdoname['DPB']='Mr. Brown'
#
#  nhc pitch hitters
#
    tdoname['HSM']='Hurr Supp Met'
    tdoname['HPC']='HPC, NCEP'
#
#  cphc
#
    tdoname['JDP']='Mr. Powell'
    tdoname['RTM']='Ms.undef RTM'
    tdoname['TAC']='Ms.undef TAC'
    tdoname['RWF']='Ms.undef RWF'
    tdoname['SHH']='Ms.undef SHH'
    tdoname['KRK']='Ms.undef KRK'

#
# JTWC
#

    tdoname['JSB']='Capt Blackerby, USAF'
    tdoname['CAB']='Capt Bower, USAF'
    tdoname['JWL']='Capt Leffler, USAF'
    tdoname['RMK']='Capt Kehoe, USAF'
    tdoname['JSD']='LCDR Dixon, USN'
    tdoname['JMM']='LT Marburger, USN'
    tdoname['YOP']='LT Pitts, USN'
    tdoname['___']='Mr. NOBODY'

    tdoname['ADL']='LT Aaron Lana, USN'
    tdoname['BGH']='LCDR Brad Harris,USN'
    tdoname['MBS']='Capt Matt Stratton, USAF'

#
# 2007
#
    tdoname['KAP']='Capt Katryn Payne, USAF (kathryn.payne@navy.mil)'
    tdoname['JWF']='Capt Joel Fenlason, USAF  (joel.fenlason@navy.mil)'
    tdoname['MEK']='LT Matt Kucas, USN (matthew.kucas@navy.mil)'
    tdoname['SJB']='Mr. Steve Barlow (stephen.barlow@navy.mil)'
    tdoname['MDV']='LT Mike Vancas, USN (michael.vancas@navy.mil)'
#
# new in 2008
#
    tdoname['JAM']='ENS Mayers, USN (john.a.mayers@navy.mil)'
    tdoname['GPR']='LT Ray, USN (greg.ray1@navy.mil)'


    return(tdoname)


def FcTdoSign(dtg,stmid):

    basin=stmid[2:3]
    
    if(basin == 'W'):

        sig={
            '2006051400':'RMK',
            '2006063012':'RMK',
            '2006070500':'RMK',
            '2006071000':'CAB',
            '2006071806':'CAB',
            '2006071818':'JSB',
            '2006072206':'RMK',
            '2006073106':'ADL',
            '2006080618':'CAB',
            '2006081218':'ADL',
            '2006081318':'ADL',
            '2006081400':'ADL',
            '2006081600':'MEK',
            '2006091018':'ADL',
            '2006091118':'CAB',
            '2006091218':'CAB',
            '2006091318':'ADL',
            '2006091418':'ADL',
            '2006091706':'JMM',
            '2006091712':'JMM',
            '2006091818':'MEK',
            '2006092518':'CAB',
            '2006100206':'MBS',
            '2006100212':'MBS',
            '2006100918':'MBS',
            '2006101000':'MBS',
            '2006101018':'MBS',
            '2006101100':'MBS',
            '2006102806':'MBS',
            '2006102812':'MBS',
            '2006102906':'MBS',
            '2006102912':'MBS',
            '2006103006':'MBS',
            '2006103012':'MBS',
            '2006110906':'JSB',
            '2006110918':'ADL',
            '2006111018':'MBS',
            '2006111100':'MBS',
            '2006112718':'ADL',
            '2006113018':'SJB',
            '2006120718':'JWF',
            '2006120918':'MBS',
            '2006121118':'KAP',
            }
        
    else:
        
        sig={}

    try:
        tdo=sig[dtg]
    except:
        tdo=None

    return(tdo)



 
