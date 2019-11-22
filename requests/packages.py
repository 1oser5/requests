#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import sys

# This code exists for backwards compatibility reasons.
# I don't like it either. Just look the other way. :)
'''
@Time    :   2019/11/21 17:41:20
@Author  :   Xia
先把 'urllib3', 'idna', 'chardet' 这三个包 import 进来，然后
'''
for package in ('urllib3', 'idna', 'chardet'):
    locals()[package] = __import__(package)
    print(locals()[package])
    # This traversal is apparently necessary such that the identities are
    # preserved (requests.packages.urllib3.* is urllib3.*)
    for mod in list(sys.modules):
        if mod == package or mod.startswith(package + '.'):
            sys.modules['requests.packages.' + mod] = sys.modules[mod]
            # print(sys.modules['requests.packages.' + mod])

# Kinda cool, though, right?
