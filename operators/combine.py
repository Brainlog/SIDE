# Combine will be polymorphic, and will be able to combine any two
# (image_collection1, image_collection2) -> image_collection
# (image1, image2) -> image (consider each pixel as a scope's row)
# (feature_collection1, feature_collection2) -> feature_collection
import copy
from ..objects.image import Image

class Combiner:
    def __init__(self):
        pass
    
    def combine(Image1, Image2):
        image = copy.deepcopy(Image1)
        image.data = Image1.data + Image2.data
        image.file_path = None
        image.temp_path = None
        return image