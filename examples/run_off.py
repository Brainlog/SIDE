import sys
import os

script_dir = os.path.dirname(__file__)
mymodule_dir1 = os.path.join(script_dir, '..', 'objects')
mymodule_dir2 = os.path.join(script_dir, '..', 'operators')
sys.path.append(mymodule_dir1)
sys.path.append(mymodule_dir2)

from combine import Combiner
from image import Image
from image_collection import ImageCollection
from load import Loader
from map import Mapper
from reduce import Reducer


sr1 = Image(file_path="../images/sr1_INDIA_2017_18.tif")
sr2 = Image(file_path="../images/sr2_INDIA_2017_18.tif")
sr3 = Image(file_path="../images/sr3_INDIA_2017_18.tif")
rains1 = ImageCollection(['../images/rain1_INDIA_2017_18_f.tif', '../images/rain2_INDIA_2017_18_f.tif', '../images/rain3_INDIA_2017_18_f.tif', '../images/rain4_INDIA_2017_18_f.tif', '../images/rain5_INDIA_2017_18_f.tif'])
rains2 = ImageCollection(['../images/rain3_INDIA_2017_18_f.tif', '../images/rain4_INDIA_2017_18_f.tif', '../images/rain5_INDIA_2017_18_f.tif'])
loader = Loader()
sr1 = loader.load(sr1)
sr2 = loader.load(sr2)
sr3 = loader.load(sr3)
rains1 = loader.load(rains1)
rains2 = loader.load(rains2)

reducer = Reducer()
reduced_rain1 = reducer.reduce_image_collection(rains1, 'mean')
reduced_rain2 = reducer.reduce_image_collection(rains2, 'mean')

rain1_reprojected = reduced_rain1.reproject(None, 30)
rain2_reprojected = reduced_rain2.reproject(None, 30)

combiner = Combiner()
m1 = combiner.combine([sr1, rain1_reprojected])
m2 = combiner.combine([sr2, rain1_reprojected])
m3 = combiner.combine([sr3, rain2_reprojected])
runoff = combiner.combine([m1, m2, m3, sr1, sr2, sr3, rain1_reprojected, rain2_reprojected])

print(runoff)


