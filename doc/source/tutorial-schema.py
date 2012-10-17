import validatingconfigparser
import formencode.validators as validators
import formencode.schema as schema

class MySchema(schema.Schema):
    # Not validating names!

    gender = validators.OneOf(['male', 'female'])
    age = validators.Int(min=0)
    married = validators.StringBool()
    weight = validators.Number()
    

parser = validatingconfigparser.ConfigParser(schema=MySchema)
parser.read('tutorial-config.ini')

print parser.get('peter', 'name')
print parser.get('peter', 'gender')
print parser.get('peter', 'age')
print parser.get('peter', 'married')
print parser.get('peter', 'weight')

print parser.items("peter")

print parser.set('peter', 'age', -1)
