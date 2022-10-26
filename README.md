# pylandtemp

[![GitHub license](https://img.shields.io/github/license/pylandtemp/pylandtemp)](https://github.com/pylandtemp/pylandtemp/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/pylandtemp/pylandtemp)](https://github.com/pylandtemp/pylandtemp/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/pylandtemp/pylandtemp)](https://github.com/pylandtemp/pylandtemp/network)
[![GitHub issues](https://img.shields.io/github/issues/pylandtemp/pylandtemp)](https://github.com/pylandtemp/pylandtemp/issues)

## Description

**pylandtemp** is a Python library that provides a simple API for computing **global land surface temperature and emissivity** from NASA's [Landsat](https://www.usgs.gov/landsat-missions) Level 1 satellite images (starting from Landsat 5 to Landsat 8).  It contains some implementations of Single-Channel and split window techniques. More methodologies under these groups will be added in the future.

Additionally, it also provides multiple methods for computing land surface emissivity. It is targeted towards supporting research and science workflows in many fields including climate science, earth sciences, remote sensing, space tech, geospatial data science, environmental studies, among others.


## Installation

The pylandtemp Python package is available through [PyPI](https://pypi.org/project/pylandtemp/):

```
pip install pylandtemp
```


## Documentation

The pylandtemp Python library is divided into multiple methods which provide access to set of algorithms for different computations.


- **Land surface temperature**

    - Single-Channel: through the `single_window()` method
    - Split window: through the `split_window()` method

- **Land surface emissivity**
    - Through the `emmissivity()` method.

- **Brightness temperature**
    - Through the `brightness_temperature()` method.

- **Normalized Difference Vegetation Index (NDVI)**
    - Through the `ndvi()` method.


## Example

To compute land surface temperature using [Jiminez-Munoz et al. (2014)](https://ieeexplore.ieee.org/abstract/document/6784508/?casa_token=A6cR6LeSSuoAAAAA:eFg3nxZvDTJpEBhvAmOwwJxo9rWy-y3aTdnArzEfbtM1UWUbBLhG9NhmeiQstFLTY8jbsT7x) split window technique and [Ugur Avdan et al. (2014)](https://www.hindawi.com/journals/js/2016/1480307/) emissivity computation method, a simple implementation  is shown below:

```python
import numpy as np
from pylandtemp import split_window

# lst_method and emissivity_method should point to keys of chosen -
# algorithms for temeprature and emmisivity, respectively

# Keys for available algorithms are presented in the next section

# tempImage10 is a numpy array of band 10 brightness temperature 
# tempImage11 is a numpy array of band 10 brightness temperature 
# redImage is a numpy array of the red band
# nirImage is a numpy array of the near infra-red (NIR) band

lst_image_split_window = split_window(
    tempImage10, 
    tempImage11, 
    redImage, 
    nirImage, 
    lst_method='jiminez-munoz', 
    emissivity_method='avdan',
    unit='celcius'
)

# The function returns a numpy array which is the land surface temperature image.
```


## Supported algorithms and their reference keys

#### Land surface temperature --- Split window 

| Algorithm                                                                                                                                                                                  | key             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- |
| [Jiminez-Munoz et al. (2014)](https://ieeexplore.ieee.org/abstract/document/6784508/?casa_token=A6cR6LeSSuoAAAAA:eFg3nxZvDTJpEBhvAmOwwJxo9rWy-y3aTdnArzEfbtM1UWUbBLhG9NhmeiQstFLTY8jbsT7x) | 'jiminez-munoz' |
| [Sobrino et al. (1993)](https://link.springer.com/content/pdf/10.1007/BF02524225.pdf)                                                                                                      | 'sobrino-1993'  |
| [Kerr et al. (1992)](https://www.sciencedirect.com/science/article/abs/pii/003442579290078X)                                                                                               | 'kerr'          |
| [McMillin et al. (1975)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JC080i036p05113)                                                                                          | 'mc-millin'     |
| [Price (1984)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JD089iD05p07231)                                                                                                    | 'price'         |

#### Land surface temperature --- Single-Channel 

| Algorithm                                                                     | key           |
| ----------------------------------------------------------------------------- | ------------- |
| [Ugur Avdan et al. (2014)](https://www.hindawi.com/journals/js/2016/1480307/) | 'mono-window' |

#### Land surface emissivity 

| Algorithm                                                                                                                                                                                   | key        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| [Gopinadh Rongali et al. (2018)](https://www.researchgate.net/publication/327461405_Split-Window_Algorithm_for_Retrieval_of_Land_Surface_Temperature_Using_Landsat_8_Thermal_Infrared_Data) | 'gopinadh' |
| [Ugur Avdan et al. (2014)](https://www.hindawi.com/journals/js/2016/1480307/)                                                                                                               | 'advan'    |
| [Xiaolei Yu et al. (2014)](https://www.mdpi.com/2072-4292/6/10/9829)                                                                                                                        | 'xiaolei'  |


## Tutorials
The notebooks [here](https://github.com/pylandtemp/pylandtemp/tree/master/tutorials) are tutorials on how to use pylandtemp package.


## Contributing

Open source thrives on collaborations and contributions. Let us work on this package in the same spirit.

If you catch any bug, find any typo or have any suggestions that will make this package better, 

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request


## What's new
- ***September 2022***: Started to work on intergrating with with google Earth Engine to pull data directly and automate the workflow.
- ***July 2022***: Poster presentation of this project at Scipy 2022. Link [here](https://hub-binder.mybinder.ovh/user/pylandtemp-pylandtemp-45pztpvy/doc/workspaces/auto-w/tree/tutorials)
- ***December 2021***: version 0.0.1-alpha.1 pre-release version is out on PyPI. Find it [here](https://pypi.org/project/pylandtemp/) 
- ***December 2021***: Implemented tutorial notebooks based on the different methods. Find them [here](https://github.com/pylandtemp/pylandtemp/tree/master/tutorials)
- ***November 2021***: Implemented a runner for dynamic dispatch.


## Code license 

The code of this library is available under the [Apache 2.0 license](https://fossa.com/blog/open-source-licenses-101-apache-license-2-0/).


## Sponsor

* [GitHub](https://github.com/sponsors/dimejimudele)


## How to cite

```
Mudele, O., (2021). pylandtemp: A Python package for computing land surface 
temperature from Landsat satellite imagery. GitHub: https://github.com/pylandtemp/pylandtemp.
```

If preferred, here is the BibTex:
```
@Misc{pylandtemp,
author = {Oladimeji Mudele},
title =        {pylandtemp: A Python package for computing land surface temperature from Landsat satellite imagery},
howpublished = {GitHub},
year =         {2021},
url =          {https://github.com/pylandtemp/pylandtemp}
}
```


