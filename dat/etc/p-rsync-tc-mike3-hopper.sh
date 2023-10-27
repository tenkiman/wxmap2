#!/bin/bash

rsync -alv --exclude="*.grb*"  /w21/dat/tc/ mfiorino@hopper1.orc.gmu.edu://scratch/mfiorino/dat/tc/

