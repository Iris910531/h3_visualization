import geopandas as gpd
import pandas as pd
import os
import ellipsis as el
from shapely.geometry import Point
import re
### due to the different preprocessing required by the data, there is no function for preprocessing.

# read dataframe including geometry dataset
def gdf_read_file(file_path):
    root = '/mnt/data/charging-point-localization/data/raw'
    FILE_LOC = file_path
    data_path = os.path.join(root, FILE_LOC)
    gdf = gpd.read_file(data_path)
    return gdf

# read dataframe dataset
def df_read_file(file_path):
    root = '/mnt/data/charging-point-localization/data/raw'
    FILE_LOC = file_path
    data_path = os.path.join(root, FILE_LOC)
    df = pd.read_csv(data_path, low_memory=False)
    return df

# delete islands nearby Taiwan
def del_outlying_islands(data):
    excluded_counties = ['澎湖縣', '連江縣', '金門縣']
    excluded_town = ['蘭嶼鄉', '琉球鄉', '綠島鄉']
    filter_counties_gdf = data[~data["COUNTY"].isin(excluded_counties)]
    filter_town_gdf = filter_counties_gdf[~filter_counties_gdf["TOWN"].isin(excluded_town)]
    return filter_town_gdf

# convert coordinate system
def crs_to_4326(geodata):
    ori_crs = geodata.crs
    print('original coordinate system：', ori_crs)
    geodata = geodata.to_crs('epsg:4326')
    print('new coordinate system：', geodata.crs)
    return geodata

# produce hexagons covering main island of Taiwan
def produce_tw_hexagons(mainland, resolution, distance):
    hexagons_tw = mainland.h3.polyfill_resample(resolution)
    hexagons_nei = hexagons_tw.h3.hex_ring(distance, True)
    hexagons_boun = hexagons_nei.set_index('h3_hex_ring', drop=True)
    hexagons_boun = hexagons_boun.drop(columns=["geometry"])
    bound = hexagons_boun.h3.h3_to_geo_boundary()
    bound = bound.drop_duplicates(subset='geometry')
    bound.plot()
    return bound

# calculate each hexagon containing how many data(for example, population or income)
def cal_hex(data, boundary):
    hexagon_data = []
    data['area'] = data['geometry'].area
    
    for each_hex in boundary.geometry:
        intersecting_areas = gpd.sjoin(data, gpd.GeoDataFrame(geometry=[each_hex]), how='inner', op='intersects')
        
        intersecting_areas['proportion'] = intersecting_areas.apply(lambda row: (each_hex.intersection(row['geometry']).area / row['area']) if row['area'] > 0 else 0,axis=1)
    
        intersecting_areas['hex_count'] = intersecting_areas['proportion'] * intersecting_areas['count']
        
        hexagon_data.append(round(intersecting_areas['hex_count'].sum(), 0))
    
    boundary['count'] = hexagon_data
    
    return boundary.copy()

# polt a 3D picture to ellipsis drive
def draw_to_drive(data, file_name):
    token = el.account.logIn('iris_910531', 'a7654321')
    pathId = el.path.vector.add(file_name, token = token)['id']
    timestampId = el.path.vector.timestamp.add(pathId, token)['id']
    result = el.path.vector.timestamp.feature.add(pathId, timestampId, data, token)
    return None

# convert geometry string to geometry object
def convert_to_point(geometry_str):
    # Extract coordinates from the string using a regular expression
    coords = re.findall(r"[-+]?\d*\.\d+|\d+", geometry_str)
    # Create a Point object from these coordinates
    return Point(float(coords[0]), float(coords[1]))

# calculate each hexagon containing how many data(for example, the number of charging stations)
# (The charging smith dataset is including Point rather than Polygon, so the function is different from cal_hex)
def cal_hex_point(data, boundary):
    check_id = []
    hexagon_point_counts = []
    for each_hex in boundary.geometry:
        #points_within_hex = data[data['geom'].within(each_hex)]
        points_within_hex = data['geometry'].apply(lambda point: point.within(each_hex))
        hexagon_point_counts.append(len(points_within_hex[points_within_hex]))
        check_id.append(data["id"][points_within_hex])
    boundary['count'] = hexagon_point_counts
    
    return boundary.copy(), check_id