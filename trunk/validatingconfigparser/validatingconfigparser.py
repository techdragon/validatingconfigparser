
"""
    Extend Python's ConfigParser classes to allow validation of values.
    
    - The the `RawConfigParser`, `ConfigParser` and `SafeConfigParser` classes
      now accept a new `schema` keyword argument, e.g.
      
      >>> parser = ConfigParser(schema=my_schema)
    
    - The `set()` and `get()` methods of above classes accept a new `validator` 
      keyword argument.
      
      >>> value = parser.get(section, option, validator=my_validator)
      >>> parser.set(section, option, value, validator=my_validator)

      If no `validator` argument is provided, then either a matching validator 
      of the schema will be used or `value` will be used as is.
      
    - The `items()` method of above classes will observe the validation schema
      of the parser.

      >>> parser.schema = my_other_schema
      >>> items = parser.items()
      
    - All other methods remain unchanged. The `getint()`, `getfloat()`
      and `getboolean()` methods do not provide validation beyond their
      original logic of coercing the value into an integer, float or
      boolean type. If validation of such values is required one has to 
      use the `get()` method with a suitable validator instead, e.g.

      >>> from formencode.validators import Int, 
      >>> parser.get(section, option, validator=Int())
      
    Schemas and validators must follow the same API as their counterparts
    of the `Formencode` package. The `validatingconfigparser` package
    was explicitely designed so that the classes provided by `Formencode`
    can be used as is.     
   
"""

__author__ = "Markus Juenemann"
__license__ = "Apache License 2.0"
__revision__ = "$Rev:$"


# Import the parser classes from ConfigParser into the local namespace, 
# but ensure that the ConfigParser, SafeConfigParser and RawConfigParser
# classes are available under a different name as they are being
# overwritten by this module.
#
from ConfigParser import ConfigParser as _ConfigParser
from ConfigParser import SafeConfigParser as _SafeConfigParser
from ConfigParser import RawConfigParser as _RawConfigParser

# The Validator base class always returns the original value unchanged.
# This makes it useful as a "dummy" default validator.
#
from formencode.api import Validator


class ValidatingMixIn(object):
    """
    Provides the validating variants of `get()`, `set()` and `items()` methods.

    """

    def __init__(self, *args, **kwargs):
        try:
            self.schema = kwargs.pop("schema")
        except KeyError:
            self.schema = None  

        # Find my parent class. This is one of
        # * _RawConfigParser
        # * _ConfigParser
        # * _SafeConfigParser
        # 
        # IMPORTANT The code below must be separate ``if`` statements
        #    and not an ``if/elif`` construct. Also the ``if`` statements
        #    must appear in the exact order. Don't change the code below.
            
        if isinstance(self, _RawConfigParser):
            self.parent = _RawConfigParser
        
        if isinstance(self, ConfigParser):
            self.parent = _ConfigParser
        
        if isinstance(self, _SafeConfigParser):
            self.parent = _SafeConfigParser
            
        self.parent.__init__(self, *args, **kwargs)


    def find_validator(self, section, option):
        """
        Find a validator for option in section.
        
        The returned validator will be
        - a validator for `option` if there is one in the schema, or
        - a dummy validator. 
         
        """
        
        try:
            return self.schema.fields[option]
        except (KeyError, AttributeError):
            return Validator()
        
        
    def get(self, section, option, validator=None, *args, **kwargs):
        """
        Add `validator` keyword argument to parent's `get()` method.
        
        Parent will be one of `ConfigParser.RawConfigParser`, `ConfigParser.ConfigParser`
        or ``ConfigParser.SafeConfigParser`.  
                
        With the exception of `validator` all arguments (`section`, `option`, `*args` and
        `**kwargs`) will be passed on to the parent's `get()` method. The parent method 
        will raise exception if it receives an argument that it does not support.    

        Validation will be performed on the string value returned by the parent's `get()`
        method.
        
        """
        
        if validator is None:
            validator = self.find_validator(section, option)
          
        return validator.to_python(self.parent.get(self, section, option, 
                                                   *args, **kwargs))
    

    def set(self, section, option, value, validator=None, *args, **kwargs):
        """
        Add `validator` keyword argument to parent's `set()` method.
    
        Parent will be one of `ConfigParser.RawConfigParser`, `ConfigParser.ConfigParser`
        or ``ConfigParser.SafeConfigParser`.  
                
        With the exception of `validator` all arguments (`section`, `option`, `*args` and
        `**kwargs`) will be passed on to the parent's `getboolean()` method. The parent method 
        will raise an exception if it receives an argument that it does not support.
        
        Validation will be performed *before* the parent's `set()` method is being called.  
        
        """
        
        if validator is None:
            validator = self.find_validator(section, option)
        
        self.parent.set(self, section, option, validator.from_python(value), 
                        *args, **kwargs)


    def items(self, section, *args, **kwargs):
        """
        Extend parent's `items()` method to validate every returned option against a schema.
        
        Schema refers to the value of the `schema` attribute which can be given as an argument
        to the `__init__()` method or set later. If no schema is available the items will be
        returned as is. The same applies to individual values if there is no matching
        validator in the schema.
         
        """
        
        items = self.parent.items(self, section, *args, **kwargs)
        
        if self.schema is None:
            return items
        else:
            validated_items = []
            for (option, value) in items:
                
                # Find a matching validator for this `option` in `self.schema` 
                # or return the default validator which simply returns the 
                # `value` unchanged.
                #
                validator = self.find_validator(section, option)
                
                # Validate the `value` and add it to the dictionary of validated
                # items.
                #
                validated_value = validator.to_python(value)
                validated_items.append((option, validated_value))
                
            return validated_items
                 
        
class RawConfigParser(ValidatingMixIn, _RawConfigParser): pass


class ConfigParser(ValidatingMixIn, _ConfigParser): pass


class SafeConfigParser(ValidatingMixIn, _SafeConfigParser): pass
