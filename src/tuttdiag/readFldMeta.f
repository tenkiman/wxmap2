      subroutine readFldMeta(tcmetapath,ierr)

      use const
      use trkParams
      use f77outputmeta

      real*4 clat,clon,cbearing

      integer*4 ios,pos,i,j,k,l,n,m,nlevs

      character*128 tcmetapath

      character(len=512) :: buffer
      logical verb

      verb=.true.
      verb=.false.

      open( unit=1, file=tcmetapath(1:ichlen(tcmetapath,128)), form='formatted',action='read',err=812)

      ios=0

      do while ( ios == 0 )

 5      continue
        read( 1, '(a)', iostat=ios ) buffer

        print*,'buffer: ',buffer(1:128)
 
        if ( ios == 0 ) then

          pos = index(buffer, 'ni:')
          if ( pos .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+3),'(I3)') ni
            if(verb) print*,'ni---------------------- ',pos,ni
              allocate(xgrd(ni),STAT=istat)
          end if

          pos = index(buffer, 'nj:')
          if ( index(buffer, 'nj:') .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+3),'(I10)') nj
            if(verb) print*,'nj---------------------- ',pos,nj
            allocate(ygrd(nj),STAT=istat)
            allocate(coslatI(nj),STAT=istat)
            goto 5
          end if

          pos = index(buffer, "lonW:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+3),'(f6.2)') elon
            if(verb) print*,'elon---------------------- ',pos,elon
          end if


          pos = index(buffer, "lonE:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+3),'(f6.2)') elon
            if(verb) print*,'elon---------------------- ',pos,elon
            goto 5
          end if

          pos = index(buffer, "latS:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f5.2)') blat
            if(verb) print*,'blat---------------------- ',pos,blat
          end if

          pos = index(buffer, "latN:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f5.2)') elat
            if(verb) print*,'elat---------------------- ',pos,elat
            goto 5
          end if

          pos = index(buffer, "dlon:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f5.2)') dlon
            if(verb) print*,'dlon---------------------- ',pos,dlon
          end if

          pos = index(buffer, "dlat:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f5.2)') dlat
            if(verb) print*,'dlat---------------------- ',pos,dlat
            goto 5
          end if

          pos = index(buffer, 'nk:')
          if ( pos .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+3),'(I10)') nk
            if(verb) print*,'nk---------------------- ',pos,nk

            if(nk > 0) then
              nlevs=nk
              allocate(iplevs(nlevs),STAT=istat)
              allocate(plevs(nlevs),STAT=istat)
              do i=1,nlevs
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:7),'(f7.2)') plevs(i)
                iplevs(i)=nint(plevs(i))
                if(verb) print*,'plevs---------------------- ',iplevs(i),plevs(i)
              enddo
            endif
            goto 5
          endif

          pos = index(buffer, 'nt:')
          if ( pos .ne. 0 ) then
            pos=pos+4
            read(buffer(pos:pos+3),'(I4)') nt
            if(verb) print*,'nt---------------------- ',pos,nt

            if(nt > 0) then
              allocate(itaus(nt),STAT=istat)
              allocate(DataPaths(nt),STAT=istat)
              do i=1,nt
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:3),'(i3,1x,a128)') itaus(i)
                read(buffer(5:128+5),'(a)') DataPaths(i)
                if(verb) print*,'itaus---------------------- ',itaus(i),DataPaths(i)
              enddo

c--       set vars in trkParams from input, taus, and the gdat array
c
              
              dtau=6
              maxhour=itaus(nt)
              if(nt > 1) dtau=itaus(2)-itaus(1)
              maxhr=((maxhour/dtau)+1)
              allocate(gdat(numvar,0:maxhr,maxtc,0:maxfix),stat=istat)
              if(istat.gt.0) go to 814

            endif
            goto 5
          endif

          pos = index(buffer, 'ntf:')
          if ( pos .ne. 0 ) then
            pos=pos+5
            read(buffer(pos:pos+3),'(I4)') ntf
            if(verb) print*,'ntf--------------------- ',pos,ntf

            if(nt > 0) then
              allocate(itaus(nt),STAT=istat)
              do i=1,nt
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:3),'(i3)') itaus(i)
                if(verb) print*,'itaus---------------------- ',itaus(i)
              enddo
            endif
            goto 5
          endif

          pos = index(buffer, 'nvarsSfc:')
          if ( pos .ne. 0 ) then
            pos=pos+9
            read(buffer(pos:pos+3),'(I10)') nvarsfc
            if(verb) print*,'nvarssfc---------------------- ',pos,nvarsfc

            pos = index(buffer, 'nvarsUA:')
            print*, buffer
            if ( pos .ne. 0 ) then
              pos=pos+9
              read(buffer(pos:pos+3),'(I10)') nvarua
              if(verb) print*,'nvarua ---------------------- ',pos,nvarua
            endif

c--       parse out the sfc and ua variable names
c
            if(nvarsfc > 0) then
              allocate(varsfc(nvarsfc),STAT=istat)
              do i=1,nvarsfc
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:10),'(a)') varsfc(i)
                if(verb) print*,'varsfc---------------------- ',varsfc(i)
              enddo
            endif

            if(nvarua > 0) then
              allocate(varua(nvarua),STAT=istat)
              do i=1,nvarua
                read( 1, '(a)', iostat=ios ) buffer
                read(buffer(1:10),'(a)') varua(i)
                if(verb) print*,'varua---------------------- ',varua(i)
              enddo
            endif

            goto 5

          end if

          pos = index(buffer, "lonC:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f6.2)') clon
            if(verb) print*,'clon---------------------- ',pos,clon
          end if

          pos = index(buffer, "latC:")
          if ( pos .ne. 0 ) then
            pos=pos+6
            read(buffer(pos:pos+6),'(f6.2)') clat
            if(verb) print*,'clat---------------------- ',pos,clat
          end if

          pos = index(buffer, "bearingC:")
          if ( pos .ne. 0 ) then
            pos=pos+10
            read(buffer(pos:pos+6),'(f6.2)') cbearing
            if(verb) print*,'cbearing---------------------- ',pos,cbearing
            goto 5
          end if

        end if

      end do


C         
C..       define the grid; now from input
C
      do i=1,ni
        xgrd(i)=blon+dlon*(i-1)
      end do
      
      do j=1,nj
        ygrd(j)=blat+dlat*(j-1)
        clat=cos(ygrd(j)*dtr)
        coslatI(j)=1.0
        if(clat.ge.0.001) coslatI(j)=1.0/clat
      end do
      

      return

 812  continue

      print*,'error opening input field file'
      print*,tcmetapath
      stop 812

 814  continue
      print*,'error in allocate...readFldMeta'
      stop 814


      end subroutine readFldMeta

