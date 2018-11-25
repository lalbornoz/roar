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

var palette = (function(){

  var palette = new Matrix (32, 2, function(x,y){
    var lex = new Lex (x,y)
    return lex
  })

  var palette_index = localStorage.getItem("ascii.palette") || 1
  var palette_list = [all_hue, all_inv_hue, mirc_color, mirc_color_reverse]
  var palette_fn = palette_list[palette_index]
  var dither = {
    aa: '▓▒░ ',
    a: '▓',
    b: '▒',
    c: '░',
    d: ' ',
    p: function(n){
      return dither.aa[Math.floor(Math.abs(n) % 4)]
    }
  }
  palette.chars = "  " + dither.a + dither.b + dither.c

  palette.repaint = function(){
    var xw = use_experimental_palette ? 5 : 2
    if (canvas.vertical) {
      palette.resize( xw, 16 )
    }
    else {
      palette.resize( 32, xw )
    }

    palette.forEach(function(lex,x,y){
      if (canvas.vertical) { x=x^y;y=x^y;x=x^y;x*=2 }
      if (y < 2) {
        lex.bg = palette_fn(x>>1)
        lex.fg = palette_fn(x>>1)
      }
      else {
        lex.bg = fillColor
        lex.fg = palette_fn(x>>1)
      }
      lex.char = palette.chars[y]
      lex.opacity = 1
      lex.build()
      if (lex.char == "_") lex.char = " "
    })
  }
  palette.repaint()
  var use_experimental_palette = false
  palette.experimental = function(state){
    use_experimental_palette = typeof state == "boolean" ? state : ! use_experimental_palette
    use_experimental_palette ? palette.resize(32, 5) : palette.resize(32, 2)
    palette.repaint()
    return use_experimental_palette
  }

  palette.bind = function(){
    palette.forEach(function(lex, x, y){
      if (lex.bound) return
      lex.bound = true

      lex.span.addEventListener('mousedown', function(e){
        e.preventDefault()
        if (e.shiftKey) {
          palette_index = (palette_index+1) % palette_list.length
          localStorage.setItem("ascii.palette", palette_index)
          palette_fn = palette_list[palette_index]
          palette.repaint()
          return
        }
        if (e.ctrlKey || e.which == 3) return
        if (brush.char == " " && lex.char == " ") {
          brush.fg = lex.fg
          brush.bg = lex.bg
          brush.char = lex.char
        }
        else if (lex.char != " ") {
          brush.fg = lex.bg
          brush.bg = lex.fg
          brush.char = lex.char
        }
        else {
          brush.fg = lex.bg
          brush.bg = fillColor
//           brush.char = lex.char
        }
        brush.opacity = lex.opacity
        if (! brush.modified) {
          brush.generate()
        }
        if (filling || e.ctrlKey) {
          fillColor = lex.bg
        }
        letters.repaint()
      })

      lex.span.addEventListener('contextmenu', function(e){
        e.preventDefault()
        fillColor = y ? lex.fg : lex.bg
        palette.repaint()
        brush.fg = lex.fg
        brush.char = lex.char
        brush.opacity = lex.opacity
        brush.generate()
        brush_wrapper.style.borderColor = css_reverse_lookup[fillColor]
        return
      })

    })
  }

  brush_wrapper.style.borderColor = css_reverse_lookup[fillColor]

  return palette

})()
