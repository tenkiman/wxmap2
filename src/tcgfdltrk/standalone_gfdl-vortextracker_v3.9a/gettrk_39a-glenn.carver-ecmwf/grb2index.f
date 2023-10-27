      PROGRAM GRB2INDEX
C$$$  MAIN PROGRAM DOCUMENTATION BLOCK
C
C MAIN PROGRAM: GRB2INDEX     WRITE A GRIB2 INDEX FILE
C   PRGMMR: GILBERT          ORG: W/NP11        DATE: 2002-01-03
C
C ABSTRACT: PROGRAM CREATES AN INDEX FILE FROM A GRIB2 FILE.
C   THE INDEX FILE SERVES AS A TABLE OF CONTENTS FOR THE GRIB FILE,
C   ENABLING QUICK ACCESS TO THE DATA.  THE GRIB FILE MUST BE UNBLOCKED,
C   BUT THERE CAN BE A GAP BEFORE THE FIRST GRIB MESSAGE OF AT MOST
C   32000 BYTES AND GAPS BETWEEN MESSAGES OF AT MOST 4000 BYTES.
C   THE TWO FILE NAMES ARE RETRIEVED FROM THE COMMAND LINE ARGUMENTS.
C   THE FIRST ARGUMENT IS THE NAME OF THE INPUT GRIB FILE.
C   THE SECOND ARGUMENT IS THE NAME OF THE OUTPUT INDEX FILE.
C   FOR THIS PROGRAM, ONLY GRIB VERSION 2 CAN BE READ.
C   VERSION 1 OF THE INDEX FILE HAS THE FOLLOWING FORMAT:
C     81-BYTE S.LORD HEADER WITH 'GB2IX1' IN COLUMNS 42-47 FOLLOWED BY
C     81-BYTE HEADER WITH NUMBER OF BYTES TO SKIP BEFORE INDEX RECORDS,
C     TOTAL LENGTH IN BYTES OF THE INDEX RECORDS, NUMBER OF INDEX RECORDS,
C     AND GRIB FILE BASENAME WRITTEN IN FORMAT ('IX1FORM:',3I10,2X,A40).
C     EACH FOLLOWING INDEX RECORD CORRESPONDS TO A FIELD IN A GRIB2 MESSAGE
C     AND HAS THE INTERNAL FORMAT:
C       BYTE 001 - 004: LENGTH OF INDEX RECORD
C       BYTE 005 - 008: BYTES TO SKIP IN DATA FILE BEFORE GRIB MESSAGE
C       BYTE 009 - 012: BYTES TO SKIP IN MESSAGE BEFORE GDS
C       BYTE 013 - 016: BYTES TO SKIP IN MESSAGE BEFORE PDS
C       BYTE 017 - 020: BYTES TO SKIP IN MESSAGE BEFORE DRS
C       BYTE 021 - 024: BYTES TO SKIP IN MESSAGE BEFORE BMS
C       BYTE 025 - 032: BYTES TOTAL IN THE MESSAGE
C       BYTE 033 - 033: GRIB VERSION NUMBER ( CURRENTLY 2 )
C       BYTE 034 - 034: MESSAGE DISCIPLINE
C       BYTE 035 - 036: FIELD NUMBER WITHIN GRIB2 MESSAGE
C       BYTE 037 -  II: IDENTIFICATION SECTION (IDS)
C       BYTE II+1-  JJ: GRID DEFINITION SECTION (GDS)
C       BYTE JJ+1-  KK: PRODUCT DEFINITION SECTION (PDS)
C       BYTE KK+1-  LL: THE DATA REPRESENTATION SECTION (DRS)
C       BYTE LL+1-LL+6: FIRST 6 BYTES OF THE BIT MAP SECTION (BMS)
C
C PROGRAM HISTORY LOG:
C   92-11-22  IREDELL
C 2002-01-03  GILBERT   - MODIFIED FROM PROGRAM GRBINDEX TO WORK WITH GRIB2
C 2005-02-25  GILBERT   - Removed buffering option (see baseto).
C 2012-08-01  VUONG     - CHANGED HOSTNAME TO HOSTNAM
C
C USAGE: grb2index gribfile indexfile
C
C INPUT FILE:
C   gribfile     GRIB2 FILE
C
C OUTPUT FILE:
C   indexfile    UNBLOCKED INDEX FILE
C
C SUBPROGRAMS CALLED:
C   IARGC        COUNT THE COMMAND LINE ARGUMENTS
C   GETARG       GET COMMAND LINE ARGUMENT
C   WRGI1H       WRITE INDEX HEADERS
C   GETG2IR       GET INDEX BUFFER
C   BAWRITE      BYTE-ADDRESSABLE WRITE
C   ERRMSG       WRITE A MESSAGE TO STDERR
C   ERREXIT      EXIT WITH RETURN CODE
C
C EXIT STATES:
C   COND =   0 - SUCCESSFUL RUN
C   COND =   1 - GRIB MESSAGE NOT FOUND
C   COND =   2 - INCORRECT ARGUMENTS
C   COND =   8 - ERROR ACCESSING FILE
C
C ATTRIBUTES:
C   LANGUAGE: FORTRAN 90
C
C$$$
      PARAMETER(MSK1=32000,MSK2=4000)
      CHARACTER CGB*256,CGI*256
      CHARACTER(LEN=1),POINTER,DIMENSION(:) :: CBUF
      CHARACTER CARG*300
      INTEGER NARG,IARGC
      INTERFACE
         SUBROUTINE GETG2IR(LUGB,MSK1,MSK2,MNUM,CBUF,NLEN,NNUM,
     &                      NMESS,IRET)
           INTEGER,INTENT(IN) :: LUGB,MSK1,MSK2,MNUM
           CHARACTER(LEN=1),POINTER,DIMENSION(:) :: CBUF
           INTEGER,INTENT(OUT) :: NLEN,NNUM,NMESS,IRET
         END SUBROUTINE GETG2IR
      END INTERFACE
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C  GET ARGUMENTS
      NARG=IARGC()
      IF(NARG.NE.2) THEN
        CALL ERRMSG('grb2index:  Incorrect usage')
        CALL ERRMSG('Usage: grb2index gribfile indexfile')
        CALL ERREXIT(2)
      ENDIF
      CALL GETARG(1,CGB)
      NCGB=LEN_TRIM(CGB)
      CALL BAOPENR(11,CGB(1:NCGB),IOS)
      !CALL BASETO(1,1)
      IF(IOS.NE.0) THEN
        LCARG=LEN('grb2index:  Error accessing file '//CGB(1:NCGB))
        CARG(1:LCARG)='grb2index:  Error accessing file '//CGB(1:NCGB)
        CALL ERRMSG(CARG(1:LCARG))
        CALL ERREXIT(8)
      ENDIF
      CALL GETARG(2,CGI)
      NCGI=LEN_TRIM(CGI)
      CALL BAOPEN(31,CGI(1:NCGI),IOS)
      IF(IOS.NE.0) THEN
        LCARG=LEN('grb2index:  Error accessing file '//CGI(1:NCGI))
        CARG(1:LCARG)='grb2index:  Error accessing file '//CGI(1:NCGI)
        CALL ERRMSG(CARG(1:LCARG))
        CALL ERREXIT(8)
      ENDIF
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C  WRITE INDEX FILE
      MNUM=0
      CALL GETG2IR(11,MSK1,MSK2,MNUM,CBUF,NLEN,NNUM,NMESS,IRGI)
      IF(IRGI.GT.1.OR.NNUM.EQ.0.OR.NLEN.EQ.0) THEN
        CALL ERRMSG('grb2index:  No GRIB messages detected in file '
     &              //CGB(1:NCGB))
        CALL BACLOSE(11,IRET)
        CALL BACLOSE(31,IRET)
        CALL ERREXIT(1)
      ENDIF
      NUMTOT=NUMTOT+NNUM
      MNUM=MNUM+NMESS
      CALL WRGI1H(31,NLEN,NUMTOT,CGB(1:NCGB))
      IW=162
      CALL BAWRITE(31,IW,NLEN,KW,CBUF)
      IW=IW+NLEN
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C  EXTEND INDEX FILE IF INDEX BUFFER LENGTH TOO LARGE TO HOLD IN MEMORY
      IF(IRGI.EQ.1) THEN
        DOWHILE(IRGI.EQ.1.AND.NNUM.GT.0)
          IF (ASSOCIATED(CBUF)) THEN
             DEALLOCATE(CBUF)
             NULLIFY(CBUF)
          ENDIF
          CALL GETG2IR(11,MSK1,MSK2,MNUM,CBUF,NLEN,NNUM,NMESS,IRGI)
          IF(IRGI.LE.1.AND.NNUM.GT.0) THEN
            NUMTOT=NUMTOT+NNUM
            MNUM=MNUM+NMESS
            CALL BAWRITE(31,IW,NLEN,KW,CBUF)
            IW=IW+NLEN
          ENDIF
        ENDDO
        CALL WRGI1H(31,IW,NUMTOT,CGB(1:NCGB))
      ENDIF
      CALL BACLOSE(11,IRET)
      CALL BACLOSE(31,IRET)
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
      END
C-----------------------------------------------------------------------
      SUBROUTINE WRGI1H(LUGI,NLEN,NNUM,CGB)
C$$$  SUBPROGRAM DOCUMENTATION BLOCK
C
C SUBPROGRAM: WRGI1H         WRITE INDEX HEADERS
C   PRGMMR: IREDELL          ORG: W/NMC23     DATE: 93-11-22
C
C ABSTRACT: THIS SUBPROGRAM WRITES TWO INDEX HEADERS.
C
C PROGRAM HISTORY LOG:
C   93-11-22  IREDELL
C   95-10-31  IREDELL   - MODULARIZE SYSTEM CALLS
C 2005-02-25  GILBERT   - Set Header bytes  49-54 to blanks.
C 2012-08-01  VUONG     - CHANGED HOSTNAME TO HOSTNAM
C
C USAGE:    CALL WRGI1H(LUGI,NLEN,NNUM,CGB)
C   INPUT ARGUMENTS:
C     LUGI         INTEGER LOGICAL UNIT OF OUTPUT INDEX FILE
C     NLEN         INTEGER TOTAL LENGTH OF INDEX RECORDS
C     NNUM         INTEGER NUMBER OF INDEX RECORDS
C     CGB          CHARACTER NAME OF GRIB FILE
C
C SUBPROGRAMS CALLED:
C   NCBASE       GET BASENAME OF FILE
C   HOSTNAM      GET SYSTEM NAME
C   BAWRITE      BYTE-ADDRESSABLE WRITE
C
C ATTRIBUTES:
C   LANGUAGE: FORTRAN
C
C$$$
      CHARACTER CGB*(*)
      CHARACTER CD8*8,CT10*10,HOSTNAM*15
      CHARACTER CHEAD(2)*81
      character*15 chostname
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C  FILL FIRST 81-BYTE HEADER
      NCGB=LEN(CGB)
      NCGB1=NCBASE(CGB,NCGB)
      NCGB2=NCBASE(CGB,NCGB1-2)
      CALL DATE_AND_TIME(CD8,CT10)
      CHEAD(1)='!GFHDR!'
      CHEAD(1)(9:10)=' 1'
      CHEAD(1)(12:14)='  1'
      WRITE(CHEAD(1)(16:20),'(I5)') 162
      CHEAD(1)(22:31)=CD8(1:4)//'-'//CD8(5:6)//'-'//CD8(7:8)
      CHEAD(1)(33:40)=CT10(1:2)//':'//CT10(3:4)//':'//CT10(5:6)
      CHEAD(1)(42:47)='GB2IX1'
      !CHEAD(1)(49:54)=CGB(NCGB2:NCGB1-2)
      CHEAD(1)(49:54)='      '
      call hostnm(chostname)
      CHEAD(1)(56:70)=chostname(1:15)
      CHEAD(1)(72:80)='grb2index'
      CHEAD(1)(81:81)=CHAR(10)
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C  FILL SECOND 81-BYTE HEADER
      CHEAD(2)='IX1FORM:'
      WRITE(CHEAD(2)(9:38),'(3I10)') 162,NLEN,NNUM
      CHEAD(2)(41:80)=CGB(NCGB1:NCGB)
      CHEAD(2)(81:81)=CHAR(10)
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C  WRITE HEADERS AT BEGINNING OF INDEX FILE
      CALL BAWRITE(LUGI,0,162,KW,CHEAD)
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
      RETURN
      END
C-----------------------------------------------------------------------
      FUNCTION NCBASE(C,N)
C$$$  SUBPROGRAM DOCUMENTATION BLOCK
C
C SUBPROGRAM: NCBASE         LOCATE BASENAME OF A FILE
C   PRGMMR: IREDELL          ORG: W/NMC23     DATE: 93-11-22
C
C ABSTRACT: THIS SUBPROGRAM LOCATES THE CHARACTER NUMBER AFTER THE LAST 
C   IN A CHARACTER STRING.  FOR UNIX FILENAMES, THE CHARACTER NUMBER
C   RETURNED MARKS THE BEGINNING OF THE BASENAME OF THE FILE.
C
C PROGRAM HISTORY LOG:
C   93-11-22  IREDELL
C
C USAGE:     ...=NCBASE(C,N)
C   INPUT ARGUMENTS:
C     C            CHARACTER STRING TO SEARCH
C     N            INTEGER LENGTH OF STRING
C
C ATTRIBUTES:
C   LANGUAGE: CRAY FORTRAN
C
C$$$
      CHARACTER C*(*)
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
      K=N
      DOWHILE(K.GE.1.AND.C(K:K).NE.'/')
        K=K-1
      ENDDO
      NCBASE=K+1
C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
      RETURN
      END

