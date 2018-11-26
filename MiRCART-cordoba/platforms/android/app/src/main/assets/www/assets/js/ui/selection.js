var selection = (function(){

  var creating = false, moving = false, copying = false

  var selection_canvas = new Matrix (1, 1, function(x,y){
    var lex = new Lex (x,y)
    lex.build()
    return lex
  })

  var selector_el = document.createElement("div")
  selector_el.className = "selector_el"
  selection_canvas.append(selector_el)
  document.body.appendChild(selector_el)

  // in selection mode..
  // - we start by clicking the canvas. this positions the selection, and copies
  //   the character
  // - then we drag down and to the right. this resizes the selection and pushes new
  //   rows and columns. each of these copies the character underneath.
  // - on mouseup, the selection is locked. then..
  // - drag the selection to move it -- this "cuts" it and leaves a blank space on the canvas.
  // - shift-drag the selection to copy it

  var a = [0, 0]
  var b = [0, 0]
  var c = [0, 0]
  var d = [0, 0]

  function reset () {
    a[0] = a[1] = b[0] = b[1] = 0
  }
  function left (a,b) { return min(a[0],b[0]) }
  function top (a,b) { return min(a[1],b[1]) }
  function right (a,b) { return max(a[0],b[0]) }
  function bottom (a,b) { return max(a[1],b[1]) }
  function width (a,b) { return abs(a[0]-b[0])+1 }
  function height (a,b) { return abs(a[1]-b[1])+1 }
  function mag_x (a,b) { return a[0]-b[0] }
  function mag_y (a,b) { return a[1]-b[1] }
  function orient (a,b) {
    var l = left(a,b), m = top(a,b), n = right(a,b), o = bottom(a,b)
    a[0] = l ; a[1] = m ; b[0] = n ; b[1] = o
  }

  function contains (a,b,point) {
    var contains_x = a[0] <= point[0] && point[0] <= b[0]
    var contains_y = a[1] <= point[1] && point[1] <= b[1]
    return (contains_x && contains_y)
  }
  function reposition (aa, bb) {
    aa = aa || a
    bb = bb || b
    var cell = canvas.aa[top(aa, bb)][left(aa, bb)].span
    var cell_left = cell.offsetLeft
    var cell_top = cell.offsetTop
    var cell_width = cell.offsetWidth
    var cell_height = cell.offsetHeight

    var w = width(aa, bb)
    var h = height(aa, bb)

    selector_el.style.top = (cell_top-1) + "px"
    selector_el.style.left = (cell_left-1) + "px"
    selector_el.style.width = (cell_width*w+1) + "px"
    selector_el.style.height = (cell_height*h+1) + "px"
  }
  function down (e, lex, point){
    if ( ! contains(a,b,point) ) {
      copying = false
      moving = false
      creating = true
      a[0] = point[0]
      a[1] = point[1]
      b[0] = point[0]
      b[1] = point[1]
      reposition(a,b)
      selection.hidden = false
      selector_el.classList.add("creating")
    } else {
      copying = false
      moving = true
      creating = false
      c[0] = point[0]
      c[1] = point[1]
      d[0] = point[0]
      d[1] = point[1]
    }
    show()
    selector_el.classList.remove("dragging")
  }
  function move (e, lex, point){
    if (creating) {
      b[0] = point[0]
      b[1] = point[1]
      reposition(a,b)
    }
    else if (moving) {
      d[0] = point[0]
      d[1] = point[1]
      var dx = - clamp( mag_x(c,d), b[0] - canvas.w + 1, a[0] )
      var dy = - clamp( mag_y(c,d), b[1] - canvas.h + 1, a[1] )
      reposition( [ a[0] + dx, a[1] + dy ], [ b[0] + dx, b[1] + dy ])
    }
    else if (copying) {
    }
  }
  function up (e) {
    if (creating) {
      orient(a,b)
      selection_canvas.resize(width(a,b), height(a,b))
      reposition(a,b)
      blit.copy_from( canvas, selection_canvas, a[0], a[1] )
      selection_canvas.build()
      selector_el.classList.remove("creating")
    }
    if (moving) {
      var dx = - clamp( mag_x(c,d), b[0] - canvas.w + 1, a[0] )
      var dy = - clamp( mag_y(c,d), b[1] - canvas.h + 1, a[1] )
      a[0] += dx
      a[1] += dy
      b[0] += dx
      b[1] += dy
      undo.new()
      undo.save_rect(a[0], a[1], b[0] - a[0] + 1, b[1] - a[1] + 1)
      blit.copy_to( canvas, selection_canvas, a[0], a[1] )
    }
    if (copying) {
    }
    creating = moving = copying = false
    selector_el.classList.remove("dragging")
  }

  function show () {
    selecting = true
  }
  function hide () {
    reset()
    selector_el.style.top = "-9999px"
    selector_el.style.left = "-9999px"
    selector_el.style.width = "0px"
    selector_el.style.height = "0px"
    creating = moving = copying = false
    selection.hidden = true
    selecting = false
  }

  var selection = {}
  selection.reposition = reposition
  selection.down = down
  selection.move = move
  selection.up = up
  selection.canvas = selection_canvas
  selection.show = show
  selection.hide = hide
  selection.hidden = true
  return selection

})()
