import os
import rasterio
from rasterio.features import rasterize
from shapely.geometry import mapping, Point, Polygon
from shapely.ops import unary_union
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# Function to generate polygon
def poly_from_utm(polygon, transform):
    poly_pts = []
    poly = unary_union(polygon)
    for i in np.array(poly.exterior.coords):
        poly_pts.append(~transform * tuple(i))
    return Polygon(poly_pts)

# Function to explode multipart features
def explode_multipart(gdf):
    exploded = gdf.explode(ignore_index=True)
    return exploded

# Function to process each pair of raster and shapefile
def process_files(raster_path, shapefile_path, save_path):
    with rasterio.open(raster_path, "r") as src:
        raster_img = src.read()
        raster_meta = src.meta

    train_df = gpd.read_file(shapefile_path)
    #train_df = train_df.to_crs(epsg=32643)

    # Explode multipart features
    train_df = explode_multipart(train_df)

    print("Processing: {}".format(os.path.basename(raster_path)))

    poly_shp = []
    im_size = (src.meta['height'], src.meta['width'])

    for _, row in train_df.iterrows():
        if row['geometry'].geom_type == 'Polygon':
            poly = poly_from_utm(row['geometry'], src.meta['transform'])
            poly_shp.append(poly)
        else:
            for p in row['geometry']:
                poly = poly_from_utm(p, src.meta['transform'])
                poly_shp.append(poly)

    mask = rasterize(shapes=poly_shp, out_shape=im_size)

    mask = mask.astype("uint16")
    bin_mask_meta = src.meta.copy()
    bin_mask_meta.update({'count': 1})

    with rasterio.open(save_path, 'w', **bin_mask_meta) as dst:
        dst.write(mask * 255, 1)


# List of raster and shapefile paths
raster_folder = r"D:\PLANET_FULL\RGB_planet_image"
shapefile_folder = r"D:\PLANET_FULL\water_vector"
output_folder = r"D:\PLANET_FULL\RGB_planet_mask"


raster_files = [os.path.join(raster_folder, file) for file in os.listdir(raster_folder) if file.endswith('.tif')]
shapefile_files = [os.path.join(shapefile_folder, file) for file in os.listdir(shapefile_folder) if file.endswith('.shp')]

# Make sure the lists are sorted to match raster and shapefile pairs
raster_files.sort()
shapefile_files.sort()

# Loop through each pair of raster and shapefile
for raster_path, shapefile_path in zip(raster_files, shapefile_files):
    filename = os.path.splitext(os.path.basename(raster_path))[0]
    save_path = os.path.join(output_folder, f"{filename}.tif")
    
    process_files(raster_path, shapefile_path, save_path)

print("Processing complete.")

