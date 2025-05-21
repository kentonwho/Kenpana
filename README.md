# Kenpana 
Kenpana is a support library for interactive large scale visualization of ensembles ADCIRC output data. The library is built in the language: 
- Xarray/UGRID/cf_conventions for the interface with large NetCDF datasets 
- Dask for support for large memory computation, Numba/Bottleneck where necessary to accelerate computation. 
- Scipy for statistics 
- Holoviews/Datashader for interactivity
From the user perspective, it is a way to bridge ADCIRC output into Holoviews templates. Thus the library's is not just a way to reuse holoviews objects, but also to be expressive enough that a person familiar with Holoviews can build their own templates. Details to convert between ADCIRC and holoviews are to be abstracted away, as well as details to matintain scalability. Exposure to Xarray internals will be kept to a minimum, as well as details about optimization specifically for ADCIRC data. This allows the user to avoid details about implementation and instead think about transforming ADCIRC mesh data into Holoviews objects. 

## What are ADCIRC mesh fields? 
Mesh fields are the basic object of Kenpana. They're mostly netcdf data (later UGRID objects) with the associated metadata to interpret it as a field. There will also be hidden optimizations for ADCIRC-specific data features, such as masking deep ocean nodes. 

## What are ADCIRC ensembles? 
Ensembles are a collection of ADCIRC mesh fields with extra metadata specifiying parameter types. On disk, they should be represented as a single netcdf file. However, in later iterations there may be support for xclim/xhydro which offer a broader suite of statistical analysis tools. 

## Why Kenpana? 
Kenpana addresses the lack of capability for interactive large ensemble visualization. The closest competitor is OVIS, an Objective-C application that has GPU support and interactive GUIs. However, the choice of Objective-C limits the expressiveness of the application as users/developers cannot utilize the expansive libraries provided by python, specifically those provided by the Scipy. The use of Dask also allows for powerful out-of-core computation, making this more accessible to users without sufficient GPU access. Lastly, Holoviews allows for a client-server interface, reducing the need to transfer large data to and from clusters. Thusly, it is built first and foremost for those working with data in an HPC environment, specifically TACC's slurm job manager. 

## Why not Kenpana? 
If you have the compute and only need simple statistics, OVIS provides a faster application with "turn-key" operation. 

Similarly, Paraview provides client-server interface with distributed compute support, if you don't mind a bit of setup for the ADCIRC data structures prior. 


### Features planned 
- cf convention API 