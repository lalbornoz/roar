#!/usr/bin/env python3
#
# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#

from PIL import Image, ImageDraw, ImageFont
import os, string, yaml, sys

from ENNToolMiRCARTColours import ENNToolMiRCARTColours
from ENNToolMiRCARTImporter import ENNToolMiRCARTImporter

#
# Entry point
def main(*argv):
    fontNormalPathName = os.path.join("assets", "DejaVuSansMono.ttf")
    fontBoldPathName = os.path.join("assets", "DejaVuSansMono-Bold.ttf")
    fontSize = int("11")
    outInfoFileName = os.path.join("assets", "textures.yaml")
    outPathName = os.path.join("assets", "textures")
    if not os.path.exists(os.path.dirname(outInfoFileName)):
        os.makedirs(os.path.dirname(outInfoFileName))
    if not os.path.exists(outPathName):
        os.makedirs(outPathName)

    pilFontNormal = ImageFont.truetype(fontNormalPathName, fontSize)
    pilFontBold = ImageFont.truetype(fontBoldPathName, fontSize)
    pilFontSize = list(pilFontNormal.getsize(" "))
    pilFontSize[0] += (8 - (pilFontSize[0] % 8))
    pilFontSize[1] = pilFontSize[0] * 2
    pilImageSize = (pilFontSize[0] * 128, pilFontSize[1])
    print("font size: {}, image size: {}".format(pilFontSize, pilImageSize))

    charMap = {}
    for fontAttrs in [[ENNToolMiRCARTImporter._CellState.CS_NONE],
                      [ENNToolMiRCARTImporter._CellState.CS_BOLD],
                      [ENNToolMiRCARTImporter._CellState.CS_UNDERLINE],
                      [ENNToolMiRCARTImporter._CellState.CS_BOLD, ENNToolMiRCARTImporter._CellState.CS_UNDERLINE]]:
        for fontColour in range(16):
            curPos = [0, 0]
            pilImage = Image.new("RGBA", pilImageSize, (0, 0, 0, 0))
            pilImageDraw = ImageDraw.Draw(pilImage)
            for fontChar in [chr(n) for n in range(128)]:
                pilFont, underLine = None, False
                for fontAttr in fontAttrs:
                    if fontAttr == ENNToolMiRCARTImporter._CellState.CS_NONE:
                        pilFont = pilFontNormal
                    elif fontAttr == ENNToolMiRCARTImporter._CellState.CS_BOLD:
                        pilFont = pilFontBold
                    elif fontAttr == ENNToolMiRCARTImporter._CellState.CS_UNDERLINE:
                        underLine = True
                    else:
                        raise ValueError
                if fontChar in string.printable:
                    pilImageDraw.text(curPos, fontChar,
                                      (*ENNToolMiRCARTColours[fontColour], 255), pilFont)
                    if underLine:
                        pilImageDraw.line(
                            xy=(curPos[0], curPos[1] + (pilFontSize[1] - 2),
                                curPos[0] + pilFontSize[0], curPos[1] + (pilFontSize[1] - 2)),
                            fill=(*ENNToolMiRCARTColours[fontColour], 255))
                    if not fontChar in charMap:
                        charMap[fontChar] = {}
                    if not fontColour in charMap[fontChar]:
                        charMap[fontChar][fontColour] = []
                    charMap[fontChar][fontColour]   \
                        += [{"attrs":fontAttrs,
                             "bl":[float((curPos[0])/pilImageSize[0]), float((curPos[1])/pilImageSize[1])],
                             "br":[float((curPos[0] + pilFontSize[0])/pilImageSize[0]), float((curPos[1])/pilImageSize[1])],
                             "tl":[float((curPos[0])/pilImageSize[0]), float((curPos[1] + pilFontSize[1])/pilImageSize[1])],
                             "tr":[float((curPos[0] + pilFontSize[0])/pilImageSize[0]), float((curPos[1] + pilFontSize[1])/pilImageSize[1])]}]
                curPos[0] += pilFontSize[0]
            fontAttrName = ""
            for fontAttr in fontAttrs:
                if fontAttr == ENNToolMiRCARTImporter._CellState.CS_NONE:
                    fontAttrName += "Normal"
                elif fontAttr == ENNToolMiRCARTImporter._CellState.CS_BOLD:
                    fontAttrName += "Bold"
                elif fontAttr == ENNToolMiRCARTImporter._CellState.CS_UNDERLINE:
                    fontAttrName += "Underline"
                else:
                    raise ValueError
            pilImage.save(os.path.join(outPathName, "{}Fg{:02d}.png".format(fontAttrName, fontColour)))

    with open(outInfoFileName, "w") as fileObject:
        yaml.dump(charMap, fileObject)

if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
