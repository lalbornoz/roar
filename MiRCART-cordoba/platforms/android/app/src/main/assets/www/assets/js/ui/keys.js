var keys = (function(){

  var keys = {}
  keys.bind = function(){
    cursor_input.addEventListener('keydown', function(e){

      // console.log("keycode:", e.keyCode)
      if (e.altKey) {
        document.body.classList.add("dropper")
      }

      switch (e.keyCode) {
        case 27: // esc
          if (!selection.hidden && current_canvas === canvas){
            selection.hide()
            selection.show()
          } else if (focused){
            focused.blur()
          }
          return
      }

      if (window.focused && focused.raw_key) {
        focused.raw_key(e)
        return
      }

      switch (e.keyCode) {
        case 219: // [
          if (current_tool.name != "text") {
            e.preventDefault()
            brush.contract(1)
            brush.modified = false
            check_if_lost_focus()
          }
          break
        case 221: // ]
          if (current_tool.name != "text") {
            e.preventDefault()
            brush.expand(1)
            brush.modified = false
          }
          break
        case 8: // backspace
          e.preventDefault()
          if (current_canvas === canvas)
            undo.new()
          current_canvas.focus_add(-1, 0)
          if (current_canvas === canvas)
            undo.save_focused_lex()
          focused.char = " "
          focused.build()
          return
        case 13: // return
          e.preventDefault()
          current_canvas.focusLex(focused.y, focused.x+1)
          return
        case 38: // up
          e.preventDefault()
          current_canvas.focus_add(0, -1)
          break
        case 40: // down
          e.preventDefault()
          current_canvas.focus_add(0, 1)
          break
        case 37: // left
          e.preventDefault()
          current_canvas.focus_add(-1, 0)
          break
        case 39: // right
          e.preventDefault()
          current_canvas.focus_add(1, 0)
          break
        // use typical windows and os x shortcuts
        // undo: ctrl-z or cmd-z
        // redo: ctrl-y or shift-cmd-z
        case 89: // y
          if (!e.ctrlKey && !e.metaKey) break;
          e.preventDefault();
          undo.redo();
          break
        case 90: // z
          if (!e.ctrlKey && !e.metaKey) break;
          e.preventDefault();
          if (e.shiftKey)
            undo.redo();
          else
            undo.undo();
          break
  //      default:
  //        if (focused) { focused.key(undefined, e.keyCode) }
      }
    })

    cursor_input.addEventListener('input', function(e){
  /*
      if (! e.metaKey && ! e.ctrlKey && ! e.altKey) {
        e.preventDefault()
      }
  */
      var char = cursor_input.value
      cursor_input.value = ""

      // console.log("input:", char)

      if (current_tool.name != "text" && ! brush.modified) {
        brush.char = char
        if (char == " ") {
          brush.bg = brush.fg
        }
        else if (brush.bg != fillColor) {
          brush.fg = brush.bg
          brush.bg = fillColor
        }
        brush.rebuild()
      }

      if (focused && char) {
        var y = focused.y, x = focused.x
        if (current_canvas === canvas){
          undo.new()
          undo.save_focused_lex()
        }
        var moving = focused.key(char, e.keyCode)
        if ( ! moving || ! ('y' in focused && 'x' in focused) ) { return }
        current_canvas.focus_add(1, 0)
      }
    })

    cursor_input.addEventListener("keyup", function(e){
      if (! e.altKey) {
        document.body.classList.remove("dropper")
      }
    })
  }

  keys.int_key = function (f) {
    return function (key, keyCode) {
      var n = parseInt(key)
      ! isNaN(n) && f(n)
    }
  }

  keys.arrow_key = function (fn) {
    return function (e){
      switch (e.keyCode) {
        case 38: // up
          e.preventDefault()
          fn(1)
          break
        case 40: // down
          e.preventDefault()
          fn(-1)
          break
      }
    }
  }
  keys.left_right_key = function (fn) {
    return function (e){
      switch (e.keyCode) {
        case 39: // right
          e.preventDefault()
          fn(1)
          break
        case 38: // up
        case 40: // down
          e.preventDefault()
          fn(0)
          break
        case 37: // left
          e.preventDefault()
          fn(-1)
          break
      }
    }
  }

  keys.single_numeral_key = function (lex, fn) {
    return keys.int_key(function(n, keyCode){
      if (n == 0) n = 10
      lex.blur()
      fn(n)
    })
  }
  keys.multi_numeral_key = function (lex, digits){
    return keys.int_key(function(n, keyCode){
      lex.read()
      if (lex.char.length < digits) {
        n = parseInt(lex.char) * 10 + n
      }
      lex.char = ""+n
      lex.build()
    })
  }
  keys.multi_numeral_blur = function (lex, fn){
    return function(){
      var n = parseInt(lex.char)
      if (isNaN(n)) return
      fn(n)
    }
  }

  return keys
})()

function check_if_lost_focus() {
  if (! window.focused || ! window.focused.span)
  window.focused = canvas.aa[0][0]
}
