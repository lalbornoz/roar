var brush = (function(){

  var brush = new Matrix (5, 5, function(x,y){
    var lex = new Lex (x,y)
    lex.build()
    return lex
  })

  brush.modified = false

  brush.mask = blit.circle

  brush.generate = function(){
    brush.fill(brush)
    brush.mask(brush)
  }

  brush.bind = function(){

    var last_point = [0,0]
    var dragging = false
    var erasing = false

    brush.forEach(function(lex, x, y){

      if (lex.bound) return
      lex.bound = true

      var point = [x,y]
      lex.span.addEventListener('contextmenu', function(e){
        e.preventDefault()
      })
      lex.span.addEventListener('mousedown', function(e){
        e.preventDefault()
        current_canvas = brush
        brush.modified = true
        dragging = true
        erasing = (e.which == "3" || e.ctrlKey)
        if (erasing) {
          lex.clear()
        }
        else {
          fillColor = brush.bg
          lex.assign(brush)
        }
        brush.focus(x, y)
      })
      lex.span.addEventListener('mousemove', function(e){
        e.preventDefault()
        if (! dragging) {
          return
        }
        erasing = (e.which == "3" || e.ctrlKey)
        if (erasing) {
          lex.clear()
        }
        else {
          lex.assign(brush)
        }
        brush.focus(x, y)
      })
    })
    window.addEventListener('mouseup', function(e){
      dragging = erasing = false
    })
  }

  brush.resize = function(w, h){
    w = this.w = clamp(w, this.min, this.max)
    h = this.h = clamp(h, this.min, this.max)
    brush.rebuild()
    controls.brush_w.char = "" + w
    controls.brush_w.build()
    controls.brush_h.char = "" + h
    controls.brush_h.build()
  }
  brush.size_add = function(w, h){
    brush.resize(brush.w + w, brush.h + h)
  }
  brush.expand = function(i){
    brush.size_add(i, i)
  }
  brush.contract = function(i){
    brush.size_add(-i, -i)
  }

  brush.load = function(lex){
    brush.char = lex.char
    brush.fg = lex.fg
    brush.bg = lex.bg
    brush.opacity = 1
  }

  brush.min = 1
  brush.max = 100

  brush.char = " "
  brush.fg = 0
  brush.bg = 1
  brush.opacity = 1

  brush.draw_fg = true
  brush.draw_bg = true
  brush.draw_char = true

  return brush

})()

var custom = (function(){

  var exports = {}

  exports.clone = function (){
    var new_brush = brush.clone()
    var wrapper = document.createElement("div")
    wrapper.className = "custom"
    new_brush.append(wrapper)
    custom_wrapper.appendChild(wrapper)
    // store in localstorage?
    wrapper.addEventListener("click", function(e){
      if (e.shiftKey) {
        wrapper.parentNode.removeChild(wrapper)
        delete new_brush
      } else {
        // load this brush
        exports.load(new_brush)
      }
    })
  }

  exports.load = function(new_brush){
    brush.assign( new_brush )
  }

  return exports

})()
