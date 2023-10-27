      subroutine ofiles(iunittca,iunittcc,iunittcf,iunittco,iunittcd,iunittcp,
     $     ni,nj,tcapath,tccpath,tcfpath,tcopath,tcdpath,tcppath)
      character tcapath*128,tccpath*128,tcfpath*128,
     $     tcopath*128,tcdpath*128,tcppath*128

      include 'params.h'

Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
C         input with model track (adeck format)
Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

      open(iunittca,file=tcapath(1:ichlen(tcapath,128)),
     $     status='old',err=810)

Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
C         input with TC structure data (from jtwc warning in adeck)
Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

      open(iunittcc,file=tccpath(1:ichlen(tccpath,128)),
     $     status='old',err=812)

Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
C         input global fields (sfc wind)
Ciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii

      open(iunittcf,file=tcfpath(1:ichlen(tcfpath,128)),
     $     status='old',err=814,
CCCCC - sgi     $     recl=ni*nj,access='direct')
CCCCC - sun     $     recl=ni*nj*4,access='direct')
CCCCC - linux     $     recl=ni*nj*4,access='direct')
     $     recl=ni*nj*4,access='direct')

Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C         output tc structure obs
Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

      open(iunittco,file=tcopath(1:ichlen(tcopath,128)),
     $     form='unformatted',status='unknown',err=816)

Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C         output tc structure diag
Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

      open(iunittcd,file=tcdpath(1:ichlen(tcdpath,128)),
     $     status='unknown',err=818)

Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
C         output tc structure radial profiles
Coooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

      open(iunittcp,file=tcppath(1:ichlen(tcppath,128)),
     $     form='unformatted',status='unknown',err=820)

      if(verb) then
        print*, 'OOO    (adeck): ',tcapath(1:ichlen(tcapath,128))
        print*, 'OOO     (carq): ',tccpath(1:ichlen(tccpath,128))
        print*, 'OOO    (field): ',tcfpath(1:ichlen(tcfpath,128))
        print*, 'OOO      (obs): ',tcopath(1:ichlen(tcopath,128))
        print*, 'OOO     (diag): ',tcdpath(1:ichlen(tcdpath,128))
        print*, 'OOO  (profile): ',tcppath(1:ichlen(tcppath,128))
      endif


      return

 810  continue
      print*,'error opening input model adeck  file: '
      print*,tcapath
      stop 810

 812  continue
      print*,'error opening input posit file: '
      print*,tcspath
      stop 812

 814  continue
      print*,'error opening input field file'
      print*,tcfpath
      stop 814

 816  continue
      print*,'error opening output obs file'
      print*,tcopath
      stop 816

 818  continue
      print*,'error opening output diag file'
      print*,tcdpath
      stop 818

 820  continue
      print*,'error opening output radial profile file'
      print*,tcppath
      stop 820

      return
      end
