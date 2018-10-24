var upload = (function(){
  var el = document.getElementById("upload_input")
  var button = document.getElementById("upload_button")
  var uploading = false
  
  function upload(blob, filename, tag, ascii){
    if (uploading) return
    filename = filename || get_filename()
    tag = tag || "shader"

    button.innerHTML = "uploading..."
    button.className = "uploading"
    
    uploading = true
    
    uploadImage({
      blob: blob,
      ascii: ascii,
      filename: filename,
      username: user.username,
      tag: tag,
      success: function(data){

        // data.url
        // data.filesize
        // data.success

        console.log(data);
        el.style.display = "block"
        el.value = data.url
        el.focus()
        setCaretToPos(el, 0)
        button.innerHTML = "upload"
        button.className = ""
        uploading = false
      },
      error: function(data){
        console.log(data)
        console.log("error uploading: " + data.error)
        button.innerHTML = "upload"
        button.className = ""
        uploading = false
      }
    });
  }

  function uploadImage(opt){
    if (! opt.blob || ! opt.filename) return;
  
    opt.username = opt.username || "";
    opt.success = opt.success || noop;
    opt.error = opt.error || noop;

    var form = new FormData();

    form.append("username", opt.username);
    form.append("filename", opt.filename);
    form.append("qqfile", opt.blob);
    form.append("tag", opt.tag);
    if (opt.ascii) {
      form.append("ascii", opt.ascii);      
    }

    var req = new XMLHttpRequest();
    req.open("POST", "/cgi-bin/im/shader/upload");
    req.onload = function(event) {
      if (req.status == 200) {
        var res = JSON.parse(req.responseText);
        if (res.success) {
          opt.success(res);
        }
        else {
          opt.error(res);
        }      
      } else {
        opt.error({ success: false, error: req.status });
      }
    };
    req.send(form);
  }
  
  return upload
})()
