#!/bin/bash

cmd="$W2_PRC_DIR/wxmap2/w2-status.py $1 $2"
exec $cmd | less

exit;
