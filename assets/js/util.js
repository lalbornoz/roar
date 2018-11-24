if (window.$) {
  $.fn.int = function(){ return parseInt($(this).val(),10) }
  $.fn.float = function(){ return parseFloat($(this).val()) }
  $.fn.string = function(){ return trim($(this).val()) }
  $.fn.enable = function() { return $(this).attr("disabled",null) }
  $.fn.disable = function() { return $(this).attr("disabled","disabled") }
}

function noop(){}
function trim(s){ return s.replace(/^\s+/,"").replace(/\s+$/,"") }

var E = Math.E
var PI = Math.PI
var PHI = (1+Math.sqrt(5))/2
var TWO_PI = PI*2
var LN10 = Math.LN10
function clamp(n,a,b){ return n<a?a:n<b?n:b }
function norm(n,a,b){ return (n-a) / (b-a) }
function lerp(n,a,b){ return (b-a)*n+a }
function mix(n,a,b){ return a*(1-n)+b*n }
function ceil(n){ return Math.ceil(n) }
function floor(n){ return Math.floor(n) }
function round(n){ return Math.round(n) }
function max(a,b){ return Math.max(a,b) }
function min(a,b){ return Math.min(a,b) }
function abs(n){ return Math.abs(n) }
function sign(n){ return Math.abs(n)/n }
function pow(n,b) { return Math.pow(n,b) }
function exp(n) { return Math.exp(n) }
function log(n){ return Math.log(n) }
function ln(n){ return Math.log(n)/LN10 }
function sqrt(n) { return Math.sqrt(n) }
function cos(n){ return Math.cos(n) }
function sin(n){ return Math.sin(n) }
function tan(n){ return Math.tan(n) }
function acos(n){ return Math.cos(n) }
function asin(n){ return Math.sin(n) }
function atan(n){ return Math.atan(n) }
function atan2(a,b){ return Math.atan2(a,b) }
function sec(n){ return 1/cos(n) }
function csc(n){ return 1/sin(n) }
function cot(n){ return 1/tan(n) }
function cosp(n){ return (1+Math.cos(n))/2 } // cos^2
function sinp(n){ return (1+Math.sin(n))/2 }
function random(){ return Math.random() }
function rand(n){ return (Math.random()*n) }
function randint(n){ return rand(n)|0 }
function randrange(a,b){ return a + rand(b-a) }
function randsign(){ return random() >= 0.5 ? -1 : 1 }
function randnullsign(){ var r = random(); return r < 0.333 ? -1 : r < 0.666 ? 0 : 1 }

function xrandom(exp){ return Math.pow(Math.random(), exp) }
function xrand(exp,n){ return (xrandom(exp)*n) }
function xrandint(exp,n){ return rand(exp,n)|0 }
function xrandrange(exp,a,b){ return a + xrand(exp,b-a) }

function choice(a){ return a[randint(a.length)] }
function deg(n){ return n*180/PI }
function rad(n){ return n*PI/180 }
function xor(a,b){ a=!!a; b=!!b; return (a||b) && !(a&&b) }
function mod(n,m){ n = n % m; return n < 0 ? (m + n) : n }
function modi(n,m){ return floor(mod(n,m)) }
function dist(x0,y0,x1,y1){ return sqrt(pow(x1-x0,2)+pow(y1-y0,2)) }
function angle(x0,y0,x1,y1){ return atan2(y1-y0,x1-x0) }
function avg(m,n,a){ return (m*(a-1)+n)/a }
function quantize(a,b){ return floor(a/b)*b }
function quantile(a,b){ return floor(a/b) }

function pixel(x,y){ return 4*(mod(y,actual_h)*actual_w+mod(x,actual_w)) }
function rgbpixel(d,x,y){
  var p = pixel(~~x,~~y)
  r = d[p]
  g = d[p+1]
  b = d[p+2]
  a = d[p+3]
}
function fit(d,x,y){ rgbpixel(d,x*actual_w/w,y*actual_h/h) }

function step(a, b){
  return (b >= a) + 0
               // ^^ bool -> int
}

function julestep (a,b,n) {
  return clamp(norm(n,a,b), 0.0, 1.0);
}

// hermite curve apparently
function smoothstep(min,max,n){
  var t = clamp((n - min) / (max - min), 0.0, 1.0);
  return t * t * (3.0 - 2.0 * t)
}

function toArray(a){ return Array.prototype.slice.call(a) }
function shuffle(a){
  for (var i = a.length; i > 0; i--){
    var r = randint(i)
    var swap = a[i-1]
    a[i-1] = a[r]
    a[r] = swap
  }
  return a
}
function reverse(a){
  var reversed = []
  for (var i = 0, _len = a.length-1; i <= _len; i++){
    reversed[i] = a[_len-i]
  }
  return reversed
}
function deinterlace(a){
  var odd = [], even = []
  for (var i = 0, _len = a.length; i < _len; i++) {
    if (i % 2) even.push(a[i])
    else odd.push(a[i])
  }
  return [even, odd]
}
function weave(a){
  var aa = deinterlace(a)
  var b = []
  aa[0].forEach(function(el){ b.push(el) })
  reverse(aa[1]).forEach(function(el){ b.push(el) })
  return b
}
function cssRule (selector, declaration) {
  var x = document.styleSheets, y = x.length-1;
  x[y].insertRule(selector+"{"+declaration+"}", x[y].cssRules.length);
}

// easing functions
function circular (t) { return Math.sqrt( 1 - ( --t * t ) ) }
function quadratic (t) { return t * ( 2 - t ) }
function back (t) {
  var b = 4;
  return ( t = t - 1 ) * t * ( ( b + 1 ) * t + b ) + 1;
}
function bounce (t) {
  if (t >= 1) return 1;
  if ( ( t /= 1 ) < ( 1 / 2.75 ) ) {
    return 7.5625 * t * t;
  } else if ( t < ( 2 / 2.75 ) ) {
    return 7.5625 * ( t -= ( 1.5 / 2.75 ) ) * t + 0.75;
  } else if ( t < ( 2.5 / 2.75 ) ) {
    return 7.5625 * ( t -= ( 2.25 / 2.75 ) ) * t + 0.9375;
  } else {
    return 7.5625 * ( t -= ( 2.625 / 2.75 ) ) * t + 0.984375;
  }
}
function elastic (t) {
  var f = 0.22,
      e = 0.4;

  if ( t === 0 ) { return 0; }
  if ( t == 1 ) { return 1; }

  return ( e * Math.pow( 2, - 10 * t ) * Math.sin( ( t - f / 4 ) * ( 2 * Math.PI ) / f ) + 1 );
}

Model=function a(b,c,d,e){function f(){var a=this,f={};a.on=function(a,b){(f[a]||
(f[a]=[])).push(b)},a.trigger=function(a,b){for(var c=f[a],d=0;c&&d<c.length;)c
[d++](b)},a.off=function(a,b){for(d=f[a]||[];b&&(c=d.indexOf(b))>-1;)d.splice(c
,1);f[a]=b?d:[]};for(c in b)d=b[c],a[c]=typeof d=="function"?function(){return(
d=this.apply(a,arguments))===e?a:d}.bind(d):d;a.init&&a.init.apply(a,arguments)
}return f.extend=function(f){d={};for(c in b)d[c]=b[c];for(c in f)d[c]=f[c],b[c
]!==e&&(d["__"+c]=b[c]);return a(d)},f},typeof module=="object"&&(module.exports
=Model);                                                              // c-{{{-<

function defaults (dest, src) {
  dest = dest || {}
  for (var i in src) {
    dest[i] = typeof dest[i] == 'undefined' ? src[i] : dest[i]
  }
  return dest
}

function setSelectionRange(input, selectionStart, selectionEnd) {
  if (input.setSelectionRange) {
    input.focus();
    input.setSelectionRange(selectionStart, selectionEnd);
  }
  else if (input.createTextRange) {
    var range = input.createTextRange();
    range.collapse(true);
    range.moveEnd('character', selectionEnd);
    range.moveStart('character', selectionStart);
    range.select();
  }
}
function setCaretToPos(input, pos) {
  setSelectionRange(input, pos, pos);
}
