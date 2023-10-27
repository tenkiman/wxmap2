

/* 

Program swaps file in place.  Running it twice gets you the
original file.  Never run on PC so not sure it works there.

 Byte swaps a file in place.  Assumes the file contains only
    16 bit (2 byte) fields.  Usage:
 
           swap file-name

    To compile:  cc swap.c -o swap

    Primarily used to swap GrADS metafiles
*/

#include <stdio.h>

void gabswp (int *, int);
int buf[1000];

main (int argc, char *argv[])  {
FILE *ifile;
int pos,rc;

  if (argc!=2) {
    printf ("File name argument is required\n");
    return;
  }
  ifile = fopen(argv[1],"r+");
  if (ifile==NULL) {
    printf ("Error opening file: %s\n",argv[1]);
    return;
  }
  
  pos = 0;
  while (1) {
    fseek(ifile,pos,0);
    rc = fread(buf,sizeof(int),1000,ifile);
    if (rc<1000) break;
    gabswp (buf,1000);
    fseek(ifile,pos,0);
    rc = fwrite(buf,sizeof(int),1000,ifile);
    if (rc!=1000) {
      printf ("write error.  file may be corrupted\n");
      return;
    }
    pos+=sizeof(int)*1000;
  }   
  if (rc>0) {
    gabswp(buf,rc);
    fseek(ifile,pos,0);
    fwrite (buf,sizeof(int),rc,ifile);
  }
  printf ("Length = %i\n",pos+rc*sizeof(int));
  fclose(ifile);
}
  
/* Byte swap requested number of 4 byte elements */

void gabswp (int *r, int cnt) {
int i;
char *ch1,*ch2,*ch3,*ch4,cc1,cc2;

ch1 = (char *)r;
ch2 = ch1+1;
ch3 = ch2+1;
ch4 = ch3+1;
for (i=0; i<cnt; i++) {
  cc1 = *ch1;
  cc2 = *ch2;
  *ch1 = *ch4;
  *ch2 = *ch3;
  *ch3 = cc2;
  *ch4 = cc1;
  ch1+=4; ch2+=4; ch3+=4; ch4+=4;
}

}
