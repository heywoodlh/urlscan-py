from setuptools import setup

setup(name='urlscan-py',
      version='1.0',
      description='urlscan.io API wrapper',
      url='https://github.com/heywoodlh/urlscan-py',
      author='Flying Circus',
      author_email='l.spencer.heywood@gmail.com',
      license='APACHE-2.0',
      packages=['urlscan-py'],
      scripts=['bin/urlscan'],
      install_requires=[
          'certifi',
          'chardet',
          'idna',
          'requests',
          'urllib3',
      ],
      zip_safe=False)
