import pytest
import xarray as xr
import numpy as np
from pathlib import Path
from kenpana.read import read_gelv

@pytest.mark.parametrize(
    #Run tests for mock and optionally real data in the data subfolder.
    "fort63_file_fixture",
    ["mock_fort63_file", "real_fort63_file"],
)

@pytest.fixture
def mock_fort63_file(tmp_path):
    """
    Create a mock fort.63 NetCDF file for testing.The mock files has 56 nodes with 4 time steps.
    """
    file_path = tmp_path / "mock_fort63.nc"
    times = np.array(
        ["2023-01-01T00:00:00", "2023-01-01T01:00:00", "2023-01-01T02:00:00", "2023-01-01T03:00:00"],
        dtype="datetime64[ns]"
    )
    nnodes = 56
    elevation = np.random.rand(len(times), nnodes)
    vertex_num = [0, 1, 2]
    rand_elements = np.random.rand(nnodes, 3)

    ds = xr.Dataset(
        {
            "zeta": (("time", "node"), elevation),
            "element": (("node", "vertex"), rand_elements),
        },
        coords={
            "time": times,
            "vertex": vertex_num,
        },
    )
    ds.to_netcdf(file_path)
    return file_path

@pytest.fixture
def mock_fort63_with_duplicates(tmp_path, mock_fort63_file):
    """
    Create a mock fort.63 NetCDF file with duplicate time values for testing.
    """
    file_path = tmp_path / "mock_fort63_with_duplicates.nc"
    ds = xr.open_dataset(mock_fort63_file)
    times = np.array(
        ["2023-01-01T00:00:00", 
         "2023-01-01T01:00:00", "2023-01-01T01:00:00", #Duplicates here
         "2023-01-01T02:00:00"],
        dtype="datetime64[ns]"
    )  # Duplicate time values

    ds["time"] = times 

    ds.to_netcdf(file_path)
    return file_path

@pytest.fixture
def mock_fort63_corrupted(tmp_path, mock_fort63_file):
    """
    Create a mock fort.63 NetCDF file representing the flushed values of a simulation that was interrupted.
    """
    file_path = tmp_path / "mock_fort63_corrupted.nc"
    ds = xr.open_dataset(mock_fort63_file)

    times = np.array(
        ["2023-01-01T00:00:00", 
        "2023-01-01T01:00:00", 
        "2023-01-01T02:00:00.123", "2023-01-01T03:00:00.456"], #Corresponding to the flushed values
        dtype="datetime64[ns]"
    )

    ds["time"] = times

    ds.to_netcdf(file_path)
    return file_path

@pytest.fixture
def real_fort63_file():
    """
    Path to a real fort.63 NetCDF file for testing.
    """
    # Replace with the actual path to your real fort.63 file
    return Path("tests/data/test.63.nc")

# Test corrupted cases

def test_read_gelv_duplicate_times(mock_fort63_with_duplicates):
    """
    Test that read_gelv raises a ValueError when duplicate time values are present.
    """
    with pytest.raises(ValueError, match="Duplicate time values found"):
        read_gelv(mock_fort63_with_duplicates)

def test_read_gelv_corrupted_file(mock_fort63_corrupted):
    """
    Test that read_gelv raises a ValueError when the file is corrupted.
    """
    with pytest.raises(ValueError, match="Timestamps are not homogeneous. Write out may have been interrupted prematurely."):
        read_gelv(mock_fort63_corrupted)


# Test non-corrupted cases

@pytest.mark.parametrize(
    "fort63_file_fixture",
    ["mock_fort63_file", "real_fort63_file"],
)
def test_read_gelv_valid_file(request, fort63_file_fixture):
    """
    Test that read_gelv correctly reads a valid fort.63 file.
    """
    path = request.getfixturevalue(fort63_file_fixture)
    dataset = read_gelv(path)
    assert isinstance(dataset, xr.Dataset)
    assert "zeta" in dataset
    assert "time" in dataset.coords
    assert "node" in dataset.dims
    assert "element" in dataset

@pytest.mark.parametrize(
    "fort63_file_fixture",
    ["mock_fort63_file", "real_fort63_file"],
)
def test_read_gelv_chunks(request, fort63_file_fixture):
    """
    Test that read_gelv applies chunking correctly, say on a 56 core machine.
    """
    path = request.getfixturevalue(fort63_file_fixture)

    chunks = {"time": None, "node": 56}
    dataset = read_gelv(path, chunks=chunks)
    assert dataset.chunks is not None
    assert dataset.chunks["time"] == (len(dataset.time),)
    assert dataset.chunks["node"][0] == 56