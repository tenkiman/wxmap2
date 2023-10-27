      subroutine wnlsm(w,mdw,mme,ma,n,l,prgopt,x,rnorm,mode,ipivot,
     1   itype,wd,h,scale,z,temp,d)
c***begin prologue  wnlsm
c***refer to  wnnls
c
c     this is a companion subprogram to wnnls( ).
c     the documentation for wnnls( ) has more complete
c     usage instructions.
c
c     written by karen h. haskell, sandia laboratories,
c     with the help of r.j. hanson, sandia laboratories,
c     december 1976 - january 1978.
c     revised march 4, 1982.
c
c     in addition to the parameters discussed in the prologue to
c     subroutine wnnls, the following work arrays are used in
c     subroutine wnlsm  (they are passed through the calling
c     sequence from wnnls for purposes of variable dimensioning).
c     their contents will in general be of no interest to the user.
c
c         ipivot(*)
c            an array of length n.  upon completion it contains the
c         pivoting information for the cols of w(*,*).
c
c         itype(*)
c            an array of length m which is used to keep track
c         of the classification of the equations.  itype(i)=0
c         denotes equation i as an equality constraint.
c         itype(i)=1 denotes equation i as a least squares
c         equation.
c
c         wd(*)
c            an array of length n.  upon completion it contains the
c         dual solution vector.
c
c         h(*)
c            an array of length n.  upon completion it contains the
c         pivot scalars of the householder transformations performed
c         in the case krank.lt.l.
c
c         scale(*)
c            an array of length m which is used by the subroutine
c         to store the diagonal matrix of weights.
c         these are used to apply the modified givens
c         transformations.
c
c         z(*),temp(*)
c            working arrays of length n.
c
c         d(*)
c            an array of length n that contains the
c         column scaling for the matrix (e).
c                                       (a)
c***routines called  h12,isamax,sasum,saxpy,scopy,snrm2,srotm,srotmg,
c                    sscal,sswap,wnlit,xerror
c***end prologue  wnlsm
c
c     the editing required to convert this subroutine from single to
c     double precision involves the following character string changes.
c     use an editing command (change) /string-1/(to)string-2/.
c     (begin changes at line with c++ in cols. 1-3.)
c     /real (12 blanks)/double precision/,/sasum/dasum/,/srotmg/drotmg/,
c     /snrm2/dnrm2/,/ sqrt/ dsqrt/,/srotm/drotm/,/amax1/dmax1/,
c     /scopy/dcopy/,/sscal/dscal/,/saxpy/daxpy/,/e0/d0/,/sswap/dswap/,
c     /isamax/idamax/,/srelpr/drelpr/
c
c     subroutine wnlsm (w,mdw,mme,ma,n,l,prgopt,x,rnorm,mode,
c    1                  ipivot,itype,wd,h,scale,z,temp,d)
c++
      real             w(mdw,1), x(1), wd(1), h(1), scale(1), dope(4)
      real             z(1), temp(1), prgopt(1), d(1), sparam(5)
      real             alamda, alpha, alsq, amax, bnorm, eanorm
      real             srelpr, fac, one, blowup
      real             rnorm, sm, t, tau, two, wmax, zero, zz, z2
      real             amax1, sqrt, snrm2, sasum
      integer ipivot(1), itype(1), isamax, idope(8)
      logical hitcon, feasbl, done, pos
      data zero /0.e0/, one /1.e0/, two /2.e0/, srelpr /0.e0/
c
c     initialize-variables
c***first executable statement  wnlsm
      assign 10 to igo998
      go to 180
c
c     perform initial triangularization in the submatrix
c     corresponding to the unconstrained variables using
c     the procedure initially-triangularize.
   10 assign 20 to igo995
      go to 280
c
c     perform wnnls algorithm using the following steps.
c
c     until(done)
c
c        compute-search-direction-and-feasible-point
c
c        when (hitcon) add-constraints
c
c        else perform-multiplier-test-and-drop-a-constraint
c
c        fin
c
c     compute-final-solution
c
   20 if (done) go to 80
c
      assign 30 to igo991
      go to 300
c
c     compute-search-direction-and-feasible-point
c
   30 if (.not.(hitcon)) go to 50
      assign 40 to igo986
      go to 370
   40 go to 70
c
c     when (hitcon) add-constraints
c
   50 assign 60 to igo983
      go to 640
   60 continue
c
c     else perform-multiplier-test-and-drop-a-constraint
c
   70 go to 20
c
   80 assign 90 to igo980
      go to 1000
c
c     compute-final-solution
c
   90 return
  100 continue
c
c     to process-option-vector
      fac = 1.e-4
c
c     the nominal tolerance used in the code,
      tau = sqrt(srelpr)
c
c     the nominal blow-up factor used in the code.
      blowup = tau
c
c     the nominal column scaling used in the code is
c     the identity scaling.
      d(1) = one
      call scopy(n, d, 0, d, 1)
c
c     define bound for number of options to change.
      nopt = 1000
c
c     define bound for positive value of link.
      nlink = 100000
      ntimes = 0
      last = 1
      link = prgopt(1)
      if (.not.(link.le.0 .or. link.gt.nlink)) go to 110
      nerr = 3
      iopt = 1
      call xerror( 'wnnls( ) the option vector is undefined', 39, nerr,
     1 iopt)
      mode = 2
      return
  110 if (.not.(link.gt.1)) go to 160
      ntimes = ntimes + 1
      if (.not.(ntimes.gt.nopt)) go to 120
      nerr = 3
      iopt = 1
      call xerror( 'wnnls( ). the links in the option vector are cycling
     1.', 53,     nerr, iopt)
      mode = 2
      return
  120 key = prgopt(last+1)
      if (.not.(key.eq.6 .and. prgopt(last+2).ne.zero)) go to 140
      do 130 j=1,n
        t = snrm2(m,w(1,j),1)
        if (t.ne.zero) t = one/t
        d(j) = t
  130 continue
  140 if (key.eq.7) call scopy(n, prgopt(last+2), 1, d, 1)
      if (key.eq.8) tau = amax1(srelpr,prgopt(last+2))
      if (key.eq.9) blowup = amax1(srelpr,prgopt(last+2))
      next = prgopt(link)
      if (.not.(next.le.0 .or. next.gt.nlink)) go to 150
      nerr = 3
      iopt = 1
      call xerror( 'wnnls( ) the option vector is undefined', 39, nerr,
     1 iopt)
      mode = 2
      return
  150 last = link
      link = next
      go to 110
  160 do 170 j=1,n
        call sscal(m, d(j), w(1,j), 1)
  170 continue
      go to 1260
  180 continue
c
c     to initialize-variables
c
c     srelpr is the precision for the particular machine
c     being used.  this logic avoids recomputing it every entry.
      if (.not.(srelpr.eq.zero)) go to 210
c*** changed back by bross
c*** changed by rf boisvert, 19-feb-92  (fails on hp 9000 series 300)
cross      srelpr = r1mach(4)
       srelpr = one
  190 if (one+srelpr.eq.one) go to 200
       srelpr = srelpr/two
       go to 190
  200 srelpr = srelpr*two
cross
  210 m = ma + mme
      me = mme
      mep1 = me + 1
      assign 220 to igo977
      go to 100
c
c     process-option-vector
  220 done = .false.
      iter = 0
      itmax = 3*(n-l)
      mode = 0
      lp1 = l + 1
      nsoln = l
      nsp1 = nsoln + 1
      np1 = n + 1
      nm1 = n - 1
      l1 = min0(m,l)
c
c     compute scale factor to apply to equal. constraint equas.
      do 230 j=1,n
        wd(j) = sasum(m,w(1,j),1)
  230 continue
      imax = isamax(n,wd,1)
      eanorm = wd(imax)
      bnorm = sasum(m,w(1,np1),1)
      alamda = eanorm/(srelpr*fac)
c
c     define scaling diag matrix for mod givens usage and
c     classify equation types.
      alsq = alamda**2
      do 260 i=1,m
c
c     when equ i is heavily weighted itype(i)=0, else itype(i)=1.
        if (.not.(i.le.me)) go to 240
        t = alsq
        itemp = 0
        go to 250
  240   t = one
        itemp = 1
  250   scale(i) = t
        itype(i) = itemp
  260 continue
c
c     set the soln vector x(*) to zero and the col interchange
c     matrix to the identity.
      x(1) = zero
      call scopy(n, x, 0, x, 1)
      do 270 i=1,n
        ipivot(i) = i
  270 continue
      go to 1230
  280 continue
c
c     to initially-triangularize
c
c     set first l comps. of dual vector to zero because
c     these correspond to the unconstrained variables.
      if (.not.(l.gt.0)) go to 290
      wd(1) = zero
      call scopy(l, wd, 0, wd, 1)
c
c     the arrays idope(*) and dope(*) are used to pass
c     information to wnlit().  this was done to avoid
c     a long calling sequence or the use of common.
  290 idope(1) = me
      idope(2) = mep1
      idope(3) = 0
      idope(4) = 1
      idope(5) = nsoln
      idope(6) = 0
      idope(7) = 1
      idope(8) = l1
c
      dope(1) = alsq
      dope(2) = eanorm
      dope(3) = fac
      dope(4) = tau
      call wnlit(w, mdw, m, n, l, ipivot, itype, h, scale, rnorm,
     1 idope, dope, done)
      me = idope(1)
      mep1 = idope(2)
      krank = idope(3)
      krp1 = idope(4)
      nsoln = idope(5)
      niv = idope(6)
      niv1 = idope(7)
      l1 = idope(8)
      go to 1240
  300 continue
c
c     to compute-search-direction-and-feasible-point
c
c     solve the triangular system of currently non-active
c     variables and store the solution in z(*).
c
c     solve-system
      assign 310 to igo958
      go to 1110
c
c     increment iteration counter and check against max. number
c     of iterations.
  310 iter = iter + 1
      if (.not.(iter.gt.itmax)) go to 320
      mode = 1
      done = .true.
c
c     check to see if any constraints have become active.
c     if so, calculate an interpolation factor so that all
c     active constraints are removed from the basis.
  320 alpha = two
      hitcon = .false.
      if (.not.(l.lt.nsoln)) go to 360
      do 350 j=lp1,nsoln
        zz = z(j)
        if (.not.(zz.le.zero)) go to 340
        t = x(j)/(x(j)-zz)
        if (.not.(t.lt.alpha)) go to 330
        alpha = t
        jcon = j
  330   hitcon = .true.
  340   continue
  350 continue
  360 go to 1220
  370 continue
c
c     to add-constraints
c
c     use computed alpha to interpolate between last
c     feasible solution x(*) and current unconstrained
c     (and infeasible) solution z(*).
      if (.not.(lp1.le.nsoln)) go to 390
      do 380 j=lp1,nsoln
        x(j) = x(j) + alpha*(z(j)-x(j))
  380 continue
  390 feasbl = .false.
      go to 410
  400 if (feasbl) go to 610
c
c     remove col jcon and shift cols jcon+1 through n to the
c     left. swap col jcon into the n-th position.  this achieves
c     upper hessenberg form for the nonactive constraints and
c     leaves an upper hessenberg matrix to retriangularize.
  410 do 420 i=1,m
        t = w(i,jcon)
        call scopy(n-jcon, w(i,jcon+1), mdw, w(i,jcon), mdw)
        w(i,n) = t
  420 continue
c
c     update permuted index vector to reflect this shift and swap.
      itemp = ipivot(jcon)
      if (.not.(jcon.lt.n)) go to 440
      do 430 i=jcon,nm1
        ipivot(i) = ipivot(i+1)
  430 continue
  440 ipivot(n) = itemp
c
c     similarly repermute x(*) vector.
      call scopy(n-jcon, x(jcon+1), 1, x(jcon), 1)
      x(n) = zero
      nsp1 = nsoln
      nsoln = nsoln - 1
      niv1 = niv
      niv = niv - 1
c
c     retriangularize upper hessenberg matrix after adding constraints.
      j = jcon
      i = krank + jcon - l
  450 if (.not.(j.le.nsoln)) go to 570
      if (.not.(itype(i).eq.0 .and. itype(i+1).eq.0)) go to 470
      assign 460 to igo938
      go to 620
c
c     (itype(i).eq.0 .and. itype(i+1).eq.0) zero-ip1-to-i-in-col-j
  460 go to 560
  470 if (.not.(itype(i).eq.1 .and. itype(i+1).eq.1)) go to 490
      assign 480 to igo938
      go to 620
c
c     (itype(i).eq.1 .and. itype(i+1).eq.1) zero-ip1-to-i-in-col-j
  480 go to 560
  490 if (.not.(itype(i).eq.1 .and. itype(i+1).eq.0)) go to 510
      call sswap(np1, w(i,1), mdw, w(i+1,1), mdw)
      call sswap(1, scale(i), 1, scale(i+1), 1)
      itemp = itype(i+1)
      itype(i+1) = itype(i)
      itype(i) = itemp
c
c     swapped row was formerly a pivot elt., so it will
c     be large enough to perform elim.
      assign 500 to igo938
      go to 620
c
c     zero-ip1-to-i-in-col-j
  500 go to 560
  510 if (.not.(itype(i).eq.0 .and. itype(i+1).eq.1)) go to 550
      t = scale(i)*w(i,j)**2/alsq
      if (.not.(t.gt.tau**2*eanorm**2)) go to 530
      assign 520 to igo938
      go to 620
  520 go to 540
  530 call sswap(np1, w(i,1), mdw, w(i+1,1), mdw)
      call sswap(1, scale(i), 1, scale(i+1), 1)
      itemp = itype(i+1)
      itype(i+1) = itype(i)
      itype(i) = itemp
      w(i+1,j) = zero
  540 continue
  550 continue
  560 i = i + 1
      j = j + 1
      go to 450
c
c     see if the remaining coeffs in the soln set are feasible.  they
c     should be because of the way alpha was determined.  if any are
c     infeasible it is due to roundoff error.  any that are non-
c     positive will be set to zero and removed from the soln set.
  570 if (.not.(lp1.le.nsoln)) go to 590
      do 580 jcon=lp1,nsoln
        if (x(jcon).le.zero) go to 600
  580 continue
  590 feasbl = .true.
  600 continue
      go to 400
  610 go to 1200
  620 continue
c
c     to zero-ip1-to-i-in-col-j
      if (.not.(w(i+1,j).ne.zero)) go to 630
      call srotmg(scale(i), scale(i+1), w(i,j), w(i+1,j), sparam)
      w(i+1,j) = zero
      call srotm(np1-j, w(i,j+1), mdw, w(i+1,j+1), mdw, sparam)
  630 go to 1290
  640 continue
c
c     to perform-multiplier-test-and-drop-a-constraint
      call scopy(nsoln, z, 1, x, 1)
      if (.not.(nsoln.lt.n)) go to 650
      x(nsp1) = zero
      call scopy(n-nsoln, x(nsp1), 0, x(nsp1), 1)
  650 i = niv1
  660 if (.not.(i.le.me)) go to 690
c
c     reclassify least squares eqations as equalities as
c     necessary.
      if (.not.(itype(i).eq.0)) go to 670
      i = i + 1
      go to 680
  670 call sswap(np1, w(i,1), mdw, w(me,1), mdw)
      call sswap(1, scale(i), 1, scale(me), 1)
      itemp = itype(i)
      itype(i) = itype(me)
      itype(me) = itemp
      mep1 = me
      me = me - 1
  680 go to 660
c
c     form inner product vector wd(*) of dual coeffs.
  690 if (.not.(nsp1.le.n)) go to 730
      do 720 j=nsp1,n
        sm = zero
        if (.not.(nsoln.lt.m)) go to 710
        do 700 i=nsp1,m
          sm = sm + scale(i)*w(i,j)*w(i,np1)
  700   continue
  710   wd(j) = sm
  720 continue
  730 go to 750
  740 if (pos .or. done) go to 970
c
c     find j such that wd(j)=wmax is maximum.  this determines
c     that the incoming col j will reduce the residual vector
c     and be positive.
  750 wmax = zero
      iwmax = nsp1
      if (.not.(nsp1.le.n)) go to 780
      do 770 j=nsp1,n
        if (.not.(wd(j).gt.wmax)) go to 760
        wmax = wd(j)
        iwmax = j
  760   continue
  770 continue
  780 if (.not.(wmax.le.zero)) go to 790
      done = .true.
      go to 960
c
c     set dual coeff to zero for incoming col.
  790 wd(iwmax) = zero
c
c     wmax .gt. zero, so okay to move col iwmax to soln set.
c     perform transformation to retriangularize, and test
c     for near linear dependence.
c     swap col iwmax into nsoln-th position to maintain upper
c     hessenberg form of adjacent cols, and add new col to
c     triangular decomposition.
      nsoln = nsp1
      nsp1 = nsoln + 1
      niv = niv1
      niv1 = niv + 1
      if (.not.(nsoln.ne.iwmax)) go to 800
      call sswap(m, w(1,nsoln), 1, w(1,iwmax), 1)
      wd(iwmax) = wd(nsoln)
      wd(nsoln) = zero
      itemp = ipivot(nsoln)
      ipivot(nsoln) = ipivot(iwmax)
      ipivot(iwmax) = itemp
c
c     reduce col nsoln so that the matrix of nonactive
c     constraints variables is triangular.
  800 j = m
  810 if (.not.(j.gt.niv)) go to 870
      jm1 = j - 1
      jp = jm1
c
c     when operating near the me line, test to see if the pivot elt.
c     is near zero.  if so, use the largest elt. above it as the pivot.
c     this is to maintain the sharp interface between weighted and
c     non-weighted rows in all cases.
      if (.not.(j.eq.mep1)) go to 850
      imax = me
      amax = scale(me)*w(me,nsoln)**2
  820 if (.not.(jp.ge.niv)) go to 840
      t = scale(jp)*w(jp,nsoln)**2
      if (.not.(t.gt.amax)) go to 830
      imax = jp
      amax = t
  830 jp = jp - 1
      go to 820
  840 jp = imax
  850 if (.not.(w(j,nsoln).ne.zero)) go to 860
      call srotmg(scale(jp), scale(j), w(jp,nsoln), w(j,nsoln), sparam)
      w(j,nsoln) = zero
      call srotm(np1-nsoln, w(jp,nsp1), mdw, w(j,nsp1), mdw, sparam)
  860 j = jm1
      go to 810
c
c     solve for z(nsoln)=proposed new value for x(nsoln).
c     test if this is nonpositive or too large.
c     if this was true or if the pivot term was zero reject
c     the col as dependent.
  870 if (.not.(w(niv,nsoln).ne.zero)) go to 890
      isol = niv
      assign 880 to igo897
      go to 980
c
c     test-proposed-new-component
  880 go to 940
  890 if (.not.(niv.le.me .and. w(mep1,nsoln).ne.zero)) go to 920
c
c     try to add row mep1 as an additional equality constraint.
c     check size of proposed new soln component.
c     reject it if it is too large.
      isol = mep1
      assign 900 to igo897
      go to 980
c
c     test-proposed-new-component
  900 if (.not.(pos)) go to 910
c
c     swap rows mep1 and niv, and scale factors for these rows.
      call sswap(np1, w(mep1,1), mdw, w(niv,1), mdw)
      call sswap(1, scale(mep1), 1, scale(niv), 1)
      itemp = itype(mep1)
      itype(mep1) = itype(niv)
      itype(niv) = itemp
      me = mep1
      mep1 = me + 1
  910 go to 930
  920 pos = .false.
  930 continue
  940 if (pos) go to 950
      nsp1 = nsoln
      nsoln = nsoln - 1
      niv1 = niv
      niv = niv - 1
  950 continue
  960 go to 740
  970 go to 1250
  980 continue
c
c     to test-proposed-new-component
      z2 = w(isol,np1)/w(isol,nsoln)
      z(nsoln) = z2
      pos = z2.gt.zero
      if (.not.(z2*eanorm.ge.bnorm .and. pos)) go to 990
      pos = .not.(blowup*z2*eanorm.ge.bnorm)
  990 go to 1280
 1000 continue
c     to compute-final-solution
c
c     solve system, store results in x(*).
c
      assign 1010 to igo958
      go to 1110
c     solve-system
 1010 call scopy(nsoln, z, 1, x, 1)
c
c     apply householder transformations to x(*) if krank.lt.l
      if (.not.(0.lt.krank .and. krank.lt.l)) go to 1030
      do 1020 i=1,krank
        call h12(2, i, krp1, l, w(i,1), mdw, h(i), x, 1, 1, 1)
 1020 continue
c
c     fill in trailing zeroes for constrained variables not in soln.
 1030 if (.not.(nsoln.lt.n)) go to 1040
      x(nsp1) = zero
      call scopy(n-nsoln, x(nsp1), 0, x(nsp1), 1)
c
c     repermute soln vector to natural order.
 1040 do 1070 i=1,n
        j = i
 1050   if (ipivot(j).eq.i) go to 1060
        j = j + 1
        go to 1050
 1060   ipivot(j) = ipivot(i)
        ipivot(i) = j
        call sswap(1, x(j), 1, x(i), 1)
 1070 continue
c
c     rescale the soln using the col scaling.
      do 1080 j=1,n
        x(j) = x(j)*d(j)
 1080 continue
      if (.not.(nsoln.lt.m)) go to 1100
      do 1090 i=nsp1,m
        t = w(i,np1)
        if (i.le.me) t = t/alamda
        t = (scale(i)*t)*t
        rnorm = rnorm + t
 1090 continue
 1100 rnorm = sqrt(rnorm)
      go to 1210
c
c     to solve-system
c
 1110 continue
      if (.not.(done)) go to 1120
      isol = 1
      go to 1130
 1120 isol = lp1
 1130 if (.not.(nsoln.ge.isol)) go to 1190
c
c     copy rt. hand side into temp vector to use overwriting method.
      call scopy(niv, w(1,np1), 1, temp, 1)
      do 1180 jj=isol,nsoln
        j = nsoln - jj + isol
        if (.not.(j.gt.krank)) go to 1140
        i = niv - jj + isol
        go to 1150
 1140   i = j
 1150   if (.not.(j.gt.krank .and. j.le.l)) go to 1160
        z(j) = zero
        go to 1170
 1160   z(j) = temp(i)/w(i,j)
        call saxpy(i-1, -z(j), w(1,j), 1, temp, 1)
 1170   continue
 1180 continue
 1190 go to 1270
 1200 go to igo986, (40)
 1210 go to igo980, (90)
 1220 go to igo991, (30)
 1230 go to igo998, (10)
 1240 go to igo995, (20)
 1250 go to igo983, (60)
 1260 go to igo977, (220)
 1270 go to igo958, (310, 1010)
 1280 go to igo897, (880, 900)
 1290 go to igo938, (460, 480, 500, 520)
      end
