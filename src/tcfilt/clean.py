#!/usr/bin/env python

import sys
import os
import string
import glob

files=glob.glob('*.f')

for file in files:
    newfile="%s.new"%(file)
    oldfile="%s.old"%(file)

    cmd="mv %s %s ; mv %s %s"%(file,oldfile,newfile,file)
    print 'CCC ',cmd
    os.system(cmd)

sys.exit()


for file in files:
    newfile="%s.new"%(file)
    print file

    cards=open(file).readlines()

    newcards=[]
    for card in cards:
        t1=string.rstrip(card)
        newcards.append(t1+'\n')
        print 'CCC %s CCC'%(t1)

    o=open(newfile,'w')
    for newcard in newcards:
        print 'nnn ',newcard

    o.writelines(newcards)
    o.close()

sys.exit()


    


