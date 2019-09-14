#!/usr/bin/env python3
#
# roar.py -- mIRC art editor for Windows & Linux
# Copyright (c) 2018, 2019 Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
#

from distutils.core import setup

setup(
    author_email="lucio@lucioillanes.de",
    author="Lucio Andrés Illanes Albornoz",
    description="mIRC art editor for Windows & Linux",
    include_package_data=True,
    install_requires=("requests==2.22.0", "urllib3==1.25.3", "wxPython==4.0.6"),
    license="MIT",
    name="roar",
    package_data={"": ["assets/*/*", "LICENCE", "README.md"]},
    packages=(".", "assets", "libcanvas", "libgui", "libroar", "librtl", "libtools"),
    url="https://github.com/lalbornoz/roar/",
    version="3.1")

# vim:expandtab foldmethod=marker sw=4 ts=4 tw=120
