from distutils.core import setup


setup(
  name='pickle-database',
  packages=['pickle_database'],
  version='0.0.1',
  license='MIT',
  description='A database that uses pickle and runs tests on data entry',
  author='Audrow Nash',
  author_email='audrowna@usc.edu',
  url='https://github.com/robotpt/pickle-database',
  install_requires=[
    'dill',
    'robotpt_common_utils',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)
