import numpy as np

class ImageCollection:
    def __init__(self, image_list):
        """Initialize with a list of Image objects."""
        self.images = image_list

    def map(self, func):
        """Apply a function to each image in the collection."""
        return [func(image) for image in self.images]

    def reduce(self, reducer):
        """Reduce the collection by applying a reduction function across images."""
        data_stack = np.array([image.data for image in self.images])
        
        if reducer == 'mean':
            return np.mean(data_stack, axis=0)
        elif reducer == 'max':
            return np.max(data_stack, axis=0)
        elif reducer == 'min':
            return np.min(data_stack, axis=0)
        else:
            raise ValueError("Unsupported reducer")
