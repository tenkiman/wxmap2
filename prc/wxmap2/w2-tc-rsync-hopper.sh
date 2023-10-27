#!/bin/bash

time rsync -aluv --timeout=120 mfiorino@hopper1.orc.gmu.edu:/scratch/mfiorino/dat/tc/ /ssd2/w22/dat/tc/

#rsync -alv --exclude "*.dat" mfiorino@hopper1.orc.gmu.edu://scratch/mfiorino/dat/sbt-v03/ /ssd2/w22/dat/sbt-v03/
#rsync -alv mfiorino@hopper1.orc.gmu.edu://scratch/mfiorino/dat/sbt-v03/ /ssd2/w22/dat/sbt-v03/
