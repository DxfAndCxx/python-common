#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-06-25 12:23:52
# Author     : 陈小雪
# E-mail     : shell_chen@yeah.net
# Version    : 1.0.1


import os
import logging
import imp


class Plugins(object):
    def __init__(self, path, *attrs):
        self.path = path
        self.attrs = attrs

    def load_module(self):
        if not os.path.isdir(self.path):
            logging.error("plugin path:[%s] is not dir"%self.path)
            return

        infos = { }
        modules = os.listdir(self.path)

        for module in modules:
            if not module.endswith(".py"):
                continue

            module_path = os.path.join(self.path, module)
            module_loaded = imp.load_source(module_path.replace('.', '_'), module_path)
            info = self.__module_init(module_loaded)

            if info:
                infos[module[0:-3]] = info

        return infos

    def __module_init(self, module):
        info = [module]
        for attr in self.attrs:
            if not hasattr(module, attr):
                logging.error("module init:%s not hasattr [%s]" %(module, attr))
                return [ ]
            info.append(hasattr(module, attr))

        return info







