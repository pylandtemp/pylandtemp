# pylandtemp

[![GitHub license](https://img.shields.io/github/license/pylandtemp/pylandtemp)](https://github.com/pylandtemp/pylandtemp/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/pylandtemp/pylandtemp)](https://github.com/pylandtemp/pylandtemp/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/pylandtemp/pylandtemp)](https://github.com/pylandtemp/pylandtemp/network)
[![GitHub issues](https://img.shields.io/github/issues/pylandtemp/pylandtemp)](https://github.com/pylandtemp/pylandtemp/issues)

## Description

**pylandtemp** is a Python library with algorithms to compute **global land surface temperature** from NASA's [Landsat](https://www.usgs.gov/landsat-missions) satellite images. It contains mono-window and split-window techniques which have been implemented in optimized ways.
Additionally, it also provides multiple methods for computing land surface emissivity. It is targeted towards supporting research and science workflows in many fields including climate science, earth sciences, remote sensing, space tech, geospatial data science, environmental studies, among others.

Even though only Landsat images are currently 'officially' supported, the methods available via this Python tool can be applied to other dataset including ASTER and MODIS.


## What's new:
- ***December 2021***: version 0.0.1-alpha.1 pre-release version is out on PyPI. Find it [here](https://pypi.org/project/pylandtemp/) 
- ***December 2021***: Implemented tutorial notebooks based on the different methods. Find them [here](https://github.com/pylandtemp/pylandtemp/tree/master/tutorials)
- ***November 2021***: Implemented a runner for dynamic dispatch.
## Installation: PyPI

`pip install pylandtemp`


## Supported algorithms

#### Land surface temperature --- Split window 
`pylandtemp.split_window(...)`
| Algorithm|key|
|----------|---|
|[Jiminez-Munoz et al. (2014)](https://ieeexplore.ieee.org/abstract/document/6784508/?casa_token=A6cR6LeSSuoAAAAA:eFg3nxZvDTJpEBhvAmOwwJxo9rWy-y3aTdnArzEfbtM1UWUbBLhG9NhmeiQstFLTY8jbsT7x)| 'jiminez-munoz' |
|[Coll C. et al. (1997)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/97JD00929)|'coll-caselles'|
|[Sobrino et al. (1993)](https://link.springer.com/content/pdf/10.1007/BF02524225.pdf)|'sobrino-1993'|
|[Kerr et al. (1992)](https://www.sciencedirect.com/science/article/abs/pii/003442579290078X)|'kerr'|
|[McClain et al. (1985)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JC090iC06p11587)|'mc-clain'|
|[Price (1984)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JD089iD05p07231)|'price'|

#### Land surface temperature --- Single window 
`pylandtemp.single_window(...)`

| Algorithm|key|
|----------|---|
|[Ugur Avdan et al. (2014)](https://www.hindawi.com/journals/js/2016/1480307/)| 'mono-window' |

#### Land surface emissivity 
`pylandtemp.emissivity(...)`

| Algorithm|key|
|----------|---|
|[Gopinadh Rongali et al. (2018)](https://www.researchgate.net/publication/327461405_Split-Window_Algorithm_for_Retrieval_of_Land_Surface_Temperature_Using_Landsat_8_Thermal_Infrared_Data)| 'gopinadh' |
|[Ugur Avdan et al. (2014)](https://www.hindawi.com/journals/js/2016/1480307/)| 'advan' |
|[Xiaolei Yu et al. (2014)](https://www.mdpi.com/2072-4292/6/10/9829)| 'xiaolei' |



## How to start using pylandtemp
The notebooks [here](https://github.com/pylandtemp/pylandtemp/tree/master/tutorials) are a good place to start.



## How to contribute to pylandtemp

All kinds of contributions are welcome --- development of enhancements, bug fixes, documentation, tutorial notebooks, new methods, new data, etc.... 

A guide to get you started with contributing will soon be made available.

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


