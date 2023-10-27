c
      subroutine getmq(ufil,vfil,imx,jmx,iumq)
      parameter(igrid=201,jgrid=81,i50min=0,i50mxgrd=201,
     *          j50min=0,j50mxgrd=81,mxitr=4)

      dimension ufil(imx,jmx)
      dimension vfil(imx,jmx)
      real*4 zmatcrse(igrid,jgrid)
      real*4 zmatfine(i50min:i50mxgrd,j50min:j50mxgrd,mxitr)
      real*4 analysis(i50min:i50mxgrd,j50min:j50mxgrd,mxitr)
      real*4 rgrid(i50min:i50mxgrd,j50min:j50mxgrd,mxitr)
         read (iumq,100) zmatcrse, zmatfine, analysis, rgrid, kmxitr,
     1                ki50min, ki50mxgrd, kj50min, kj50mxgrd,
     2                ildumy, jldumy, iudumy, judumy,
     3                cint, xdatsav, xpt, ypt, nobstot, fndflg,
     4                isym, kmxobs, kitype, ipnt, icnt, iter,
     5                sublata,sublonb,sublatc,sublond,ilvl,
     6                ipar, glatinc, gloninc
 100  format(20a4)
            do i = 1,imx
               do j = 1,jmx
                  ufil(i,j) = analysis(i,j,2)
                  vfil(i,j) = analysis(i,j,3)
               end do
            end do
              call findmx2(ufil,rmax,rmin,imx,jmx,maxi,maxj,mini,minj)
               print *,'max u mq = ',rmax,' at ',maxi,maxj
               print *,'min u mq = ',rmin,' at ',mini,minj
              call findmx2(vfil,rmax,rmin,imx,jmx,maxi,maxj,mini,minj)
               print *,'max v mq = ',rmax,' at ',maxi,maxj
               print *,'min v mq = ',rmin,' at ',mini,minj
       return
       end
