#!/bin/sh

echo 'run in tracker mode...'

time ../gettrk_genN.x < namelist.tctrk.1.5.6
echo 'do comp'
/Applications/xxdiff.app/Contents/MacOS/xxdiff fort.64 fort.64.tracker.gfortan.macos
cp fort.64 fort.64.tracker.gfortan.macos-201311

echo 'run in genesis mode...'
time ../gettrk_genN.x < namelist.tcgen.lant.1.5.6

diff fort.64 fort.64.tcgen.lant.gfortan.macos
cp fort.64 fort.64.tcgen.lant.gfortan.macos-201311

