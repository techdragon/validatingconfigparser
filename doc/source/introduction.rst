Introduction
============

The `validatingconfigparser` module overrides the classes of
of the `ConfigParser` module Python Standard Library to allow 
validation of values.

- The `RawConfigParser`, `ConfigParser` and `SafeConfigParser` classes
  accept a new `schema` keyword argument, e.g.

  >>> importvalidatingconfigparser
  >>> parser = validatingconfigparser.ConfigParser(schema=my_schema)

- The `set()` and `get()` methods of above classes accept a new `validator`
  keyword argument.

  >>> value = parser.get(section, option, validator=my_validator)
  >>> parser.set(section, option, value, validator=my_validator)

  If no `validator` argument is provided, then either a matching validator
  of the schema will be used, or `value` is used without validation, i.e.
  unchanged.

- The `items()` method of above classes will observe the validation schema
  of the parser.

  >>> parser.schema = my_other_schema
  >>> items = parser.items()

- All other methods remain unchanged. The `getint()`, `getfloat()`
  and `getboolean()` methods do not provide validation beyond their
  original logic of coercing the value into an integer, float or
  boolean type.
