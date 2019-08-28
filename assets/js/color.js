
var fillColor = 1  // black

var color_names = ("white black dark-blue green red dark-red purple orange " +
                   "yellow lime teal cyan blue magenta dark-gray light-gray").split(" ");

var all_color_hue_order = "dark-red red orange yellow lime green teal cyan blue dark-blue purple magenta black dark-gray light-gray white".split(" ");
var all_color_inv_order = "cyan teal blue dark-blue purple magenta dark-red red orange yellow lime green white light-gray dark-gray black".split(" ");
var color_hue_order = "dark-red red orange yellow lime cyan teal blue dark-blue purple magenta".split(" ");
var color_inv_order = "cyan teal blue dark-blue purple magenta dark-red red orange yellow lime green".split(" ");
var gray_names = ("black dark-gray light-gray white").split(" ")

var fire_names = ("black dark-red red orange yellow white cyan").split(" ")
var red_names = ("black dark-red red").split(" ")
var yellow_names = ("black orange yellow white").split(" ")
var green_names = ("teal green lime").split(" ")
var blue_names = ("black dark-blue blue").split(" ")
var purple_names = ("dark-blue purple magenta red").split(" ")
var dark_gray_names = ("black dark-blue teal dark-gray light-gray white").split(" ")
var color_alphabet = "abcdefghijklmnop";
var colors = {}
color_names.forEach(function(name, i){
  colors[name.replace("-", "")] = i
  colors[name] = i
})
colors.brown = 5

function get_inverse (n) { return colors[all_color_inv_order.indexOf(color_names[n])] }

function mirc_color (n) { return mod(n, 16)|0 }
function mirc_color_reverse (n) { return mod(-(n+1), 16)|0 }
function all_hue (n) { return colors[all_color_hue_order[mod(n, 16)|0]] }
function all_inv_hue (n) { return colors[all_color_inv_order[mod(n, 16)|0]] }
function hue (n) { return colors[color_hue_order[mod(n, 11)|0]] }
function rand_hue () { return colors[color_hue_order[randint(11)]] }
function rand_gray () { return colors[gray_names[randint(4)]] }
function inv_hue (n) { return colors[color_inv_order[mod(n, 11)|0]] }
function gray (n) { return colors[gray_names[mod(n, 4)|0]] }
function fire (n) { return colors[fire_names[mod(n, 7)|0]] }
function red (n) { return colors[red_names[mod(n, 3)|0]] }
function yellow (n) { return colors[yellow_names[mod(n, 4)|0]] }
function green (n) { return colors[green_names[mod(n, 3)|0]] }
function blue (n) { return colors[blue_names[mod(n, 3)|0]] }
function purple (n) { return colors[purple_names[mod(n, 4)|0]] }
function dark_gray (n) { return colors[dark_gray_names[mod(n, 4)|0]] }

var css_lookup = {
  'rgb(255, 255, 255)': 'A',
  'rgb(0, 0, 0)': 'B',
  'rgb(0, 0, 127)': 'C',
  'rgb(0, 147, 0)': 'D',
  'red': 'E',
  'rgb(127, 0, 0)': 'F',
  'rgb(156, 0, 156)': 'G',
  'rgb(252, 127, 0)': 'H',
  'rgb(255, 255, 0)': 'I',
  'rgb(0, 252, 0)': 'J',
  'rgb(0, 147, 147)': 'K',
  'rgb(0, 255, 255)': 'L',
  'rgb(0, 0, 252)': 'M',
  'rgb(255, 0, 255)': 'N',
  'rgb(127, 127, 127)': 'O',
  'rgb(210, 210, 210)': 'P',
};
var css_reverse_lookup = {}
Object.keys(css_lookup).forEach(function(color){
  css_reverse_lookup[ css_lookup[color].charCodeAt(0) - 65 ] = color
})

var ansi_fg = [
  97,  // Bright White
  30,  // Black
  94,  // Blue
  32,  // Green
  91,  // Red
  31,  // Light Red
  35,  // Pink
  33,  // Yellow
  93,  // Light Yellow
  92,  // Light Green
  36,  // Cyan
  96,  // Light Cyan
  34,  // Light Blue
  95,  // Light Pink
  90,  // Grey
  37,  // Light Grey
]

var ansi_fg_import = {
  97: 0,  // Bright White
  30: 1,  // Black
  94: 2,  // Blue
  32: 3,  // Green
  91: 4,  // Red
  31: 5,  // Light Red
  35: 6,  // Pink
  33: 7,  // Yellow
  93: 8,  // Light Yellow
  92: 9,  // Light Green
  36: 10, // Cyan
  96: 11, // Light Cyan
  34: 12, // Light Blue
  95: 13, // Light Pink
  90: 14, // Grey
  37: 15, // Light Grey
}

var ansi_fg_bold_import = {
  97: 0,  // Bright White
  30: 14, // Grey
  94: 12, // Light Blue
  32: 9,  // Light Green
  91: 4,  // Light Red
  31: 4,  // Light Red
  35: 13, // Light Pink
  33: 8,  // Light Yellow
  93: 8,  // Light Yellow
  92: 9,  // Light Green
  36: 11, // Light Cyan
  96: 11, // Light Cyan
  34: 12, // Light Blue
  95: 13, // Light Pink
  90: 14, // Grey
  37: 0,  // Bright White
}

var ansi_bg = [
  107, // Bright White
  40,  // Black
  104, // Blue
  42,  // Green
  101, // Red
  41,  // Light Red
  45,  // Pink
  43,  // Yellow
  103, // Light Yellow
  102, // Light Green
  46,  // Cyan
  106, // Light Cyan
  44,  // Light Blue
  105, // Light Pink
  100, // Grey
  47,  // Light Grey
]

var ansi_bg_import = {
  107: 0,  // Bright White
  40:  1,  // Black
  104: 2,  // Blue
  42:  3,  // Green
  101: 4,  // Red
  41:  5,  // Light Red
  45:  6,  // Pink
  43:  7,  // Yellow
  103: 8,  // Light Yellow
  102: 9,  // Light Green
  46:  10, // Cyan
  106: 11, // Light Cyan
  44:  12, // Light Blue
  105: 13, // Light Pink
  100: 14, // Grey
  47:  15, // Light Grey
}
