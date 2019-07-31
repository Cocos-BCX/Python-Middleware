#!/usr/bin/env python3

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '1.0.0'

setup(
    name='PythonMiddleware',
    version=VERSION,
    description='Python library for Cocos-BCX',
    long_description=open('README.md').read(),
    author='UnitedLabs',
    author_email='UnitedLabs@hotmail.com',
    maintainer='UnitedLabs',
    maintainer_email='UnitedLabs@hotmail.com',
    keywords=['PythonMiddleware', 'library', 'api', 'rpc'],
    packages=[
        "PythonMiddleware",
        "PythonMiddlewareapi",
        "PythonMiddlewarebase",
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial',
    ],
    install_requires=[
        "ecdsa==0.13",
        "requests==2.22.0",
        "websocket-client==0.48.0",
        "pylibscrypt==1.7.1",
        "pycryptodome==3.6.6",
        "websockets==6.0",
        "appdirs==1.4.3",
        "Events==0.3",
        "scrypt==0.8.6",
        "pycrypto==2.6.1",  # for AES, installed through graphenelib already
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
