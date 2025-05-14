import pytest
import xarray as xr
import numpy as np
from kenpana.transform import compoundness_max, water_column_height

"""
For later features where I build from a numpy primative 
@pytest.fixture
def mock_triplet(): 
    return 2, 1, 0

@pytest.fixture
def mock_triplet_invalid(): 
    return 2, -1, np.nan
 """
@pytest.fixture
def mock_triplet_time_series(): 
    """Create a mock a valid time series triplet."""
    time = np.arange("2000-01-01T00:00", "2000-01-01T10:00", dtype="datetime64[h]")
    time_compound = time + np.timedelta64(1, "h")
    time_surge_only = time - np.timedelta64(2, "h")
    time_rivers_only = time
    compound = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time_compound})
    surge_only = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time_surge_only})
    rivers_values = np.random.rand(10)
    rivers_values[0] = 999
    rivers_values[-1] = 999
    rivers_only = xr.DataArray(rivers_values, dims=["time"], coords={"time": time_rivers_only})
    return compound, surge_only, rivers_only

@pytest.fixture 
def mock_triplet_gelvs(): 
    """Test a valid global elevation object."""
    time = np.arange("2000-01-01T00:00", "2000-01-01T10:00", dtype="datetime64[h]")
    time_compound = time + np.timedelta64(1, "h")
    time_surge_only = time - np.timedelta64(2, "h")
    time_rivers_only = time
    compound = xr.DataArray(np.random.rand(10, 12), dims=["time", "node"], coords = {"time": time_compound})
    surge_only = xr.DataArray(np.random.rand(10, 12), dims=["time", "node"], coords = {"time": time_surge_only})
    rivers_only = xr.DataArray(np.random.rand(10, 12), dims=["time", "node"], coords = {"time": time_rivers_only})

    return compound, surge_only, rivers_only


"""
For later features where I support ensembles 
@pytest.fixture
def mock_ensemble_gelvs(): 
    'Test a valid ensemble of global elevation objects.'

@pytest.fixture
def mock_triplet_invalid_gelvs():
    'Test invalid objects such as mismatching meshes, time coordiate spacing,'
"""

def test_compoundness_max_time_series(mock_triplet_time_series):
    compound, surge_only, rivers_only = mock_triplet_time_series
    result = compoundness_max(compound, surge_only, rivers_only)
    assert isinstance(result, xr.DataArray), "Result should be an xarray DataArray"
    assert "time" not in result.dims, "Result should not have time as a dimension"
    assert result.shape == (), "Result should be a scalar value"
    assert result < 1, "Calculated value should account for missing/mismatched time stamps (results should be less than 1)"
    assert result > 0, "Result should be positive"
    
def test_compoundness_max_gelvs(mock_triplet_gelvs):
    compound, surge_only, rivers_only = mock_triplet_gelvs
    result = compoundness_max(compound, surge_only, rivers_only)
    assert isinstance(result, xr.DataArray), "Result should be an xarray DataArray"
    assert "time" not in result.dims, "Result should not have time as a dimension"
    assert "node" in result.dims, "Result should return a value for each node"
    assert result.shape == (12,), "Result should have the same number of nodes as the input DataArrays"

def test_compoundness_max_noncompound():
    time = np.arange(5)
    compound = xr.DataArray([1, 2, 3, 4, 5], dims=["time"], coords={"time": time})
    matching = xr.DataArray([1, 2, 3, 4, 5], dims=["time"], coords={"time": time})
    nonmatching = xr.DataArray([0, 0, 0, 0, 0], dims=["time"], coords={"time": time})

    surge_dominated_result = compoundness_max(compound, matching, nonmatching)
    rivers_dominated_result = compoundness_max(compound, nonmatching, matching)
    assert (surge_dominated_result == 0).all, "Compoundness should be zero when compound is dominated by surge"
    assert (rivers_dominated_result == 0).all(), "Compoundness should be zero when compound is dominated by rivers"

def test_compoundness_max_compound():
    time = np.arange(5)
    compound = xr.DataArray([10, 20, 30, 40, 50], dims=["time"], coords={"time": time})
    surge_only = xr.DataArray([10, 20, 0, 40, 50], dims=["time"], coords={"time": time}) 
    rivers_only = xr.DataArray([10, 20, 999, 40, 50], dims=["time"], coords={"time": time})

    result = compoundness_max(compound, surge_only, rivers_only)
    assert (result > 10).all(), "Compoundness should high when both surge and rivers are inaccurate"


"""
Future test
def test_compoundness_max_with_nans():
    time = np.arange(10)
    compound = xr.DataArray([np.nan] * 10, dims=["time"], coords={"time": time})
    surge_only = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time})
    rivers_only = xr.DataArray(np.random.rand(10), dims=["time"], coords={"time": time})

    with pytest.raises(ValueError, match="Input DataArrays contain NaNs"):
        compoundness_max(compound, surge_only, rivers_only)
"""