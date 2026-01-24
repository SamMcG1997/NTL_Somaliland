import matplotlib.pyplot as plt
import contextily as cx
import xarray as xr
import geopandas as gpd
import xarray as xr
import rioxarray
import rasterio.features

#Graph Functions
def plot_NASA_NTL(df, gdf, date: str, variable: str, title_prefix: str, source: str = "VNP46A4", cmap: str = "Spectral", 
                  robust: bool = True, vmin: float = None, vmax: float = None):
    """
    Plots a specified variable for a given year from the dataset.

    Args:
    df (xarray.Dataset): The dataset containing the data to be plotted.
    gdf (geopandas.GeoDataFrame): The GeoDataFrame for basemap context.
    date (str): The date for which to plot the data.
    variable (str): The variable in the dataset to plot. Possible values:
        - "NearNadir_Composite_Snow_Free": The radiance value per pixel.
        - "NearNadir_Composite_Snow_Free_Quality": A metric of the quality of data per pixel.
        - "NearNadir_Composite_Snow_Free_Num": The number of observations across a time period.
    title_prefix (str): The prefix for the plot title.
    source (str, optional): The data source description for attribution. Defaults to "NASA Black Marble VNP46A4".
    cmap (optional): Allows for different colour maps to be defined. 
    robust (bool, optional): Whether to correct for outliers in the data. Defaults to "True".
    
    Returns:
    None
    """
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Plot with optional vmin and vmax if robust is False
    if robust:
        df[variable].sel(time=date).plot.pcolormesh(ax=ax, cmap=cmap, robust=robust)
    else:
        df[variable].sel(time=date).plot.pcolormesh(ax=ax, cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Add basemap
    cx.add_basemap(ax, crs=gdf.crs.to_string(), source=cx.providers.CartoDB.Positron)
    
    ax.text(
        0,
        -0.1,
        f"Source: NASA Black Marble {source}",
        ha="left",
        va="center",
        transform=ax.transAxes,
        fontsize=10,
        color="black",
        weight="normal",
    )
    ax.set_title(f"{title_prefix}: {date}", fontsize=16)
    plt.axis("off")


def filter_dataset_by_bounding_box(dataset, shapefile):
    """
    Filters an xarray.Dataset to include only data points within the bounds of a shapefile.

    Args:
        dataset (xarray.Dataset): The dataset to be filtered.
        shapefile (shp file): Path to the shapefile.

    Returns:
        xarray.Dataset: Filtered dataset with data points within the shapefile's bounding box.
    """
    # Read the shapefile    
    # Extract bounds from the shapefile
    x_min, y_min, x_max, y_max = shapefile.total_bounds

    # Filter the xarray dataset within the bounding box
    filtered_dataset = dataset.where(
        (dataset.x >= x_min) & (dataset.x <= x_max) &
        (dataset.y >= y_min) & (dataset.y <= y_max),
        drop=True
    )
    
    return filtered_dataset

def mask_dataset_by_geometry(dataset, gdf):
    """
    Masks an xarray.Dataset to include only values inside the geometry of a shapefile (GeoDataFrame).

    Args:
        dataset (xarray.Dataset): The dataset to be masked (must be rioxarray-enabled).
        gdf (gpd.GeoDataFrame): The shapefile loaded as a GeoDataFrame.

    Returns:
        xarray.Dataset: Dataset masked to the shapefile geometry.
    """

    # Create the mask (True outside the geometry, False inside)
    mask = rasterio.features.geometry_mask(
        geometries=gdf.geometry,
        out_shape=(dataset.rio.height, dataset.rio.width),
        transform=dataset.rio.transform(),
        invert=True  # Keep values inside the geometry
    )

    # Convert mask to DataArray with same dims and coords
    mask_da = xr.DataArray(mask, coords={"y": dataset.y, "x": dataset.x}, dims=("y", "x"))

    # Apply mask to all data variables
    return dataset.where(mask_da)