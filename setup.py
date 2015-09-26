import os
from setuptools import setup, find_packages

def readfile(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='xml-cleaner',
    version='1.0.21',
    description='Python package for cleaning up xml and tokenizing text',
    long_description=readfile('README.md'),
    ext_modules=[],
    packages=find_packages(),
    py_modules = [],
    author='Jonathan Raiman',
    author_email='jraiman at mit dot edu',
    url='https://github.com/JonathanRaiman/xml_cleaner',
    download_url='https://github.com/JonathanRaiman/xml_cleaner',
    keywords='XML, tokenization, NLP',
    license='MIT',
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Topic :: Text Processing :: Linguistic',
    ],
    # test_suite="something.test",
    setup_requires = [],
    install_requires=[
        'cython'
    ],
    include_package_data=True,
)
