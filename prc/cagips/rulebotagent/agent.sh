#!/bin/sh
# $Id: agent.sh,v 1.2 2003/03/28 00:16:18 freitasc Exp $
#
# In some cases you need to set the agent location
#cd /home/chuck/agent

# Runs the agent distribution
exec java -Xms64m -Xmx1024m -jar ./RulebotAgent.jar $@

