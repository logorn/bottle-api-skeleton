#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.bootstrap import bootstrap

def main():
    server = bootstrap(host='localhost', port=8080)
    server.start()

if __name__ == '__main__':
   main()