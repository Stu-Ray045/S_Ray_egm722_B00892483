# import required modules
import os
import geopandas as gpd
import shapely


# set user defined extent of grid
total_bounds = gdf.total_bounds
minX, minY, maxX, maxY = total_bounds

x, y = (minX, minY) # create the grid
geom_array = []

# User to define the dimensions of squares within the grid
def square_size [input{}]
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

usa = gpd.read_file('http://localhost:8888/edit/projects/S_Ray_egm722_B00892483/data%20files/gadm41_USA_1.shp')

# Define specific shapefile for mask from attribute table


# Clip grid to mask

# save finished grid to file


