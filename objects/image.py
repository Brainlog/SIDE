## class image interface
## fields : timestamp, height, widht, bands, datatype, data, temp_path, geometry object
## methods : get_timestamp, get_height, get_width, get_bands, get_datatype, get_data, get_temp_path, set_temp_path, get_geometry, set_geometry


import cupy as cp
import datetime
from operators.reduce import ImageReducer

class Image:
    """
    A class representing an image with various metadata and image data.
    
    Fields:
    - timestamp (datetime): The timestamp when the image was created or processed.
    - height (int): The height of the image.
    - width (int): The width of the image.
    - bands (int): The number of bands in the image (e.g., RGB would have 3 bands).
    - datatype (str): The type of data in the image (e.g., 'float32', 'uint8').
    - data (cupy.ndarray): The image data stored as a CuPy array.
    - temp_path (str): The temporary file path where the image might be stored.
    - geometry_object (object): A geometry object representing the region of interest (ROI) or shape.
    """

    def __init__(self, height, width, bands, datatype, data, temp_path=None, geometry_object=None):
        self.timestamp = datetime.datetime.now()  # Automatically set the current timestamp
        self.height = height
        self.width = width
        self.bands = bands
        self.datatype = datatype
        self.data = data
        self.temp_path = temp_path
        self.geometry_object = geometry_object
        self.reducer = ImageReducer(data)

    # Getter methods
    def get_timestamp(self):
        return self.timestamp
    
    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
    
    def get_bands(self):
        return self.bands
    
    def get_datatype(self):
        return self.datatype
    
    def get_data(self):
        return self.data
    
    def get_temp_path(self):
        return self.temp_path
    
    def get_geometry(self):
        return self.geometry_object
    
    # Setter methods
    def set_temp_path(self, temp_path):
        self.temp_path = temp_path
    
    def set_geometry(self, geometry_object):
        self.geometry_object = geometry_object
    
    def reduce_region(self, reduction_type):
        """
        Apply reduction operation on a specified region of the image.

        Args:
            reduction_type (str): The type of reduction operation ('mean', 'sum').
            region (tuple): A tuple (start_row, end_row, start_col, end_col) defining the region of interest.

        Returns:
            float: The result of the reduction operation.
        """
        return self.reducer.reduce_region(reduction_type)


# Example Usage
if __name__ == "__main__":
    # Create an example image using random data
    height, width, bands = 1000, 1000, 1
    data = cp.zeros((height, width, bands))
    
    # Initialize the Image object
    image = Image(height=height, width=width, bands=bands, datatype="float32", data=data)
    
    # Accessing the image metadata and data
    print("Timestamp:", image.get_timestamp())
    print("Height:", image.get_height())
    print("Width:", image.get_width())
    print("Bands:", image.get_bands())
    print("Datatype:", image.get_datatype())
    
    print("image data : ", image.reduce_region("mean"))

