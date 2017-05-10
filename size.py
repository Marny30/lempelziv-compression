#!/usr/bin/python3
import re
import sys
i=0
for line in sys.stdin:
	if(i==0):
		i=1
	else:
		res=re.search(".* guilhem guilhem *([0-9]*) ",line)
		
		sec=res.group(1)
		print (sec)



