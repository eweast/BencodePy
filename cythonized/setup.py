__author__ = 'Eric Weast'

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name="decoder",
    #ext_modules=cythonize('decoder.py'),
    ext_modules=[Extension('decoder', ['decoder.py', 'decoder.pxd'])],
    cmdclass={'build_ext': build_ext}

)
