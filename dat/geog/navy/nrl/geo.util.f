      subroutine radf2 (ido,l1,cc,ch,wa1)
      dimension       ch(ido,2,l1)           ,cc(ido,l1,2)           ,
     1                wa1(1)
      do 101 k=1,l1
         ch(1,1,k) = cc(1,k,1)+cc(1,k,2)
         ch(ido,2,k) = cc(1,k,1)-cc(1,k,2)
  101 continue
      if (ido-2) 107,105,102
  102 idp2 = ido+2
      do 104 k=1,l1
         do 103 i=3,ido,2
            ic = idp2-i
            tr2 = wa1(i-2)*cc(i-1,k,2)+wa1(i-1)*cc(i,k,2)
            ti2 = wa1(i-2)*cc(i,k,2)-wa1(i-1)*cc(i-1,k,2)
            ch(i,1,k) = cc(i,k,1)+ti2
            ch(ic,2,k) = ti2-cc(i,k,1)
            ch(i-1,1,k) = cc(i-1,k,1)+tr2
            ch(ic-1,2,k) = cc(i-1,k,1)-tr2
  103    continue
  104 continue
      if (mod(ido,2) .eq. 1) return
  105 do 106 k=1,l1
         ch(1,2,k) = -cc(ido,k,2)
         ch(ido,1,k) = cc(ido,k,1)
  106 continue
  107 return
      end
      subroutine radf3 (ido,l1,cc,ch,wa1,wa2)
      dimension       ch(ido,3,l1)           ,cc(ido,l1,3)           ,
     1                wa1(1)     ,wa2(1)
      data taur,taui /-.5,.866025403784439/
      do 101 k=1,l1
         cr2 = cc(1,k,2)+cc(1,k,3)
         ch(1,1,k) = cc(1,k,1)+cr2
         ch(1,3,k) = taui*(cc(1,k,3)-cc(1,k,2))
         ch(ido,2,k) = cc(1,k,1)+taur*cr2
  101 continue
      if (ido .eq. 1) return
      idp2 = ido+2
      do 103 k=1,l1
         do 102 i=3,ido,2
            ic = idp2-i
            dr2 = wa1(i-2)*cc(i-1,k,2)+wa1(i-1)*cc(i,k,2)
            di2 = wa1(i-2)*cc(i,k,2)-wa1(i-1)*cc(i-1,k,2)
            dr3 = wa2(i-2)*cc(i-1,k,3)+wa2(i-1)*cc(i,k,3)
            di3 = wa2(i-2)*cc(i,k,3)-wa2(i-1)*cc(i-1,k,3)
            cr2 = dr2+dr3
            ci2 = di2+di3
            ch(i-1,1,k) = cc(i-1,k,1)+cr2
            ch(i,1,k) = cc(i,k,1)+ci2
            tr2 = cc(i-1,k,1)+taur*cr2
            ti2 = cc(i,k,1)+taur*ci2
            tr3 = taui*(di2-di3)
            ti3 = taui*(dr3-dr2)
            ch(i-1,3,k) = tr2+tr3
            ch(ic-1,2,k) = tr2-tr3
            ch(i,3,k) = ti2+ti3
            ch(ic,2,k) = ti3-ti2
  102    continue
  103 continue
      return
      end
      subroutine radf4 (ido,l1,cc,ch,wa1,wa2,wa3)
      dimension       cc(ido,l1,4)           ,ch(ido,4,l1)           ,
     1                wa1(1)     ,wa2(1)     ,wa3(1)
      data hsqt2 /.7071067811865475/
      do 101 k=1,l1
         tr1 = cc(1,k,2)+cc(1,k,4)
         tr2 = cc(1,k,1)+cc(1,k,3)
         ch(1,1,k) = tr1+tr2
         ch(ido,4,k) = tr2-tr1
         ch(ido,2,k) = cc(1,k,1)-cc(1,k,3)
         ch(1,3,k) = cc(1,k,4)-cc(1,k,2)
  101 continue
      if (ido-2) 107,105,102
  102 idp2 = ido+2
      do 104 k=1,l1
         do 103 i=3,ido,2
            ic = idp2-i
            cr2 = wa1(i-2)*cc(i-1,k,2)+wa1(i-1)*cc(i,k,2)
            ci2 = wa1(i-2)*cc(i,k,2)-wa1(i-1)*cc(i-1,k,2)
            cr3 = wa2(i-2)*cc(i-1,k,3)+wa2(i-1)*cc(i,k,3)
            ci3 = wa2(i-2)*cc(i,k,3)-wa2(i-1)*cc(i-1,k,3)
            cr4 = wa3(i-2)*cc(i-1,k,4)+wa3(i-1)*cc(i,k,4)
            ci4 = wa3(i-2)*cc(i,k,4)-wa3(i-1)*cc(i-1,k,4)
            tr1 = cr2+cr4
            tr4 = cr4-cr2
            ti1 = ci2+ci4
            ti4 = ci2-ci4
            ti2 = cc(i,k,1)+ci3
            ti3 = cc(i,k,1)-ci3
            tr2 = cc(i-1,k,1)+cr3
            tr3 = cc(i-1,k,1)-cr3
            ch(i-1,1,k) = tr1+tr2
            ch(ic-1,4,k) = tr2-tr1
            ch(i,1,k) = ti1+ti2
            ch(ic,4,k) = ti1-ti2
            ch(i-1,3,k) = ti4+tr3
            ch(ic-1,2,k) = tr3-ti4
            ch(i,3,k) = tr4+ti3
            ch(ic,2,k) = tr4-ti3
  103    continue
  104 continue
      if (mod(ido,2) .eq. 1) return
  105 continue
      do 106 k=1,l1
         ti1 = -hsqt2*(cc(ido,k,2)+cc(ido,k,4))
         tr1 = hsqt2*(cc(ido,k,2)-cc(ido,k,4))
         ch(ido,1,k) = tr1+cc(ido,k,1)
         ch(ido,3,k) = cc(ido,k,1)-tr1
         ch(1,2,k) = ti1-cc(ido,k,3)
         ch(1,4,k) = ti1+cc(ido,k,3)
  106 continue
  107 return
      end
      subroutine radf5 (ido,l1,cc,ch,wa1,wa2,wa3,wa4)
      dimension       cc(ido,l1,5)           ,ch(ido,5,l1)           ,
     1                wa1(1)     ,wa2(1)     ,wa3(1)     ,wa4(1)
      data tr11,ti11,tr12,ti12 /.309016994374947,.951056516295154,
     1-.809016994374947,.587785252292473/
      do 101 k=1,l1
         cr2 = cc(1,k,5)+cc(1,k,2)
         ci5 = cc(1,k,5)-cc(1,k,2)
         cr3 = cc(1,k,4)+cc(1,k,3)
         ci4 = cc(1,k,4)-cc(1,k,3)
         ch(1,1,k) = cc(1,k,1)+cr2+cr3
         ch(ido,2,k) = cc(1,k,1)+tr11*cr2+tr12*cr3
         ch(1,3,k) = ti11*ci5+ti12*ci4
         ch(ido,4,k) = cc(1,k,1)+tr12*cr2+tr11*cr3
         ch(1,5,k) = ti12*ci5-ti11*ci4
  101 continue
      if (ido .eq. 1) return
      idp2 = ido+2
      do 103 k=1,l1
         do 102 i=3,ido,2
            ic = idp2-i
            dr2 = wa1(i-2)*cc(i-1,k,2)+wa1(i-1)*cc(i,k,2)
            di2 = wa1(i-2)*cc(i,k,2)-wa1(i-1)*cc(i-1,k,2)
            dr3 = wa2(i-2)*cc(i-1,k,3)+wa2(i-1)*cc(i,k,3)
            di3 = wa2(i-2)*cc(i,k,3)-wa2(i-1)*cc(i-1,k,3)
            dr4 = wa3(i-2)*cc(i-1,k,4)+wa3(i-1)*cc(i,k,4)
            di4 = wa3(i-2)*cc(i,k,4)-wa3(i-1)*cc(i-1,k,4)
            dr5 = wa4(i-2)*cc(i-1,k,5)+wa4(i-1)*cc(i,k,5)
            di5 = wa4(i-2)*cc(i,k,5)-wa4(i-1)*cc(i-1,k,5)
            cr2 = dr2+dr5
            ci5 = dr5-dr2
            cr5 = di2-di5
            ci2 = di2+di5
            cr3 = dr3+dr4
            ci4 = dr4-dr3
            cr4 = di3-di4
            ci3 = di3+di4
            ch(i-1,1,k) = cc(i-1,k,1)+cr2+cr3
            ch(i,1,k) = cc(i,k,1)+ci2+ci3
            tr2 = cc(i-1,k,1)+tr11*cr2+tr12*cr3
            ti2 = cc(i,k,1)+tr11*ci2+tr12*ci3
            tr3 = cc(i-1,k,1)+tr12*cr2+tr11*cr3
            ti3 = cc(i,k,1)+tr12*ci2+tr11*ci3
            tr5 = ti11*cr5+ti12*cr4
            ti5 = ti11*ci5+ti12*ci4
            tr4 = ti12*cr5-ti11*cr4
            ti4 = ti12*ci5-ti11*ci4
            ch(i-1,3,k) = tr2+tr5
            ch(ic-1,2,k) = tr2-tr5
            ch(i,3,k) = ti2+ti5
            ch(ic,2,k) = ti5-ti2
            ch(i-1,5,k) = tr3+tr4
            ch(ic-1,4,k) = tr3-tr4
            ch(i,5,k) = ti3+ti4
            ch(ic,4,k) = ti4-ti3
  102    continue
  103 continue
      return
      end
      subroutine radfg (ido,ip,l1,idl1,cc,c1,c2,ch,ch2,wa)
      dimension       ch(ido,l1,ip)          ,cc(ido,ip,l1)          ,
     1                c1(ido,l1,ip)          ,c2(idl1,ip),
     2                ch2(idl1,ip)           ,wa(1)
      data tpi/6.28318530717959/
      arg = tpi/float(ip)
      dcp = cos(arg)
      dsp = sin(arg)
      ipph = (ip+1)/2
      ipp2 = ip+2
      idp2 = ido+2
      nbd = (ido-1)/2
      if (ido .eq. 1) go to 119
      do 101 ik=1,idl1
         ch2(ik,1) = c2(ik,1)
  101 continue
      do 103 j=2,ip
         do 102 k=1,l1
            ch(1,k,j) = c1(1,k,j)
  102    continue
  103 continue
      if (nbd .gt. l1) go to 107
      is = -ido
      do 106 j=2,ip
         is = is+ido
         idij = is
         do 105 i=3,ido,2
            idij = idij+2
            do 104 k=1,l1
               ch(i-1,k,j) = wa(idij-1)*c1(i-1,k,j)+wa(idij)*c1(i,k,j)
               ch(i,k,j) = wa(idij-1)*c1(i,k,j)-wa(idij)*c1(i-1,k,j)
  104       continue
  105    continue
  106 continue
      go to 111
  107 is = -ido
      do 110 j=2,ip
         is = is+ido
         do 109 k=1,l1
            idij = is
            do 108 i=3,ido,2
               idij = idij+2
               ch(i-1,k,j) = wa(idij-1)*c1(i-1,k,j)+wa(idij)*c1(i,k,j)
               ch(i,k,j) = wa(idij-1)*c1(i,k,j)-wa(idij)*c1(i-1,k,j)
  108       continue
  109    continue
  110 continue
  111 if (nbd .lt. l1) go to 115
      do 114 j=2,ipph
         jc = ipp2-j
         do 113 k=1,l1
            do 112 i=3,ido,2
               c1(i-1,k,j) = ch(i-1,k,j)+ch(i-1,k,jc)
               c1(i-1,k,jc) = ch(i,k,j)-ch(i,k,jc)
               c1(i,k,j) = ch(i,k,j)+ch(i,k,jc)
               c1(i,k,jc) = ch(i-1,k,jc)-ch(i-1,k,j)
  112       continue
  113    continue
  114 continue
      go to 121
  115 do 118 j=2,ipph
         jc = ipp2-j
         do 117 i=3,ido,2
            do 116 k=1,l1
               c1(i-1,k,j) = ch(i-1,k,j)+ch(i-1,k,jc)
               c1(i-1,k,jc) = ch(i,k,j)-ch(i,k,jc)
               c1(i,k,j) = ch(i,k,j)+ch(i,k,jc)
               c1(i,k,jc) = ch(i-1,k,jc)-ch(i-1,k,j)
  116       continue
  117    continue
  118 continue
      go to 121
  119 do 120 ik=1,idl1
         c2(ik,1) = ch2(ik,1)
  120 continue
  121 do 123 j=2,ipph
         jc = ipp2-j
         do 122 k=1,l1
            c1(1,k,j) = ch(1,k,j)+ch(1,k,jc)
            c1(1,k,jc) = ch(1,k,jc)-ch(1,k,j)
  122    continue
  123 continue
c
      ar1 = 1.
      ai1 = 0.
      do 127 l=2,ipph
         lc = ipp2-l
         ar1h = dcp*ar1-dsp*ai1
         ai1 = dcp*ai1+dsp*ar1
         ar1 = ar1h
         do 124 ik=1,idl1
            ch2(ik,l) = c2(ik,1)+ar1*c2(ik,2)
            ch2(ik,lc) = ai1*c2(ik,ip)
  124    continue
         dc2 = ar1
         ds2 = ai1
         ar2 = ar1
         ai2 = ai1
         do 126 j=3,ipph
            jc = ipp2-j
            ar2h = dc2*ar2-ds2*ai2
            ai2 = dc2*ai2+ds2*ar2
            ar2 = ar2h
            do 125 ik=1,idl1
               ch2(ik,l) = ch2(ik,l)+ar2*c2(ik,j)
               ch2(ik,lc) = ch2(ik,lc)+ai2*c2(ik,jc)
  125       continue
  126    continue
  127 continue
      do 129 j=2,ipph
         do 128 ik=1,idl1
            ch2(ik,1) = ch2(ik,1)+c2(ik,j)
  128    continue
  129 continue
c
      if (ido .lt. l1) go to 132
      do 131 k=1,l1
         do 130 i=1,ido
            cc(i,1,k) = ch(i,k,1)
  130    continue
  131 continue
      go to 135
  132 do 134 i=1,ido
         do 133 k=1,l1
            cc(i,1,k) = ch(i,k,1)
  133    continue
  134 continue
  135 do 137 j=2,ipph
         jc = ipp2-j
         j2 = j+j
         do 136 k=1,l1
            cc(ido,j2-2,k) = ch(1,k,j)
            cc(1,j2-1,k) = ch(1,k,jc)
  136    continue
  137 continue
      if (ido .eq. 1) return
      if (nbd .lt. l1) go to 141
      do 140 j=2,ipph
         jc = ipp2-j
         j2 = j+j
         do 139 k=1,l1
            do 138 i=3,ido,2
               ic = idp2-i
               cc(i-1,j2-1,k) = ch(i-1,k,j)+ch(i-1,k,jc)
               cc(ic-1,j2-2,k) = ch(i-1,k,j)-ch(i-1,k,jc)
               cc(i,j2-1,k) = ch(i,k,j)+ch(i,k,jc)
               cc(ic,j2-2,k) = ch(i,k,jc)-ch(i,k,j)
  138       continue
  139    continue
  140 continue
      return
  141 do 144 j=2,ipph
         jc = ipp2-j
         j2 = j+j
         do 143 i=3,ido,2
            ic = idp2-i
            do 142 k=1,l1
               cc(i-1,j2-1,k) = ch(i-1,k,j)+ch(i-1,k,jc)
               cc(ic-1,j2-2,k) = ch(i-1,k,j)-ch(i-1,k,jc)
               cc(i,j2-1,k) = ch(i,k,j)+ch(i,k,jc)
               cc(ic,j2-2,k) = ch(i,k,jc)-ch(i,k,j)
  142       continue
  143    continue
  144 continue
      return
      end
      subroutine rfftb (n,r,wsave)
      dimension       r(1)       ,wsave(1)
      if (n .eq. 1) return
      call rfftb1 (n,r,wsave,wsave(n+1),wsave(2*n+1))
      return
      end
      subroutine rfftb1 (n,c,ch,wa,ifac)
      dimension       ch(1)      ,c(1)       ,wa(1)      ,ifac(1)
      nf = ifac(2)
      na = 0
      l1 = 1
      iw = 1
      do 116 k1=1,nf
         ip = ifac(k1+2)
         l2 = ip*l1
         ido = n/l2
         idl1 = ido*l1
         if (ip .ne. 4) go to 103
         ix2 = iw+ido
         ix3 = ix2+ido
         if (na .ne. 0) go to 101
         call radb4 (ido,l1,c,ch,wa(iw),wa(ix2),wa(ix3))
         go to 102
  101    call radb4 (ido,l1,ch,c,wa(iw),wa(ix2),wa(ix3))
  102    na = 1-na
         go to 115
  103    if (ip .ne. 2) go to 106
         if (na .ne. 0) go to 104
         call radb2 (ido,l1,c,ch,wa(iw))
         go to 105
  104    call radb2 (ido,l1,ch,c,wa(iw))
  105    na = 1-na
         go to 115
  106    if (ip .ne. 3) go to 109
         ix2 = iw+ido
         if (na .ne. 0) go to 107
         call radb3 (ido,l1,c,ch,wa(iw),wa(ix2))
         go to 108
  107    call radb3 (ido,l1,ch,c,wa(iw),wa(ix2))
  108    na = 1-na
         go to 115
  109    if (ip .ne. 5) go to 112
         ix2 = iw+ido
         ix3 = ix2+ido
         ix4 = ix3+ido
         if (na .ne. 0) go to 110
         call radb5 (ido,l1,c,ch,wa(iw),wa(ix2),wa(ix3),wa(ix4))
         go to 111
  110    call radb5 (ido,l1,ch,c,wa(iw),wa(ix2),wa(ix3),wa(ix4))
  111    na = 1-na
         go to 115
  112    if (na .ne. 0) go to 113
         call radbg (ido,ip,l1,idl1,c,c,c,ch,ch,wa(iw))
         go to 114
  113    call radbg (ido,ip,l1,idl1,ch,ch,ch,c,c,wa(iw))
  114    if (ido .eq. 1) na = 1-na
  115    l1 = l2
         iw = iw+(ip-1)*ido
  116 continue
      if (na .eq. 0) return
      do 117 i=1,n
         c(i) = ch(i)
  117 continue
      return
      end
      subroutine rfftf (n,r,wsave)
      dimension       r(1)       ,wsave(1)
      if (n .eq. 1) return
      call rfftf1 (n,r,wsave,wsave(n+1),wsave(2*n+1))
      return
      end
      subroutine rfftf1 (n,c,ch,wa,ifac)
      dimension       ch(1)      ,c(1)       ,wa(1)      ,ifac(1)
      nf = ifac(2)
      na = 1
      l2 = n
      iw = n
      do 111 k1=1,nf
         kh = nf-k1
         ip = ifac(kh+3)
         l1 = l2/ip
         ido = n/l2
         idl1 = ido*l1
         iw = iw-(ip-1)*ido
         na = 1-na
         if (ip .ne. 4) go to 102
         ix2 = iw+ido
         ix3 = ix2+ido
         if (na .ne. 0) go to 101
         call radf4 (ido,l1,c,ch,wa(iw),wa(ix2),wa(ix3))
         go to 110
  101    call radf4 (ido,l1,ch,c,wa(iw),wa(ix2),wa(ix3))
         go to 110
  102    if (ip .ne. 2) go to 104
         if (na .ne. 0) go to 103
         call radf2 (ido,l1,c,ch,wa(iw))
         go to 110
  103    call radf2 (ido,l1,ch,c,wa(iw))
         go to 110
  104    if (ip .ne. 3) go to 106
         ix2 = iw+ido
         if (na .ne. 0) go to 105
         call radf3 (ido,l1,c,ch,wa(iw),wa(ix2))
         go to 110
  105    call radf3 (ido,l1,ch,c,wa(iw),wa(ix2))
         go to 110
  106    if (ip .ne. 5) go to 108
         ix2 = iw+ido
         ix3 = ix2+ido
         ix4 = ix3+ido
         if (na .ne. 0) go to 107
         call radf5 (ido,l1,c,ch,wa(iw),wa(ix2),wa(ix3),wa(ix4))
         go to 110
  107    call radf5 (ido,l1,ch,c,wa(iw),wa(ix2),wa(ix3),wa(ix4))
         go to 110
  108    if (ido .eq. 1) na = 1-na
         if (na .ne. 0) go to 109
         call radfg (ido,ip,l1,idl1,c,c,c,ch,ch,wa(iw))
         na = 1
         go to 110
  109    call radfg (ido,ip,l1,idl1,ch,ch,ch,c,c,wa(iw))
         na = 0
  110    l2 = l1
  111 continue
      if (na .eq. 1) return
      do 112 i=1,n
         c(i) = ch(i)
  112 continue
      return
      end
      subroutine rffti (n,wsave)
      dimension       wsave(1)
      if (n .eq. 1) return
      call rffti1 (n,wsave(n+1),wsave(2*n+1))
      return
      end
      subroutine rffti1 (n,wa,ifac)
      dimension       wa(1)      ,ifac(1)    ,ntryh(4)
      data ntryh(1),ntryh(2),ntryh(3),ntryh(4)/4,2,3,5/
      nl = n
      nf = 0
      j = 0
  101 j = j+1
      if (j-4) 102,102,103
  102 ntry = ntryh(j)
      go to 104
  103 ntry = ntry+2
  104 nq = nl/ntry
      nr = nl-ntry*nq
      if (nr) 101,105,101
  105 nf = nf+1
      ifac(nf+2) = ntry
      nl = nq
      if (ntry .ne. 2) go to 107
      if (nf .eq. 1) go to 107
      do 106 i=2,nf
         ib = nf-i+2
         ifac(ib+2) = ifac(ib+1)
  106 continue
      ifac(3) = 2
  107 if (nl .ne. 1) go to 104
      ifac(1) = n
      ifac(2) = nf
      tpi = 6.28318530717959
      argh = tpi/float(n)
      is = 0
      nfm1 = nf-1
      l1 = 1
      if (nfm1 .eq. 0) return
      do 110 k1=1,nfm1
         ip = ifac(k1+2)
         ld = 0
         l2 = l1*ip
         ido = n/l2
         ipm = ip-1
         do 109 j=1,ipm
            ld = ld+l1
            i = is
            argld = float(ld)*argh
            fi = 0.
            do 108 ii=3,ido,2
               i = i+2
               fi = fi+1.
               arg = fi*argld
               wa(i-1) = cos(arg)
               wa(i) = sin(arg)
  108       continue
            is = is+ido
  109    continue
         l1 = l2
  110 continue
      return
      end

      subroutine filter(azero,lsort,mlmax,jtrun,filt,sgeo,sgeox)
      dimension filt(mlmax),sgeo(mlmax,2),lsort(mlmax)      
     *, sgeox(mlmax,2)
c
      pi= 4.0*atan(1.0)
      jj= jtrun
      rj= 1.0/(jj) 
      do 1 l=2,jj
      fac= pi*(l-1.0)*rj
      filt(l)= sin(fac)/fac
      filt(l)= filt(l)**azero
    1 continue
      filt(1)= 1.0
      do 2 ml=1,mlmax
      l= lsort(ml)
      sgeox(ml,1)= sgeo(ml,1)*filt(l)
      sgeox(ml,2)= sgeo(ml,2)*filt(l)
    2 continue
c
      return
      end
      subroutine tranrs(istrt,im,jm,mlmax,poly,w,r,s)
c
      dimension poly(mlmax,jm/2),s(mlmax,2),r(im,jm),w(jm)
      dimension cc(64+3,32),work(64*32,2)
c
      common/ fftcom/ trigs(1280),ifax(19)
c
      jtrun= 2*((1+(im-1)/3)/2)
      mlx= (jtrun/2)*((jtrun+1)/2)
c
      jstrt= 1
      if(istrt.eq.0) jstrt= 2
c
      do 23 j=1,jm
      do 23 i=1,im
      cc(i,j)= r(i,j)
   23 continue
c     call fftfax(im,ifax,trigs)
c
      call rfftmlt(cc,work,trigs,ifax,1,im+3,im,jm,-1)
c
c  if istrt .eq. zero, the quadrature integral is initialized from zero,
c  otherwise the sum is added to initial 's' array passed with call.
c
      if(istrt.eq.0) then
c
      m1= 0
      do 62 l=jtrun-1,1,-2
cdir$ ivdep     
         do 63 m = 1, l
         mm= 2*m-1
         mp= mm+1
         ml= m+m1
         mk= ml+mlx
            s(ml,1) = w(1)*poly(ml,1)*(cc(mm,1)+cc(mm,jm))
            s(ml,2) = w(1)*poly(ml,1)*(cc(mp,1)+cc(mp,jm))
            s(mk,1) = w(1)*poly(mk,1)*(cc(mm,1)-cc(mm,jm))
            s(mk,2) = w(1)*poly(mk,1)*(cc(mp,1)-cc(mp,jm))
   63    continue
      m1= m1+l
   62 continue
c
      ml= mlx*2
cdir$ ivdep     
      do 64 m=2,jtrun,2
      ml=ml+1
      mm= 2*m-1
      mp= mm+1
      s(ml,1)= w(1)*poly(ml,1)*(cc(mm,1)+cc(mm,jm))
      s(ml,2)= w(1)*poly(ml,1)*(cc(mp,1)+cc(mp,jm))
   64 continue
      endif
c
      do 70 j=jstrt,jm/2
      jj= jm-j+1
      m1= 0
      do 72 l=jtrun-1,1,-2
cdir$ ivdep     
         do 73 m = 1, l
         mm= 2*m-1
         mp= mm+1
         ml= m+m1
         mk= ml+mlx
            s(ml,1) = s(ml,1)+w(j)*poly(ml,j)*(cc(mm,j)+cc(mm,jj))
            s(ml,2) = s(ml,2)+w(j)*poly(ml,j)*(cc(mp,j)+cc(mp,jj))
            s(mk,1) = s(mk,1)+w(j)*poly(mk,j)*(cc(mm,j)-cc(mm,jj))
            s(mk,2) = s(mk,2)+w(j)*poly(mk,j)*(cc(mp,j)-cc(mp,jj))
   73    continue
      m1= m1+l
   72 continue
c
      ml= mlx*2
cdir$ ivdep     
      do 65 m=2,jtrun,2
      ml=ml+1
      mm= 2*m-1
      mp= mm+1
      s(ml,1)= s(ml,1)+w(j)*poly(ml,j)*(cc(mm,j)+cc(mm,jj))
      s(ml,2)= s(ml,2)+w(j)*poly(ml,j)*(cc(mp,j)+cc(mp,jj))
   65 continue
   70 continue
c
      return
      end
      subroutine transr(im,jm,mlmax,poly,s,r,iqp,ichar,jchar)
c
      dimension poly(mlmax,jm/2),s(mlmax,2),r(im,jm)
      dimension cc(64+3,32),work(64*32,2)
c
      common/ fftcom/ trigs(1280),ifax(19)
c
      character*8 ichar,jchar
c
c
      jtrun= 2*((1+(im-1)/3)/2)
      mlx= (jtrun/2)*((jtrun+1)/2)
c
ccmic$ do all autoscope
ccmic$1 shared (im,jm,mlx,jtrun,poly,s,cc)
ccmic$1 private (j,jj,m,ml,mm,mp,mk,m1)
c
      do 5 j=1,jm/2
      jj= jm+1-j
cdir$ ivdep
      do 55 m=1,im+3
      cc(m,j)= 0.0
      cc(m,jj)= 0.0
   55 continue
      ml= 2*mlx
cdir@ ivdep
      do 3 m=2,jtrun,2
      ml= ml+1
      mm= 2*m-1
      mp= mm+1
      cc(mm,j)= poly(ml,j)*s(ml,1)
      cc(mp,j)= poly(ml,j)*s(ml,2)
      cc(mm,jj)= cc(mm,j)
      cc(mp,jj)= cc(mp,j)
    3 continue
c
      m1= 0
      do 5 l=jtrun-1,1,-2
cdir@ ivdep
      do 6 m=1,l
      mm= 2*m-1
      mp= mm+1
      ml= m+m1
      mk= ml+mlx
      cc(mm,j)= cc(mm,j)+poly(ml,j)*s(ml,1)+poly(mk,j)*s(mk,1)
      cc(mm,jj)=cc(mm,jj)+poly(ml,j)*s(ml,1)-poly(mk,j)*s(mk,1)
      cc(mp,j)= cc(mp,j)+poly(ml,j)*s(ml,2)+poly(mk,j)*s(mk,2)
      cc(mp,jj)=cc(mp,jj)+poly(ml,j)*s(ml,2)-poly(mk,j)*s(mk,2)
    6 continue
      m1= m1+l
    5 continue
c
      call rfftmlt(cc,work,trigs,ifax,1,im+3,im,jm,1)
c
ccmic$ do all shared(jm,im,cc,r)
ccmic$1  private(j, i)
      do 22 j=1,jm
cdir$ ivdep
      do 22 i=1,im
      r(i,j)= cc(i,j)
   22 continue
c
      if(iqp.gt.0) then    
      if(iqp.ge.2) call qprnth(r(1,1),ichar//jchar,1,1,im,jm)
      if(iqp.ge.1)call qpnh(r(1,1),ichar//jchar,1,1,im,jm
     *, xmin,xmax)
      endif
c
      return
      end
      subroutine shft(im,jm,num,x)
      dimension x(im,jm,num),xx(64)   
c
      ioff= im/6
c
      do 100 kk=1,num
      do 400 j=1,jm
      do 410 i=ioff+1,im
      xx(i)= x(i-ioff,j,kk)
  410 continue
c
      do 420 i=1,ioff
      xx(i)= x(i+im-ioff,j,kk)
  420 continue
      do 400 i=1,im 
      x(i,j,kk)= xx(i)
  400 continue
  100 continue
      return
      end
      subroutine qprnth(a,t1,ic,jc,m,n) 
c
c         
c  qprnth prints an array a(m,n) starting at address a(1+ic,1+jc).    
c  values are automatically scaled to allow integer format printing.  
c         
c a= fwa of m x n array       
c t1 = title (16 character) 
c ic,jc=lower left corner coords to be printed    
c up to 43 x 83 points printed
c
      dimension ix(43)
      character*16 t1
      dimension a(m,n)   
c
	haf= 0.5
c  determine grid limits      
    3 ie=min0(ic+42,m)        
      jl= n         
c  index backwards checking for max     
c         
   11 xm=0.         
      do 14 j=jc,jl 
      do 14 i=ic,ie 
      af= a(i,j)
   14 xm=max(xm,abs(af))      
c  determine scaling factor limits      
      if(xm.lt.1.e-35) xm=99. 
	x99= 99.
      xm=log10(x99/xm)       
      kp=xm         
      if(xm.lt.0.)kp=kp-1     
c  print scaling constants    
   12 print 1,t1,kp,(i,i=ic,ie,2)        
    1 format(1h0,a16,'   k=',i3, /1x,22i6)        
      fk=10.**kp    
c  quickprint field 
      jli= jl+1     
      do 2 j=jc,jl  
      jli= jli-1    
      ii= 0         
      if(kp.ne.0) go to 8     
      do 9 i=ic,ie  
      ii=ii+1       
      af= a(i,jli)
    9 ix(ii)=af+sign(haf,af)   
      go to 10      
    8 do 7 i=ic,ie  
      ii=ii+1       
      af= a(i,jli)
    7 ix(ii)=af*fk+sign(haf,af)
   10 print 6,jli,(ix(i),i=1,ii),jli    
    6 format(i4,44i3)         
    2 continue      
      return        
      end 
      subroutine sortml(jtrun,mlmax,msort,lsort,mlsort)
c
      dimension msort(mlmax),lsort(mlmax),mlsort(jtrun,jtrun)
c
      mlx= (jtrun/2)*((jtrun+1)/2)
      ml= 0
      do 1 k=1,jtrun-1,2
      do 1 m=1,jtrun-k  
      ml= ml+1
      mlp= ml+mlx
      mlsort(m,m+k)= mlp
      mlsort(m,m+k-1)= ml
      msort(ml)= m
      lsort(ml)= m+k-1
      msort(mlp)= m
      lsort(mlp)= m+k
    1 continue
c
      ml= mlp
      do 2 m=2,jtrun,2
      ml= ml+1
      mlsort(m,jtrun)= ml
      msort(ml)= m
      lsort(ml)= jtrun
    2 continue
      return
      end
      subroutine qpnh(fld,title,i1,j1,im,jm,xmin,xmax)        
c
c         
      dimension fld(im,jm)    
      character*16 title
c     
      xmin= 1.0e35  
      xmax= -1.0e35
      imin=1
      jmin=1
      imax=1
      imin=1
c         
      do 10 j=j1,jm
      do 10 i=i1,im
      if(fld(i,j).le.xmin) then      
      xmin= fld(i,j)
      jmin= j
      imin= i       
      endif         
      if(fld(i,j).gt.xmax) then      
      xmax= fld(i,j)       
      jmax= j
      imax= i       
      endif         
   10 continue      
c         
      print 9000, title         
 9000 format(1h0,a16)         
      print 8995, imax,jmax,xmax,imin,jmin,xmin   
 8995 format(' imax=',i4,' jmax=',i4,' xlarg=',g12.5        
     *,' imin=',i4,' jmin=',i4,' xsmal=',g12.5)   
      return        
      end 
      subroutine lgndr(jm2,jtrun,mlmax,mlsort,poly,dpoly,sinl)
c         
c  generate legendre polynomials and their derivatives on the         
c  gaussian latitudes         
c         
c         
c ref= belousov, s. l., 1962= tables of normalized associated         
c        legendre polynomials. pergamon press, new york     
c         
      dimension poly(mlmax,jm2),dpoly(mlmax,jm2),sinl(jm2) 
     *, mlsort(jtrun,jtrun)
c
      parameter (jtrunx= 100)
      dimension pnm(jtrunx+1,jtrunx),dpnm(jtrunx+1,jtrunx)      
c         
c sinl is sin(latitude) = cos(colatitude)         
c pnm(np,mp) is legendre polynomial p(n,m) with np=n+1, mp=m+1        
c pnm(mp,np+1) is x derivative of p(n,m) with np=n+1, mp=m+1
c         
      jtrunp= jtrun+1        
      do 1001 j=1,jm2
      xx= sinl(j)       
      sn= sqrt(1.0-xx*xx)     
       sn2i = 1.0/(1.0 - xx*xx)         
      rt2= sqrt(2.0)
       c1 = rt2     
c         
       pnm(1,1) = 1.0/rt2     
      theta=-atan(xx/sqrt(1.0-xx*xx))+2.0*atan(1.0)         
c         
      do 20 n=1,jtrun         
       np = n + 1   
      fn=n
       fn2 = fn + fn
       fn2s = fn2*fn2         
c eq 22   
      c1= c1*sqrt(1.0-1.0/fn2s)         
      c3= c1/sqrt(fn*(fn+1.0))
       ang = fn*theta         
       s1 = 0.0     
       s2 = 0.0     
       c4 = 1.0     
       c5 = fn      
       a = -1.0     
       b = 0.0      
c      
      do 27 kp=1,np,2         
       k = kp - 1   
      s2= s2+c5*sin(ang)*c4   
      if (k.eq.n) c4 = 0.5*c4 
      s1= s1+c4*cos(ang)      
       a = a + 2.0  
       b = b + 1.0  
      fk=k
       ang = theta*(fn - fk - 2.0)      
       c4 = (a*(fn - b + 1.0)/(b*(fn2 - a)))*c4   
       c5 = c5 - 2.0
   27 continue      
c eq 19   
       pnm(np,1) = s1*c1      
c eq 21   
       pnm(np,2) = s2*c3      
   20 continue      
c         
      do 4 mp=3,jtrunp        
       m = mp - 1   
      fm= m         
       fm1 = fm - 1.0         
       fm2 = fm - 2.0         
       fm3 = fm - 3.0         
      c6= sqrt(1.0+1.0/(fm+fm))         
c eq 23   
       pnm(mp,mp) = c6*sn*pnm(m,m)      
      if (mp - jtrunp) 3,4,4  
    3 continue      
       nps = mp + 1 
c         
      do 41 np=nps,jtrunp     
       n = np - 1   
      fn= n         
       fn2 = fn + fn
       c7 = (fn2 + 1.0)/(fn2 - 1.0)     
       c8 = (fm1 + fn)/((fm + fn)*(fm2 + fn))     
      c= sqrt((fn2+1.0)*c8*(fm3+fn)/(fn2-3.0))    
      d= -sqrt(c7*c8*(fn-fm1))
      e= sqrt(c7*(fn-fm)/(fn+fm))       
c eq 17   
       pnm(np,mp) = c*pnm(np-2,mp-2)    
     1            + xx*(d*pnm(np-1,mp-2) + e*pnm(np - 1,mp))
   41 continue      
    4 continue      
c     
      do 50 mp=1,jtrun        
      fm= mp-1.0    
       fms = fm*fm  
      do 50 np=mp,jtrun       
      fnp= np       
       fnp2 = fnp + fnp       
       cf = (fnp*fnp - fms)*(fnp2 - 1.0)/(fnp2 + 1.0)       
      cf= sqrt(cf)  
c der     
      dpnm(np,mp)   = -sn2i*(cf*pnm(np+1,mp) - fnp*xx*pnm(np,mp))     
   50 continue      
c    
      do 71 m=1,jtrun
      do 71 l=m,jtrun
      ml= mlsort(m,l)
      poly(ml,j)= pnm(l,m)    
      dpoly(ml,j)=dpnm(l,m)  
   71 continue
      dpoly(1,j)= 0.0
 1001 continue
      return        
      end 
      subroutine rfftmlt(cc,w,trigs,ifax,ist,nxp,nx,my,isign)
c
c  this subroutine if a temporary version of the cray scientific
c  software library routine that will eventually be used.  the
c  fft being used is a fortran version of the cyber 205 routines
c  developed by clive temperton of the ukmo
c
      dimension cc(nxp,my),w(my,nx),trigs(nx),ifax(*)
c
      logical first
      data first/.true./
c
c  on first call compute necessary coefficient arrays
c
      onx= 1.0/nx
      if(first) then
      first=.false.
      call rffti(nx,trigs)
      endif
c
      if(isign.lt.0) then
c
      do 20 j=1,my
c
      call rfftf(nx,cc(1,j),trigs)
c
      do 25 i=nx,2,-1
      cc(i+1,j)= cc(i,j)*onx
c      cc(i,j)= cc(i,j)*onx
   25 continue
      cc(2,j)= 0.0 
      cc(1,j)= cc(1,j)*onx
   20 continue
c
      else
c
      do 40 j=1,my
      do 45 i=2,nx
      cc(i,j)= cc(i+1,j)
   45 continue
c
      call rfftb(nx,cc(1,j),trigs)
c
   40 continue
      endif
c
      return
      end     
      subroutine nfwrit(filnam,msg,itype,istrt,numrec,len,x,itau,cdtg
     *,istat)
c
c
      dimension x(len,numrec)
      character*8 cdtg
      character*48 filnam,blk24
      character*54 file
c
      parameter (nf=20)
      common/fncom/ cfiles(nf)
      common/fucom/ fcall
      character*48 cfiles
      logical fcall
c
      data blk24/'                                                '/
c
      if(fcall) then
      fcall=.false.
      do 5 i=1,nf
      cfiles(i)=blk24
    5 continue
      endif
c
      do 10 k=1,nf 
      kk= k
      if(cfiles(k).eq.blk24) cfiles(k)= filnam
      if(cfiles(k).eq.filnam) go to 20 
   10 continue
   20 iun= 10+kk   
c
      call nfopen(filnam,itau,len,iun,file)
c
      do 30 j=1,numrec
      irec= istrt+j-1
      write(iun,rec=irec,err=45) (x(i,j),i=1,len),itau,cdtg
   30 continue
      if(itau.ge.0) close(unit= iun)
c
      if(msg.eq.0) return
      print 100,file,numrec,istrt,len
  100 format(1x,a54,'write: ',i3,' records starting at rec=',i4
     *,' : len= ',i8)
      print 200, itau,cdtg
  200 format(' data written for tau=',i6,' : dtg= ',a8)
      istat= 0
      return
c
   45 print 400, file,iun,irec
  400 format(' bad write on ',a54,' : unit=',i3,' : record= ',i4)
      istat= 1
      return
      end
      subroutine nfread(filnam,msg,itype,istrt,numrec,len,x,itau,cdtg
     *,istat)
c
      dimension x(len,numrec)
c
      character*8 cdtg
      character*48 filnam,blk24
      character*54 file
c
      parameter (nf=20)
      common/fncom/ cfiles(nf)
      common/fucom/ fcall
      character*48 cfiles
      logical fcall
      dimension itau2(2)
c
      data blk24/'                                                '/
      if(fcall) then
      fcall=.false.
      do 5 i=1,nf
      cfiles(i)=blk24
    5 continue
      endif
c
      do 10 k=1,nf 
      kk= k
      if(cfiles(k).eq.blk24) cfiles(k)= filnam
      if(cfiles(k).eq.filnam) go to 20 
   10 continue
   20 iun= 10+kk   
c
      call nfopen(filnam,itau,len,iun,file)
c
      do 30 j=1,numrec
      irec= istrt+j-1
      read(iun,rec=irec,err=45) (x(i,j),i=1,len),itau2,cdtg 
   30 continue
      if(itau.ge.0) close(unit=iun)
c
      if(msg.eq.0) return
      print 100,file,numrec,istrt,len
  100 format(1x,a54,'read: ',i3,' records starting at rec=',i4
     *,' : len= ',i8)
      print 200, itau2,cdtg
  200 format(' data read for tau=',2i6,' : dtg= ',a8)
      istat= 0
      return
c
   45 print 400, file,iun,irec
  400 format(' bad read on ',a54,' : unit=',i3,' : record= ',i4)
      istat= 1
      return
      end
      subroutine nfopen(filnam,itau,len,iun,file) 
c
      character*54 file
      character*48 filnam
      character*8 status
      character*6 ctau
      common/fucom/ fcall
      logical fcall
c
      logical lex,opn
      data fcall/.true./
c
      lenr= 4*(4+len)
c
      call chlen(filnam,lenc)
      write(ctau,'(i6.6)') itau
c
      if(itau.lt.0) then
      file= filnam(1:lenc)
      else
      file= filnam(1:lenc)//ctau
      endif
c
      inquire(file=file,exist=lex,opened=opn)
      if(opn) return
c
      if(lex) then 
      status='old' 
      else
      status='new' 
      endif
      print*, file,'status=',status
c
      open(unit=iun,file=file,access='direct',form='unformatted'
     *, recl=lenr,status=status)
c
      print 100, filnam,iun,lenr 
  100 format(1x,a54,' opened as unit=',i3,' : lenr=',i9,' bytes ')
      return 
      end
      subroutine radb2 (ido,l1,cc,ch,wa1)
      dimension       cc(ido,2,l1)           ,ch(ido,l1,2)           ,
     1                wa1(1)
      do 101 k=1,l1
         ch(1,k,1) = cc(1,1,k)+cc(ido,2,k)
         ch(1,k,2) = cc(1,1,k)-cc(ido,2,k)
  101 continue
      if (ido-2) 107,105,102
  102 idp2 = ido+2
      do 104 k=1,l1
         do 103 i=3,ido,2
            ic = idp2-i
            ch(i-1,k,1) = cc(i-1,1,k)+cc(ic-1,2,k)
            tr2 = cc(i-1,1,k)-cc(ic-1,2,k)
            ch(i,k,1) = cc(i,1,k)-cc(ic,2,k)
            ti2 = cc(i,1,k)+cc(ic,2,k)
            ch(i-1,k,2) = wa1(i-2)*tr2-wa1(i-1)*ti2
            ch(i,k,2) = wa1(i-2)*ti2+wa1(i-1)*tr2
  103    continue
  104 continue
      if (mod(ido,2) .eq. 1) return
  105 do 106 k=1,l1
         ch(ido,k,1) = cc(ido,1,k)+cc(ido,1,k)
         ch(ido,k,2) = -(cc(1,2,k)+cc(1,2,k))
  106 continue
  107 return
      end
      subroutine radb3 (ido,l1,cc,ch,wa1,wa2)
      dimension       cc(ido,3,l1)           ,ch(ido,l1,3)           ,
     1                wa1(1)     ,wa2(1)
      data taur,taui /-.5,.866025403784439/
      do 101 k=1,l1
         tr2 = cc(ido,2,k)+cc(ido,2,k)
         cr2 = cc(1,1,k)+taur*tr2
         ch(1,k,1) = cc(1,1,k)+tr2
         ci3 = taui*(cc(1,3,k)+cc(1,3,k))
         ch(1,k,2) = cr2-ci3
         ch(1,k,3) = cr2+ci3
  101 continue
      if (ido .eq. 1) return
      idp2 = ido+2
      do 103 k=1,l1
         do 102 i=3,ido,2
            ic = idp2-i
            tr2 = cc(i-1,3,k)+cc(ic-1,2,k)
            cr2 = cc(i-1,1,k)+taur*tr2
            ch(i-1,k,1) = cc(i-1,1,k)+tr2
            ti2 = cc(i,3,k)-cc(ic,2,k)
            ci2 = cc(i,1,k)+taur*ti2
            ch(i,k,1) = cc(i,1,k)+ti2
            cr3 = taui*(cc(i-1,3,k)-cc(ic-1,2,k))
            ci3 = taui*(cc(i,3,k)+cc(ic,2,k))
            dr2 = cr2-ci3
            dr3 = cr2+ci3
            di2 = ci2+cr3
            di3 = ci2-cr3
            ch(i-1,k,2) = wa1(i-2)*dr2-wa1(i-1)*di2
            ch(i,k,2) = wa1(i-2)*di2+wa1(i-1)*dr2
            ch(i-1,k,3) = wa2(i-2)*dr3-wa2(i-1)*di3
            ch(i,k,3) = wa2(i-2)*di3+wa2(i-1)*dr3
  102    continue
  103 continue
      return
      end
      subroutine radb4 (ido,l1,cc,ch,wa1,wa2,wa3)
      dimension       cc(ido,4,l1)           ,ch(ido,l1,4)           ,
     1                wa1(1)     ,wa2(1)     ,wa3(1)
      data sqrt2 /1.414213562373095/
      do 101 k=1,l1
         tr1 = cc(1,1,k)-cc(ido,4,k)
         tr2 = cc(1,1,k)+cc(ido,4,k)
         tr3 = cc(ido,2,k)+cc(ido,2,k)
         tr4 = cc(1,3,k)+cc(1,3,k)
         ch(1,k,1) = tr2+tr3
         ch(1,k,2) = tr1-tr4
         ch(1,k,3) = tr2-tr3
         ch(1,k,4) = tr1+tr4
  101 continue
      if (ido-2) 107,105,102
  102 idp2 = ido+2
      do 104 k=1,l1
         do 103 i=3,ido,2
            ic = idp2-i
            ti1 = cc(i,1,k)+cc(ic,4,k)
            ti2 = cc(i,1,k)-cc(ic,4,k)
            ti3 = cc(i,3,k)-cc(ic,2,k)
            tr4 = cc(i,3,k)+cc(ic,2,k)
            tr1 = cc(i-1,1,k)-cc(ic-1,4,k)
            tr2 = cc(i-1,1,k)+cc(ic-1,4,k)
            ti4 = cc(i-1,3,k)-cc(ic-1,2,k)
            tr3 = cc(i-1,3,k)+cc(ic-1,2,k)
            ch(i-1,k,1) = tr2+tr3
            cr3 = tr2-tr3
            ch(i,k,1) = ti2+ti3
            ci3 = ti2-ti3
            cr2 = tr1-tr4
            cr4 = tr1+tr4
            ci2 = ti1+ti4
            ci4 = ti1-ti4
            ch(i-1,k,2) = wa1(i-2)*cr2-wa1(i-1)*ci2
            ch(i,k,2) = wa1(i-2)*ci2+wa1(i-1)*cr2
            ch(i-1,k,3) = wa2(i-2)*cr3-wa2(i-1)*ci3
            ch(i,k,3) = wa2(i-2)*ci3+wa2(i-1)*cr3
            ch(i-1,k,4) = wa3(i-2)*cr4-wa3(i-1)*ci4
            ch(i,k,4) = wa3(i-2)*ci4+wa3(i-1)*cr4
  103    continue
  104 continue
      if (mod(ido,2) .eq. 1) return
  105 continue
      do 106 k=1,l1
         ti1 = cc(1,2,k)+cc(1,4,k)
         ti2 = cc(1,4,k)-cc(1,2,k)
         tr1 = cc(ido,1,k)-cc(ido,3,k)
         tr2 = cc(ido,1,k)+cc(ido,3,k)
         ch(ido,k,1) = tr2+tr2
         ch(ido,k,2) = sqrt2*(tr1-ti1)
         ch(ido,k,3) = ti2+ti2
         ch(ido,k,4) = -sqrt2*(tr1+ti1)
  106 continue
  107 return
      end
      subroutine radb5 (ido,l1,cc,ch,wa1,wa2,wa3,wa4)
      dimension       cc(ido,5,l1)           ,ch(ido,l1,5)           ,
     1                wa1(1)     ,wa2(1)     ,wa3(1)     ,wa4(1)
      data tr11,ti11,tr12,ti12 /.309016994374947,.951056516295154,
     1-.809016994374947,.587785252292473/
      do 101 k=1,l1
         ti5 = cc(1,3,k)+cc(1,3,k)
         ti4 = cc(1,5,k)+cc(1,5,k)
         tr2 = cc(ido,2,k)+cc(ido,2,k)
         tr3 = cc(ido,4,k)+cc(ido,4,k)
         ch(1,k,1) = cc(1,1,k)+tr2+tr3
         cr2 = cc(1,1,k)+tr11*tr2+tr12*tr3
         cr3 = cc(1,1,k)+tr12*tr2+tr11*tr3
         ci5 = ti11*ti5+ti12*ti4
         ci4 = ti12*ti5-ti11*ti4
         ch(1,k,2) = cr2-ci5
         ch(1,k,3) = cr3-ci4
         ch(1,k,4) = cr3+ci4
         ch(1,k,5) = cr2+ci5
  101 continue
      if (ido .eq. 1) return
      idp2 = ido+2
      do 103 k=1,l1
         do 102 i=3,ido,2
            ic = idp2-i
            ti5 = cc(i,3,k)+cc(ic,2,k)
            ti2 = cc(i,3,k)-cc(ic,2,k)
            ti4 = cc(i,5,k)+cc(ic,4,k)
            ti3 = cc(i,5,k)-cc(ic,4,k)
            tr5 = cc(i-1,3,k)-cc(ic-1,2,k)
            tr2 = cc(i-1,3,k)+cc(ic-1,2,k)
            tr4 = cc(i-1,5,k)-cc(ic-1,4,k)
            tr3 = cc(i-1,5,k)+cc(ic-1,4,k)
            ch(i-1,k,1) = cc(i-1,1,k)+tr2+tr3
            ch(i,k,1) = cc(i,1,k)+ti2+ti3
            cr2 = cc(i-1,1,k)+tr11*tr2+tr12*tr3
            ci2 = cc(i,1,k)+tr11*ti2+tr12*ti3
            cr3 = cc(i-1,1,k)+tr12*tr2+tr11*tr3
            ci3 = cc(i,1,k)+tr12*ti2+tr11*ti3
            cr5 = ti11*tr5+ti12*tr4
            ci5 = ti11*ti5+ti12*ti4
            cr4 = ti12*tr5-ti11*tr4
            ci4 = ti12*ti5-ti11*ti4
            dr3 = cr3-ci4
            dr4 = cr3+ci4
            di3 = ci3+cr4
            di4 = ci3-cr4
            dr5 = cr2+ci5
            dr2 = cr2-ci5
            di5 = ci2-cr5
            di2 = ci2+cr5
            ch(i-1,k,2) = wa1(i-2)*dr2-wa1(i-1)*di2
            ch(i,k,2) = wa1(i-2)*di2+wa1(i-1)*dr2
            ch(i-1,k,3) = wa2(i-2)*dr3-wa2(i-1)*di3
            ch(i,k,3) = wa2(i-2)*di3+wa2(i-1)*dr3
            ch(i-1,k,4) = wa3(i-2)*dr4-wa3(i-1)*di4
            ch(i,k,4) = wa3(i-2)*di4+wa3(i-1)*dr4
            ch(i-1,k,5) = wa4(i-2)*dr5-wa4(i-1)*di5
            ch(i,k,5) = wa4(i-2)*di5+wa4(i-1)*dr5
  102    continue
  103 continue
      return
      end
      subroutine radbg (ido,ip,l1,idl1,cc,c1,c2,ch,ch2,wa)
      dimension       ch(ido,l1,ip)          ,cc(ido,ip,l1)          ,
     1                c1(ido,l1,ip)          ,c2(idl1,ip),
     2                ch2(idl1,ip)           ,wa(1)
      data tpi/6.28318530717959/
      arg = tpi/float(ip)
      dcp = cos(arg)
      dsp = sin(arg)
      idp2 = ido+2
      nbd = (ido-1)/2
      ipp2 = ip+2
      ipph = (ip+1)/2
      if (ido .lt. l1) go to 103
      do 102 k=1,l1
         do 101 i=1,ido
            ch(i,k,1) = cc(i,1,k)
  101    continue
  102 continue
      go to 106
  103 do 105 i=1,ido
         do 104 k=1,l1
            ch(i,k,1) = cc(i,1,k)
  104    continue
  105 continue
  106 do 108 j=2,ipph
         jc = ipp2-j
         j2 = j+j
         do 107 k=1,l1
            ch(1,k,j) = cc(ido,j2-2,k)+cc(ido,j2-2,k)
            ch(1,k,jc) = cc(1,j2-1,k)+cc(1,j2-1,k)
  107    continue
  108 continue
      if (ido .eq. 1) go to 116
      if (nbd .lt. l1) go to 112
      do 111 j=2,ipph
         jc = ipp2-j
         do 110 k=1,l1
            do 109 i=3,ido,2
               ic = idp2-i
               ch(i-1,k,j) = cc(i-1,2*j-1,k)+cc(ic-1,2*j-2,k)
               ch(i-1,k,jc) = cc(i-1,2*j-1,k)-cc(ic-1,2*j-2,k)
               ch(i,k,j) = cc(i,2*j-1,k)-cc(ic,2*j-2,k)
               ch(i,k,jc) = cc(i,2*j-1,k)+cc(ic,2*j-2,k)
  109       continue
  110    continue
  111 continue
      go to 116
  112 do 115 j=2,ipph
         jc = ipp2-j
         do 114 i=3,ido,2
            ic = idp2-i
            do 113 k=1,l1
               ch(i-1,k,j) = cc(i-1,2*j-1,k)+cc(ic-1,2*j-2,k)
               ch(i-1,k,jc) = cc(i-1,2*j-1,k)-cc(ic-1,2*j-2,k)
               ch(i,k,j) = cc(i,2*j-1,k)-cc(ic,2*j-2,k)
               ch(i,k,jc) = cc(i,2*j-1,k)+cc(ic,2*j-2,k)
  113       continue
  114    continue
  115 continue
  116 ar1 = 1.
      ai1 = 0.
      do 120 l=2,ipph
         lc = ipp2-l
         ar1h = dcp*ar1-dsp*ai1
         ai1 = dcp*ai1+dsp*ar1
         ar1 = ar1h
         do 117 ik=1,idl1
            c2(ik,l) = ch2(ik,1)+ar1*ch2(ik,2)
            c2(ik,lc) = ai1*ch2(ik,ip)
  117    continue
         dc2 = ar1
         ds2 = ai1
         ar2 = ar1
         ai2 = ai1
         do 119 j=3,ipph
            jc = ipp2-j
            ar2h = dc2*ar2-ds2*ai2
            ai2 = dc2*ai2+ds2*ar2
            ar2 = ar2h
            do 118 ik=1,idl1
               c2(ik,l) = c2(ik,l)+ar2*ch2(ik,j)
               c2(ik,lc) = c2(ik,lc)+ai2*ch2(ik,jc)
  118       continue
  119    continue
  120 continue
      do 122 j=2,ipph
         do 121 ik=1,idl1
            ch2(ik,1) = ch2(ik,1)+ch2(ik,j)
  121    continue
  122 continue
      do 124 j=2,ipph
         jc = ipp2-j
         do 123 k=1,l1
            ch(1,k,j) = c1(1,k,j)-c1(1,k,jc)
            ch(1,k,jc) = c1(1,k,j)+c1(1,k,jc)
  123    continue
  124 continue
      if (ido .eq. 1) go to 132
      if (nbd .lt. l1) go to 128
      do 127 j=2,ipph
         jc = ipp2-j
         do 126 k=1,l1
            do 125 i=3,ido,2
               ch(i-1,k,j) = c1(i-1,k,j)-c1(i,k,jc)
               ch(i-1,k,jc) = c1(i-1,k,j)+c1(i,k,jc)
               ch(i,k,j) = c1(i,k,j)+c1(i-1,k,jc)
               ch(i,k,jc) = c1(i,k,j)-c1(i-1,k,jc)
  125       continue
  126    continue
  127 continue
      go to 132
  128 do 131 j=2,ipph
         jc = ipp2-j
         do 130 i=3,ido,2
            do 129 k=1,l1
               ch(i-1,k,j) = c1(i-1,k,j)-c1(i,k,jc)
               ch(i-1,k,jc) = c1(i-1,k,j)+c1(i,k,jc)
               ch(i,k,j) = c1(i,k,j)+c1(i-1,k,jc)
               ch(i,k,jc) = c1(i,k,j)-c1(i-1,k,jc)
  129       continue
  130    continue
  131 continue
  132 continue
      if (ido .eq. 1) return
      do 133 ik=1,idl1
         c2(ik,1) = ch2(ik,1)
  133 continue
      do 135 j=2,ip
         do 134 k=1,l1
            c1(1,k,j) = ch(1,k,j)
  134    continue
  135 continue
      if (nbd .gt. l1) go to 139
      is = -ido
      do 138 j=2,ip
         is = is+ido
         idij = is
         do 137 i=3,ido,2
            idij = idij+2
            do 136 k=1,l1
               c1(i-1,k,j) = wa(idij-1)*ch(i-1,k,j)-wa(idij)*ch(i,k,j)
               c1(i,k,j) = wa(idij-1)*ch(i,k,j)+wa(idij)*ch(i-1,k,j)
  136       continue
  137    continue
  138 continue
      go to 143
  139 is = -ido
      do 142 j=2,ip
         is = is+ido
         do 141 k=1,l1
            idij = is
            do 140 i=3,ido,2
               idij = idij+2
               c1(i-1,k,j) = wa(idij-1)*ch(i-1,k,j)-wa(idij)*ch(i,k,j)
               c1(i,k,j) = wa(idij-1)*ch(i,k,j)+wa(idij)*ch(i-1,k,j)
  140       continue
  141    continue
  142 continue
  143 return
      end
      subroutine chlen(file,lenc)
      character*1 file(*)
      character*1 blnk1
      data blnk1/' '/
      lenc= 0
      do 1 i=1,100
      if(file(i).eq.blnk1) return  
      lenc= i
    1 continue
      return
      end
      subroutine gausl3 (n,xa,xb,wt,ab) 
c         
c weights and abscissas for nth order gaussian quadrature on (xa,xb). 
c input arguments   
c n  -the order desired       
c xa -the left endpoint of the interval of integration      
c xb -the right endpoint of the interval of integration     
c output arguments  
c ab -the n calculated abscissas        
c wt -the n calculated weights
c         
      implicit double precision (a-h,o-z)
c
      real  ab(n) ,wt(n),xa,xb     
c         
c machine dependent constants---        
c  tol - convergence criterion for double precision iteration         
c  pi  - given to 15 significant digits 
c  c1  -  1/8                     these are coefficients in mcmahon"s 
c  c2  -  -31/(2*3*8**2)          expansions of the kth zero of the   
c  c3  -  3779/(2*3*5*8**3)       bessel function j0(x) (cf. abramowitz,        
c  c4  -  -6277237/(3*5*7*8**5)   handbook of mathematical functions).
c  u   -  (1-(2/pi)**2)/4     
c         
      data tol/1.d-14/,pi/3.14159265358979/,u/.148678816357662/       
      data c1,c2,c3,c4/.125,-.080729166666667,.246028645833333,       
     1                 -1.82443876720609 /        
c         
c maximum number of iterations before giving up on convergence        
c         
      data maxit /5/
c         
c arithmetic statement function for converting integer to double      
c         
      dbli(i) = dble(float(i))
c         
      ddif = .5d0*(dble(xb)-dble(xa))   
      dsum = .5d0*(dble(xb)+dble(xa))   
      if (n .gt. 1) go to 101 
      ab(1) = 0.    
      wt(1) = 2.*ddif         
      go to 107     
  101 continue      
      nnp1 = n*(n+1)
      cond = 1./sqrt((.5+float(n))**2+u)
      lim = n/2     
c         
      do 105 k=1,lim
         b = (float(k)-.25)*pi
         bisq = 1./(b*b)      
c         
c rootbf approximates the kth zero of the bessel function j0(x)       
c         
         rootbf = b*(1.+bisq*(c1+bisq*(c2+bisq*(c3+bisq*c4))))        
c         
c      initial guess for kth root of legendre poly p-sub-n(x)         
c         
         dzero = cos(rootbf*cond)       
         do 103 i=1,maxit     
c         
            dpm2 = 1.d0       
            dpm1 = dzero      
c         
c       recursion relation for legendre polynomials         
c         
            do 102 nn=2,n     
               dp = (dbli(2*nn-1)*dzero*dpm1-dbli(nn-1)*dpm2)/dbli(nn)
               dpm2 = dpm1    
               dpm1 = dp      
  102       continue
            dtmp = 1.d0/(1.d0-dzero*dzero)        
            dppr = dbli(n)*(dpm2-dzero*dp)*dtmp   
            dp2pri = (2.d0*dzero*dppr-dbli(nnp1)*dp)*dtmp   
            drat = dp/dppr    
c         
c       cubically-convergent iterative improvement of root  
c         
            dzeri = dzero-drat*(1.d0+drat*dp2pri/(2.d0*dppr))         
            ddum= dabs(dzeri-dzero)
         if (ddum .le. tol) go to 104  
            dzero = dzeri     
  103    continue   
         print 504
  504    format(1x,' in gausl3, convergence failed')         
  104    continue   
         ddifx = ddif*dzero   
         ab(k) = dsum-ddifx   
         wt(k) = 2.d0*(1.d0-dzero*dzero)/(dbli(n)*dpm2)**2*ddif       
         i = n-k+1  
         ab(i) = dsum+ddifx   
         wt(i) = wt(k)        
  105 continue      
c         
      if (mod(n,2) .eq. 0) go to 107    
      ab(lim+1) = dsum        
      nm1 = n-1     
      dprod = n     
      do 106 k=1,nm1,2        
         dprod = dbli(nm1-k)*dprod/dbli(n-k)      
  106 continue      
      wt(lim+1) = 2.d0/dprod**2*ddif    
  107 return        
      end
