## MiRCART-{cordoba,nw,www} -- mIRC art editor for {Android,{Linux,Windows},browsers} (WIP)
Originally based on [[1](#r1)].

## IrcMiRCARTBot.py -- IRC<->MiRC2png bot (for EFnet #MiRCART) (pending cleanup)
* Prerequisites: python3 && python3-{json,requests,urllib3} on Debian-family Linux distributions
* IrcMiRCARTBot.py usage: IrcMiRCARTBot.py `<IRC server hostname>` [`<IRC server port; defaults to 6667>`] [`<IRC bot nick name; defaults to pngbot>`] [`<IRC bot user name; defaults to pngbot>`] [`<IRC bot real name; defaults to pngbot>`] [`<IRC bot channel name; defaults to #MiRCART>`]

## MiRCARTToPngFile.py -- convert ASCII w/ mIRC control codes to monospaced PNG (pending cleanup)
* Prerequisites: python3 && python3-pil on Debian-family Linux distributions
* MiRC2png.py usage: MiRC2png.py `<MiRCART input file pathname>` `<PNG image output file pathname>` [`<Font file pathname; defaults to DejaVuSansMono.ttf>`] [`<Font size; defaults to 11>`]

## References
``Fri, 05 Jan 2018 17:01:47 +0100  [1]`` <a href="https://asdf.us/asciiblaster" id="r1">asciiblaster</a>  
  
vim:tw=0
