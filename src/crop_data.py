import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def crop_data(file_path, lolabox, processed_dir):
    """
    Process and plot wind data within a specified bounding box and save the results.

    Parameters:
    - file_path: Path to the NetCDF file.
    - lolabox: Bounding box as a tuple (lon_min, lon_max, lat_min, lat_max).
    - img_dir: Directory to save images.
    - processed_dir: Directory to save processed NetCDF files.
    """
    # Load dataset
    for file in file_path:
        ds = xr.open_dataset(file)
        
        # Adjust longitude coordinates
        ds_expert = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180))
        
        # Subset the dataset based on the bounding box
        lolasubset = (
            (ds_expert.longitude >= lolabox[0]) &
            (ds_expert.longitude <= lolabox[1]) & 
            (ds_expert.latitude >= lolabox[2]) &
            (ds_expert.latitude <= lolabox[3])
        )
        
        if lolasubset.any():
            ds_expert_sub = ds_expert.where(lolasubset, drop=True)
            
            # Check if required variables exist
            required_vars = ['wind_speed_karin_2', 'wind_speed_model_u', 'wind_speed_model_v']
            if all(var in ds_expert_sub for var in required_vars):
    
                # Ensure output directories exist
                os.makedirs(processed_dir, exist_ok=True)
    
                # Save plot
                time_coverage_begin = ds_expert_sub.attrs['time_coverage_start']
                safe_time_coverage = time_coverage_begin.replace(':', '').replace('T', '_').replace('Z', '')
                
                # Save subset as NetCDF
                netcdf_file_path = os.path.join(processed_dir, f"SWOT_L2_LR_SSH_{safe_time_coverage}.nc")
                ds_expert_sub.to_netcdf(path=netcdf_file_path)
                
                print(f"Processed data. \nNetCDF: {netcdf_file_path}")
                
            else:
                missing_vars = [var for var in required_vars if var not in ds_expert_sub]
                print(f"Missing required variables in dataset: {missing_vars}")
        else:
            time_coverage_begin = ds.attrs['time_coverage_start']
            print(f"No data within the specified bounding box {time_coverage_begin}")

# Example usage
# file_path = "path/to/your/dataset.nc"  # Update this path
# lolabox = (-71.5, -69.5, 39.5, 43.5)  # Longitude and latitude bounds
# img_dir = "/path/to/save/images"  # Update this path
# processed_dir = "/path/to/save/processed/data"  # Update this path

# # Call the function with your dataset and desired parameters
# process_and_plot_data(file_path, lolabox, img_dir, processed_dir)
