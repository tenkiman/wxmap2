      program s2g
C         
C         convert single level observations to GrADS format
C         
C         recipe to run this sample program:
C         
C*******
C*******  set the icray flag in the parameter statement (icray=1 for cray)
C*******  if NOT a cray then comment out the call assign line
C*******
C         cray:
C
C         cf77 s2g.f -o s2g
C         s2g
C         stnmap -i s.ctl
C         grads -lc "open s.ctl"
C         
C         Files:
C         
C         s.txt    ASCII source data: s.txt
C         
C         cray:
C
C         s.cray.obs    GrADS CRAY binary format (unblocked) 
C         s.cray.smp    station map file (32 bytes on cray 32 bytes machine indenpendent)
C         s.cray.ctl    GrADS data descriptor file
C         
      character id*8
      character clev*3,cyy*2,cmm*2,cdd*2,chh*2
      character card*80
      open(10,file='s.txt',status='old',err=800)

      read(10,'(1x,a3,1x,i2,1x,i2,1x,i2,1x,i2,1x,i4)') 
     $     clev,iyy,imm,idd,ihh,nobs

      write(cyy,'(i02)') iyy
      write(cmm,'(i02)') imm
      write(cdd,'(i02)') idd
      write(chh,'(i02)') ihh

      if(cyy(1:1).eq.' ') cyy(1:1)='0'
      if(cmm(1:1).eq.' ') cmm(1:1)='0'
      if(cdd(1:1).eq.' ') cdd(1:1)='0'
      if(chh(1:1).eq.' ') chh(1:1)='0'


C         
C         for cray, this assign produces pure station data WITHOUT blocks
C         as in unix unformatted writes
C
      card='assign -s unblocked -a s.cray.obs fort.12'
      call assign(card)

      rt=0.0
      nlev=1
      iflag=1
      do i=1,nobs
        read(10,'(4i5)') ilat,ilon,iu,iv
        rlat=ilat*0.1
        rlon=ilon*0.1
        u=iu*0.1
        v=iv*0.1
        write(id,'(i7,a1)') i,'\0'
        print*,i,rlat,rlon,u,v,id
        write(12) id,rlat,rlon,rt,nlev,iflag
        write(12) u,v
      end do
C         
C         write out end of time record
C         
      write(id,'(i7,a1)') -999,'\0'
      rlon=0.0
      rlat=0.0
      rt=0.0
      nlev=0
      write(12) id,rlat,rlon,rt,nlev,iflag
C         
C         all done

      go to 999
 800  continue
      print*,'unable to open tmp.asc'
 999  continue
      close(12)
      close(10)
      stop
      end

