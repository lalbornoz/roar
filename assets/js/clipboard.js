var clipboard = (function () {

  var exports = {
    format: "mirc",
    importing: false,
    visible: false,
    canvas: document.createElement("canvas"),
    canvas_r: document.createElement("canvas"),

    bind: function () {
      import_button.addEventListener("click", exports.import_colorcode)
      import_textarea.addEventListener("focus", exports.focus)
      import_textarea.addEventListener("blur", exports.blur)
      import_textarea.addEventListener('paste', exports.paste)
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
        case 'mirc':
          output = canvas.mirc({cutoff: 425})
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

  }

  return exports

})()


