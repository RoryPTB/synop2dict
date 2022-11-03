from setuptools import setup
import io
import os


def read(filename, encoding='utf-8'):
    """read file contents"""
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with io.open(full_path, encoding=encoding) as fh:
        contents = fh.read().strip()
    return contents


setup(name='synop2dict',
      version='0.1',
      description='Convert a SYNOP tac messages or a SYNOP file into a dictionary ready for conversion to BUFR4.',
      author='Rory Burke',
      author_email='RBurke@wmo.int',
      install_requires=read('requirements.txt').splitlines(),
      packages=['synop2dict'],
      zip_safe=False
      )
