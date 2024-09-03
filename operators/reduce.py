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


class ImageCollectionReducer(Reducer):
    def reduce(self, image_collection):
        # Implement reduction logic specific to image collections
        pass

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
        else:
            raise ValueError("Unsupported reduction type. Use 'mean' or 'sum'.")

class ReducerManager:
    def __init__(self):
        self.reducers = {
            'image': ImageReducer(),
            'image_collection': ImageCollectionReducer(),
            'feature_collection': FeatureCollectionReducer()
        }
    
    def get_reducer(self, data_type):
        return self.reducers.get(data_type)
