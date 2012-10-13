




import validatingconfigparser
import formencode.validators

from nose.tools import *


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


class IntTests():
    def test_get_Int(self):
        validator = formencode.validators.Int()
        assert self.parser.get("firstsection", "integer", validator) == 1
        
    def test_get_Int_within_min_max(self):
        validator = formencode.validators.Int(min=1, max=1)
        assert self.parser.get("firstsection", "integer", validator) == 1
    
    @raises(formencode.Invalid)
    def test_get_Int_outside_min_max(self):
        validator = formencode.validators.Int(min=2, max=2)
        assert self.parser.get("firstsection", "integer", validator) == 1


    def test_getint_Int(self):
        validator = formencode.validators.Int()
        assert self.parser.getint("firstsection", "integer", validator) == 1
        
    def test_getint_Int_within_min_max(self):
        validator = formencode.validators.Int(min=1, max=1)
        assert self.parser.getint("firstsection", "integer", validator) == 1
    
    @raises(formencode.Invalid)
    def test_getint_Int_outside_min_max(self):
        validator = formencode.validators.Int(min=2, max=2)
        assert self.parser.getint("firstsection", "integer", validator) == 1


class BoolTests():
    def test_get_StringBool_false(self):
        validator = formencode.validators.StringBool()
        assert self.parser.get("firstsection", "stringbool_false", validator) is False
    
    def test_get_StringBool_true(self):
        validator = formencode.validators.StringBool()
        assert self.parser.get("firstsection", "stringbool_true", validator) is True
        
        
    def test_getboolean_StringBool_false(self):
        validator = formencode.validators.StringBool()
        assert self.parser.getboolean("firstsection", "stringbool_false", validator) is False
    
    def test_getboolean_StringBool_true(self):
        validator = formencode.validators.StringBool()
        assert self.parser.getboolean("firstsection", "stringbool_true", validator) is True
        
        
#    def test_get_Bool_false(self):
#        validator = formencode.validators.Bool()
#        assert self.parser.get("firstsection", "bool_false", validator) is False
    
    def test_get_Bool_true(self):
        validator = formencode.validators.Bool()
        assert self.parser.get("firstsection", "bool_true", validator) is True
        
        
#    def test_getboolean_Bool_false(self):
#        validator = formencode.validators.Bool()
#        assert self.parser.getboolean("firstsection", "bool_false", validator) is False
    
    def test_getboolean_Bool_true(self):
        validator = formencode.validators.StringBool()
        assert self.parser.getboolean("firstsection", "bool_true", validator) is True
    
    
class AllTests(IntTests, BoolTests): pass  
        
class TestRawConfigParserWithoutSchema(RawConfigParserWithoutSchema, AllTests): pass                

class TestConfigParserWithoutSchema(ConfigParserWithoutSchema, AllTests): pass

class TestSafeConfigParserWithoutSchema(SafeConfigParserWithoutSchema, AllTests): pass
