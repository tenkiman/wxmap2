#!/usr/bin/perl -I/w21/prc/flddat/tigge/ECMWF
use ECMWF::DataServer;
#use strict;

my $client = ECMWF::DataServer->new(
    portal => 'http://tigge-portal.ecmwf.int/d/dataserver/',
    token  => 'd907f75cd718ed40eff12e8bdd115f8b',
    email  => 'michael.fiorino@noaa.gov',
);

print "getting...... \n";

$ymd="20090309";
$hh="12";

$client->retrieve( 
    dataset  => "tigge",
    step     => "0/to/156/by/12",
    number   => "all",
    levtype  => "pl",
    level    => "1000/850/700/500/200",
    date     => "${ymd}",
    time     => "$hh",
    origin   => "all",
    type     => "fc",
    param    => "130/131/132/133/156",
    area     => "global",
    grid     => "1.0/1.0",
    target   => "ua.10.${ymd}${hh}.grb2",
    );

$client->retrieve( 
    dataset  => "tigge",
    step     => "0/to/156/by/6",
    number   => "all",
    levtype  => "sl",
    date     => "20090309",
    time     => "00",
    origin   => "all",
    type     => "fc",
    param    => "msl/10u/10v/tp",
    area     => "global",
    grid     => "0.5/0.5",
    target   => "sfc.05.${ymd}${hh}.grb2",
    );



print "DONE....\n";
