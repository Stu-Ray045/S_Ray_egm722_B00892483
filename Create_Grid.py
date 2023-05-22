# import required modules
import os
import geopandas as gpd
import shapely

def get_input_aoi_bounds() -> str: #prompt user to define area of interest
    while True:
        print('Enter WGS 84 WKT string or valid GIS file path: ')
        aoi = input()

        try: # validate user input as a GIS file or WKT
            if os.path.exists(aoi):
                aoi_geometry = gpd.read_file(aoi, crs=4326)
            else:
                aoi_geometry = gpd.Geoseries.from_wkt([aoi], crs=4326)

            # build a list of rounded integer aoi bounding coords for grid creation
            # EPSG:3957 used to ensure all squares will have the same orientation
            aoi_bounds = [
                int(round(coord, 0))
                for coord in aoi_geometry.to_crs(3857).total_bounds
            ]

        #  catch errors and continue while loop
        except Exception:
            print('Invlaid input path, file, or WKT.')


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


