<!-- # SIDE (Satellite Images Dataflow Engine) -->


## Semantics of SIDE operators : 
- Images state level
- Extractor = (filepaths) -> (Image_Collection)
            = (filepath) -> (Image)
            = (filepath) -> (FeatureCollection)

- Clipper = (Image) -> (Image)
- Reprojector = (Image) -> (Image)

- Mapper = (Image_Collection) -> (Image_Collection)
            (Feature_Collection) -> (Feature_Collection)
- Reducer = (Image_Collection) -> (Image)
            (Feature_Collection) -> (Feature)
- Combine = (Image1, Image2) -> (Image)
            (Image_Collection_1, Image_Collection_2) -> (Image_Collection)
- Filter = (Image_Collection, Conf) -> (Image_Collection)
            (Feature_Collection, Conf) -> (Feature_Collection)

- GPU_Load = (Image) -> (Image)
- GPU_Deload = (Image) -> (Image) 


**TODOS**

1. Combine operator