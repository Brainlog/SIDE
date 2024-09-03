# reduce will polymorphic operator
# 1. (image_collection, function) -> image
# 2. (feature_collection, function) -> feature


from abc import ABC, abstractmethod
import cupy as cp

class Reducer(ABC):
    @abstractmethod
    def reduce(self, data):
        """
        Perform reduction on the given data.
        """
        pass

# reducer implementation for image collection 
class ImageCollectionReducer(Reducer):
    def reduce(self, image_collection):
        # Implement reduction logic specific to image collections
        pass


# reducer implementation for feature collection
class FeatureCollectionReducer(Reducer):
    def reduce(self, feature_collection):
        # Implement reduction logic specific to feature collections
        pass



class ImageReducer:
    def __init__(self, image_data):
        self.image_data = image_data

    def reduce_region(self, reduction_type):
        """
        Apply the specified reduction operation to the given region of the image.

        Args:
            region (tuple): A tuple (start_row, end_row, start_col, end_col) defining the region of interest.
            reduction_type (str): The type of reduction operation ('mean', 'sum').

        Returns:
            float or any other reduction result.
        """
        
        if reduction_type == 'mean':
            return cp.mean(self.image_data).get()  # Use .get() to move data from GPU to CPU
        elif reduction_type == 'sum':
            return cp.sum(self.image_data).get()  # Use .get() to move data from GPU to CPU
        elif reduction_type == 'min':
            return cp.min(self.image_data).get()  # Minimum value in the region
        elif reduction_type == 'max':
            return cp.max(self.image_data).get()  # Maximum value in the region
        elif reduction_type == 'std':
            return cp.std(self.image_data).get()  # Standard deviation of values
        elif reduction_type == 'median':
            return cp.median(self.image_data).get()  # Median value of the region
        else:
            raise ValueError("Unsupported reduction type. Use 'mean', 'sum', 'min', 'max', 'std', or 'median'.")
        
    
    def reduce(self, reduction_type):
        """
        Apply the specified reduction operation across the bands of the image.
        
        Args:
            reduction_type (str): The type of reduction operation ('max', 'min', etc.).

        Returns:
            cupy.ndarray: A 2D array where each pixel value is the result of the reduction
                          applied across the bands.
        """
        if reduction_type == 'max':
            # Reduce across the bands (axis=-1) to get the max value for each pixel
            return cp.max(self.image_data, axis=-1)
        elif reduction_type == 'min':
            # Reduce across the bands (axis=-1) to get the min value for each pixel
            return cp.min(self.image_data, axis=-1)
        elif reduction_type == 'mean':
            # Compute the mean across the bands (axis=-1) for each pixel
            return cp.mean(self.image_data, axis=-1)
        elif reduction_type == 'sum':
            # Compute the sum across the bands (axis=-1) for each pixel
            return cp.sum(self.image_data, axis=-1)
        else:
            raise ValueError(f"Unsupported reduction type '{reduction_type}'. Supported types are 'max', 'min', 'mean', and 'sum'.")



# centeral class to manage all the reducer type may be used
class ReducerManager:
    def __init__(self):
        self.reducers = {
            'image': ImageReducer(),
            'image_collection': ImageCollectionReducer(),
            'feature_collection': FeatureCollectionReducer()
        }
    
    def get_reducer(self, data_type):
        return self.reducers.get(data_type)
