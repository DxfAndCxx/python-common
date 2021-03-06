#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-06-26 11:50:40
# @Author  : 陈小雪 (shell_chen@yeah.net)
# @Link    :
# @Version : $Id$

import os
import urllib
import urllib2
import time
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f", dest="filename",help="publish article filename", required = True)
parser.add_argument("-p", help = "is publish?", default = False)
parser.add_argument("-t", dest="title", help = "article title", default = int(time.time()))
parser.add_argument("-c", dest="cls", help="article class", default="未分类")
parser.add_argument("-tags", dest="tags", help="article tags",default="其他")

args = parser.parse_args()

def requset(title, cls, tags, context, publish):
    url = "http://127.0.0.1:8001/blog/add/"
    values = {
        "title" : title,
        "tags" : tags,
        "cls" :  cls,
        "context": context,
        "publish": publish
        }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

def start():
    filename = args.filename
    if not os.path.isfile(filename):
        print "file : %s is not a file"%filename
        return
    context = " "
    with open(filename) as fp:
        context = fp.read()
    requset(args.title, args.cls, args.tags, context, args.publish)

if __name__ == "__main__":
    start()

