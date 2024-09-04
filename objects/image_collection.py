## class image_collection interface
## fields : image_object_list, metadata_image_collection


import cupy as cp
from operators.reduce import ImageCollectionReducer
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
        self.stacked_image_data = cp.stack([cp.array(image.get_data()) for image in self.image_list], axis=-1)
        self.reducer = ImageCollectionReducer(self.stacked_image_data)


        

    def _check_dimensions(self):
        if not all(image.get_height() == self.image_list[0].get_height() and
                   image.get_width() == self.image_list[0].get_width() for image in self.image_list):
            raise ValueError("Not all images in the collection have the same dimensions.")
        
    def check_shape(self):

        return self.stacked_image_data.shape
    
    def reduce(self, reduction_type):
        """
        Apply reduction operation on a specified region of the image collection.

        Args:
            reduction_type (str): The type of reduction operation ('mean', 'sum').
            region (tuple): A tuple (start_row, end_row, start_col, end_col) defining the region of interest. (todo)

        Returns:
            (height, width, bands): The result of the reduction operation.
        """
        return self.reducer.reduce(reduction_type)

    
    def map(self, func):
        """
        Apply a function to each image in the stack.

        Args:
            stacked_images (cupy.ndarray): Stacked image array with shape (height, width, bands, images).
            func (callable): Function to apply. It should accept NIR and RED bands as inputs.
        
        Returns:
            (height, width, number of images) : A new image collection having only one band
        """
        height, width, bands, num_images = self.stacked_image_data.shape
        new_images = cp.empty((height, width, num_images))  # Prepare an empty array for results
        
        for i in range(num_images):
            # Extract the NIR and RED bands for the current image
            nir = self.stacked_image_data[..., 0, i]  # Example: assuming band 0 is NIR
            red = self.stacked_image_data[..., 1, i]  # Example: assuming band 1 is RED
            
            # Apply the function
            new_images[..., i] = func(nir, red)
        
        return new_images
        
    

def calculate_ndvi(nir, red):
    """
    Calculate NDVI from NIR and RED bands.
    
    Args:
        nir (cupy.ndarray): NIR band image.
        red (cupy.ndarray): RED band image.
    
    Returns:
        cupy.ndarray: NDVI image.
    """
    return (nir - red) / (nir + red)

# only user can handle how to write the vectorized mapping
# def second_way_to_implement_map():
#     """
#     Calculate NDVI for a stack of images.

#     Args:
#         stacked_images (cupy.ndarray): Stacked image array with shape (height, width, bands, images).
    
#     Returns:
#         cupy.ndarray: NDVI image stack.
#     """
#     # Assume band 0 is NIR and band 1 is RED
#     nir_band = stacked_images[..., 0, :]  # Extract NIR band from all images
#     red_band = stacked_images[..., 1, :]  # Extract RED band from all images
    
#     # Calculate NDVI using vectorized operations
#     ndvi_stack = (nir_band - red_band) / (nir_band + red_band + cp.finfo(cp.float32).eps)  # Adding epsilon to avoid division by zero
    
#     return ndvi_stack

    

## Example Usage of reducer functionality
if __name__ == "__main__":

    height, width, bands = 3, 3, 3
    data = cp.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                     [[9, 8, 7], [6, 5, 4], [3, 2, 1]],
                     [[1, 4, 7], [2, 5, 8], [3, 6, 9]]], dtype=cp.float32)

    image1 = Image(height=height, width=width, bands=bands, datatype="float32", data=data)
    image2 = Image(height=height, width=width, bands=bands, datatype="float32", data=data)

    print(f"image1 {image1.get_data()}")
    print(f"image2 {image2.get_data()}")

    image_collection = ImageCollection([image1, image2])

    # print(f"image collection shape {image_collection.check_shape()}")

    # min_image = image_collection.reduce('sum')

    # print(f"reduce image collection {min_image}")

    ndvi_image = image_collection.map(calculate_ndvi)

    print(f"ndvi image shape {ndvi_image.shape}")


    


        
    

    
