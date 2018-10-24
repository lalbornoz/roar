var shader = (function(){
  var fn_str, fn, lex
  var exports = {}
  var animating = false
  
  exports.init = function(){
    lex = new Lex (0, 0)
    exports.build(demo_shader.innerHTML)
  }
  exports.build = function (fn_str){
    try {
      new_fn = new Function('lex', 'x', 'y', 'w', 'h', 't', fn_str)
      new_fn(lex, 0, 0, 1, 1, 0)
    }
    catch (e) {
      throw 'Shader execution error'
    }
    exports.fn = fn = new_fn
    return fn
  }
  exports.run = function(canvas){
    var t = +new Date
    shader.canvas = shader.canvas || canvas
    var w = shader.canvas.w, h = shader.canvas.h
    shader.canvas.forEach(function(lex, x, y){
      fn(lex, x, y, w, h, t)
      lex.build()
    })
  }
  exports.toggle = function(state){
    animating = typeof state == "boolean" ? state : ! animating
    shader_fps_el.classList.toggle('hidden')
    return animating
  }
  exports.pause = function(){
    animating = false
    shader_fps_el.classList.add('hidden')
    shader.fps_time = 0
  }
  exports.play = function(){
    animating = true
    shader_fps_el.classList.remove('hidden')
  }
  exports.animate = function (t){
    requestAnimationFrame(exports.animate)
    if (! animating) { return } 
    if (shader.fps_time){
      var ms = Date.now() - shader.fps_time
      fps = 1000 / ms
      shader_fps_el.innerHTML = (fps | 0) + ' fps'
    }
    shader.fps_time = Date.now()
    exports.run(canvas)
  }
  
  return exports

})()
