#!/usr/bin/env python3
import os,sys,re

def parcour(repertoire, prof):
    liste=os.listdir(repertoire)
    for fichier in liste:
        cmd="./comp.sh "+fichier    
        os.system(cmd)         


parcour(sys.argv[1],0)
