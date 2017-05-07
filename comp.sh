#!/bin/bash
cp ./projet/$1.c ./projet/$1.LZ.c
cp ./projet/$1.c ./projet/$1.XZ.c
cp ./projet/$1.c ./projet/$1.BZ.c
cp ./projet/$1.c ./projet/$1.ZIP.c
echo "\documentclass[10pt,a4paper]{article}"
echo "\usepackage{tikz}"
echo "\usepackage{pgfplots}"
echo "\begin{document}"
echo "\begin{tikzpicture}[scale=0.7]"
echo "\begin{axis}[ybar,xticklabels={0,0,lzma,xz,bzip2,zip,huffman}]"

MyLZMA=$({ time lzma -z ./projet/$1.LZ.c; } 2>&1 | grep real| sed -e 's/real\t0m//'| sed -e 's/s//')
MyXZ=$({ time xz -z ./projet/$1.XZ.c; } 2>&1 | grep real| sed -e 's/real\t0m//'| sed -e 's/s//')
MyBZIP2=$({ time  bzip2 -z ./projet/$1.BZ.c; } 2>&1 | grep real| sed -e 's/real\t0m//'| sed -e 's/s//')
MyZIP=$({ time  zip -q -r ./projet/$1.ZIP.c.zip ./projet/$1.ZIP.c; } 2>&1 | grep real| sed -e 's/real\t0m//'| sed -e 's/s//')
echo "\addplot coordinates{(1,"$MyLZMA")(2,"$MyXZ")(3,"$MyBZIP2")(4,"$MyZIP")(5,0.025)};"

echo "\end{axis}"
echo "\end{tikzpicture}"
echo "\end{document}"


rm ./projet/*.lzma ./projet/*.xz ./projet/*.bz2 ./projet/*ZIP*
