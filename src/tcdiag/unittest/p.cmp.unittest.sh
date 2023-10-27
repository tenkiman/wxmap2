#!/bin/sh


ofile="tcdiag.rtfim9.2012102400.18l.2012.fim9-tmtrkN.txt"
ofilecomp="tcdiag.rtfim9.2012102400.18l.2012.fim9-tmtrkN.txt-UNITTEST"
#ofilecmp="tcdiag.rtfim9.2012102400.18l.2012.fim9-tmtrkN.txt-aori"
ofile="tcdiag.rtfim9.2012102400.18l.2012.fim9-tmtrkN.txt-aori"

cmpcmd="diff $ofile $ofilecomp"
echo $cmpcmd
exec $cmpcmd
exit


