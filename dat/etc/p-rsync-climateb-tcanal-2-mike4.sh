#!/bin/bash
cd $W2/dat/tc
pwd
rsync -alv --exclude "*.dat" --exclude "*.grb*" --exclude "*.gmp*" mfiorino@climateb:/braid1/mfiorino/w22/dat/tc/tcanal/ tcanal/

cd $W2/dat/
pwd
rsync -alv --exclude "tcanal*" --exclude "*.grb*" --exclude "*.gmp*" mfiorino@climateb:/braid1/mfiorino/w22/dat/tc/ tc/

rsync -alv mfiorino@climateb:/braid1/mfiorino/w22/products/ /dat21/products/

rsync -alv --exclude "era5*" mfiorino@climateb:/braid1/mfiorino/w22/dat/nwp2/ /dat21/dat/nwp2/
