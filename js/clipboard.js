var clipboard = (function () {

  var exports = {
    format: "irssi",
    importing: false,
    visible: false,
    canvas: document.createElement("canvas"),
    canvas_r: document.createElement("canvas"),

    bind: function () {
//      import_ascii.addEventListener("change", exports.setFormat("ascii"))
//      import_irssi.addEventListener("change", exports.setFormat("irssi"))
//      import_mirc.addEventListener("change", exports.setFormat("mirc"))
      import_button.addEventListener("click", exports.import_colorcode)
      export_button.addEventListener("click", exports.export_data)
      save_button.addEventListener("click", exports.save_png)
      upload_button.addEventListener("click", exports.upload_png)
      import_textarea.addEventListener("focus", exports.focus)
      import_textarea.addEventListener("blur", exports.blur)
      import_textarea.addEventListener('paste', exports.paste)
//      import_irssi.setAttribute("checked", true)
    },
    setFormat: function (name) {
      return function () {
        clipboard.format = name
        if (! clipboard.importing) { clipboard.export_data() }
      }
    },
    show: function () { import_rapper.style.display = "block"; clipboard.visible = true; changed = false },
    hide: function () { import_rapper.style.display = "none"; clipboard.visible = false },
    focus: function () {
      if (! clipboard.importing) {
        import_textarea.focus()
        import_textarea.select()
      }
    },
    blur: function () {
    },

    import_mode: function () {
      focus()
      clipboard.importing = true
      gallery_rapper.style.display = 'none'
      format_el.style.display = 'none'
      cutoff_warning_el.style.display = 'none'
      import_buttons.style.display = "inline"
      import_textarea.value = ""
    },
    export_mode: function () {
      focus()
      clipboard.importing = false
      import_buttons.style.display = "none"
      format_el.style.display = 'inline'
      cutoff_warning_el.style.display = 'none'
      gallery_rapper.style.display = 'inline'
      clipboard.export_data()
    },

    paste: function (e) {
      e.preventDefault()
      // images will come through as files
      var types = toArray(e.clipboardData.types)
      import_textarea.value = ""
      types.forEach(function(type, i){
        console.log(type)
        // this can be text/plain or text/html..
        if (type.match('text/plain')) {
          import_textarea.value = e.clipboardData.getData(type)
        }
        else {
          console.error("unknown type!", item.type)
        }
      })
    },
    
    import_colorcode: function (data, no_undo) {
    	if (data && data.preventDefault) {
				data = import_textarea.value
    	}
    	else {
				data = data || import_textarea.value
    	}
      
      var irssi_style_regex = /^\s*\/exec -out printf ("%b" )?"/;

      // turn irssi style into mirc style
      if (data.match(irssi_style_regex)){
        data = data.replace(/\\x03/gm, '\x03')
                   .replace(/(\\x..)+/gm, unicode.unescapeFromEscapedBytes)
                   .replace(/\\x5C/g, '\\')
                   .replace(/\\n/gm, '\n')
                   .replace(/\\`/gm, '`')
                   .replace(/\\"/gm, '"')
                   .replace(/\\\$/gm, '$')
                   .replace(irssi_style_regex, '')
                   .replace(/"\s*$/, '')
      }

      // not a colorcode
      if (!data.match(/\x03/))
        return exports.import_text();

      var json = colorcode.to_json(data, {fg:0, bg:1})

      if (!no_undo) undo.new()
      if (!no_undo) undo.save_rect(0,0, canvas.w, canvas.h)
      if (json.w !== canvas.w || json.h !== canvas.h){
        if (!no_undo) undo.save_size(canvas.w, canvas.h)
        canvas.resize(json.w, json.h, true)
      }
      canvas.clear()

      for (var y = 0, line; line = json.lines[y]; y++){
        var row = canvas.aa[y]
        for (var x = 0, char; char = line[x]; x++){
          var lex = row[x]
          lex.char = String.fromCharCode(char.value)
          lex.fg = char.fg
          lex.bg = char.bg
          lex.opacity = 1
          lex.build()
        }
      }

      current_filetool && current_filetool.blur()     
    },
    
    import_text: function () {
      var data = import_textarea.value
      var lines = data.split("\n")
      var width = lines.reduce(function(a,b){ console.log(a,b); return Math.max(a, b.length) }, 0)
      var height = lines.length
      if (width > canvas.max) {
        return alert("input too wide")
      }
      if (height > canvas.max) {
        return alert("input too tall")
      }
      undo.new()
      undo.save_rect(0,0, canvas.w, canvas.h)
      canvas.clear()
      lines.forEach(function(line, y){
        var row = canvas.aa[y]
        if (! row) return
        for (var x = 0; x < line.length; x++) {
          var lex = row[x]
          if (! lex) return
          lex.char = line[x]
          lex.fg = brush.bg
          lex.opacity = 1
          lex.build()
        }
      })
      // TODO: some notion of a "selected" region which cuts/clones the underlying region
      
//       var pasted_region = new Matrix (width, height, function(x,y){
//         var lex = new Lex (x,y)
//         lex.char = lines[y][x] || " "
//         lex.build()
//         return lex
//       })
    },
    export_data: function () {
      var output
      // switch (clipboard.format) {
      switch (controls.save_format.value) {
        case 'ascii':
          output = canvas.ascii()
          break
        case 'mirc':
          output = canvas.mirc({cutoff: 400})
          break
        case 'irssi':
          output = canvas.irssi({cutoff: 400})
          break
        case 'ansi':
          output = canvas.ansi()
          break
      }
      if (output.cutoff){
        cutoff_warning_el.style.display = 'block'
      } else {
        cutoff_warning_el.style.display = 'none'
      }
      import_textarea.value = output
      clipboard.focus()
      return output
    },
    
    rotate_canvas: function(){
      var cr = clipboard.canvas_r, c = clipboard.canvas
      cr.width = c.height
      cr.height = c.width
      var ctx = cr.getContext('2d')
      ctx.resetTransform()
      ctx.translate(0, cr.height)
      ctx.rotate(-Math.PI / 2)
      ctx.drawImage(c, 0, 0)
      return cr
    },

    export_canvas: function (done_fn) {
      var opts = {
        palette: 'mirc',
        font: canvas.pixels ? 'fixedsys_8x8' : 'fixedsys_8x15',
        fg: 0,
        bg: 1,
        canvas: clipboard.canvas
      }
      opts.done = function(){
        var c = canvas.rotated ? clipboard.rotate_canvas() : clipboard.canvas
        if (done_fn) done_fn(c)
      }

      var start = Date.now();
      colorcode.to_canvas(canvas.mirc(), opts)
      var total = Date.now() - start;
      console.log("took " + total)
    },
    
    filename: function () {
      return [ +new Date, "ascii", user.username ].join("-")
    },

    save_png: function () {
      var save_fn = function(canvas_out){
        var filename = clipboard.filename() + ".png"
        var blob = PNG.canvas_to_blob_with_colorcode(canvas_out, canvas.mirc())
        saveAs(blob, filename);
      }
      clipboard.export_canvas(save_fn)
    },
    
    upload_png: function () {
      var upload_fn = function(canvas_out){
        var blob = PNG.canvas_to_blob_with_colorcode(canvas_out, canvas.mirc())
        var filename = clipboard.filename()
        var tag = 'ascii'
        upload(blob, filename, tag, canvas.mirc())
      }
      clipboard.export_canvas(upload_fn)
    }

  }
 
  // http...?a=1&b=2&b=3 -> {a: '1', b: ['2', '3']}
  function parse_url_search_params(url){
    var params = {}
    url = url.split('?')
    if (url.length < 2) return params

    var search = url[1].split('&')
    for (var i = 0, pair; pair = search[i]; i++){
      pair = pair.split('=')
      if (pair.length < 2) continue
      var key = pair[0]
      var val = pair[1]
      if (key in params){
        if (typeof params[key] === 'string'){
          params[key] = [params[key], val]
        }
        else params[key].push(val)
      }
      else params[key] = val
    }
    return params
  }

  function get_filetype(txt){
    txt = txt.split('.')
    return txt[txt.length - 1].toLowerCase() 
  }

  function fetch_url(url, f, type){
    type = type || 'arraybuffer'
    url = "/cgi-bin/proxy?" + url
    //url = "http://198.199.72.134/cors/" + url
    var xhr = new XMLHttpRequest()
    xhr.open('GET', url, true)
    xhr.responseType = type
    xhr.addEventListener('load', function(){ f(xhr.response) })
    xhr.send()
  }

  function load_text(txt){
    clipboard.import_colorcode(txt, true)
  }

  function load_png(buf){
    var chunks = PNG.decode(buf)
    if (!chunks) return
    var itxt_chunks = []
    for (var i=0, c; c=chunks[i]; i++){
      if (c.type !== 'iTXt') continue
      var itxt = PNG.decode_itxt_chunk(c)
      if (!itxt.keyword || itxt.keyword !== 'colorcode') continue
      clipboard.import_colorcode(itxt.data, true)
    }
  }
  
  function sally_url_convert(url){
    var png_regex = /^https?:\/\/jollo\.org\/den\/sallies\/([0-9]+)\/([^.]+)\.png$/
    var matches = url.match(png_regex)
    if (!matches) return url
    return 'http://jollo.org/den/sallies/' + matches[1] + '/raw-' + matches[2] + '?.txt'
    // txt suffix to force asdf proxy
  }

  exports.load_from_location = function(){
    var params = parse_url_search_params(window.location + '')
    if (!params.url) return
    var url = params.url
    url = sally_url_convert(url)
    var type = get_filetype(url)
    switch (type){
      case 'txt':
        fetch_url(url, load_text, 'text')
        break
      case 'png':
        fetch_url(url, load_png)
        break
    } 

  }
  
  return exports
  
})()


