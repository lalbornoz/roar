#!/usr/bin/env python3
#
# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
# Copyright (c) 2018 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
# This project is licensed under the terms of the MIT license.
#
# TODO:
# 1) -A, -S: replace w/ -s, implement animation script: render frame #1, render frame #2, ...; scrolling script; effects: rotate, smash into bricks, swirl, wave, ...
# 2) Feature: include ETA(s) @ progress bar(s)
# 3) Feature: autodetect video width from widest mircart
# 4) Feature: render mircart as 3D blocks vs flat surface

#
# 1) Optimisation: speed up ENNToolMiRCARTImporter
# 2) Cleanup: use names @ optdict + set from optdefaults
# 3) Feature: scrolling speed as <how many Y units>x<count of frame(s)>
# 4) Cleanup: use VAOs + glVertexAttribFormat + glVertexAttribBinding
# 5) Optimisation: split mIRC art into separate VBOs & implement rudimentary culling
# 6) Optimisation: only call glReadPixels() when changes were made relative to the last call
# 7) Split video output into separate module, switch to GUI
# 8) FBOs http://www.songho.ca/opengl/gl_fbo.html
#

from getopt import getopt, GetoptError
from glob import glob
from OpenGL.GL import *
import os, sys, time
import wx

from ENNToolGLCanvasPanel import ENNToolGLCanvas, ENNToolGLPanel
from ENNToolGLTTFTexture import ENNToolGLTTFTexture
from ENNToolGLVideoWriter import ENNToolGLVideoWriter
from ENNToolMiRCARTImporter import ENNToolMiRCARTImporter

class ENNToolApp(object):
    """XXX"""

    # {{{ parseArgv(self, argv): XXX
    def parseArgv(self, argv):
        def usage(argv0):
            print("usage: {}".format(os.path.basename(argv0)), file=sys.stderr)
            print("       [-A] [-f fps] [-h] [-o fname]".format(os.path.basename(argv0)), file=sys.stderr)
            print("       [-p] [-r WxH] [-R WxH] [-s fname]", file=sys.stderr)
            print("       [-S] [-v] [--] fname..", file=sys.stderr)
            print("", file=sys.stderr)
            print("       -a........: select animation mode (UNIMPLEMENTED)", file=sys.stderr)
            print("       -f fps....: set video FPS; defaults to 25", file=sys.stderr)
            print("       -h........: show this screen", file=sys.stderr)
            print("       -o fname..: output video filename; extension determines video type", file=sys.stderr)
            print("       -p........: play video after rendering", file=sys.stderr)
            print("       -r WxH....: set video resolution; defaults to 1152x864", file=sys.stderr)
            print("       -R WxH....: set MiRCART cube resolution; defaults to 0.1x0.2", file=sys.stderr)
            print("       -s fname..: input script filename", file=sys.stderr)
            print("       -S........: select scrolling mode", file=sys.stderr)
            print("       -v........: be verbose", file=sys.stderr)
        try:
            optlist, argv = getopt(argv[1:], "Af:ho:pr:R:s:Sv")
            optdict = dict(optlist)

            if "-h" in optdict:
                usage(sys.argv[0]); exit(0);
            elif not len(argv):
                raise GetoptError("at least one MiRCART input fname must be specified")

            if not "-f" in optdict:
                optdict["-f"] = "25"
            if not "-r" in optdict:
                optdict["-r"] = "1152x864"
            if not "-R" in optdict:
                optdict["-R"] = "0.1x0.2"

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
    # {{{ modeScroll(self, argv, optdict, GLVideoWriter, GLpanel, GLpanel, fps=25, scrollRate=0.1): XXX
    def modeScroll(self, argv, optdict, GLVideoWriter, GLcanvas, GLpanel, fps=25, scrollRate=0.1):
        MiRCART = []
        if "-v" in optdict:
            time0 = time.time()
        for inFileArg in argv:
            for inFile in sorted(glob(inFileArg)):
                MiRCART += ENNToolMiRCARTImporter(inFile).outMap
        if "-v" in optdict:
            print("mIRC art import delta {:.3f}ms".format((time.time() - time0) * 1000))

        if "-v" in optdict:
            time0 = time.time()
        artTextureId, artInfo = ENNToolGLTTFTexture(MiRCART, optdict["-R"], optdict["-r"]).getParams()
        if "-v" in optdict:
            print("TTF texture generation delta {:.3f}ms".format((time.time() - time0) * 1000))
        artVbo, artVboLen, lastY, numVertices = GLcanvas.renderMiRCART(artInfo, MiRCART, cubeSize=optdict["-R"])
        if "-v" in optdict:
            print("{} vertices".format(numVertices))
        def scrollFrameFun():
            curY, rotateX, rotateY, translateY = 0, 0, 0, scrollRate
            w, h = GLcanvas.GetClientSize(); w, h = max(w, 1.0), max(h, 1.0);
            def scrollFrame():
                nonlocal curY
                self.printProgress(curY, lastY)
                GLcanvas.renderFrame(artTextureId, artVbo, artVboLen)
                if translateY:
                    glTranslatef(0, translateY, 0); curY += translateY
                if rotateX:
                    glRotatef(rotateX * (180.0/w), 0.0, 1.0, 0.0)
                if rotateY:
                    glRotatef(rotateY * (180.0/h), 1.0, 0.0, 0.0)
                if "-o" in optdict:
                    GLVideoWriter.saveFrame()
                else:
                    GLcanvas.SwapBuffers()
                if curY >= lastY:
                    self.printProgress(curY, lastY)
                    if "-o" in optdict:
                        GLVideoWriter.saveVideo()
                    return False
                return True
            return scrollFrame
        if "-o" in optdict:
            frameFun = scrollFrameFun()
            while True:
                if not frameFun():
                    break
        else:
            GLpanel.frameFun = scrollFrameFun()
            self.wxApp.MainLoop()
    # }}}
    # {{{ __init__(self, argv): XXX
    def __init__(self, argv):
        argv, optdict = self.parseArgv(argv)
        self.wxApp = wx.App(False)
        appFrameSize = [c + 128 for c in optdict["-r"]]
        self.appFrame = wx.Frame(None, size=appFrameSize)
        appPanelSkin = wx.Panel(self.appFrame, wx.ID_ANY)

        videoFps, videoPath = int(optdict["-f"]), optdict["-o"] if "-o" in optdict else None
        GLpanel = ENNToolGLPanel(appPanelSkin, size=optdict["-r"], parentFrame=self.appFrame)
        GLcanvas = ENNToolGLCanvas(GLpanel, optdict["-r"])
        GLcanvas.initOpenGL()
        GLcanvas.initShaders()
        GLVideoWriter = ENNToolGLVideoWriter(videoPath, GLpanel.GetClientSize(), videoFps=videoFps)

        if "-o" in optdict:
            self.appFrame.Hide()
        else:
            self.appFrame.Show(); self.appFrame.SetFocus();

        if "-v" in optdict:
            time0 = time.time()
        self.modeScroll(argv, optdict, GLVideoWriter, GLcanvas, GLpanel, fps=videoFps)
        if "-v" in optdict:
            print("delta {}s".format(time.time() - time0))
        if  "-o" in optdict \
        and "-p" in optdict:
            os.startfile(videoPath)
    # }}}

#
# Entry point
def main(*argv):
    ENNToolApp(argv)

if __name__ == "__main__":
    main(*sys.argv)

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
