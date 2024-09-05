# reduce will polymorphic operator
# 1. (image_collection, function) -> image
# 2. (feature_collection, function) -> feature

import sys
import os

script_dir = os.path.dirname(__file__)
mymodule_dir1 = os.path.join(script_dir, '..', 'objects')
mymodule_dir2 = os.path.join(script_dir, '..', 'operators')
sys.path.append(mymodule_dir1)
sys.path.append(mymodule_dir2)

from abc import ABC, abstractmethod
import cupy as np
from image_collection import ImageCollection
from image import Image
import numpy as np
import copy

class Reducer(ABC):
    @abstractmethod
    def reduce(self, data):
        """
        Perform reduction on the given data.
        """
        pass


class Reducer():
    def __init__(self):
        pass

    def reduce_region(self, image, reduction_type):
        """
        Apply the specified reduction operation to the given region of the image.

        Args:
            region (tuple): A tuple (start_row, end_row, start_col, end_col) defining the region of interest.
            reduction_type (str): The type of reduction operation ('mean', 'sum').

        Returns:
            float or any other reduction result.
        """
        new_image = copy.deepcopy(image)
        if reduction_type == 'mean':
            new_image.data = np.mean(image) 
        elif reduction_type == 'sum':
            new_image.data =  np.sum(image).get()  # Use .get() to move data from GPU to cpu
        elif reduction_type == 'min':
            new_image.data =  np.min(image).get()  # Minimum value in the region
        elif reduction_type == 'max':
            new_image.data =  np.max(image).get()  # Maximum value in the region
        elif reduction_type == 'std':
            new_image.data =  np.std(image).get()  # Standard deviation of values
        elif reduction_type == 'median':
            new_image.data =  np.median(image).get()  # Median value of the region
        else:
            raise ValueError("Unsupported reduction type. Use 'mean', 'sum', 'min', 'max', 'std', or 'median'.")
        
        return new_image
        
    
    def reduce_image(self, image, reduction_type):
        """
        Apply the specified reduction operation across the bands of the image.
        
        Args:
            reduction_type (str): The type of reduction operation ('max', 'min', etc.).

        Returns:
            cupy.ndarray: A 2D array where each pixel value is the result of the reduction
                          applied across the bands.
        """
        new_image = copy.deepcopy(image)
        if reduction_type == 'max':
            # Reduce across the bands (axis=-1) to get the max value for each pixel
            new_image =  np.max(image, axis=-1)
        elif reduction_type == 'min':
            # Reduce across the bands (axis=-1) to get the min value for each pixel
            new_image =  np.min(image, axis=-1)
        elif reduction_type == 'mean':
            # Compute the mean across the bands (axis=-1) for each pixel
            new_image =  np.mean(image, axis=-1)
        elif reduction_type == 'sum':
            # Compute the sum across the bands (axis=-1) for each pixel
            new_image =  np.sum(image, axis=-1)
        else:
            raise ValueError(f"Unsupported reduction type '{reduction_type}'. Supported types are 'max', 'min', 'mean', and 'sum'.")
        
        return new_image
        

    def reduce_image_collection(self, image_collection, reduction_type):
        """
        Apply the specified reduction operation across the bands of the image.
        
        Args:
            reduction_type (str): The type of reduction operation ('max', 'min', etc.).

        Returns:
            cupy.ndarray: A (height, width, bands) array where each pixel value is the result of the reduction
                          applied across the bands.
        """
        new_image = Image(file_path=None)
        if reduction_type == 'max':
            # Reduce across the bands (axis=-1) to get the max value for each pixel
            new_image =  np.max(image_collection, axis=-1)
        elif reduction_type == 'min':
            # Reduce across the bands (axis=-1) to get the min value for each pixel
            new_image =  np.min(image_collection, axis=-1)
        elif reduction_type == 'mean':
            # Compute the mean across the bands (axis=-1) for each pixel
            new_image =  np.mean(image_collection, axis=-1)
        elif reduction_type == 'sum':
            # Compute the sum across the bands (axis=-1) for each pixel
            new_image =  np.sum(image_collection, axis=-1)
        else:
            raise ValueError(f"Unsupported reduction type '{reduction_type}'. Supported types are 'max', 'min', 'mean', and 'sum'.")

        return new_image



    def reducer(self, obj, func):

        if isinstance(obj, Image):
            self.reduce_image(obj, func)
        elif isinstance(obj, ImageCollection):
            self.reduce_image_collection(obj, func)
        else:
            raise ValueError(f"Unsupported object type. Supported types Image, ImageCollection")