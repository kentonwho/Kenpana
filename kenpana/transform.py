"""
This module provides functionalities to do computations/transformations on the data. 

Currently, since the data and transformations are pretty simple, this module is also simple. 
However, in the future, it may desirable to define abstract data classes so this is more of a 
template for future development. This may include an "ensemble" data class. 

Notes: 
- The ensemble data should have a time dimension, and be exactly aligned. How should we key xarray to handle nonaligned data?
- Where data is dry, NaNs are used. Should we write custom routines to accelerate these? Should we use water column heihgt or water elevation? 
- Under the philosphy of "abstracting away" Xarray implementation, we should return full 'mesh data' dataset objects. 
- Optimize by using depth skipping paramater? This would justify the use of the whole dataset. 
- Should I "bootstrap" the compoundness function to create a hidden primitave "compoundness" function that also works on numpy types?
"""

import xarray as xr 
import numpy as np

def compoundness_max(compound: xr.DataArray, surge_only: xr.DataArray, rivers_only: xr.DataArray, strict=True):
    """
    Computes the 'compoundness' of a triplet of time series, assuming an inner join alignment. 

    Parameters
    ----------
    compound : xr.DataArray
        The time series of water column height from a compound forced run. 
    surge_only : xr.DataArray  
        The time series of water column height surge only forced run.
    rivers_only : xr.DataArray 
        The time series of water column height flow only forced run. 
    strict : bool, optional
        If true, the function will do sanity checks on the data. Note that this will force the data to load into
        memory and may eat up some time.

    Returns
    -------
    xr.Dataset (?) maybe a float
        The compoundness of the triplet of time series. 
    """


    xr.set_options(arithmetic_join='inner')
    if strict: 
        if compound.isnull().any() or surge_only.isnull().any() or rivers_only.isnull().any():
            raise ValueError("Input DataArrays contain NaNs. Please handle NaNs before calling this function.")
        
        if (compound < 0).any() or (surge_only < 0).any() or (rivers_only < 0).any():
            raise ValueError("Input DataArrays contain negative values. Please ensure all values correspond to water column height.")

    diff_compound_surge = abs(compound - surge_only)
    diff_compound_rivers = abs(compound - rivers_only)
    surge_error = diff_compound_surge.max(dim='time')
    rivers_error = diff_compound_rivers.max(dim='time')
    compoundness = np.minimum(surge_error, rivers_error)

    return compoundness

def water_column_height(elv: xr.Dataset) -> xr.Dataset: 
    """
    Computes the water column height from the water elevation. 

    Parameters
    ----------
    elv : xr.DataArray
        The water elevation. 

    Returns
    -------
    xr.DataArray
        The water column height. 
    """

    water_column_height = elv.drop_vars("zeta")
    bathymetry = elv["depth"]
    water_column_height["water_column_height"] = xr.where(np.isnan(elv["zeta"]), 0, elv["zeta"] + bathymetry)
    return water_column_height

    

