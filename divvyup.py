#!/usr/bin/env python2

import os
import sys

import divvyup

if __name__ == '__main__':

    # With installation
    #for path in sys.path:
    #    if path[-14:] == "/site-packages":
    #        cwd = path + "/divvyup"
    #divvyup.divvyup.main(cwd)

    # No installation
    divvyup.divvyup.main()

