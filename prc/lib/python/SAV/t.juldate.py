#!/usr/bin/env python
"""Returns the Julian day number of a date."""

import mf


dtg='1983080500'

jday=mf.Dtg2JulianDay(dtg)
print 'dtg: ',dtg,' jday: ',jday
year=dtg[0:4]
ymd=mf.YearJulianDay2YMD(year,jday)

print 'ymd ',ymd
