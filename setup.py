#!/usr/bin/env python2

from distutils.core import setup

setup(scripts=['script/divvyup'],
      name='DivvyUp',
      version='0.5',
      description='A simple application that uses the envelope system to help you budget your money.',
      author='David Couzelis',
      author_email='drcouzelis@gmail.com',
      url='http://sourceforge.net/projects/divvyup/',
      license = 'GPL',
      packages=['divvyup'],
      package_data={'divvyup':['icons/*', 'help/*']}
)

