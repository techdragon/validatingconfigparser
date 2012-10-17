
class EvenValidator(object):
    def validate(self, value):
        if (value % 2) == 0:
            return value
        else:
            raise ValueError("%s not an even number" %(value))

    def to_python(self, value):
        # Called by get() - must accept string.
        return self.validate(int(value))

    def from_python(self, value):
        # Called by set() - must return string.
        return self.str(self.validate(value))


print EvenValidator().to_python(2)
print EvenValidator().to_python(1)
