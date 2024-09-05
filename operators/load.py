import rasterio
import numpy as np
from ..objects.image import Image
from ..objects.image_collection import ImageCollection

class Loader:
    def __init__(self):
        pass

    def load(self, data):
        """
        Load data based on the type of input.

        Args:
            data (Image or list of Image): An Image object or a list of Image objects.
        """
        if isinstance(data, Image):
            # Single Image object
            return self._load_image(data)
        elif isinstance(data, list) and all(isinstance(d, Image) for d in data):
            # List of Image objects
            return self._load_image_collection(data)
        else:
            raise TypeError("Input must be an Image object or a list of Image objects.")

    def _load_image(self, image):
        """
        Load a single image from an Image object.

        Args:
            image (Image): An Image object.

        Returns:
            Image: The Image object with loaded data.
        """
        with rasterio.open(image.file_path) as src:
            data = src.read()
            image.data = data
        return image

    def _load_image_collection(self, image_objects):
        """
        Load multiple images from a list of Image objects.

        Args:
            image_objects (list of Image): List of Image objects.

        Returns:
            ImageCollection: An ImageCollection object with loaded data.
        """
        images = []
        for image in image_objects:
            with rasterio.open(image.file_path) as src:
                data = src.read()
                image.data = data
                images.append(image)
        
        return ImageCollection(image_path_list=[img.file_path for img in images], metadata_image_collection={"images": [img.file_path for img in images]})
