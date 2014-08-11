from distutils.core import setup
import os

description = ''
if os.path.isfile('README.md'):
    with open('README.md', 'r') as f:
        description = f.read()

setup(
    name='bencodepy',
    version='0.9.1',
    packages=['bencodepy'],
    url='https://github.com/eweast/bencodepy',
    license='GPLv2',
    author='Eric Weast',
    author_email='eweast@hotmail.com',
    description='Bencode encoder/decoder written in Python 3 under the GPLv2.',
    long_description=description
)
