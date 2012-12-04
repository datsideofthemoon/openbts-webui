var array = new Array();
var speed = 10;
var timer = 10;

// Loop through all the divs in the slider parent div //
// Calculate seach content divs height and set it to a variable //
function slider(target,showfirst) {
  var slider = document.getElementById(target);
  var divs = slider.getElementsByTagName('div');
  var divslength = divs.length;
  for(i = 0; i < divslength; i++) {
    var div = divs[i];
    var divid = div.id;
    if(divid.indexOf("header") != -1) {
      div.onclick = new Function("processClick(this)");
    } else if(divid.indexOf("content") != -1) {
      var section = divid.replace('-content','');
      array.push(section);
      div.maxh = div.offsetHeight;
      if(showfirst == 1 && i == 1) {
        div.style.display = 'block';
      } else {
        div.style.display = 'none';
      }
    } 
  }
}

// Process the click - expand the selected content and collapse the others //
function processClick(div) {
  var catlength = array.length;
  for(i = 0; i < catlength; i++) {
    var section = array[i];
    var head = document.getElementById(section + '-header');
    var cont = section + '-content';
    var contdiv = document.getElementById(cont);
    clearInterval(contdiv.timer);
    if(head == div && contdiv.style.display == 'none') {
      contdiv.style.height = '0px';
      contdiv.style.display = 'block';
      initSlide(cont,1);
    } else if(contdiv.style.display == 'block') {
      initSlide(cont,-1);
    }
  }
}

// Setup the variables and call the slide function //
function initSlide(id,dir) {
  var cont = document.getElementById(id);
  var maxh = cont.maxh;
  cont.direction = dir;
  cont.timer = setInterval("slide('" + id + "')", timer);
}

// Collapse or expand the div by incrementally changing the divs height and opacity //
function slide(id) {
  var cont = document.getElementById(id);
  var maxh = cont.maxh;	
  var currheight = cont.offsetHeight;
  var dist;
  if(cont.direction == 1) {
    dist = (Math.round((maxh - currheight) / speed));
  } else {
    dist = (Math.round(currheight / speed));
  }
  if(dist <= 1) {
    dist = 1;
  }
  cont.style.height = currheight + (dist * cont.direction) + 'px';
  cont.style.opacity = currheight / cont.maxh;
  cont.style.filter = 'alpha(opacity=' + (currheight * 100 / cont.maxh) + ')';
  if(currheight < 2 && cont.direction != 1) {
    cont.style.display = 'none';
    clearInterval(cont.timer);
  } else if(currheight > (maxh - 2) && cont.direction == 1) {
    clearInterval(cont.timer);
  }
}