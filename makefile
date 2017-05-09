all:
	./exec.py projet/ > allsource.tex
	split -l 11 --additional-suffix=.tex allsource.tex
	texi2pdf *.tex
	pdftk xa*.pdf cat output final.pdf
	rm xa*
