#!/usr/bin/env python
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='uricore',
    version='0.1.0',
    description='URI Parsing for Humans.',
    long_description=open('README.md').read(),
    author='Matthew Hooker & Jeremy Avnet & Matt Chisholm',
    author_email='uricore@librelist.com',
    url='https://github.com/core/uricore',
    py_modules= ['uricore',],
    license='BSD',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    )
)
