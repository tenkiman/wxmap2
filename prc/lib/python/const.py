"""
basic constants and settings

"""
from math import atan2
pi=4.0*atan2(1.0,1.0)
pi4=pi/4.0
pi2=pi/2.0

deg2rad=pi/180.0
rad2deg=1.0/deg2rad

# -- earth ~ flattened sheriod r=6335.4 -> 6399.6 km
# this values is mean GC distance
#
rearth=6371.0

km2nm=60.0/(2*pi*rearth/360.0)
nm2km=1.0/km2nm
deglat2km=((2.0*pi*rearth)/360.0)
deglat2nm=60.0
knots2ms=1000.0/(km2nm*3600.0)
ms2knots=1.0/knots2ms

# -- units 
#
tcunits='metric'
tcunits='english'

# -- epsilon
#
epsilon=1e-10
epsilonm5=1.0e-5

# --- wmo gravity
#
gravity=9.80665
