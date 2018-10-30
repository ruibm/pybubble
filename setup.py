#!/usr/bin/env python

from distutils.core import setup
import glob
import py2exe

setup(console=['pybubble.py'],
		name='pybubble',
      version='0.1',
		description='Python Puzzle Bubble Clone',
      author='Rui Barbosa Martins',
      author_email='ruibmartins@gmail.com',
		options={"py2exe":{"optimize":2}},
      url='http://www.python.org/',
		data_files=[("images", glob.glob("images\\*.bmp"))],
     )

