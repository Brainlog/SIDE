import os
from rasterio.merge import merge
import rasterio

class Loader:
    def __init__(self):
        pass
    
    def load_image_collection(self, paths):
        paths = list(set(paths))
        images = []
        for path in paths:
            all_files = os.listdir(path)
            temp_images = []
            for fil in all_files:
                file_loc = os.path.join(path, fil)
                img = rasterio.open(file_loc)
                temp_images.append(img)
            merged_data, merged_transform = merge(temp_images)
            images.append([merged_data, merged_transform])
        return images
                    
    def load_image(path):
        path = list(set(path))
        all_files = os.listdir(path)
        temp_images = []
        for fil in all_files:
            file_loc = os.path.join(path, fil)
            img = rasterio.open(file_loc)
            temp_images.append(img)
        merged_data, merged_transform = merge(temp_images)
        return [merged_data, merged_transform]
        
    
    def load_feature_collection(path):
        pass
    
