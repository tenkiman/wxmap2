@echo off
rem $Id: agent.bat,v 1.2 2003/02/20 00:05:34 freitasc Exp $

set CMD_LINE_ARGS=%*


rem set JAVA_HOME=c:\Program Files\Java\jdk1.5.0_03




rem if "%JAVA_HOME%" == "" goto noJavaHome
rem goto gotJavaHome


rem :noJavaHome
rem echo 
rem echo "JRE not found with installation or JAVA_HOME variable is not set."
rem echo  "If a Java VM or JRE is not installed, please install a copy."
rem echo 


rem :gotJavaHome


rem echo "starting Rulebot agent ... %JAVA_HOME%\jre\bin\java"

rem execute the agent
rem  

java  -Xms64m -Xmx1024m -Djava.util.logging.config.file=logging.properties -cp ".;lib/commons-httpclient-3.0.1.jar;lib/commons-codec-1.3.jar;lib/commons-logging-1.1.jar;lib/jnlp.jar;lib/FnmocCommons.jar;RulebotAgent.jar" mil.navy.fnmoc.rulebot.agent.RulebotAgent %CMD_LINE_ARGS%


rem "%JAVA_HOME%\\jre\\bin\\java"  -Xms64m -Xmx1024m -Djava.util.logging.config.file=logging.properties  -cp ".;%JAVA_HOME%\\jre\\lib\\javaws.jar;lib/commons-httpclient-3.0.1.jar;lib/commons-codec-1.3.jar;lib/commons-logging-1.1.jar;lib/jnlp.jar;lib/FnmocCommons.jar;RulebotAgent.jar"  mil.navy.fnmoc.rulebot.agent.RulebotAgent %CMD_LINE_ARGS% 

goto end

:end
