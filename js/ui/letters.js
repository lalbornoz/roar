var letters = (function(){

  var last_charset = ""
  var charset_index = 0
  var charsets = [
    'Basic Latin',
    'Latin-1 Supplement',
    'Box Drawing',
    'Block Elements',
  ]
  
  var letters = new Matrix (1, 1, function(x,y){
    var lex = new Lex (x,y)
    return lex
  })
  
  letters.charset = ""

  letters.repaint = function(charset){
    letters.charset = charset = charset || last_charset
    last_charset = charset
    var chars = unicode.block(charset, 32)
    if (chars[0] != " ") chars.unshift(" ")
    if (canvas.vertical) {
      letters.resize( Math.ceil( chars.length / 16 ), 16 )
    }
    else {
      letters.resize( 32, Math.ceil( chars.length / 32 ) )
    }

    var i = 0

    letters.forEach(function(lex,x,y){
      if (canvas.vertical) { x=x^y;y=x^y;x=x^y }
      var char = chars[i++]
      if (palette.chars.indexOf(brush.char) > 1) {
        lex.bg = brush.fg
        lex.fg = brush.bg
      }
      else {
        lex.bg = colors.black
        lex.fg = brush.fg == fillColor ? colors.black : brush.fg
      }
      lex.char = char
      lex.opacity = 1
      lex.build()
    })
  }
  
  letters.bind = function(){
    letters.forEach(function(lex,x,y){
      if (lex.bound) return
      lex.bound = true

      lex.span.addEventListener('mousedown', function(e){
        e.preventDefault()
        if (e.shiftKey) {
          charset_index = (charset_index+1) % charsets.length
          letters.repaint(charsets[charset_index])
          return
        }
        else if (e.ctrlKey || e.which == 3) {
          brush.char = lex.char
          brush.bg = brush.fg
          brush.fg = fillColor
        }
        else {
          brush.char = lex.char
          if (lex.char == " ") {
            brush.bg = brush.fg
          }
          else if (brush.bg != fillColor) {
            brush.fg = brush.bg
            brush.bg = fillColor
          }
        }
        if (! brush.modified) {
          brush.generate()
        }
        palette.repaint()
      })
      lex.span.addEventListener('contextmenu', function(e){
        e.preventDefault()
      })
    })
  }
  
  return letters
})()