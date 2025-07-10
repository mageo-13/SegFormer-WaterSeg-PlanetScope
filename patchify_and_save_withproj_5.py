import rasterio
from rasterio.windows import Window
import os
 
def split_and_save_tiff(input_path, output_folder, tile_size):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
 
    with rasterio.open(input_path) as src:
        # Get metadata from the source TIFF
        meta = src.meta
 
        # Get the dimensions of the input raster
        width, height = src.width, src.height
 
        # Calculate the number of tiles in both dimensions
        num_tiles_x = width // tile_size
        num_tiles_y = height // tile_size
 
        for tile_y in range(num_tiles_y):
            for tile_x in range(num_tiles_x):
                # Calculate the window for the current tile
                window = Window(
                    tile_x * tile_size, tile_y * tile_size, tile_size, tile_size
                )
 
                # Read the data for the current tile
                tile_data = src.read(window=window)
 
                # Update metadata for the current tile
                meta.update({
                    'width': tile_size,
                    'height': tile_size,
                    'transform': src.window_transform(window)
                })
 
                # Save the tile as a TIFF file with tile x and tile y information in the filename
                output_filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_patch_{tile_x}_{tile_y}.tif"
                output_path = os.path.join(output_folder, output_filename)
                with rasterio.open(output_path, 'w', **meta) as dest:
                    dest.write(tile_data)


def process_folder(input_folder, output_folder, tile_size):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

    for input_file in input_files:
        # Construct the full path for the input file
        input_path = os.path.join(input_folder, input_file)

        # Call your split_and_save_tiff function for each file
        split_and_save_tiff(input_path, output_folder, tile_size)


if __name__ == "__main__":
    
    # full TIFF part
    #input_folder = r"C:\Users\DELL\Downloads\soi_tankhalpart_planet_image"
    #output_tiles_folder = r"C:\Users\DELL\Downloads\PLANET_FULL\planet_patches_tiff"
    
    input_folder = r"D:\PLANET_FULL\RGB_planet_mask"
    output_tiles_folder = r"D:\PLANET_FULL\planet_masks_tiff"
    
    tile_size = 512

    process_folder(input_folder, output_tiles_folder, tile_size)
