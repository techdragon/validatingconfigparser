


from types import *

import validatingconfigparser
from formencode.validators import *
from formencode import *
import formencode.schema

from nose.tools import *


class Schema(formencode.schema.Schema):
    integer_good = Int()
    integer_too_small = Int(min=1)
    integer_too_big = Int(max=10)
    bool_zero = Bool()
    bool_one = Bool()
    stringbool_true = StringBool()
    stringbool_false = StringBool()
    stringbool_yes = StringBool()
    stringbool_no = StringBool()
    number_int_good = Number()
    number_int_too_small = Number(min=5)
    number_int_too_big = Number(max=50)
    number_float_good = Number()
    number_float_too_small = Number(min=5.0)
    number_float_too_big = Number(max=50.0)



class RawConfigParserWithoutSchema():
    def setup(self):
        self.parser = validatingconfigparser.RawConfigParser()
        self.parser.read("validatingcfgparser.1")
        
class ConfigParserWithoutSchema():
    def setup(self):
        self.parser = validatingconfigparser.ConfigParser()
        self.parser.read("validatingcfgparser.1")
        
class SafeConfigParserWithoutSchema():
    def setup(self):
        self.parser = validatingconfigparser.SafeConfigParser()
        self.parser.read("validatingcfgparser.1")

class RawConfigParserWithSchema():
    def setup(self):
        self.parser = validatingconfigparser.RawConfigParser(schema=Schema(allow_extra_fields=True))
        self.parser.read("validatingcfgparser.1")

class ConfigParserWithSchema():
    def setup(self):
        self.parser = validatingconfigparser.ConfigParser(schema=Schema(allow_extra_fields=True))
        self.parser.read("validatingcfgparser.1")
        
class SafeConfigParserWithSchema():
    def setup(self):
        self.parser = validatingconfigparser.SafeConfigParser(schema=Schema(allow_extra_fields=True))
        self.parser.read("validatingcfgparser.1")
        

class IntTests():
    def test_get_Int(self):
        if self.parser.schema is None:
            validator = Int()
            assert self.parser.get("firstsection", "integer_good", validator) == 1
        else:
            assert self.parser.get("firstsection", "integer_good") == 1
        
    @raises(Invalid)
    def test_get_Int_too_small(self):
        if self.parser.schema is None:
            validator = Int(min=1)
            self.parser.get("firstsection", "integer_too_small", validator)
        else:
            self.parser.get("firstsection", "integer_too_small")
        
    @raises(Invalid)
    def test_get_Int_too_big(self):
        if self.parser.schema is None:
            validator = Int(max=10)
            self.parser.get("firstsection", "integer_too_big", validator) == 1
        else:
            self.parser.get("firstsection", "integer_too_big") == 1
    
class BoolTests():
    def test_get_Bool_zero(self):
        # The string '0' is interpreted as True!
        if self.parser.schema is None:
            validator = Bool()
            assert self.parser.get("firstsection", "bool_zero", validator) is True
        else:
            assert self.parser.get("firstsection", "bool_zero") is True

    def test_get_Bool_one(self):
        if self.parser.schema is None:
            validator = Bool()
            assert self.parser.get("firstsection", "bool_one", validator) is True
        else:
            assert self.parser.get("firstsection", "bool_one") is True

class StringBoolTests():
    def test_get_StringBool_true(self):
        if self.parser.schema is None:
            validator = StringBool()
            assert self.parser.get("firstsection", "stringbool_true", validator) is True
        else:
            assert self.parser.get("firstsection", "stringbool_true") is True

    def test_get_StringBool_false(self):
        if self.parser.schema is None:
            validator = StringBool()
            assert self.parser.get("firstsection", "stringbool_false", validator) is False
        else:
            assert self.parser.get("firstsection", "stringbool_false") is False

    def test_get_StringBool_yes(self):
        if self.parser.schema is None:
            validator = StringBool()
            assert self.parser.get("firstsection", "stringbool_yes", validator) is True
        else:
            assert self.parser.get("firstsection", "stringbool_yes") is True

    def test_get_StringBool_no(self):
        if self.parser.schema is None:
            validator = StringBool()
            assert self.parser.get("firstsection", "stringbool_no", validator) is False
        else:
            assert self.parser.get("firstsection", "stringbool_no") is False

class NumberTests():
    def test_number_int_good(self):
        if self.parser.schema is None:
            validator = Number()
            assert self.parser.get("firstsection", "number_int_good", validator) is 10
        else:
            assert self.parser.get("firstsection", "number_int_good") is 10

    @raises(Invalid)
    def test_number_int_too_small(self):
        if self.parser.schema is None:
            validator = Number(min=5)
            self.parser.get("firstsection", "number_int_too_small", validator)
        else:
            self.parser.get("firstsection", "number_int_too_small")

    @raises(Invalid)
    def test_number_int_too_big(self):
        if self.parser.schema is None:
            validator = Number(max=50)
            self.parser.get("firstsection", "number_int_too_big", validator)
        else:
            self.parser.get("firstsection", "number_int_too_big")

    def test_number_float_good(self):
        if self.parser.schema is None:
            validator = Number()
            assert self.parser.get("firstsection", "number_float_good", validator) == 10.5
        else:
            assert self.parser.get("firstsection", "number_float_good") == 10.5

    @raises(Invalid)
    def test_number_float_too_small(self):
        if self.parser.schema is None:
            validator = Number(min=5.0)
            self.parser.get("firstsection", "number_float_too_small", validator)
        else:
            self.parser.get("firstsection", "number_float_too_small")

    @raises(Invalid)
    def test_number_float_too_big(self):
        if self.parser.schema is None:
            validator = Number(max=50.0)
            self.parser.get("firstsection", "number_float_too_big", validator)
        else:
            self.parser.get("firstsection", "number_float_too_big")

class SchemaTests():
    def test_no_validator(self):
        if self.parser.schema is None:
            assert self.parser.get("firstsection", "no_validator") == "10"
        else:
            self.parser.get("firstsection", "no_validator") == "10"

    def test_items(self):
        items = self.parser.items("good_section")
        if self.parser.schema is None:
            # Without schema, all values are returned as strings.
            for (option, value) in items:
                assert isinstance(value, StringType)
        else:
            assert items[0][1] == 1		# integer_good
            assert items[1][1] is True		# bool_one
            assert items[2][1] is True		# bool_zero, '0' == True
            assert items[3][1] is True		# stringbool_true
            assert items[4][1] is False		# stringbool_false
            assert items[5][1] is True		# stringbool_yes
            assert items[6][1] is False		# stringbool_no
            assert items[7][1] == 10		# number_int_good
            assert items[8][1] == 10.5		# number_float_good
            assert items[9][1] == "10"		# no_validator
    
class AllTests(IntTests, BoolTests, StringBoolTests, NumberTests, SchemaTests): 
    pass  
        
class TestRawConfigParserWithoutSchema(RawConfigParserWithoutSchema, AllTests): pass                

class TestConfigParserWithoutSchema(ConfigParserWithoutSchema, AllTests): pass

class TestSafeConfigParserWithoutSchema(SafeConfigParserWithoutSchema, AllTests): pass

class TestRawConfigParserWithSchema(RawConfigParserWithSchema, AllTests): pass

class TestConfigParserWithSchema(ConfigParserWithSchema, AllTests): pass

class TestSafeConfigParserWithSchema(SafeConfigParserWithSchema, AllTests): pass
