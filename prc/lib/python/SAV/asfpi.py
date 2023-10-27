import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

import os
import sys
from math import sqrt

import struct
import array

import mf
import w2

class asfpi:

    import mf
    import w2
    
    W2Center='FNMOC/JTWC'
    
    undef=1e20

    def __init__(self,dtgopt='cur'):

        self.Center='FNMOC/JTWC'
        
        self.Areas=[
            'asia',
            'wconus',
            'conus',
            'bigaus',
            'tropwpac',
            'tropnio',
            'tropsio',
            'tropoz',
            'tropswpac',
            'tropepac',
            'troplant'
            ]


    def ReadCard(self):
        card=self.fd.readline()
        return(card)

    def ReadCards(self,filehandle=None):
        if(filehandle == None):
            filehandle=self.fd
        cards=filehandle.readlines()
        return(cards)

        
if (__name__ == "__main__"):

    verb=0

    #
    # instantiate the upamon object which opens a file
    #

    jt=asfpi('cur')

    print jt.Center

    

    
