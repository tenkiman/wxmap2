import w2

Color2Hex={}
Color2Hex['black']='#000000'
Color2Hex['white']='#FFFFFF'

Color2Hex['navy']='#000080'
Color2Hex['royalblue']='#4169E1'
Color2Hex['steelblue']='#4682B4'
Color2Hex['usafblue']='#CCCCFF'
Color2Hex['mediumslateblue']='#7B68EE'
Color2Hex['mediumblue']='#0000CD'
Color2Hex['powderblue']='#B0E0E6'

Color2Hex['yellow']='#FFFF00'
Color2Hex['gold']='#FFD700'
Color2Hex['yellowgreen']='#9ACD32'
Color2Hex['khaki']='#F0E68C'
Color2Hex['goldenrod']='#DAA520'
Color2Hex['lightgoldenrodyellow']='#FAFAD2'
Color2Hex['tan']='#D2B48C'

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
Color2Hex['darkgreen']='#006400'

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

GaColorRgb={}

GaColorRgb[0] =[0,0,0]
GaColorRgb[1] =[255,255,255]
GaColorRgb[2] =[250,60,60]
GaColorRgb[3] =[0,220,0]
GaColorRgb[4] =[30,60,255]
GaColorRgb[5] =[0,200,200]
GaColorRgb[6] =[240,0,130]
GaColorRgb[7] =[230,220,50]
GaColorRgb[8] =[240,130,40]
GaColorRgb[9] =[160,0,200]
GaColorRgb[10]=[160,230,50]
GaColorRgb[11]=[0,160,255]
GaColorRgb[12]=[230,175,45]
GaColorRgb[13]=[0,210,140]
GaColorRgb[14]=[130,0,220]
GaColorRgb[15]=[170,170,170]

GaColorName2Rgb={}
GaColorName2Rgb['black']=GaColorRgb[0] 
GaColorName2Rgb['white']=GaColorRgb[1] 
GaColorName2Rgb['red']=GaColorRgb[2] 
GaColorName2Rgb['green']=GaColorRgb[3] 
GaColorName2Rgb['blue']=GaColorRgb[4] 
GaColorName2Rgb['lightblue']=GaColorRgb[5] 
GaColorName2Rgb['magenta']=GaColorRgb[6] 
GaColorName2Rgb['yellow']=GaColorRgb[7] 
GaColorName2Rgb['orange']=GaColorRgb[8] 
GaColorName2Rgb['purple']=GaColorRgb[9] 
GaColorName2Rgb['yellowgreen']=GaColorRgb[10]
GaColorName2Rgb['mediumblue']=GaColorRgb[11]
GaColorName2Rgb['darkyellow']=GaColorRgb[12]
GaColorName2Rgb['aqua']=GaColorRgb[13]
GaColorName2Rgb['darkpurple']=GaColorRgb[14]
GaColorName2Rgb['gray']=GaColorRgb[15]

#  0   background       0   0   0 (black by default)
#  1   foreground     255 255 255 (white by default)
#  2   red            250  60  60 
#  3   green            0 220   0 
#  4   dark blue       30  60 255 
#  5   light blue       0 200 200 
#  6   magenta        240   0 130 
#  7   yellow         230 220  50 
#  8   orange         240 130  40 
#  9   purple         160   0 200 
# 10   yellow/green   160 230  50 
# 11   medium blue      0 160 255 
# 12   dark yellow    230 175  45 
# 13   aqua             0 210 140 
# 14   dark purple    130   0 220 
# 15   gray           170 170 170 


    
def hex2dec(s):
    return int(s, 16)

def dec2hex(n):
    """return the hexadecimal string representation of integer n"""
    return "%X" % n

def hex2rgb(scolor):

    r=hex2dec(scolor[1:3])
    g=hex2dec(scolor[3:5])
    b=hex2dec(scolor[5:7])
    return(r,g,b)


if (__name__ == "__main__"):

    mcol='teal'

    scolor=Color2Hex[mcol]

    print scolor
    (r,g,b)=hex2rgb(scolor)
    print r,g,b
    
    
    


