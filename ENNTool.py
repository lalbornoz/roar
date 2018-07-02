#!/usr/bin/env python3
#
# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#
# TODO:
# 1) -A: render frame #1, render frame #2, ...
# 2) -o: support at least {GIF,MP4,WEBM}
# 3) -s: effects: rotate, smash into bricks, swirl, wave, ...
# 4) Feature: include ETA @ progress bar
# 5) Feature: autodetect video width from widest mircart
# 6) Feature: render mircart as 3D blocks vs flat surface
# 7) Optimisation: dont stall GPU w/ glReadPixels(), switch to asynchronous model w/ FBO or PBO (http://www.songho.ca/opengl/gl_fbo.html, http://www.songho.ca/opengl/gl_pbo.html)
# 8) OpenGL: use VAOs + glVertexAttribFormat + glVertexAttribBinding
# 9) OpenGL: use glEnable(GL_BLEND) + glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) & multiply texel * bgcolour (https://learnopengl.com/Advanced-OpenGL/Blending)
#

from getopt import getopt, GetoptError
from glob import glob
from OpenGL.GL import *
import os, sys, time
import wx

from ENNToolGLCanvasPanel import ENNToolGLCanvasPanel
from ENNToolGLTTFTexture import ENNToolGLTTFTexture
from ENNToolMiRCARTImporter import ENNToolMiRCARTImporter

class ENNToolApp(object):
    """XXX"""

    # {{{ parseArgv(self, argv): XXX
    def parseArgv(self, argv):
        def usage(argv0):
            print("usage: {}".format(os.path.basename(argv0)), file=sys.stderr)
            print("       [-A] [-f fps] [-h] [-o pname]".format(os.path.basename(argv0)), file=sys.stderr)
            print("       [-p] [-r WxH] [-R WxH] [-s pname]", file=sys.stderr)
            print("       [-S] [-t pname] [-v] [--] pname..", file=sys.stderr)
            print("", file=sys.stderr)
            print("       -a........: select animation mode", file=sys.stderr)
            print("       -f fps....: set video FPS; defaults to 25", file=sys.stderr)
            print("       -h........: show this screen", file=sys.stderr)
            print("       -o pname..: output video pathname", file=sys.stderr)
            print("       -p........: play video after rendering", file=sys.stderr)
            print("       -r WxH....: set video resolution; defaults to 1152x864", file=sys.stderr)
            print("       -R WxH....: set MiRCART cube resolution; defaults to 0.1x0.2", file=sys.stderr)
            print("       -s pname..: input script pathname", file=sys.stderr)
            print("       -S........: select scrolling mode", file=sys.stderr)
            print("       -t pname..: set MiRCART texture pathname; defaults to {}".format(os.path.join("assets", "texture.png")), file=sys.stderr)
            print("       -v........: be verbose", file=sys.stderr)
        try:
            optlist, argv = getopt(argv[1:], "Af:ho:pr:R:s:St:v")
            optdict = dict(optlist)

            if "-h" in optdict:
                usage(sys.argv[0]); exit(0);
            elif not "-o" in optdict:
                raise GetoptError("-o pname must be specified")
            elif not len(argv):
                raise GetoptError("at least one MiRCART input pname must be specified")

            if not "-f" in optdict:
                optdict["-f"] = "25"
            if not "-r" in optdict:
                optdict["-r"] = "1152x864"
            if not "-R" in optdict:
                optdict["-R"] = "0.1x0.2"
            if not "-t" in optdict:
                optdict["-t"] = os.path.join("assets", "texture.png")

            if "-r" in optdict:
                optdict["-r"] = [int(r) for r in optdict["-r"].split("x")][0:2]
            if "-R" in optdict:
                optdict["-R"] = [float(r) for r in optdict["-R"].split("x")][0:2]
        except GetoptError as e:
            print(e.msg); usage(sys.argv[0]); exit(1);
        return argv, optdict
    # }}}
    # {{{ printProgress(self, progressCur, progressMax): XXX
    def printProgress(self, progressCur, progressMax):
        progressDiv = float(progressCur / progressMax)
        if progressDiv >= 1:
            progressDiv = 1; endChar = "\n";
        else:
            endChar = ""
        print("\r[{:<50}] {}%".format(
            ("=" * int(progressDiv * 50)), int(progressDiv * 100)), end=endChar)
    # }}}
    # {{{ modeScroll(self, argv, optdict, panelGLCanvas, texturePathName, fps=25, scrollRate=0.25): XXX
    def modeScroll(self, argv, optdict, panelGLCanvas, texturePathName, fps=25, scrollRate=0.25):
        MiRCART = []
        for inFileArg in argv:
            for inFile in sorted(glob(inFileArg)):
                MiRCART += ENNToolMiRCARTImporter(inFile).outMap

        curY, rotateX, rotateY, translateY = 0, 0, 0, scrollRate
        artTextureId, artInfo = ENNToolGLTTFTexture(MiRCART, optdict["-R"], optdict["-r"]).getParams()
        artVbo, artVboLen, lastY, numVertices = panelGLCanvas.renderMiRCART(artInfo, MiRCART, cubeSize=optdict["-R"])
        if "-v" in optdict:
            print("{} vertices".format(numVertices))
        w, h = panelGLCanvas.GetClientSize(); w, h = max(w, 1.0), max(h, 1.0);

        while True:
            self.printProgress(curY, lastY)
            for numFrame in range(fps):
                panelGLCanvas.renderFrame(artTextureId, artVbo, artVboLen)
                if translateY:
                    glTranslatef(0, translateY, 0); curY += translateY
                if rotateX:
                    glRotatef(rotateX * (180.0/w), 0.0, 1.0, 0.0)
                if rotateY:
                    glRotatef(rotateY * (180.0/h), 1.0, 0.0, 0.0)
                panelGLCanvas.saveFrame()
            if curY >= lastY:
                self.printProgress(curY, lastY); break;
    # }}}
    # {{{ __init__(self, argv): XXX
    def __init__(self, argv):
        argv, optdict = self.parseArgv(argv)
        wxApp = wx.App(False)
        appFrameSize = optdict["-r"]
        appFrame = wx.Frame(None, size=appFrameSize); appFrame.Hide();
        appPanelSkin = wx.Panel(appFrame, wx.ID_ANY)

        videoFps, videoPath = int(optdict["-f"]), optdict["-o"]
        panelGLCanvas = ENNToolGLCanvasPanel(appPanelSkin, size=appFrameSize, videoPath=videoPath)
        panelGLCanvas.initOpenGL()
        panelGLCanvas.initShaders()
        panelGLCanvas.initVideoWriter(fps=videoFps)

        if "-v" in optdict:
            time0 = time.time()
        self.modeScroll(argv, optdict, panelGLCanvas, fps=videoFps, texturePathName=optdict["-t"])
        if "-v" in optdict:
            print("delta {}s".format(time.time() - time0))
        if "-p" in optdict:
            os.startfile(videoPath)
    # }}}

#
# Entry point
def main(*argv):
    ENNToolApp(argv)

if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
