import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='neze-young-interference',
    version='1',
    author="Clement Durand",
    author_email="durand.clement.13@gmail.com",
    description="Young interference visualisation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
    ),
    install_requires=['matplotlib','numpy','python-dateutil'],
)
