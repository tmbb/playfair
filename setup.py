from setuptools import setup

install_requirements = [
  'matplotlib',
  'python-docx'
]

test_requirements = [
  'hypothesis',
  'pytest'
]

setup(name='playfair',
      version='0.1',
      description='Utilities for visualizing and publishing research',
      url='http://github.com/tmbb/playfair',
      author='Tiago Barroso',
      author_email='tmbb@campus.ul.pt',
      license='MIT',
      install_requires=install_requirements,
      test_requires=test_requirements,
      packages=['playfair'],
      zip_safe=False)