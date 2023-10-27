
/////// STORE DROPDOWN MENU LINKS /////////

var fadeInTime = 75;
var modColSpacing = 50; // pixels
var numModPerRow = 4;
var loopSpd = 1500; // milliseconds
var maxSpeed = 300;
var minSpeed = 3000;
var spdInterval = 400;
var showLabelTime = 1000;

var numDTGweb = 7;  

var menulinks=new Array()

menulinks[0]='<a href="http://ruc.noaa.gov/hfip/tceps/" target="_blank">MF TCeps page</a>'
menulinks[1]='<a href="http://ruc.noaa.gov/hfip/tcdiag/" target="_blank">MF TCdiag page</a>'
menulinks[2]='<a href="http://www.esrl.noaa.gov/psd/forecasts/gfsenkf/ens/" target="_blank">JW GFS(254) EnKF EPS page</a>'
menulinks[3]='<a href="http://ruc.noaa.gov/tracks/" target="_blank">Paula\'s TCeps page</a>'
menulinks[4]='<a id="poop" href="http://www.nrlmry.navy.mil/TC.html" target="_blank">NRL TC page</a>'

// STORE STORM LINKS //
var stmlinks=new Array()
for (i=0 ; i<allStorms.length ; i++) {
    stm = allStorms[i];
    stmNum = i+1
    stmlinks[i] = '<a id=stmlink'+stmNum+'><font color=blue> ' + stm + '</font> <font color=red>' + stormDict[stm][1] + '</font></a>';
}

/////// CREATE BUTTONS ///////

function createButton( parentID , ID, value, initClass, over, out ) {
    inputInfo = "<input id=" + ID + " type='button' class=" + initClass + " value=" + value + ">";
    $('#'+parentID).append("<div class='divCell'>" + inputInfo + "</div>");
    $('#'+ID).attr({
        onMouseOver: over,
        onMouseOut:  out
        });
}

// initialization
//resetVars()

// -- make buttons
//

// domains
for (var i=1 ; i<=allDomains.length ; i++) {
    domain = allDomains[i-1];
    domainstr = "domain" + i
    createButton( 'DomainSect', domainstr, domain, 'btn50darkorange',
                  "className='btn50darkorangeover'", "className='btn50darkorange'" );
}

// storms dropdown
createButton( 'DomainSect','storms','# Stms...','btnsmldrop',
              "dropdownmenu(this, event, stmlinks, '300px', stormDict)" , "delayhidemenu()" );
// have to reapply name b/c only first word apears on button(?)
$('#storms').val('# Stms...');

// "extra" buttons
createButton( 'ExtraSect','zoom1','Zm++','btn50t',"className='btn50tover'","className='btn50t'" );
createButton( 'ExtraSect','zoom2','Zm--','btn50t',"className='btn50tover'","className='btn50t'" );
createButton( 'ExtraSect','veriFcst','VERI','btn75c',"className='btn75cover'","className='btn75c'" );
createButton( 'ExtraSect','reset','RESET','breset',"className='bresetover'","className='breset'" );
createButton( 'ExtraSect','doc','doc...','btn75d',"className='btn75dover'","className='btn75d'" );
createButton( 'ExtraSect','links','Links...','btnsmldrop',
              "dropdownmenu(this, event, menulinks, '250px', [])" , "delayhidemenu()" );

// dtgs
for (var i=1 ; i<=numDTGweb ; i++) {
    dtg = allDtgs[i-1];
    dtgstr = "dtg" + i;
    createButton( 'DtgSect', dtgstr, dtg, 'btndtga', "className='btndtgaover'", "className='btndtga'" );
}

modCount = 0;
rowCount = 1;
totalBtnLen = 0;

// Create entire Modeling section
while (modCount < modelLabels.length) {

    //create new row in model table
    rowstr = 'modRow' + rowCount;
    rowInfo = "<div class='divRow' id='" + rowstr + "'></div>";
    $('#modTable').append( rowInfo )

    for (i=1 ; i<=numModPerRow; i++) {
        if (modCount < modelLabels.length) {

            // create a new model section and its model label button
            sectstr = "modSect" + modCount;
            $('#'+rowstr).append("<div id='"+sectstr+"' class='divCell' style='width:280px'></div>");
            modelLab = modelLabels[modCount];
            createButton( sectstr , 'model'+modCount, modelLab , 'btn120grna', 'btn120grna', 'btn120grna');
            // only first word appears...
            $('#model'+modCount).val(modelLab);
            $('#model'+modCount).attr('disabled',true) // make unclickable
            totalBtnLen += parseInt($('#model'+modCount).outerWidth());

            modNum = modCount + 1
            // create products in model section
            for (j=0 ; j<allProducts.length ; j++) {
                id = 'model' + allProducts[j] + '-' + modNum;
                createButton( sectstr , id , allProducts[j] , 'btn25ptype',
                              "className='btn25ptypeover'", "className='btn25ptype'" );
                totalBtnLen += parseInt($('#'+id).outerWidth());
            }
            // create taus in model section
            for (j=0 ; j<allTaus.length ; j++) {
                id = 'model' + allTaus[j] + 'hr' + modNum;
                dayNum = Math.floor(parseInt(allTaus[j]) / 24);
                label = 'd+' + dayNum;
                createButton( sectstr , id , label , 'btnsmltau25',
                              "className='btnsmltau25over'" , "className='btnsmltau25'" );
                totalBtnLen += parseInt($('#'+id).outerWidth());
            }

            // calc combined length of all label, product, and tau btns
            totColWidth = totalBtnLen + modColSpacing;
            $('#'+sectstr).css('width', totColWidth);
            totalBtnLen = 0;

            modCount += 1;
}
}
rowCount+= 1;
}

// create model tau loop btns
totalBtnLen = 0;
sectstr = 'loopModTauSect'
$('#loopMod').append("<div id="+sectstr+" class='divCell'></div>");

createButton( sectstr,'loopModLabel','Loop Models TAU','btn120loop','btn120loop','btn120loop' );
// only first word appears on button...
$('#loopModLabel').val('Loop Models TAU');
$('#loopModLabel').attr('disabled',true);
totalBtnLen += parseInt($('#loopModLabel').outerWidth());

// create tau loop btns
for (i=0 ; i<allTaus.length ; i++) {
    ctau=allTaus[i];
    id = 'loopMod'+ctau+'hr';
    dayNum = Math.floor(parseInt(ctau) / 24);
    label = 'd+' + dayNum;
    //rc=chkLoopModels(ctau);
    rc=1

    if(rc) {
        btnloop='btnsmltauloop'
        btnloopover='btnsmltauloopover'
        } else {
            btnloop='btnsmltauloopnot'
            btnloopover='btnsmltauloopnot'
        }
    clsbtnloop="className="+btnloop
    clsbtnloopover="className="+btnloopover
    createButton( sectstr , id , label, btnloop,
                  clsbtnloopover , clsbtnloop );
    totalBtnLen += parseInt($('#'+id).outerWidth());
}
totColWidth = totalBtnLen + modColSpacing;
$('#'+sectstr).css('width', totColWidth);


// create mouseover model buttons (initially hidden)
totalBtnLen = 0;
sectstr = 'loopModModelSect';
$('#loopMod').append("<div id="+sectstr+" class='divCell'></div>");
for (i=0 ; i<allModels.length ; i++) {
    id = 'loopMod'+allModels[i];
    createButton( sectstr , id , allModels[i] , 'btnsmlmodloop',
                  "" , "className='btnsmlmodloop'" ); // for now, don't do anything on mouseover
    totalBtnLen += ( parseInt($('#'+id).outerWidth()) + parseInt($('#'+id).css('margin-left')) );
}
totColWidth = totalBtnLen + modColSpacing;
$('#'+sectstr).css('width', totColWidth);


// create product loop buttons (initially hidden)
totalBtnLen = 0;
sectstr = 'loopModProductSect';
$('#loopMod').append("<div id="+sectstr+" class='divCell'></div>");
for (i=0 ; i<allProducts.length ; i++) {
    id = 'loopMod'+allProducts[i];
    createButton( sectstr , id , allProducts[i] , 'btnsmlmodloop',
                  "" , "className='btnsmlmodloop'" ); // for now, don't do anything on mouseover
    totalBtnLen += ( parseInt($('#'+id).outerWidth()) + parseInt($('#'+id).css('margin-left')) );
}
totColWidth = totalBtnLen + modColSpacing;
$('#'+sectstr).css('width', totColWidth);


// create model speed buttons (initially hidden)
sectstr = 'loopModSpeedSect'
$('#loopMod').append("<div id="+sectstr+" class='divCell'></div>");
createButton( sectstr , 'loopModSpdUp' , 'Faster' , 'btnsmlspeed' ,
              "className='btnsmlspeedover'", "className='btnsmlspeed'");
createButton( sectstr , 'loopModSpdDown' , 'Slower' , 'btnsmlspeed' ,
              "className='btnsmlspeedover'", "className='btnsmlspeed'");




///////// UPDATE FUNCTIONS ///////////

function tauToDtg( dtgi, tau ) {
    // returns the final dtg given an initial dtg and a tau
    //   ex:  dtgi=2013072600  tau=60  -->  return 2013072812
    numDtgi = parseInt( dtgi );
    yr = Math.floor(numDtgi/1000000);
    mon = Math.floor((numDtgi%1000000)/10000);
    day = Math.floor((numDtgi%10000)/100);
    hr = numDtgi%100;

    datei = new Date( yr, mon-1, day, hr);
    datef = new Date( datei.getTime() + 3600000*tau ); //add tau num of hrs

    dtgf = datef.getFullYear().toString();
    if (datef.getMonth()+1 < 10 ) { dtgf += '0' }
    dtgf += (datef.getMonth()+1).toString();
    if (datef.getDate() < 10) { dtgf+='0' }
    dtgf += datef.getDate().toString();
    if (datef.getHours() < 10) { dtgf+='0' }
    dtgf += datef.getHours().toString();

    return dtgf;
}

// update image
function updateImage(ifTransition) {

    if (curTau < 10) { tau = '00' + parseInt(curTau) }
    else if (curTau < 100) { tau = '0' + parseInt(curTau) }
    else { tau = parseInt(curTau) }

    if (curProduct == 'v85') { prod='n850' }
    else if (curProduct == 'prp') { prod=curProduct }

    if(curMode == 'fcst') {
        bdtg=curDTG	
        vdtg=tauToDtg( bdtg, curTau )
        } else if(curMode == 'veri') {
            vdtg=curDTG	
            bdtg=tauToDtg( vdtg, -curTau )
        }

    src =   './' + bdtg.substring(0,4) + '/' +    //year folder
    bdtg + '/' + curModel.toLowerCase() + '.' +
    vdtg + '.' + tau + '.' +
    curDomain.toLowerCase() + '.trop'+curDomain.toLowerCase()+'.'+ 
    prod +'.'+ curMode + '.gentracker.png'

    if (ifTransition) {
        // fade in new image
        pos = $('#myImage').position();
        $('#link').prepend('<img src="' + src + '" id="newImage" style="position:absolute"></img>');
        $('#newImage').attr({
            height: $('#myImage').attr('height'),
            width: $('#myImage').attr('width') });
        $('#newImage').css({
            left: pos.left+'px',
            top:  pos.top+'px' });
        $('#newImage').hide();
        $('#newImage').fadeIn(fadeInTime, function() { $(this).attr('id','myImage') });
        $('#myImage').fadeOut(fadeInTime, function() { $(this).remove() }) ;
        } else {
            $('#myImage').attr('src',src);
        }

    //change headRow
    $('#headDtg').text(curDTG+' ');
    $('#headDomain').text(curDomain+' ');
    $('#headModel').text(curModel+' ');

    //change title
    $('#title').text('Tcgen :: ' + curDTG)

}

function resetVars() {
    // resets all useful globals to a default and updates
    curDTG = allDtgs[0];
    curModel = Object.keys(dtgDict[allDtgs[0]])[0];
    curModel = curModel.substring(0,curModel.length-4); // take of fcst/veri part
    curDomain = allDomains[0];
    curTau = '60';
    curMode = 'fcst';
    curProduct = 'prp';
}


function resetAll() {
    // resets all useful globals to a default and updates
    resetVars()
    $('#myImage').attr( 'height', '1060' );
    $('#myImage').attr( 'width', '1440' );

    updateImage(false);
    updateDtgBtns();
}


//// update DTG buttons when one is clicked
function updateDtgBtns() {

    var ind = allDtgs.indexOf(curDTG);
    var curBtnNum;

    //shift buttons over
    var limit = Math.floor(numDTGweb/2.0);
    if (ind>=limit && ind<=(allDtgs.length-1)-limit) { // dtg is in middle

                                                       var counter = limit;
                                                       for(var i=1;i<=numDTGweb;i++) {
                                                           dtgstr = '#dtg' + i;
                                                           $(dtgstr).attr('value',allDtgs[ind-counter]);
                                                           counter--;
                                                       }       
                                                       if (numDTGweb%2==1) {
                                                           curBtnNum = Math.ceil(numDTGweb/2.0);
                                                           } else { // even number
                                                                    curBtnNum = Math.ceil(numDTGweb/2.0) + 1;
                                                                    }       

                                                       } else if (ind<limit) { //first few allDtgs

                                                                               for (var i=0;i<numDTGweb;i++) {
                                                                                   dtgNum = i+1
                                                                                   dtgstr = '#dtg' + dtgNum;
                                                                                   $(dtgstr).attr("value",allDtgs[i]);
                                                                               }       
                                                                               curBtnNum = ind+1;

                                                                               } else { //last few allDtgs

                                                                                        for (var i=0;i<numDTGweb;i++) {
                                                                                            dtgNum = i+1
                                                                                            dtgstr = '#dtg' + dtgNum;
                                                                                            tmp = (allDtgs.length - numDTGweb) + i
                                                                                            $(dtgstr).attr("value",allDtgs[tmp]);
                                                                                        }       
                                                                                        curBtnNum = numDTGweb - (allDtgs.length-(ind+1))
}       

    // change color attrs of current button
    dtgstr = '#dtg' + curBtnNum
    $(dtgstr).attr({
    class: "btndtgacur",
    onMouseOver: "className='btndtgacurover'",
    onMouseOut:  "className='btndtgacur'"
    });     

    for (var i=1;i<=numDTGweb;i++) {
        //change color of non-current buttons (and make active/inactive)
        if (i != curBtnNum) {
            dtgstr = '#dtg' + i;
            dtg = $(dtgstr).attr('value')
            $(dtgstr).attr({
        class: 'btndtga',
        onMouseOver: "className='btndtgaover'",
        onMouseOut:  "className='btndtga'"
        });
        }
    }

    // make sure tau and model are available for new dtg
    checkIfAvailable()
}

function updateModelBtns() {
    // Updates all the visual tau, product, model buttons to reflect the
    //   current values stored in the global variables
    indModel = allModels.indexOf(curModel) + 1;
    indProduct = allProducts.indexOf(curProduct) + 1;
    indTau = allTaus.indexOf(curTau) + 1;

    for (i=1 ; i<=allModels.length ; i++) {

        //check if no products or taus for model
        prodsAndTaus = dtgDict[curDTG][allModels[i-1]+curMode];
        if ( prodsAndTaus[0].length == 0 || prodsAndTaus[1].length == 0 ) {
            allDisabled = true;
            } else{ allDisabled = false;}

        // update current and uncurrent products 
        for (j=1 ; j<=allProducts.length ; j++) {
            if (i==indModel && j==indProduct) { // current model
                                                $('#model'+curProduct+'-'+i).attr({
    class: "btn25ptypecur",
    onMouseOver: "className='btn25ptypecurover'",
    onMouseOut:  "className='btn25ptypecur'"
    });
    $('#model'+allProducts[j-1]+'-'+i).removeAttr('disabled');
    // check if to disable if not in dtg dict
    } else if (prodsAndTaus[0].indexOf( allProducts[j-1] ) == -1 || allDisabled) {
        $('#model'+allProducts[j-1]+'-'+i).attr({
            class: "btn25ptypenot",
            onMouseOver: "className='btn25ptypenot'",
            onMouseOut:  "className='btn25ptypenot'",
            disabled:    true
        });
    // keep enabled but not current
    } else {
        $('#model'+allProducts[j-1]+'-'+i).attr({
            class: "btn25ptype",
            onMouseOver: "className='btn25ptypeover'",
            onMouseOut:  "className='btn25ptype'"
        });
        $('#model'+allProducts[j-1]+'-'+i).removeAttr('disabled');
    }
    }

    //update cur/uncurrent taus
    for (j=1 ; j<=allTaus.length ; j++) {
        if (i==indModel && j==indTau) {
            $('#model'+curTau+'hr'+i).attr({
        class: "btnsmltau25cur",
        onMouseOver: "className='btnsmltau25curover'",
        onMouseOut:  "className='btnsmltau25cur'"
        });
        $('#model'+allTaus[j-1]+'hr'+i).removeAttr('disabled');
        } else if (prodsAndTaus[1].indexOf( allTaus[j-1] ) == -1 || allDisabled) {
            $('#model'+allTaus[j-1]+'hr'+i).attr({
                class: "btnsmltau25not",
                onMouseOver: "className='btnsmltau25not'",
                onMouseOut:  "className='btnsmltau25not'",
                disabled:    true
            });
        } else {
            $('#model'+allTaus[j-1]+'hr'+i).attr({
                class: "btnsmltau25",
                onMouseOver: "className='btnsmltau25over'",
                onMouseOut:  "className='btnsmltau25'"
            });
            $('#model'+allTaus[j-1]+'hr'+i).removeAttr('disabled');
        }
    }

    //update model loop buttons
    if (prodsAndTaus[0].indexOf(curProduct) == -1 || prodsAndTaus[1].indexOf(curTau) == -1) {
        $('#loopMod'+allModels[i-1]).attr('disabled',true);
        $('#loopMod'+allModels[i-1]).attr('class','btnsmlmodloopnot');
        } else {
            $('#loopMod'+allModels[i-1]).removeAttr('disabled');
            $('#loopMod'+allModels[i-1]).attr('class','btnsmlmodloop');
        }
}
}

function enterLoopMode( ifEnter ) {
    // update loop-related buttons to visible or hidden
    clearTimeout( loopTimeoutId ) // if tau looping, stop
    if (ifEnter) {
        $('.btnsmlmodloop').css('visibility','visible');
        $('.btnsmlmodloopnot').css('visibility','visible');
        $('.btnsmlspeed').css('visibility','visible');
        $('.btnsmlspeednot').css('visibility','visible');
        $('#loopModSpdUp').attr('className','btnsmlspeed');
        $('#loopModSpdDown').attr('className','btnsmlspeed');
        } else {
            $('.btnsmlmodloop').css('visibility','hidden');
            $('.btnsmlmodloopnot').css('visibility','hidden');
            $('.btnsmlspeed').css('visibility','hidden');
            $('.btnsmlspeednot').css('visibility','hidden');
        }
}

function chkLoopModels(ctau) {
    var rc=0;
    var ii
    for (ii=0 ; ii<allModels.length ; ii++) {
        tmodel=allModels[ii];
        if(dtgDict[curDTG][tmodel+curMode][0].indexOf(curProduct) != -1 && 
           dtgDict[curDTG][tmodel+curMode][1].indexOf(ctau) != -1)   {
               rc=1
    return (rc)
    }
    }
    return (rc)
}

function updateLoop() {
    curModel = allModels[modNumInLoop];
    // if product/tau aren't available for model, skip the model
    while (dtgDict[curDTG][curModel+curMode][0].indexOf(curProduct) == -1 || 
        dtgDict[curDTG][curModel+curMode][1].indexOf(curTau) == -1) {
    modNumInLoop++;
    if (modNumInLoop == allModels.length) { modNumInLoop = 0; };
    curModel = allModels[modNumInLoop];
    }
    updateImage(false);
    updateModelBtns();
    modNumInLoop++;
    if (modNumInLoop == allModels.length) { modNumInLoop = 0; }
}


function checkIfAvailable() {
    ///// Change current product and tau if not avialable for current model
    //      and dtg
    // if product isn't present
    if (dtgDict[curDTG][curModel+curMode][0].indexOf(curProduct) == -1) {
        // if other product for same model, take it
        if (dtgDict[curDTG][curModel+curMode][0].length > 0) {
            curProduct = dtgDict[curDTG][curModel+curMode][0][0];
            } else { // keep trying other products until one is found
                     for ( modelKey in dtgDict[curDTG] ) {
                         if ( dtgDict[curDTG][modelKey][0].length > 0 && modelKey.substring(modelKey.length-4)==curMode) {
                             curModel = modelKey.substring(0,modelKey.length-4); // take off fcst/veri
                             curProduct = dtgDict[curDTG][curModel+curMode][0][0]; 
    break;
    }
    }
    }
    }

    // if tau isn't present
    if (dtgDict[curDTG][curModel+curMode][1].indexOf(curTau) == -1) {
        for ( modelKey in dtgDict[curDTG] ) {
            if ( dtgDict[curDTG][modelKey][1].length > 0 && modelKey.substring(modelKey.length-4)==curMode) {
                curModel = modelKey.substring(0,modelKey.length-4); // take off fcst/veri
                curTau = dtgDict[curDTG][curModel+curMode][1][0];
            }
        }
    }

    updateModelBtns()
}



///////// CONNECT BUTTONS //////////

// connect various buttons (dtg, tau, model, domain)
function connect( varString ) {

    $(varString).click(function(evt) {

        enterLoopMode( false );

        // update everything except for image
        if (varString.substr(1,3) == 'dtg') {
            curDTG = $(this).attr('value');
            updateDtgBtns();

            } else if (varString.search('hr') != -1) {
label = $(this).attr('value');
if (label == 'd+0') { curTau = '0'; }
else { curTau = ((parseInt( label.slice(2) )*24) + 12).toString(); }

curModel = allModels[varString.charAt(varString.length-1)-1];
products = dtgDict[curDTG][curModel+curMode][0];
// make sure same product is available
if ( products.indexOf( curProduct ) == -1) {
    curProduct = products[ 0 ];
}
updateModelBtns();

} else if (varString.search('-') != -1) {
    curProduct = $(this).attr('value');
curModel = allModels[varString.charAt(varString.length-1)-1];
// make sure same tau is available
taus = dtgDict[curDTG][curModel+curMode][1];
if ( taus.indexOf( curTau ) == -1) {
    curTau = taus[ taus.length - 1]; // take last tau
}
updateModelBtns();

} else if (varString.substr(1,6) == 'domain') {
    curDomain = $(this).attr('value');
curDTG = domainDict[curDomain][0];
updateDtgBtns();
//updateLatLon();
// if loop btn pressed, do nothing except update image
}

        updateImage(false);

        });
}

//connect dtg buttons
for (i=1 ; i<=allDtgs.length ; i++) {
    dtgstr = '#dtg' + i;
    connect(dtgstr);
}

//connect domain buttons
for (i=1 ; i<=allDomains.length ; i++) {
    domainstr = '#domain' + i;
    connect(domainstr);
}

//connect product btns
for (i=1 ; i<=allModels.length ; i++) {
    for (j=1 ; j<=allProducts.length ; j++) {
        taustr = '#model' + allProducts[j-1] + '-' + i;
        connect(taustr);
    }
}

//connect tau btns
for (i=1 ; i<=allModels.length ; i++) {
    for (j=1 ; j<=allTaus.length ; j++) {
        taustr = '#model' + allTaus[j-1] + 'hr' + i;
        connect(taustr);
    }
}

imgPercent = 100;
// get initial height/width of image
initH = parseInt( $('#myImage').attr( 'height' ) );
initW = parseInt( $('#myImage').attr( 'width' ) );

function updateZoom( zm ) {
    if ( zm=='in' ) { imgPercent+=10 } // 10% bigger than original image
    else { imgPercent-=10 } // zoom out 10% smaller

    if ( imgPercent>=50 && imgPercent <=200 ) { // set zoom limits
                                                newH = initH * (imgPercent/100);
                                                newW = initW * (imgPercent/100);

                                                $('#myImage').attr('height', newH.toString() );
                                                $('#myImage').attr('width' , newW.toString() );

                                                if ( $('#loading').length == 0 ) {
                                                    $('#mainTable').append("<span class='loadText' id='loading'>Zoom "+imgPercent+"%</span>");
                                                    notifyTimeoutId = setTimeout( function() { $('#loading').remove() } , 1000 ); // show for little< 2 sec
                                                    } else {
                                                        clearTimeout( notifyTimeoutId );
                                                        $('#loading').html('Zoom '+imgPercent+'%'); // if already present, just update label
                                                        notifyTimeoutId = setTimeout( function() { $('#loading').remove() } , 1000 );
                                                    }
}
}

// Zm buttons
$('#zoom1').click( function(evt) {updateZoom( 'in' )} );
$('#zoom2').click( function(evt) {updateZoom( 'out')} );	

// veriFcst button
$('#veriFcst').click( function(evt) {

    enterLoopMode( false );

    curMode = $(this).attr('value').toLowerCase();
    if (curMode == 'fcst') {
        $(this).attr('value','VERI');
        } else { //curMode == 'veri'
                 $(this).attr('value','FCST');
                 }

    checkIfAvailable()
    updateImage(true);

});

// reset button
$('#reset').click( function(evt) { 
    location.reload()
});

// doc button
$('#doc').click( function(evt) {
    window.open('http://ruc.noaa.gov/hfip/tcgen/doc', '_blank' ).focus();
});

var notifyTimeoutId = NaN;
var loopTimeoutId = NaN;
var modNumInLoop;

// recursive function used instead of setInterval(), so that
//    global variable "loopSpd" can be changed
var beginLoop = function() {
    clearTimeout(loopTimeoutId);
    updateLoop();
    loopTimeoutId = setTimeout( beginLoop , loopSpd );
}

// Loop mod tau buttons
for (i=0 ; i<allTaus.length ; i++) {
    $('#loopMod'+allTaus[i]+'hr').click( function(evt) {
        ctau=allTaus[i]
        //rc=chkLoopModels(ctau)
        //if(rc) { doloop=true } else { doloop=false }
        doloop=true
        enterLoopMode( doloop );
        $('.btnsmlspeed').css('visibility','visible'); // unhide fast/slow btns
        $('.btnsmlspeednot').css('visibility','visible');
        modNumInLoop = 0;  // go to first model

        $('#loading').remove(); // in case loading element already present
        $('#mainTable').append("<span class='loadText' id='loading'>Looping...</span>");
        setTimeout( function() { $('#loading').remove() } , showLabelTime ); // show for little <= showLabelTime

        label = $(this).attr('value');
        if (label == 'd+0') { curTau = '0'; }
        else { curTau = ((parseInt( label.slice(2) )*24) + 12).toString(); }

        updateLoop();
        loopTimeoutId = setTimeout( beginLoop, loopSpd);
        });
}

// Loop mod model buttons
for (i=0; i<allModels.length ; i++) {
    document.getElementById('loopMod'+allModels[i]).onmouseover = function() {
        clearTimeout( loopTimeoutId ) // if tau looping, stop
        curModel = $(this).attr('value');
        updateImage(false);
        updateModelBtns();
        $('.btnsmlspeed').css('visibility','hidden');
        $('.btnsmlspeednot').css('visibility','hidden');
    }
}

// Loop mod product buttons
for (i=0; i<allProducts.length ; i++) {
    $('#loopMod'+allProducts[i]).click( function(evt) {
        if (curProduct != $(this).attr('value') ) {
            curProduct = $(this).attr('value');
            clearTimeout( notifyTimeoutId );
            $('#loading').remove(); // in case loading element already present
            $('#mainTable').append("<span class='loadText' id='loading'>Changing product...</span>");
            notifyTimeoutId = setTimeout( function() { $('#loading').remove() } , showLabelTime );
        }
        updateImage(true);
        });
}


// Loop mod speed buttons
$('#loopModSpdUp').click( function(evt) {
    if (loopSpd-spdInterval >= maxSpeed) { 
        loopSpd -= spdInterval;
        clearTimeout( notifyTimeoutId );
        $('#loading').remove(); // in case loading element already present
        $('#mainTable').append("<span class='loadText' id='loading'>Speeding up...</span>");
        notifyTimeoutId = setTimeout( function() { $('#loading').remove() } , showLabelTime ); // show for little< 2 sec

        // if were able to increase zoom, should be able to now decrease it
        $('#loopModSpdDown').attr('class','btnsmlspeed');
        $('#loopModSpdDown').removeAttr('disabled');
}

    if (loopSpd-spdInterval < maxSpeed) {
        $('#loopModSpdUp').attr('class','btnsmlspeednot');
        $('#loopModSpdUp').attr('disabled',true);
    }
});
$('#loopModSpdDown').click( function(evt) {
    if (loopSpd+spdInterval <= minSpeed) { 
        loopSpd += spdInterval;
        clearTimeout( notifyTimeoutId );
        $('#loading').remove(); // in case loading element already present
        $('#mainTable').append("<span class='loadText' id='loading'>Slowing down...</span>");
        notifyTimeoutId = setTimeout( function() { $('#loading').remove() } , showLabelTime );

        $('#loopModSpdUp').attr('class','btnsmlspeed');
        $('#loopModSpdUp').removeAttr('disabled');
}

    if (loopSpd+spdInterval > minSpeed) {
        $('#loopModSpdDown').attr('class','btnsmlspeednot');
        $('#loopModSpdDown').attr('disabled',true);
    }
});


resetAll()
