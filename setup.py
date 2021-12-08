from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pylandtemp",
    packages=["pylandtemp"],
    version="1.0.0",
    description="Compute land surface temperature(LST) from Landsat-8 data",
    author="Oladimeji Mudele",
    license="Apache 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pylandtemp/pylandtemp",
    install_requires=[
        "numpy",
    ],
    keywords="sample, setuptools, development",
    package_dir={"": "pylandtemp"},
)
