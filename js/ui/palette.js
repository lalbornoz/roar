var palette = (function(){

  var palette = new Matrix (32, 2, function(x,y){
    var lex = new Lex (x,y)
    return lex
  })

  var palette_index = localStorage.getItem("ascii.palette") || 1
  var palette_list = [all_hue, all_inv_hue, mirc_color, mirc_color_reverse]
  var palette_fn = palette_list[palette_index]
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
        brush_rapper.style.borderColor = css_reverse_lookup[fillColor]
        return
      })

    })
  }

  brush_rapper.style.borderColor = css_reverse_lookup[fillColor]

  return palette

})()
