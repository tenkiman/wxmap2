#!/bin/ksh

# Compares two (code) trees using difftool.
fail() { 
   print -e "\n$1\n"
   print "\"target\":"
   print
   for target in $(ls .w2localrc.* | cut -f3-5 -d.)
   do	   
      print $target
   done
   exit 1
}	   


test "$1"  || fail "usage: $(basename $0) \"target\""

target=$1

cd ..
pwd

ln -s -f etc/run.cron.tcsh 
ln -s -f etc/.w2env
if [ -e etc/.w2rc.$target ]; then
  echo "found local .w2rc.$target ... doing ln -s"
  ln -s -f etc/.w2rc.$target .w2rc
else
  echo "using standard .w2rc"
  ln -s -f etc/.w2rc .w2rc
fi

ln -s -f etc/.pythonrc
ln -s -f etc/.w2alias.$target .w2alias
ln -s -f etc/.w2localrc.$target .w2localrc
ln -s -f etc/cookies.txt cookies.txt 
