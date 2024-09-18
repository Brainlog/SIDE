## class feature interface
## fields : dictionary of properties (properties can be any object)
## methods : get_properties, set_properties

import geopandas as gpd

class FeatureCollection:
    def __init__(self, gdf):
        """Initialize with a GeoDataFrame."""
        self.gdf = gdf

    def filter(self, condition):
        """Filter the collection based on a condition."""
        return self.gdf[self.gdf.apply(condition, axis=1)]
