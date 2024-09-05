# map will be polymorphic operator
# 1. (image_collection, function) -> image_collection
# 2. (feature_collection, function) -> feature_collection

import sys
import os

script_dir = os.path.dirname(__file__)
mymodule_dir1 = os.path.join(script_dir, '..', 'objects')
mymodule_dir2 = os.path.join(script_dir, '..', 'operators')
sys.path.append(mymodule_dir1)
sys.path.append(mymodule_dir2)

from image_collection import ImageCollection
from image import Image
import copy

class Mapper():


    def __init__(self):
        pass

    def map_image_collection(self, image_collection, func):
        """
        Apply the given function to each image in the ImageCollection.

        Args:
            image_collection (ImageCollection): The collection of images.
            func (function): A function that takes an image (NumPy array) and returns a transformed image.
        
        Returns:
            ImageCollection: A new ImageCollection with transformed images.
        """
        transformed_images = []
        
        # Iterate through each image in the ImageCollection
        for image in image_collection.image_object_list:
            
            # Apply the function to the image's data
            transformed_data = func(image.data)
            new_image = copy.deepcopy(image)
            
            # Set the transformed data in the new image object
            new_image.data = transformed_data
            
            # Add the new image to the list of transformed images
            transformed_images.append(new_image)
        
        # Return a new ImageCollection with the transformed images
        return ImageCollection(transformed_images, image_path_list=None, metadata_image_collection=None) # todo image path and metadata

    
    def map_image(self, image, func):
        """
        Apply the given function to image

        Args:
            image: The single of image.
            func (function): A function that take an image and returns a transformed image.
        
        Returns:
            Image: A new transformed image
        """

        transformed_data = func(image.data)

        # Create a new Image object to store the transformed image
        transformed_image = copy.deepcopy(image)
        transformed_image.data = transformed_data
        
        return transformed_image
    
    def map(self, obj, func):

        if isinstance(obj, Image):
            self.map_image(obj, func)
        elif isinstance(obj, ImageCollection):
            self.map_image_collection(obj, func)
        else:
            raise ValueError(f"Unsupported object type. Supported types Image, ImageCollection")






    