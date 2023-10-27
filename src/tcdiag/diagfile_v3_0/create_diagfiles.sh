#!/bin/bash
# script create_diagfiles.sh
###############################################################################
# This script takes grib2 input and makes diagnostic files
# for each of the model initial times specified in input.list.
# See README for further details.
###############################################################################
# Required input files:
#   -input.params
#   -input.list
#   -input.plvls   -added in Version 1.1
#   -parent and nested grid files 
#      -for cases specified in input.list
#      -for all times specified in input.params
#   -adeck (track) file(s) for storm(s) in input.list
###############################################################################
# Version 3.0, last modified 05/15/2015
#   -updated parameters pulled from input.params
#   -replaced nameparse.f with filename parsing in create_diagfiles.sh
#   -replaced getcenter.f with adeck (track) parsing in create_diagfiles.sh
#      -removed dataio.f, dataioparms.inc, dataformats.inc
#   -replaced gridparse.f with grid parsing in create_diagfiles.sh
#   -added handling of all global basins
#      -updated gbland.f; added aland.f, shland.f, wland.f
#      -updated aland.dat, shland.dat, wland.dat
#   -removed all early exit conditions from create_diagfiles.sh
#      -for missing initial files and tracks, script will proceed to next case
#      -for missing grids, script will fill forecast hour with missing values
# Version 2.1, last modified 12/31/2012
#   -added alternate field names for SLP, SST for nested grid
#   -added control flag and files for printing averaging radii
#   -adjusted exit on missing nest file to not occur when parent file
#    is missing as well
# Version 2.0, last modified 08/07/2012, created 03/02/2012
#   -added ifort compilation support
#   -adjusted handling of global models to adjust for lack of nests
#   -shifted from ascii data files to binary data files
#   -added alternate field names for surface T, SLP, and SST
#   -code maintenance
# Version 1.1, last modified 02/11/2011
#   -added pressure level specification support, text field headers
#   -addressed missing vortex cases
#   -fixed missing fields, including surface fields and nested fields
# Version 1, 01/11/2011
###############################################################################

date

###############################################################################
#Setup directories
###############################################################################

#:setup base directory
homedir=${HOME}'/'
currdir=`pwd`
basedir=${currdir}'/'

#:specify directories for diagnostic code and diag files
maindir=${basedir}'code/'
outputdir=${basedir}'diag_out/'

cd ${maindir}

###############################################################################
#Specify email logging information (if flag enabled in input.params)
###############################################################################

logemailfile=${maindir}"diagemail.log"
date > ${logemailfile}

###############################################################################
#Begin code
###############################################################################

#:retrieve the maximum time, the time interval, and the model override
#: from the input.params file
#:-note: tmax, tint (in hrs); not currently set up for minutes
set `cat ${maindir}'input.params'`
nlvls=${1}       #number of pressure levels specified in input.plvls
tmax=${2}        #maximum forecast hour to process
tint=${3}        #interval between forecast hours
mnested=${4}     #if 1, process nested grid as well as parent grid
mnameflag=${5}   #if 0, use smodel from input file in output; else use smodel2
smodel2=${6}     #user-designated output model id
sruntype=${7}    #one-character runtype designator for output
sversion=${8}    #four-character version specification for output
logemailflag=${9}   #if 1, then send email with details about run
logemail=${10}      #email address used with logemailflag=1

if [ ${logemailflag} -eq 1 ]
then
   echo "Email logging is specified, sending mail to ${logemail}"
fi

#:number of times that will be processed based on user-provided tmax and tint
#:tmin is assumed to be zero [(tmax-tmin)/tint + 1]
ntimes=$(( $tmax / $tint + 1 ))

imiss=-9999
imissn=$(( ${imiss} * -1 ))

#:specify text strings for finding and printing fields
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

#:setup variables to keep track of how many input files are provided
#: and how many output files are produced
countinput=`cat ${maindir}input.list | wc -l`
countdiag=0

#:loop through all available input files - initial times
#:-will only accept pressure lvl data on regular lat/lon grid
for initfile in `cat ${maindir}input.list`
do
#:process filename
   if [ ! -s ${initfile} ]
   then
      echo "Error: initial file: ${initfile} not found, skipping." | tee -a ${logemailfile}
      continue
   fi
   initbase=`basename ${initfile}`
   initdir=`dirname ${initfile}`

#
#: parse initial filename - HWRF model specific
#
   nameinfo=`echo ${initbase} | awk 'BEGIN { FS="."} { print $1 ; }'`
   dtginfo=`echo ${initbase} | awk 'BEGIN { FS="."} { print $2 ; }'`
   gridinfo=`echo ${initbase} | awk 'BEGIN { FS="."} { print $3 ; }'`
   ftimeinfo=`echo ${initbase} | awk 'BEGIN { FS="."} { print $4 ; }'`

   #processing variable-length nameinfo portion of filename {sname, snum, sbasin}
   nameinfolen=`expr $nameinfo : '.*'`
   namelen=`expr $nameinfolen - 3`
   basinchar=${nameinfolen}
   numstartchar=`expr $nameinfolen - 2`
   numendchar=`expr $nameinfolen - 1`
   sname=`echo ${nameinfo} | cut -c1-${namelen}`
   snameuc=`echo ${sname} | tr 'a-z' 'A-Z'`
   snum=`echo ${nameinfo} | cut -c${numstartchar}-${numendchar}`
   cbasin=`echo ${nameinfo} | cut -c${basinchar}`
   #the one-character basin designator needs to be converted to two-character
   #for reference: l=al, e=ep, c=cp, w=wp, i=io, 
   #               b=bb(io), a=na(io), s=si(sh), p=sp(sh), q=sl
   #               cbasin contains the one-character (sub-)basin designator
   #               sbasin contains the lower-case two-character basin
   #               subbasin contains the lower-case two-character (sub-)basin
   if [ ${cbasin} == 'l' ]
   then
      sbasin='al'
      subbasin=${pbasin}
   elif [ ${cbasin} == 'e' ]
   then
      sbasin='ep'
      subbasin=${pbasin}
   elif [ ${cbasin} == 'c' ]
   then
      sbasin='cp'
      subbasin=${pbasin}
   elif [ ${cbasin} == 'w' ]
   then
      sbasin='wp'
      subbasin=${pbasin}
   elif [ ${cbasin} == 'i' ]
   then
      sbasin='io'
      subbasin=${pbasin}
   elif [ ${cbasin} == 'b' ]
   then
      sbasin='io'
      subbasin='bb'
   elif [ ${cbasin} == 'a' ]
   then
      sbasin='io'
      subbasin='na'
   elif [ ${cbasin} == 's' ]
   then
      sbasin='sh'
      subbasin='si'
   elif [ ${cbasin} == 'p' ]
   then
      sbasin='sh'
      subbasin='sp'
   elif [ ${cbasin} == 'q' ]
   then
      sbasin='sl'
      subbasin=${pbasin}
   else
      echo "Unrecognized basin: ${cbasin}, skipping."
      continue
   fi
   sbasinuc=`echo ${sbasin} | tr 'a-z' 'A-Z'`
   subbasinuc=`echo ${subbasin} | tr 'a-z' 'A-Z'`

   #processing dtginfo portion of filename {sdtg, syr, smo, sda, sti}
   sdtg=$dtginfo
   syr=`echo ${sdtg} | cut -c1-4`
   smo=`echo ${sdtg} | cut -c5-6`
   sda=`echo ${sdtg} | cut -c7-8`
   sti=`echo ${sdtg} | cut -c9-10`

   #adjusting storm year if southern hemisphere storm (July-Dec: syr=syr+1)
   if [ ${cbasin} == 's' ] || [ ${cbasin} == 'p' ] || [ ${cbasin} == 'q' ]
   then
      if [ $smo -ge 7 ]
      then
         syr=$(( ${syr} + 1 ))
      fi
   fi

   #processing gridinfo portion of filename {smodel, svert, sgrid}
   smodel=`echo ${gridinfo} | cut -c1-4`
   smodeluc=`echo ${smodel} | tr 'a-z' 'A-Z'`
#   smodellc=`echo ${smodel} | tr 'A-Z' 'a-z'`
   svert=`echo ${gridinfo} | cut -c5-7`
   sgrid=`echo ${gridinfo} | cut -c9`

   #processing variable-length ftimeinfo portion of filename {sfitype, sforeti(unused)}
   ftimeinfolen=`expr $ftimeinfo : '.*'`
   sfitype=`echo ${ftimeinfo} | cut -c1-4`
   fhourbase=`echo ${ftimeinfo} | cut -c6-${ftimeinfolen}`
   fhournumchar=`expr $ftimeinfolen - 5`
   if [ ${fhournumchar} -eq 2 ]
   then
      fhour="0${fhourbase}"
   elif [ ${fhournumchar} -eq 3 ]
   then
      fhour=${fhourbase}
   else
      echo "Unrecognized forecast hour from filename ${initbase}: ${fhourbase}"
   fi
   sforeti=${fhour}

   #putting together partial filenames
   sfint="${nameinfo}.${dtginfo}.${gridinfo}.${sfitype}f"
   sfipregr="${nameinfo}.${dtginfo}.${smodel}${svert}_"
   sfipostgrnt=".${sfitype}f"
#   echo "$sfint $sfipregr $sfipostgrnt"

#
#: specify diagnostic filename and adeck filename
#
#* change handling of adeck files
#*   sfiadeck=${adeckdir}'a'${sbasin}${snum}${syr}'.dat'
   adeckdir=${initdir}'/'
   sfiadeck=${adeckdir}${nameinfo}'.'${dtginfo}'.trak.'${smodel}'.atcfunix'

#:check for adeck/track file
   echo 'looking for track file:'${sfiadeck}
   if [ ! -s ${sfiadeck} ]
   then
      echo 'track file:'${sfiadeck}' not found'
      sfiadeck=${adeckdir}'a'${sbasin}${snum}${syr}'_'${smodeluc}'_'${sdtg}'.dat'
      echo 'looking for track file:'${sfiadeck}
      if [ ! -s ${sfiadeck} ]
      then
         echo 'track file:'${sfiadeck}' not found'
         sfiadeck=${adeckdir}'a'${subbasin}${snum}${syr}'_'${smodeluc}'_'${sdtg}'.dat'
         echo 'looking for track file:'${sfiadeck}
         if [ ! -s ${sfiadeck} ]
         then
            echo "Error: track file for initial file: ${initfile} not found, skipping." | tee -a ${logemailfile}
            continue
         else
            cat ${sfiadeck} | sed "s/^${subbasinuc}/${sbasinuc}/g" > tempadeck.dat
         fi
      else
         cp ${sfiadeck} tempadeck.dat
      fi
   else
      cp ${sfiadeck} tempadeck.dat
   fi
#   cp ${sfiadeck} tempadeck.dat

#:name output diagnostic file
   if [ ${mnameflag} -ne 0 ]
   then
      sfiout='s'${sbasin}${snum}${syr}'_'${smodel2}'_'${sruntype}${sversion}'_'${sdtg}'_diag.dat'
   else
      sfiout='s'${sbasin}${snum}${syr}'_'${smodel}'_'${sruntype}${sversion}'_'${sdtg}'_diag.dat'
   fi

#
#:set up control file for creating total diagnostic files
#
   dtxt='diaginfo.txt'
   echo ${nlvls} > ${dtxt}
   echo ${mnested} >> ${dtxt}
   echo ${tmax} >> ${dtxt}
   echo ${tint} >> ${dtxt}
   echo ${sdtg} >> ${dtxt}
   if [ ${mnameflag} -eq 0 ]
   then
      echo ${smodeluc} >> ${dtxt}
   else
      smodel2uc=`echo ${smodel2} | tr 'a-z' 'A-Z'`
      echo ${smodel2uc} >> ${dtxt}
   fi
   echo ${sbasinuc} >> ${dtxt}
   echo ${snum} >> ${dtxt}
   echo ${snameuc} >> ${dtxt}

#:set base filenames for the chosen run
   pbase=${initdir}'/'${sfipregr}'p'${sfipostgrnt}
   nbase=${initdir}'/'${sfipregr}'n'${sfipostgrnt}

#:set output filenames for current forecast time (text files)
   outptxt=${maindir}temp_fieldp.txt
   outntxt=${maindir}temp_fieldn.txt

#:loop through times indicated by tmax and tint (starting at 0)
   currtime=0
   countmiss=0
   while [ $currtime -le $tmax ]
   do
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
#:tests for existence of parent grid
      pgexist=1
      if [ ! -s ${pcurr} ]
      then
         echo "Error: parent grid:${pcurr} not found." | tee -a ${logemailfile}
         pgexist=0
      fi
#:tests for existence of nested grid
      ngexist=1
      if [ ${mnested} -eq 1 ]
      then
         if [ ! -s ${ncurr} ]
         then
            echo "Error: expected nested grid:${ncurr} not found." | tee -a ${logemailfile}
            ngexist=0
         fi
      fi

#
#:grab and process latitude, longitude, vmax, and pmin from adeck (track) file
#
      centerline=`cat tempadeck.dat | grep "$sdtg" | grep "$smodeluc" | awk -v testtime="$currtime" 'BEGIN { FS="," ; } ($6 == testtime ) { print $7 $8 $9 $10; }'`
      clat=`echo ${centerline} | awk '{ print $1 }'`
      clon=`echo ${centerline} | awk '{ print $2 }'`
      cvmax=`echo ${centerline} | awk '{ print $3 }'`
      cpmin=`echo ${centerline} | awk '{ print $4 }'`
      clatnum=`expr "$clat" : '.*'`
      clonnum=`expr "$clon" : '.*'`
      cvmaxnum=`expr "$cvmax" : '.*'`
      cpminnum=`expr "$cpmin" : '.*'`
#      echo "*${clat}*, ${clatnum}, *${clon}*, ${clonnum}, *${cvmax}*, ${cvmaxnum}, *${cpmin}*, ${cpminnum}"
      if [ ${clatnum} -eq 0 ] || [ ${clonnum} -eq 0 ]
      then
         ilat=${imissn}
         ilon=${imissn}
      else
         clatend=$(( $clatnum - 1 ))
         clonend=$(( $clonnum - 1 ))
         hemns=`echo ${clat} | cut -c${clatnum}`
         ilat=`echo ${clat} | cut -c1-${clatend}`
         hemew=`echo ${clon} | cut -c${clonnum}`
         ilon=`echo ${clon} | cut -c1-${clonend}`
#         echo "*${ilat}*, *${ilon}*, *${hemns}*, *${hemew}*"
         if [ ${ilat} -eq 0 ] || [ ${ilon} -eq 0 ]
         then
            ilat=${imissn}
            ilon=${imissn}
         else
            if [ $hemns == "S" ] && [ ${ilat} -ne 0 ]
            then
               ilat="-${ilat}"
            fi
            if [ $hemew == "W" ] && [ ${ilon} -ne 0 ]
            then
               ilon=$(( 3600 - $ilon ))
            fi
         fi
      fi
      if [ ${cvmaxnum} -eq 0 ] || [ ${cvmax} -eq 0 ]
      then
         ivmax=${imissn}
      else
         ivmax=${cvmax}
      fi
      if [ ${cpminnum} -eq 0 ] || [ ${cpmin} -eq 0 ]
      then
         ipmin=${imissn}
      else
         ipmin=${cpmin}
      fi
#      echo "*${ilat}*, *${ilon}*, *${ivmax}*, *${ipmin}*"
      printf "%6d%6d%6d%6d\n" ${ilat} ${ilon} ${ivmax} ${ipmin} > center.txt
      centerlat=${ilat}
      centerlon=${ilon}
      echo "Track position at hour ${currtime} is: lat ${centerlat} lon ${centerlon}."

#:if center location exists at current time, get parent and nested grids
#: otherwise, skip grids and call null case for parameter file fill-in
      if [ ${centerlat} -eq ${imissn} ] || [ ${centerlon} -eq ${imissn} ]
      then
#:    fill in the missing value array here for current time
         ./inddiagnull.x
         mv params.txt params${fcurr}.txt
         echo params${fcurr}.txt >> ${dtxt}
         echo "Missing track at hour ${currtime}, filling in missing array."
         countmiss=$(( $countmiss + 1 ))
#:if parent grid is missing at current time, fill in the missing value array
      elif [ ${pgexist} -eq 0 ]
      then
         ./inddiagnull.x
         mv params.txt params${fcurr}.txt
         echo params${fcurr}.txt >> ${dtxt}
         echo "Warning: Missing parent grid file at hour ${currtime}, filling in missing array."
         countmiss=$(( $countmiss + 1 ))
#:if expected nested grid is missing at current time, fill in the missing value array
      elif [ ${mnested} -eq 1 ] && [ ${ngexist} -eq 0 ]
      then
         ./inddiagnull.x
         mv params.txt params${fcurr}.txt
         echo params${fcurr}.txt >> ${dtxt}
         echo "Warning: Missing expected nested grid file at hour ${currtime}, filling in missing array."
         countmiss=$(( $countmiss + 1 ))
#
#:get parent grid information (nx, ny, lat, lon, lat/lon intervals)
#
      else
         wgrib2 -grid ${pcurr} 2>/dev/null | head -n 4 > testgrid.tmp
         #get nx and ny
         cnx=`head -n 2 testgrid.tmp | tail -n 1 | awk '{ print $2 ; }'`
         cnxlen=`expr $cnx : '.*'`
         inx=`echo ${cnx} | cut -c7-${cnxlen}`
         cny=`head -n 2 testgrid.tmp | tail -n 1 | awk '{ print $4 ; }'`
         cnylen=`expr $cny : '.*'`
         inylen=`expr $cnylen - 1`
         iny=`echo ${cny} | cut -c1-${inylen}`
#         echo "nx=${inx} ny=${iny}"
         #get input and output lat-lon directions
         inlld=`head -n 2 testgrid.tmp | tail -n 1 | awk '{ print $8 ; }'`
         outlld=`head -n 2 testgrid.tmp | tail -n 1 | awk '{ print $10 ; }'`
         inlond=`echo ${inlld} | cut -c1-2`
         inlatd=`echo ${inlld} | cut -c4-5`
         outlond=`echo ${outlld} | cut -c1-2`
         outlatd=`echo ${outlld} | cut -c4-5`
#         echo "Input lat dir: ${inlatd} ; Output lat dir: ${outlatd}"
#         echo "Input lon dir: ${inlond} ; Output lon dir: ${outlond}"
         #get startlat, endlat, and dlat
         startlat=`head -n 3 testgrid.tmp | tail -n 1 | awk '{ print $2 ; }'`
         endlat=`head -n 3 testgrid.tmp | tail -n 1 | awk '{ print $4 ; }'`
         dlat=`head -n 3 testgrid.tmp | tail -n 1 | awk '{ print $6 ; }'`
#         echo "startlat=${startlat} endlat=${endlat} dlat=${dlat}"
         #get startlon, endlon, and dlon
         startlon=`head -n 4 testgrid.tmp | tail -n 1 | awk '{ print $2 ; }'`
         endlon=`head -n 4 testgrid.tmp | tail -n 1 | awk '{ print $4 ; }'`
         dlon=`head -n 4 testgrid.tmp | tail -n 1 | awk '{ print $6 ; }'`
#         echo "startlon=${startlon} endlon=${endlon} dlon=${dlon}"
         #get numpoints
         numpoints=`head -n 4 testgrid.tmp | tail -n 1 | awk '{ print $7 ; }' | awk 'BEGIN { FS="="} { print $2 ; }'`
#         echo "number of points: ${numpoints}"
         #account for discrepancies in input and output lat-lon directions
         latb=${startlat}
         late=${endlat}
         if [ "${inlatd}" != "${outlatd}" ]
         then
#            echo "Adjusting latitude (if needed) for output field direction: ${inlatd} --> ${outlatd}"
            ilatb=`echo ${latb} | awk 'BEGIN { FS="."} { print $1$2 ; }'`
            ilate=`echo ${late} | awk 'BEGIN { FS="."} { print $1$2 ; }'`
            if [ "${outlatd}" == "SN" ] && [ ${ilatb} -gt ${ilate} ]
            then
               latb=${endlat}
               late=${startlat}
            elif [ "${outlatd}" == "NS" ] && [ ${ilatb} -lt ${ilate} ]
            then
               latb=${endlat}
               late=${startlat}
            fi
         fi
#         echo "new: startlat=${latb} endlat=${late} dlat=${dlat}"
         lonb=${startlon}
         lone=${endlon}
         if [ "${inlond}" != "${outlond}" ]
         then
#            echo "Adjusting longitude (if needed) for output field direction: ${inlond} --> ${outlond}"
            ilonb=`echo ${lonb} | awk 'BEGIN { FS="."} { print $1$2 ; }'`
            ilone=`echo ${lone} | awk 'BEGIN { FS="."} { print $1$2 ; }'`
            #Note:this does not account for wrap-around longitude (340 -> 20)
            if [ "${outlond}" == "WE" ] && [ ${ilonb} -gt ${ilone} ]
            then
               lonb=${endlon}
               lone=${startlon}
            elif [ "${outlond}" == "EW" ] && [ ${ilonb} -lt ${ilone} ]
            then
               lonb=${endlon}
               lone=${startlon}
            fi
         fi
#         echo "new: startlon=${lonb} endlon=${lone} dlon=${dlon}"
         rm testgrid.tmp
         echo "${inx}" > temp_gridp.txt
         echo "${iny}" >> temp_gridp.txt
         echo "${latb}" >> temp_gridp.txt
         echo "${late}" >> temp_gridp.txt
         echo "${dlat}" >> temp_gridp.txt
         echo "${lonb}" >> temp_gridp.txt
         echo "${lone}" >> temp_gridp.txt
         echo "${dlon}" >> temp_gridp.txt
         echo "${numpoints}" >> temp_gridp.txt

         echo "Running diagnostic on ${sname} ${sbasin}${snum}${syr} ${sdtg} for hour ${currtime}."

#
#:get parent grid fields
#
#        T 2m
         outpbin=${fieldT}${fieldsurf}'_p.bin'
         wgrib2 -match "TMP:2 m " -bin ${outpbin} ${pcurr}
         if [ ! -s "$outpbin" ]
         then
            echo "Warning: No field for ${outpbin}, skipping."
            rm ${outpbin}
#           added search for alternate field name for surface temperature
            wgrib2 -match "TMP:surf" -bin ${outpbin} ${pcurr}
            if [ ! -s "$outpbin" ]
            then
               echo "Warning: No field for ${outpbin} alternate name, skipping."
               rm ${outpbin}
            fi
#           end alternate field name search for surface temperature
         fi
#        RH 2m
         outpbin=${fieldR}${fieldsurf}'_p.bin'
         wgrib2 -match "RH:2 m " -bin ${outpbin} ${pcurr}
         if [ ! -s "$outpbin" ]
         then
            echo "Warning: No field for ${outpbin}, skipping."
            rm ${outpbin}
         fi
#        U 10m
         outpbin=${fieldU}${fieldsurf}'_p.bin'
         wgrib2 -match "UGRD:10 m " -bin ${outpbin} ${pcurr}
         if [ ! -s "$outpbin" ]
         then
            echo "Warning: No field for ${outpbin}, skipping."
            rm ${outpbin}
         fi
#        V 10m
         outpbin=${fieldV}${fieldsurf}'_p.bin'
         wgrib2 -match "VGRD:10 m " -bin ${outpbin} ${pcurr}
         if [ ! -s "$outpbin" ]
         then
            echo "Warning: No field for ${outpbin}, skipping."
            rm ${outpbin}
         fi
#        SLP
         outpbin=${fieldP}${fieldsurf}'_p.bin'
         wgrib2 -match "PRMSL" -bin ${outpbin} ${pcurr}
         if [ ! -s "$outpbin" ]
         then
            echo "Warning: No field for ${outpbin}, skipping."
            rm ${outpbin}
#           added search for alternate field name(s) for SLP
            wgrib2 -match "MSL" -bin ${outpbin} ${pcurr}
            if [ ! -s "$outpbin" ]
            then
               echo "Warning: No field for ${outpbin} alternate name, skipping."
               rm ${outpbin}
               wgrib2 -match "mean sea level" -bin ${outpbin} ${pcurr}
               if [ ! -s "$outpbin" ]
               then
                  echo "Warning: No field for ${outpbin} alternate names, skipping."
                  rm ${outpbin}
               fi
            fi
#           end alternate field name search for SLP
         fi

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
#           T
            fieldname=${fieldbegT}${currplvl}${fieldend}
            outpbin=${fieldT}${currplvlt}'_p.bin'
            wgrib2 -match "${fieldname}" -bin ${outpbin} ${pcurr}
            if [ ! -s "$outpbin" ]
            then
               echo "Warning: No field for ${outpbin}, skipping."
               rm ${outpbin}
            fi
#           RH
            fieldname=${fieldbegR}${currplvl}${fieldend}
            outpbin=${fieldR}${currplvlt}'_p.bin'
            wgrib2 -match "${fieldname}" -bin ${outpbin} ${pcurr}
            if [ ! -s "$outpbin" ]
            then
               echo "Warning: No field for ${outpbin}, skipping."
               rm ${outpbin}
            fi
#           Z
            fieldname=${fieldbegZ}${currplvl}${fieldend}
            outpbin=${fieldZ}${currplvlt}'_p.bin'
            wgrib2 -match "${fieldname}" -bin ${outpbin} ${pcurr}
            if [ ! -s "$outpbin" ]
            then
               echo "Warning: No field for ${outpbin}, skipping."
               rm ${outpbin}
            fi
#           U
            fieldname=${fieldbegU}${currplvl}${fieldend}
            outpbin=${fieldU}${currplvlt}'_p.bin'
            wgrib2 -match "${fieldname}" -bin ${outpbin} ${pcurr}
            if [ ! -s "$outpbin" ]
            then
               echo "Warning: No field for ${outpbin}, skipping."
               rm ${outpbin}
            fi
#           V
            fieldname=${fieldbegV}${currplvl}${fieldend}
            outpbin=${fieldV}${currplvlt}'_p.bin'
            wgrib2 -match "${fieldname}" -bin ${outpbin} ${pcurr}
            if [ ! -s "$outpbin" ]
            then
               echo "Warning: No field for ${outpbin}, skipping."
               rm ${outpbin}
            fi
         done

#        TPW
         outpbin=${fieldTPW}'_p.bin'
         wgrib2 -match "PWAT" -bin ${outpbin} ${pcurr}
         if [ ! -s "$outpbin" ]
         then
            echo "Warning: No field for ${outpbin}, skipping."
            rm ${outpbin}
         fi
#        SST
         outpbin=${fieldSST}'_p.bin'
         wgrib2 -match "WTMP:surf" -bin ${outpbin} ${pcurr}
         if [ ! -s "$outpbin" ]
         then
            echo "Warning: No field for ${outpbin}, skipping."
            rm ${outpbin}
#           added search for alternate field name for SST
            wgrib2 -match "TMP:surf" -bin ${outpbin} ${pcurr}
            if [ ! -s "$outpbin" ]
            then
               echo "Warning: No field for ${outpbin} alternate name, skipping."
               rm ${outpbin}
            fi
#           end alternate field name search for SST
         fi
#:list the _p.bin files into outptxt
         ls -1 *_p.bin > ${outptxt}
#:if no parent fields are found make an empty list file
         if [ ! -f "$outptxt" ]
         then
            touch ${outptxt}
         fi

#
#:get nested grid if nested grid is specified
#
         if [ ${mnested} -eq 1 ]
         then
#:get nested grid information (nx, ny, lat, lon, lat/lon intervals)
            wgrib2 -grid ${ncurr} 2>/dev/null | head -n 4 > testgrid.tmp
            #get nx and ny
            cnx=`head -n 2 testgrid.tmp | tail -n 1 | awk '{ print $2 ; }'`
            cnxlen=`expr $cnx : '.*'`
            inx=`echo ${cnx} | cut -c7-${cnxlen}`
            cny=`head -n 2 testgrid.tmp | tail -n 1 | awk '{ print $4 ; }'`
            cnylen=`expr $cny : '.*'`
            inylen=`expr $cnylen - 1`
            iny=`echo ${cny} | cut -c1-${inylen}`
#            echo "nx=${inx} ny=${iny}"
            #get input and output lat-lon directions
            inlld=`head -n 2 testgrid.tmp | tail -n 1 | awk '{ print $8 ; }'`
            outlld=`head -n 2 testgrid.tmp | tail -n 1 | awk '{ print $10 ; }'`
            inlond=`echo ${inlld} | cut -c1-2`
            inlatd=`echo ${inlld} | cut -c4-5`
            outlond=`echo ${outlld} | cut -c1-2`
            outlatd=`echo ${outlld} | cut -c4-5`
#            echo "Input lat dir: ${inlatd} ; Output lat dir: ${outlatd}"
#            echo "Input lon dir: ${inlond} ; Output lon dir: ${outlond}"
            #get startlat, endlat, and dlat
            startlat=`head -n 3 testgrid.tmp | tail -n 1 | awk '{ print $2 ; }'`
            endlat=`head -n 3 testgrid.tmp | tail -n 1 | awk '{ print $4 ; }'`
            dlat=`head -n 3 testgrid.tmp | tail -n 1 | awk '{ print $6 ; }'`
#            echo "startlat=${startlat} endlat=${endlat} dlat=${dlat}"
            #get startlon, endlon, and dlon
            startlon=`head -n 4 testgrid.tmp | tail -n 1 | awk '{ print $2 ; }'`
            endlon=`head -n 4 testgrid.tmp | tail -n 1 | awk '{ print $4 ; }'`
            dlon=`head -n 4 testgrid.tmp | tail -n 1 | awk '{ print $6 ; }'`
#            echo "startlon=${startlon} endlon=${endlon} dlon=${dlon}"
            #get numpoints
            numpoints=`head -n 4 testgrid.tmp | tail -n 1 | awk '{ print $7 ; }' | awk 'BEGIN { FS="="} { print $2 ; }'`
#            echo "number of points: ${numpoints}"
            #account for discrepancies in input and output lat-lon directions
            latb=${startlat}
            late=${endlat}
            if [ "${inlatd}" != "${outlatd}" ]
            then
#               echo "Adjusting latitude (if needed) for output field direction: ${inlatd} --> ${outlatd}"
               ilatb=`echo ${latb} | awk 'BEGIN { FS="."} { print $1$2 ; }'`
               ilate=`echo ${late} | awk 'BEGIN { FS="."} { print $1$2 ; }'`
               if [ "${outlatd}" == "SN" ] && [ ${ilatb} -gt ${ilate} ]
               then
                  latb=${endlat}
                  late=${startlat}
               elif [ "${outlatd}" == "NS" ] && [ ${ilatb} -lt ${ilate} ]
               then
                  latb=${endlat}
                  late=${startlat}
               fi
            fi
#            echo "new: startlat=${latb} endlat=${late} dlat=${dlat}"
            lonb=${startlon}
            lone=${endlon}
            if [ "${inlond}" != "${outlond}" ]
            then
#               echo "Adjusting longitude (if needed) for output field direction: ${inlond} --> ${outlond}"
               ilonb=`echo ${lonb} | awk 'BEGIN { FS="."} { print $1$2 ; }'`
               ilone=`echo ${lone} | awk 'BEGIN { FS="."} { print $1$2 ; }'`
               #Note:this does not account for wrap-around longitude (340->20)
               if [ "${outlond}" == "WE" ] && [ ${ilonb} -gt ${ilone} ]
               then
                  lonb=${endlon}
                  lone=${startlon}
               elif [ "${outlond}" == "EW" ] && [ ${ilonb} -lt ${ilone} ]
               then
                  lonb=${endlon}
                  lone=${startlon}
               fi
            fi
#            echo "new: startlon=${lonb} endlon=${lone} dlon=${dlon}"
            rm testgrid.tmp
            echo "${inx}" > temp_gridn.txt
            echo "${iny}" >> temp_gridn.txt
            echo "${latb}" >> temp_gridn.txt
            echo "${late}" >> temp_gridn.txt
            echo "${dlat}" >> temp_gridn.txt
            echo "${lonb}" >> temp_gridn.txt
            echo "${lone}" >> temp_gridn.txt
            echo "${dlon}" >> temp_gridn.txt
            echo "${numpoints}" >> temp_gridn.txt
#
#:get nested grid fields
#
#           U 10m
            outnbin=${fieldU}${fieldsurf}'_n.bin'
            wgrib2 -match "UGRD:10 m " -bin ${outnbin} ${ncurr}
            if [ ! -s "$outnbin" ]
            then
               echo "Warning: No field for ${outnbin}, skipping."
               rm ${outnbin}
            fi
#           V 10m
            outnbin=${fieldV}${fieldsurf}'_n.bin'
            wgrib2 -match "VGRD:10 m " -bin ${outnbin} ${ncurr}
            if [ ! -s "$outnbin" ]
            then
               echo "Warning: No field for ${outnbin}, skipping."
               rm ${outnbin}
            fi
#           SLP
            outnbin=${fieldP}${fieldsurf}'_n.bin'
            wgrib2 -match "PRMSL" -bin ${outnbin} ${ncurr}
            if [ ! -s "$outnbin" ]
            then
               echo "Warning: No field for ${outnbin}, skipping."
               rm ${outnbin}
#              added search for alternate field name(s) for SLP
               wgrib2 -match "MSL" -bin ${outnbin} ${ncurr}
               if [ ! -s "$outnbin" ]
               then
                  echo "Warning: No field for ${outnbin} alternate name, skipping."
                  rm ${outnbin}
                  wgrib2 -match "mean sea level" -bin ${outnbin} ${ncurr}
                  if [ ! -s "$outnbin" ]
                  then
                     echo "Warning: No field for ${outnbin} alternate names, skipping."
                     rm ${outnbin}
                  fi
               fi
#              end alternate field name search for SLP
            fi
#           SST
            outnbin=${fieldSST}'_n.bin'
            wgrib2 -match "WTMP:surf" -bin ${outnbin} ${ncurr}
            if [ ! -s "$outnbin" ]
            then
               echo "Warning: No field for ${outnbin}, skipping."
               rm ${outnbin}
#              added search for alternate field name for SST
               wgrib2 -match "TMP:surf" -bin ${outnbin} ${ncurr}
               if [ ! -s "$outnbin" ]
               then
                  echo "Warning: No field for ${outnbin} alternate name, skipping."
                  rm ${outnbin}
               fi
#              end alternate field name search for SST
            fi
#:list the _n.bin files into outntxt
            ls -1 *_n.bin > ${outntxt}
#:if no nested fields are found make an empty list file
            if [ ! -f "$outntxt" ]
            then
               touch ${outntxt}
            fi
         fi

#:setup file to specify radii output for comment section
         if [ $currtime -eq 0 ]
         then
            echo "1" > printradiiflag.txt
         else
            echo "0" > printradiiflag.txt
         fi

#:run diagnostic parameter calculation for current time
         ./inddiag.x
         mv params.txt params${fcurr}.txt
         echo params${fcurr}.txt >> ${dtxt}

#:remove binary files before starting next time
         rm *.bin
         rm ${outptxt}
         if [ ${mnested} -eq 1 ]
         then
            rm ${outntxt}
         fi

      fi   #finish if statement for reading and calculating parameters

#:calculate next forecast time
      currtime=$(( $currtime + $tint ))
   done   #finish loop for each individual time

#:check for existence of radii file before including in diag file
   if [ -s lsdiagradii.txt ]
   then
      echo "1" > printradiiflag.txt
   else
      echo "0" > printradiiflag.txt
   fi

#:run diagnostic file output from accumulation of individual times
   if [ ${countmiss} -lt ${ntimes} ]
   then
      ./totaldiag.x
      mv diag.txt ${outputdir}${sfiout}
      #:note completion for specified initial file
      echo "Processing complete for ${initfile}" | tee -a ${logemailfile}
      echo "Diagnostic file stored in ${outputdir}${sfiout}" | tee -a ${logemailfile}
      countdiag=$(( $countdiag + 1 ))
   else
      echo "Error: Diagnostic file ${sfiout} filled with missing values, skipping." | tee -a ${logemailfile}
   fi

#:remove temporary files
   rm temp*
   rm lsdiagradii.txt
   rm printradiiflag.txt
#:remove temporary parameter files (individual times)
   rm center*
   rm params*
   rm diaginfo.txt

done   #finish loop for each specified initial file

#:note the complete number of files expected and produced
#: -these numbers can differ without an error, one example is it could
#:  indicate a case was specified multiple times in the input.list file
echo "Total number of initial files specified: ${countinput}." | tee -a ${logemailfile}
echo "Total number of diagnostic files produced: ${countdiag}." | tee -a ${logemailfile}

###############################################################################
#Send email log file if flag enabled
###############################################################################
if [ $logemailflag -eq 1 ]
then
   echo "Sending email."
   date >> ${logemailfile}
   grep "^Error:" ${logemailfile} > emailerror.tmp
   if [ -s emailerror.tmp ]
   then
      logemailsubject="create_diagfiles errors found"
   else
      logemailsubject="create_diagfiles successful completion"
   fi
   rm emailerror.tmp
   cat ${logemailfile} | mail -s "${logemailsubject}" ${logemail}
fi
rm ${logemailfile}

date

exit 0
