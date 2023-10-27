      subroutine wndspd(rcomp,tcomp,wc,mr,mt,mp,nr,nt,np,rmiss)
c     The routine calculates the magnitude of the wind based on the
c     radial and tangential components of the wind.
c
      dimension rcomp(0:mr,0:mt,0:mp),tcomp(0:mr,0:mt,0:mp),
     +          wc(0:mr,0:mt,0:mp)
c
c
      do kk=0,np
      do jj=0,nt
      do ii=0,nr
         if ((rcomp(ii,jj,kk) .le. rmiss) .or.
     +       (tcomp(ii,jj,kk) .le. rmiss)) then
            wc(ii,jj,kk) = rmiss
         else
            wc(ii,jj,kk) = sqrt(  rcomp(ii,jj,kk)*rcomp(ii,jj,kk)
     +                       + tcomp(ii,jj,kk)*tcomp(ii,jj,kk) )
         endif
      enddo
      enddo
      enddo

      return
      end

