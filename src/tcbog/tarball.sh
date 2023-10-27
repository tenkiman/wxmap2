#!/bin/sh

tar -cvf tcbog.src.tar Makefile
tar -uvf tcbog.src.tar *.f
tar -uvf tcbog.src.tar *.h
tar -uvf tcbog.src.tar *.CUR.*
tar -uvf tcbog.src.tar test.sh
tar -uvf tcbog.src.tar tcbog.posits.txt
tar -uvf tcbog.src.tar README.src.txt

