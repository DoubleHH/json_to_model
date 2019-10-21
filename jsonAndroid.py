#! /usr/bin/python
#coding:utf-8
import json
from sys import argv
import re

classList = {}
gClassName = ""
isShort = 1

COLORS  = {
    "blue": "0;34m",
    "green": "0;32m",
    "cyan": "0;36m",
    "red": "0;31m",
    "purple": "0;35m",
    "brown": "0;33m",
    "yellow": "1;33m",
    "lred": "1;31m",
}

def print_color_string(string, color):
    print ("\033[" + COLORS[color])
    print string
    print '\033[0m'

def capitalize(name, capFirst=True):
    if len(name) == 0 :
        return name
    nameArray = name.split('_')
    result = ""
    index = 0
    for nameTemp in nameArray:
        if not capFirst and index == 0:
            result += nameTemp
        else:
            result += nameTemp.capitalize()
        index += 1
    return result

def composeClassName(prefix, subfixKey):
    global gClassName
    global isShort
    if isShort == 1:
        return (gClassName + capitalize(subfixKey))
    else:
        return (prefix + capitalize(subfixKey))

def simpleTypeName(ktype):
    if ktype == "<type 'int'>" or  ktype == "<type 'float'>":
        return "Int"
    elif ktype == "<type 'bool'>":
        return "bool"
    elif ktype == "<type 'str'>" or ktype == "<type 'unicode'>":
        return "String"
    return None


def iterItem(item, className):
    if not str(type(item)) == "<type 'dict'>" :
        print "item type is: " , type(item)
        return
    for k , v in item.items():
        tempType = str(type(v))
        if tempType == "<type 'list'>":
            if len(v) > 0:
                it = v[0]
                ittype = str(type(it))
                if ittype == "<type 'dict'>":
                    subname = composeClassName(className, listItemClassSuffix(k))
                    iterItem(it, subname)
        elif tempType == "<type 'dict'>":
            subname = composeClassName(className, k)
            iterItem(v, subname)
    printHeader(item, className)

def listItemClassSuffix(key):
    suffix = "item"
    listSuffix = "_list"
    if key.endswith(listSuffix):
        suffix = key[:(len(key) - len(listSuffix))] + "_item"
    elif not key == "list":
        suffix = key + "_item"
    return suffix

def printHeader(item, className):
    t = str(type(item))
    if not  t == "<type 'dict'>" :
        print "error type: " , t
        print "item is  : " , item
        print "className is: " , className
        return None
    global classList
    varlist = {}
    protocols = []
    header = "data class " + className + "Model (\n"
    index = 0
    for k, v in item.items():
        ktype = str(type(v))
        pname = unicode(k)
        propertyPrefix = "    @SerializedName(\"%s\") val %s: " % (pname, capitalize(pname, False))
        if ktype == "<type 'dict'>":
            classType = composeClassName(className, k) + "Model"
            header += propertyPrefix + classType
        elif ktype == "<type 'list'>":
            if len(v) > 0:
                it = v[0]
                t = str(type(it))
                nn = simpleTypeName(t)
                if nn == None:
                    varlist[pname] = composeClassName(className, listItemClassSuffix(k)) + "Model"
                    header += propertyPrefix + "List<%s>" % (varlist[pname])
                else:
                    header += propertyPrefix + "List<%s>" % (nn)
        else:
            header += propertyPrefix + "String"
        note = ("" if (ktype == "<type 'dict'>" or ktype == "<type 'list'>") else (" // %s" % v))
        if index + 1 == len(item):
            header += "?%s\n" % (note)
        else:
            header += "?,%s\n" % (note)
        index += 1
    header += ")"
    print_color_string(header, "lred")
    classList[className] = varlist
    

def make_json(path,className):
    f = file(path)
    j = json.load(f, encoding='utf8')
    f.close()
    entryKeyList = ["data", "result"]
    for key in entryKeyList:
        if key in j and str(type(j[key])) == "<type 'dict'>":
            iterItem(j[key], className)
            return
    iterItem(j, className)

if __name__ == '__main__':
    if len(argv) < 3:
        print "Usage: python jsonmodel_decoder.py data_file_name className\n"
        exit(0)
    gClassName = argv[2]
    if len(argv) == 4 and argv[3] == "-l":
        isShort = 0
    make_json(argv[1], argv[2])
