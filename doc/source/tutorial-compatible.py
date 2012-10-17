import validatingconfigparser

parser = validatingconfigparser.ConfigParser()
parser.read('tutorial-config.ini')

print parser.get('peter', 'name')
print parser.get('peter', 'gender')
print parser.getint('peter', 'age')
print parser.getboolean('peter', 'married')
print parser.getfloat('peter', 'weight')

print parser.set('peter', 'age', str(31))  # Peter is getting older.
print parser.getint('peter', 'age')

print parser.get('peter', 'height')	   # no such option!

