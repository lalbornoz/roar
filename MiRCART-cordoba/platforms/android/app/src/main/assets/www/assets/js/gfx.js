
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

var draw = (function(){

  var last_point = [0,0]

  function down (e, lex, point) {
    var w = canvas.w, h = canvas.h
    erasing = (e.which == "3" || e.ctrlKey)
    changed = true
    if (e.shiftKey) {
      line (lex, last_point, point, erasing)
    }
    else {
      stamp (canvas, brush, point[0], point[1], erasing)
    }
    last_point[0] = point[0]
    last_point[1] = point[1]
  }

  function set_last_point (e, point) {
    last_point[0] = point[0]
    last_point[1] = point[1]
  }

  function move (e, lex, point) {
    var w = canvas.w, h = canvas.h
    line(lex, last_point, point, erasing)
    last_point[0] = point[0]
    last_point[1] = point[1]
  }

  function move_toroidal (e, lex, point) {
    var w = canvas.w, h = canvas.h
    var src_x_quantile = quantile( last_point[0], w )
    var src_y_quantile = quantile( last_point[1], h )
    var dst_x_quantile = quantile( point[0], w )
    var dst_y_quantile = quantile( point[1], h )
    var src_x_mod = mod( last_point[0], w )
    var src_y_mod = mod( last_point[1], h )
    var dst_x_mod = mod( point[0], w )
    var dst_y_mod = mod( point[1], h )
    // if we've moved across the edge of the board, draw two lines
    if (src_x_quantile != dst_x_quantile || src_y_quantile != dst_y_quantile) {
      var xa, ya
      if (src_x_quantile < dst_x_quantile) {
        xa = [
          [src_x_mod, dst_x_mod + w],
          [src_x_mod-w, dst_x_mod],
        ]
      }
      else if (src_x_quantile == dst_x_quantile) {
        xa = [
          [src_x_mod, dst_x_mod],
          [src_x_mod, dst_x_mod],
        ]
      }
      else {
        xa = [
          [src_x_mod, dst_x_mod-w],
          [src_x_mod+w, dst_x_mod],
        ]
      }

      if (src_y_quantile < dst_y_quantile) {
        ya = [
          [src_y_mod, dst_y_mod + h],
          [src_y_mod-h, dst_y_mod],
        ]
      }
      else if (src_y_quantile == dst_y_quantile) {
        ya = [
          [src_y_mod, dst_y_mod],
          [src_y_mod, dst_y_mod],
        ]
      }
      else {
        ya = [
          [src_y_mod, dst_y_mod-h],
          [src_y_mod+h, dst_y_mod],
        ]
      }
      line(lex, [ xa[0][0], ya[0][0] ], [ xa[0][1], ya[0][1] ], erasing)
      line(lex, [ xa[1][0], ya[1][0] ], [ xa[1][1], ya[1][1] ], erasing)
    }
    else {
      var x_a = mod( last_point[0], w )
      var y_a = mod( last_point[1], h )
      var x_b = mod( point[0], w )
      var y_b = mod( point[1], h )
      var last_point_mod = [x_b, y_b], point_mod = [x_a, y_a]
      line(lex, last_point_mod, point_mod, erasing)
    }
    last_point[0] = point[0]
    last_point[1] = point[1]
    // y = point.y
  }

  function point (lex, x, y, erasing) {
    stamp (canvas, brush, x, y, erasing)
  }

  function line (lex, a, b, erasing) {
    var len = dist(a[0], a[1], b[0], b[1])
    var bw = 1
    var x, y, i;
    for (var i = 0; i <= len; i += bw) {
      x = lerp(i / len, a[0], b[0])
      y = lerp(i / len, a[1], b[1])
      stamp (canvas, brush, x, y, erasing)
    }
  }

  function stamp (canvas, brush, x, y, erasing) {
    var hh = brush.w/2|0
    brush.forEach(function(lex, s, t){
      s = round( s + x-hh )
      t = round( t + y-hh )
      if (s >= 0 && s < canvas.w && t >= 0 && t < canvas.h) {
        if (lex.opacity === 0 && lex.char === ' ') return;
        var aa = canvas.aa[t][s]
        undo.save_lex(s, t, aa)
        if (erasing) {
          aa.erase(lex)
        }
        else {
          aa.stamp(lex, brush)
        }
      }
    })
  }

  function fill (lex, x, y) {
    var q = [ [x,y] ]
    var aa = canvas.aa
    var target = aa[y][x].clone()
    var n, w = 0, e = 0, j = 0
    var kk = 0
    // gets into a weird infinite loop if we don't break here.. :\
    if (target.eq(lex)) { return }
    LOOP: while (q.length) {
      n = q.shift()
      if (aa[n[1]][n[0]].ne(target)) {
        continue LOOP
      }
      w = e = n[0]
      j = n[1]
      WEST: while (w > 0) {
        if (aa[j][w-1].eq(target)) {
          w = w-1
        }
        else {
          break WEST
        }
      }
      EAST: while (e < canvas.w-1) {
        if (aa[j][e+1].eq(target)) {
          e = e+1
        }
        else {
          break EAST
        }
      }
      for (var i = w; i <= e; i++) {
        undo.save_lex(i, j, aa[j][i])
        aa[j][i].assign(lex)
        if (j > 0 && aa[j-1][i].eq(target)) {
          q.push([ i, j-1 ])
        }
        if (j < canvas.h-1 && aa[j+1][i].eq(target)) {
          q.push([ i, j+1 ])
        }
      }
    }
  }

  var draw = {}
  draw.down = down
  draw.set_last_point = set_last_point
  draw.move = move
  draw.move_toroidal = move_toroidal
  draw.stamp = stamp
  draw.line = line
  draw.point = point
  draw.fill = fill
  return draw

})()

