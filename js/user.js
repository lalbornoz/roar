var user = (function(){

  var user = {}
  var el = document.getElementById("username_input")

  user.init = function(){
    user.load()
    user.bind()
  }
  user.bind = function(){
    el.addEventListener("input", user.save)
  }
  user.load = function(){
    user.username = user.getCookie()
    if (! user.username) {
      user.username = '00' + randint(9876876)
      user.setCookie(user.username)
    }
    if (!user.username.match(/^00/)) {
      el.value = user.username
    }
  }
  user.prefs = new function(){}
  user.prefs.get = function (key){
    return localStorage.getItem("im.prefs." + key)
  }
  user.prefs.set = function (key,value){
    return localStorage.setItem("im.prefs." + key, value)
  }
  user.sanitize = function(){
    return el.value.replace(/[^-_ a-zA-Z0-9]/g,"")
  }
  user.getCookie = function () {
    var username = localStorage.getItem("im.name") || "";
    if (document.cookie && ! username.length) {
      var cookies = document.cookie.split(";")
      for (i in cookies) {
        var cookie = cookies[i].split("=")
        if (cookie[0].indexOf("imname") !== -1) {
          if (cookie[1] !== 'false' && cookie[1] !== 'undefined' && cookie[1].length) {
            return cookie[1]
          }
        }
      }
    }
    return username
  }
  var timeout
  user.save = function(){
    clearTimeout(timeout)
    timeout = setTimeout(function(){
      var username = user.sanitize()
      if (username != user.username) user.setCookie(username);
    })
  }
  user.setCookie = function(username){
    if (!user.username.match(/^00/)) {
      console.log("setting to " + username)
    }
    document.cookie = "imname="+username+";path=/;domain=.asdf.us;max-age=1086400"
    localStorage.setItem("im.name", username);
  }
  
  user.init()
  
  return user
})()
