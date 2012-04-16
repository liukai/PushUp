DOC=report
.PHONY: view clean

$(DOC).pdf: $(DOC).dvi
	dvipdf $(DOC).dvi

$(DOC).dvi: *.tex *.cls *.bib
	latex $(DOC).tex
	bibtex $(DOC)
	latex $(DOC).tex

view:
	open $(DOC).pdf -a pdfview

clean:
	rm -f *.dvi *.bbl *.aux *.log *.blg *.toc *.pdf
