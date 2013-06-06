#!/usr/bin/env python
"""
    setup for pymensa
"""

from setuptools import setup


REQUIREMENTS = [
    'sqlite3',
    'urllib2',
    'lxml',
    'pyxmpp2'
]

SCRIPTS = [
    'bin/pymensa_create_db',
    'bin/pymensa_update_db',
    'bin/pymensa_send_xmpp',
    'bin/pymensa',
]

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Topic :: Utilities",
]

PLATFORMS = ["Linux", "Mac OS-X", "Unix"]

setup(
    name='pymensa',
    version='0.1.0',
    description='A mensamenu parser and XMPP Client',
    author='Henning Dickten',
    author_email='pymensa@dickten.info',
    requires=REQUIREMENTS,
    packages=['pymensa'],
    scripts=SCRIPTS,
    url='https://github.com/hensing/pymensa',
    download_url='https://github.com/hensing/pymensa',
    license='Expat/MIT',
    platforms=PLATFORMS,
    classifiers=CLASSIFIERS
)
