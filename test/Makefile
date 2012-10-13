
NOSETESTS := nosetests -v --stop --pdb --pdb-failures


all: test_configparser_standard \
     test_configparser_validating \
     test_validating_configparser


# Run the Python Standard Library test suite against the
# `ConfigParser` of the Python Standard Library. This is simply 
# to verify that there is nothing wrong with the original
# test suite and module.
#
# The test suite as been extended by an additional test 
# which must be excluded here as it is specific to the
# `validatingconfigparser`.
#
test_configparser_standard:
	$(NOSETESTS) test_cfgparser_standard.py


# Run the Python Standard Library test suite against the
# `validatingconfigparser` module as this module is meant
# to be API compatible with the `ConfigParser` module.
#
# Running this requires some tweaking so the the test suite
# imports a different module
#
test_configparser_validating:
	PYTHONPATH=../validatingconfigparser $(NOSETESTS) test_cfgparser_validating.py


# Run specific tests for the `validatingconfigparser`
# module.
#
test_validating_configparser:
	PYTHONPATH=../validatingconfigparser $(NOSETESTS) test_validatingcfgparser.py


#reset_ConfigParser:
#	-rm -fv ConfigParser.py
#
#fake_ConfigParser: reset_ConfigParser
#	ln -sv ../validatingconfigparser/validatingconfigparser.py ConfigParser.py
	
