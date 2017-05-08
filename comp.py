#!/usr/bin/python3
import re
import sys

res=re.search("(.*)m(.*)",sys.argv[1])
min=res.group(1)
sec=res.group(2)
print (60*float(min)+float(sec))



