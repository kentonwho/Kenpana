import xarray as xr
import numpy as np

#Eventually, I would want this to read into dedicated classes/UGRID objects. 
def read_63(fname: str, classic = False, chunks: dict = {'time': None, 'node': 'auto'}, **kwargs) -> xr.Dataset:
    """
    Read a fort.63 (Global elevation) file and return a chunked xarray dataset.
    
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
    
    Returns
    -------
    xr.Dataset
        The xarray dataset containing the data from the file.
    """
    # Open the file using xarray
    global_elevation_ds = xr.open_dataset(fname, chunks=chunks, **kwargs)
    if classic: 
        global_elevation_ds = global_elevation_ds['zeta']

    unique_times, counts = np.unique(global_elevation_ds['time'].values, return_counts=True)
    dupes = unique_times[counts > 1]
    if dupes.size > 0:
        raise ValueError(f"Duplicate time values found: {dupes}. Please check the file.")
    
    # Return the dataset
    return global_elevation_ds