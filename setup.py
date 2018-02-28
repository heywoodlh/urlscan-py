from setuptools import setup
import os
import io

setup(name='urlscan-py',
      version='1.0',
      description='urlscan.io API wrapper',
      url='https://github.com/heywoodlh/urlscan-py',
      author='Spencer Heywood',
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

here = os.path.dirname(__file__)

readme_path = os.path.join(here, 'README.md')
with io.open(readme_path, encoding='utf-8') as readme_file:
    long_description = readme_file.read()
