


import rasterio

def load_raster(filepath):
    """Load a raster file using rasterio."""
    return rasterio.open(filepath)

def save_raster(filepath, data, meta):
    """Save a raster using rasterio."""
    with rasterio.open(filepath, 'w', **meta) as dst:
        dst.write(data)
