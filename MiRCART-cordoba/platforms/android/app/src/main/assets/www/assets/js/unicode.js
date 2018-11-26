var unicode = (function(){
  var UNICODE_BLOCK_LIST = [
    0x0020, 0x007F, "Basic Latin",
    0x0080, 0x00FF, "Latin-1 Supplement",
    0x2500, 0x257F, "Box Drawing",
    0x2580, 0x259F, "Block Elements",
  ]
  var UNICODE_BLOCK_COUNT = UNICODE_BLOCK_LIST.length / 3
  var UNICODE_LOOKUP = {}
  for (var i = 0, len = UNICODE_BLOCK_LIST.length; i < len; i += 3) {
    UNICODE_LOOKUP[ UNICODE_BLOCK_LIST[i+2] ] = [ UNICODE_BLOCK_LIST[i], UNICODE_BLOCK_LIST[i+1] ]
  }

  function block (name, n){
    var b = UNICODE_LOOKUP[name]
    if (! b) return ""
    return range.apply(null, b).map(function(n){ return String.fromCharCode(n) })
  }
  function entities (a) {
    return a.map(function(k){ return "&#" + k.join(";&#") + ";" }).join("<br>")
  }
  function index (j) {
    return [ UNICODE_BLOCK_LIST[j*3], UNICODE_BLOCK_LIST[j*3+1], UNICODE_BLOCK_LIST[j*3+2], [] ]
  }
  function range(m,n){
    if (m > n) return []
    var a = new Array (n-m)
    for (var i = 0, j = m; j <= n; i++, j++) {
      a[i] = j
    }
    return a
  }

  // [ 0xE3, 0x81, 0x82, 0xE3, 0x81, 0x84 ] => '\xE3\x81\x82\xE3\x81\x84'
  // [ 0343, 0201, 0202, 0343, 0201, 0204 ] => '\343\201\202\343\201\204'
  function convertBytesToEscapedString(data_bytes, base) {
    var escaped = '';
    for (var i = 0; i < data_bytes.length; ++i) {
      var prefix = (base == 16 ? "\\x" : "\\");
      var num_digits = base == 16 ? 2 : 3;
      var escaped_byte = prefix + formatNumber(data_bytes[i], base, num_digits)
      escaped += escaped_byte;
    }
    return escaped;
  }
  // r'\xE3\x81\x82\xE3\x81\x84' => [ 0xE3, 0x81, 0x82, 0xE3, 0x81, 0x84 ]
  // r'\343\201\202\343\201\204' => [ 0343, 0201, 0202, 0343, 0201, 0204 ]
  function convertEscapedBytesToBytes(str) {
    var parts = str.split("\\x");
    parts.shift();  // Trim the first element.
    var codes = [];
    var max = Math.pow(2, 8);
    for (var i = 0; i < parts.length; ++i) {
      var code = parseInt(parts[i], 16);
      if (code >= 0 && code < max) {
        codes.push(code);
      } else {
        // Malformed code ignored.
      }
    }
    return codes;
  }
  // [ 0x3042, 0x3044 ] => "ã‚ã„"
  function convertUnicodeCodePointsToString(unicode_codes) {
    var utf16_codes = convertUnicodeCodePointsToUtf16Codes(unicode_codes);
    return convertUtf16CodesToString(utf16_codes);
  }
  // 0x3042 => [ 0xE3, 0x81, 0x82 ]
  function convertUnicodeCodePointToUtf8Bytes(unicode_code) {
    var utf8_bytes = [];
    if (unicode_code < 0x80) {  // 1-byte
      utf8_bytes.push(unicode_code);
    } else if (unicode_code < (1 << 11)) {  // 2-byte
      utf8_bytes.push((unicode_code >>> 6) | 0xC0);
      utf8_bytes.push((unicode_code & 0x3F) | 0x80);
    } else if (unicode_code < (1 << 16)) {  // 3-byte
      utf8_bytes.push((unicode_code >>> 12) | 0xE0);
      utf8_bytes.push(((unicode_code >> 6) & 0x3f) | 0x80);
      utf8_bytes.push((unicode_code & 0x3F) | 0x80);
    } else if (unicode_code < (1 << 21)) {  // 4-byte
      utf8_bytes.push((unicode_code >>> 18) | 0xF0);
      utf8_bytes.push(((unicode_code >> 12) & 0x3F) | 0x80);
      utf8_bytes.push(((unicode_code >> 6) & 0x3F) | 0x80);
      utf8_bytes.push((unicode_code & 0x3F) | 0x80);
    }
    return utf8_bytes;
  }
  // [ 0x3042, 0x3044 ] => [ 0x3042, 0x3044 ]
  // [ 0xD840, 0xDC0B ] => [ 0x2000B ]  // A surrogate pair.
  function convertUnicodeCodePointsToUtf16Codes(unicode_codes) {
    var utf16_codes = [];
    for (var i = 0; i < unicode_codes.length; ++i) {
      var unicode_code = unicode_codes[i];
      if (unicode_code < (1 << 16)) {
        utf16_codes.push(unicode_code);
      } else {
        var first = ((unicode_code - (1 << 16)) / (1 << 10)) + 0xD800;
        var second = (unicode_code % (1 << 10)) + 0xDC00;
        utf16_codes.push(first)
        utf16_codes.push(second)
      }
    }
    return utf16_codes;
  }
  // [ 0xE3, 0x81, 0x82, 0xE3, 0x81, 0x84 ] => [ 0x3042, 0x3044 ]
  function convertUtf8BytesToUnicodeCodePoints(utf8_bytes) {
    var unicode_codes = [];
    var unicode_code = 0;
    var num_followed = 0;
    for (var i = 0; i < utf8_bytes.length; ++i) {
      var utf8_byte = utf8_bytes[i];
      if (utf8_byte >= 0x100) {
        // Malformed utf8 byte ignored.
      } else if ((utf8_byte & 0xC0) == 0x80) {
        if (num_followed > 0) {
          unicode_code = (unicode_code << 6) | (utf8_byte & 0x3f);
          num_followed -= 1;
        } else {
          // Malformed UTF-8 sequence ignored.
        }
      } else {
        if (num_followed == 0) {
          unicode_codes.push(unicode_code);
        } else {
          // Malformed UTF-8 sequence ignored.
        }
        if (utf8_byte < 0x80){  // 1-byte
          unicode_code = utf8_byte;
          num_followed = 0;
        } else if ((utf8_byte & 0xE0) == 0xC0) {  // 2-byte
          unicode_code = utf8_byte & 0x1f;
          num_followed = 1;
        } else if ((utf8_byte & 0xF0) == 0xE0) {  // 3-byte
          unicode_code = utf8_byte & 0x0f;
          num_followed = 2;
        } else if ((utf8_byte & 0xF8) == 0xF0) {  // 4-byte
          unicode_code = utf8_byte & 0x07;
          num_followed = 3;
        } else {
          // Malformed UTF-8 sequence ignored.
        }
      }
    }
    if (num_followed == 0) {
      unicode_codes.push(unicode_code);
    } else {
      // Malformed UTF-8 sequence ignored.
    }
    unicode_codes.shift();  // Trim the first element.
    return unicode_codes;
  }
  // [ 0x3042, 0x3044 ] => "ã‚ã„"
  function convertUtf16CodesToString(utf16_codes) {
    var unescaped = '';
    for (var i = 0; i < utf16_codes.length; ++i) {
      unescaped += String.fromCharCode(utf16_codes[i]);
    }
    return unescaped;
  }
  // 0xff => "ff"
  // 0xff => "377"
  function formatNumber(number, base, num_digits) {
    var str = number.toString(base).toUpperCase();
    for (var i = str.length; i < num_digits; ++i) {
      str = "0" + str;
    }
    return str;
  }

  // encodes unicode characters as escaped bytes - \xFF
  // encodes ONLY non-ascii characters
  function escapeToEscapedBytes (txt) {
    var escaped_txt = "", kode, utf8_bytes
    for (var i = 0; i < txt.length; i++) {
      kode = txt.charCodeAt(i)
      if (kode > 0x7f) {
        utf8_bytes = convertUnicodeCodePointToUtf8Bytes(kode)
        escaped_txt += convertBytesToEscapedString(utf8_bytes, 16)
      }
      else {
        escaped_txt += txt[i]
      }
    }
    return escaped_txt
  }

  // convert \xFF\xFF\xFF to unicode
  function unescapeFromEscapedBytes (str) {
    var data_bytes = convertEscapedBytesToBytes(str);
    var unicode_codes = convertUtf8BytesToUnicodeCodePoints(data_bytes);
    return convertUnicodeCodePointsToString(unicode_codes);
  }

  return {
    raw: UNICODE_BLOCK_LIST,
    lookup: UNICODE_LOOKUP,
    index: index,
    range: range,
    block: block,
    escapeToEscapedBytes: escapeToEscapedBytes,
    unescapeFromEscapedBytes: unescapeFromEscapedBytes,
  }
})()
