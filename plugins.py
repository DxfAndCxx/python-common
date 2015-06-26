#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-06-26 14:40:30
# @Author  : 陈小雪 (shell_chen@yeah.net)
# @Link    :
# @Version : 0.0.1

import os
import logging
import imp

class Plugins(object):
    def __init__(self, path, fun):
        self.path = path
        self.call_back = fun
        self.ignore_path = None
        self.ignore_modules = [ ]

    def load_modules(self):
        if not os.path.isdir(self.path):
            logging.error("plugin path:[%s] is not dir"%self.path)
            return

        modules = os.listdir(self.path)

        for module in modules:
            if not module.endswith(".py"):
                continue

            module_name = module[0:-3]

            if module in self.ignore_modules or module_name in self.plugins_ignore:
                logging.info("plugin ignore module:%s"%module_name)
                continue

            module_path = os.path.join(self.path, module)
            module_loaded = imp.load_source(module_path[0:-3], module_path)
            self.fun(module_loaded)


    def get_ignore_modules(self):
        self.ignore_path = os.path.join(self.path, ".modulesignore")
        if os.path.isfile(self.ignore_path):
            with open(self.ignore_path) as fp:
                for line in fp.readlines():
                    line = line.strip()
                    if not line:continue
                    self.ignore_modules.append(line)

    def module_init_hook(self, module):








