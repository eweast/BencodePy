from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name='bencodepy_opti',
    version='0.9.3',
    packages=['bencodepy_opti'],
    url='https://github.com/eweast/bencodepy_opti',
    license='GPLv2',
    author='Eric Weast',
    author_email='eweast@hotmail.com',
    description='Cythonized Bencode encoder/decoder written in Python 3 under the GPLv2.',
    long_description='',
    ext_modules=[Extension('decoder', ['../bencodepy/decoder.py', 'bencodepy_opti/decoder.pxd'])],
    cmdclass={'build_ext': build_ext}
)