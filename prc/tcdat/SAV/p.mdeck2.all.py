#!/usr/bin/env python

from M import *

years=[2006,2007]
years=[2006,2007,2008,2009,2010]
years=[2007,2008,2009]
years=[2003,2004]
years=[2001,2002]
years=[2005]
years=[2005,2006,2007,2008,2009,2010]
years=[2001,2002,2003,2004]
years=[2007,2008,2009]
years=[2010]
years=[2011]
years=[2007,2008,2009,2010,2011]
years=[2001,2002,2003,2004,2005,2006]
years=[2007,2008]
years=[2005,2006]

years=[2007,2008]
years=[2000,2001,2002,2003,2004,2005,2006]
years=[2001,2002,2003,2004,2005,2006]
years=[2007,2008,2009,2010,2011]

years=[2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011]
years=[2007,2008]
years=[2000,2001,2002,2003,2004,2005,2006]
years=[2009,2010,2011]
years=[2011]
years=[2008,2009,2010]
years=[2010]
years=[2006,2007,2008,2009]

years=[2009]
md2tagopt='-t tcc07-09'

years=[2011]
years=[1974,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010]
years=[2009]
years=[2011]


years=range(2000,2011)
md2tagopt='-t 00-10'

years=[2007,2008,2009,2010,2011]
md2tagopt=''

# -- for cur mdeck2 just do two years
#

years=[2008,2009,2010,2011]
years=[2009,2010,2011,2012]
years=[2011]
years=[2009,2010]
years=[2012]

# -- 2010s
years=[2010,2011,2012]
md2tagopt='10-12'
md2tagopt='10-12'
# -- on kaze
years=[2012]
# -- on kishou
years=[2012]
md2tagopt=''
bypasstcc=1
# -- update 2008 got final bdecks from nhc using -a
#
years=[2008]
md2tagopt='00-10'

# -- on kishou
years=[2013]
md2tagopt=''

# -- update on kishou
md2tagopt='79-99'
years=range(1979,2000)

# 20130402 -- messed it up on kaze; update realtime on kishou
#
# -- update on kishou
years=[2012,2013]
#years=[2013]
md2tagopt=''

# -- older data  -- mods to tcbase TcData()
#
md2tagopt='49-70'
years=range(1949,1970)

md2tagopt='69-79'
years=range(1969,1980)

md2tagopt='79-99'
years=range(1979,2000)

years=[2010,2011,2012]
md2tagopt='10-12'

bypasstcc=1
basins=['l','e','c','w','i','s','q']
tccbasins=['lant','epac','wpac','nio','sio','spac']
ropt='norun'

# now use -Y mechanism, e.g,
# -- 20140908 -- redo because format changed...
# -- 20141103 -- bug in selecting jt v nhc in overlap basins -- only do if current year! (working best track)
#
#md2 -y 2010.2013 -Y -t 10-13 -r
#md2 -y 2014 -Y -t 10-13 -b s -r
#md2 -y 2000.2009 -Y -t 00-09 -r
#md2 -y 2010 -Y -t 00-09 -r -b s
#md2 -y 1990.1999 -Y -t 90-99 -r
#md2 -y 2000 -Y -t 90-99 -r -b s
#md2 -y 1980.1989 -Y -t 80-89 -r
#md2 -y 1990 -Y -t 80-89 -r -b s
#md2 -y 1970.1979 -Y -t 70-79 -r
#md2 -y 1980 -Y -t 70-79 -r -b s
#md2 -y 1960.1969 -Y -t 60-69 -r
#md2 -y 1948.1959 -Y -t 48-59 -r

#md2 -y 1969.1980 -Y -t 69-79 -r
#md2 -y 1949.1970 -Y -t 49-70 -r

years=range(2009,2015)

ropt='norun'
ropt=''

for year in years:
    cmd="w2-tc-dss-md2.py -y %s -Y -t %s -r"%(year,year)
    mf.runcmd(cmd,ropt)


sys.exit()




for year in years:

    # -- 20111016 - something wrong with netcdf lib?  no; undef for lat != undef in file?  for some reasons?
    # fixed w2.tc.tcc.py
    #
    dotcc=0
    if(year >= 2007 and year <= 2009 and not(bypasstcc)): dotcc=1


    if(dotcc):
        for tccbasin in tccbasins:
            if(tcbasin == 'wpac'  and md2tag == ''): md2tag="%s -Z"%(md2tag)
            cmd="../tctcc/w2.tc.tcc.py %s %s %s"%(year,tccbasin,md2tag)
            mf.runcmd(cmd,ropt)

    for basin in basins:
        md2tag=''
        if(md2tagopt != ''):
            md2tag='-t %s'%(md2tagopt)

        # for 2012 nhem	force use of zipfiles
        #

        zipopt=''
        if( (basin == 'w' or basin == 'e' or basin == 'i' or
             basin == 'c' or basin == 'l')
            and year >= 2012): zipopt='-Z'

        if( year >= 2012): zipopt='-Z'

        if(year >= 1999):
            if(zipopt != ''):
                cmd="w2-tc-dss-md2.py -S 90-99%s.%d %s -U"%(basin,year,md2tag)
                mf.runcmd(cmd,ropt)   

            cmd="w2-tc-dss-md2.py -S 90-99%s.%d %s %s"%(basin,year,md2tag,zipopt)
            mf.runcmd(cmd,ropt)

        cmd="w2-tc-dss-md2.py -S %s.%d %s"%(basin,year,md2tag)
        mf.runcmd(cmd,ropt)




# -- make inventory
#cmd="w2-tc-dss-md2.py -k"
#mf.runcmd(cmd,ropt)
