var blit = (function(){
  var blit = {}
  blit.and = blit.atop = function(A, B, x, y){
    x = x || 0 ; y = y || 0
    B.forEach(function(lex, u, v){
      var cell = A.getCell(u+x, v+y)
      if (cell && lex.opacity > 0) {
        cell.assign(lex)
      }
    })
  }
  blit.or = blit.under = function(A, B, x, y){
    x = x || 0 ; y = y || 0
    B.forEach(function(lex, u, v){
      var cell = A.getCell(u+x, v+y)
      if (cell && cell.opacity == 0) {
        cell.assign(lex)
      }
    })
  }
  // copy the region of A beginning at x,y into B
  blit.copy_from = function(A, B, x, y){
    x = x || 0 ; y = y || 0
    B.forEach(function(lex, u, v){
      var cell = A.getCell(u+x, v+y)
      if (cell) {
        lex.assign(cell)
      }
    })
  }
  blit.copy_toroidal_from = function(A, B, x, y){
    x = x || 0 ; y = y || 0
    B.forEach(function(lex, u, v){
      var cell = A.get(u+x, v+y)
      if (cell) {
        lex.assign(cell)
      }
    })
  }
  blit.copy_to = function(A, B, x, y){
    x = x || 0 ; y = y || 0
    B.forEach(function(lex, u, v){
      var cell = A.getCell(u+x, v+y)
      if (cell) {
        cell.assign(lex)
      }
    })
  }
  blit.invert = function(A, B, x, y){
    x = x || 0 ; y = y || 0
    B.forEach(function(lex, u, v){
      var cell = A.getCell(u+x, v+y)
      if (cell && lex.opacity > 0) {
        cell.fg = get_inverse(cell.fg)
        cell.bg = get_inverse(cell.bg)
      }
    })
  }
  var distance_rect = function(x, y, ratio){
    return Math.sqrt((Math.pow(y * ratio, 2)) + Math.pow(x, 2))
  }
  var distance_square = function(x, y, ratio){
    return Math.sqrt((Math.pow(y * ratio, 2)) + Math.pow(x * ratio, 2))
  }
  blit.circle = function(A, lex){
    var hw = brush.w/2, hh = brush.h/2
    var ratio, distance
    
    if (brush.w === brush.h){
      distance = distance_square
      ratio = hw / hh * (brush.w === 3 || brush.w === 5 ? 1.2 : 1.05)
    } else {
      distance = distance_rect
      ratio = hw / hh
    }

    A.forEach(function(lex,x,y) {
      if (distance(x - hw + 0.5, y - hh + 0.5, ratio) > hw){
        lex.clear()
      }
    })
  }
  blit.cross = function(A, lex){
    A.forEach(function(lex,x,y) {
      if ((x+y)%2) {
        lex.clear()
      }
    })
  }
  blit.inverted_cross = function(A, lex){
    // 1x1 brush should still draw something
    if (A.w == 1 && A.h == 1) {
      return
    }
    A.forEach(function(lex,x,y) {
      if (!((x+y)%2)) {
        lex.clear()
      }
    })
  }
  blit.square = function(A, lex){
  	// i.e. no transparency
  }
  return blit
})()
