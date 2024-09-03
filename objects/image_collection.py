## class image_collection interface
## fields : image_object_list, metadata_image_collection


import cupy as cp
# from operators.reduce import ImageCollectionReducer
from objects.image import Image


class ImageCollection:
    def __init__(self, metadata_image_collection=None):
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

    def add_image(self, image):
        """
        Add an Image object to the collection.

        Args:
            image (Image): The Image object to be added.
        
        Raises:
            ValueError: If the image's dimensions don't match the existing images in the collection.
        """
        if not self.image_object_list:
            # If the collection is empty, initialize the dimensions based on the first image
            self.height, self.width, self.bands = image.get_height(), image.get_width(), image.get_bands()
        else:
            # Check if the new image matches the dimensions of the existing images
            if (image.get_height() != self.height or
                image.get_width() != self.width or
                image.get_bands() != self.bands):
                raise ValueError("Image dimensions do not match the existing images in the collection.")

        self.image_object_list.append(image)

    def remove_image(self, index):
        """
        Remove an Image object from the collection by its index.

        Args:
            index (int): The index of the Image object to be removed.
        """
        if 0 <= index < len(self.image_object_list):
            self.image_object_list.pop(index)
        else:
            raise IndexError("Index out of range")

    def get_image(self, index):
        """
        Retrieve an Image object from the collection by its index.

        Args:
            index (int): The index of the Image object to retrieve.

        Returns:
            Image: The Image object at the specified index.
        """
        if 0 <= index < len(self.image_object_list):
            return self.image_object_list[index]
        else:
            raise IndexError("Index out of range")

    def size(self):
        """
        Get the number of images in the collection.

        Returns:
            int: The number of Image objects in the collection.
        """
        return len(self.image_object_list)

    def get_metadata(self):
        """
        Get the metadata of the image collection.

        Returns:
            dict: The metadata of the collection.
        """
        return self.metadata_image_collection

    def set_metadata(self, metadata):
        """
        Set the metadata for the image collection.

        Args:
            metadata (dict): Metadata to set for the collection.
        """
        self.metadata_image_collection = metadata


## Example how to create an image collection
# if __name__ == "__main__":
#     # Example metadata for the image collection
#     collection_metadata = {
#         "timestamp": "2024-09-03T12:00:00Z",
#         "collection_name": "Satellite Images Collection",
#     }

#     # Initialize an ImageCollection
#     image_collection = ImageCollection(metadata_image_collection=collection_metadata)

#     # Example Image objects with the same dimensions
#     image1 = Image(height=1000, width=1000, bands=3, datatype="float32", data=cp.zeros((1000, 1000, 3)))
#     image2 = Image(height=1000, width=1000, bands=3, datatype="float32", data=cp.ones((1000, 1000, 3)))

#     # Add images to the collection
#     image_collection.add_image(image1)
#     image_collection.add_image(image2)

#     # Example of an image with different dimensions (this will raise an error)
#     try:
#         image3 = Image(height=500, width=500, bands=3, datatype="float32", data=cp.ones((500, 500, 3)))
#         image_collection.add_image(image3)
#     except ValueError as e:
#         print(f"Error: {e}")

#     # Get metadata and size of the collection
#     print("Collection Metadata:", image_collection.get_metadata())
#     print("Number of images in collection:", image_collection.size())
