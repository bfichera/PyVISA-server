import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('.version', 'r') as fh:
    version = fh.read().splitlines()[0]

setuptools.setup(
    name='PyVISA-server',
    version=version,
    author='Bryan Fichera',
    author_email='bfichera@mit.edu',
    description=(
        'A local server designed to manage communication between'
        'clients and multiple different VISA instruments.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bfichera/PyVISA-server',
    packages=setuptools.find_packages(),
    classifiers=[
`       'Programming Language :: Python :: 3',
        'Licence :: OSI Approved :: MIT License',
        'Operating System :: Unix',
    ],
    python_requires='>=3.9',
    scripts=['bin/pyvisa-server'],
    install_requires=[
        'appdirs',
        'dill',
        'pyvisa',
    ]
)
