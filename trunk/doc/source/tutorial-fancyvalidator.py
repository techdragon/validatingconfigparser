from formencode import Invalid
from formencode.api import FancyValidator

class EvenValidator(FancyValidator):
    def validate_python(self, value, state):
        if (value % 2) == 0:
            return value
        else:
            raise Invalid("%s not an even number" %(value), value, state)

    def _to_python(self, value, state):
        # Called by get() - must accept string.
        return int(value)

    def _from_python(self, value, state):
        # Called by set() - must return string.
        return str(value)


print EvenValidator().to_python(2)
print EvenValidator().to_python(1)
