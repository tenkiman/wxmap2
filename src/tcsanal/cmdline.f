      subroutine cmdline(nlpath,copt)

      character nlpath*128,tcapath*128,tccpath*128,tcfpath*128,tcopath*128,
     $     tcdpath*128,tcppath*128

      character copt*2

Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
C         
C         command line processing
C
Ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      
C         call getarg(1,tcapath)
C         call getarg(2,tccpath)
C         call getarg(3,tcfpath)
C         call getarg(4,tcopath)
C         call getarg(5,tcdpath)
C         call getarg(6,tcppath)

      call getarg(1,nlpath)
      call getarg(2,copt) 
      spdcrit=15.0
      vcrit=7.5

      narg=iargc()
      
      if(narg.lt.1) then

        print*,'Arguments to tcsanal.x:'
        print*,' '
        print*,'     nlpath : path to namelist with params / paths'
C        print*,'   tcapath : path to input model adeck track forecast file'
C        print*,'   tccpath : path to input CARQ posit, structure file'
C        print*,'   tcfpath : path to input model field data file (sfc, 850 wind)'
C        print*,'   tcopath : path to output obs file'
C        print*,'   tcdpath : path to output diag file'
C        print*,'   tcppath : path to output radial profile file'
        print*,'    [copt] : optional character option:'
        print*,'             -v verbose'
        print*,' '
        print*,'Example'
        print*,' '
        print*,'tcsanal.x tcsanal.namelist.txt'
        print*,' '
        stop 

      endif

      return
      end
