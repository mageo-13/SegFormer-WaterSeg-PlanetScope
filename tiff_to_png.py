from osgeo import gdal
import numpy as np
import os
from PIL import Image

def convert_16bit_to_8bit(inputRaster, outputRaster, outputPixType='Byte', outputFormat='GTiff', percentiles=[2, 98]):
    srcRaster = gdal.Open(inputRaster)
    driver = gdal.GetDriverByName(outputFormat)

    # Create output raster
    output = driver.Create(outputRaster, srcRaster.RasterXSize, srcRaster.RasterYSize, srcRaster.RasterCount, gdal.GDT_Byte)

    # Copy projection and geotransform
    output.SetProjection(srcRaster.GetProjection())
    output.SetGeoTransform(srcRaster.GetGeoTransform())

    # Iterate through bands
    for bandId in range(srcRaster.RasterCount):
        bandId = bandId + 1
        band = srcRaster.GetRasterBand(bandId)

        bmin = band.GetMinimum()
        bmax = band.GetMaximum()
        if bmin is None or bmax is None:
            (bmin, bmax) = band.ComputeRasterMinMax(1)
        band_arr_tmp = band.ReadAsArray()
        bmin = np.percentile(band_arr_tmp.flatten(), percentiles[0])
        bmax = np.percentile(band_arr_tmp.flatten(), percentiles[1])

        # Rescale the values to 8-bit
        band_arr_scaled = np.interp(band_arr_tmp, (bmin, bmax), (0, 255)).astype(np.uint8)
        #band_arr_scaled = np.interp(band_arr_tmp, (bmin, bmax), (0, 1)).astype(np.uint8)

        # Write the scaled array to the output raster
        output.GetRasterBand(bandId).WriteArray(band_arr_scaled)

    # Close datasets
    srcRaster = None
    output = None

# Modify the path to your directory in Google Drive
path =  r"D:\PLANET_FULL\planet_masks_tiff"

files = os.listdir(path)

for file in files:
    resimPath = os.path.join(path, file)
    dstPath   = r"D:\PLANET_FULL\planet_patches_png_0255"
    dstPath   = os.path.join(dstPath, os.path.splitext(file)[0] + ".png")

    convert_16bit_to_8bit(resimPath, dstPath)
    
    
   
    
#---------------------------------3 band png ------------------------------
from osgeo import gdal
import numpy as np
import os
from PIL import Image

def convert_16bit_to_8bit(inputRaster, outputRaster, outputPixType='Byte', outputFormat='GTiff', percentiles=[2, 98], bands=[1, 2, 3]):
    srcRaster = gdal.Open(inputRaster)
    driver = gdal.GetDriverByName(outputFormat)

    # Create output raster
    output = driver.Create(outputRaster, srcRaster.RasterXSize, srcRaster.RasterYSize, 3, gdal.GDT_Byte)

    # Copy projection and geotransform
    output.SetProjection(srcRaster.GetProjection())
    output.SetGeoTransform(srcRaster.GetGeoTransform())

    # Iterate through bands
    for i in range(3):
        bandId = bands[i]
        band = srcRaster.GetRasterBand(bandId)

        bmin = band.GetMinimum()
        bmax = band.GetMaximum()
        if bmin is None or bmax is None:
            (bmin, bmax) = band.ComputeRasterMinMax(1)
        band_arr_tmp = band.ReadAsArray()
        bmin = np.percentile(band_arr_tmp.flatten(), percentiles[0])
        bmax = np.percentile(band_arr_tmp.flatten(), percentiles[1])

        # Rescale the values to 8-bit
        band_arr_scaled = np.interp(band_arr_tmp, (bmin, bmax), (0, 255)).astype(np.uint8)

        # Write the scaled array to the output raster
        output.GetRasterBand(i + 1).WriteArray(band_arr_scaled)

    # Close datasets
    srcRaster = None
    output = None

path = r"D:\PLANET_FULL\planet_patches_tiff"
files = os.listdir(path)

for file in files:
    resimPath = os.path.join(path, file)
    dstPath   = r"D:\PLANET_FULL\planet_patches_png"
    dstPath   = os.path.join(dstPath, os.path.splitext(file)[0] + ".png")

    convert_16bit_to_8bit(resimPath, dstPath)
  
