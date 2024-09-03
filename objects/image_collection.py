## class image_collection interface
## fields : image_object_list, metadata_image_collection


import cupy as cp
# from operators.reduce import ImageCollectionReducer
from objects.image import Image


class ImageCollection:
    def __init__(self, image_list, metadata_image_collection=None):
        """
        Initialize an ImageCollection.

        Args:
            metadata_image_collection (dict, optional): Metadata for the image collection.
        """
        self.image_object_list = []
        self.metadata_image_collection = metadata_image_collection or {}
        self.height = None
        self.width = None
        self.bands = None

        self.image_list = image_list
        self._check_dimensions()

        # Move all images to GPU
        self.image_data_list = [cp.array(image.get_data()) for image in self.image_list]

    def _check_dimensions(self):
        if not all(image.get_height() == self.image_list[0].get_height() and
                   image.get_width() == self.image_list[0].get_width() for image in self.image_list):
            raise ValueError("Not all images in the collection have the same dimensions.")

    
