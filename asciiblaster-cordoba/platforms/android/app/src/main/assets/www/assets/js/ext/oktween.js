/*
  oktween.add({
    obj: el.style,
    units: "px",
    from: { left: 0 },
    to: { left: 100 },
    duration: 1000,
    easing: oktween.easing.circ_out,
    update: function(obj){
      console.log(obj.left)
    }
    finished: function(){
      console.log("done")
    }
  })
*/

var oktween = (function(){
  var oktween = {}
  var tweens = oktween.tweens = []
  var last_t = 0
  var id = 0
  oktween.speed = 1
  oktween.raf = requestAnimationFrame
  oktween.add = function(tween){
    tween.id = id++
    tween.obj = tween.obj || {}
    if (tween.easing) {
      if (typeof tween.easing == "string") {
        tween.easing = oktween.easing[tween.easing]
      }
    }
    else {
      tween.easing = oktween.easing.linear
    }
    if (! ('from' in tween) && ! ('to' in tween)) {
      tween.keys = []
    }
    else if (! ('from' in tween) ) {
      tween.from = {}
      tween.keys = Object.keys(tween.to)
      tween.keys.forEach(function(prop){
        tween.from[prop] = parseFloat(tween.obj[prop])
      })
    }
    else {
      tween.keys = Object.keys(tween.from)
    }
    tween.delay = tween.delay || 0
    tween.start = last_t + tween.delay
    tween.done = false
    tween.after = tween.after || []
    tween.then = function(fn){ tween.after.push(fn); return tween }
    tween.cancel = function(){
      var index = tweens.indexOf(tween)
      if (index != -1) tweens.splice(index, 1)
      tween.obj = null
      tween.after = null
      tween.done = null
    }
    tween.tick = 0
    tween.skip = tween.skip || 1
    tween.dt = 0
    tweens.push(tween)
    return tween
  }
  oktween.update = function(t) {
    oktween.raf(oktween.update)
    last_t = t * oktween.speed
    if (tweens.length == 0) return
    var done = false
    tweens.forEach(function(tween, i){
      var dt = Math.min(1.0, (t - tween.start) / tween.duration)
      tween.tick++
      if (dt < 0 || (dt < 1 && (tween.tick % tween.skip != 0))) return
      var ddt = tween.dt = tween.easing(dt)
      tween.keys.forEach(function(prop){
        val = lerp( ddt, tween.from[prop], tween.to[prop] )
        if (tween.round) val = Math.round(val)
        if (tween.units) val = (Math.round(val)) + tween.units
        tween.obj[prop] = val
      })
      tween.update && tween.update(tween.obj, dt)
      if (dt == 1) {
        tween.finished && tween.finished(tween)
        if (tween.after.length) {
          var twn = tween.after.shift()
          twn.obj = twn.obj || tween.obj
          twn.after = tween.after
          oktween.add(twn)
        }
        if (tween.loop) {
          tween.start = t + tween.delay
        }
        else {
          done = tween.done = true
        }
      }
    })
    if (done) {
      tweens = tweens.filter(function(tween){ return ! tween.done })
    }
  }
  function lerp(n,a,b){ return (b-a)*n+a }

  // requestAnimationFrame(oktween.update)

  oktween.easing = {
    linear: function(t){
      return t
    },
    circ_out: function(t) {
      return Math.sqrt(1 - (t = t - 1) * t)
    },
    circ_in: function(t){
      return -(Math.sqrt(1 - (t * t)) - 1)
    },
    circ_in_out: function(t) {
      return ((t*=2) < 1) ? -0.5 * (Math.sqrt(1 - t * t) - 1) : 0.5 * (Math.sqrt(1 - (t -= 2) * t) + 1)
    },
    quad_in: function(n){
      return Math.pow(n, 2)
    },
    quad_out: function(n){
      return n * (n - 2) * -1
    },
    quad_in_out: function(n){
      n = n * 2
      if(n < 1){ return Math.pow(n, 2) / 2 }
      return -1 * ((--n) * (n - 2) - 1) / 2
    },
    cubic_bezier: function (mX1, mY1, mX2, mY2) {
      function A(aA1, aA2) { return 1.0 - 3.0 * aA2 + 3.0 * aA1; }
      function B(aA1, aA2) { return 3.0 * aA2 - 6.0 * aA1; }
      function C(aA1)      { return 3.0 * aA1; }

      // Returns x(t) given t, x1, and x2, or y(t) given t, y1, and y2.
      function CalcBezier(aT, aA1, aA2) {
        return ((A(aA1, aA2)*aT + B(aA1, aA2))*aT + C(aA1))*aT;
      }

      // Returns dx/dt given t, x1, and x2, or dy/dt given t, y1, and y2.
      function GetSlope(aT, aA1, aA2) {
        return 3.0 * A(aA1, aA2)*aT*aT + 2.0 * B(aA1, aA2) * aT + C(aA1);
      }

      function GetTForX(aX) {
        // Newton raphson iteration
        var aGuessT = aX;
        for (var i = 0; i < 10; ++i) {
          var currentSlope = GetSlope(aGuessT, mX1, mX2);
          if (currentSlope == 0.0) return aGuessT;
          var currentX = CalcBezier(aGuessT, mX1, mX2) - aX;
          aGuessT -= currentX / currentSlope;
        }
        return aGuessT;
      }

      return function(aX) {
        if (mX1 == mY1 && mX2 == mY2) return aX; // linear
        return CalcBezier(aX, mY1, mY2);
      }
    }
  }
  
  return oktween
})()
