
"""
    Extend Python's ConfigParser classes to allow validation of values.

.. warning:: 

    The classes in the `ConfigParser` module of the Python Standard library are
    old-style classes (http://bugs.python.org/issue5807), i.e. they don't inherit
    from `object`. In contrast the classes in this module are new style classes.
   
"""

__author__ = "Markus Juenemann"
__license__ = "Apache License 2.0"
__revision__ = "$Rev:$"


# Import everything from ConfigParser into the local namespace, but
# ensure that the ConfigParser, SafeConfigParser and RawConfigParser
# classes are available under a different name as they are being
# overwritten by this module.
#
from ConfigParser import *
from ConfigParser import ConfigParser as _ConfigParser
from ConfigParser import SafeConfigParser as _SafeConfigParser
from ConfigParser import RawConfigParser as _RawConfigParser
#from ConfigParser import _default_dict

import formencode.validators
import formencode.schema


class DummySchema(formencode.schema.Schema):
    def __init__(self, *args, **kwargs):
        super(DummySchema, self).__init__(allow_extra_fields=True, *args, **kwargs)


class DummyValidator(formencode.validators.FancyValidator):
    """
    Base class for derived validators.

    TODO: Rewrite this __doc__
    
    `Validator` is loosely modelled after the `formencode.api.FancyValidator` class.
    It provides two methods, `to_python()` and `from_python()`. The `to_python()`
    method is called by the `get\*()` methods of a configuration parser to convert and validate 
    a value before it is returned to the caller. The `from_python()` method is called by the 
    `set()` method to validate and convert a value before it is written to a configuration file. 
    Logically this looks like this:
    
    ::
    
      to_python(get(...))  
      to_python(getint(...))
      to_python(getfloat(...))
      to_python(getboolean(...))
      
      set(..., from_python(value))
      
    The `Validator` base class does actually not perform any validation at all. It is expected that
    any derived classes override the `_to_python()` and `_from_python()` (note the leading
    underscore!) methods and perform any validations within these methods. If validations is 
    successful `_to_python()` and `_from_python()` must return the validated value. Both methods
    may convert or format the value as they deem necessary. Care must be taken that the value
    returned by `_from_python()` can be converted to a string so that it can be written to the
    configuration file.  
    
    In contrast to `formencode.api.FancyValidator` the `Validator` class of this module
    does neither provide `validate_python()` and `validate_others()` methods nor does its
    `__init__()` method accept any arguments.
    
    """
    
    def _to_python(self, value, state):
        """
        Called by `to_python()` to validate and convert `value`.
        
        :param value: The value to be validated and converted.
        
        `_to_python` should be overwritten by derived classes as the default
        simply returns the original `value`.
        
        """

        return value
        
    def _from_python(self, value, state):
        """
        Called by `from_python()` to validate and convert `value`.
        
        :param value: The value to be validated and converted.
        
        `_from_python` should be overwritten by derived classes as the default
        simply returns the original `value`.
        
        """
        
        return value
    

class ValidatingMixIn(object):
    def __init__(self, *args, **kwargs):
        try:
            self.schema = kwargs.pop("schema")
        except KeyError:
            self.schema = None  #DummySchema()

        """
        Find my parent class. This is one of
        * _RawConfigParser
        * _ConfigParser
        * _SafeConfigParser
        
        .. important:: The code below must be separate ``if`` statements
            and not an ``if/elif`` construct. Also the ``if`` statements
            must appear in the exact order.
            
        """            
        
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
            return DummyValidator()
        
        
    def get(self, section, option, validator=None, *args, **kwargs):
        """
        Add `validator` keyword argument to parent's `get()` method.
        
        Parent will be one of `ConfigParser.RawConfigParser`, `ConfigParser.ConfigParser`
        or ``ConfigParser.SafeConfigParser`.  
                
        With the exception of `validator` all arguments (`section`, `option`, `*args` and
        `**kwargs`) will be passed on to the parent's `get()` method. The parent method 
        will raise ``TypeError`` if it receives an argument that it does not support.    
        
        """
        
        if validator is None:
            validator = self.find_validator(section, option)
          
        return validator.to_python(self.parent.get(self, section, option, 
                                                   *args, **kwargs))
    
    
    def getint(self, section, option, validator=None, *args, **kwargs):
        """
        Add `validator` keyword argument to parent's `getint()` method.
        
        Parent will be one of `ConfigParser.RawConfigParser`, `ConfigParser.ConfigParser`
        or ``ConfigParser.SafeConfigParser`.  
                
        With the exception of `validator` all arguments (`section`, `option`, `*args` and
        `**kwargs`) will be passed on to the parent's `getint()` method. The parent method 
        will raise ``TypeError`` if it receives an argument that it does not support.  
        
        Validation will be performed on the value that is returned by the parent's
        `getint()` method.   
        
        """
        
        if validator is None:
            validator = self.find_validator(section, option)
        
        return validator.to_python(self.parent.getint(self, section, option, 
                                                      *args, **kwargs))
    
    
    def getfloat(self, section, option, validator=None, *args, **kwargs):
        """
        Add `validator` keyword argument to parent's `getfloat()` method.
        
        Parent will be one of `ConfigParser.RawConfigParser`, `ConfigParser.ConfigParser`
        or ``ConfigParser.SafeConfigParser`.  
                
        With the exception of `validator` all arguments (`section`, `option`, `*args` and
        `**kwargs`) will be passed on to the parent's `getfloat()` method. The parent method 
        will raise ``TypeError`` if it receives an argument that it does not support.
        
        Validation will be performed on the value that is returned by the parent's
        `getfloat()` method.   
        
        """
        
        if validator is None:
            validator = self.find_validator(section, option)
        
        return validator.to_python(self.parent.getfloat(self, section, option, 
                                                        *args, **kwargs))
    
    
    def getboolean(self, section, option, validator=None, *args, **kwargs):
        """
        Add `validator` keyword argument to parent's `getboolean()` method.
        
        Parent will be one of `ConfigParser.RawConfigParser`, `ConfigParser.ConfigParser`
        or ``ConfigParser.SafeConfigParser`.  
                
        With the exception of `validator` all arguments (`section`, `option`, `*args` and
        `**kwargs`) will be passed on to the parent's `getboolean()` method. The parent method 
        will raise ``TypeError`` if it receives an argument that it does not support.
        
        Validation will be performed on the value that is returned by the parent's
        `getboolean()` method.   
        
        """
        
        if validator is None:
            validator = self.find_validator(section, option)
        
        return validator.to_python(self.parent.getboolean(self, section, option, 
                                                          *args, **kwargs))
    

    def set(self, section, option, value, validator=None, *args, **kwargs):
        """
        Add `validator` keyword argument to parent's `set()` method.
    
        Parent will be one of `ConfigParser.RawConfigParser`, `ConfigParser.ConfigParser`
        or ``ConfigParser.SafeConfigParser`.  
                
        With the exception of `validator` all arguments (`section`, `option`, `*args` and
        `**kwargs`) will be passed on to the parent's `getboolean()` method. The parent method 
        will raise ``TypeError`` if it receives an argument that it does not support.
        
        Validation will be performed *before* the parent's `set()` method is being called.  
        
        """
        
        if validator is None:
            # Find a matching validator for this `option` in `self.schema` or
            # return the default validator which simply returns the `value`
            # unchanged.
            #
            validator = getattr(self.schema, option, DummyValidator())
        
        self.parent.set(self, section, option, validator.from_python(value), 
                        *args, **kwargs)


    def items(self, section, *args, **kwargs):
        """
        Extend parent's `items()` method to validate every returned option against a schema.
        
        Schema refers to the value of the `schema` attribute which can be given as an argument
        to the `__init__()` method or set later. If no schema is available 
         
        """
        
        items = self.parent.items(self, section, *args, **kwargs)
        
        if self.schema is None:
            return items
        else:
            # TODO: change items dictionary inline instad of copying
            #       all entries to validated_items.
            validated_items = dict()
            
            for (option, value) in items:
                
                # Find a matching validator for this `option` in `self.schema` 
                # or return the default validator which simply returns the 
                # `value` unchanged.
                #
                validator = getattr(self.schema, option, DummyValidator())
                
                # Validate the `value` and add it to the dictionary of validated
                # items.
                #
                validated_items[option] = validator.to_python(value)
                
            return validated_items
                 
        
class RawConfigParser(ValidatingMixIn, _RawConfigParser): pass


class ConfigParser(ValidatingMixIn, _ConfigParser): pass


class SafeConfigParser(ValidatingMixIn, _SafeConfigParser): pass
