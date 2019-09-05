#!/usr/bin/env python3
#
# Colours.py -- XXX
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

# {{{ AnsiBgToMiRCARTColours: XXX
AnsiBgToMiRCARTColours = {
    107: 0,  # Bright White
    40:  1,  # Black
    104: 2,  # Blue
    42:  3,  # Green
    101: 4,  # Red
    41:  5,  # Light Red
    45:  6,  # Pink
    43:  7,  # Yellow
    103: 8,  # Light Yellow
    102: 9,  # Light Green
    46:  10, # Cyan
    106: 11, # Light Cyan
    44:  12, # Light Blue
    105: 13, # Light Pink
    100: 14, # Grey
    47:  15, # Light Grey
};
# }}}
# {{{ AnsiFgBoldToMiRCARTColours: XXX
AnsiFgBoldToMiRCARTColours = {
    97: 0,   # Bright White
    30: 14,  # Grey
    94: 12,  # Light Blue
    32: 9,   # Light Green
    91: 4,   # Light Red
    31: 4,   # Light Red
    35: 13,  # Light Pink
    33: 8,   # Light Yellow
    93: 8,   # Light Yellow
    92: 9,   # Light Green
    36: 11,  # Light Cyan
    96: 11,  # Light Cyan
    34: 12,  # Light Blue
    95: 13,  # Light Pink
    90: 14,  # Grey
    37: 0,   # Bright White
};
# }}}
# {{{ AnsiFgToMiRCARTColours: XXX
AnsiFgToMiRCARTColours = {
    97: 0,   # Bright White
    30: 1,   # Black
    94: 2,   # Blue
    32: 3,   # Green
    91: 4,   # Red
    31: 5,   # Light Red
    35: 6,   # Pink
    33: 7,   # Yellow
    93: 8,   # Light Yellow
    92: 9,   # Light Green
    36: 10,  # Cyan
    96: 11,  # Light Cyan
    34: 12,  # Light Blue
    95: 13,  # Light Pink
    90: 14,  # Grey
    37: 15,  # Light Grey
};
# }}}
# {{{ ColourMapBold: mIRC colour number to RGBA map given ^B (bold)
ColourMapBold = [
    [255, 255, 255],    # Bright White
    [85,  85,  85],     # Black
    [85,  85,  255],    # Light Blue
    [85,  255, 85],     # Green
    [255, 85,  85],     # Red
    [255, 85,  85],     # Light Red
    [255, 85,  255],    # Pink
    [255, 255, 85],     # Yellow
    [255, 255, 85],     # Light Yellow
    [85,  255, 85],     # Light Green
    [85,  255, 255],    # Cyan
    [85,  255, 255],    # Light Cyan
    [85,  85,  255],    # Blue
    [255, 85,  255],    # Light Pink
    [85,  85,  85],     # Grey
    [255, 255, 255],    # Light Grey
]
# }}}
# {{{ ColourMapNormal: mIRC colour number to RGBA map given none of ^[BFV_] (bold, italic, reverse, underline)
ColourMapNormal = [
    [255, 255, 255],    # Bright White
    [0,   0,   0],      # Black
    [0,   0,   187],    # Light Blue
    [0,   187, 0],      # Green
    [255, 85,  85],     # Red
    [187, 0,   0],      # Light Red
    [187, 0,   187],    # Pink
    [187, 187, 0],      # Yellow
    [255, 255, 85],     # Light Yellow
    [85,  255, 85],     # Light Green
    [0,   187, 187],    # Cyan
    [85,  255, 255],    # Light Cyan
    [85,  85,  255],    # Blue
    [255, 85,  255],    # Light Pink
    [85,  85,  85],     # Grey
    [187, 187, 187],    # Light Grey
]
# }}}
# {{{ Colours: mIRC colour number to RGBA map given none of ^[BFV_] (bold, italic, reverse, underline],
Colours = [
    [255, 255, 255, 255, "White"],
    [0,   0,   0,   255, "Black"],
    [0,   0,   187, 255, "Blue"],
    [0,   187, 0,   255, "Green"],
    [255, 85,  85,  255, "Light Red"],
    [187, 0,   0,   255, "Red"],
    [187, 0,   187, 255, "Purple"],
    [187, 187, 0,   255, "Yellow"],
    [255, 255, 85,  255, "Light Yellow"],
    [85,  255, 85,  255, "Light Green"],
    [0,   187, 187, 255, "Cyan"],
    [85,  255, 255, 255, "Light Cyan"],
    [85,  85,  255, 255, "Light Blue"],
    [255, 85,  255, 255, "Pink"],
    [85,  85,  85,  255, "Grey"],
    [187, 187, 187, 255, "Light Grey"],
];
# }}}
# {{{ MiRCARTToAnsiColours: XXX
MiRCARTToAnsiColours = [
    97,  # Bright White 
    30,  # Black        
    94,  # Light Blue   
    32,  # Green        
    91,  # Red          
    31,  # Light Red    
    35,  # Pink         
    33,  # Yellow       
    93,  # Light Yellow 
    92,  # Light Green  
    36,  # Cyan         
    96,  # Light Cyan   
    34,  # Blue         
    95,  # Light Pink   
    90,  # Grey         
    37,  # Light Grey   
];
# }}}

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
