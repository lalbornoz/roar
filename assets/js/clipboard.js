var clipboard = (function () {

  var exports = {
    format: "mirc",
    exporting: false,
    visible: false,
    canvas: document.createElement("canvas"),
    canvas_r: document.createElement("canvas"),

    bind: function () {
      export_textarea.addEventListener("focus", exports.export_focus)
      export_textarea.addEventListener("blur", exports.blur)
      import_button.addEventListener("click", exports.import_click)
      import_textarea.addEventListener("focus", exports.import_focus)
      import_textarea.addEventListener("paste", exports.paste)
    },
    setFormat: function (name) {
      return function () {
        clipboard.format = name
        if (! clipboard.exporting) { clipboard.export_data() }
      }
    },
    import_hide: function () { import_wrapper.style.display = "none"; clipboard.visible = false },
    import_show: function () { import_wrapper.style.display = "block"; clipboard.visible = true; },
    export_hide: function () { export_wrapper.style.display = "none"; clipboard.visible = false },
    export_show: function () { export_wrapper.style.display = "block"; clipboard.visible = true; changed = false },
    export_focus: function () {
      if (! clipboard.exporting) {
        export_textarea.focus()
        export_textarea.select()
      }
    },
    import_focus: function () {
      import_textarea.focus()
      import_textarea.select()
    },

    blur: function () {
    },

    export_mode: function () {
      exports.export_focus()
      clipboard.exporting = true
      export_cutoff_warning_el.style.display = "none"
      export_format_el.style.display = "inline"
      clipboard.export_data()
    },

    import_mode: function () {
      import_button.style.display = "inline"
      import_format_el.style.display = "inline"
      import_textarea.value = ""
      exports.import_focus()
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

    import_click: function (data, no_undo) {
      switch (controls.load_format.value) {
        case 'ansi':
          exports.import_ansi(data, no_undo)
          break
        case 'mirc':
          exports.import_mirc(data, no_undo)
          break
      }
    },

    import_ansi: function (data, no_undo) {
      if (data && data.preventDefault) {
        data = import_textarea.value
      } else {
        data = data || import_textarea.value
      }

      var to_json = function(string, opts){
        var lines_in = string.split(/\r?\n/)
        var lines_out = []
        var bg = 1, bg_ansi = 30, bold = false, fg = 15, fg_ansi = 37
        var w = 0, h = 0
        for (var y = 0; y < lines_in.length; y++) {
          var cells = [], line = lines_in[y]
          if (line.length === 0) {
            continue
          } else {
            for (var x = 0; x < line.length; x++) {
              var m = line.substring(x).match(/^\x1b\[((?:\d{1,3};?)+)m/)
              if (m !== null) {
                m[1].split(";").forEach(function(c){
                  c = parseInt(c);
                  if (c == 0) {
                    bg = 1; bg_ansi = 30; bold = false; fg = 15; fg_ansi = 37;
                  } else if (c == 1) {
                    bold = true; fg = ansi_fg_bold_import[fg_ansi];
                  } else if (c == 2) {
                    bold = false; fg = ansi_fg_import[fg_ansi];
                  } else if (ansi_bg_import[c] !== undefined) {
                    bg = ansi_bg_import[c]; bg_ansi = c;
                  } else if (bold && (ansi_fg_bold_import[c] !== undefined)) {
                    fg = ansi_fg_bold_import[c]; fg_ansi = c;
                  } else if (!bold && (ansi_fg_import[c] !== undefined)) {
                    fg = ansi_fg_import[c]; fg_ansi = c;
                  }
                });
                x += (m[0].length - 1);
              } else {
                m = line.substring(x).match(/^\x1b\[(\d+)C/)
                if (m !== null) {
                  for (var n = 0, nmax = parseInt(m[1]); n < nmax; n++) {
                    cells.push({bg: bg, fg: fg, value: " "})
                  }
                  x += (m[0].length - 1);
                } else {
                  cells.push({bg: bg, fg: fg, value: line[x]})
                }
              }
            }
            if (cells.length > 0) {
              if (w < cells.length) {
                w = cells.length
              } else if (w > cells.length) {
                for (var n = cells.length, nmax = w; n < nmax; n++) {
                  cells.push({bg: bg, fg: fg, value: " "})
                }
              }
              lines_out.push(cells); h++;
            }
          }
        }
        return {h: h, lines: lines_out, w: w}
      }
      var json = to_json(data, {fg:0, bg:1})

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
          lex.char = char.value
          lex.fg = char.fg
          lex.bg = char.bg
          lex.opacity = 1
          lex.build()
        }
      }

      current_filetool && current_filetool.blur()
    },

    import_mirc: function (data, no_undo) {
      if (data && data.preventDefault) {
        data = import_textarea.value
      } else {
        data = data || import_textarea.value
      }

      var to_json = function(string, opts){
        var lines_in = string.split(/\r?\n/)
        var lines_out = []
        var w = 0, h = 0
        for (var y = 0; y < lines_in.length; y++) {
          var bg = 1, fg = 15
          var cells = [], line = lines_in[y]
          if (line.length === 0) {
            continue
          } else {
            for (var x = 0; x < line.length; x++) {
              switch (line[x]) {
              case "\x02":  // ^B (unimplemented)
                break
              case "\x03":  // ^C
                var parseColour = function(line, x) {
                  if (/1[0-5]/.test(line.substr(x, 2))) {
                    colour = parseInt(line.substr(x, 2))
                    return [colour, x + 2]
                  } else if (/0[0-9]/.test(line.substr(x, 2))) {
                    colour = parseInt(line.substr(x, 2))
                    return [colour, x + 2]
                  } else if (/[0-9]/.test(line.substr(x, 1))) {
                    colour = parseInt(line.substr(x, 1))
                    return [colour, x + 1]
                  } else {
                    return [undefined, x]
                  }
                }
                var bg_ = undefined, fg_ = undefined, x_ = x + 1;
                [fg_, x_] = parseColour(line, x_)
                if (line[x_] === ",") {
                  [bg_, x_] = parseColour(line, x_ + 1)
                }
                if ((bg_ == undefined) && (fg_ == undefined)) {
                  [bg, fg] = [1, 15]
                } else {
                  bg = (bg_ != undefined) ? bg_ : bg;
                  fg = (fg_ != undefined) ? fg_ : fg;
                };
                if (x_ != x) {x = x_ - 1}; break;
              case "\x06":  // ^F (unimplemented)
                break
              case "\x0f":  // ^O
                [bg, fg] = [1, 15]; break;
              case "\x16":  // ^V
                [bg, fg] = [fg, bg]; break;
              case "\x1f":  // ^_ (unimplemented)
                break
              default:
                cells.push({bg: bg, fg: fg, value: line[x]})
              }
            }
            if (cells.length > 0) {
              if (w < cells.length) {
                w = cells.length
              }
              lines_out.push(cells); h++;
            }
          }
        }
        return {h: h, lines: lines_out, w: w}
      }
      var json = to_json(data, {fg:0, bg:1})

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
          lex.char = char.value
          lex.fg = char.fg
          lex.bg = char.bg
          lex.opacity = 1
          lex.build()
        }
      }

      current_filetool && current_filetool.blur()
    },

    export_data: function () {
      var output
      // switch (clipboard.format) {
      switch (controls.save_format.value) {
        case 'ascii':
          output = canvas.ascii()
          break
        case 'ansi':
          output = canvas.ansi()
          break
        case 'mirc':
          output = canvas.mirc({cutoff: 425})
          break
      }
      if (output.cutoff){
        export_cutoff_warning_el.style.display = 'block'
      } else {
        export_cutoff_warning_el.style.display = 'none'
      }
      export_textarea.value = output
      clipboard.export_focus()
      return output
    },

  }

  return exports

})()


