import geopandas as gpd # Import the geopandas module
from shapely import geometry # Import the geometry function from the shapely module

# set extent of grid
total_bounds = gdf.total_bounds
minX, minY, maxX, maxY = total_bounds

x, y = (minX, minY) # create the grid
geom_array = []

input square_size []
while y <= maxY:
    while x <= MaxX
        geom = geometry.Polygon([(x,y), (x, y+square_size), (x+square_size, y+square_size), (x+square_size, y), (x, y)])
        geom_array.append(geom)
        x += square_size
    x = minX
    y += square_size

fishnet = gpd.GeoDataFrame(geom_array, columns=['geometry']).set_crs('EPSG:3857') # set the grid CRS
fishnet.to_file('fishnet_grid.shp')

# import shapefile mask for clipping



