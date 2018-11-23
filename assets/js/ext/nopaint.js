var nopaint = (function(){
  
  controls.no = new Tool (nopaint_no_el)
  controls.no.use = function(state){
    undo.undo()
    controls.paint.focus()
  }
  controls.no.context = function(e){
    e.preventDefault()
    nopaint.turbo()
  }

  controls.paint = new Tool (nopaint_paint_el)
  controls.paint.use = function(state){
    nopaint.paint()
    nopaint_pause_el.classList.toggle("hidden", false)
    focused = controls.paint.lex
  }
  controls.paint.context = function(e){
    e.preventDefault()
    nopaint.autoplay()
  }
  
  controls.nopaint_pause = new Tool (nopaint_pause_el)
  controls.nopaint_pause.use = function(state){
    // nopaint.pause()
    nopaint.autoplay(false)
    nopaint_pause_el.classList.toggle("hidden", true)
    focused = canvas.aa[0][0]
  }
  
  // use own stepwise clock to drive tweens
  oktween.raf = function(){}  
  
  var nopaint = {}
  nopaint.debug = true
  nopaint.delay = nopaint.normal_delay = 100
  nopaint.turbo_delay = 0
  nopaint.tool = null
  nopaint.tools = {}
  nopaint.keys = []
  nopaint.weights = []
  nopaint.step = 0
  nopaint.time = 0
  nopaint.timeout = false
  nopaint.toggle = function(state){
    var state = typeof state == "boolean" ? state : nopaint_rapper.classList.contains("hidden")
    nopaint_rapper.classList.toggle("hidden", ! state)
    nopaint_pause_el.classList.toggle("hidden", true)
    document.body.classList.toggle("nopaint", state)
    return state
  }
  nopaint.no = function(){
    undo.undo()
    nopaint.paint()
  }
  nopaint.raw_key = controls.paint.lex.raw_key = keys.left_right_key(function(n){
    if (! nopaint.timeout) return
    if (n < 0) nopaint.no()
    else if (n > 0) nopaint.paint()
    else nopaint.pause()
  })
  nopaint.pause = nopaint.blur = function(){
    clearTimeout(nopaint.timeout)
    nopaint.timeout = 0
    nopaint.step = 0
  }
  nopaint.paint = function(){
    var state = undo.new()
    delete state.focus
    nopaint.pause()
    nopaint.switch_tool()
    nopaint.go()
  }
  nopaint.go = function(){
    nopaint.timeout = setTimeout(nopaint.go, nopaint.delay)
    oktween.update(nopaint.time)
    nopaint.tool.paint( nopaint.step )
    nopaint.time += 1
    nopaint.step += 1
  }
  nopaint.switch_tool = function(){
    last_tool = nopaint.tool
    last_tool && last_tool.finish()
    nopaint.tool = nopaint.get_random_tool( last_tool )
    nopaint.tool.start( last_tool )
    nopaint.debug && console.log("> %s", nopaint.tool.type)
  }
  nopaint.add_tool = function(fn){
    nopaint.tools[fn.type] = fn
  }
  nopaint.disable_all_tools = function(){
    Object.keys(nopaint.tools).forEach(function(key){
      nopaint.tools[key].disabled = true
    })
  }
  nopaint.enable_tools = function(keys){
    keys.forEach(function(key){
      if (nopaint.tools[key]) nopaint.tools[key].disabled = false
    })
  }
  nopaint.get_random_tool = function( last_tool ){
    var n = rand( nopaint.sum )
    for (var i = 0, _len = nopaint.weights.length; i < _len; i++) {
      if (n < nopaint.weights[i] && (! last_tool || nopaint.keys[i] !== last_tool.key)) {
        return nopaint.tools[ nopaint.keys[i] ]
      }
    }
    return nopaint.tools[ choice(nopaint.keys) ]
  }
  nopaint.regenerate_weights = function(){
    nopaint.sum = 0
    nopaint.weights = []
    nopaint.keys = Object.keys( nopaint.tools ).sort(function(a,b){
      return nopaint.tools[b].opt.weight-nopaint.tools[a].opt.weight
    }).filter(function(key){
      return ! nopaint.tools[key].disabled
    })
    nopaint.keys.forEach(function(key){
      nopaint.sum += nopaint.tools[key].opt.weight
      nopaint.weights.push( nopaint.sum )
    })
  }
  
  nopaint.is_turbo = false
  nopaint.turbo = function(state){
    nopaint.is_turbo = typeof state == "boolean" ? state : ! nopaint.is_turbo
    nopaint.delay = nopaint.is_turbo ? nopaint.turbo_delay : nopaint.normal_delay
    if (nopaint.is_turbo) {
      nopaint_no_el.classList.add("locked")
    }
    else {
      nopaint_no_el.classList.remove("locked")
    }
  }

  nopaint.is_autoplay = false  
  nopaint.autoplay = function(state){ 
    nopaint.is_autoplay = typeof state == "boolean" ? state : ! nopaint.is_autoplay
    if (nopaint.is_autoplay) {
      nopaint_paint_el.classList.add("locked")
      if (! nopaint.player) {
        nopaint.player = new RandomPlayer ()
      }
      if (! nopaint.timeout) nopaint.paint()
      nopaint.player.play()
    }
    else {
      nopaint_paint_el.classList.remove("locked")
      nopaint.pause()
      nopaint.player && nopaint.player.pause()
    }
  }
  
  var NopaintPlayer = Model({
    type: "player",
    upload_png: false,
    upload_interval: 100,
    step: 0,
    timeout: null,
    delay: function(){
      return nopaint.is_turbo ? randrange(150, 300) : randrange(400, 800)
    },
    reset: function(){
      this.no_count = 0
      this.paint_count = 0
    },
    pause: function(){
      clearTimeout(this.timeout)
      this.timeout = 0
    },
    play: function(){
      clearTimeout(this.timeout)
      var delay = this.delay()
      this.timeout = setTimeout(this.play.bind(this), delay)
      this.check_fitness()
      this.step += 1
    },
    check_fitness: function(){
      switch (this.fitness()) {
        case "no":
          nopaint.no_count += 1
          nopaint.since_last_no = 0
          nopaint.since_last_paint += 1
          nopaint.no()
          break
        case "paint":
          nopaint.paint_count += 1
          nopaint.since_last_no += 1
          nopaint.since_last_paint = 0
          nopaint.paint()
          break
        case "screenshot":
          if (this.save_as_png) break
          console.log("uploading...")
          setTimeout(clipboard.upload_png, 0)
          // fall thru
        default:
          nopaint.since_last_no += 1
          nopaint.since_last_paint += 1
          break
      }
    },
    fitness: function(){},
  })
  
  var RandomPlayer = NopaintPlayer.extend({
    type: "random_player",
    upload_png: false,
    fitness: function(){
      var no_prob = random()
      var paint_prob = 1 - no_prob 
      if (paint_prob < 0.3) {
        return "paint"
      }
      else if (no_prob < 0.5) {
        return "no"
      }
      else if ( this.paint_count > 100 && (this.step % 100) == 99 ) {
        return "screenshot"
      }
    }
  })

  var StylePlayer = NopaintPlayer.extend({
    type: "style_player",
    upload_png: false,
    fitness: function(){
      var no_prob = random()
      var paint_prob = 1 - no_prob
      var np, pp
      var steps = this.since_last_paint

      if (nopaint.tool.is_brush) {
        if (nopaint.tool.is_clone) {
          if (steps < randrange(3,8)) return
          np = 0.3
          pp = 0.4
        }
        else if (nopaint.tool.is_erase) {
          if (steps < randrange(2,6)) return
          np = 0.3
          pp = 0.4
        }
        else {
          if (steps < randrange(2,4)) return
          np = 0.1
          pp = 0.3
        }
      }
      if (nopaint.tool.is_shader) {
        switch (nopaint.tool.name) {
          case "rotate":
          case "scale":
            if (steps < randrange(2,4)) return
            np = 0.1
            pp = 0.2
            break
          default:
            np = 0.2
            pp = 0.2
        }
      }
      if (nopaint.tool.is_fill) {
        np = 0.4
        pp = 0.1
      }

      if (steps > 10) {
        np *= 0.7
        pp *= 1.5

        if (nopaint.is_turbo) {
          np *= 1.2
          pp *= 1.2
        }
      }

      if (paint_prob < np) {
        return "paint"
      }
      else if (no_prob < np) {
        return "no"
      }
      else if ( this.paint_count > 100 && (this.step % 100) == 99 ) {
        return "screenshot"
      }
    }
  })

  /* Base models for brushes */

  var NopaintTool = Model({
    type: "none",
    init: function(opt){
      this.opt = opt || {}
    },
    start: function(){},
    paint: function(t){},
    update: function(t){},
    finish: function(){},
  })
  
  var NopaintBrush = NopaintTool.extend({
    type: "brush",
    is_brush: true,
    init: function(opt){
      this.opt = opt || {}
      this.opt.max_radius = this.opt.max_radius || 10
      this.p = {x: randint(canvas.w), y: randint(canvas.h)}
      this.fg = 0
      this.bg = 1
      this.char = " "
      this.tweens = []
    },
    
    start: function(last_brush){
      this.set_brush_mask()
      this.toggle_channels()
      this.reset( last_brush )
      this.regenerate()
      draw.down({}, null, [this.p.x, this.p.y])
    },
    
    paint: function(t){
      this.update(t)
      draw.move_toroidal({}, null, [this.p.x, this.p.y])
    },
    
    finish: function(){
      this.tweens.forEach(function(t){ t.cancel() })
      this.tweens = []
    },
    
    reorient: function(last_brush){
      var a = {}, b
      
      if (last_brush) {
        this.p.x = a.x = randint(canvas.w)
        this.p.y = a.y = randint(canvas.h)
      }
      else {
        a.x = this.p.x
        a.y = this.p.y
      }

      b = this.get_next_point()

      var tween = oktween.add({
        obj: this.p,
        from: a,
        to: b,
        duration: b.duration,
        easing: b.easing,
        update: b.update,
        finished: function(){
          this.iterate()
          this.regenerate()
        }.bind(this)
      })
      this.tweens.push(tween)
    },

    get_next_point: function(){
      var radius = randrange(2, this.opt.max_radius)
      var b = {}
      b.duration = randrange(1, 7)
      b.easing = choice(easings)
      b.x = this.p.x + randrange(-radius, radius)
      b.y = this.p.y + randrange(-radius, radius)
      return b
    },
    
    set_brush_mask: function(){
      var r = Math.random()
      if (r < 0.2) {
        brush.mask = blit.square
      }
      else if (r < 0.6) {
        brush.mask = blit.circle
      }
      else if (r < 0.9) {
        brush.mask = blit.cross
      }
      else{
        brush.mask = blit.inverted_cross
      }
    },
    
    toggle_channels: function(){
      if (Math.random() < 0.001) { controls.bg.use(false) }
      else if (! brush.draw_bg && Math.random() < 0.25) { controls.bg.use(true) }

      if (Math.random() < 0.1) { controls.fg.use(false) }
      else if (! brush.draw_fg && Math.random() < 0.5) { controls.fg.use(true) }

      if (Math.random() < 0.02) { controls.char.use(false) }
      else if (! brush.draw_char && Math.random() < 0.2) { controls.char.use(true) }
    },

    iterate: function( last_brush ){
      this.reorient( last_brush )
    },

    regenerate: function(){
      brush.load( this )
      brush.generate()
    }
  })
  
  var easings = "linear circ_out circ_in circ_in_out quad_in quad_out quad_in_out".split(" ")
  
  /* Standard brushes */
  
  var SolidBrush = NopaintBrush.extend({
    type: "solid",
    
    recolor: function(){
      this.fg = this.bg = randint(16)
      this.char = " "
    },
    
    resize: function(m,n){
      m = m || 3
      n = n || 0
      var bw = xrandrange(5, 0, m) + n
      brush.resize( round(bw * randrange(0.9, 1.8)) || 1, round(bw) || 1 )
    },
    
    reset: function( last_brush ){
      this.opt.max_radius = randrange(5,20)
      this.resize()
      this.reorient( last_brush )
      this.recolor( last_brush )
      this.regenerate()
    },
    
    iterate: function( last_brush ){
      this.resize()
      this.reorient( last_brush )
    },
  })
  
  var EraseBrush = SolidBrush.extend({
    type: "erase",
    reset: function( last_brush ){
      this.opt.max_radius = randrange(8, 20)
      this.reorient( last_brush )
      this.bg = random() < 0.2 ? colors.white : colors.black
      this.char = " "
      brush.load( this )
      this.resize(3,2)
    },
  })

  var ShadowBrush = NopaintBrush.extend({
    type: "shadow",
    pairs: [
      [ colors.yellow, colors.orange ],
      [ colors.orange, colors.darkred ],
      [ colors.red, colors.darkred ],
      [ colors.lime, colors.green ],
      [ colors.cyan, colors.teal ],
      [ colors.cyan, colors.blue ],
      [ colors.blue, colors.darkblue ],
      [ colors.magenta, colors.purple ],
      [ colors.lightgray, colors.darkgray ],
      [ colors.darkgray, colors.black ],
      [ colors.white, colors.lightgray ],
      [ colors.white, colors.black ],
    ],
    shapes: [
      [[0],[1]],
      [[0,0],[1,1]],
      [[1,0,0],[1,1,1]],
      [[0,0,1],[1,1,1]],
      [[0,0,0],[1,1,1]],
      [[0,0,0,0],[1,1,1,1]],
      [[1,0,0,0],[null,1,1,1]],
      [[0,0,0,1],[1,1,1,null]],
      [[0,0],[1,0],[1,1]],
      [[0,0],[0,1],[1,1]],
    ],
    reset: function( last_brush ){
      var pair = choice(this.pairs)
      var shape = choice(this.shapes)
      this.reorient( last_brush )
      brush.char = " "
      brush.resize(shape[0].length, shape.length)
      brush.generate()
      brush.rebuild()
      brush.forEach(function(lex,x,y){
        if (shape[y][x] == null) {
          lex.opacity = 0
        }
        else {
          lex.fg = lex.bg = pair[ shape[y][x] ]
          lex.opacity = 1
        }
        lex.build()
      })
    },
    regenerate: function(){},
  })
  
  var RandomBrush = SolidBrush.extend({
    type: "random",
    iterate: function( last_brush ){
      this.reorient( last_brush )
      this.recolor( last_brush )
    },
  })
  
  var HueBrush = SolidBrush.extend({
    type: "hue",
    recolor: function(){
      this.fg = this.bg = rand_hue()
      this.char = " "
    },
  })

  var GrayBrush = SolidBrush.extend({
    type: "gray",
    recolor: function(){
      this.fg = this.bg = rand_gray()
      this.char = " "
    },
  })

  var LetterBrush = SolidBrush.extend({
    type: "letter",
    recolor: function(){
      this.fg = rand_hue()
      this.bg = rand_hue()
      this.char = choice( unicode.block(letters.charset, 32) )
    },
  })
  
  var RandomLetterBrush = LetterBrush.extend({
    type: "random-letter",
    iterate: function(){
      if (Math.random() < 0.01) {
        this.fg += 1
      }
      if (Math.random() < 0.05) {
        var n = this.fg
        this.fg = this.bg
        this.bg = n
      }
      if (Math.random() < 0.7) {
        this.char = choice( unicode.block(letters.charset, 32) )
      }
      this.regenerate()
      this.__iterate()
    },
    update: function(){
      if (Math.random() < 0.3) {
        this.char = choice( unicode.block(letters.charset, 32) )
      }
      this.regenerate()
    },
  })

  var CloneBrush = SolidBrush.extend({
    type: "clone",
    
    is_clone: true,
    
    reset: function( last_brush ){
      this.opt.max_radius = randrange(5, 20)
      this.reorient( last_brush )
      this.resize(4,2)
      this.clone_random_region()
    },
    
    clone_random_region: function(x, y){
      var x = randrange(0, canvas.w - brush.w)
      var y = randrange(0, canvas.h - brush.h)
      this.clone_region(x, y)
    },
    
    clone_region: function(x, y){
      blit.copy_toroidal_from(canvas, brush, round(x-brush.w/2), round(y-brush.h/2))
      brush.mask(brush)
    },

    iterate: function( last_brush ){
      this.reorient( last_brush )
    },
    
    regenerate: function(){},
  })
  
  var SmearBrush = CloneBrush.extend({
    type: "smear",
    
    update: function(){
      var r = random()
      var jitter_x = randnullsign() * xrand(2, 2)
      var jitter_y = randnullsign() * xrand(2, 2)
      this.clone_region( this.p.x + jitter_x, this.p.y + jitter_y )
    },

    iterate: function( last_brush ){
      this.resize(4, 2)
      this.update()
      this.reorient( last_brush )
    }
  })

  var StarsTool = NopaintBrush.extend({
    type: "stars",
    chars: "....,,'''*",

    start: function(last_brush){
      this.reorient( last_brush )
    },
    
    paint: function(t){
      if (Math.random() < 0.5) {
        var lex = canvas.get(this.p.x, this.p.y)
        undo.save_lex(lex.x, lex.y, lex)
        lex.fg = rand_hue()
        // lex.bg = colors.black
        lex.char = choice(this.chars)
        lex.build()
      }
    },
  })

  /* Fill tool */

  var FillTool = NopaintTool.extend({
    type: "fill",
    rate: 25,
    is_fill: true,
    start: function(){
      this.fill()
    },
    paint: function(t){
      if ((t % this.rate) == this.rate-1) {
        this.fill()
      }
    },
    recolor: function(){
      this.fg = this.bg = randint(16)
      this.char = " "
      this.opacity = 1
    },
    fill: function(){
      var x = randint(canvas.w)
      var y = randint(canvas.h)
      this.recolor()
      draw.fill(this, x, y)
    }
  })
  
  var FillLetterTool = FillTool.extend({
    type: "fill-letter",
    rate: 25,
    recolor: function(){
      this.fg = randint(16)
      this.bg = randint(16)
      this.char = choice( unicode.block(letters.charset, 32) )
      this.opacity = 1
    },
  })

  /* Shader Tools */
  
  var ShaderTool = NopaintTool.extend({
    type: "shader",
    speed: 3,
    is_shader: true,
    is_recursive: false,
    start: function(){
      undo.save_rect(0, 0, canvas.w, canvas.h)
      this.canvas = canvas.clone()
    },
    paint: function(t){
      if ((t % this.speed) == 0) {
        var w = canvas.w
        var h = canvas.h
        var lex
        if (this.is_recursive) {
          this.canvas.assign(canvas)
        }
        this.before_shade()
        for (var x = 0; x < w; x++) {
          for (var y = 0; y < h; y++) {
            lex = canvas.get(x, y)
            if (! this.shade( this.canvas, canvas, lex, x, y, w, h )) {
              lex.build()
            }
          }
        }
      }
    },
    before_shade: function(){},
    shade: function(src, dest, lex, x, y, w, h){},
    finish: function(){
      this.canvas.demolish()
    }
  })
  
  var ColorizeTool = ShaderTool.extend({
    type: "colorize",
    fns: [mirc_color_reverse,hue,inv_hue,gray,fire,red,yellow,green,blue,purple,dark_gray],
    speed: 5,
    start: function(){
      this.__start()
      this.i = randint(this.fns.length)
    },
    before_shade: function(){
      this.i = (this.i + 1) % this.fns.length
      this.fn = this.fns[this.i]
    },
    shade: function(src, dest, lex, x, y, w, h){
      lex.bg = this.fn( lex.bg )
      return false
    },
  })
  
  var TranslateTool = ShaderTool.extend({
    type: "translate",
    dx: 0,
    dy: 0,
    speed: 3,
    start: function(){
      this.__start()
      this.dx = randint(3)-1
      this.dy = randint(3)-1
      this.x = this.y = 0
      if (! this.dx && ! this.dy) {
        this.dx = 1
        this.dy = 0
      }
    },
    before_shade: function(){
      this.x += this.dx
      this.y += this.dy
    },
    shade: function(src, dest, lex, x, y, w, h){
      var copy = src.get(x+this.x, y+this.y)
      lex.assign(copy)
      return true
    },
  })

  var SliceTool = ShaderTool.extend({
    type: "slice",
    dx: 0,
    dy: 0,
    speed: 1,
    is_recursive: true,
    start: function(){
      this.__start()
      this.is_y = Math.random() > 0.3
      this.limit = this.is_y ? canvas.h : canvas.w
      this.position = randint(this.limit)
      this.direction = 1
    },
    before_shade: function(){
      if (Math.random() < 0.6) {
        this.position = mod(this.position + 1, this.limit)
      }
      if (Math.random() > 0.8) {
        this.direction = randsign()
      }
    },
    shade: function(src, dest, lex, x, y, w, h){
      if (this.is_y) {
        if (y >= this.position) {
          var copy = src.get(x + this.direction, y)
          lex.assign(copy)
        }
      }
      else if (x >= this.position) {
        var copy = src.get(x, y + this.direction)
        lex.assign(copy)
      }
      return true
    },
  })

  var ScaleTool = ShaderTool.extend({
    type: "scale",
    scale: 1,
    dscale: 0,
    speed: 3,
    start: function(){
      this.__start()
      var sign = randsign()
      this.x_scale = 1
      this.y_scale = 1
      this.dx_scale = randsign() * randrange(0.0005, 0.01)
      var r = Math.random()
      if (r < 0.333) {
        this.dy_scale = this.dx_scale * randrange(0.85, 1.25)
      }
      else if (r < 0.666) {
        this.dy_scale = this.dx_scale
      }
      else {
        this.dy_scale = randsign() * randrange(0.0005, 0.01)
      }
    },
    before_shade: function(){
      this.x_scale += this.dx_scale
      this.y_scale += this.dy_scale
    },
    shade: function(src, dest, lex, x, y, w, h){
      x = (x/w) * 2 - 1
      y = (y/h) * 2 - 1
      x *= this.x_scale
      y *= this.y_scale
      x = (x + 1) / 2 * w
      y = (y + 1) / 2 * h
      var copy = src.get(x, y)
      lex.assign(copy)
      return true
    },
  })

  var RotateTool = ShaderTool.extend({
    type: "rotate",
    theta: 0,
    d_theta: 0,
    
    start: function(){
      this.__start()
      var sign = randsign()
      this.theta = 0
      this.d_theta = randsign() * randrange(0.001, 0.05)
    },
    before_shade: function(){
      this.theta += this.d_theta
    },
    shade: function(src, dest, lex, x, y, w, h){
      x = (x/w) * 2 - 1
      y = (y/h) * 2 - 1
      var ca = cos(this.theta)
      var sa = sin(this.theta)
      var a = x * ca - y * sa
      var b = x * sa + y * ca
      x = (a + 1) / 2 * w
      y = (b + 1) / 2 * h
      var copy = src.get(x, y)
      lex.assign(copy)
      return true
    },
  })

  var CycleTool = ShaderTool.extend({
    type: "cycle",
    n: 0,
    speed: 5,
    is_recursive: true,
    start: function(){
      this.__start()
      this.n = randsign()
      if (random() < 0.2) this.n *= randint(15)
    },
    shade: function(src, dest, lex, x, y){
      lex.bg += this.n
      return false
    },
  })
  
  nopaint.add_tool( new SolidBrush({ weight: 5 }) )
  nopaint.add_tool( new ShadowBrush({ weight: 10 }) )
  nopaint.add_tool( new EraseBrush({ weight: 5 }) )
  nopaint.add_tool( new RandomBrush({ weight: 4 }) )
  nopaint.add_tool( new HueBrush({ weight: 5 }) )
  nopaint.add_tool( new GrayBrush({ weight: 5 }) )
  nopaint.add_tool( new LetterBrush({ weight: 2 }) )
  nopaint.add_tool( new RandomLetterBrush({ weight: 12 }) )
  nopaint.add_tool( new CloneBrush({ weight: 8 }) )
  nopaint.add_tool( new SmearBrush({ weight: 10 }) )
  nopaint.add_tool( new FillTool({ weight: 3 }) )
  nopaint.add_tool( new FillLetterTool({ weight: 6 }) )
  nopaint.add_tool( new StarsTool({ weight: 2 }) )
  nopaint.add_tool( new TranslateTool({ weight: 4 }) )
  nopaint.add_tool( new CycleTool({ weight: 1 }) )
  nopaint.add_tool( new ScaleTool({ weight: 3 }) )
  nopaint.add_tool( new RotateTool({ weight: 3 }) )
  nopaint.add_tool( new SliceTool({ weight: 4 }) )
  nopaint.add_tool( new ColorizeTool({ weight: 1 }) )
  nopaint.regenerate_weights()

  nopaint.toggle(true)

  nopaint.player = new StylePlayer ()

  return nopaint
})()
