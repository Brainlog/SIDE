import geopandas as gpd
from shapely.geometry import shape, Point, Polygon, LineString
from shapely.ops import unary_union

class Geometry:
    def __init__(self, filepath):
        """Initialize the Geometry class by loading a shapefile and storing its geometry."""
        self.gdf = gpd.read_file(filepath)
        self.geom = self._get_shapely_geom()

    def _get_shapely_geom(self):
        """Extract the Shapely geometry from the first feature in the GeoDataFrame."""
        return self.gdf.geometry.iloc[0]

    def area(self):
        """Return the area of the geometry (for polygons)."""
        if hasattr(self.geom, 'area'):
            return self.geom.area
        else:
            raise TypeError("Area operation not supported for this geometry type.")
        
    def length(self):
        """Return the length of the geometry (for polygons and lines)."""
        if hasattr(self.geom, 'length'):
            return self.geom.length
        else:
            raise TypeError("Length operation not supported for this geometry type.")

    def centroid(self):
        """Return the centroid of the geometry."""
        if hasattr(self.geom, 'centroid'):
            return self.geom.centroid
        else:
            raise TypeError("Centroid operation not supported for this geometry type.")
        
    def union(self, other):
        """Return the union of this geometry with another geometry."""
        if isinstance(other, Geometry):
            return Geometry(unary_union([self.geom, other.geom]))
        else:
            raise TypeError("Union operation requires another Geometry object.")

    def intersection(self, other):
        """Return the intersection of this geometry with another geometry."""
        if isinstance(other, Geometry):
            return Geometry(self.geom.intersection(other.geom))
        else:
            raise TypeError("Intersection operation requires another Geometry object.")
    
    def difference(self, other):
        """Return the difference of this geometry with another geometry."""
        if isinstance(other, Geometry):
            return Geometry(self.geom.difference(other.geom))
        else:
            raise TypeError("Difference operation requires another Geometry object.")
    
    def contains(self, other):
        """Check if this geometry contains another geometry."""
        if isinstance(other, Geometry):
            return self.geom.contains(other.geom)
        else:
            raise TypeError("Contains operation requires another Geometry object.")
    
    def distance(self, other):
        """Calculate the distance between this geometry and another geometry."""
        if isinstance(other, Geometry):
            return self.geom.distance(other.geom)
        else:
            raise TypeError("Distance operation requires another Geometry object.")
    
    def to_shapely(self):
        """Return the Shapely geometry object."""
        return self.geom
