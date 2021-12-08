from setuptools import setup

setup(
    name="pylandtemp",
    packages=["pylandtemp"],
    version="0.0.10",
    description="Compute land surface temperature(LST) from Landsat-8 data",
    author="Oladimeji Mudele",
    license="Apache 2.0",
    install_requires=[
        "numpy",
    ],
)
