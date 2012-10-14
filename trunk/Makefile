

help:
	@echo "make test       - Run all tests"
	@echo "make coverage   - Run test and report coverage"
	@echo "make bdist      - Run 'setup.py bdist'"
	@echo "make sdist      - Run 'setup.py sdist'"
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


FORCE:
