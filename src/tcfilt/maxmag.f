      function maxmag(a,length)
cc
cc*********************************************************************
cc                                                                    *
cc   this function obtains the index (or location)  of the maximum    *
cc   or minimum value of an array                                     *
cc                                                                    *
cc*********************************************************************
cc                                                                    *
cc
ccc       function returns zero origin index!!!!!
      dimension a(length)
       htemp=-1.e30
       do 10 i=1,length
       if(a(i).gt.htemp) ib=i
       if(a(i).gt.htemp) htemp=a(i)
 10    continue
       maxmag=ib-1
       return
       entry minmag(a,length)
       htemp=1.e30
       do 11 i=1,length
       if(a(i).lt.htemp) ib=i
       if(a(i).lt.htemp) htemp=a(i)
11     continue
       minmag=ib-1
       return
      entry minval(a,length)
       htemp=1.e30
       do 20 i=1,length
       if(a(i).lt.htemp) ib=i
       if(a(i).lt.htemp) htemp=a(i)
 20    continue
       minval=ib-1
       return
       entry maxval(a,length)
       htemp=-1.e30
       do 21 i=1,length
       if(a(i).gt.htemp) ib=i
       if(a(i).gt.htemp) htemp=a(i)
21     continue
       maxval=ib-1
      return
      end
