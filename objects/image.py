import rasterio
import numpy as np
from datetime import datetime
from shapely.geometry import box
from geometry import Geometry

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
        self._extract_metadata()

    def _extract_metadata(self):
        """Extract metadata from the .tif file."""
        with rasterio.open(self.file_path) as src:
            self.height = src.height
            self.width = src.width
            self.bands = src.count
            self.datatype = src.dtypes[0]
            self.timestamp = datetime.strptime(src.tags().get('TIFFTAG_DATETIME', '1970:01:01 00:00:00'), '%Y:%m:%d %H:%M:%S')
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
    

