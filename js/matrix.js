function Matrix (w,h,f){
  this.x = 0
  this.y = 0
  this.w = w
  this.h = h
  this.f = f
  this.focus_x = 0
  this.focus_y = 0
  this.initialize()
}
Matrix.prototype.initialize = function(f){
  var w = this.w || 1, h = this.h || 1, f = f || this.f
  var aa = new Array (h)
  for (var y = 0; y < h; y++) {
    aa[y] = new Array (w)
    for (var x = 0; x < w; x++) {
      aa[y][x] = f(x,y)
    }
  }
  this.aa = aa
}
Matrix.prototype.rebuild = function (){
  this.demolish()
  this.initialize()
  this.append()
  this.bind()
  this.generate && this.generate()
  this.focus_clamp()
  check_if_lost_focus()
}
Matrix.prototype.clone = function () {
  var base = this
  var clone = new Matrix(this.w, this.h, function(x,y){
    return base.getCell(x,y).clone()
  })
  clone.f = this.f
  return clone
}
Matrix.prototype.assign = function (mat) {
  var base = this
  this.demolish()
  this.w = mat.w
  this.h = mat.h
//  this.f = function(){}
  this.initialize(function(x,y){
    var el = mat.getCell(x,y).clone()
    el.build()
    return el
  })
  this.append()
  this.bind()
  check_if_lost_focus()
  return this
}

Matrix.prototype.bind = function () {}
Matrix.prototype.demolish = function (){
  this.forEach(function(lex){
    lex.demolish()
  })
  while (this.rapper && this.rapper.firstChild) {
    this.rapper.removeChild(this.rapper.firstChild);
  }
  this.aa.forEach(function(row){
    row.length = 0
  })
  this.aa.length = 0
}
Matrix.prototype.forEach = function(f){
  this.aa.forEach(function(row, y){
    row.forEach(function(lex, x){
      f(lex, x, y)
    })
  })
}
Matrix.prototype.focus_clamp = function(){
  this.focus_x = clamp(this.focus_x, 0, this.w - 1)
  this.focus_y = clamp(this.focus_y, 0, this.h - 1)
}
Matrix.prototype.focus_add = function(x, y){
  this.focus(this.focus_x + x, this.focus_y + y)
}
Matrix.prototype.focus = function(x, y){
  if (x === undefined) x = this.focus_x
  if (y === undefined) y = this.focus_y
  x = mod(x, this.w)
  y = mod(y, this.h)
  this.focus_x = x
  this.focus_y = y
   
  //focused_input = this
  this.aa[y][x].focus()
}
Matrix.prototype.focusLex = function(y,x){
  if (x < 0) {
    y -= 1
  }
  if (x > this.aa[0].length) {
    y += 1
  }
  this.aa[mod(y,this.h)][mod(x,this.w)].focus()
}
Matrix.prototype.clear = function(){
  this.forEach(function(lex,x,y){ lex.clear() })
}
Matrix.prototype.erase = function(){
  this.forEach(function(lex,x,y){ lex.erase() })
}
Matrix.prototype.fill = function(lex){
  this.fg = lex.fg
  this.bg = lex.bg
  this.char = lex.char
  this.opacity = lex.opacity
  this.forEach(function(el,x,y){
    el.assign(lex)
    el.build()
  })
}

Matrix.prototype.build = function(){
  this.forEach(function(lex,x,y){
    lex.build()
  })
}
Matrix.prototype.append = function(rapper){
  rapper = this.rapper = rapper || this.rapper
  if (! this.rapper) return
  this.aa.forEach(function(row, y){
    var div = document.createElement("div")
    row.forEach(function(lex, x) {
      div.appendChild(lex.span)
    })
    rapper.appendChild( div )
  })
}
Matrix.prototype.region = function(w,h,x,y) {
  w = w || 1
  h = h || 1
  x = x || 0
  y = y || 0
  var parent = this
  var mat = new Matrix(w, h, function(x,y){
    return parent.aa[y][x]
  })
  mat.f = this.f
  return mat
}
Matrix.prototype.setCell = function(lex,x,y){
  this.aa[y] && this.aa[y][x] && this.aa[y][x].assign(lex)
}
Matrix.prototype.getCell = function(x,y){
  if (this.aa[y] && this.aa[y][x]) return this.aa[y][x]
  else return null
}
Matrix.prototype.get = function(x,y){
  y = floor(mod(y || 0, this.h))
  x = floor(mod(x || 0, this.w))
  if (this.aa[y] && this.aa[y][x]) return this.aa[y][x]
  else return null
}

Matrix.prototype.resize = function(w,h){
  w = w || canvas.w
  h = h || canvas.h
  var div, row, lex
  var f = this.f, old_h = this.aa.length, old_w = this.aa[0].length
  var rapper = this.rapper
  w = max(w, 1)
  h = max(h, 1)
  if (h < old_h) {
    for (var y = old_h; y > h; y--) {
      row = this.aa.pop()
      div = row[0].span.parentNode
      row.forEach(function(lex, x){
        lex.demolish()
      })
      div.parentNode.removeChild(div)
    }
  }
  else if (h > old_h) {
    for (var y = old_h; y < h; y++) {
      div = document.createElement("div")
      rapper.appendChild( div )
      this.aa[y] = new Array (w)
      for (var x = 0; x < w; x++) {
        lex = this.aa[y][x] = f(x,y)
        div.appendChild(lex.span)
      }
    }
  }
  
  if (w < old_w) {
    this.aa.forEach(function(row, y){
      while (row.length > w) {
        lex = row.pop()
        lex.demolish()
      }
    })
  }
  else if (w > old_w) {
    this.aa.forEach(function(row, y){
      div = row[0].span.parentNode
      for (var x = row.length; x < w; x++) {
        lex = row[x] = f(x,y)
        div.appendChild(lex.span)
      }
    })
  }
  
  this.w = w
  this.h = h
  this.bind && this.bind()
  this.focus_clamp()
  if (this.rapper && this.rapper.parentNode != document.body) {
    this.resize_rapper()
  }
}
Matrix.prototype.resize_rapper = function(){
	var cell = canvas.aa[0][0].span
	var cw = cell.offsetWidth
	var ch = cell.offsetHeight
// 	if (canvas.grid) { ch++ }
	var width = cw * this.aa[0].length
	var height = ch * this.aa.length
	if (canvas.grid) { width++; height++ }
  if (this.rotated) {
    this.rapper.parentNode.classList.add("rotated")
    this.rapper.parentNode.style.height = (width) + "px"
    this.rapper.parentNode.style.width = (height) + "px"
    this.rapper.style.top = (width/2) + "px"
    // this.rapper.style.left = ((canvas_rapper.offsetHeight+20)/2) + "px"
  }
  else {
    this.rapper.parentNode.classList.remove("rotated")
    this.rapper.parentNode.style.height = ""
    this.rapper.style.width = 
      this.rapper.parentNode.style.width = (width) + "px"
    this.rapper.style.top = ""
    // canvas_rapper.style.left = "auto"
  }
}
Matrix.prototype.ascii = function () {
  var lines = this.aa.map(function(row, y){
    var last, line = ""
    row.forEach(function(lex, x) {
      line += lex.ascii()
    })
    return line // .replace(/\s+$/,"")
  })
  var txt = lines.join("\n")
  return txt
}
Matrix.prototype.ansi = function (opts) {
  var lines = this.aa.map(function(row, y){
    var last, line = ""
    row.forEach(function(lex, x) {
      if (lex.eqColor(last)) {
        line += lex.sanitize()
      } 
      else {
        line += lex.ansi()
        last = lex
      }
    })
    return line
  })
  var txt = lines.filter(function(line){ return line.length > 0 }).join('\\e[0m\\n') + "\\e[0m"
  return 'echo -e "' + txt + '"'
}
Matrix.prototype.mirc = function (opts) {
  var cutoff = false
  var lines = this.aa.map(function(row, y){
    var last, line = ""
    row.forEach(function(lex, x) {
      if (lex.eqColor(last)) {
        line += lex.sanitize()
      } 
      else {
        line += lex.mirc()
        last = lex
      }
    })
    if (opts && opts.cutoff && line.length > opts.cutoff) {
      cutoff = true
      return line.substr(0, opts.cutoff)
    }
    return line
  })
  
  var txt = lines.filter(function(line){ return line.length > 0 }).join('\n')
  
  if (cutoff) {
    txt = new String(txt)
    txt.cutoff = true
  }
  return txt
}
Matrix.prototype.irssi = function(opts){
  var mirc = this.mirc(opts)
  var txt = mirc  
                // .replace(/\%/g, '%%')
                .replace(/\\/g, '\\x5C')
                .replace(/\"/g, '\\\"')
                // .replace(/\'/g, '\\\'')
                .replace(/\`/g, '\\\`')
                .replace(/\$/g, '\\$')
                // .replace(/\n\s+/g, '\n')
                // .replace(/\s+$/g, '\n')
                // .replace(/^\n+/, '')
                .replace(/\n/g, '\\n')
                .replace(/\x02/g, '\\x02')
                .replace(/\x03/g, '\\x03')
 
  txt = unicode.escapeToEscapedBytes(txt)
  txt = '/exec -out printf "%b" "' + txt + '"\n'
  if (mirc.cutoff){
    txt = new String(txt)
    txt.cutoff = true
  }
  return txt
}
