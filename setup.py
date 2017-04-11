import os
from setuptools import setup, find_packages

def readfile(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ciseau',
    version='1.0.0',
    description='Word and sentence tokenization.',
    long_description=readfile('README.md'),
    ext_modules=[],
    packages=find_packages(),
    py_modules = [],
    author='Jonathan Raiman',
    author_email='jonathanraiman@gmail.com',
    url='https://github.com/JonathanRaiman/ciseau',
    download_url='https://github.com/JonathanRaiman/ciseau',
    keywords='XML, tokenization, NLP',
    license='MIT',
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
    ],
    setup_requires = [],
    install_requires=[
    ],
    include_package_data=True,
)
