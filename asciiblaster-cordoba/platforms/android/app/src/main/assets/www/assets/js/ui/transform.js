var transform = (function(){

  var p = [0,0], q = [0,0]
  var mode
  var copy

  function down (e, lex, point){
    p[0] = point[0]
    p[1] = point[1]
    q[0] = e.pageX
    q[1] = e.pageY
    undo.new()
    undo.save_rect(0, 0, canvas.w, canvas.h)
    copy = canvas.clone()
    mode.init(e)
  }
  function move (e, lex, point){
    var pdx = point[0] - p[0]
    var pdy = point[1] - p[1]
    var dx = e.pageX - q[0]
    var dy = e.pageY - q[1]
    var w = canvas.w
    var h = canvas.h
    mode.before(dx, dy, pdx, pdy, point)
    for (var x = 0; x < w; x++) {
      for (var y = 0; y < h; y++) {
        lex = canvas.get(x, y)
        if (! mode.shade( copy, canvas, lex, x, y, w, h )) {
          lex.build()
        }
      }
    }
  }
  function up (e){
  }

  var modes = {

    rotate: {
      init: function(e){
        mode.theta = 0
      },
      before: function(dx, dy){
        var radius = dist(0, 0, dx, dy)
        if (radius < 10) return
        mode.theta = angle(0, 0, dx, -dy)
      },
      shade: function(src, dest, lex, x, y, w, h){
        x = (x/w) * 2 - 1
        y = (y/h) * 2 - 1
        var ca = cos(mode.theta)
        var sa = sin(mode.theta)
        var a = x * ca - y * sa
        var b = x * sa + y * ca
        x = (a + 1) / 2 * w
        y = (b + 1) / 2 * h
        var copy = src.get(x, y)
        lex.assign(copy)
        return true
      },
    },

    scale: {
      init: function(e){
        mode.independent = e.shiftKey || e.altKey || e.metaKey
        mode.x_scale = mode.y_scale = 0
      },
      before: function(dx, dy, pdx, pdy){
        if (mode.independent) {
          mode.x_scale = Math.pow(2, -pdx / (canvas.w / 8))
          mode.y_scale = Math.pow(2, -pdy / (canvas.h / 8))
        }
        else {
          mode.x_scale = mode.y_scale = Math.pow(2, -pdx / (canvas.w / 8))
        }
      },
      shade: function(src, dest, lex, x, y, w, h){
        x = ((x-p[0])/w) * 2 - 1
        y = ((y-p[1])/h) * 2 - 1
        x *= mode.x_scale
        y *= mode.y_scale
        x = (x + 1) / 2 * w
        y = (y + 1) / 2 * h
        var copy = src.get(x+p[0], y+p[1])
        lex.assign(copy)
        return true
      },
    },

    translate: {
      init: function(e){
        mode.dx = mode.dy = 0
      },
      before: function(dx, dy, pdx, pdy){
        mode.dx = -pdx
        mode.dy = -pdy
      },
      shade: function(src, dest, lex, x, y, w, h){
        var copy = src.get(x+mode.dx, y+mode.dy)
        lex.assign(copy)
        return true
      },
    },

    slice: {
      init: function(e){
        mode.is_y = ! (e.altKey || e.metaKey)
        mode.reverse = !! (e.shiftKey)
        mode.position = 0
        mode.direction = 0
        mode.last_dd = -1
      },
      before: function(dx, dy, pdx, pdy, point){
        var new_position = mode.is_y ? point[1] : point[0]
        var dd = mode.is_y ? pdx : pdy

        if (mode.position !== new_position) {
          mode.position = new_position
          mode.direction = 0
        }
        if (mode.last_dd !== -1) {
          mode.direction = mode.last_dd - dd
        }
        console.log(mode.position)
        mode.last_dd = dd
        copy.assign(canvas)
      },
      shade: function(src, dest, lex, x, y, w, h){
        if (mode.is_y) {
          if (y >= mode.position || (mode.reverse && mode.position >= y)) {
            var copy = src.get(x + mode.direction, y)
            lex.assign(copy)
          }
        }
        else if (x >= mode.position || (mode.reverse && mode.position >= x)) {
          var copy = src.get(x, y + mode.direction)
          lex.assign(copy)
        }
        return true
      },
    },

/*
    mode: {
      init: function(e){
      },
      before: function(dx, dy, pdx, pdy){
      },
      shade: function(src, dest, lex, x, y, w, h){
      },
    },
*/
  }

  function set_mode(m){
    if (m in modes) {
      mode = modes[m]
      transforming = true
    }
  }

  function done(){
    transforming = false
    copy && copy.demolish()
  }

  return {
    down: down,
    move: move,
    up: up,
    set_mode: set_mode,
    modes: modes,
    done: done,
  }

})()