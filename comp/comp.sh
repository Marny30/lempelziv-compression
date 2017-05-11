#!/bin/bash
cp ./projet/$1 ./projet/$1.LZ
cp ./projet/$1 ./projet/$1.XZ
cp ./projet/$1 ./projet/$1.BZ
cp ./projet/$1 ./projet/$1.ZIP
cp ./projet/$1 ./projet/$1.HUFF
echo "\documentclass[10pt,a4paper]{article}"
echo "\usepackage{tikz}"
echo "\usepackage{pgfplots}"
echo "\begin{document}"
echo "\begin{tikzpicture}[scale=0.7]"
echo "\begin{axis}[ybar,xticklabels={0,0,lzma,xz,zip,bzip2,huffman}]"

MyLZMA=$({ time lzma -z ./projet/$1.LZ; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyXZ=$({ time xz -z ./projet/$1.XZ; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyBZIP2=$({ time  bzip2 -z ./projet/$1.BZ; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyZIP=$({ time  zip -q -r ./projet/$1.ZIP.zip ./projet/$1.ZIP; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyHUFF=$({ time ./huff/huf ./projet/$i.HUFF ./projet/$1.HUFF.huff; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')

LZMA=$(./comp.py $MyLZMA)
XZ=$(./comp.py $MyXZ)
BZIP2=$(./comp.py $MyBZIP2)
ZIP=$(./comp.py $MyZIP)
HUFF=$(./comp.py $MyHUFF)

echo "\addplot coordinates{(1,"$LZMA")(2,"$XZ")(4,"$BZIP2")(3,"$ZIP")(5,"$HUFF")};"

#SizeLZMA=$(ls projet/ -al|grep $1.LZ.lzma|cut -d " " -f5)
#SizeXZ=$(ls projet/ -al|grep $1.XZ.xz|cut -d " " -f5)
#SizeBZIP2=$(ls projet/ -al|grep $1.BZ.bz2|cut -d " " -f5)
#SizeZIP=$(ls projet/ -al|grep $1.ZIP.zip|cut -d " " -f5)
#echo "\addplot coordinates{(1,"$SizeLZMA")(2,"$SizeXZ")(3,"$SizeBZIP2")(4,"$SizeZIP")(5,0)};"

##decomp
MyunLZMA=$({ time lzma -d ./projet/$1.LZ.lzma; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyunXZ=$({ time xz -d ./projet/$1.XZ.xz; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyunBZIP2=$({ time  bzip2 -d ./projet/$1.BZ.bz2; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyunZIP=$({ time  zip -r ./projet/$1.ZIP ./projet/$1.ZIP.zip; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')
MyunHUFF=$({ time ./huff/dehuf ./projet/$i.HUFF ./projet/$1.HUFF.huff; } 2>&1 | grep real| sed -e 's/real\t//'| sed -e 's/s//')

LZMA=$(./comp.py $MyunLZMA)
XZ=$(./comp.py $MyunXZ)
BZIP2=$(./comp.py $MyunBZIP2)
ZIP=$(./comp.py $MyunZIP)
HUFF=$(./comp.py $MyunHUFF)



echo "\end{axis}"
echo "\end{tikzpicture}"
echo "\begin{tikzpicture}[scale=0.7]"
echo "\begin{axis}[ybar,xticklabels={0,0,lzma,xz,zip,bzip2,huffman}]"
echo "\addplot coordinates{(1,"$LZMA")(2,"$XZ")(4,"$BZIP2")(3,"$ZIP")(5,"$HUFF")};"
echo "\end{axis}"
echo "\end{tikzpicture}"
echo "temps de compression et de decompression de "$1"en secondes "
echo "\end{document}"


rm ./projet/*.lzma ./projet/*.xz ./projet/*.bz2 ./projet/*ZIP* ./projet/*HUFF* ./projet/*BZ* ./projet/*LZ* ./projet/*XZ* 
