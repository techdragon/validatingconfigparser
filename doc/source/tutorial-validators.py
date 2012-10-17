import validatingconfigparser
import formencode.validators as validators

parser = validatingconfigparser.ConfigParser()
parser.read('tutorial-config.ini')

print parser.get('peter', 'name', validator=validators.String())
print parser.get('peter', 'gender', validator=validators.OneOf(['male', 'female']))
print parser.get('peter', 'age', validator=validators.Int(min=0))
print parser.get('peter', 'married', validator=validators.StringBool())
print parser.get('peter', 'weight', validator=validators.Number())

print parser.set('peter', 'age', -1, 
        validator=validators.Int(min=0))  # Peter is back in the womb!
