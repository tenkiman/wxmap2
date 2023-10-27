      subroutine getfg (ufil,vfil, iu, zmattemp,
     2                  level, param4,
     5                  igrid, jgrid, imin, imx, jmin, jmx,
     6                  mxtim,mxprm,mxlvl,
     7                  mxdimx, mxdimy, iftime, ilevel, iparam)
c
c use file (09) for the 06/18z 50 km gridded first guess.  the 00/12z
c nogaps fields [2.5 deg resolution] are read from file (10)
c
      real*4 ufil(imx,jmx),vfil(imx,jmx)
      real*4 zmattemp(imin:imx,jmin:jmx)
c
      integer found, fgzflg
c
      character*4 param4(mxprm), lll
      character*7 level(mxlvl), curlvl,ll
      character*80 htitle1, htitle2, title
c
      icnt = 0
      found = 0
      print *,'nx0,ny0 = ',nx0,ny0,' imx,jmx = ',imx,jmx
1     do while (found .eq. 0)
             call readit(iu,zmattemp,igrid,jgrid,htitle1,
     *       imin,imx,jmin,jmx)
         print *,'ilevel,level = ',ilevel,level(ilevel)
         print *,'iparam,param4 = ',iparam,param4(iparam)
c
c show the progress of the search at each new level...
c
            write (6,1080) htitle1(1:20)
1080     format (1x,'***processing ',a20,'***')
c
c now see if the header info matches the desired record...
c
         ll = level(ilevel)
         lll = ll(1:4)
         if( lll .eq. htitle1(7:10) .and.
     2       param4(iparam) .eq. htitle1(1:4)) then
            found = 1
            icnt = icnt+1
            title = htitle1
               print *, 'processing 50km first guess '
               print *,'imin,max = ',imin,imax,' jmin,max = ',jmin,jmax
               print *,title
               do i = imin, imx
                  do j = jmin, jmx
                     if(icnt .eq. 1) ufil(i,j) = zmattemp(i,j)
                     if(icnt .eq. 2) vfil(i,j) = zmattemp(i,j)
                  end do
               end do
              print *,'set rgrid0, icnt = ',icnt,i,j
              if( icnt .eq. 1 ) then
              call findmx2(ufil,rmax,rmin,imx,jmx,maxi,maxj,mini,minj)
              else
              call findmx2(vfil,rmax,rmin,imx,jmx,maxi,maxj,mini,minj)
              endif
               print *,'max fg = ',rmax,' at ',maxi,maxj
               print *,'min fg = ',rmin,' at ',mini,minj
               print *, 'calculate coefficients for 50km first ',
     1                  'guess...'
               ldf0 = nx0
            end if
      end do
c
c  if read u, then go back and get v
c
      if( icnt .eq. 1 ) then
         found = 0
         iparam = iparam + 1
         go to 1
      endif
c
999   return
      end
