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
def get_input_grid_resolution() -> int:

    while True:  # enter infinite while loop until user enters valid input
        print('Enter required grid resolution in metres:')

        try:
            return int(input())

        except ValueError as e:
            print(f'{e}: invalid input integer.')
            continue

# create grid
def create_aoi_grid(aoi_bounds: list, grid_resolution: int) -> gpd.GeoDataFrame:
    ''
    # set up necessary variables for grid creation
    min_x, min_y, max_x, max_y, = aoi_bounds
    y = max_y
    geom_array = []

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

def get_input_state_geometry(state_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    while True:
        print('Enter comma separated two letter state abbreviations (eg. AL,AK,AZ): ') # prompt user for two letter state code

        state_list = [
            state
            for state in input_states
            if state not in state_list # list user inputs not in state abbreviation list
        ]

        if len(input_errors) > 0: # continue while loop if errors are present
            print(f'Inputs not in list of available states: {input_errors}')
            continue

        # return geodataframe of dtates from input list
        return gpd.GeoDataFrame(
            geometry=state_gdf[state_gdf['STATE_CODE'].isin(input_states)]['geometry']
        )

# Clip grid to mask
def extract_grid_by_state(grid_gdf, state_gdf):
    return gpd.sjoin(grid_gdf, state_gdf)

# Add columsn for attribute table
def add_columns(grid_gdf: gpd_GeoDataFrame):
    return gpd.GeoDataFrame(
        grid_gdf.reindex(
            columns=['Damage', 'Cause', 'Functionality', 'geometry']
        )
    )

# save finished grid to file


