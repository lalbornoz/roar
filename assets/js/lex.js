function Lex (x,y) {
  if (typeof x == "number") {
    this.y = y
    this.x = x
    this.span = document.createElement("span")
  }
  else {
    this.span = x
  }
  this.fg = colors.white
  this.bg = colors.black
  this.char = " "
  this.opacity = 1
  this.focused = false
}
Lex.prototype.build = function(){
  if (isNaN(this.bg) || this.bg == Infinity || this.bg == -Infinity) this.bg = colors.black
  if (isNaN(this.fg) || this.fg == Infinity || this.fg == -Infinity) this.fg = colors.black
  this.span.className = this.css()
  this.span.innerHTML = this.html()
}
Lex.prototype.css = function(){
   return (
    this.focused ?
      "focused " : ""
  ) + (
    this.opacity === 0 ?
      "transparent f" + color_alphabet[modi(this.fg,16)] :
      "f" + color_alphabet[modi(this.fg,16)] + " b" + color_alphabet[modi(this.bg,16)]
  )
}
Lex.prototype.html = function(){
  return this.char == " " ? "&nbsp;" : this.char || "&nbsp;"
}
Lex.prototype.read = function(){
  this.char = this.span.innerHTML
  return this.char
}
Lex.prototype.ascii = function(){
  return this.char || " "
}
Lex.prototype.sanitize = function(){
  switch (this.char) {
//    case "%": return "%"
    case undefined:
    case "":  return " "
    default:  return this.char
  }
}
Lex.prototype.ansi = function(bg_, fg_){
  var char = this.char || " "
  var charIsNaN = isNaN(parseInt(char))
  if ((bg_ == this.fg) && (fg_ == this.bg)) {
    bg_ = this.bg; fg_ = this.fg
    return [bg_, fg_, "\x1b[7m" + char]
  } else if ((bg_ != this.bg) && (fg_ != this.fg)) {
    bg_ = this.bg; fg_ = this.fg;
    return [bg_, fg_, "\x1b[" + ansi_bg[bg_] + ";" + ansi_fg[fg_] + "m" + char]
  } else if (bg_ != this.bg) {
    bg_ = this.bg
    return [bg_, fg_, "\x1b[" + ansi_bg[bg_] + "m" + char]
  } else if (fg_ != this.fg) {
    fg_ = this.fg
    return [bg_, fg_, "\x1b[" + ansi_fg[fg_] + "m" + char]
  }
}
Lex.prototype.mirc = function(bg_, fg_){
  var char = this.char || " "
  var charIsNaN = isNaN(parseInt(char))
  if ((bg_ == this.fg) && (fg_ == this.bg)) {
    bg_ = this.bg; fg_ = this.fg
    return [bg_, fg_, "\x16" + char]
  } else if ((bg_ == this.bg) && (fg_ != this.fg)) {
    fg_ = this.fg
    return [bg_, fg_, "\x03" + ((this.fg&15) < 10 && !charIsNaN ? "0" : "") + (this.fg&15) + char]
  } else {
    bg_ = this.bg; fg_ = this.fg
    return [bg_, fg_, "\x03" + (this.fg&15) + "," + ((this.bg&15) < 10 && !charIsNaN ? "0" : "") + (this.bg&15) + char]
  }
}
Lex.prototype.assign = function (lex){
  this.fg = lex.fg
  this.bg = lex.bg
  this.char = lex.char
  this.opacity = lex.opacity
  this.build()
}
Lex.prototype.stamp = function (lex, brush){
  if (brush.draw_fg) this.fg = lex.fg
  if (brush.draw_bg && lex.opacity > 0) this.bg = lex.bg
  if (brush.draw_char) this.char = lex.char
  this.opacity = 1
  this.build()
}
Lex.prototype.clone = function () {
  var lex = new Lex (0,0)
  lex.assign(this)
  return lex
}
Lex.prototype.erase = function (){
  this.fg = fillColor
  this.bg = fillColor
  this.char = " "
  this.opacity = 1
  this.build()
}
Lex.prototype.eq = function(lex){
  return lex && this.fg == lex.fg && this.bg == lex.bg && this.char == lex.char
}
Lex.prototype.eqColor = function(lex){
  return lex && this.fg == lex.fg && this.bg == lex.bg
}
Lex.prototype.ne = function(lex){
  return ! this.eq(lex)
}
Lex.prototype.clear = function(){
  this.bg = colors.black
  this.fg = 0
  this.char = " "
  this.opacity = 0
  this.build()
}
Lex.prototype.isClear = function(){
  return this.bg == 1 && this.fg == 0 && this.char == " "
}
Lex.prototype.focus = function(){
  if (focused) focused.blur()
  this.span.classList.add('focused')
  this.focused = true
  focused = this
}
Lex.prototype.blur = function(){
  focused = null
  this.span && this.span.classList.remove('focused')
  this.focused = false
  this.onBlur && this.onBlur()
}
Lex.prototype.demolish = function(){
  if (this.span.parentNode) { this.span.parentNode.removeChild(this.span) }
  this.span = null
}
Lex.prototype.key = function(char, keyCode) {
  if (! char) { return }
  this.char = char
  this.fg = brush.fg
  this.build()
  return true
}
