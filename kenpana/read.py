"""
This module reads the ADCIRC files. 

Notes: 
-   Should NaN's be handled here or in the calling function?
-   The 63 with the metadata will be our "abstract spatial field" object. 
"""
import xarray as xr
import numpy as np

#Eventually, I would want this to read into dedicated classes/UGRID objects. 
def read_gelv(fname: str, chunks: dict = {'time': None, 'node': 'auto'}, strict = True, **kwargs) -> xr.Dataset:
    """
    Read a fort.63 (Global elevation above geoid) file with metadata and return a chunked xarray dataset.
    
    Parameters
    ----------
    filename : str
        The name of the file to read.
    
    chunk : dict, optional
        A dictionary specifying the chunk sizes for the dataset. The default is chunks along nodes and 
        leaves time dimensions intact, which prepares the dataset for processing nodes in parallel. 

    classic : bool, optional
        If true, only the global elevation is read, which corresponds to the classic fort.63 file definition.
        Elsewise, the entire NetCDF file is read, which may contain additional data such as mesh information.

    strict: bool, optional
        If true, this function will try to catch any malformed NetCDF files. You may want to skip this if you 
        are relatively sure the file is well-formed and you want to speed up the read process.

    Returns
    -------
    xr.Dataset
        The xarray dataset containing the global elevation data, with pertinent metadata to interpret the data 
        spatially. 
    """
    global_elevation_ds = xr.open_dataset(fname, chunks=chunks, **kwargs)

    if strict: 
        unique_times, counts = np.unique(global_elevation_ds['time'].values, return_counts=True)
        dupes = unique_times[counts > 1]
        if dupes.size > 0:
            raise ValueError(f"Duplicate time values found: {dupes}. Please check the file.")
        
        times = global_elevation_ds['time'].values
        time_diffs = np.diff(times)
        nspoolge = time_diffs[0]
        if not np.all(time_diffs == nspoolge):
            raise ValueError("Timestamps are not homogeneous. Write out may have been interrupted prematurely.")

    
    # Return the dataset
    return global_elevation_ds

def read_fort63(fname: str, chunks: dict = {'time': None, 'node': 'auto'}, **kwargs) -> xr.Dataset:
    """
        Read a fort.63 (Global elevation above geoid file) without metadata, as per the classic fort.63 file definition.
    """