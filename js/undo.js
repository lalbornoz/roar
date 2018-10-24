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
