From karin.meier@dkrz.deThu Apr 25 13:53:29 1996
Date: Mon, 1 Apr 1996 16:04:36 -0600
From: Karin Meier <karin.meier@dkrz.de>
To: Mike Fiorino <fiorino@typhoon.llnl.gov>
Subject: Re: spinning globe script

Hello Mike,

sorry for the late reply, but I had stayed the last week in Munich.
I've appended the spinning globes script at this mail.

Bye,
Karin

------------------ cut here ---------------------------------------------------
'reinit'
'open DKRZ_a50.ctl'
'open DKRZ_a100.ctl'
'enable print orthogr.mf'

palette()

lonmin =  -360.0
lonmax =  -180.0
latmin =  -90.0
latmax =   90.0
max    =   36
inc    =   10.0

cint = 1.0
cmin = -6.0
cmax =  6.0
lev1 = "-6.0 -5.0 -4.0 -3.0 -2.0 -1.0 0.0 "
lev2 = "1.0 2.0 3.0 4.0 5.0 6.0"
levels = lev1%lev2
col1 = "17   18   19   21   22  23  24  25  26  27  "
col2 = "28  29  30  50"
colors = col1%col2

'set vpage 0.0 11.0 0.0 8.5'
'set parea 1.0 10.0 1.4 8.5'
'set dbuff on'
'set lat 'latmin' 'latmax
'set lon 'lonmin' 'lonmax
'set mpvals 'lonmin' 'lonmax' 'latmin' 'latmax
'set map 1 1 8'
'set mproj orthogr'
'set grid on 5 1'
'set gxout shaded'

count = 0

while (count < max)
  'set parea 1.0 10.0 1.4 8.5'
  'set strsiz 0.22 0.24'
  'set string 1 tc 0.18'
  'draw string 5.5 7.85 Szenario A'
  l0 = lonmin + (count * inc)
  l1 = lonmax + (count * inc)
  'set lon 'l0' 'l1
  'set mpvals 'l0' 'l1' 'latmin' 'latmax
  'set grads off'
  'set parea 1.0 5.3 1.4 7.9'
  'set cint 'cint
  'set cmin 'cmin
  'set cmax 'cmax
  'set clevs 'levels
  'set ccols 'colors
  'd sza.1'
  'draw title A50'
  'set parea 5.7 10.0 1.4 7.9'
  'set cint 'cint
  'set cmin 'cmin
  'set cmax 'cmax
  'set clevs 'levels
  'set ccols 'colors
  'd sza.2'
  'draw title A100'
  'run /usr/people/k202043/grads/Scripts/cbar.gs'
  'set clip 1.0 10.0 1.4 7.9'
  'swap'
  count = count + 1
endwhile

'print'
'disable print'

**************************************
function palette()
***************************************
*
* color palette fuer szenarien video....
* entsprechend NCAR indices!
*
'set rgb  16  0  0  20'
'set rgb  17  0  29  85'
'set rgb  18  0  44  128'
'set rgb  19  0  83  230'
'set rgb  20  0  112  225'
'set rgb  21  0  151  250'
'set rgb  22  104  173  255'
'set rgb  23  177  213  255'
'set rgb  24  255  250  110'
'set rgb  25  255  209  116'
'set rgb  26  255  160  80'
'set rgb  27  255  100  65'
'set rgb  28  238  44  0'
'set rgb  29  182  34  0'
'set rgb  30  122  22  0'
'set rgb  50  100  22  0'
'set rgb  51  255  255  170'
'set rgb  52  200  240  255'
return

-------------- cut here
--------------------------------------------------------

-- 
--------------------- Deutsches Klimarechenzentrum GmbH ----------------------
                 (German Climate Computing Center - Hamburg)
  Karin Meier                   | 
  DKRZ - Hamburg                | 
  Bundesstr. 55                 | e-mail:       karin.meier@dkrz.de
  D-20146 Hamburg               | phone:        +49 40 41173 332
  Germany                       | fax:          +49 40 41173 270
------------------------------------------------------------------------------
