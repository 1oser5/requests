# -*- coding: utf-8 -*-

"""
requests._internal_utils
~~~~~~~~~~~~~~

Provides utility functions that are consumed internally by Requests
which depend on extremely few external helpers (such as compat)
"""
'''
@Time    :   2019/11/20 15:22:51
@Author  :   Xia
内部使用函数库
'''
from .compat import is_py2, builtin_str, str


def to_native_string(string, encoding='ascii'):
    """Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """
    '''
    @Time    :   2019/11/20 16:42:30
    @Author  :   Xia
    因为看懂这个函数还去恶补了一下编码问题，我怀疑可能是 python2.x 使用的 str 编码和 python3.x 有所不同
    事实上 python2.x 有两种字符串类型，str 和 Unicode 
    str 是 ascii 编码，无法表示中文

    builtin_str 在 compat.py 里表示 ASCII
    下述代码表示如果 string 是 ASCII 就直接输出
    如果不是就用 ASCII 码编码后输出

    那中文怎么办？？
    '''
    if isinstance(string, builtin_str):
        out = string
    else:
        if is_py2:
            out = string.encode(encoding)
        else:
            out = string.decode(encoding)

    return out


def unicode_is_ascii(u_string):
    """Determine if unicode string only contains ASCII characters.

    :param str u_string: unicode string to check. Must be unicode
        and not Python 2 `str`.
    :rtype: bool
    """
    assert isinstance(u_string, str)
    try:
        u_string.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False
