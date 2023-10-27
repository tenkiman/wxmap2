from subprocess import Popen, PIPE, STDOUT,check_output
import os,sys,glob,time,getopt,copy,getpass,struct,errno
import inspect
import shelve
import cPickle as pickle
from socket import gethostname,getfqdn
import datetime

from time import time as timer
from time import sleep,mktime
from types import StringType,IntType,FloatType,ListType,DictType,TupleType
from math import atan2,atan,pi,fabs,cos,sin,log,tan,acos,sqrt
import array

import zipfile
import filecmp

NewPageChar=chr(014)

# file: mf.py
#
# Change Log:
#
# 20011030 - added gtime2dtg and cname3
# 20020116 - added ndaymo
# 20020702 - mods from AT at JTWC

MandatoryPressureLevels=[1000,925,850,700,500,400,300,250,200,150,100,70,50,30,20,10]

# -- set units or 'metric'
#
units='english'

# -- 20030828 -- set calendar; can change by mf.calendar='365day'
#
calendar='gregorian'

# -- new future w3 vars for moving to hopper.orc.gmu.edu
# -- funny place to put because of the many imports

ptmpBaseDir=os.getenv('PTMP')

