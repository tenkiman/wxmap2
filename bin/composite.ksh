#!/bin/ksh 

#print  "args: $*"

if [[ -n "$DYLD_LIBRARY_PATH" ]] ; then
    #print 'test'
    dyld=$DYLD_LIBRARY_PATH
    #print $dyld
    unset DYLD_LIBRARY_PATH
fi

cmd="composite $*"
#print "run convert: $cmd"
$cmd

if [[ -n "$dyld" ]] ; then
    export DYLD_LIBRARY_PATH=$dyld
fi
