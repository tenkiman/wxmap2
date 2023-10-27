f77 -c lmoments.f
ld -r -o liblmoments.a lmoments.o

for install (-i) option we need to be root.
if you run pyfort after this, /build will be owned by root and thus 
you need to run as root even if you just use the build option (-b) and do
not install (-i)
pyfort -b -c g77 -L. -llmoments Lmoments.pyf

the .so will be in build/lib.linux-i686-1.5/
