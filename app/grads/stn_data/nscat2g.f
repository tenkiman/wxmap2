      program nscat2g
C         
C         convert NSCAT sfc wind observations to GrADS format
C         
C         unix:
C
C         f77 s2g.f -o s2g
C         s2g
C         stnmap -i s.seq.ctl
C         grads -lc "open s.seq.ctl"
C         
C         Files:
C         
C         nscat.txt    ASCII source data: nscat.txt
C         
C         unix:
C
C         nscat.seq.be.obs    GrADS binary format (sequential big endian) 
C         nscat.seq.be.smp    station map file (16 bytes on 32-bit machines 32 bytes machine independent)
C         nscat.seq.be.ctl    GrADS data descriptor file
C
C         nscat.seq.be.multi_times.obs    GrADS binary format (sequential) 
C         nscat.seq.be.multi_times.smp    station map file (16 bytes on 32-bit machines
C         nscat.seq.be.multi_times.ctl    GrADS data descriptor file
C
      character id*8,id0*8
      character clev*3,cyy*2,cmm*2,cdd*2,chh*2
      character card*80

      integer rc

      logical mtimes

      mtimes=.true.
      mtimes=.false.

      id0(1:7)="endtime"
      rlat0=0.0
      rlon0=0.0
      rt0=0.0
      nlev0=0
      iflag0=0

C         
C         open the input ASCII data file
C
      open(10,file='nscat.txt',status='old',err=800)
C         
C         open the output file
C         
      if(mtimes) then
        open(12,file='nscat.seq.be.multi_times.obs',
     $       form='unformatted',status='unknown')
      else
        open(12,file='nscat.seq.be.obs',
     $       form='unformatted',status='unknown')
      endif

C         
C         position to the first record
C

      read(10,'(a)',end=802) card
      do while(card(1:6).ne.'Rec = ')
        read(10,'(a)',end=802) card
      end do

      ijunk=1
      icnt=0
      do while(ijunk.eq.1) 

        icnt=icnt+1
        call rec_proc(rc)
        print*,'xxxxxxxx rec ',icnt
        if(mtimes) write(12) id0,rlat0,rlon0,rt0,nlev0,iflag0
        if(rc.eq.-2) go to 999
      end do

C         
C         all done
C         

      go to 999
C         
C         error conditions
C
 800  continue
      print*,'unable to open tmp.asc'
      stop '800'

 802  continue
      print*,'premature end of data'
      stop '800'

 999  continue

C         
C         write out end of time record
C         
      write(12) id0,rlat0,rlon0,rt0,nlev0,iflag0

      close(12)
      close(10)
      stop
      end

      subroutine rec_proc(rc)
      character card*80,id*8
      integer rc

      d2r=3.141592654/180.0

      rc=0
      do while(rc.ge.0) 
        read(10,'(a)',err=802,end=802) card

        if(card(1:8).eq.'Processi') then
          rc=-2
          return
        else if(card(1:6).eq.'Rec = ') then
          rc=-1
          return
        else
          if(card(37:39).ne.'Lat') then
            rc=rc+1
            write(*,'(a,i3,a)') 'rc = ',rc,card
            read(card,'(34x,f7.2,3x,f7.2,3x,f6.2,2x,f6.2)') 
     $           rlat,rlon,rspd,rdir
C         
C         convert winds to u,v
C
            ff=90.0-rdir
            u=-rspd*cos(ff*d2r)
            v=-rspd*sin(ff*d2r)

            write(id,'(i7,a1)') rc,'\0'

            write(*,
     $           '(f7.2,1x,f7.2,1x,f6.2,1x,f6.2,1x,f6.2,1x,f6.2,1x,a)') 
     $           rlon,rlat,rspd,rdir,u,v,id

            rt=0.0
            nlev=1
            iflag=1
            write(12) id,rlat,rlon,rt,nlev,iflag
            write(12) u,v

          endif

        endif

      end do

      return
 802  continue
      rc=0
      return
      end



