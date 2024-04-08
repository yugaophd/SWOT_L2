import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def crop_and_plot_data(file_path, lolabox, img_dir, processed_dir):
    """
    Process and plot data within a specified bounding box and save the results.

    Parameters:
    - file_path: Path to the NetCDF file.
    - lolabox: Bounding box as a tuple (lon_min, lon_max, lat_min, lat_max).
    - img_dir: Directory to save images.
    - processed_dir: Directory to save processed NetCDF files.
    """
    # Load dataset
    ds_21day = xr.open_dataset(file_path)
    
    # Adjust longitude coordinates
    ds_expert = ds_21day.assign_coords(longitude=(((ds_21day.longitude + 180) % 360) - 180))
    
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
        if 'ssha' in ds_expert_sub and 'ssha_noiseless' in ds_expert_sub:
            # Initialize figure and axes
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
            
            # Plot settings
            plot_settings = dict(vmin=-0.5, vmax=0.5, cmap='viridis', transform=ccrs.PlateCarree())
            
            # Plot data
            ds_expert_sub.ssha.plot(ax=ax1, **plot_settings)
            ds_expert_sub.ssha_noiseless.plot(ax=ax2, **plot_settings)
            
            # Set titles and add coastlines
            ax1.set_title('Sea Surface Height Anomaly')
            ax2.set_title('Sea Surface Height Anomaly Noiseless')
            for ax in [ax1, ax2]:
                ax.coastlines()
                ax.gridlines(draw_labels=True)
            
            # Ensure output directories exist
            os.makedirs(img_dir, exist_ok=True)
            os.makedirs(processed_dir, exist_ok=True)
            
            # Extract and format time_coverage_begin for file naming
            time_coverage_begin = ds_expert_sub.attrs['time_coverage_begin']
            safe_time_coverage = time_coverage_begin.replace(':', '').replace('T', '_').replace('Z', '')
            
            # Save plot
            img_file_path = os.path.join(img_dir, f"SSHA_{safe_time_coverage}.png")
            plt.savefig(img_file_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            # Save subset as NetCDF
            netcdf_file_path = os.path.join(processed_dir, f"SSH_SWOT_L3_{safe_time_coverage}.nc")
            ds_expert_sub.to_netcdf(path=netcdf_file_path)
            
            print(f"Processed data and plot saved. \nImage: {img_file_path} \nNetCDF: {netcdf_file_path}")
        else:
            print("Missing 'ssha' or 'ssha_noiseless' in dataset.")
    else:
        print("No data within the specified bounding box.")

# Example usage
# file_path = "path/to/your/dataset.nc"  # Update this path
# lolabox = (-71.5, -69.5, 39.5, 43.5)  # Longitude and latitude bounds
# img_dir = "/path/to/save/images"  # Update this path
# processed_dir = "/path/to/save/processed/data"  # Update this path

# # Call the function with your dataset and desired parameters
# process_and_plot_data(file_path, lolabox, img_dir, processed_dir)
