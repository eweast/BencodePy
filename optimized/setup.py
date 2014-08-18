from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name="decoder",
    ext_modules=[Extension('decoder', ['../bencodepy/decoder.py', 'decoder.pxd'])],
    cmdclass={'build_ext': build_ext}

)