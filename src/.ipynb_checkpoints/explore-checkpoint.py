def load_dataset(subdir_name, file_pattern="*.nc"):
    """
    Load datasets from a specified subdirectory within the base directory.
    Assumes files are in NetCDF format.
    
    Parameters:
    - subdir_name: The name of the subdirectory (e.g., "L2_LR_windwave")
    - file_pattern: Pattern to match files within the subdirectory
    
    Returns:
    - A combined xarray Dataset of all files matching the pattern
    """
    path_pattern = os.path.join(base_dir, subdir_name, file_pattern)
    files = glob.glob(path_pattern)
    
    if not files:
        raise FileNotFoundError(f"No files found for pattern {path_pattern}")
    
    # Load and concatenate datasets
    ds_list = [xr.open_dataset(file) for file in files]
    combined_ds = xr.concat(ds_list, dim='time')
    
    return combined_ds

