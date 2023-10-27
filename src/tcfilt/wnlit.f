      subroutine wnlit(w,mdw,m,n,l,ipivot,itype,h,scale,rnorm,idope,
     1   dope,done)
c***begin prologue  wnlit
c***refer to  wnnls
c
c     this is a companion subprogram to wnnls( ).
c     the documentation for wnnls( ) has more complete
c     usage instructions.
c
c     note  the m by (n+1) matrix w( , ) contains the rt. hand side
c           b as the (n+1)st col.
c
c     triangularize l1 by l1 subsystem, where l1=min(m,l), with
c     col interchanges.
c     revised march 4, 1982.
c***routines called  h12,isamax,scopy,srotm,srotmg,sscal,sswap
c***end prologue  wnlit
c
c     the editing required to convert this subroutine from single to
c     double precision involves the following character string changes.
c     use an editing command (change) /string-1/(to)string-2/.
c     (begin changes at line with c++ in cols. 1-3.)
c     /real (12 blanks)/double precision/,/scopy/dcopy/,/srotm/drotm/,
c     /sscal/dscal/,
c     /sswap/dswap/,/amax1/dmax1/,/isamax/idamax/,/.e-/.d-/,/e0/d0/
c
c++
      real             w(mdw,1), h(1), scale(1), dope(4), sparam(5)
      real             alsq, amax, eanorm, fac, factor, hbar, one, rn
      real             rnorm, sn, t, tau, tenm3, zero
      real             amax1
      integer itype(1), ipivot(1), idope(8)
      integer isamax
      logical indep, done, recalc
      data tenm3 /1.e-3/, zero /0.e0/, one /1.e0/
c
c***first executable statement  wnlit
      me = idope(1)
      mep1 = idope(2)
      krank = idope(3)
      krp1 = idope(4)
      nsoln = idope(5)
      niv = idope(6)
      niv1 = idope(7)
      l1 = idope(8)
c
      alsq = dope(1)
      eanorm = dope(2)
      fac = dope(3)
      tau = dope(4)
      np1 = n + 1
      lb = min0(m-1,l)
      recalc = .true.
      rnorm = zero
      krank = 0
c     we set factor=1.e0 so that the heavy weight alamda will be
c     included in the test for col independence.
      factor = 1.e0
      i = 1
      ip1 = 2
      lend = l
   10 if (.not.(i.le.lb)) go to 150
c
c     set ir to point to the i-th row.
      ir = i
      mend = m
      assign 20 to igo996
      go to 460
c
c     update-col-ss-and-find-pivot-col
   20 assign 30 to igo993
      go to 560
c
c     perform-col-interchange
c
c     set ic to point to i-th col.
   30 ic = i
      assign 40 to igo990
      go to 520
c
c     test-indep-of-incoming-col
   40 if (.not.(indep)) go to 110
c
c     eliminate i-th col below diag. using mod. givens transformations
c     applied to (a b).
      j = m
      do 100 jj=ip1,m
        jm1 = j - 1
        jp = jm1
c     when operating near the me line, use the largest elt.
c     above it as the pivot.
        if (.not.(j.eq.mep1)) go to 80
        imax = me
        amax = scale(me)*w(me,i)**2
   50   if (.not.(jp.ge.i)) go to 70
        t = scale(jp)*w(jp,i)**2
        if (.not.(t.gt.amax)) go to 60
        imax = jp
        amax = t
   60   jp = jp - 1
        go to 50
   70   jp = imax
   80   if (.not.(w(j,i).ne.zero)) go to 90
        call srotmg(scale(jp), scale(j), w(jp,i), w(j,i), sparam)
        w(j,i) = zero
        call srotm(np1-i, w(jp,ip1), mdw, w(j,ip1), mdw, sparam)
   90   j = jm1
  100 continue
      go to 140
  110 continue
      if (.not.(lend.gt.i)) go to 130
c
c     col i is dependent. swap with col lend.
      max = lend
c
c     perform-col-interchange
      assign 120 to igo993
      go to 560
  120 continue
      lend = lend - 1
c
c     find col in remaining set with largest ss.
      max = isamax(lend-i+1,h(i),1) + i - 1
      hbar = h(max)
      go to 30
  130 continue
      krank = i - 1
      go to 160
  140 i = ip1
      ip1 = ip1 + 1
      go to 10
  150 krank = l1
  160 continue
      krp1 = krank + 1
      if (.not.(krank.lt.me)) go to 290
      factor = alsq
      do 170 i=krp1,me
        if (l.gt.0) w(i,1) = zero
        call scopy(l, w(i,1), 0, w(i,1), mdw)
  170 continue
c
c     determine the rank of the remaining equality constraint
c     equations by eliminating within the block of constrained
c     variables.  remove any redundant constraints.
      lp1 = l + 1
      recalc = .true.
      lb = min0(l+me-krank,n)
      i = lp1
      ip1 = i + 1
  180 if (.not.(i.le.lb)) go to 280
      ir = krank + i - l
      lend = n
      mend = me
      assign 190 to igo996
      go to 460
c
c     update-col-ss-and-find-pivot-col
  190 assign 200 to igo993
      go to 560
c
c     perform-col-interchange
c
c     eliminate elements in the i-th col.
  200 j = me
  210 if (.not.(j.gt.ir)) go to 230
      jm1 = j - 1
      if (.not.(w(j,i).ne.zero)) go to 220
      call srotmg(scale(jm1), scale(j), w(jm1,i), w(j,i), sparam)
      w(j,i) = zero
      call srotm(np1-i, w(jm1,ip1), mdw, w(j,ip1), mdw, sparam)
  220 j = jm1
      go to 210
c
c     set ic=i=col being eliminated
  230 ic = i
      assign 240 to igo990
      go to 520
c
c     test-indep-of-incoming-col
  240 if (indep) go to 270
c
c     remove any redundant or dependent equality constraints.
      jj = ir
  250 if (.not.(ir.le.me)) go to 260
      w(ir,1) = zero
      call scopy(n, w(ir,1), 0, w(ir,1), mdw)
      rnorm = rnorm + (scale(ir)*w(ir,np1)/alsq)*w(ir,np1)
      w(ir,np1) = zero
      scale(ir) = one
c     reclassify the zeroed row as a least squares equation.
      itype(ir) = 1
      ir = ir + 1
      go to 250
c
c     reduce me to reflect any discovered dependent equality
c     constraints.
  260 continue
      me = jj - 1
      mep1 = me + 1
      go to 300
  270 i = ip1
      ip1 = ip1 + 1
      go to 180
  280 continue
  290 continue
  300 continue
      if (.not.(krank.lt.l1)) go to 420
c
c     try to determine the variables krank+1 through l1 from the
c     least squares equations.  continue the triangularization with
c     pivot element w(mep1,i).
c
      recalc = .true.
c
c     set factor=alsq to remove effect of heavy weight from
c     test for col independence.
      factor = alsq
      kk = krp1
      i = kk
      ip1 = i + 1
  310 if (.not.(i.le.l1)) go to 410
c
c     set ir to point to the mep1-st row.
      ir = mep1
      lend = l
      mend = m
      assign 320 to igo996
      go to 460
c
c     update-col-ss-and-find-pivot-col
  320 assign 330 to igo993
      go to 560
c
c     perform-col-interchange
c
c     eliminate i-th col below the ir-th element.
  330 irp1 = ir + 1
      j = m
      do 350 jj=irp1,m
        jm1 = j - 1
        if (.not.(w(j,i).ne.zero)) go to 340
        call srotmg(scale(jm1), scale(j), w(jm1,i), w(j,i), sparam)
        w(j,i) = zero
        call srotm(np1-i, w(jm1,ip1), mdw, w(j,ip1), mdw, sparam)
  340   j = jm1
  350 continue
c
c     test if new pivot element is near zero. if so, the col is
c     dependent.
      t = scale(ir)*w(ir,i)**2
      indep = t.gt.tau**2*eanorm**2
      if (.not.indep) go to 380
c
c     col test passed. now must pass row norm test to be classified
c     as independent.
      rn = zero
      do 370 i1=ir,m
        do 360 j1=ip1,n
          rn = amax1(rn,scale(i1)*w(i1,j1)**2)
  360   continue
  370 continue
      indep = t.gt.tau**2*rn
c
c     if independent, swap the ir-th and krp1-st rows to maintain the
c     triangular form.  update the rank indicator krank and the
c     equality constraint pointer me.
  380 if (.not.(indep)) go to 390
      call sswap(np1, w(krp1,1), mdw, w(ir,1), mdw)
      call sswap(1, scale(krp1), 1, scale(ir), 1)
c     reclassify the least sq. equation as an equality constraint and
c     rescale it.
      itype(ir) = 0
      t = sqrt(scale(krp1))
      call sscal(np1, t, w(krp1,1), mdw)
      scale(krp1) = alsq
      me = mep1
      mep1 = me + 1
      krank = krp1
      krp1 = krank + 1
      go to 400
  390 go to 430
  400 i = ip1
      ip1 = ip1 + 1
      go to 310
  410 continue
  420 continue
  430 continue
c
c     if pseudorank is less than l, apply householder trans.
c     from right.
      if (.not.(krank.lt.l)) go to 450
      do 440 i=1,krank
        j = krp1 - i
        call h12(1, j, krp1, l, w(j,1), mdw, h(j), w, mdw, 1, j-1)
  440 continue
  450 niv = krank + nsoln - l
      niv1 = niv + 1
      if (l.eq.n) done = .true.
c
c  end of initial triangularization.
      idope(1) = me
      idope(2) = mep1
      idope(3) = krank
      idope(4) = krp1
      idope(5) = nsoln
      idope(6) = niv
      idope(7) = niv1
      idope(8) = l1
      return
  460 continue
c
c     to update-col-ss-and-find-pivot-col
c
c     the col ss vector will be updated at each step. when
c     numerically necessary, these values will be recomputed.
c
      if (.not.(ir.ne.1 .and. (.not.recalc))) go to 480
c     update col ss =sum of squares.
      do 470 j=i,lend
        h(j) = h(j) - scale(ir-1)*w(ir-1,j)**2
  470 continue
c
c     test for numerical accuracy.
      max = isamax(lend-i+1,h(i),1) + i - 1
      recalc = hbar + tenm3*h(max).eq.hbar
c
c     if required, recalculate col ss, using rows ir through mend.
  480 if (.not.(recalc)) go to 510
      do 500 j=i,lend
        h(j) = zero
        do 490 k=ir,mend
          h(j) = h(j) + scale(k)*w(k,j)**2
  490   continue
  500 continue
c
c     find col with largest ss.
      max = isamax(lend-i+1,h(i),1) + i - 1
      hbar = h(max)
  510 go to 600
  520 continue
c
c     to test-indep-of-incoming-col
c
c     test the col ic to determine if it is linearly independent
c     of the cols already in the basis.  in the init tri
c     step, we usually want the heavy weight alamda to
c     be included in the test for independence.  in this case the
c     value of factor will have been set to 1.e0 before this
c     procedure is invoked.  in the potentially rank deficient
c     problem, the value of factor will have been
c     set to alsq=alamda**2 to remove the effect of the heavy weight
c     from the test for independence.
c
c     write new col as partitioned vector
c             (a1)  number of components in soln so far = niv
c             (a2)  m-niv components
c     and compute  sn = inverse weighted length of a1
c                  rn = inverse weighted length of a2
c     call the col independent when rn .gt. tau*sn
      sn = zero
      rn = zero
      do 550 j=1,mend
        t = scale(j)
        if (j.le.me) t = t/factor
        t = t*w(j,ic)**2
        if (.not.(j.lt.ir)) go to 530
        sn = sn + t
        go to 540
  530   rn = rn + t
  540   continue
  550 continue
      indep = rn.gt.tau**2*sn
      go to 590
  560 continue
c
c     to perform-col-interchange
c
      if (.not.(max.ne.i)) go to 570
c     exchange elements of permuted index vector and perform col
c     interchanges.
      itemp = ipivot(i)
      ipivot(i) = ipivot(max)
      ipivot(max) = itemp
      call sswap(m, w(1,max), 1, w(1,i), 1)
      t = h(max)
      h(max) = h(i)
      h(i) = t
  570 go to 580
  580 go to igo993, (30, 200, 330, 120)
  590 go to igo990, (40, 240)
  600 go to igo996, (20, 190, 320)
      end
