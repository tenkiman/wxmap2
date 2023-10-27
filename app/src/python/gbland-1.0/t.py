#!/usr/bin/env python

import gbland as gb

def run():

	for lat in range(-90,90,10):
		for lon in range(0,360,25):
			dist=gb.latlon2land(lat,lon)
			print 'lat/lon: %5.1f/%6.1f d2l: %6.0f'%(lat,lon,dist)

if __name__=='__main__':
    run()

