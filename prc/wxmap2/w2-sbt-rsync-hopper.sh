#!/bin/bash

rsync -aluv --exclude "*.dat" mfiorino@hopper1.orc.gmu.edu://scratch/mfiorino/dat/sbt-v03/ /ssd2/w22/dat/sbt-v03/
rsync -aluv mfiorino@hopper1.orc.gmu.edu://scratch/mfiorino/dat/sbt-v03/ /ssd2/w22/dat/sbt-v03/
