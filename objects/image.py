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
            region (tuple): A tuple (start_row, end_row, start_col, end_col) defining the region of interest. (todo)

        Returns:
            float: The result of the reduction operation.
        """
        return self.reducer.reduce_region(reduction_type)

    def reduce(self, reduction_type):
        """
        Apply reduction operation on a specified region of the image.

        Args:
            reduction_type (str): The type of reduction operation ('mean', 'sum').
            region (tuple): A tuple (start_row, end_row, start_col, end_col) defining the region of interest. (todo)

        Returns:
            float: The result of the reduction operation.
        """
        return self.reducer.reduce(reduction_type)


# Example Usage of reduce_region functionality
# if __name__ == "__main__":
#     # Create an example image using random data
#     height, width, bands = 1000, 1000, 1
#     data = cp.zeros((height, width, bands))
    
#     # Initialize the Image object
#     image = Image(height=height, width=width, bands=bands, datatype="float32", data=data)
    
#     # Accessing the image metadata and data
#     print("Timestamp:", image.get_timestamp())
#     print("Height:", image.get_height())
#     print("Width:", image.get_width())
#     print("Bands:", image.get_bands())
#     print("Datatype:", image.get_datatype())
    
#     print("image data : ", image.reduce_region("max"))


## Example of reducer functionality
# if __name__ == "__main__":
#     # Create a small test image (3x3 pixels with 3 bands)
#     height, width, bands = 3, 3, 3
#     data = cp.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
#                      [[9, 8, 7], [6, 5, 4], [3, 2, 1]],
#                      [[1, 4, 7], [2, 5, 8], [3, 6, 9]]], dtype=cp.float32)
    
#     image = Image(height=height, width=width, bands=bands, datatype="float32", data=data)
    
#     # Print the input data
#     print("Input Image Data:")
#     print(data.get())  # Use .get() to bring data to the CPU for display

#     # Initialize the ImageReducer object

#     # Perform max reduction across the bands
#     max_value_image = image.reduce("max")
#     print("\nMax value image:")
#     print(max_value_image.get())  # Use .get() to bring data to the CPU for display

#     # Perform min reduction across the bands
#     min_value_image = image.reduce("min")
#     print("\nMin value image:")
#     print(min_value_image.get())  # Use .get() to bring data to the CPU for display

#     # Perform mean reduction across the bands
#     mean_value_image = image.reduce("mean")
#     print("\nMean value image:")
#     print(mean_value_image.get())  # Use .get() to bring data to the CPU for display

#     # Perform sum reduction across the bands
#     sum_value_image = image.reduce("sum")
#     print("\nSum value image:")
#     print(sum_value_image.get())  # Use .get() to bring data to the CPU for display



