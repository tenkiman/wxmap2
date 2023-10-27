#
# Makefile skeleton for compiling java .class files
#
# Include this file in your makefile as below:
#
# <makefile>
#
# DEST_DIR=-d /bubba/projects/JAVA/classes
#
# SRCS=foo.java
#
# .include java.mk
#
# </makefile>
#
# Chris Toshok
# Copyright (C) 1995
# First Step Research
# 

.SUFFIXES: .java .class

JSTAMPS=$(SRCS:%.java=.stamp-%)

all:: $(JSTAMPS)

doc:: 
	javadoc $(DOC_DEST_DIR) $(PACKAGE) $(DOC_SRCS)

.stamp-%: %.java
	/bubba/projects/JAVA/bin/javac -classpath /bubba/projects/JAVA/classes:/bubba/projects/JAVA/JDK/classes:$(CLASSPATH) $(DEST_DIR) $<
	@touch $@
