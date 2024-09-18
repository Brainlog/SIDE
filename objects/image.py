import random
import rasterio
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, Resampling

class Image:
    def __init__(self, filepath):
        """Initialize the Image object from a raster file."""
        self.filepath = filepath
        self.dataset = rasterio.open(filepath)
        self.data = self.dataset.read()  # Load raster data as a NumPy array

    def reduce(self, reducer):
        """Apply a reduction function (e.g., mean, max) over the raster bands."""
        if reducer == 'mean':
            return np.mean(self.data, axis=0)
        elif reducer == 'max':
            return np.max(self.data, axis=0)
        elif reducer == 'min':
            return np.min(self.data, axis=0)
        else:
            raise ValueError("Unsupported reducer")
    
    def check_dimensions(self):
        """Check and return the dimensions of the image (bands, height, width)."""
        bands = self.dataset.count
        height = self.dataset.height
        width = self.dataset.width
        return bands, height, width
    
    def get_data(self):
        return self.data
    

    def map(self, func):
        """Apply a custom function to each pixel in the image."""
        return func(self.data)

    def save(self, output_filepath):
        """Save the current image data to a new file."""
        with rasterio.open(output_filepath, 'w', **self.dataset.meta) as dst:
            dst.write(self.data)

    def get_resolution(self):
        """
        Returns the resolution of the image in the units of its CRS.

        Returns:
            tuple: A tuple containing the x and y resolution (width and height of a pixel) in the image's CRS units.
        """
        return self.dataset.res

    def reproject(self, dst_crs, dst_resolution=None):
        """Reproject the image to a new CRS and optionally resample to a new resolution.
        
        Args:
            dst_crs (str or dict): The destination coordinate reference system.
            dst_resolution (tuple or float, optional): The desired output resolution in the form 
                                                       (x_resolution, y_resolution) or a single float 
                                                       for uniform resolution in both directions.
        """
        transform, width, height = calculate_default_transform(
            self.dataset.crs, dst_crs, self.dataset.width, self.dataset.height, *self.dataset.bounds, resolution=dst_resolution
        )

        kwargs = self.dataset.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        reprojected_data = np.empty((self.dataset.count, height, width), dtype=self.dataset.dtypes[0])

        for i in range(1, self.dataset.count + 1):
            reproject(
                source=rasterio.band(self.dataset, i),
                destination=reprojected_data[i - 1],
                src_transform=self.dataset.transform,
                src_crs=self.dataset.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest  # You can change the resampling method here
            )
        
        self.data = reprojected_data
        self.dataset.close()
        return self
    
    # def reproject(self, dst_crs, dst_res):
    #     """
    #     Reproject a TIFF image to a new CRS and scale.

    #     Args:
    #         dst_crs (str): The target CRS (e.g., 'EPSG:4326').
    #         dst_transform (affine.Affine): The target affine transform.
    #         dst_res (float): The target resolution (scale).
    #     """
    #     if(dst_crs == None):
    #         dst_crs = self.crs
    #     src = self.metadata
    #     metadata = src.meta.copy()
    #     transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds, resolution=dst_res)
    #     metadata.update({
    #         'crs': dst_crs,
    #         'transform': transform,
    #         'width': width,
    #         'height': height
    #     })
    #     s = random.randint(1000, 9999)
    #     output_file_path = f'./projected_{s}.tif'
    #     with rasterio.open(output_file_path, 'w', **metadata) as dst:
    #         for i in range(1, src.count + 1):
    #             reproject(
    #                 source=rasterio.band(src, i),
    #                 destination=rasterio.band(dst, i),
    #                 src_transform=src.transform,
    #                 src_crs=src.crs,
    #                 dst_transform=transform,
    #                 dst_crs=dst_crs,
    #                 resampling=Resampling.bilinear
    #             )
    #     self.file_path = output_file_path
    #     self.data = None
