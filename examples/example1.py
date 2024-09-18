import sys
import os

script_dir = os.path.dirname(__file__)
mymodule_dir1 = os.path.join(script_dir, '..', 'objects')
mymodule_dir2 = os.path.join(script_dir, '..', 'operators')
mymodule_dir3 = os.path.join(script_dir, '..', 'utils')
sys.path.append(mymodule_dir1)
sys.path.append(mymodule_dir2)
sys.path.append(mymodule_dir3)

from image import Image
from image_collection import ImageCollection
from reduce import reduce_image_collection
from spatial_utils import load_raster


img1 = Image('../data/sr1_INDIA_2017_18.tif')
# img2 = Image('../data/sr2_INDIA_2017_18.tif')
# rain1 = Image('../data/rain1_INDIA_2017_18_f.tif')

# print(img1.check_dimensions())
# print(img2.check_dimensions())
# print(rain1.check_dimensions())
# print(img1.get_resolution())

# print(rain1.get_data())

img_reprojected = img1.reproject(dst_crs='EPSG:3857', dst_resolution=(10, 10))

# # Save the reprojected image
img_reprojected.save('../data/reprojected_image.tif')