      program tcdiagdriver
          implicit none
          integer*4 :: ios,pos,i,j,k,
     +                 ni,nj,nk,vars,
     +                 nargs
          real*4 :: slat,slon,
     +              elat,elon,
     +              clat,clon,
     +              dlat,dlon,
     +              undef

          real*4, allocatable :: xylat(:), xylon(:),
     +                           u(:,:,:), v(:,:,:),p(:,:,:)

          character(len=512) :: metafile,datafile,buffer,label,outfile

          nk = 1
          ios = 0
          undef = -1e20
          nargs = iargc()

          if ( nargs .ne. 3 ) then
              write(*,*) "You need the metadata, data"
              write(*,*) "and output files as cmdline args."
              stop
          else
              call getarg( 1, metafile )
              call getarg( 2, datafile )
              call getarg( 3, outfile  )
          end if

          open( unit=1, file=metafile, form='formatted',action='read')

          do while ( ios == 0 )
5             read( 1, '(a)', iostat=ios ) buffer
              if ( ios == 0 ) then
                  pos = index(buffer, 'ni:')
                  if ( pos .ne. 0 ) then
                      read(buffer(pos+4:pos+6),'(I10)') ni
                  end if
                  pos = index(buffer, 'nj:')
                  if ( index(buffer, 'nj:') .ne. 0 ) then
                      read(buffer(pos+4:pos+6),'(I10)') nj
                      goto 5
                  end if
                  !pos = index(buffer, 'nk:')
                  !if ( pos .ne. 0 ) then
                  !    read(buffer(pos+4:pos+6),'(I10)') nk
                  !end if
                  pos = index(buffer, "lonW:")
                  if ( pos .ne. 0 ) then
                      read(buffer(pos+6:pos+12),'(f6.2)') slon
                  end if
                  pos = index(buffer, "lonE:")
                  if ( pos .ne. 0 ) then
                      read(buffer(pos+6:pos+12),'(f6.2)') elon
                      goto 5
                  end if
                  pos = index(buffer, "latS:")
                  if ( pos .ne. 0 ) then
                      read(buffer(pos+6:pos+12),'(f5.2)') slat
                  end if
                  pos = index(buffer, "latN:")
                  if ( pos .ne. 0 ) then
                      read(buffer(pos+6:pos+12),'(f5.2)') elat
                      goto 5
                  end if
                  pos = index(buffer, "dlon:")
                  if ( pos .ne. 0 ) then
                      read(buffer(pos+6:pos+12),'(f5.2)') dlon
                  end if
                  pos = index(buffer, "dlat:")
                  if ( pos .ne. 0 ) then
                      read(buffer(pos+6:pos+12),'(f5.2)') dlat
                      goto 5
                  end if
                  pos = index(buffer, "nvarsSfc:")
                  if ( pos .ne. 0 ) then
                      read(buffer(pos+11:pos+13),'(i10)') vars
                      goto 5
                  end if

              end if
          end do

          allocate(xylon(ni))
          allocate(xylat(nj))
          allocate(u(ni,nj,nk))
          allocate(v(ni,nj,nk))
          allocate(p(ni,nj,nk))

          clon = (slon+elon) / 2.0
          clat = (slat+elat) / 2.0

          do i = 1, ni, 1
              xylon(i) = slon + (i-1) * dlon
          end do
          do j = 1, nj, 1
              xylat(j) = slat + (j-1) * dlat
          end do

          open( unit = 2, file=datafile, form='unformatted',
     +         access='sequential', action='read', status='old')
          read(2) u
          read(2) v
          if ( vars .eq. 3 ) then 
              read(2) p
          else 
              p = undef
          end if
          call tcdiag(ni,nj,nk,u,v,p,xylon,xylat,clat,clon,undef,
     +                outfile)

      end program tcdiagdriver

