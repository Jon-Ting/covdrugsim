import setuptools


__version__ = '1.0.1'
with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="covdrugsim",
    version=__version__,
    author="Jonathan Yik Chang Ting",
    author_email="jonting97@gmail.com",
    description = "Package to automate quantum mechanical calculations and molecular dynamics simulations of covalent drugs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jon-Ting/covdrugsim",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
)

