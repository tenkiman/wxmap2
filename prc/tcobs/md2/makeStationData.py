from M import *
import math

MF = MFutils()

NO_OUTPUT = ['dtg','lat','lon','lev']

class MakeStnData ( ):

    def __init__ ( self, varDict, dataDict=None, inputPath=None, outputPath='output', title="Station Date", numTimes=1, dtgStart='2000010101', timeInc=6, undef=-999.99, varNoInput=[], varNoOutput=[] ):
    #PRE:  varDict: a dictionary containing a dictionary that defines the characteristics of the data for GrADS.
    #        varDict is setup as follows (you are required to include the dtg in yyyymmddhh format, lat, lon (and lev if file contains pressure level dependent data):
    #          'variableName':{
    #                          'descr': 'description of the variable',
    #                          'unit':  '[units]',
    #                          'lev':   'lev = 0 for surface data not defined by pressure, 1 for level dependent data defined by pressure height, and None if the data point will not be plotted'x,
    #                          'start': 'the first index for the variable in a line (set to None if passing a dataDict)',
    #                          'end':   'the last index + 1 for the variable in a line (set to None if passing a dataDict)'
    #                         }
    #      dataDict: the dictionary containing a dictionary of the data.
    #        dataDict must be setup as follows:
    #          'stnid (must be a string of 8 characters': {
    #                       'variableName': [float(data point)]
    #                     }
    #      inputPath: if not passing a dataDict, you can send an input path to data file.
    #        the data file must have each variable on every line.
    #        use the start and end to parse the file
    #      outputPath: the directory and filename for the control, station map, and data file. DO NOT INCLUDE AND EXTENSION
    #      title: the title within the GrADS control file.
    #      numTimes: the number of time steps contained by the file. Can be set to 1
    #      dtgStart: the start date for the data. must be in yyyymmddhh format. If numTimes set to 1, then the dtg should be the same as in the file.
    #      timeInc: the interval between time steps. Must be defined even if numTimes = 1
    #      undef: a number (typically a float) that represents undefined data. If data contains NA or None, please set to a float.
    #      varNoInput: If using inputPath option and manipulating the data to display other parameters, state which dictionary keys in varDict are not to be parsed
    #      varNoOutput: If using inputPath option, certain dictionary keys in varDict can be excluded from the GrADS control and observation files
    #POST: Calls fuction to produce the GrADS control file in outputPath. If inputPath != None, parses the input data file.
        if ( (dataDict == None and inputPath == None) or (dataDict != None and inputPath != None)):
            print "You must define the dataDict or the inputPath. You cannot leave both undefined or define both."
            sys.exit()
        self.varDict = varDict
        self.dataDict = dataDict
        self.inputPath = inputPath
        self.title = title
        self.numTimes = numTimes
        self.dtgStart = dtgStart
        self.timeInc = timeInc
        self.undef = undef
        self.outputPath = outputPath
        self.varNoInput = varNoInput
        self.varNoOutput = NO_OUTPUT + varNoOutput

        self.varKeys = self.varDict.keys()
        self.varKeys.sort()
        self.StnIdInc = 0
        try:
            print "%s.obs"%self.outputPath
            self.openOutputPath = open( "%s.obs"%( self.outputPath), 'w' )
        except:
            raise IOError( 'Unable to open: %s.obs'%( self.outputPath ) )

        self.MakeCtl()
        if ( self.inputPath != None ):
            try:
                self.openInputPath = open( self.inputPath )
            except:
                raise IOError( 'Unable to open: %s'% ( self.inputPath ) )
            self.ParseCards()
        else:
            self.openInputPath = None

    def MakeCtl ( self ):
    #POST: Generates GrADS control file

        try:
            openCtlPath = open( "%s.ctl"%( self.outputPath ), 'w' )
        except:
            raise IOError( 'Unable to open: %s.ctl'%( self.outputPath ) )

        ctlVars = []
        gtimeStart = mf.dtg2gtime( self.dtgStart )

        for lev in range(2):
            for var in self.varKeys:
                if (self.varDict[var]['lev'] == lev):
                    try:
                        self.varNoOutput.index(var)
                    except:
                        ctlVars.append( "%-7s %d 0 %s %s"%( var, self.varDict[var]['lev'], self.varDict[var]['descr'], self.varDict[var]['unit'] ) )

        ctl = """dset    ^%s
title   %s
dtype   station
stnmap  ^%s
undef   -999.99
tdef    %d linear %s %dhr
vars    %d
"""%( "%s.obs"%(self.outputPath), self.title, "%s.smp"%(self.outputPath), self.numTimes, gtimeStart, self.timeInc, len( ctlVars ) )

        for var in ctlVars:
            ctl += "%s\n" % ( var )
        ctl += "endvars"

        openCtlPath.writelines( ctl )
        openCtlPath.close()

    def ParseCards ( self ):
    #POST: pareses the input path file to generate the data dictionary
        if ( self.openInputPath == None ):
            print "You are not using the inputPath option."
            print "Please check your instance of the object."
            sys.exit()
        cards = self.openInputPath.readlines()
        inc = 0
        self.dataDict = {}

        for card in cards:
            stnid = "%08d"%(inc)
            inc += 1
            for var in self.varKeys:
                try:
                    self.varNoInput.index( var )
                except:
                    try:
                        self.dataDict[stnid][var].append(card[self.varDict[var]['start']:self.varDict[var]['end']])
                    except:
                        try:
                            self.dataDict[stnid][var] = []
                            self.dataDict[stnid][var].append(card[self.varDict[var]['start']:self.varDict[var]['end']])
                        except:
                            self.dataDict[stnid] = {}
                            self.dataDict[stnid][var] = []
                            self.dataDict[stnid][var].append(card[self.varDict[var]['start']:self.varDict[var]['end']])

    def GetData ( self ):
    #POST: returns the data dictionary
        return( self.dataDict )

    def StationOutput ( self, outputData = None ):
    #PRE:  outputData must be in the dataDict format explained in the init. All variables in outputData must have been defined in varDict
    #POST: Generates the GrADS observation file and does a station map.
        records = {}
        if ( outputData == None ): outputData = self.dataDict
        stnids = outputData.keys()
        stnids.sort()
        for stnid in stnids:
            for inc in range(len(outputData[stnid]['dtg'])):
                timei1 = MF.Dtg2Timei( outputData[stnid]['dtg'][inc] )
                timei2 = MF.Dtg2Timei( self.dtgStart )
                dtime = MF.DeltaTimei( timei1, timei2 )
                curtime = int(math.floor(dtime / float( self.timeInc ))) + 1
                rtime = dtime / float(self.timeInc) - curtime + 1
                if (rtime > 0.5):
                    curtime += 1
                    rtime = rtime - 1

                if ( rtime > self.numTimes ):
                    print "GrADS relative time greater than number of times stated in control filei."
                    print "To correct the issue, set numTimes > rtime in object instance."
                    sys.exit()
                if ( dtime < 0 ):
                    print "The data point's time is less than dtgStart."
                    print "Please change the dtgStart to a value > than data points."
                    sys.exit()

                lon = float( outputData[stnid]['lon'][inc] )
                if ( lon < 0.0 ): lon = 360.0 + lon
                stnheaduad = struct.pack('8sfffii', stnid, float(outputData[stnid]['lat'][inc]), lon, rtime, 1, 0 )
                stnheadsfc = struct.pack('8sfffii', stnid, float(outputData[stnid]['lat'][inc]), lon, rtime, 1, 1 ) 
                try:
                    self.varKeys.index('lev')
                    stnrecuad = struct.pack('f', float(outputData[stnid]['lev'][inc]) )
                except:
                    print "Warning: if you are generating upper air data, you need a lev variable in your varDict"
            
                writeuad = False
                sfcFirst = True
                for var in self.varKeys:
                    if ( self.varDict[var]['lev'] != None ):
                        datum = outputData[stnid][var][inc]
                        if ( datum == self.undef): datum = -999.99
                        else: datum = float(datum)
                        stnrec = struct.pack('f',datum)
                        if ( self.varDict[var]['lev'] == 1 ):
                            writeuad = True
                            stnrecuad += stnrec
                        if ( self.varDict[var]['lev'] == 0 ):
                            if ( sfcFirst == True ):
                                stnrecsfc = stnrec
                                sfcFirst = False
                            else:
                                stnrecsfc += stnrec


                if ( sfcFirst == False ):
                    curlev = 1
                    try:
                        records[(curlev,curtime)].append((stnheadsfc,stnrecsfc))
                    except:
                        records[(curlev,curtime)] = []
                        records[(curlev,curtime)].append((stnheadsfc,stnrecsfc))
                if ( writeuad == True ):
                    curlev = 2
                    try:
                        records[(curlev,curtime)].append((stnheaduad,stnrecuad))
                    except:
                        records[(curlev,curtime)] = []
                        records[(curlev,curtime)].append((stnheaduad,stnrecuad))

        levstimes = records.keys()
        for time in range(1,self.numTimes+1):
            for lev in range(1,2+1):
                try:
                    levstimes.index((lev,time))
                    for rec in records[(lev,time)]:
                        self.openOutputPath.write(rec[0])
                        self.openOutputPath.write(rec[1])
                except:
                    None
            stnid = "time%04d"%time
            stnhead = struct.pack( '8sfffii', stnid, 0.0, 0.0, 0.0, 0, 0 )
            self.openOutputPath.write(stnhead)

        self.openOutputPath.close()

        os.system( 'stnmap -q -i %s.ctl' % ( self.outputPath ) )

if ( __name__ == '__main__'):

    varDict = {
        'dtg':{
               'descr': 'date time group',
               'unit':  '[yyyymmddhh]',
               'lev':   None,
               'start': 0, 
               'end':   10,
              },
        'lat':{
               'descr': 'latitude',
               'unit':  '[degrees]',
               'lev':   None,
               'start': 16, 
               'end':   23,
              },
        'lon':{
               'descr': 'longitude',
               'unit':  '[degrees]',
               'lev':   None,
               'start': 24,
               'end':   32,
              },
        'u':  {
               'descr': 'u comp wind',
               'unit':  '[m/s]',
               'lev':   1,
               'start': 52,
               'end':   59,
              },
        'v':  {
               'descr': 'v comp wind',
               'unit':  '[m/s]',
               'lev':   1,
               'start': 61,
               'end':   68,
              },
        'lev':{
               'descr': 'pressure level',
               'unit':  '[hPa]',
               'lev':   None,
               'start': 73,
               'end':   77,
              },

    }

    stnData = MakeStnData( varDict, inputPath="../../../dat/tc/cira/mtcswa/2010/04e/2010EP04_MPSATWD_2010062512.obs", numTimes=10, dtgStart='2010062400' )
    stnData.StationOutput()

