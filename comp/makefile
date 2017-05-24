all:
	./exec.py projet/ > allsource.tex
	split -l 16 --additional-suffix=.tex allsource.tex
	texi2pdf *.tex
	convert -quality 100 -density 150 xa*.pdf final.pdf
	rm x*
