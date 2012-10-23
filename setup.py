#!/usr/bin/env python
"""
Deployment script for prismscript.
"""
__author__ = 'Neil Tallim'

from distutils.core import setup

setup(
 name = 'prismscript',
 version = '1.0.2',
 description = 'A flexible, embeddable interpreted language for I/O-control logic',
 author = 'Neil Tallim',
 author_email = 'neil.tallim@linux.com',
 license = 'CC3-BY-SA',
 url = 'http://code.google.com/p/prismscript/',
 packages = [
  'prismscript',
  'prismscript.processor',
  'prismscript.processor.grammar',
  'prismscript.processor.grammar.structure',
  'prismscript.stdlib',
  'prismscript.stdlib.lang',
  'prismscript.stdlib.math',
  'prismscript.stdlib.util',
 ],
)

