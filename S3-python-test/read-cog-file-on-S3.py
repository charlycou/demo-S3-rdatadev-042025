import rioxarray
from matplotlib import pyplot as plt

url = "https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/36/Q/WD/2020/7/S2A_36QWD_20200701_0_L2A/TCI.tif"

xds = rioxarray.open_rasterio(url, chunks=True)
#print(xds.rio.bounds()) # (499980.0, 1790220.0, 609780.0, 1900020.0)

# Define a spatial window using coordinates (in CRS of the dataset)
# Here we define a bounding box (in the same CRS as the raster)
# You could use lat/lon with a transform, or project it first
subset_window = {
    "x": slice(550000, 560000),  # Easting (X)
    "y": slice(1850000, 1860000)  # Northing (Y) - reversed order!
}

subset = xds.rio.slice_xy(550000,1850000,560000,1855000)

subset.astype("int").plot.imshow(rgb="band")
plt.show()