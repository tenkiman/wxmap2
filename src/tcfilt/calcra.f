       subroutine calcra(ro,rtan,iang,dist)
       parameter ( nmx=24)
       parameter (imx=201 , jmx=81)
       common /winds/ dmmm(imx,jmx,2),tang(imx,jmx),
     *      del(imx,jmx),tha(imx,jmx),xf(imx,jmx),ds(imx,jmx)
c
       common  /total/ ddel,dtha
       common  /coor/ xv,yv,xold,yold,xcorn,ycorn,factr,id1,id2
c
          pi = 4.*atan(1.0)
       pi180 = 4.*atan(1.0)/180.
       fact =  cos(yold)
c
       dx=ddel/pi180
       dy=dtha/pi180
       xc = (xold-xcorn)*dx
       yc = (yold-ycorn)*dy

c
        theta= 2.*pi*float(iang-1)/float(nmx)
        x=ro/fact*cos(theta)+xc
        y=ro*sin(theta)+yc
        ix=int(x/dx)
        iy=int(y/dy)
        ix1=ix+1
        iy1=iy+1
        p=x/dx-float(ix)
        q=y/dy-float(iy)
       rtan=(1.-p)*(1.-q)*xf(ix,iy) +(1.-p)*q*xf(ix,iy+1)
     1      +  (1.-q)*p*xf(ix+1,iy) + p*q*xf(ix+1,iy+1)
10     continue
c
c
         return
         end
