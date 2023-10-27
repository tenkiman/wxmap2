
$pi=4.0*atan2(1.0,1.0);
$pi4=$pi/4.0;
$pi2=$pi/2.0;

$deg2rad=$pi/180.0;
$rad2deg=1.0/$deg2rad;
$rearth=6371.0;
$km2nm=60.0/(2*$pi*$rearth/360.0);
$nm2km=1.0/$km2nm;
$knots2ms=1000/($km2nm*3600);
$ms2knots=1/$knots2ms;
$units='metric';
$units='english';

#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#
#  sub tc_setup
#
#  define basins, models, etc
#
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

sub tc_setup {

@modelstc=('ifs','ngp');

@basins=(L,C,E,W,A,B,S,P,T);
@basins_global=(L,C,E,W,A,B,S,P,T);
@basins_shem=(S,P);
@basins_nhem=(L,C,E,W,A,B);

$basin_ukm{'NWP','code'}='W';
$basin_ukm{'NEP','code'}='E';
$basin_ukm{'NAT','code'}='L';
$basin_ukm{'NI','code'}='I';
$basin_ukm{'AUS','code'}='P';
$basin_ukm{'SWI','code'}='S';


$basin{'L','num'}='1';
$basin{'E','num'}='2';
$basin{'W','num'}='3';
$basin{'C','num'}='4';
$basin{'A','num'}='5';
$basin{'B','num'}='6';
$basin{'I','num'}='6';
$basin{'S','num'}='7';
$basin{'P','num'}='8';
$basin{'T','num'}='9';

$basin{'L','name'}='North Atlantic       ';
$basin{'C','name'}='central North Pacific';
$basin{'E','name'}='eastern North Pacific';
$basin{'W','name'}='western North Pacific';
$basin{'A','name'}='Arabian Sea (NIO)    ';
$basin{'B','name'}='Bay of Bengal (NIO)  ';
$basin{'I','name'}='North Indian Ocean   ';
$basin{'S','name'}='Southern Indian Ocean';
$basin{'P','name'}='Southwest Pacific    ';
$basin{'T','name'}='South Atlantic       ';

$basin{'L','2dname'}='AL'; $basin{'C','2dname'}='CP';
$basin{'E','2dname'}='EP'; $basin{'W','2dname'}='WP';
$basin{'A','2dname'}='IO'; $basin{'B','2dname'}='IO';
$basin{'I','2dname'}='IO'; $basin{'S','2dname'}='SH';
$basin{'P','2dname'}='SH';
$basin{'T','2dname'}='SL';


#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#
#   LANT
#
#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

$basin{'L','r30',30}=60;
$basin{'L','r30',40}=80;
$basin{'L','r30',50}=95;
$basin{'L','r30',60}=110;
$basin{'L','r30',70}=120;
$basin{'L','r30',80}=130;
$basin{'L','r30',90}=140;
$basin{'L','r30',100}=145;
$basin{'L','r30',110}=150;
$basin{'L','r30',120}=155;
$basin{'L','r30',130}=160;

$basin{'L','r50',50}=20;
$basin{'L','r50',60}=40;
$basin{'L','r50',70}=60;
$basin{'L','r50',80}=65;
$basin{'L','r50',90}=70;
$basin{'L','r50',100}=80;
$basin{'L','r50',110}=80;
$basin{'L','r50',120}=85;
$basin{'L','r50',130}=90;

#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#
#   EPAC
#
#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

$basin{'E','r30',30}=60;
$basin{'E','r30',40}=90;
$basin{'E','r30',50}=100;
$basin{'E','r30',60}=100;
$basin{'E','r30',70}=105;
$basin{'E','r30',80}=110;
$basin{'E','r30',90}=115;
$basin{'E','r30',100}=120;
$basin{'E','r30',110}=125;
$basin{'E','r30',120}=130;
$basin{'E','r30',130}=140;

$basin{'E','r50',50}=20;
$basin{'E','r50',60}=30;
$basin{'E','r50',70}=35;
$basin{'E','r50',80}=40;
$basin{'E','r50',90}=45;
$basin{'E','r50',100}=50;
$basin{'E','r50',110}=50;
$basin{'E','r50',120}=50;
$basin{'E','r50',130}=50;


#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#
#   WPAC
#
#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

$basin{'W','r30',30}=40;
$basin{'W','r30',40}=50;
$basin{'W','r30',50}=60;
$basin{'W','r30',60}=70;
$basin{'W','r30',70}=90;
$basin{'W','r30',80}=105;
$basin{'W','r30',90}=140;
$basin{'W','r30',100}=140;
$basin{'W','r30',110}=145;
$basin{'W','r30',120}=145;
$basin{'W','r30',130}=150;

$basin{'W','r50',50}=20;
$basin{'W','r50',60}=40;
$basin{'W','r50',70}=60;
$basin{'W','r50',80}=60;
$basin{'W','r50',90}=70;
$basin{'W','r50',100}=70;
$basin{'W','r50',110}=75;
$basin{'W','r50',120}=75;
$basin{'W','r50',130}=80;

#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#
#   NIO
#
#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

$basin{'I','r30',30}=50;
$basin{'I','r30',40}=50;
$basin{'I','r30',50}=55;
$basin{'I','r30',60}=55;
$basin{'I','r30',70}=60;
$basin{'I','r30',80}=60;
$basin{'I','r30',90}=60;
$basin{'I','r30',100}=60;
$basin{'I','r30',110}=60;
$basin{'I','r30',120}=60;
$basin{'I','r30',130}=60;

$basin{'I','r50',50}=20;
$basin{'I','r50',60}=20;
$basin{'I','r50',70}=25;
$basin{'I','r50',80}=25;
$basin{'I','r50',90}=30;
$basin{'I','r50',100}=35;
$basin{'I','r50',110}=35;
$basin{'I','r50',120}=40;
$basin{'I','r50',130}=45;

$basin{'A','r30',30}=50;
$basin{'A','r30',40}=50;
$basin{'A','r30',50}=55;
$basin{'A','r30',60}=55;
$basin{'A','r30',70}=60;
$basin{'A','r30',80}=60;
$basin{'A','r30',90}=60;
$basin{'A','r30',100}=60;
$basin{'A','r30',110}=60;
$basin{'A','r30',120}=60;
$basin{'A','r30',130}=60;

$basin{'A','r50',50}=20;
$basin{'A','r50',60}=20;
$basin{'A','r50',70}=25;
$basin{'A','r50',80}=25;
$basin{'A','r50',90}=30;
$basin{'A','r50',100}=35;
$basin{'A','r50',110}=35;
$basin{'A','r50',120}=40;
$basin{'A','r50',130}=45;


$basin{'B','r30',30}=50;
$basin{'B','r30',40}=50;
$basin{'B','r30',50}=55;
$basin{'B','r30',60}=55;
$basin{'B','r30',70}=60;
$basin{'B','r30',80}=60;
$basin{'B','r30',90}=60;
$basin{'B','r30',100}=60;
$basin{'B','r30',110}=60;
$basin{'B','r30',120}=60;
$basin{'B','r30',130}=60;

$basin{'B','r50',50}=20;
$basin{'B','r50',60}=20;
$basin{'B','r50',70}=25;
$basin{'B','r50',80}=25;
$basin{'B','r50',90}=30;
$basin{'B','r50',100}=35;
$basin{'B','r50',110}=35;
$basin{'B','r50',120}=40;
$basin{'B','r50',130}=45;


#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#
#   SIO
#
#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

$basin{'S','r30',30}=40;
$basin{'S','r30',40}=50;
$basin{'S','r30',50}=60;
$basin{'S','r30',60}=70;
$basin{'S','r30',70}=80;
$basin{'S','r30',80}=90;
$basin{'S','r30',90}=100;
$basin{'S','r30',100}=120;
$basin{'S','r30',110}=125;
$basin{'S','r30',120}=130;
$basin{'S','r30',130}=130;

$basin{'S','r50',50}=20;
$basin{'S','r50',60}=25;
$basin{'S','r50',70}=30;
$basin{'S','r50',80}=35;
$basin{'S','r50',90}=40;
$basin{'S','r50',100}=45;
$basin{'S','r50',110}=50;
$basin{'S','r50',120}=55;
$basin{'S','r50',130}=60;


#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#
#   SPAC
#
#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

$basin{'P','r30',30}=40;
$basin{'P','r30',40}=50;
$basin{'P','r30',50}=65;
$basin{'P','r30',60}=80;
$basin{'P','r30',70}=100;
$basin{'P','r30',80}=110;
$basin{'P','r30',90}=120;
$basin{'P','r30',100}=125;
$basin{'P','r30',110}=130;
$basin{'P','r30',120}=140;
$basin{'P','r30',130}=150;

$basin{'P','r50',50}=20;
$basin{'P','r50',60}=30;
$basin{'P','r50',70}=40;
$basin{'P','r50',80}=45;
$basin{'P','r50',90}=50;
$basin{'P','r50',100}=60;
$basin{'P','r50',110}=65;
$basin{'P','r50',120}=70;
$basin{'P','r50',130}=80;


$basin{'E','r30'}='2';
$basin{'W','r30'}='3';
$basin{'C','r30'}='4';
$basin{'I','r30'}='9';
$basin{'A','r30'}='5';
$basin{'B','r30'}='6';
$basin{'S','r30'}='7';
$basin{'P','r30'}='8';


$atcf{'clp','name'}='JCLP';
$atcf{'clp','namex'}='JCLX';

$atcf{'ifs','name'}='JECM';
$atcf{'ifs','namex'}='JECX';

$atcf{'ngp','name'}='JNGP';
$atcf{'ngp','namex'}='JNGX';

$atcf{'avn','name'}='JAVN';
$atcf{'avn','namex'}='JAVX';

$atcf{'ukm','name'}='JUKM';
$atcf{'ukm','namex'}='JUKX';

$atcf{'mrf','name'}='JMRF';
$atcf{'mrf','namex'}='JMRX';

$atcf{'ifs','num'}='70';
$atcf{'ifs','numx'}='70';

$atcf{'ngp','num'}='71';
$atcf{'ngp','numx'}='71';

$atcf{'avn','num'}='72';
$atcf{'avn','numx'}='72';

$atcf{'mrf','num'}='73';
$atcf{'mrf','numx'}='73';

$atcf{'ukm','num'}='74';
$atcf{'ukm','numx'}='74';

$atcf{'clp','num'}='75';
$atcf{'clp','numx'}='75';

$bname{1}='LANT';
$bname{2}='EPAC';
$bname{3}='WPAC';
$bname{4}='CPAC';
$bname{5}='ASEA';
$bname{6}='BAYB';
$bname{7}='SIO';
$bname{8}='SPAC';
$bname{9}='ALLTC';

$basin{'W'}='wpc';
$basin{'L'}='atl';
$basin{'C'}='epc';
$basin{'E'}='epc';
$basin{'P'}='aus';
$basin{'T'}='slt';
$basin{'A'}='nio';
$basin{'B'}='nio';
$basin{'I'}='nio';
$basin{'S'}='sio';


$basin_neumann{'W'}='wpc';
$basin_neumann{'L'}='atl';
$basin_neumann{'E'}='epc';
$basin_neumann{'I'}='nio';
$basin_neumann{'S'}='shm';

$sname_u2n{1995,'02A'}='02A';
$sname_n2u{1995,'02A'}='02A';
$sname_u2n{1995,'03B'}='03B';
$sname_n2u{1995,'03B'}='03B';
$sname_u2n{1995,'04B'}='04B';
$sname_n2u{1995,'04B'}='04B';
$sname_u2n{1995,'ADOLPH'}='02E';
$sname_n2u{1995,'02E'}='ADOLPH';
$sname_u2n{1995,'BARBARA'}='03E';
$sname_n2u{1995,'03E'}='BARBARA';
$sname_u2n{1995,'COSME'}='04E';
$sname_n2u{1995,'04E'}='COSME';
$sname_u2n{1995,'DALILA'}='05E';
$sname_n2u{1995,'05E'}='DALILA';
$sname_u2n{1995,'ERICK'}='06E';
$sname_n2u{1995,'06E'}='ERICK';
$sname_u2n{1995,'FLOSSIE'}='07E';
$sname_n2u{1995,'07E'}='FLOSSIE';
$sname_u2n{1995,'GIL'}='08E';
$sname_n2u{1995,'08E'}='GIL';
$sname_u2n{1995,'HENRIETTE'}='09E';
$sname_n2u{1995,'09E'}='HENRIETTE';
$sname_u2n{1995,'ISMAEL'}='10E';
$sname_n2u{1995,'10E'}='ISMAEL';
$sname_u2n{1995,'JULIETTE'}='11E';
$sname_n2u{1995,'11E'}='JULIETTE';
$sname_u2n{1995,'ALLISON'}='01L';
$sname_n2u{1995,'01L'}='ALLISON';
$sname_u2n{1995,'BARRY'}='02L';
$sname_n2u{1995,'02L'}='BARRY';
$sname_u2n{1995,'CHANTAL'}='03L';
$sname_n2u{1995,'03L'}='CHANTAL';
$sname_u2n{1995,'DEAN'}='04L';
$sname_n2u{1995,'04L'}='DEAN';
$sname_u2n{1995,'ERIN'}='05L';
$sname_n2u{1995,'05L'}='ERIN';
$sname_u2n{1995,'FELIX'}='07L';
$sname_n2u{1995,'07L'}='FELIX';
$sname_u2n{1995,'GABRIELLE'}='08L';
$sname_n2u{1995,'08L'}='GABRIELLE';
$sname_u2n{1995,'HUMBERTO'}='09L';
$sname_n2u{1995,'09L'}='HUMBERTO';
$sname_u2n{1995,'IRIS'}='10L';
$sname_n2u{1995,'10L'}='IRIS';
$sname_u2n{1995,'JERRY'}='11L';
$sname_n2u{1995,'11L'}='JERRY';
$sname_u2n{1995,'KAREN'}='12L';
$sname_n2u{1995,'12L'}='KAREN';
$sname_u2n{1995,'LUIS'}='13L';
$sname_n2u{1995,'13L'}='LUIS';
$sname_u2n{1995,'MARILYN'}='15L';
$sname_n2u{1995,'15L'}='MARILYN';
$sname_u2n{1995,'NOEL'}='16L';
$sname_n2u{1995,'16L'}='NOEL';
$sname_u2n{1995,'OPAL'}='17L';
$sname_n2u{1995,'17L'}='OPAL';
$sname_u2n{1995,'PABLO'}='18L';
$sname_n2u{1995,'18L'}='PABLO';
$sname_u2n{1995,'ROXANNE'}='19L';
$sname_n2u{1995,'19L'}='ROXANNE';
$sname_u2n{1995,'SEBASTIEN'}='20L';
$sname_n2u{1995,'20L'}='SEBASTIEN';
$sname_u2n{1995,'TANYA'}='21L';
$sname_n2u{1995,'21L'}='TANYA';
$sname_u2n{1995,'WILLIAM'}='05P';
$sname_n2u{1995,'05P'}='WILLIAM';
$sname_u2n{1995,'AGNES'}='22P';
$sname_n2u{1995,'22P'}='AGNES';
$sname_u2n{1995,'VIOLET'}='14P';
$sname_n2u{1995,'14P'}='VIOLET';
$sname_u2n{1995,'WARREN'}='15P';
$sname_n2u{1995,'15P'}='WARREN';
$sname_u2n{1995,'20S'}='20S';
$sname_n2u{1995,'20S'}='20S';
$sname_u2n{1995,'AGNIELLE'}='01S';
$sname_n2u{1995,'01S'}='AGNIELLE';
$sname_u2n{1995,'BENTHA'}='06S';
$sname_n2u{1995,'06S'}='BENTHA';
$sname_u2n{1995,'BOBBY'}='12S';
$sname_n2u{1995,'12S'}='BOBBY';
$sname_u2n{1995,'CHLOE'}='21S';
$sname_n2u{1995,'21S'}='CHLOE';
$sname_u2n{1995,'CHRISTELLE'}='07S';
$sname_n2u{1995,'07S'}='CHRISTELLE';
$sname_u2n{1995,'DORINA'}='08S';
$sname_n2u{1995,'08S'}='DORINA';
$sname_u2n{1995,'EMMA'}='02S';
$sname_n2u{1995,'02S'}='EMMA';
$sname_u2n{1995,'FODAH'}='09S';
$sname_n2u{1995,'09S'}='FODAH';
$sname_u2n{1995,'FRANK'}='03S';
$sname_n2u{1995,'03S'}='FRANK';
$sname_u2n{1995,'GAIL'}='10S';
$sname_n2u{1995,'10S'}='GAIL';
$sname_u2n{1995,'GERTIE'}='04S';
$sname_n2u{1995,'04S'}='GERTIE';
$sname_u2n{1995,'HEIDA'}='11S';
$sname_n2u{1995,'11S'}='HEIDA';
$sname_u2n{1995,'INGRID'}='13S';
$sname_n2u{1995,'13S'}='INGRID';
$sname_u2n{1995,'JOSTA'}='16S';
$sname_n2u{1995,'16S'}='JOSTA';
$sname_u2n{1995,'KYLIE'}='17S';
$sname_n2u{1995,'17S'}='KYLIE';
$sname_u2n{1995,'MARLENE'}='19S';
$sname_n2u{1995,'19S'}='MARLENE';
$sname_u2n{1995,'01B'}='16W';
$sname_n2u{1995,'16W'}='01B';
$sname_u2n{1995,'ANGELA'}='29W';
$sname_n2u{1995,'29W'}='ANGELA';
$sname_u2n{1995,'BRIAN'}='30W';
$sname_n2u{1995,'30W'}='BRIAN';
$sname_u2n{1995,'CHUCK'}='02W';
$sname_n2u{1995,'02W'}='CHUCK';
$sname_u2n{1995,'COLLEEN'}='31W';
$sname_n2u{1995,'31W'}='COLLEEN';
$sname_u2n{1995,'DAN'}='35W';
$sname_n2u{1995,'35W'}='DAN';
$sname_u2n{1995,'DEANNA'}='03W';
$sname_n2u{1995,'03W'}='DEANNA';
$sname_u2n{1995,'ELI'}='04W';
$sname_n2u{1995,'04W'}='ELI';
$sname_u2n{1995,'FAYE'}='05W';
$sname_n2u{1995,'05W'}='FAYE';
$sname_u2n{1995,'GARY'}='07W';
$sname_n2u{1995,'07W'}='GARY';
$sname_u2n{1995,'HELEN'}='08W';
$sname_n2u{1995,'08W'}='HELEN';
$sname_u2n{1995,'IRVING'}='09W';
$sname_n2u{1995,'09W'}='IRVING';
$sname_u2n{1995,'JANIS'}='10W';
$sname_n2u{1995,'10W'}='JANIS';
$sname_u2n{1995,'KENT'}='12W';
$sname_n2u{1995,'12W'}='KENT';
$sname_u2n{1995,'LOIS'}='13W';
$sname_n2u{1995,'13W'}='LOIS';
$sname_u2n{1995,'MARK'}='14W';
$sname_n2u{1995,'14W'}='MARK';
$sname_u2n{1995,'NINA'}='15W';
$sname_n2u{1995,'15W'}='NINA';
$sname_u2n{1995,'OSCAR'}='17W';
$sname_n2u{1995,'17W'}='OSCAR';
$sname_u2n{1995,'POLLY'}='18W';
$sname_n2u{1995,'18W'}='POLLY';
$sname_u2n{1995,'RYAN'}='19W';
$sname_n2u{1995,'19W'}='RYAN';
$sname_u2n{1995,'SIBYL'}='20W';
$sname_n2u{1995,'20W'}='SIBYL';
$sname_u2n{1995,'TED'}='24W';
$sname_n2u{1995,'24W'}='TED';
$sname_u2n{1995,'VAL'}='25W';
$sname_n2u{1995,'25W'}='VAL';
$sname_u2n{1995,'WARD'}='26W';
$sname_n2u{1995,'26W'}='WARD';
$sname_u2n{1995,'YVETTE'}='27W';
$sname_n2u{1995,'27W'}='YVETTE';
$sname_u2n{1995,'ZACK'}='28W';
$sname_n2u{1995,'28W'}='ZACK';
$sname_u2n{1996,'02A'}='02A';
$sname_n2u{1996,'02A'}='02A';
$sname_u2n{1996,'15S'}='15S';
$sname_n2u{1996,'15S'}='15S';
$sname_u2n{1996,'ARTHUR'}='01L';
$sname_n2u{1996,'01L'}='ARTHUR';
$sname_u2n{1996,'CHANTELLE'}='07S';
$sname_n2u{1996,'07S'}='CHANTELLE';
$sname_u2n{1996,'FERGUS'}='13P';
$sname_n2u{1996,'13P'}='FERGUS';
$sname_u2n{1996,'LINDSAY'}='01S';
$sname_n2u{1996,'01S'}='LINDSAY';
$sname_u2n{1996,'OPHELIA'}='11S';
$sname_n2u{1996,'11S'}='OPHELIA';
$sname_u2n{1996,'ZAKA'}='20P';
$sname_n2u{1996,'20P'}='ZAKA';
$sname_u2n{1996,'04A'}='04A';
$sname_n2u{1996,'04A'}='04A';
$sname_u2n{1996,'05A'}='05A';
$sname_n2u{1996,'05A'}='05A';
$sname_u2n{1996,'01B'}='01B';
$sname_n2u{1996,'01B'}='01B';
$sname_u2n{1996,'03B'}='03B';
$sname_n2u{1996,'03B'}='03B';
$sname_u2n{1996,'06B'}='06B';
$sname_n2u{1996,'06B'}='06B';
$sname_u2n{1996,'07B'}='07B';
$sname_n2u{1996,'07B'}='07B';
$sname_u2n{1996,'08B'}='08B';
$sname_n2u{1996,'08B'}='08B';
$sname_u2n{1996,'ALMA'}='03E';
$sname_n2u{1996,'03E'}='ALMA';
$sname_u2n{1996,'BORIS'}='04E';
$sname_n2u{1996,'04E'}='BORIS';
$sname_u2n{1996,'CRISTINA'}='05E';
$sname_n2u{1996,'05E'}='CRISTINA';
$sname_u2n{1996,'DOUGLAS'}='07E';
$sname_n2u{1996,'07E'}='DOUGLAS';
$sname_u2n{1996,'ELIDA'}='08E';
$sname_n2u{1996,'08E'}='ELIDA';
$sname_u2n{1996,'FAUSTO'}='09E';
$sname_n2u{1996,'09E'}='FAUSTO';
$sname_u2n{1996,'GENEVIEVE'}='10E';
$sname_n2u{1996,'10E'}='GENEVIEVE';
$sname_u2n{1996,'HERNAN'}='11E';
$sname_n2u{1996,'11E'}='HERNAN';
$sname_u2n{1996,'BERTHA'}='02L';
$sname_n2u{1996,'02L'}='BERTHA';
$sname_u2n{1996,'CESAR'}='03L';
$sname_n2u{1996,'03L'}='CESAR';
$sname_u2n{1996,'DOLLY'}='04L';
$sname_n2u{1996,'04L'}='DOLLY';
$sname_u2n{1996,'EDOUARD'}='05L';
$sname_n2u{1996,'05L'}='EDOUARD';
$sname_u2n{1996,'FRAN'}='06L';
$sname_n2u{1996,'06L'}='FRAN';
$sname_u2n{1996,'GUSTAV'}='07L';
$sname_n2u{1996,'07L'}='GUSTAV';
$sname_u2n{1996,'HORTENSE'}='08L';
$sname_n2u{1996,'08L'}='HORTENSE';
$sname_u2n{1996,'ISIDORE'}='09L';
$sname_n2u{1996,'09L'}='ISIDORE';
$sname_u2n{1996,'JOSEPHINE'}='10L';
$sname_n2u{1996,'10L'}='JOSEPHINE';
$sname_u2n{1996,'KYLE'}='11L';
$sname_n2u{1996,'11L'}='KYLE';
$sname_u2n{1996,'LILI'}='12L';
$sname_n2u{1996,'12L'}='LILI';
$sname_u2n{1996,'MARCO'}='13L';
$sname_n2u{1996,'13L'}='MARCO';
$sname_u2n{1996,'ATU'}='21P';
$sname_n2u{1996,'21P'}='ATU';
$sname_u2n{1996,'BARRY'}='05P';
$sname_n2u{1996,'05P'}='BARRY';
$sname_u2n{1996,'BETI'}='23P';
$sname_n2u{1996,'23P'}='BETI';
$sname_u2n{1996,'CELESTE'}='09P';
$sname_n2u{1996,'09P'}='CELESTE';
$sname_u2n{1996,'CYRIL'}='06P';
$sname_n2u{1996,'06P'}='CYRIL';
$sname_u2n{1996,'DENNIS'}='13P';
$sname_n2u{1996,'13P'}='DENNIS';
$sname_u2n{1996,'JACOB'}='10P';
$sname_n2u{1996,'10P'}='JACOB';
$sname_u2n{1996,'PHIL'}='12P';
$sname_n2u{1996,'12P'}='PHIL';
$sname_u2n{1996,'YASI'}='08P';
$sname_n2u{1996,'08P'}='YASI';
$sname_u2n{1996,'02S'}='02S';
$sname_n2u{1996,'02S'}='02S';
$sname_u2n{1996,'03S'}='03S';
$sname_n2u{1996,'03S'}='03S';
$sname_u2n{1996,'12S'}='12S';
$sname_n2u{1996,'12S'}='12S';
$sname_u2n{1996,'ANTOINETTE'}='04S';
$sname_n2u{1996,'04S'}='ANTOINETTE';
$sname_u2n{1996,'BELLAMINE'}='05S';
$sname_n2u{1996,'05S'}='BELLAMINE';
$sname_u2n{1996,'BONITA'}='06S';
$sname_n2u{1996,'06S'}='BONITA';
$sname_u2n{1996,'DANIELLA'}='08S';
$sname_n2u{1996,'08S'}='DANIELLA';
$sname_u2n{1996,'DOLORESSE'}='14S';
$sname_n2u{1996,'14S'}='DOLORESSE';
$sname_u2n{1996,'EDWIGE'}='16S';
$sname_n2u{1996,'16S'}='EDWIGE';
$sname_u2n{1996,'ELVINA'}='09S';
$sname_n2u{1996,'09S'}='ELVINA';
$sname_u2n{1996,'ETHEL'}='19P';
$sname_n2u{1996,'19P'}='ETHEL';
$sname_u2n{1996,'FLOSSY'}='17S';
$sname_n2u{1996,'17S'}='FLOSSY';
$sname_u2n{1996,'GUYLIANNE'}='22S';
$sname_n2u{1996,'22S'}='GUYLIANNE';
$sname_u2n{1996,'HANSELLA'}='24S';
$sname_n2u{1996,'24S'}='HANSELLA';
$sname_u2n{1996,'HUBERT'}='07S';
$sname_n2u{1996,'07S'}='HUBERT';
$sname_u2n{1996,'ISOBEL'}='11S';
$sname_n2u{1996,'11S'}='ISOBEL';
$sname_u2n{1996,'ITELLE'}='26S';
$sname_n2u{1996,'26S'}='ITELLE';
$sname_u2n{1996,'JENNA'}='28S';
$sname_n2u{1996,'28S'}='JENNA';
$sname_u2n{1996,'KIRSTY'}='18S';
$sname_n2u{1996,'18S'}='KIRSTY';
$sname_u2n{1996,'NICHOLAS'}='10S';
$sname_n2u{1996,'10S'}='NICHOLAS';
$sname_u2n{1996,'OLIVIA'}='25S';
$sname_n2u{1996,'25S'}='OLIVIA';
$sname_u2n{1996,'ABEL'}='30W';
$sname_n2u{1996,'30W'}='ABEL';
$sname_u2n{1996,'ANN'}='02W';
$sname_n2u{1996,'02W'}='ANN';
$sname_u2n{1996,'BART'}='04W';
$sname_n2u{1996,'04W'}='BART';
$sname_u2n{1996,'BETH'}='32W';
$sname_n2u{1996,'32W'}='BETH';
$sname_u2n{1996,'CAM'}='05W';
$sname_n2u{1996,'05W'}='CAM';
$sname_u2n{1996,'CARLO'}='33W';
$sname_n2u{1996,'33W'}='CARLO';
$sname_u2n{1996,'DALE'}='36W';
$sname_n2u{1996,'36W'}='DALE';
$sname_u2n{1996,'DAN'}='06W';
$sname_n2u{1996,'06W'}='DAN';
$sname_u2n{1996,'ERNIE'}='37W';
$sname_n2u{1996,'37W'}='ERNIE';
$sname_u2n{1996,'EVE'}='07W';
$sname_n2u{1996,'07W'}='EVE';
$sname_u2n{1996,'FERN'}='42W';
$sname_n2u{1996,'42W'}='FERN';
$sname_u2n{1996,'FRANKIE'}='08W';
$sname_n2u{1996,'08W'}='FRANKIE';
$sname_u2n{1996,'GLORIA'}='09W';
$sname_n2u{1996,'09W'}='GLORIA';
$sname_u2n{1996,'GREG'}='43W';
$sname_n2u{1996,'43W'}='GREG';
$sname_u2n{1996,'HERB'}='10W';
$sname_n2u{1996,'10W'}='HERB';
$sname_u2n{1996,'IAN'}='11W';
$sname_n2u{1996,'11W'}='IAN';
$sname_u2n{1996,'JOY'}='12W';
$sname_n2u{1996,'12W'}='JOY';
$sname_u2n{1996,'KIRK'}='13W';
$sname_n2u{1996,'13W'}='KIRK';
$sname_u2n{1996,'LISA'}='14W';
$sname_n2u{1996,'14W'}='LISA';
$sname_u2n{1996,'MARTY'}='16W';
$sname_n2u{1996,'16W'}='MARTY';
$sname_u2n{1996,'NIKI'}='18W';
$sname_n2u{1996,'18W'}='NIKI';
$sname_u2n{1996,'ORSON'}='19W';
$sname_n2u{1996,'19W'}='ORSON';
$sname_u2n{1996,'PIPER'}='20W';
$sname_n2u{1996,'20W'}='PIPER';
$sname_u2n{1996,'RICK'}='22W';
$sname_n2u{1996,'22W'}='RICK';
$sname_u2n{1996,'SALLY'}='23W';
$sname_n2u{1996,'23W'}='SALLY';
$sname_u2n{1996,'TOM'}='25W';
$sname_n2u{1996,'25W'}='TOM';
$sname_u2n{1996,'VIOLET'}='26W';
$sname_n2u{1996,'26W'}='VIOLET';
$sname_u2n{1996,'WILLIE'}='27W';
$sname_n2u{1996,'27W'}='WILLIE';
$sname_u2n{1996,'YATES'}='28W';
$sname_n2u{1996,'28W'}='YATES';
$sname_u2n{1996,'ZANE'}='29W';
$sname_n2u{1996,'29W'}='ZANE';
$sname_u2n{1997,'03A'}='03A';
$sname_n2u{1997,'03A'}='03A';
$sname_u2n{1997,'12P'}='12P';
$sname_n2u{1997,'12P'}='12P';
$sname_u2n{1997,'29P'}='29P';
$sname_n2u{1997,'29P'}='29P';
$sname_u2n{1997,'04A'}='04A';
$sname_n2u{1997,'04A'}='04A';
$sname_u2n{1997,'01B'}='01B';
$sname_n2u{1997,'01B'}='01B';
$sname_u2n{1997,'02B'}='02B';
$sname_n2u{1997,'02B'}='02B';
$sname_u2n{1997,'OLIWA'}='02C';
$sname_n2u{1997,'02C'}='OLIWA';
$sname_u2n{1997,'PAKA'}='05C';
$sname_n2u{1997,'05C'}='PAKA';
$sname_u2n{1997,'ANDRES'}='01E';
$sname_n2u{1997,'01E'}='ANDRES';
$sname_u2n{1997,'BLANCA'}='02E';
$sname_n2u{1997,'02E'}='BLANCA';
$sname_u2n{1997,'CARLOS'}='04E';
$sname_n2u{1997,'04E'}='CARLOS';
$sname_u2n{1997,'DOLORES'}='06E';
$sname_n2u{1997,'06E'}='DOLORES';
$sname_u2n{1997,'ENRIQUE'}='07E';
$sname_n2u{1997,'07E'}='ENRIQUE';
$sname_u2n{1997,'FELICIA'}='08E';
$sname_n2u{1997,'08E'}='FELICIA';
$sname_u2n{1997,'GUILLERMO'}='09E';
$sname_n2u{1997,'09E'}='GUILLERMO';
$sname_u2n{1997,'HILDA'}='10E';
$sname_n2u{1997,'10E'}='HILDA';
$sname_u2n{1997,'IGNACIO'}='11E';
$sname_n2u{1997,'11E'}='IGNACIO';
$sname_u2n{1997,'JIMENA'}='12E';
$sname_n2u{1997,'12E'}='JIMENA';
$sname_u2n{1997,'KEVIN'}='13E';
$sname_n2u{1997,'13E'}='KEVIN';
$sname_u2n{1997,'LINDA_NEP'}='14E';
$sname_n2u{1997,'14E'}='LINDA_NEP';
$sname_u2n{1997,'MARTY'}='15E';
$sname_n2u{1997,'15E'}='MARTY';
$sname_u2n{1997,'NORA'}='16E';
$sname_n2u{1997,'16E'}='NORA';
$sname_u2n{1997,'OLAF'}='17E';
$sname_n2u{1997,'17E'}='OLAF';
$sname_u2n{1997,'PAULINE'}='18E';
$sname_n2u{1997,'18E'}='PAULINE';
$sname_u2n{1997,'RICK'}='19E';
$sname_n2u{1997,'19E'}='RICK';
$sname_u2n{1997,'ANA'}='01L';
$sname_n2u{1997,'01L'}='ANA';
$sname_u2n{1997,'BILL'}='02L';
$sname_n2u{1997,'02L'}='BILL';
$sname_u2n{1997,'CLAUDETTE'}='03L';
$sname_n2u{1997,'03L'}='CLAUDETTE';
$sname_u2n{1997,'DANNY'}='04L';
$sname_n2u{1997,'04L'}='DANNY';
$sname_u2n{1997,'ERIKA'}='06L';
$sname_n2u{1997,'06L'}='ERIKA';
$sname_u2n{1997,'FABIAN'}='07L';
$sname_n2u{1997,'07L'}='FABIAN';
$sname_u2n{1997,'GRACE'}='08L';
$sname_n2u{1997,'08L'}='GRACE';
$sname_u2n{1997,'03P'}='03P';
$sname_n2u{1997,'03P'}='03P';
$sname_u2n{1997,'37P'}='37P';
$sname_n2u{1997,'37P'}='37P';
$sname_u2n{1997,'DRENA'}='16P';
$sname_n2u{1997,'16P'}='DRENA';
$sname_u2n{1997,'EVAN'}='17P';
$sname_n2u{1997,'17P'}='EVAN';
$sname_u2n{1997,'FREDA'}='22P';
$sname_n2u{1997,'22P'}='FREDA';
$sname_u2n{1997,'GAVIN'}='31P';
$sname_n2u{1997,'31P'}='GAVIN';
$sname_u2n{1997,'GILLIAN'}='24P';
$sname_n2u{1997,'24P'}='GILLIAN';
$sname_u2n{1997,'HAROLD'}='26P';
$sname_n2u{1997,'26P'}='HAROLD';
$sname_u2n{1997,'HINA'}='33P';
$sname_n2u{1997,'33P'}='HINA';
$sname_u2n{1997,'IAN'}='34P';
$sname_n2u{1997,'34P'}='IAN';
$sname_u2n{1997,'ITA'}='28P';
$sname_n2u{1997,'28P'}='ITA';
$sname_u2n{1997,'JUNE'}='35P';
$sname_n2u{1997,'35P'}='JUNE';
$sname_u2n{1997,'JUSTIN'}='32P';
$sname_n2u{1997,'32P'}='JUSTIN';
$sname_u2n{1997,'KELI'}='38P';
$sname_n2u{1997,'38P'}='KELI';
$sname_u2n{1997,'LUSI'}='02P';
$sname_n2u{1997,'02P'}='LUSI';
$sname_u2n{1997,'MARTIN'}='04P';
$sname_n2u{1997,'04P'}='MARTIN';
$sname_u2n{1997,'NUTE'}='05P';
$sname_n2u{1997,'05P'}='NUTE';
$sname_u2n{1997,'OSEA'}='06P';
$sname_n2u{1997,'06P'}='OSEA';
$sname_u2n{1997,'PAM'}='07P';
$sname_n2u{1997,'07P'}='PAM';
$sname_u2n{1997,'PHIL'}='12P';
$sname_n2u{1997,'12P'}='PHIL';
$sname_u2n{1997,'01S'}='01S';
$sname_n2u{1997,'01S'}='01S';
$sname_u2n{1997,'18S'}='18S';
$sname_n2u{1997,'18S'}='18S';
$sname_u2n{1997,'27S'}='27S';
$sname_n2u{1997,'27S'}='27S';
$sname_u2n{1997,'FABRIOLA'}='14S';
$sname_n2u{1997,'14S'}='FABRIOLA';
$sname_u2n{1997,'GRETELLE'}='20S';
$sname_n2u{1997,'20S'}='GRETELLE';
$sname_u2n{1997,'ILETTA'}='21S';
$sname_n2u{1997,'21S'}='ILETTA';
$sname_u2n{1997,'JOSIE'}='23S';
$sname_n2u{1997,'23S'}='JOSIE';
$sname_u2n{1997,'KARLETTE'}='25S';
$sname_n2u{1997,'25S'}='KARLETTE';
$sname_u2n{1997,'LISETTE'}='30S';
$sname_n2u{1997,'30S'}='LISETTE';
$sname_u2n{1997,'PANCHO'}='19S';
$sname_n2u{1997,'19S'}='PANCHO';
$sname_u2n{1997,'RACHEL'}='15S';
$sname_n2u{1997,'15S'}='RACHEL';
$sname_u2n{1997,'RHONDA'}='36S';
$sname_n2u{1997,'36S'}='RHONDA';
$sname_u2n{1997,'SELWYN'}='09S';
$sname_n2u{1997,'09S'}='SELWYN';
$sname_u2n{1997,'SID'}='08S';
$sname_n2u{1997,'08S'}='SID';
$sname_u2n{1997,'AMBER'}='18W';
$sname_n2u{1997,'18W'}='AMBER';
$sname_u2n{1997,'BING'}='19W';
$sname_n2u{1997,'19W'}='BING';
$sname_u2n{1997,'CASS'}='20W';
$sname_n2u{1997,'20W'}='CASS';
$sname_u2n{1997,'DAVID'}='21W';
$sname_n2u{1997,'21W'}='DAVID';
$sname_u2n{1997,'ELLA'}='23W';
$sname_n2u{1997,'23W'}='ELLA';
$sname_u2n{1997,'FRITZ'}='22W';
$sname_n2u{1997,'22W'}='FRITZ';
$sname_u2n{1997,'GINGER'}='24W';
$sname_n2u{1997,'24W'}='GINGER';
$sname_u2n{1997,'HANK'}='25W';
$sname_n2u{1997,'25W'}='HANK';
$sname_u2n{1997,'HANNAH'}='01W';
$sname_n2u{1997,'01W'}='HANNAH';
$sname_u2n{1997,'ISA'}='02W';
$sname_n2u{1997,'02W'}='ISA';
$sname_u2n{1997,'IVAN'}='27W';
$sname_n2u{1997,'27W'}='IVAN';
$sname_u2n{1997,'JIMMY'}='03W';
$sname_n2u{1997,'03W'}='JIMMY';
$sname_u2n{1997,'JOAN'}='28W';
$sname_n2u{1997,'28W'}='JOAN';
$sname_u2n{1997,'KEITH'}='29W';
$sname_n2u{1997,'29W'}='KEITH';
$sname_u2n{1997,'KELLY'}='04W';
$sname_n2u{1997,'04W'}='KELLY';
$sname_u2n{1997,'LEVI'}='05W';
$sname_n2u{1997,'05W'}='LEVI';
$sname_u2n{1997,'LINDA_NI'}='30W';
$sname_n2u{1997,'30W'}='LINDA_NI';
$sname_u2n{1997,'MARIE'}='06W';
$sname_n2u{1997,'06W'}='MARIE';
$sname_u2n{1997,'MORT'}='31W';
$sname_n2u{1997,'31W'}='MORT';
$sname_u2n{1997,'NESTOR'}='07W';
$sname_n2u{1997,'07W'}='NESTOR';
$sname_u2n{1997,'OPAL'}='08W';
$sname_n2u{1997,'08W'}='OPAL';
$sname_u2n{1997,'PETER'}='09W';
$sname_n2u{1997,'09W'}='PETER';
$sname_u2n{1997,'ROSIE'}='10W';
$sname_n2u{1997,'10W'}='ROSIE';
$sname_u2n{1997,'SCOTT'}='11W';
$sname_n2u{1997,'11W'}='SCOTT';
$sname_u2n{1997,'TINA'}='12W';
$sname_n2u{1997,'12W'}='TINA';
$sname_u2n{1997,'VICTOR'}='13W';
$sname_n2u{1997,'13W'}='VICTOR';
$sname_u2n{1997,'WINNIE'}='14W';
$sname_n2u{1997,'14W'}='WINNIE';
$sname_u2n{1997,'YULE'}='16W';
$sname_n2u{1997,'16W'}='YULE';
$sname_u2n{1997,'ZITA'}='17W';
$sname_n2u{1997,'17W'}='ZITA';
$sname_u2n{1998,'TUI'}='00P';
$sname_n2u{1998,'00P'}='TUI';
$sname_u2n{1998,'02A'}='02A';
$sname_n2u{1998,'02A'}='02A';
$sname_u2n{1998,'03A'}='03A';
$sname_n2u{1998,'03A'}='03A';
$sname_u2n{1998,'04A'}='04A';
$sname_n2u{1998,'04A'}='04A';
$sname_u2n{1998,'05A'}='05A';
$sname_n2u{1998,'05A'}='05A';
$sname_u2n{1998,'08A'}='08A';
$sname_n2u{1998,'08A'}='08A';
$sname_u2n{1998,'01B'}='01B';
$sname_n2u{1998,'01B'}='01B';
$sname_u2n{1998,'06B'}='06B';
$sname_n2u{1998,'06B'}='06B';
$sname_u2n{1998,'07B'}='07B';
$sname_n2u{1998,'07B'}='07B';
$sname_u2n{1998,'AGATHA'}='01E';
$sname_n2u{1998,'01E'}='AGATHA';
$sname_u2n{1998,'BLAS'}='03E';
$sname_n2u{1998,'03E'}='BLAS';
$sname_u2n{1998,'CELIA'}='04E';
$sname_n2u{1998,'04E'}='CELIA';
$sname_u2n{1998,'DARBY'}='05E';
$sname_n2u{1998,'05E'}='DARBY';
$sname_u2n{1998,'ESTELLE'}='06E';
$sname_n2u{1998,'06E'}='ESTELLE';
$sname_u2n{1998,'FRANK'}='07E';
$sname_n2u{1998,'07E'}='FRANK';
$sname_u2n{1998,'GEORGETTE'}='08E';
$sname_n2u{1998,'08E'}='GEORGETTE';
$sname_u2n{1998,'HOWARD'}='09E';
$sname_n2u{1998,'09E'}='HOWARD';
$sname_u2n{1998,'ISIS'}='10E';
$sname_n2u{1998,'10E'}='ISIS';
$sname_u2n{1998,'JAVIER'}='11E';
$sname_n2u{1998,'11E'}='JAVIER';
$sname_u2n{1998,'KAY'}='13E';
$sname_n2u{1998,'13E'}='KAY';
$sname_u2n{1998,'LESTER'}='14E';
$sname_n2u{1998,'14E'}='LESTER';
$sname_u2n{1998,'MADELINE'}='15E';
$sname_n2u{1998,'15E'}='MADELINE';
$sname_u2n{1998,'ALEX_NAT'}='01L';
$sname_n2u{1998,'01L'}='ALEX_NAT';
$sname_u2n{1998,'BONNIE'}='02L';
$sname_n2u{1998,'02L'}='BONNIE';
$sname_u2n{1998,'CHARLEY'}='03L';
$sname_n2u{1998,'03L'}='CHARLEY';
$sname_u2n{1998,'DANIELLE'}='04L';
$sname_n2u{1998,'04L'}='DANIELLE';
$sname_u2n{1998,'EARL'}='05L';
$sname_n2u{1998,'05L'}='EARL';
$sname_u2n{1998,'FRANCES'}='06L';
$sname_n2u{1998,'06L'}='FRANCES';
$sname_u2n{1998,'GEORGES'}='07L';
$sname_n2u{1998,'07L'}='GEORGES';
$sname_u2n{1998,'HERMINE'}='08L';
$sname_n2u{1998,'08L'}='HERMINE';
$sname_u2n{1998,'IVAN'}='09L';
$sname_n2u{1998,'09L'}='IVAN';
$sname_u2n{1998,'JEANNE'}='10L';
$sname_n2u{1998,'10L'}='JEANNE';
$sname_u2n{1998,'KARL'}='11L';
$sname_n2u{1998,'11L'}='KARL';
$sname_u2n{1998,'LISA'}='12L';
$sname_n2u{1998,'12L'}='LISA';
$sname_u2n{1998,'MITCH'}='13L';
$sname_n2u{1998,'13L'}='MITCH';
$sname_u2n{1998,'NICOLE'}='14L';
$sname_n2u{1998,'14L'}='NICOLE';
$sname_u2n{1998,'08P'}='08P';
$sname_n2u{1998,'08P'}='08P';
$sname_u2n{1998,'ALAN'}='32P';
$sname_n2u{1998,'32P'}='ALAN';
$sname_u2n{1998,'BART'}='37P';
$sname_n2u{1998,'37P'}='BART';
$sname_u2n{1998,'CORA'}='09P';
$sname_n2u{1998,'09P'}='CORA';
$sname_u2n{1998,'KATRINA'}='12P';
$sname_n2u{1998,'12P'}='KATRINA';
$sname_u2n{1998,'LES'}='14P';
$sname_n2u{1998,'14P'}='LES';
$sname_u2n{1998,'MAY'}='25P';
$sname_n2u{1998,'25P'}='MAY';
$sname_u2n{1998,'NATHAN'}='30P';
$sname_n2u{1998,'30P'}='NATHAN';
$sname_u2n{1998,'RON'}='10P';
$sname_n2u{1998,'10P'}='RON';
$sname_u2n{1998,'SUSAN'}='11P';
$sname_n2u{1998,'11P'}='SUSAN';
$sname_u2n{1998,'URSULA'}='17P';
$sname_n2u{1998,'17P'}='URSULA';
$sname_u2n{1998,'VELI'}='18P';
$sname_n2u{1998,'18P'}='VELI';
$sname_u2n{1998,'WES'}='19P';
$sname_n2u{1998,'19P'}='WES';
$sname_u2n{1998,'YALI'}='29P';
$sname_n2u{1998,'29P'}='YALI';
$sname_u2n{1998,'ZUMAN'}='31P';
$sname_n2u{1998,'31P'}='ZUMAN';
$sname_u2n{1998,'02S'}='02S';
$sname_n2u{1998,'02S'}='02S';
$sname_u2n{1998,'13S'}='13S';
$sname_n2u{1998,'13S'}='13S';
$sname_u2n{1998,'34S'}='34S';
$sname_n2u{1998,'34S'}='34S';
$sname_u2n{1998,'ALISON'}='04S';
$sname_n2u{1998,'04S'}='ALISON';
$sname_u2n{1998,'ANACELLE'}='20S';
$sname_n2u{1998,'20S'}='ANACELLE';
$sname_u2n{1998,'BELTANE'}='23S';
$sname_n2u{1998,'23S'}='BELTANE';
$sname_u2n{1998,'BILLY'}='05S';
$sname_n2u{1998,'05S'}='BILLY';
$sname_u2n{1998,'CATHY'}='10S';
$sname_n2u{1998,'10S'}='CATHY';
$sname_u2n{1998,'DONALINE'}='26S';
$sname_n2u{1998,'26S'}='DONALINE';
$sname_u2n{1998,'ELSIE'}='27S';
$sname_n2u{1998,'27S'}='ELSIE';
$sname_u2n{1998,'FIONA'}='28S';
$sname_n2u{1998,'28S'}='FIONA';
$sname_u2n{1998,'GEMMA'}='32S';
$sname_n2u{1998,'32S'}='GEMMA';
$sname_u2n{1998,'THELMA'}='06S';
$sname_n2u{1998,'06S'}='THELMA';
$sname_u2n{1998,'TIFFANY'}='15S';
$sname_n2u{1998,'15S'}='TIFFANY';
$sname_u2n{1998,'VICTOR'}='22S';
$sname_n2u{1998,'22S'}='VICTOR';
$sname_u2n{1998,'ZELIA'}='03S';
$sname_n2u{1998,'03S'}='ZELIA';
$sname_u2n{1998,'ALEX'}='19W';
$sname_n2u{1998,'19W'}='ALEX';
$sname_u2n{1998,'BABS'}='20W';
$sname_n2u{1998,'20W'}='BABS';
$sname_u2n{1998,'CHIP'}='21W';
$sname_n2u{1998,'21W'}='CHIP';
$sname_u2n{1998,'DAWN'}='22W';
$sname_n2u{1998,'22W'}='DAWN';
$sname_u2n{1998,'ELVIS'}='23W';
$sname_n2u{1998,'23W'}='ELVIS';
$sname_u2n{1998,'FAITH'}='24W';
$sname_n2u{1998,'24W'}='FAITH';
$sname_u2n{1998,'GIL'}='25W';
$sname_n2u{1998,'25W'}='GIL';
$sname_u2n{1998,'NICHOLE'}='02W';
$sname_n2u{1998,'02W'}='NICHOLE';
$sname_u2n{1998,'OTTO'}='04W';
$sname_n2u{1998,'04W'}='OTTO';
$sname_u2n{1998,'PENNY'}='05W';
$sname_n2u{1998,'05W'}='PENNY';
$sname_u2n{1998,'REX'}='06W';
$sname_n2u{1998,'06W'}='REX';
$sname_u2n{1998,'STELLA'}='08W';
$sname_n2u{1998,'08W'}='STELLA';
$sname_u2n{1998,'TODD'}='10W';
$sname_n2u{1998,'10W'}='TODD';
$sname_u2n{1998,'VICKI'}='11W';
$sname_n2u{1998,'11W'}='VICKI';
$sname_u2n{1998,'WALDO'}='13W';
$sname_n2u{1998,'13W'}='WALDO';
$sname_u2n{1998,'YANNI'}='14W';
$sname_n2u{1998,'14W'}='YANNI';
$sname_u2n{1998,'ZEB'}='18W';
$sname_n2u{1998,'18W'}='ZEB';
$sname_u2n{1999,'02A'}='02A';
$sname_n2u{1999,'02A'}='02A';
$sname_u2n{1999,'01B'}='01B';
$sname_n2u{1999,'01B'}='01B';
$sname_u2n{1999,'03B'}='03B';
$sname_n2u{1999,'03B'}='03B';
$sname_u2n{1999,'DANI'}='11P';
$sname_n2u{1999,'11P'}='DANI';
$sname_u2n{1999,'ELLA'}='19P';
$sname_n2u{1999,'19P'}='ELLA';
$sname_u2n{1999,'FRANK'}='22P';
$sname_n2u{1999,'22P'}='FRANK';
$sname_u2n{1999,'GITA'}='24P';
$sname_n2u{1999,'24P'}='GITA';
$sname_u2n{1999,'HALI'}='27P';
$sname_n2u{1999,'27P'}='HALI';
$sname_u2n{1999,'OLINDA'}='13P';
$sname_n2u{1999,'13P'}='OLINDA';
$sname_u2n{1999,'PETE'}='14P';
$sname_n2u{1999,'14P'}='PETE';
$sname_u2n{1999,'RONA'}='20P';
$sname_n2u{1999,'20P'}='RONA';
$sname_u2n{1999,'18S'}='18S';
$sname_n2u{1999,'18S'}='18S';
$sname_u2n{1999,'21S'}='21S';
$sname_n2u{1999,'21S'}='21S';
$sname_u2n{1999,'ALDA'}='12S';
$sname_n2u{1999,'12S'}='ALDA';
$sname_u2n{1999,'CHIKITA'}='17S';
$sname_n2u{1999,'17S'}='CHIKITA';
$sname_u2n{1999,'DAMIEN'}='15S';
$sname_n2u{1999,'15S'}='DAMIEN';
$sname_u2n{1999,'DAVINA'}='25S';
$sname_n2u{1999,'25S'}='DAVINA';
$sname_u2n{1999,'ELAINE'}='28S';
$sname_n2u{1999,'28S'}='ELAINE';
$sname_u2n{1999,'EVRINA'}='31S';
$sname_n2u{1999,'31S'}='EVRINA';
$sname_u2n{1999,'GWENDA'}='32S';
$sname_n2u{1999,'32S'}='GWENDA';
$sname_u2n{1999,'HAMISH'}='33S';
$sname_n2u{1999,'33S'}='HAMISH';
$sname_u2n{1999,'VANCE'}='30S';
$sname_n2u{1999,'30S'}='VANCE';
$sname_u2n{1999,'HILDA'}='01W';
$sname_n2u{1999,'01W'}='HILDA';
$sname_u2n{1999,'IRIS'}='02W';
$sname_n2u{1999,'02W'}='IRIS';
$sname_u2n{1999,'JACOB'}='03W';
$sname_n2u{1999,'03W'}='JACOB';
$sname_u2n{1999,'KATE'}='04W';
$sname_n2u{1999,'04W'}='KATE';
$sname_u2n{1999,'LEO'}='05W';
$sname_n2u{1999,'05W'}='LEO';
$sname_u2n{1999,'MAGGIE'}='06W';
$sname_n2u{1999,'06W'}='MAGGIE';

}

sub dist_err{

local(
      $blat,$blon,$blat1,$blon1,$flat,$flon) = @_;

local($xa,$ya,$xb,$yb,$xr,$yr,$rr,$factor);

($xa,$ya)=&mercat($flat,$flon);
($xb,$yb)=&mercat($blat,$blon);
($xr,$yr)=&mercat($blat1,$blon1);

$difx=$xb-$xr;
$dify=$yb-$yr;

if ($difx == 0.0) {
  $theta=0.0 if($dify > 0.0);
  $theta=$pi if($dify < 0.0);

} else {
  $slope=$dify/$difx;
  if (abs($slope) < 1e-10) {
    $theta=$pi2 if($difx > 0) ;
    $theta=3*$pi/2.0 if($difx < 0) ;
  }  else {
    $theta=atan(1./$slope);
    if ($difx > 0.0){
      $theta=$pi-$theta if($dify < 0.0);
    } else {
       if ($dify > 0.) {
	 $theta=2*$pi+$theta;
       } else {
	 $theta=$pi+$theta;
       }
     }
  }
}

$biasx=cos($theta)*($xa-$xb)-sin($theta)*($ya-$yb);
$biasy=sin($theta)*($xa-$xb)+cos($theta)*($ya-$yb);
$factor=cos($deg2rad*($blat+$flat)*0.5);
$biasx=$biasx*$rearth*$factor;
$biasy=$biasy*$rearth*$factor;

$rr=sqrt($biasx*$biasx+$biasy*$biasy);
#$dist_x=abs($biasx);
#$dist_y=abs($biasy);


print "mmm $blat $blon $xa $ya $xb $yb $xr $yr $biasx $biasy \n"  if($verb);
print "mmm $blat $blon $flat $flon $rr $dist_x $dist_y $error1\n"  if($verb);

return($rr,$biasx,$biasy);

}

sub gc_dist{

my(
      $rlat0,$rlon0,$rlat1,$rlon1) = @_;

my($f1,$f2,$rm,$finv,$rr,
      $rlogtd1,$rlogtd2,
      $rdenom,$course,$angle);

$f1=$deg2rad*$rlat0;
$f2=$deg2rad*$rlat1;
$rm=$deg2rad*($rlon0-$rlon1);
$finv=cos($f1)*cos($f2)*cos($rm)+sin($f1)*sin($f2);
$rr=$rearth*acos($finv);
$rr=$rr*$km2nm if($units eq 'english') ;

return($rr);


}

sub mercat {

local($rlat,$rlon) = @_;
local($rla,$rlo);

$rla=$rlat*$deg2rad;

if($rlon < 0.0){
  $rlo=360.0+$rlon;
} else {
  $rlo=$rlon;
} 

$x=$rlo*$deg2rad;
$y=log(tan($pi4+$rla*0.5));

@rc=($x,$y);
return(@rc);

}


sub rumltlg {

  my($course,$speed,$dt,$rlat0,$rlon0)=@_;
  my($icrse,$distnce,$dlon,$d1,$d2,$td1,$td2,$rdenom,$rlogtd1,$rlogtd2,$rlat1,$rlon1);


####  print "qqq $course,$speed,$dt,$rlat0,$rlon0\n";
#c****	    routine to calculate lat,lon after traveling "dt" time
#c****	    along a rhumb line specifed by the course and speed
#c****	    of motion
#
#--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
#
#  assume $speed is in kts and $dt is hours
#
#      
  $distnce=$speed*$dt;

  $icrse=int($course+0.01);
#
  if($icrse == 90.0 || $icrse == 270.0) {
#      
#*****		  take care of due east and west motion
#
    $dlon=$distnce/(60.0*cos($rlat0*$deg2rad));
    $rlon1=$rlon0+$dlon if($icrse == 90.0) ;
    $rlon1=$rlon0-$dlon if($icrse == 270.0) ;
    $rlat1=$rlat0;

  } else {

    $rlat1=$rlat0+$distnce*cos($course*$deg2rad)/60.0;
    $d1=(45.0+0.5*$rlat1)*$deg2rad;
    $d2=(45.0+0.5*$rlat0)*$deg2rad;
    $td1=tan($d1);
    $td2=tan($d2);
    $rlogtd1=log($td1);
    $rlogtd2=log($td2);
    $rdenom=$rlogtd1-$rlogtd2 ;
    $rlon1=$rlon0+(tan($course*$deg2rad)*$rdenom)*$rad2deg;
    
  }
  
  return($rlat1,$rlon1);
  
}




sub rumhdsp{
my(
      $rlat0,$rlon0,$rlat1,$rlon1,$dt,$units,$opt) = @_;


my($d1,$d2,$td1,$td2,$rnumtor,
   $rlogtd1,$rlogtd2,
   $verb,
   $rdenom,$course,$angle);

$verb=0;

if($verb) {
print"***** $rlat0,$rlon0,$rlat1,$rlon1,$dt,$units,$opt\n";
}

if($units eq "metric") {
  $distfac=111.19;
  $spdfac=0.2777;
} else {
  $distfac=60;
  $spdfac=1.0;
}


#
# assumes deg W
#
$rnumtor=($rlon0-$rlon1)*$deg2rad;

#
#--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
#

$rnumtor=($rlon1-$rlon0)*$deg2rad;
$d1=(45.0+0.5*$rlat1)*$deg2rad;
$d2=(45.0+0.5*$rlat0)*$deg2rad;

$td1=tan($d1);
$td2=tan($d2);
$rlogtd1=log($td1);
$rlogtd2=log($td2);
$rdenom=$rlogtd1-$rlogtd2;
$rmag=$rnumtor*$rnumtor + $rdenom*$rdenom;
$course=0.0;
if($rmag != 0.0) {
  $course=atan2($rnumtor,$rdenom)*$rad2deg;
}
if($course <= 0.0)  {
  $course=360.0+$course;
}

#
#...     now find distance
#

$icourse=int($course+0.1);
if($icourse ==  90.0 || $icourse == 270.0 ){
  $distance=$distfac*abs($rlon0-$rlon1)*cos($rlat0*$deg2rad);
} else {
  $distance=$distfac*abs($rlat0-$rlat1)/abs(cos($course*$deg2rad));
}

#
#...     now get speed
#
$speed=$distance/$dt;

#
#...      convert to u and v motion
#

$spdmtn=$speed*$spdfac;
$ispeed=int($spdmtn*100+0.5)/100;
$angle=(90.0-$course)*$deg2rad;
$umotion=$spdmtn*cos($angle);
$vmotion=$spdmtn*sin($angle);
$iumotion=int($umotion*100+0.5)/100;
$ivmotion=int($vmotion*100+0.5)/100;
printf("%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f\n",$distance,$icourse,$spdmtn,$angle,$umotion,$vmotion) if($verb);


return($icourse,$ispeed,$iumotion,$ivmotion);

}

sub tan{
  local($ang)=@_;
  return(sin($ang)/cos($ang));
}

sub atan{
  local($x)=@_;
  return(atan2($x,1.0))
}

sub acos{
local($x)=@_;
local($x1,$asin,$acos);
return(0) if(abs($x)>=1.0) ;
$x1=$x/sqrt(1.0-$x*$x);
$asin=atan($x1);
$acos=$pi2-$asin;
return($acos);

}


sub btdata ($btpath) {

  my($dtg,$dtg4,$verb,$btpath);

  $verb=0;

  ($btpath)=@_;

  if($verb) {
    print "QQQ $btpath\n";
  }

  open(BT,$btpath) || die "unable to open file: $btpath in bdata";

  $j=0;
  while(<BT>) {

    $card=$_;
    chomp($card);
#2000020700 11S 075 9999 -17.8  98.3   50  120 254.0  10.9
    @tt=split(' ',$card);
    $dtg4=$tt[0];

    $sname=$tt[1];
    $bcode=substr($sname,2,1);
	
    $btcnt{$sname}++;
    $bt{$sname,$btcnt{$sname},'dtg'}=$dtg4;

    $mw=$tt[2]*1;
    $pmin=$ttt[3];
      
    $lat=$tt[4];
    $lon=$tt[5];
    
    $r50=$tt[6];
    $r30=$tt[7];
    $tcdir=$tt[8];
    $tcspd=$tt[9];

    if($verb) {
	print "qqq $card\n";
	print "qqqq $lat $lon $mw $pmin $r50 $r30 $tcdir $tcspd\n";
    }

    $bt{$sname,$btcnt{$sname},'dtg'}=$dtg4;
    $bt{$sname,$dtg4,'mw'}=$mw;
    $bt{$sname,$dtg4,'pmin'}=$pmin;
    $bt{$sname,$dtg4,'lat'}=$lat;
    $bt{$sname,$dtg4,'lon'}=$lon;
    $bt{$sname,$dtg4,'r30'}=$r30;
    $bt{$sname,$dtg4,'r50'}=$r50;
    $bt{$sname,$dtg4,'tcspd'}=$tcspd;
    $bt{$sname,$dtg4,'tcdir'}=$tcdir;
    
    $btstorms{$dtg4}="$btstorms{$dtg4} $sname";

    if($doliststorms) {
      $ncard=sprintf("NAVY: 19%s %s %1s  %5s%1s %6s%1s",$dtg,$sname,$bcode,$rlat,$nshem,$rlon,$ewhem);
      print "$ncard\n";
    }
    
  }

  close(BT);

}


sub incmm($ym,$inc) {
  my($ym,$y,$m,$inc);
  ($ym,$inc)=@_;
  $inc=1 if($inc eq '');
  $y=substr($ym,0,4);
  $m=substr($ym,4,2);
  $m=$m + $inc;

  while($m<-12) {
    $y--;
    $m=$m+12;
  }

  if($m>12) {
    $y++;
    $m=1;
  }
  if($m==0) {
    $y--;
    $m=12;
  }
  if($m<0) {
    $y--;
    $m=$m + 12;
  }
  
  $ym=sprintf("%04d%02d",$y,$m);
  return($ym);

}


1;
