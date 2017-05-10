all:
	./exec.py projet/ > allsource.tex
	split -l 10 --additional-suffix=.tex allsource.tex
	texi2pdf *.tex
	convert xa*.pdf final.pdf
	rm xa*
