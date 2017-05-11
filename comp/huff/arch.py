#!/usr/bin/env python3
import os,sys

def archive(repertoire):
    os.system("cat ./"+repertoire+"/* > "+repertoire+".arch")
    os.system("./huf "+repertoire+".arch "+repertoire+".arch.archuff")
    os.system("rm "+repertoire+".arch")



archive(sys.argv[1])
