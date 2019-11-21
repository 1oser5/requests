#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
requests.certs
~~~~~~~~~~~~~~

This module returns the preferred default CA certificate bundle. There is
only one — the one from the certifi package.

If you are packaging Requests, e.g., for a Linux distribution or a managed
environment, you can change the definition of where() to return a separately
packaged CA bundle.
"""
'''
@Time    :   2019/11/21 14:24:48
@Author  :   Xia
查看证书在哪的
'''
from certifi import where

if __name__ == '__main__':
    print(where())
