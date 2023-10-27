#!/bin/sh
# $Id: agent.sh,v 1.2 2003/03/28 00:16:18 freitasc Exp $
#
# In some cases you need to set the agent location
#cd /Volumes/dat2/w21/prc/cagips/rulebotagent/
cd  /data/amb/users/fiorino/w21/prc/cagips/rulebotagent

# Runs the agent distribution
exec /usr/bin/java -Xms64m -Xmx1024m -jar ./RulebotAgent.jar -hidden
#exec /usr/bin/java -jar ./RulebotAgent.jar run
# use this one to configure tdir in properties
#exec /usr/bin/java -jar ./RulebotAgent.jar 

