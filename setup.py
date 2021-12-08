from setuptools import setup

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="pylandtemp",
    packages=["pylandtemp"],
    version="1.0.0",
    description="Compute land surface temperature(LST) from Landsat-8 data",
    author="Oladimeji Mudele",
    license="Apache 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/pylandtemp/pylandtemp",
    install_requires=[
        "numpy",
    ],
)
