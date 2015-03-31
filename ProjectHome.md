Extends Python's ConfigParser classes to allow validation of values.

For example, the code below shows how an exception is raised if the integer
value of an option fails validation.
```
>>> import validatingconfigparser
>>> import formencode.validators

>>> parser = validatingconfigparser.ConfigParser()
>>> parser.read('myconfig.ini')

>>> validator = formencode.validators.Int(max=10)

>>> value = parser.get("a_section", "an_option", validator=validator)
Traceback (most recent call last):
    ...
Invalid: Please enter a number that is 10 or smaller
```

The full documentation is available here: https://validatingconfigparser.readthedocs.org/