# mirc2png -- convert ASCII w/ mIRC control codes to monospaced PNG (for EFnet #MiRCART)
* Prerequisites: python3 && python3-pil (&& python3-{json,requests,urllib3} for pngbot.py) on Debian-family Linux distributions
* mirc2png.py usage: mirc2png.py `<MiRCART input file pathname>` `<PNG image output file pathname>` [`<Font file pathname; defaults to DejaVuSansMono.ttf>`] [`<Font size; defaults to 11>`]
* pngbot.py usage: pngbot.py `<IRC server hostname>` [`<IRC server port; defaults to 6667>`] [`<IRC bot nick name; defaults to pngbot>`] [`<IRC bot user name; defaults to pngbot>`] [`<IRC bot real name; defaults to pngbot>`] [`<IRC bot channel name; defaults to #MiRCART>`]
