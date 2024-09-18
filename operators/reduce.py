# reduce will polymorphic operator
# 1. (image_collection, function) -> image
# 2. (feature_collection, function) -> feature



def reduce_image(image, reducer):
    """Reduce an image using a reducer."""
    return image.reduce(reducer)

def reduce_image_collection(image_collection, reducer):
    """Reduce an image collection using a reducer."""
    return image_collection.reduce(reducer)

