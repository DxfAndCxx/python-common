#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-06-25 12:23:52
# Author     : 陈小雪
# E-mail     : shell_chen@yeah.net
# Version    : 1.0.1
"""
插件思想来自于在web开发中, 业务功能和视图模块相对应,
现在把它抽象出来 用于可加载web插件的的通用模块,
目前,这种思想已用于到cottle和sunshine中

Plugins在初始化时需要两个参数:
    path : 加载插件的目录
    attr : 自动加载的模块中的 属性
           加载的模块中必须要有这两个属性,否则会报错
           attr[0]:为模块名字, 会用于url的前缀
           attr[1]:模块中的url集
通过Plugin.URLS可以得到 url和视图函数对应的list

"""

import os
import logging
import imp

class Plugins(object):
    URLS = [ ]
    PLUGINS = [ ]
    def __init__(self, path, *attrs, **kwagrs):
        self.path = path
        self.attrs = attrs
        self.infos = { }
        self.plugins_ignore = kwagrs.get("ignore",[ ])
        self.__load_views()
        self.__logurls()

    def __load_modules(self):
        if not os.path.isdir(self.path):
            logging.error("plugin path:[%s] is not dir"%self.path)
            return

        modules = os.listdir(self.path)

        for module in modules:
            if not module.endswith(".py"):
                continue

            module_name = module[0:-3]
            if module in self.plugins_ignore:
                continue
            if module_name in self.plugins_ignore:
                continue

            module_path = os.path.join(self.path, module)
            module_loaded = imp.load_source(module_name, module_path)
            info = self.__module_init(module_loaded)

            if info:
                self.infos[module_name] = info

    def __module_init(self, module):
        info = [module]
        for attr in self.attrs:
            if not hasattr(module, attr):
                logging.error("module init:%s not hasattr [%s]" %(module, attr))
                return [ ]
            info.append(getattr(module, attr))

        return info

    def __url_groups(self, urls):
        i = 0
        t = [ ]
        while i < len(urls):
            t.append((urls[i], urls[i+1]))
            i += 2
        return t

    def __load_views(self):
        """
        加载视图函数, 得到url对应视图函数的list
        """
        self.__load_modules()
        for module, name , urls in self.infos.values():
            for url, fun in self.__url_groups(urls):
                if url.startswith("/"):
                    url = "/%s%s"%(name, url)
                else:
                    url = os.path.join("/", name, url)

                if isinstance(fun, basestring):
                    if not hasattr(module, fun):
                        logging.error("plugin %s not hasattr [%s]"%(module, fun))
                        continue
                    fun = getattr(module, fun)

                self.URLS.append((url, fun))

            self.PLUGINS.append((name, module))

    def __logurls(self):
        """
             打印url 对应视图函数的日志
        """
        maxlen = 0
        for url, fun in self.URLS:
            if len(url) > maxlen:
                maxlen = len(url)

        lines = [""]
        for url, fun in self.URLS:
            lines.append("%s ===> %s" % (url.ljust(maxlen), fun))
        logging.info("\n".join(lines))

    def get_urls(self):
        return self.URLS



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    #filename=".log",
    )

    path = "/home/cxx/github/DxfAndCxx/python-common/plugins"
    plugins = Plugins(path, "name", "urls", ignore=["test1"])
    ulrs = plugins.get_urls()
