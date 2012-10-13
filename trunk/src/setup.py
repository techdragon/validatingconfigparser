from distutils.core import setup
import sys

#sys.path.append('validatingconfigparser')
import validatingconfigparser

setup(name='validatingconfigparser',
      version='0.1',
      author='Markus Juenemann',
      author_email='markus.at.juenemann@gmail.com',
      url='http://code.google.com/p/validatingconfigparser/',
      download_url='http://code.google.com/p/validatingconfigparser/downloads/list',
      description="Python's ConfigParser classes with validation",
      long_description=validatingconfigparser.__doc__,
      package=['validatingconfigparser'],
      provides=['validatingconfigparser'],
      keywords='ConfigParser configparser validation Formencode',
      license='Apache License 2.0',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: Apache Software License',
                   'Topic :: Software Development :: Libraries :: Python Modules' 
                  ],
     )
