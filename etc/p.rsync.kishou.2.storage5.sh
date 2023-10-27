#!/bin/sh

base5='/storage5/kishou'

cd /opt/linux
pwd
rsync -avl --delete . $base5/opt/linux/.

cd /var/lib
pwd
rsync -avL --delete mysql $base5/var/lib/

cd /home/mfiorino/
pwd
rsync -avL  . $base5/home/mfiorino/

cd /wxmap2/
pwd
rsync -avl  --delete --exclude-from=/wxmap2/ex-wxmap2.txt . $base5/wxmap2/.



