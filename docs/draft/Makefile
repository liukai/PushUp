DOC=report
.PHONY: view clean

$(DOC).pdf: *.tex *.cls *.bib
	pdflatex $(DOC).tex

view:
	open $(DOC).pdf -a PdfView

clean:
	 rm -f *.dvi *.bbl *.aux *.log *.blg *.toc *.pdf
