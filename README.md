# Kenpana 
Kenpana is a support library for interactive large scale visualization of ensembles ADCIRC output data. The library is built in the language: 
- Xarray/UGRID/cf_conventions for the interface with large NetCDF datasets 
- Dask for support for computation
- Scipy for statistics 
- Holoviews/Datashader for interactivity
From the user perspective, it is a way to bridge ADCIRC output into Holoviews templates. Thus the library's is not just a way to reuse holoviews objects, but also to be expressive enough that a person familiar with Holoviews can build their own templates. Details to convert between ADCIRC and holoviews are to be abstracted away, as well as details to matintain scalability. 

## Why Kenpana? 
Kenpana addresses the lack of capability for interactive large ensemble visualization. The closest competitor is OVIS, an Objective-C application that has GPU support and interactive GUIs. However, the choice of Objective-C limits the expressiveness of the application as users/developers cannot utilize the expansive libraries provided by python, specifically those provided by the Scipy. The use of Dask also allows for powerful out-of-core computation, making this more accessible to users without sufficient GPU access. Lastly, Holoviews allows for a client-server interface, reducing the need to transfer large data to and from clusters. 

## Why not Kenpana? 
If you have the compute and only need simple statistics, OVIS provides a faster application with "turn-key" operation. 

Similarly, Paraview provides client-server interface with distributed compute support, if you don't mind a bit of setup for the ADCIRC data structures prior. 


### Features planned 
- cf convention API 