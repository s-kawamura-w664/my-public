#!/usr/bin/env python3

import os
import sys

mod_check = 0

##################################################
def main():
    global mod_check

    args = sys.argv
    if (len(args) < 3):
        print("Usage: ./check-weight.py <dir1> <dir1> [-c] [-g]")
        print("")
        print("ex: ./check-weight.py ./website/content/en ./website/content/ja")
        sys.exit(1)

    dirpath1 = args[1]
    dirpath2 = args[2]

    if (len(args) >= 4):
        if args[3] == "-c":
            mod_check = 1
        elif args[3] == "-g":
            mod_check = 2

    fullpath1 = os.path.abspath(dirpath1)
    fullpath2 = os.path.abspath(dirpath2)

    if (os.path.isdir(fullpath1) is not True):
        print("Directory not found. {}".format(fullpath1))
        sys.exit(1)
    if (os.path.isdir(fullpath2) is not True):
        print("Directory not found. {}".format(fullpath2))
        sys.exit(1)

    check_dir(fullpath1, fullpath2, fullpath1, ".md")

##################################################
def check_dir(dirpath1, dirpath2, curpath, ext):
    dict_dir = dict()
    dict_file = dict()
    dict_file2 = dict()
    
    #dirpath1から辿ったディレクトリのファイル一覧を取得
    dict_file, dict_dir = get_filelist(curpath, ext)
    
    #dirpath2の関連するディレクトリのファイル一覧を取得
    #  以下の処理が古いPython3だと使えないため書き換えた
    #  dirname2 = curpath.removeprefix(dirpath1).lstrip("/\\")
    if curpath.startswith(dirpath1):
        dirname2 = curpath[len(dirpath1):]
        dirname2 = dirname2.lstrip("/\\")
    else:
        dirname2 = curpath
    dirname2 = os.path.join(dirpath2, dirname2)
    dict_file2, _ = get_filelist(dirname2, ext)
    
    reslist = []
    #dirpath1とdirpath2のファイル一覧を比較する
    if mod_check == 0:
        print("##{}".format(curpath))
        compare_weight(curpath, dirname2, dict_file, dict_file2, reslist)
    elif mod_check == 1:
        result = compare_weight(curpath, dirname2, dict_file, dict_file2, reslist)
        if result > 0:
            print("##{:100} (count={})".format(curpath, result))
    elif mod_check == 2:
        result = compare_weight(curpath, dirname2, dict_file, dict_file2, reslist)
        if result > 0:
            print("##{:100} (count={})".format(curpath, result))
            for message in reslist:
                print(message)

    for d,_ in sorted(dict_dir.items()):
        fullpath = os.path.join(curpath, d)
        check_dir(dirpath1, dirpath2, fullpath, ext)

##################################################
def compare_weight(dirpath1, dirpath2, dict_file1, dict_file2, reslist):
    result = 0  #同じ
    for filename1,_ in sorted(dict_file1.items()):            #dir1の対象を全ループ
        w1 = get_weight(os.path.join(dirpath1, filename1))     #file1のweight取得
        if filename1 in dict_file2:         #dir2の中にファイルがあるかどうか
            w2 = get_weight(os.path.join(dirpath2, filename1))     #file2のweight取得
            message = print_compare(filename1, filename1, w1, w2)
            reslist.append(message)
            if w1 != w2:
                result = result + 1  #差異あり
            del dict_file2[filename1]
        else:
            message = print_compare(filename1, "--", w1, "")
            reslist.append(message)

    if len(dict_file2) > 0:
        for filename2,_ in sorted(dict_file2.items()):
            w2 = get_weight(os.path.join(dirpath2, filename2))     #file2のweight取得
            message = print_compare("--", filename2, "", w2)
            reslist.append(message)

    return result

##################################################
def print_compare(fname1, fname2, weight1, weight2):
    message = "   {:80}   {:80}  [{:>3}][{:>3}]".format(fname1, fname2, weight1, weight2)
    if mod_check == 0:
        print(message)
    return message

##################################################
def get_weight(path):
    line = 0
    with open(path, encoding='utf-8') as f:
        while True:
            str = f.readline()              # 1行読み込み
            if(str == ""):
                break
            if "weight" in str == False:    # weightが無い場合
                break
            tokens = str.split(":")         # トークン分割
            if len(tokens) <= 1:
                continue
            if tokens[0] == "weight":       # キー名が"weight"だったら
                value = tokens[1].strip()
                tokens2 = value.split("#")              # コメント文があったら削除する
                return tokens2[0].strip()
    return ""

##################################################
def get_filelist(path, ext):
    dict_file = dict()
    dict_dir = dict()
    if (os.path.isdir(path) is not True):
        return dict_file, dict_dir

    for f in os.listdir(path):
        if(f[0] == "."):
            continue
        fullpath = os.path.join(path, f)
        if(os.path.isdir(fullpath)):
            dict_dir[f] = ""
            continue
        exts = os.path.splitext(f)
        if(exts[1] != ext):
            continue
        dict_file[f] = ""

    return dict_file, dict_dir

##################################################
def check_ctrlcode(filepath):
    line = 0
    with open(filepath, encoding='utf-8') as f:
        while True:
            str = f.readline()
            if(str == ""):
                break
            line = line + 1
            
            ignore = False
            italic = 0
            isMultiCode = False
            for ch in str:
            	if(ignore == False):
	            	if(ch == '_'):
	            		italic = italic + 1
	            		if(italic == 2):
	            			break
            		
            	if(ch == '<'):	# Skip lapped strings
            		ignore=True
            		italic=0
            		
            	if(ch == '>'):
            		ignore=False
            	if(ord(ch) >= 256):
            		isMultiCode=True
            
            if(italic < 2):
            	continue
            	
            if(isMultiCode == False):
            	continue
            
            print("{0} <L{1}>: {2}".format(filepath, line, str.replace('\n','')))
            

main()
