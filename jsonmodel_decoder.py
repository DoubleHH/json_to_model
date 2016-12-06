#! /usr/bin/python
import json
from sys import argv

classList = {}
gClassName = ""
isShort = 1

def capitalize(name):
    if len(name) == 0 :
        return name
    nameArray = name.split('_')
    result = ""
    for nameTemp in nameArray:
        result = result + nameTemp.capitalize()
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
        return "NSNumber"
    elif ktype == "<type 'bool'>":
        return "BOOL"
    elif ktype == "<type 'str'>" or ktype == "<type 'unicode'>":
        return "NSString"
    return None


def iterItem(item,className):

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
                    subname = composeClassName(className, k)
                    iterItem(it, subname)

        elif tempType == "<type 'dict'>":
            subname = composeClassName(className, k)
            iterItem(v,subname)

    printHeader(item,className)

def printHeader(item,className):

    t = str(type(item))
    if not  t == "<type 'dict'>" :
        print "error type: " , t
        print "item is  : " , item
        print "className is: " , className
        return None

    global classList
    varlist = {}
    print "@interface " , className + "Model" , " : JSONModel \n"

    for k , v in item.items():
        ktype = str(type(v))
        pname = k

        if ktype == "<type 'int'>" or  ktype == "<type 'float'>":
            print "@property (nonatomic, strong) NSNumber *%s;" %  pname
        elif ktype == "<type 'bool'>":
            print "@property (nonatomic, assign) BOOL %s;" % pname
        elif ktype == "<type 'str'>" or ktype == "<type 'unicode'>":
            print "@property (nonatomic, strong) NSString *%s;" % pname
        elif ktype == "<type 'dict'>":
            classType = composeClassName(className, k) + "Model"
            print "@property (nonatomic, strong) %s *%s ;  " % (classType, pname)
        elif ktype == "<type 'list'>":
            if len(v) > 0:
                it = v[0]
                t = str(type(it))
                nn = simpleTypeName(t)
                if nn == None :
                    varlist[pname] = composeClassName(className, k) + "Model"
                    print "@property (nonatomic, strong) NSArray<%s> *%s;" % (varlist[pname], pname)
                else:
                    print "@property (nonatomic, strong) NSArray *%s;" % (pname)
        else:
            #print "type is: " , ktype , "for key : " , pname
            print "@property (nonatomic)         typename<Optional>* %s;" % pname

    classList[className] = varlist
    print "\n@end\n\n"

def printImplemention(className , mapKeys):
    print "@implementation ",className+"Model\n"
    if mapKeys != None and len(mapKeys) > 0:
        print "+ (NSDictionary *)modelContainerPropertyGenericClass"
        print "{"
        print "    return @{\n",
        value = ""
        for k,v in mapKeys.items():
            value += "        @\"%s\": [%s class],\n" % (k,v)
        print value,
        print "    };"
        print "}\n"

    print "+ (BOOL)propertyIsOptional:(NSString *)propertyName"
    print "{"
    print "    return YES;"
    print "}\n"

    print "@end\n\n"

def makeJson(path,className):

    f = file(path)
    j = json.load(f,encoding='utf8')
    f.close()

    iterItem(j,className)


    print "\n\n\n\n"
    print "//for implementation"
    for k , v in classList.items():
        printImplemention(k,v)



if __name__ == '__main__':

    if len(argv) < 3:
        print "Usage: python json_decoder.py data_file_name className\n"
        exit(0)
    gClassName = argv[2]
    if len(argv) == 4 and argv[3] == "-l":
        isShort = 0
    makeJson(argv[1], argv[2])
