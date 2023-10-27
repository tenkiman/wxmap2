#!/bin/sh

time tcdiag.x test.tcdiag.meta.txt test.tcdiag.dat test.tcdiag.out.txt
diff test.tcdiag.out test.tcdiag.out.txt
