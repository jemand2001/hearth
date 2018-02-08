#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='Hearthstone rebuild',
    version='0.1.0.1a',
    author=u'Björn Brandt',
    packages=find_packages(),
    scripts=['main.py'],
    package_data={
        'gui': ['*.png', '*.bmp']
    }
)
# install_requires=['pygame'],
