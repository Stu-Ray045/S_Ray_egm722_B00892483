# import required modules
import os
import geopandas as gpd
import shapely

def get_input_aoi_bounds() -> str: # prompt user to define area of interest
    while True:
        print('Enter WGS 84 WKT string or valid GIS file path: ')
        aoi = input()

        try: # validate user input as a GIS file or WKT
            if os.path.exists(aoi):
                aoi_geometry = gpd.read_file(aoi, crs=4326)
            else:
                aoi_geometry = gpd.GeoSeries.from_wkt([aoi], crs=4326)

            # build a list of rounded integer aoi bounding coords for grid creation
            # EPSG:3957 used to ensure all squares will have the same orientation
            aoi_bounds = [
                int(round(coord, 0))
                for coord in aoi_geometry.to_crs(3857).total_bounds
            ]

            return aoi_bounds

        #  catch errors and continue while loop
        except Exception:
            print('Invlaid input path, file, or WKT.')
            continue


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

    while y >= min_y:
        x = min_x
        while x <= max_x:
            geom = shapely.geometry.Polygon(
                [
                    (x, y),
                    (x, y - grid_resolution),
                    (x + grid_resolution, y - grid_resolution),
                    (x + grid_resolution, y),
                    (x, y)
                ]
            )
            geom_array.append(geom)

            x += grid_resolution # add resolution to x after each polygon is created

        y -= grid_resolution # subtract resolution to y after each polygon is created

    return gpd.GeoDataFrame(geometry=geom_array, crs=3857).to_crs(4326) # return a wgs 84 projected geodataframe

# import shapefile mask for clipping

def get_input_state_geometry(state_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    while True:
        print('Enter comma separated two letter state abbreviations (eg. AL,AK,AZ): ') # prompt user for two letter state code

        input_states = [state.upper() for state in input().split(',')]

        state_list = list(state_gdf.STATE_CODE.unique())

        input_errors = [
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

# Add columns for attribute table
def add_columns(grid_gdf: gpd.GeoDataFrame):
    return gpd.GeoDataFrame(
        grid_gdf.reindex(
            columns=['Damage', 'Cause', 'Functionality', 'geometry']
        )
    )

# chain all functions together
def main():
    aoi_bounds = get_input_aoi_bounds()
    grid_resolution = get_input_grid_resolution()
    grid_gdf = create_aoi_grid(aoi_bounds, grid_resolution)

    # point code to data folder
    state_gdf = gpd.read_file(r'data\USA_GADM41_States.gpkg')

    state_gdf = get_input_state_geometry(state_gdf)
    state_grid_gdf = extract_grid_by_state(grid_gdf, state_gdf)
    state_grid_gdf = add_columns(state_grid_gdf)

    # save product to geopackage
    state_grid_gdf.to_file('grid,gpkg')

# executes code only if run directly by interpreter
# prevents automatic execution of code if imported
if __name__ == '__main__':
    main()



