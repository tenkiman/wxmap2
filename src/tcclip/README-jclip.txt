2016110312
how to build the jclip.so

   629	18:43	f2py -c jtwc.clipper.lib.f -m jclip
   630	18:45	/opt/local/bin/gfortran -Wall -g -m64 -Wall -g -undefined dynamic_lookup -bundle /var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmp9GxDFt/var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmp9GxDFt/src.macosx-10.5-x86_64-2.7/jclipmodule.o /var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmp9GxDFt/var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmp9GxDFt/src.macosx-10.5-x86_64-2.7/fortranobject.o /var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmp9GxDFt/jtwc.clipper.lib.o /var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmp9GxDFt/var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmp9GxDFt/src.macosx-10.5-x86_64-2.7/jclip-f2pywrappers.o -L/opt/local/lib/gcc49/gcc/x86_64-apple-darwin15/4.9.4 -L/w21/app/anaconda-4.0/lib -lgfortran -o ./jclip.so


nclip.so:

f2py nhc.clipper.lib.f -m nclip -h nclip.pyf --overwrite-signature
ws.nw nclip.pyf change 'type(' to 'integer('

f2py -c nclip.pyf nhc.clipper.lib.f
opt/local/bin/gfortran -Wall -g -m64 -Wall -g -undefined dynamic_lookup -bundle /var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmpNzISwG/var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmpNzISwG/src.macosx-10.5-x86_64-2.7/nclipmodule.o /var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmpNzISwG/var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmpNzISwG/src.macosx-10.5-x86_64-2.7/fortranobject.o /var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmpNzISwG/nhc.clipper.lib.o /var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmpNzISwG/var/folders/br/2cm9fkcj44s9yyp79v5j65w80004z7/T/tmpNzISwG/src.macosx-10.5-x86_64-2.7/nclip-f2pywrappers.o -L/opt/local/lib/gcc49/gcc/x86_64-apple-darwin15/4.9.4 -L/w21/app/anaconda-4.0/lib -lgfortran -o ./nclip.so
