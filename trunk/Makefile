

help:
	@echo "make test       - Run all tests"
	@echo "make coverage   - Run test and report coverage"
	@echo "make bdist      - Run 'setup.py bdist'"
	@echo "make sdist      - Run 'setup.py sdist'"
	@echo "make doc        - Create documentation"
	@echo "make all        - test + bdist + sdist"


all: test bdist sdist


test: FORCE
	make -C test test

coverage: FORCE
	make -C test coverage

bdist: FORCE
	python setup.py bdist

sdist: FORCE
	python setup.py sdist

#----------------------------------------------------------
#
# Documentation
#
doc: doc_html doc_pdf doc_epub

doc_html: doc_pickle
	make -C doc html

doc_pdf: doc_pickle
	make -C doc latexpdf

doc_epub: doc_pickle
	make -C doc epub

doc_pickle:
	make -C doc pickle



FORCE:
