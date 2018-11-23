
var dragging = false
var drawing = false
var erasing = false
var selecting = false
var filling = false
var changed = false
var transforming = false
var mirror_x = false
var mirror_y = false
var focused

var canvas, tools, palette, controls, brush, mode 
var current_tool, current_filetool, current_canvas
var mouse = { x: 0, y: 0 }

function init () {
  build()
  bind()
}
function build () {
  canvas.append(canvas_rapper)
  brush.append(brush_rapper)
  palette.append(palette_rapper)
  letters.append(letters_rapper)
  letters.repaint("Basic Latin")
  
  controls.circle.focus()

  brush.bg = colors.red
  brush.generate()
  brush.build()

  // controls.grid.use()
  canvas.resize_rapper()
}
function bind () {
  canvas.bind()
  palette.bind()
  letters.bind()
  brush.bind()
  controls.bind()
  keys.bind()
  clipboard.bind()
  
  window.addEventListener('mouseup', function(e){
    dragging = erasing = false
    
    var ae = document.activeElement

    if (ae !== import_textarea) {
      if (is_desktop) cursor_input.focus()
    }

    if (selecting) {
      selection.up(e)
    }
    else if (transforming) {
      transform.up(e)
    }
  })
  window.addEventListener("touchend", function(){
    if (current_tool.name === "text") {
      if (is_desktop) cursor_input.focus()
    }
    dragging = false
  })
  
  window.addEventListener('mousedown', function(e){
    // if (is_desktop) { cursor_input.focus() }
  })
 
  document.addEventListener('DOMContentLoaded', function(){
    if (is_desktop) { cursor_input.focus() }
    document.body.classList.remove('loading')
  })
  
  window.onbeforeunload = function() {
    // if (changed && !in_iframe()) return "You have edited this drawing."
  }

  function in_iframe () {
    try {
      return window.self !== window.top;
    } catch (e) {
      return true;
    }
  }
}

init()
