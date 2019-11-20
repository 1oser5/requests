# -*- coding: utf-8 -*-

#   __
#  /__)  _  _     _   _ _/   _
# / (   (- (/ (/ (- _)  /  _)
#          /

"""
Requests HTTP Library
~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings.
Basic GET usage:

   >>> import requests
   >>> r = requests.get('https://www.python.org')
   >>> r.status_code
   200
   >>> b'Python is a programming language' in r.content
   True

... or POST:

   >>> payload = dict(key1='value1', key2='value2')
   >>> r = requests.post('https://httpbin.org/post', data=payload)
   >>> print(r.text)
   {
     ...
     "form": {
       "key1": "value1",
       "key2": "value2"
     },
     ...
   }

The other HTTP methods are supported - see `requests.api`. Full documentation
is at <https://requests.readthedocs.io>.

:copyright: (c) 2017 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

'''
@Time    :   2019/11/20 14:51:11
@Author  :   Xia
依赖检查，报错格式设置等
'''
import urllib3
import chardet
import warnings
from .exceptions import RequestsDependencyWarning


def check_compatibility(urllib3_version, chardet_version):
    urllib3_version = urllib3_version.split('.')
    assert urllib3_version != ['dev']  # Verify urllib3 isn't installed from git.

    # Sometimes, urllib3 only reports its version as 16.1.
    if len(urllib3_version) == 2:
        urllib3_version.append('0')

    # Check urllib3 for compatibility.
    major, minor, patch = urllib3_version  # noqa: F811
    major, minor, patch = int(major), int(minor), int(patch)
    # urllib3 >= 1.21.1, <= 1.25
    assert major == 1
    assert minor >= 21
    assert minor <= 25

    # Check chardet for compatibility.
    major, minor, patch = chardet_version.split('.')[:3]
    major, minor, patch = int(major), int(minor), int(patch)
    # chardet >= 3.0.2, < 3.1.0
    assert major == 3
    assert minor < 1
    assert patch >= 2


def _check_cryptography(cryptography_version):
    # cryptography < 1.3.4
    try:
        cryptography_version = list(map(int, cryptography_version.split('.')))
    except ValueError:
        return
    '''
    @Time    :   2019/11/20 14:52:06
    @Author  :   Xia
    列表比大小默认从第一项开始，如果不是同类型会报错
    '''
    if cryptography_version < [1, 3, 4]:
        warning = 'Old version of cryptography ({}) may cause slowdown.'.format(cryptography_version)
        warnings.warn(warning, RequestsDependencyWarning)

# Check imported dependencies for compatibility.
try:
    check_compatibility(urllib3.__version__, chardet.__version__)
    '''
    @Time    :   2019/11/20 15:00:06
    @Author  :   Xia
    因为上述函数一个是使用 assert 比较，一个是抛出错误，看代码好像 try 可以捕获作用域内函数的错误
    
    warning.warn 函数的格式是 warning.warn(message,ErrorType),后面的 RequestsDependencyWarning 应该是封装在 exceptions.py 中的错误类型
    '''
except (AssertionError, ValueError):
    warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
                  "version!".format(urllib3.__version__, chardet.__version__),
                  RequestsDependencyWarning)

# Attempt to enable urllib3's SNI support, if possible
try:
    from urllib3.contrib import pyopenssl
    pyopenssl.inject_into_urllib3()

    # Check cryptography version
    from cryptography import __version__ as cryptography_version
    _check_cryptography(cryptography_version)
except ImportError:
    pass

# urllib3's DependencyWarnings should be silenced.
from urllib3.exceptions import DependencyWarning
warnings.simplefilter('ignore', DependencyWarning)

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__
from .__version__ import __copyright__, __cake__
'''
@Time    :   2019/11/20 15:12:55
@Author  :   Xia
from . import xxx 表示从当前路径引用 xxx 文件
'''
from . import utils
from . import packages
from .models import Request, Response, PreparedRequest
from .api import request, get, head, post, patch, put, delete, options
from .sessions import session, Session
from .status_codes import codes
from .exceptions import (
    RequestException, Timeout, URLRequired,
    TooManyRedirects, HTTPError, ConnectionError,
    FileModeWarning, ConnectTimeout, ReadTimeout
)

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler
'''
@Time    :   2019/11/20 15:14:43
@Author  :   Xia
TODO
'''
logging.getLogger(__name__).addHandler(NullHandler())

# FileModeWarnings go off per the default.
warnings.simplefilter('default', FileModeWarning, append=True)
