all:
	./exec.py projet/ > allsource.tex
	split -l 11 --additional-suffix=.tex allsource.tex
	texi2pdf *.tex
