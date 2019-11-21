# -*- coding: utf-8 -*-

"""
requests.hooks
~~~~~~~~~~~~~~

This module provides the capabilities for the Requests hooks system.

Available hooks:

``response``:
    The response generated from a Request.
"""
HOOKS = ['response']


def default_hooks():
    return {event: [] for event in HOOKS}

# TODO: response is the only one


def dispatch_hook(key, hooks, hook_data, **kwargs):
    """Dispatches a hook dictionary on a given piece of data."""
    hooks = hooks or {}
    hooks = hooks.get(key)
    if hooks:
        if hasattr(hooks, '__call__'):
            hooks = [hooks]
        for hook in hooks:
            _hook_data = hook(hook_data, **kwargs)
            if _hook_data is not None:
                hook_data = _hook_data
    return hook_data
    '''
    @Time    :   2019/11/21 15:50:04
    @Author  :   Xia
    28行判断了 hooks 中有没有可调用对象，如果有的话，就把 hook 变成一个数组
    然后遍历调用每一个可调用对象，记录上次以保存的值，这个可用用来防御 SSRF 漏洞。
    '''
        
