//http://www.codelifter.com/main/javascript/capturemouseposition1.html
// Detect if the browser is IE or not.
// If it is not IE, we assume that the browser is NS.
var IE = document.all?true:false

// If NS -- that is, !IE -- then set up for mouse capture
if (!IE) document.captureEvents(Event.MOUSEMOVE)

// Set-up to use getMouseXY function onMouseMove
// this pull mouse from all locations on document
document.animation.onmousemove = getMouseXY;

// this only pulls for myImage put up by psway()
//document.animation.onmousemove = getMouseXY;

// Temporary variables to hold mouse x-y pos.s

// Main function to retrieve mouse x-y pos.s

function getMouseXY(e) {
  if (IE) { // grab the x-y pos.s if browser is IE
    tempX = event.clientX + document.body.scrollLeft + IEoffsetX
    tempY = event.clientY + document.body.scrollTop + IEoffsetY
  } else {  // grab the x-y pos.s if browser is NS
    tempX = e.pageX
    tempY = e.pageY
  }  
  // catch possible negative values in NS4
  if (tempX < 0){tempX = 0}
  if (tempY < 0){tempY = 0}  
  // show the position values in the form named Show
  // in the text fields named MouseX and MouseY

//alert('Selected area:\nTop corner: ' + tempX + tempY );


tempX=tempX-offsetxL
tempY=tempY-offsetyT


lonX=lonL + (tempX-xL)*dlonP
latY=latB + (yB-tempY)*dlatP


if(lonX > 180.0) {
  var clon = new NumberFormat(360.0-lonX);
  clon.setPlaces(1);
  var oclon = clon.toFormatted()+'W';
} else if(lonX <= 0.0) {
  var clon = new NumberFormat(-1*lonX);
  clon.setPlaces(1);
  var oclon = clon.toFormatted()+'W';
} else {
  var clon = new NumberFormat(lonX);
  clon.setPlaces(1);
  var oclon = clon.toFormatted()+'E';
}

if(latY > 0.0) {
  var clat = new NumberFormat(latY);
  clat.setPlaces(1);
  var oclat = clat.toFormatted()+'N';
} else {
  var clat = new NumberFormat(-1*latY);
  clat.setPlaces(1);
  var oclat = clat.toFormatted()+'S';
}


//  document.Show.MouseY.value = tempY
  document.Show.MouseY.value = oclat

//  document.Show.MouseX.value = tempX
  document.Show.MouseX.value = oclon

  return true
}

function getElPos(el)
  { x = el.offsetLeft;
    y = el.offsetTop;
    elp = el.offsetParent;
    while(elp!=null)
      { x+=elp.offsetLeft;
        y+=elp.offsetTop;
        elp=elp.offsetParent;
      }
    return new Array(x,y);
  }

tp=getElPos(document.animation);
// alert('Selected area:\nTop corner: ' + tp[0] + tp[1] );
