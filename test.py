#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import argparse


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-i', '--input', default='IN')
    parser.add_argument ('-o', '--output', default='OUT')
    return parser

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    # print (namespace)
    print ("Привет, {}!".format (namespace.input))

    print ("Привет, {}!".format (namespace.output))
