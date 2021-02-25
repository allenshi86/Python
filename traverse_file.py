#!/usr/bin/env python3

import os


def convert_encoding(file,from_encoding='gbk',to_encoding='utf8'):
    try:
        with open(file,'r',encoding=from_encoding) as f:
            filedata = f.readlines()
        with open(file,'w',encoding=to_encoding) as f:
            f.writelines(filedata)
    except Exception as e:
        print(e)


def listfile(path):
    if os.path.isdir(path):
        files = os.listdir(path)
        for filename in files:
            filepath = os.path.join(path,filename)
            if os.path.isdir(filepath):
               listfile(filepath)
            else:
                if filename.endswith('.sh'):
                    print(filepath)
                    convert_encoding(filepath)

    else:
        print("%s is not a filepath!" %path)

if __name__ == '__main__':
    fpath = input("请输入您的目录路径:")
    listfile(fpath)
