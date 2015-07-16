#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2015-07-15 15:07:19
# Author  : 陈小雪
# E-mail  : shell_chen@yeah.net
# Version : v1.0.1

import os
IGNORE = [".pyc",".git",".log"]
PROMPT = [".h",".c",".py",".sh"]


class Dir(object):
    def __init__(self, path, ignore_file=None, prompt_file=None, depth=-1):
        self.path = os.path.normpath(path)
        self.depth = depth
        # self._ignores = self._load_file(ignore_file)
        # self._prompts = self._load_file(prompt_file)
        self._ignores = IGNORE
        self._prompts = PROMPT

        self.DIRS = [ ]
        self._load_path(path)

    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Dir, cls).__new__(cls,*args, **kw)
        return cls._instance

    def _load_file(self, filename):
        tmp = [ ]
        if (not filename) or (not os.path.isfile(filename)):
            return tmp

        with open(filename, "r") as fp:
            lines = fp.readlines()
            for line in lines:
                line = line.strip()
                line = line.strip("*")
                if not line:
                    continue
                tmp.append(line.strip())
        return tmp

    def _get_deepth(self, path):
        return len(path.split("/")) - len(self.path.split("/"))

    def _load_path(self, path):
        if not os.path.isdir(path):
            raise Exception("%s is not a dir"%path)

        if self._get_deepth(path) < self.depth:
            return

        dirs = os.listdir(path)
        for d in dirs:
            if d in self._ignores:
                continue

            splits = os.path.splitext(d)
            postfix = splits[1]

            if not postfix:
                postfix = splits[0]

            if postfix in self._ignores:
                continue

            abs_path = os.path.join(path,d)
            if os.path.isdir(abs_path):
                dir_path = abs_path[len(self.path)+1:]
                self.DIRS.append(dir_path)
                self._load_path(abs_path)

            else:
                if splits[1] not in self._prompts:
                    continue
                file_path = abs_path[len(self.path)+1:]
                self.DIRS.append(file_path)

    def get_paths(self):
        return self.DIRS

    def match(self, word):
        for d in self.DIRS:
            if word in d:
                return True
        else:
            return False

    def get_match(self, word):
        tmp = [ ]
        for d in self.DIRS:
            if word in d:
                tmp.append(d)

        tmp = sorted(tmp)
        return tmp


if __name__ == "__main__":
    dirs = Dir("/home/cxx/github/DxfAndCxx/sunshine")
    word = "s"
    if dirs.match(word):
        print dirs.get_match(word)

