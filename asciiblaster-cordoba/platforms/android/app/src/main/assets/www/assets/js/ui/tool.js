var Tool = Model({
  init: function (el) {
    this.el = el
    this.lex = new Lex (el)
    this.name = el.innerHTML
  },
  bind: function(){
    var tool = this
    tool.el.addEventListener('mousedown', function(e){
      tool.focus()
    })
    tool.el.addEventListener('contextmenu', function(e){
      tool.context(e)
    })
    if (tool.memorable) {
      // console.log(tool.name, localStorage.getItem("ascii.tools." + tool.name) )
      tool.use( localStorage.getItem("ascii.tools." + tool.name) == "true" )
    }
  },
  use: function(){},
  context: function(e){},
  done: function(){},
  focus: function(){
    // focused && focused.blur()
    current_tool && current_tool.blur()
    current_tool = this
    this.el.classList.add('focused')
    this.use()
    cursor_input.focus()
  },
  blur: function(){
    current_tool = null
    this.el.classList.remove('focused')
    this.done()
  }
})

var FileTool = Tool.extend({
  focus: function(){
    if (current_filetool === this) {
      this.blur()
      return
    }
    current_filetool && current_filetool.blur()
    current_filetool = this
    this.el.classList.add('focused')
    this.use()
    cursor_input.focus()
  },
  blur: function(){
    current_filetool = null
    this.el.classList.remove('focused')
    this.done()
  }
})

var RadioItem = Tool.extend({
  init: function(group, el){
    this.group = group
    this.el = el
  },
  focus: function(){
    this.el.classList.add('focused')
  },
  blur: function(){
    this.el.classList.remove('focused')
  },
  bind: function(){
    var control = this
    this.el.addEventListener('mousedown', function(){
      control.group.use(control)
    })
  }
})

var RadioGroup = Tool.extend({
  init: function(el){
    this.el = el
    this.controls = {}
    var names = el.innerHTML.split(' ')
    el.innerHTML = ''
    var group = this
    names.forEach(function(value){
      var el = document.createElement('span')
      el.classList.add('radio','tool')
      var control = new RadioItem(group, el)
      if (value.substr(0,1) === '*') {
        control.value = value = value.substr(1)
        group.use(control)
      }
      control.value = el.innerHTML = value
      group.controls[value] = control
      group.el.appendChild(el)
    })
  },
  use: function(control){
    if (typeof control === 'string') {
      control = this.controls[control]
    }
    this.selected_control && this.selected_control.blur()
    this.value = control.value
    this.selected_control = control
    control.focus()
    control.use()
    if (this.memorable){
      localStorage.setItem("ascii.tools." + this.name, this.value)
    }
  },
  bind: function(){
    var tool = this
    for (var n in this.controls){
      this.controls[n].bind()
    }
    if (tool.memorable) {
      var value = localStorage.getItem("ascii.tools." + tool.name)
      if (value) tool.use(value)
    }
  }
})

var Checkbox = Tool.extend({
  init: function (el){
    this.__init(el)
    var name = this.name.replace(/^[x_] /,"")
    var state = localStorage.getItem("ascii.tools." + name) == "true" || this.name[0] == "x"
    this.name = name
    this.update(state)
  },
  update: function(state){
    if (state) this.el.innerHTML = "x " + this.name
    else       this.el.innerHTML = "_ " + this.name
    if (this.memorable) { localStorage.setItem("ascii.tools." + this.name, !! state) }
  }
})

var BlurredCheckbox = Checkbox.extend({
  focus: function(){
    this.use()
  },
  blur: function(){
    this.el.classList.remove('focused')
    this.done()
  }
})

var BlurredTool = Tool.extend({
  focus: function(){
    this.use()
  },
  blur: function(){
    this.el.classList.remove('focused')
    this.done()
  }
})

var HiddenCheckbox = BlurredCheckbox.extend({
  on: "o",
  off: ".",
  init: function (el){
    this.el = el
    this.lex = new Lex (el)
    this.name = this.el.id
    var state = localStorage.getItem("ascii.tools." + name) == "true" || this.el.innerHTML[0] == this.on
    this.update(state)
  },
  update: function(state){
    this.el.innerHTML = state ? this.on : this.off
    if (this.memorable) { localStorage.setItem("ascii.tools." + this.name, !! state) }
  }
})
