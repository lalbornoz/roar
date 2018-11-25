var canvas = current_canvas = (function(){

  var cols = 100
  var rows = 30

  var canvas = new Matrix (cols, rows, function(x,y){
    var lex = new Lex (x,y)
    lex.build()
    return lex
  })

  canvas.bind = function(){

    canvas.forEach(function(lex, x, y){

      if (lex.bound) return
      lex.bound = true
      var point = [x,y]
      lex.span.addEventListener('contextmenu', function(e){
        e.preventDefault()
      })
      lex.span.addEventListener('mousedown', function(e){
        e.preventDefault()
        dragging = true
        current_canvas = canvas
        if (e.altKey) {
          if (e.shiftKey) {
            blit.copy_from(canvas, brush, floor(x-brush.w/2), floor(y-brush.h/2))
            brush.mask(brush)
            draw.set_last_point(e, point)
          }
          else {
            brush.load(lex)
            brush.generate()
            dragging = false
          }
          return
        }
        else if (drawing) {
          undo.new()
          draw.down(e, lex, point)
        }
        else if (selecting) {
          selection.down(e, lex, point)
        }
        else if (transforming) {
          transform.down(e, lex, point)
        }
        else if (filling) {
          undo.new()
          draw.fill(brush, x, y)
        }
        canvas.focus(x, y)
      })

      lex.span.addEventListener("mousemove", function(e){
        mouse.x = x
        mouse.y = y
        if (! dragging) return
        if (drawing) {
          draw.move(e, lex, point)
        }
        else if (selecting) {
          selection.move(e, lex, point)
        }
        else if (transforming) {
          transform.move(e, lex, point)
        }
        canvas.focus(x, y)
      })

    })
  }

  canvas.min = 1
  canvas.max = 999

  // canvas.resize(1, 1, true) // wont create undo state
  canvas.resize = function(w, h, no_undo){
    var old_w = this.w, old_h = this.h
    w = this.w = clamp(w, this.min, this.max)
    h = this.h = clamp(h, this.min, this.max)
    if (old_w === w && old_h === h) return;

    if (!no_undo){
      undo.new()
      undo.save_resize(w, h, old_w, old_h)
     }

    canvas.__proto__.resize.call(canvas, w, h)
    controls.canvas_w.char = "" + w
    controls.canvas_w.build()
    controls.canvas_h.char = "" + h
    controls.canvas_h.build()
  }
  canvas.size_add = function(w, h){
    canvas.resize(canvas.w + w, canvas.h + h)
  }

  return canvas

})()
