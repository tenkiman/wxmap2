#!/bin/bash
# script create_diagfiles.sh
#####################################################################
# This script takes grib2 input and makes diagnostic files
# for each of the model initial times specified in input.list.
#####################################################################
# Required input files:
#   input.params
#   input.list
#   input.plvls   -added in Version 1.1
#   parent and nested grid files specified in input.list
#      (for all times specified in input.params)
#   adeck (track) file(s) for storm(s) in input.list
#####################################################################
# Version 1.1, last modified 02/11/2011
#   -added pressure level specification support, text field headers
#   -addressed missing vortex cases
#   -fixed missing fields, including surface fields and nested fields
# Version 1, 01/11/2011
#####################################################################

#:starting from home directory
homedir=`pwd`

#:specify directories for model grib2 files and diag files
maindir=${homedir}
outputdir=${maindir}'/diags/'
adeckdir=${homedir}'/modelships/inputfiles/adeck/'

cd ${maindir}

#:retrieve the maximum time, the time interval, and the model override
#: from the input.params file
#:-note: tmax, tint (in hrs); not currently set up for minutes
set `cat ${maindir}'input.params'`
#tmax=${1} tint=${2} smodel2=${3}
nlvls=${1} 
tmax=${2} 
tint=${3}
mnested=${4}
smodel2=${5} 
sruntype=${6} 
sversion=${7}

exit;
imiss=-9999
imissn=$(( ${imiss} * -1 ))

#nlvls=21
#tmax=126
#tint=6
#smodel2='hwrf'

#:currently specifying fixed runtype and version, can be altered
#: for inclusion in input.params at later time
#:added mnested flag to specify if nested grid exists
#mnested=1
#sruntype='d'
#sversion='oper'

#:add text strings for finding and printing fields
fieldbegT='TMP:'
fieldbegR='RH:'
fieldbegZ='HGT:'
fieldbegU='UGRD:'
fieldbegV='VGRD:'
fieldend=' mb'
fieldtextbeg='FIELD:'
fieldT='T_'
fieldR='R_'
fieldZ='Z_'
fieldU='U_'
fieldV='V_'
fieldP='P_'
fieldSST='SST'
fieldOHC='OHC'
fieldTPW='TPW'
fieldsurf='SURF'

#:loop through all available input files - initial times
#:-requires presence of parent grid; nested grid only will not work
#:-requires presence of nested grid (no adeck to provide center fix)
#:-will only accept pressure lvl data
for initfile in `cat ${maindir}input.list`
do
#:process filename
#   echo ${initfile}
   test -e ${initfile}
   if [ $? -ne 0 ]
   then
      echo 'initial file:'${initfile}' not found'
      exit 1
   fi
   initbase=`basename ${initfile}`
   initdir=`dirname ${initfile}`
#   echo ${initbase}
#   echo ${initdir}
   echo ${initbase} > ${maindir}'tname.txt'
   ./nameparse.x
#   rm tname.txt
   set `cat ${maindir}'tname2.txt'`
   sname=${1} snum=${2} sbasin=${3} sdtg=${4}
   syr=${5} smo=${6} sda=${7} sti=${8}
   smodel=${9} svert=${10} sgrid=${11} sfitype=${12}
   sforeti=${13} sfint=${14} sfipregr=${15} sfipostgrnt=${16}
#   echo ${sname}
#   echo ${snum}
   sfiout='s'${sbasin}${snum}${syr}'_'${smodel2}'_'${sruntype}${sversion}'_'${sdtg}'_diag.dat'
   sfiadeck=${adeckdir}'a'${sbasin}${snum}${syr}'.dat'
#   echo ${sfiout}
#   echo ${sfiadeck}
   test -e ${sfiadeck}
   if [ $? -ne 0 ]
   then
      echo 'track file:'${sfiadeck}' not found'
      exit 1
   fi
   cp ${sfiadeck} tempadeck.dat
#:set up control file for creating total diagnostic files
   dtxt='diaginfo.txt'
   echo ${nlvls} > ${dtxt}
   echo ${mnested} >> ${dtxt}
   echo ${tmax} >> ${dtxt}
   echo ${tint} >> ${dtxt}
   echo ${sdtg} >> ${dtxt}
   echo ${smodel} >> ${dtxt}
   echo ${sbasin} >> ${dtxt}
   echo ${snum} >> ${dtxt}
   echo ${sname} >> ${dtxt}

#:set base filenames for the chosen run
   pbase=${initdir}'/'${sfipregr}'p'${sfipostgrnt}
   nbase=${initdir}'/'${sfipregr}'n'${sfipostgrnt}
#   echo ${pbase}
#   echo ${nbase}

#:set output filenames for current forecast time (text files)
   outptxt=${maindir}temp_fieldp.txt
   outntxt=${maindir}temp_fieldn.txt

#:loop through times indicated by tmax and tint (starting at 0)
   currtime=0
   while [ $currtime -le $tmax ]
   do
#      echo "$currtime"
      if [ $currtime -lt 10 ]
      then
         pcurr=${pbase}'0'${currtime}
         ncurr=${nbase}'0'${currtime}
         fcurr='f00'${currtime}
         diagcurr='mdiagf00'${currtime}'.dat'
      elif [ $currtime -lt 100 ]
      then
         pcurr=${pbase}${currtime}
         ncurr=${nbase}${currtime}
         fcurr='f0'${currtime}
         diagcurr='mdiagf0'${currtime}'.dat'
      else
         pcurr=${pbase}${currtime}
         ncurr=${nbase}${currtime}
         fcurr='f'${currtime}
         diagcurr='mdiagf'${currtime}'.dat'
      fi
#      echo ${pcurr}
#      echo ${sdtg} ${smodel} ${imiss} ${currtime}
      test -e ${pcurr}
      if [ $? -ne 0 ]
      then
         echo 'parent grid:'${pcurr}' not found'
         exit 1
      fi
#      echo ${ncurr}
      test -e ${ncurr}
      if [ $? -ne 0 ]
      then
         echo 'nested grid:'${ncurr}' not found'
         exit 1
      fi
#      echo ${diagcurr}

#:get current center location from tmpadeck.dat
      echo ${sdtg} ${smodel} ${imiss} ${currtime} > tempadinfo.txt
#      cp tempadinfo.txt tempadinfo${fcurr}.txt
      ./getcenter.x
#      cp center.txt center${fcurr}.txt
#      echo center${fcurr}.txt >> ${dtxt}

      set `cat ${maindir}'center.txt'`
      centerlat=${1} centerlon=${2}
#      echo ${centerlat}
#      echo ${centerlon}

#:if center location exists at current time, get parent and nested grids
#: otherwise, skip grids and call null case for parameter file fill-in

      if [ ${centerlat} -eq ${imissn} ] || [ ${centerlon} -eq ${imissn} ]
      then
#:    fill in the missing value array here for current time
         ./inddiagnull.x
         mv params.txt params${fcurr}.txt
         echo params${fcurr}.txt >> ${dtxt}

      else
#:get parent grid information (nx, ny, lat, lon, lat/lon intervals)
         wgrib2 -nxny -d 1 ${pcurr} > tempnxny.txt
         wgrib2 -grid -d 1 ${pcurr} > templatlon.txt
         ./gridparse.x
         mv tempgrid.txt temp_gridp.txt

#:get parent grid fields
         fieldtext=${fieldtextbeg}${fieldT}${fieldsurf}
         echo ${fieldtext} > ${outptxt}
         wgrib2 -match "TMP:2 m" -append -text ${outptxt} ${pcurr}
         fieldtext=${fieldtextbeg}${fieldR}${fieldsurf}
         echo ${fieldtext} >> ${outptxt}
         wgrib2 -match "RH:2 m" -append -text ${outptxt} ${pcurr}
         fieldtext=${fieldtextbeg}${fieldU}${fieldsurf}
         echo ${fieldtext} >> ${outptxt}
         wgrib2 -match "UGRD:10 m" -append -text ${outptxt} ${pcurr}
         fieldtext=${fieldtextbeg}${fieldV}${fieldsurf}
         echo ${fieldtext} >> ${outptxt}
         wgrib2 -match "VGRD:10 m" -append -text ${outptxt} ${pcurr}
         fieldtext=${fieldtextbeg}${fieldP}${fieldsurf}
         echo ${fieldtext} >> ${outptxt}
         wgrib2 -match "PRMSL" -append -text ${outptxt} ${pcurr}

#:cycle through specified pressure levels to retrieve sounding data
         for currplvl in `cat ${maindir}input.plvls`
         do
            if [ $currplvl -lt 10 ]
            then
               currplvlt='000'${currplvl}
            elif [ $currplvl -lt 100 ]
            then
               currplvlt='00'${currplvl}
            elif [ $currplvl -lt 1000 ]
            then
               currplvlt='0'${currplvl}
            else
               currplvlt=${currplvl}
            fi
            fieldtext=${fieldtextbeg}${fieldT}${currplvlt}
            echo ${fieldtext} >> ${outptxt}
            fieldname=${fieldbegT}${currplvl}${fieldend}
            wgrib2 -match "${fieldname}" -append -text ${outptxt} ${pcurr}
            fieldtext=${fieldtextbeg}${fieldR}${currplvlt}
            echo ${fieldtext} >> ${outptxt}
            fieldname=${fieldbegR}${currplvl}${fieldend}
            wgrib2 -match "${fieldname}" -append -text ${outptxt} ${pcurr}
            fieldtext=${fieldtextbeg}${fieldZ}${currplvlt}
            echo ${fieldtext} >> ${outptxt}
            fieldname=${fieldbegZ}${currplvl}${fieldend}
            wgrib2 -match "${fieldname}" -append -text ${outptxt} ${pcurr}
            fieldtext=${fieldtextbeg}${fieldU}${currplvlt}
            echo ${fieldtext} >> ${outptxt}
            fieldname=${fieldbegU}${currplvl}${fieldend}
            wgrib2 -match "${fieldname}" -append -text ${outptxt} ${pcurr}
            fieldtext=${fieldtextbeg}${fieldV}${currplvlt}
            echo ${fieldtext} >> ${outptxt}
            fieldname=${fieldbegV}${currplvl}${fieldend}
            wgrib2 -match "${fieldname}" -append -text ${outptxt} ${pcurr}
         done

         fieldtext=${fieldtextbeg}${fieldTPW}
         echo ${fieldtext} >> ${outptxt}
         wgrib2 -match "PWAT" -append -text ${outptxt} ${pcurr}
         fieldtext=${fieldtextbeg}${fieldSST}
         echo ${fieldtext} >> ${outptxt}
         wgrib2 -match "WTMP:surf" -append -text ${outptxt} ${pcurr}

#:if nested grid specified:
         if [ ${mnested} -eq 1 ]
         then
#:get nested grid information (nx, ny, lat, lon, lat/lon intervals)
            wgrib2 -nxny -d 1 ${ncurr} > tempnxny.txt
            wgrib2 -grid -d 1 ${ncurr} > templatlon.txt
            ./gridparse.x
            mv tempgrid.txt temp_gridn.txt
#:get nested grid fields
            fieldtext=${fieldtextbeg}${fieldU}${fieldsurf}
            echo ${fieldtext} > ${outntxt}
            wgrib2 -match "UGRD:10 m" -append -text ${outntxt} ${ncurr}
            fieldtext=${fieldtextbeg}${fieldV}${fieldsurf}
            echo ${fieldtext} >> ${outntxt}
            wgrib2 -match "VGRD:10 m" -append -text ${outntxt} ${ncurr}
            fieldtext=${fieldtextbeg}${fieldP}${fieldsurf}
            echo ${fieldtext} >> ${outntxt}
            wgrib2 -match "PRMSL" -append -text ${outntxt} ${ncurr}
            fieldtext=${fieldtextbeg}${fieldSST}
            echo ${fieldtext} >> ${outntxt}
            wgrib2 -match "WTMP:surf" -append -text ${outntxt} ${ncurr}
         fi

#:run diagnostic parameter calculation for current time
         ./inddiag.x
         mv params.txt params${fcurr}.txt
         echo params${fcurr}.txt >> ${dtxt}

      fi   #finish if statement for reading and calculating parameters

      currtime=$(( $currtime + $tint ))
   done   #finish loop for each individual time

#:run diagnostic file output from accumulation of individual times
   ./totaldiag.x
   mv diag.txt ${outputdir}${sfiout}

done   #finish loop for each specified initial file

exit 1

#:remove temporary files
rm tname.txt
rm tname2.txt
rm temp*
#:remove temporary parameter files (individual times)
rm center*
rm params*
rm diaginfo.txt

exit 0
