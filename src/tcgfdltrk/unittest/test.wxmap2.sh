#!/bin/sh

echo 'run in tracker mode...'

time ../gettrk_genN.x < namelist.tctrk.1.5.6
echo 'do comp'
meld fort.64 fort.64.tracker.gfortan.linux

echo 'run in genesis mode...'
time ../gettrk_genN.x < namelist.tcgen.lant.1.5.6

meld fort.64 fort.64.tcgen.lant.gfortan.linux

