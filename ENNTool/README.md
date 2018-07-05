# ENNTool -- mIRC art animation tool (for EFnet #MiRCART) (WIP)
Copyright (c) 2018 Lucio Andrés Illanes Albornoz <<lucio@lucioillanes.de>>  
This project is licensed under the terms of the MIT licence.

## Installation instructions on Windows
1. Install Python v>=3.5.x[[4](#r4)]
2. Install script dependencies w/ the following elevated command prompt command line:  
   `pip install chardet numpy Pillow PyOpenGL wxPython`
3. Download OpenCV wheel[[1](#r1)] and install w/ the following elevated command prompt command line:  
   `pip install <path to OpenCV wheel>`

## How to run
```
usage: ENNTool.py
       [-A] [-f fps] [-h] [-o fname]
       [-p] [-r WxH] [-R WxH] [-s fname]
       [-S] [-v] [--] fname..

       -a........: select animation mode (UNIMPLEMENTED)
       -f fps....: set video FPS; defaults to 25
       -h........: show this screen
       -o fname..: output video filename; extension determines video type
       -p........: play video after rendering
       -r WxH....: set video resolution; defaults to 1152x864
       -R WxH....: set MiRCART cube resolution; defaults to 0.1x0.2
       -s fname..: input script filename
       -S........: select scrolling mode
       -v........: be verbose
```

## References
``Wed, 04 Jul 2018 09:33:53 +0200 [1]`` <a href="https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv" id="r1">Python Extension Packages for Windows - Christoph Gohlke</a>  
``Wed, 04 Jul 2018 09:38:28 +0200 [2]`` <a href="https://github.com/cisco/openh264/releases" id="r2">Releases · cisco/openh264 · GitHub</a>  
``Wed, 04 Jul 2018 09:49:38 +0200 [3]`` <a href="https://github.com/opencv/opencv/issues/6080" id="r3">opencv_ffmpeg and OpenH264-x.y.z · Issue #6080 · opencv/opencv · GitHub</a>  
``Wed, 04 Jul 2018 10:24:12 +0200 [4]`` <a href="https://www.python.org/downloads/windows" id="r4">Python Releases for Windows | Python.org</a>  
