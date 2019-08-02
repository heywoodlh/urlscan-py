from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='urlscan-py',
      version='1.0.5',
      description="urlscan.io API wrapper",
      long_description=readme(),
      long_description_content_type='text/markdown',
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

