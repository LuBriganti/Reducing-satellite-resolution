# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 18:55:58 2022

@author: fd_25
"""

import numpy as np
import os
import xarray as xr
import pandas as pd
import netCDF4
from netCDF4 import Dataset, date2index , MFDataset
import bottleneck as bn
import scipy.ndimage as sci

#retrieving and exploring data

working_dir = os.chdir('C:/Users/fd_25/Desktop/Project/GOES16-2022001')
files = os.listdir(working_dir)  
nc_files = []
for file in files:
   if file.endswith('.nc'):
       nc_files.append(file)

arr = xr.open_mfdataset(nc_files,concat_dim= 't', combine = 'nested',
                        engine ='netcdf4')

subset =np.arange(0,5424,8)
time_var = arr['t'][:].values
x_var = arr['x'][:].values
x_var_new = x_var[subset] #subsetting for later
y_var = arr['y'][:].values
y_var_new = y_var[subset] #subsetting for later


## calculating the avg uniformly from the 5424x5424 grid
arr_avg = np.empty((144,5424,5424), dtype='float32') 

for i in np.arange(0, len(nc_files), 1):
   
    arr = xr.open_dataset(nc_files[i]) 
    radiance = (arr['Rad'][:].load()).values  

    #Find indices that you need to replace
    inds = np.where(np.isnan(radiance))

    #Place column means in the indices. Align the arrays using take
    radiance[inds] = np.nanmean(radiance)

    
    arr_avg[i,:,:] = sci.uniform_filter(radiance, size=8, mode='nearest')



low_res_grid = arr_avg[:,subset,:]
low_res_grid = low_res_grid [:,:,subset]


## writting the new xarray to export it


radiance = xr.DataArray(
           low_res_grid,
              coords={
                  "time": time_var,
                  "y": y_var_new,
                  "x": x_var_new,
                   },          
        dims=["time", "x", "y"],
        attrs=dict(
            description="Radiance dataset",
            units_radiance="'mW m-2 sr-1 (cm-1)-1'",
            Rad_long_name= 'ABI L1b Radiances',
            Rad_standard_name = 'toa_outgoing:radiance_per_unit_wavenumber',
            Rad_sensor_band_bit_depth = '12',
            Rad_resolution ='',
            y_units = 'rad',
            y_axis = 'Y',
            y_long_name = 'GOES fixed grid projection y-coordinate',
            y_standard_name= ' projection_y_coordinate',
            x_units= 'rad',
            x_axis = 'X',
            x_long_name = 'GOES fixed grid projection y-coordinate',
            x_standard_name= ' projection_x_coordinate'
            
            
        
 )

)


radiance['radiance'] =(('time','x','y'), low_res_grid)
radiance.chunk(chunks = { "time" : 30,
                            "x" :  11,
                            "y" : 11 } )


radiance.to_netcdf(path="C:/Users/fd_25/Desktop/Project/GOES16-2022001/task.nc", 
                  mode='w') 
#                  engine={"h5netcdf"
 #                         }, 
  #                encoding={ "radiance" : {
   #                   "dtype": "float32",                         
    #                   "zlib": True,
     #                  'complevel':5} }
      #               )
