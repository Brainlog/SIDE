# map will be polymorphic operator
# 1. (image_collection, function) -> image_collection
# 2. (feature_collection, function) -> feature_collection

from objects.image_collection import ImageCollection
from objects.image import Image
import copy

class Map():


    def __init__(self):
        pass

    def map(self, image_collection, func):
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

    
    def map(self, image, func):
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






    