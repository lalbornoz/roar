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
    fontSize = int("26")
    outInfoFileName = os.path.join("assets", "textures.yaml")
    outFileName = os.path.join("assets", "DejaVuSansMono.png")
    if not os.path.exists(os.path.dirname(outInfoFileName)):
        os.makedirs(os.path.dirname(outInfoFileName))
    if not os.path.exists(os.path.dirname(outFileName)):
        os.makedirs(os.path.dirname(outFileName))

    pilFontNormal = ImageFont.truetype(fontNormalPathName, fontSize)
    pilFontBold = ImageFont.truetype(fontBoldPathName, fontSize)
    pilFontSize = list(pilFontNormal.getsize(" "))
    pilFontSize[0] += (8 - (pilFontSize[0] % 8))
    pilFontSize[1] = pilFontSize[0] * 2
    pilImageSize = (pilFontSize[0] * 128, (pilFontSize[1] * 16 * 4))
    print("font size: {}, image size: {}".format(pilFontSize, pilImageSize))

    curPos = [0, 0]
    pilImage = Image.new("RGBA", pilImageSize, (0, 0, 0, 0))
    pilImageDraw = ImageDraw.Draw(pilImage)

    pilImageTmp = Image.new("RGBA", pilFontSize, (0, 0, 0, 0))
    pilImageTmpDraw = ImageDraw.Draw(pilImageTmp)

    for fontAttr in [ENNToolMiRCARTImporter._CellState.CS_BOLD | ENNToolMiRCARTImporter._CellState.CS_UNDERLINE,
                     ENNToolMiRCARTImporter._CellState.CS_UNDERLINE,
                     ENNToolMiRCARTImporter._CellState.CS_BOLD,
                     ENNToolMiRCARTImporter._CellState.CS_NONE]:
        for fontColour in reversed(range(16)):
            for fontChar in [chr(n) for n in range(128)]:
                pilFont, underLine = pilFontNormal, False
                if fontAttr & ENNToolMiRCARTImporter._CellState.CS_BOLD:
                    pilFont = pilFontBold
                if fontAttr & ENNToolMiRCARTImporter._CellState.CS_UNDERLINE:
                    underLine = True
                if fontChar in string.printable:
                    pilImageTmpDraw.text((0, 0), fontChar,
                                      (*ENNToolMiRCARTColours[fontColour], 255), pilFont)
                    pilImage.paste(pilImageTmp, tuple(curPos))
                    pilImageTmpDraw.rectangle((0, 0, pilFontSize[0], pilFontSize[1]),
                                              fill=(0, 0, 0, 0))
                    if underLine:
                        pilImageDraw.line(
                            xy=(curPos[0], curPos[1] + (pilFontSize[1] - 2),
                                curPos[0] + pilFontSize[0], curPos[1] + (pilFontSize[1] - 2)),
                            fill=(*ENNToolMiRCARTColours[fontColour], 255))
                curPos[0] += pilFontSize[0]
            curPos[0], curPos[1] = 0, curPos[1] + pilFontSize[1]
    pilImage.save(outFileName)
    artInfo = {}
    artInfo["rowHeight"] = pilFontSize[1]
    artInfo["rowWidth"] = pilFontSize[0]
    artInfo["texHeight"] = pilImageSize[1]
    artInfo["texWidth"] = pilImageSize[0]
    with open(outInfoFileName, "w") as fileObject:
        yaml.dump(artInfo, fileObject)

if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
