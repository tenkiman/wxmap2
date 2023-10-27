#!/bin/sh


ofile="tcdiag.rtfim9.2012102400.18l.2012.fim9-tmtrkN.txt"
ofilecomp="tcdiag.rtfim9.2012102400.18l.2012.fim9-tmtrkN.txt-UNITTEST"

cmd="time ../lsdiag.x rtfim9.2012102400.nhem.meta.txt tcmeta.18l.2012.rtfim9.2012102400.txt oisst.2012102400.nhem.dat $ofile"
exec $cmd
