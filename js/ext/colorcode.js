!function(e){if("object"==typeof exports)module.exports=e();else if("function"==typeof define&&define.amd)define(e);else{var o;"undefined"!=typeof window?o=window:"undefined"!=typeof global?o=global:"undefined"!=typeof self&&(o=self),o.colorcode=e()}}(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var colorcode = {};
module.exports = colorcode;
colorcode.to_json = require('./src/to_json');
colorcode.from_json = require('./src/from_json');
colorcode.style = require('./src/style');
colorcode.to_canvas = require('./src/canvas');
colorcode.color = require('./src/color');
colorcode.font = require('./src/font');

},{"./src/canvas":2,"./src/color":3,"./src/font":4,"./src/from_json":8,"./src/style":9,"./src/to_json":10}],2:[function(require,module,exports){
var to_json = require('./to_json');
var fontload = require('./font').load;
var style = require('./style');
var color = require('./color');

// node-canvas
var Canvas = require('canvas');
if (typeof Image === "undefined") Image = Canvas.Image;

var make_canvas = function(){
  if (typeof document === "undefined" && typeof Canvas !== "undefined")
    return new Canvas();
  else
    return document.createElement("canvas");
}

var canvas_tmp;

var render_colorcode = function(json, canvas, font, opts){

  var cw = font.char_w
    , ch = font.char_h
    , ctx = canvas.getContext('2d')
    , canvas_tmp = canvas_tmp || make_canvas()
    , ctx_tmp = canvas_tmp.getContext("2d")

  var palette = color.palettes[opts.palette || style.palette];
  var bg = opts.bg || style.bg;

  canvas_tmp.width = cw;
  canvas_tmp.height = ch;
  
  canvas.width = json.w * cw;
  canvas.height = json.h * ch;

  // pre fill entire canvas with bg color
  // is this a good optimization?
  if (bg === color.transparent_index){
    // already cleared when resized above
    // canvas.clearRect(0,0, canvas.width,canvas.height);
  } else {
    ctx.fillStyle = palette[bg];
    ctx.fillRect(0,0, canvas.width,canvas.height);
  }

  for (var l=0; l<json.lines.length; l++){
    var line = json.lines[l];
    for (var c=0; c<line.length; c++){
      var char = line[c];
      var x = c * cw
      var y = l * ch
      
      // draw bg for this char if not already filled
      if (char.bg !== bg) {
        if (char.bg === color.transparent_index) {
            ctx.clearRect(x, y, cw, ch)
        } else { 
          ctx.fillStyle = palette[char.bg]
          ctx.fillRect(x, y, cw, ch);
        }
      }

      if (font.is_char_blank(char.value)) continue;

      // draw char in fg
      var fg = palette[char.fg]
      if (fg !== color.transparent){
        ctx_tmp.globalCompositeOperation = 'source-over'
        ctx_tmp.fillStyle = fg
        ctx_tmp.fillRect(0,0,cw,ch)
        ctx_tmp.globalCompositeOperation = 'destination-in'
        font.render_char(font, char.value, ctx_tmp, 0, 0, char)
        ctx.drawImage(canvas_tmp, x, y)
      } else { // transparent foreground punches out bg
        ctx.globalCompositeOperation = 'destination-out'
        font.render_char(font, char.value, ctx, x, y, char)
        ctx.globalCompositeOperation = 'source-over'
      }

    }
  }

  if (opts.done) opts.done(canvas)


}

var to_canvas = function(string_or_json, opts){
  opts = opts || {};
  
  if (typeof string_or_json === 'string')
    string_or_json = to_json(string_or_json, opts);
  
  var canvas = opts.canvas || make_canvas();
  var font_name = opts.font || style.font;

  fontload(font_name, function(font){ 
    render_colorcode(string_or_json, canvas, font, opts)
  });

  return canvas;
}

module.exports = to_canvas;

},{"./color":3,"./font":4,"./style":9,"./to_json":10,"canvas":11}],3:[function(require,module,exports){
var style = require('./style');

var color = {};
module.exports = color;

style.palette = 'mirc';

color.transparent_index = 99;
color.transparent = 'rgba(0,0,0,0)';
var ps = color.palettes = {};

ps.mirc = [
 'rgb(255,255,255)'
,'rgb(0,0,0)'
,'rgb(0,0,127)'
,'rgb(0,147,0)'
,'rgb(255,0,0)'
,'rgb(127,0,0)'
,'rgb(156,0,156)'
,'rgb(252,127,0)'
,'rgb(255,255,0)'
,'rgb(0,252,0)'
,'rgb(0,147,147)'
,'rgb(0,255,255)'
,'rgb(0,0,252)'
,'rgb(255,0,255)'
,'rgb(127,127,127)'
,'rgb(210,210,210)'
];

ps.winxp = [
 'rgb(255,255,255)'
,'rgb(0,0,0)'
,'rgb(0,0,128)'
,'rgb(0,128,0)'
,'rgb(255,0,0)'
,'rgb(128,0,0)'
,'rgb(128,0,128)'
,'rgb(255,128,0)'
,'rgb(255,255,0)'
,'rgb(0,255,0)'
,'rgb(0,128,128)'
,'rgb(0,255,255)'
,'rgb(0,0,255)'
,'rgb(255,0,255)'
,'rgb(128,128,128)'
,'rgb(192,192,192)'
];

ps.vga = [
 'rgb(255,255,255)'
,'rgb(0,0,0)'
,'rgb(0,0,170)'
,'rgb(0,170,0)'
,'rgb(255,85,85)'
,'rgb(170,0,0)'
,'rgb(170,0,170)'
,'rgb(170,85,0)'
,'rgb(255,255,85)'
,'rgb(85,255,85)'
,'rgb(0,170,170)'
,'rgb(85,255,255)'
,'rgb(85,85,255)'
,'rgb(255,85,255)'
,'rgb(85,85,85)'
,'rgb(170,170,170)'
];

ps.c64 = [
 'rgb(255,255,255)'
,'rgb(0,0,0)'
,'rgb(69,32,170)'
,'rgb(101,170,69)'
,'rgb(138,101,32)'
,'rgb(138,69,32)'
,'rgb(138,69,170)'
,'rgb(101,69,0)'
,'rgb(207,207,101)'
,'rgb(170,239,138)'
,'rgb(138,138,138)'
,'rgb(101,170,207)'
,'rgb(138,101,223)'	
,'rgb(207,138,101)'
,'rgb(69,69,69)'
,'rgb(170,170,170)'
];

ps.appleii = [
 'rgb(255,255,255)' 
,'rgb(0,0,0)'
,'rgb(64,53,121)'
,'rgb(64,75,7)'
,'rgb(191,180,248)'
,'rgb(109,41,64)'
,'rgb(218,60,241)'
,'rgb(218,104,15)'
,'rgb(191,202,134)'
,'rgb(38,195,16)'
,'rgb(19,87,64)'
,'rgb(146,214,191)'
,'rgb(37,151,240)'
,'rgb(236,168,191)'
,'rgb(128,128,128)'
,'rgb(128,128,128)'
];


},{"./style":9}],4:[function(require,module,exports){
var __dirname="/src";var style = require('./style');
// node-canvas
var Canvas = require('canvas');
if (typeof Image === "undefined") Image = Canvas.Image;

var font = {};
module.exports = font;

// hack for loading fonts in node... todo, fix this
font.img_path = "";
if (typeof document === "undefined") font.img_path = __dirname + "/../examples/web/"


font.list = {};

var fsexps = require('./font/fixedsys');
var cp437s = require('./font/cp437');
for (f in fsexps) font.list[fsexps[f].name] = fsexps[f];
for (f in cp437s) font.list[cp437s[f].name] = cp437s[f];

style.font = 'fixedsys_8x16';

var err_font_load = function(){
  console.log("couldn't load font")
}


font.load = function(font_name, callback_fn){
  if (!(font_name in font.list)) { return;} // todo error
  
  var f = font.list[font_name]
  
  if (f.loaded) {
    callback_fn(f);
  } else {
    f.sheet = new Image();
    f.sheet.crossOrigin = 'anonymous'
    // node-canvas doesn't have addEventListener :(
    f.sheet.onload = function(){
      f.loaded = true
      callback_fn(f);
    }
    f.sheet.src = font.img_path + f.sheet_url

  }
}


},{"./font/cp437":5,"./font/fixedsys":6,"./style":9,"canvas":11}],5:[function(require,module,exports){
var cp437s = [[8,8],[8,12],[8,14],[8,16],[10,10],[10,16],[12,12],[16,16]]
var fonts = {};
module.exports = fonts;

// utf8 -> cp437 function by sheetjs
// edited from https://github.com/SheetJS/js-codepage/blob/master/bits/437.js
var cp437 = (function(){ var d = "\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\b\t\n\u000b\f\r\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001a\u001b\u001c\u001d\u001e\u001f !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ ", D = [], e = {}; for(var i=0;i!=d.length;++i) { if(d.charCodeAt(i) !== 0xFFFD) e[d[i]] = i; D[i] = d.charAt(i); } return {"enc": e, "dec": D }; })();

var render_char = function(font, char_value, ctx, ctx_x, ctx_y){
  char_value = cp437.enc[String.fromCharCode(char_value)] | 0;
  var sheet_x = (char_value % font.sheet_w_in_chars) * font.char_w
  var sheet_y = ((char_value / font.sheet_w_in_chars) |0) * font.char_h
  ctx.drawImage(font.sheet, 
               sheet_x|0, sheet_y|0, font.char_w, font.char_h,
               ctx_x|0, ctx_y|0, font.char_w, font.char_h)

}

for (var i=0, wh; wh=cp437s[i]; i++){
  var font = {};
  font.is_char_blank = require('../fontutil').is_char_blank;
  font.render_char = render_char;
  font.name = 'cp437_' + wh[0] + 'x' + wh[1];
  font.sheet_url = './img/' + font.name + '.png'
  font.sheet_w_in_chars = 16;
  font.char_w = wh[0]
  font.char_h = wh[1]
  fonts[font.name] = font;
}



// window.cp437 = cp437;

},{"../fontutil":7}],6:[function(require,module,exports){
var fsexps = [[8,16,0],[8,15,1],[8,8,5]]
var fonts = {};
module.exports = fonts;

var render_char = function(font, char_value, ctx, ctx_x, ctx_y, char){
  var sheet_x = 0, sheet_y = 3;
  if (char_value >= 0x20 && char_value <= 0x7e){ // ascii
    sheet_x = (char_value - 0x20) * font.char_w_sheet
    if (char.i){ // italic
      sheet_y = 1 * font.char_h_sheet + 3
    }
 } else if (char_value >= 0x80 && char_value <= 0xff){ // latin-1
    sheet_x = (char_value - 0x80) * font.char_w_sheet; 
    sheet_y = 2 * font.char_h_sheet + 3
 } else if (char_value >= 0x0100 && char_value <= 0x017f){ // latin a
    sheet_x = (char_value - 0x0100) * font.char_w_sheet; 
    sheet_y = 3 * font.char_h_sheet + 3
 } else if (char_value >= 0x0180 && char_value <= 0x024f){ // latin b
    sheet_x = (char_value - 0x0180) * font.char_w_sheet; 
    sheet_y = 4 * font.char_h_sheet + 3
 } else if (char_value >= 0x2500 && char_value <= 0x25ff){ // geom
    sheet_x = (char_value - 0x2500) * font.char_w_sheet; 
    sheet_y = 5 * font.char_h_sheet + 3
  } else if (char_value >= 0x2600 && char_value <= 0x26ff){ // emoji
    sheet_x = (char_value - 0x2600) * font.char_w_sheet; 
    sheet_y = 6 * font.char_h_sheet + 3
  }

  // var sheet_x = (char_value % font.sheet_w_in_chars) * font.char_w
  // var sheet_y = ((char_value / font.sheet_w_in_chars) |0) * font.char_h + 3
  ctx.drawImage(font.sheet, 
               sheet_x|0, (sheet_y|0) + font.y_adj, font.char_w, font.char_h,
               ctx_x|0, ctx_y|0, font.char_w, font.char_h)

}

for (var i=0, wh; wh=fsexps[i]; i++){
  var font = {
    name: 'fixedsys_' + wh[0] + 'x' + wh[1],
    sheet_url: './img/fsex-simple.png',
    sheet_w_in_chars: 128,
    char_w_sheet: 8,
    char_h_sheet: 16,
    char_w: wh[0],
    char_h: wh[1],
    y_adj: wh[2],
    is_char_blank: require('../fontutil').is_char_blank,
    render_char: render_char
  }
  fonts[font.name] = font
}
},{"../fontutil":7}],7:[function(require,module,exports){
var util = {};
module.exports = util;

util.is_char_blank = function(char_value){
  if (char_value === 32) return true;
}

util.render_char = function(font, char_value, ctx, ctx_x, ctx_y){
  var sheet_x = (char_value % font.sheet_w_in_chars) * font.char_w
  var sheet_y = ((char_value / font.sheet_w_in_chars) |0) * font.char_h
  ctx.drawImage(font.sheet, 
               sheet_x|0, sheet_y|0, font.char_w, font.char_h,
               ctx_x|0, ctx_y|0, font.char_w, font.char_h)

}


},{}],8:[function(require,module,exports){
var char_color = '\x03';

var make_colorcode_fgbg = function(fg, bg){
  // pad numbers: this prevents irc parsing confusion
  // when the character after the colorcode is a number
  if (fg < 10) fg = "0" + fg;
  if (bg < 10) bg = "0" + bg;
  return char_color + fg + "," + bg
}

var colorcode_from_json = function(json, opts){
  var out = "";
  for (var li=0, line; line=json.lines[li]; li++){
    for (var ci=0, char; char=line[ci]; ci++){
      out += make_colorcode_fgbg(char.fg, char.bg)
      out += String.fromCharCode(char.value)
    }   
    out += "\n";
  }
  return out;
}


module.exports = colorcode_from_json;

},{}],9:[function(require,module,exports){
// default settings for fonts, colors, etc
var style = {};
module.exports = style;

},{}],10:[function(require,module,exports){
var char_color = '\x03';
var regexp_color = /(^[\d]{1,2})?(?:,([\d]{1,2}))?/;

var style_chars = {
  '\x02': 'bold',
  '\x1d': 'italic',
  '\x1f': 'underline',
  '\x0f': 'reset',
  '\x16': 'inverse'
};

var Style = function(style){
  this.b = style.b;
  this.i = style.i;
  this.u = style.u;
  this.fg = style.fg;
  this.bg = style.bg;
};

var style_fns = {};

style_fns.bold = function(style){ style.b = !style.b };

style_fns.italic = function(style){ style.i = !style.i };

style_fns.underline = function(style){ style.u = !style.u };

style_fns.inverse = function(style){
  var tmp = style.fg;
  style.fg = style.bg;
  style.bg = tmp;
};

style_fns.reset = function(style, base_style){
  style.b =  base_style.b;
  style.i =  base_style.i;
  style.u =  base_style.u;
  style.fg = base_style.fg;
  style.bg = base_style.bg;
};

var colorcode_to_json = function(string, opts){
  // looks like its already converted
  if (typeof string === 'object' &&
      'lines' in string &&
      'w' in string &&
      'h' in string)
    return string;
 

  opts = opts || {};
  var d = colorcode_to_json.defaults;

  var base_style = {
    b:  "b" in opts ? opts.b : d.b,
    i:  "i" in opts ? opts.i : d.i,
    u:  "u" in opts ? opts.u : d.u,
    fg: "fg" in opts ? opts.fg : d.fg,
    bg: "bg" in opts ? opts.bg : d.bg
  };

  var lines_in = string.split(/\r?\n/);
  var lines_out = [];
  var w = 0, h = 0;

  for (var i=0; i<lines_in.length; i++){
    var line = lines_in[i];
    if (line.length === 0) continue; // skip blank lines
    var json_line = line_to_json(line, base_style);
    if (w < json_line.length) w = json_line.length;
    lines_out.push(json_line);
    h++;
  }

  return {w:w, h:h, lines:lines_out};
};

colorcode_to_json.defaults = {
  b: false
, i: false
, u: false
, fg: 1
, bg: 99
};

var line_to_json = function(line, base_style){
  var out = [];
  var pos = -1;
  var len = line.length -1;
  var char;
  var style = new Style(base_style); 
  
  while (pos < len){ pos++;

    char = line[pos];
    
    // next char is a styling char
    if (char in style_chars){
      style_fns[style_chars[char]](style, base_style);
      continue;
    }

    // next char is a color styling char, with possible color nums after
    if (char === char_color){
      var matches = line.substr(pos+1,5).match(regexp_color);
      
      // \x03 without color code is a soft style reset 
      if (matches[1] === undefined && matches[2] === undefined) {
        style.fg = base_style.fg;
        style.bg = base_style.bg;
        continue;
      }

      if (matches[1] !== undefined)
        style.fg = Number(matches[1]);

      if (matches[2] !== undefined)
        style.bg = Number(matches[2]);

      pos += matches[0].length;
      continue;
       
    }

    // otherwise, next char is treated as normal content
    var data = new Style(style);
    //data.value = char;
    data.value = char.charCodeAt(0);

    out.push(data);
  }
  return out;
};

module.exports = colorcode_to_json;

},{}],11:[function(require,module,exports){

},{}]},{},[1])
(1)
});