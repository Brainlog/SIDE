import rasterio
import numpy as np
from datetime import datetime
from shapely.geometry import box
from geometry import Geometry
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.enums import Resampling
import random
import copy

class Image:
    def __init__(self, file_path):
        """Initialize the Image class with metadata extracted from the .tif file."""
        self.file_path = file_path
        self.geometry = None
        self.timestamp = None
        self.height = None
        self.width = None
        self.bands = None
        self.datatype = None
        self.data = None
        self.metadata = None
        self.crs = None
        if(file_path != None):
            self._extract_metadata()

    def _extract_metadata(self):
        """Extract metadata from the .tif file."""
        with rasterio.open(self.file_path) as src:
            self.height = src.height
            self.width = src.width
            self.bands = src.count
            self.datatype = src.dtypes[0]
            self.metadata = src.meta.copy()
            self.timestamp = datetime.strptime(src.tags().get('TIFFTAG_DATETIME', '1970:01:01 00:00:00'), '%Y:%m:%d %H:%M:%S')
            self.crs = src.crs
            # deep copy src.bounds
            self.bounds = copy.deepcopy(src.bounds)
            # Create a default geometry from the bounds of the raster
            self.geometry = Geometry(self._create_geometry(src.bounds))

    def _create_geometry(self, bounds):
        """Create a default geometry from the raster bounds."""
        minx, miny, maxx, maxy = bounds
        return box(minx, miny, maxx, maxy)
    
    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
    
    def reproject(self, dst_crs, dst_res):
        """
        Reproject a TIFF image to a new CRS and scale.

        Args:
            dst_crs (str): The target CRS (e.g., 'EPSG:4326').
            dst_transform (affine.Affine): The target affine transform.
            dst_res (float): The target resolution (scale).
        """
        if(dst_crs == None):
            dst_crs = self.crs
        src = self.metadata
        metadata = src.meta.copy()
        transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds, resolution=dst_res)
        metadata.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        s = random.randint(1000, 9999)
        output_file_path = f'./projected_{s}.tif'
        with rasterio.open(output_file_path, 'w', **metadata) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.bilinear
                )
        self.file_path = output_file_path
        self.data = None
            
            
    
    
    

