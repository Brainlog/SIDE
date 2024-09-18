# Reproject Semantics : 
# (Input Numpy Image handle, Projection) -> Output Numpy Image handle




def reproject_image(image, dst_crs):
    """Reproject the image to a new CRS."""
    return image.reproject(dst_crs)
