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
  while (this.wrapper && this.wrapper.firstChild) {
    this.wrapper.removeChild(this.wrapper.firstChild);
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
Matrix.prototype.append = function(wrapper){
  wrapper = this.wrapper = wrapper || this.wrapper
  if (! this.wrapper) return
  this.aa.forEach(function(row, y){
    var div = document.createElement("div")
    row.forEach(function(lex, x) {
      div.appendChild(lex.span)
    })
    wrapper.appendChild( div )
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
  var wrapper = this.wrapper
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
      wrapper.appendChild( div )
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
  if (this.wrapper && this.wrapper.parentNode != document.body) {
    this.resize_wrapper()
  }
}
Matrix.prototype.resize_wrapper = function(){
  var cell = canvas.aa[0][0].span
  var cw = cell.offsetWidth
  var ch = cell.offsetHeight
//  if (canvas.grid) { ch++ }
  var width = cw * this.aa[0].length
  var height = ch * this.aa.length
  if (canvas.grid) { width++; height++ }
  this.wrapper.parentNode.style.height = ""
  this.wrapper.style.width =
  this.wrapper.parentNode.style.width = (width) + "px"
  this.wrapper.style.top = ""
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
    var last, line = "", bg_ = -1, fg_ = -1
    row.forEach(function(lex, x) {
      if (lex.eqColor(last)) {
        line += lex.sanitize()
      }
      else {
        [bg_, fg_, line_] = lex.ansi(bg_, fg_)
        line += line_; last = lex;
      }
    })
    return line
  })

  var txt = lines.filter(function(line){ return line.length > 0 }).join('\n')

  return txt
}
Matrix.prototype.mirc = function (opts) {
  var cutoff = false
  var lines = this.aa.map(function(row, y){
    var last, line = "", bg_ = -1, fg_ = -1
    row.forEach(function(lex, x) {
      if (lex.eqColor(last)) {
        line += lex.sanitize()
      }
      else {
        [bg_, fg_, line_] = lex.mirc(bg_, fg_)
        line += line_; last = lex;
      }
    })
    if (opts && opts.cutoff && line.length > opts.cutoff) {
      cutoff = true
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

var undo = (function(){

var max_states = 200;

// undotimetotal = 0;

var stack = {undo: [], redo: []};
var current_undo = null;
var dom = {undo: undo_el, redo: redo_el};
dom.undo.is_visible = dom.redo.is_visible = false

var LexState = function(lex){
  this.fg = lex.fg;
  this.bg = lex.bg;
  this.char = lex.char;
  this.opacity = lex.opacity;
};

var update_dom_visibility = function(type){
  var el = dom[type]
  if (el.is_visible){
    if (stack[type].length === 0) {
      el.classList.add('hidden')
      el.is_visible = false
    }
  } else if (stack[type].length > 0){
    el.classList.remove('hidden')
    el.is_visible = true
  }
}
var update_dom = function(){
  update_dom_visibility('undo')
  update_dom_visibility('redo')
}

// state is an undo or redo state that might contain these props
// {  lexs: {'0,0': LexState, ...},    // for sparse lex changes (eg brush, fill)
//    focus: {x:, y: },
//    size: {w:, h: },
//    rects: [{x:, y:, w:, h:, lexs: [LexState, ...]}, ...]
// }
var new_state = function(){
  var state = {lexs:{}};
  save_focus(canvas.focus_x, canvas.focus_y, state)
  return state
}
var new_redo = function(){
  return new_state()
}
var new_undo = function(){
  current_undo = new_state()
  stack.redo = []
  stack.undo.push(current_undo)
  if (stack.undo.length > max_states) stack.undo.shift();
  update_dom()
  return current_undo
}

var save_focus = function(x, y, state){
  state = state || current_undo
  state.focus = {x:x, y:y}
}
var save_size = function(w, h, state){
  state = state || current_undo
  state.size = {w:w, h:h};
}
// the reason for stringifying the x y coords is so that each
// coordinate is saved only once in an undo state.
// otherwise there would be problems with, eg, a brush stroke
// that passed over the same grid cell twice.
var save_lex = function(x, y, lex, state){
  // var start = Date.now()
  state = state || current_undo
  var lexs = state.lexs;
  var xy = x + "," + y;
  if (xy in lexs) return;
  lexs[xy] = new LexState(lex)
  // undotimetotal += Date.now() - start
}
var save_focused_lex = function(state){
  state = state || current_undo
  var x = canvas.focus_x
  var y = canvas.focus_y
  save_lex(x, y, canvas.aa[y][x], state)
}
var save_rect = function(xpos, ypos, w, h, state){
  if (w === 0 || h === 0) return;
  state = state || current_undo;
  state.rects = state.rects || []
  var aa = canvas.aa;
  var rect = {x: xpos, y: ypos, w: w, h: h, lexs: []}
  var lexs = rect.lexs
  var xlen = xpos + w
  var ylen = ypos + h
  for (var y = ypos; y < ylen; y++){
    var aay = aa[y]
    for (var x = xpos; x < xlen; x++){
      lexs.push(new LexState(aay[x]))
    }
  }
  state.rects.push(rect)
}
var save_resize = function(w, h, old_w, old_h, state){
  state = state || current_undo
  save_size(old_w, old_h, state)
  if (old_w > w){
    // .---XX
    // |   XX
    // |___XX
    save_rect(w, 0, old_w - w, old_h, state)
    if (old_h > h){
      // .----.
      // |    |
      // XXXX_|
      save_rect(0, h, w, old_h - h, state)
    }
  } else if (old_h > h){
    // .----.
    // |    |
    // XXXXXX
    save_rect(0, h, old_w, old_h - h, state)
  }
}

var restore_state = function(state){
  // all redo states will have a cached undo state on them
  // an undo state might have a cached redo state
  // if it doesn't have one, generate one
  var make_redo = ! ('redo' in state || 'undo' in state);
  var aa = canvas.aa
  var lex, lexs;

  if (make_redo){
    state.redo = new_redo()

    // copy saved rects that intersect with current canvas size
    // important to do this before resizing canvas
    if ('rects' in state){
      for (var ri=0, rect; rect=state.rects[ri]; ri++){
        if (rect.x >= canvas.w ||
            rect.y >= canvas.h) continue;
        var w = Math.min(rect.w, canvas.w - rect.x)
        var h = Math.min(rect.h, canvas.h - rect.y)
        save_rect(rect.x, rect.y, w, h, state.redo)
      }
    }
    if ('size' in state){
      save_resize(state.size.w, state.size.h, canvas.w, canvas.h, state.redo)
    }
  }

  if ('size' in state){
    canvas.resize(state.size.w, state.size.h, true);
  }

  if ('rects' in state){
    for (var ri=0, rect; rect=state.rects[ri]; ri++){
      lexs = rect.lexs
      for (var li=0; lex=lexs[li]; li++){
        var x = (li % rect.w) + rect.x
        var y = ((li / rect.w)|0) + rect.y
        aa[y][x].assign(lex)
      }
    }
  }

  lexs = state.lexs
  for (var key in lexs){
    var xy = key.split(',');
    lex = aa[xy[1]][xy[0]]
    if (make_redo)
      save_lex(xy[0], xy[1], lex, state.redo)
    lex.assign(lexs[key])
  }

  if ('focus' in state){
    canvas.focus_x = state.focus.x
    canvas.focus_y = state.focus.y
    if (current_canvas === canvas){
      canvas.focus()
    }
  }
}

var undo = function(){
  var state = stack.undo.pop();
  if (!state) return;

  restore_state(state)

  // now take the applied undo state and store it on the redo state
  // and push the redo state to the redo stack
  state.redo.undo = state
  stack.redo.push(state.redo)
  delete state.redo

  update_dom()
}

var redo = function(){
  var state = stack.redo.pop();
  if (!state) return;

  restore_state(state)

  state.undo.redo = state
  stack.undo.push(state.undo)
  delete state.undo

  update_dom()
}

return {
  stack: stack,
  new: new_undo,
//  new_redo: new_redo,
  save_focus: save_focus,
  save_size: save_size,
  save_lex: save_lex,
  save_focused_lex: save_focused_lex,
  save_rect: save_rect,
  save_resize: save_resize,
  undo: undo,
  redo: redo
}

})()
