#!/usr/bin/env python

from distutils.core import setup

setup(name='gmail-backup',
      version='1.0',
      description='Backup gmail emails',
      author='Charles Teinturier',
      author_email='teintu.c@gmail.com',
      scripts=['gmailbackup'],
      packages=['core'],
      install_requires=[
        'configparser',
        ]
     )
