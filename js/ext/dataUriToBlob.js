var dataUriToUint8Array = function(uri){
  var data = uri.split(',')[1];
  var bytes = atob(data);
  var buf = new ArrayBuffer(bytes.length);
  var u8 = new Uint8Array(buf);
  for (var i = 0; i < bytes.length; i++) {
    u8[i] = bytes.charCodeAt(i);
  }
  return u8 
}

window.dataUriToBlob = (function(){
/**
 * Blob constructor.
 */

var Blob = window.Blob;

/**
 * ArrayBufferView support.
 */

var hasArrayBufferView = new Blob([new Uint8Array(100)]).size == 100;

/**
 * Return a `Blob` for the given data `uri`.
 *
 * @param {String} uri
 * @return {Blob}
 * @api public
 */

var dataUriToBlob = function(uri){
  var data = uri.split(',')[1];
  var bytes = atob(data);
  var buf = new ArrayBuffer(bytes.length);
  var arr = new Uint8Array(buf);
  for (var i = 0; i < bytes.length; i++) {
    arr[i] = bytes.charCodeAt(i);
  }

  if (!hasArrayBufferView) arr = buf;
  var blob = new Blob([arr], { type: mime(uri) });
  blob.slice = blob.slice || blob.webkitSlice;
  return blob;
};

/**
 * Return data uri mime type.
 */

function mime(uri) {
  return uri.split(';')[0].slice(5);
}

return dataUriToBlob;

})()