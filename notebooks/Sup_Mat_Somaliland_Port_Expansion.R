#Code created by Phillip to expand the Sahil region to include Berbera Port
# Full code can be found on his GitHub page. This is for reproducibility purposes.

library(sf)
library(dplyr)
library(magrittr)


####################################Creating Somaliland with Berbera Port################################
setwd("C:/Users/phill/Documents/Somaliland/Satelite data/Analysis/Satelite/Somaliland Shape")
n_somaliland <- st_read("C:/Users/phill/Documents/Somaliland/Satelite data/Analysis/Satelite/Somaliland Shape/SL_SixRegions.shp")
head(n_somaliland)
plot(n_somaliland)

# Step 1: Create matrix of coordinates manually
# Step 1: Your Berbera points
berbera_add <- st_sfc(
  st_point(c(44.990222, 10.435328)),
  st_point(c(44.992990, 10.436626)),
  st_point(c(44.996713, 10.438525)),
  st_point(c(44.999063, 10.439747)),
  st_point(c(45.001444, 10.438945)),
  st_point(c(44.994214, 10.428197)),
  st_point(c(45.007947, 10.434275)),
  st_point(c(44.992368, 10.430603)),
  st_point(c(45.004342, 10.437736)),
  st_point(c(44.988190, 10.438735)),####increasing the size to see if that changes anything for sam
  st_point(c(44.985444, 10.442998)),#increasing the size to see if that changes anything for sam
  st_point(c(44.997331, 10.447050)),#increasing the size to see if that changes anything for sam
  st_point(c(44.998962, 10.442492)),#increasing the size to see if that changes anything for sam
  crs = 4326
)

# Step 2: Combine and create convex hull
berbera_patch <- st_union(berbera_add) %>%
  st_convex_hull()

# Step 3: Plot
plot(berbera_patch, col = "red", main = "Berbera Patch Convex Hull")

# 1. Make sure both geometries are in the same CRS
# 1. Extract Sahil geometry from the admin shapefile
# 1. Extract Sahil from the shapefile
sahil <- roi_sf %>% dplyr::filter(admin1Name == "Sahil")

# 2. Match CRS with Berbera patch
berbera_patch <- st_transform(berbera_patch, st_crs(sahil))

# 3. Union Sahil with Berbera patch
sahil_expanded <- st_union(st_geometry(sahil), berbera_patch)

# 4. Convert to sf with attributes
sahil_expanded <- st_sf(
  admin1Name = "Sahil",
  geometry = sahil_expanded
)

# 5. Plot to verify
plot(sahil_expanded$geometry, col = "lightgreen", main = "Expanded Sahil with Berbera Patch")
plot(
  sahil_expanded$geometry,
  col = "lightgreen",
  main = "Zoomed-In View: Expanded Sahil (Berbera Area)",
  xlim = c(44.98, 45.02),  # Longitude range
  ylim = c(10.42, 10.45)   # Latitude range
)

# Optional: Overlay berbera_patch in red to verify it's included
plot(berbera_patch, col = "red", add = TRUE)

# Replace Sahil with sahil_expanded in the full shapefile
roi_updated <- roi_sf %>%
  dplyr::filter(admin1Name != "Sahil") %>%         # Remove old Sahil
  dplyr::bind_rows(sahil_expanded)                 # Add updated Sahil

# Save to a new shapefile (you can change the path)
st_write(roi_updated, "somaliland_with_berbera.shp", delete_layer = TRUE)

setwd("C:/Users/phill/Documents/Somaliland/Satelite data/Analysis/Satelite")
roi_check <- st_read("somaliland_with_berbera.shp")
plot(roi_check["admin1Name"], main = "Final Somaliland with Expanded Sahil")
