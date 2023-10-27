#!/usr/bin/perl -I/w21/prc/lib/perl/ECMWF
use ECMWF::DataServer;
use strict;

my $client = ECMWF::DataServer->new(
    portal => 'http://tigge-portal.ecmwf.int/d/dataserver/',
    token  => 'd907f75cd718ed40eff12e8bdd115f8b',
    email  => 'michael.fiorino@noaa.gov',
);

$client->retrieve( 
    dataset  => "tigge",
    step     => "24/to/120/by/24",
    number   => "all",
    levtype  => "sl",
    date     => "20071001/to/20071003",
    time     => "00/12",
    origin   => "all",
    type     => "pf",
    param    => "tp",
    area     => "70/-130/30/-60",
    grid     => "2/2",
    target   => "data.grib",
    );

