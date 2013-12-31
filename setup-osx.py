"""
Based on:
- https://github.com/tam7t/markdown-editor/blob/master/setup-osx.py
- https://github.com/tam7t/photograbber/blob/master/setup-osx.py

Usage: python setup-osx.py py2app
"""

from setuptools import setup

setup(
    setup_requires=['py2app'],
    app=['done/done.py'],
    options={
        'py2app': {
            'iconfile': 'done.icns'
        }
    }
)
