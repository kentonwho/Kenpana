import pytest
import xarray as xr
import numpy as np
from kenpana.transform import compoundness_max

def test_compoundness_max_valid_input():
    time = np.arange(10)
    compound = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time})
    surge_only = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time})
    rivers_only = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time})

    result = compoundness_max(compound, surge_only, rivers_only)
    assert isinstance(result, xr.DataArray), "Result should be an xarray DataArray"
    assert "time" in result.dims, "Result should have a 'time' dimension"

def test_compoundness_max_with_nans():
    time = np.arange(10)
    compound = xr.DataArray([np.nan] * 10, dims=["time"], coords={"time": time})
    surge_only = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time})
    rivers_only = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time})

    with pytest.raises(ValueError, match="Input DataArrays contain NaNs"):
        compoundness_max(compound, surge_only, rivers_only)

def test_compoundness_max_different_time_coords():
    compound = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": np.arange(10)})
    surge_only = xr.DataArray(np.random.rand(8), dims=["time"], coords={"time": np.arange(8)})
    rivers_only = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": np.arange(10)})

    with pytest.raises(ValueError):
        compoundness_max(compound, surge_only, rivers_only)

def test_compoundness_max_edge_case():
    time = np.arange(5)
    compound = xr.DataArray([1, 2, 3, 4, 5], dims=["time"], coords={"time": time})
    surge_only = xr.DataArray([1, 2, 3, 4, 5], dims=["time"], coords={"time": time})
    rivers_only = xr.DataArray([1, 2, 3, 4, 5], dims=["time"], coords={"time": time})

    result = compoundness_max(compound, surge_only, rivers_only)
    assert (result == 0).all(), "Compoundness should be zero when all inputs are identical"