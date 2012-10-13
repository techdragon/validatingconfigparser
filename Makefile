

help:
	@echo "make test	- Run all tests"
	@echo "make bdist	- Run 'setup.py bdist'"
	@echo "make sdist	- Run 'setup.py sdist'"
	@echo "make all		- test + bdist + sdist"


all: test bdist sdist


test: FORCE
	make -C test test

bdist: FORCE
	python setup.py bdist

sdist: FORCE
	python setup.py sdist


FORCE:
