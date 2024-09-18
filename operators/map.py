# map will be polymorphic operator
# 1. (image_collection, function) -> image_collection
# 2. (feature_collection, function) -> feature_collection

def map_image(image, func):
    """Apply a function to an image."""
    return image.map(func)

def map_image_collection(image_collection, func):
    """Apply a function to each image in the collection."""
    return image_collection.map(func)





    