#!/bin/bash
cp ./projet/$1 ./projet/$1.LZ
cp ./projet/$1 ./projet/$1.XZ
cp ./projet/$1 ./projet/$1.BZ
cp ./projet/$1 ./projet/$1.ZIP
echo "\documentclass[10pt,a4paper]{article}"
echo "\usepackage{tikz}"
echo "\usepackage{pgfplots}"
echo "\begin{document}"
echo "\begin{tikzpicture}[scale=0.7]"
echo "\begin{axis}[ybar,xticklabels={0,0,lzma,xz,bzip2,zip,huffman}]"

MyLZMA=$({ time lzma -z ./projet/$1.LZ; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyXZ=$({ time xz -z ./projet/$1.XZ; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyBZIP2=$({ time  bzip2 -z ./projet/$1.BZ; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyZIP=$({ time  zip -q -r ./projet/$1.ZIP.zip ./projet/$1.ZIP; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')

LZMA=$(./comp.py $MyLZMA)
XZ=$(./comp.py $MyXZ)
BZIP2=$(./comp.py $MyBZIP2)
ZIP=$(./comp.py $MyZIP)

echo "\addplot coordinates{(1,"$LZMA")(2,"$XZ")(3,"$BZIP2")(4,"$ZIP")(5,0)};"

SizeLZMA=$(ls projet/ -al|grep $1.LZ.lzma|cut -d " " -f5)
SizeXZ=$(ls projet/ -al|grep $1.XZ.xz|cut -d " " -f5)
SizeBZIP2=$(ls projet/ -al|grep $1.BZ.bz2|cut -d " " -f5)
SizeZIP=$(ls projet/ -al|grep $1.ZIP.zip|cut -d " " -f5)
echo "\addplot coordinates{(1,"$SizeLZMA")(2,"$SizeXZ")(3,"$SizeBZIP2")(4,"$SizeZIP")(5,0)};"

echo "\end{axis}"
echo "\end{tikzpicture}"
echo "\end{document}"


rm ./projet/*.lzma ./projet/*.xz ./projet/*.bz2 ./projet/*ZIP*
