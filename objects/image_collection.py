## class image_collection interface
## fields : image_object_list, metadata_image_collection

import cupy as cp
from image import Image


class ImageCollection:
    def __init__(self, image_path_list, metadata_image_collection=None):
        """
        Initialize an ImageCollection.

        Args:
            metadata_image_collection (dict, optional): Metadata for the image collection.
        """
        self.image_object_list = None
        self.metadata_image_collection = metadata_image_collection or {}
        self.image_list = image_path_list
        self._check_dimensions()

    def set_image_object_list(self, image_object_list):
        self.image_object_list = image_object_list
    


        
    

    
