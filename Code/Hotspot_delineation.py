"""
Hotspot delineation
(Ramírez-Delgado et al. 2025)

This script identifies richness hotspots based on:
    - a percentile-based threshold
    - a target hotspot coverage (2.5%, 5%, 10%)
    - contiguity filtering to remove clusters < 10 km² (via RegionGroup)

Use cases in the paper:
- All mammals
- Mammals with declining population trends
- Mammals with threatened status

And across three hotspot thresholds:
- 2.5%
- 5%
- 10%

To reproduce results for a specific group + threshold:
    - Set `richness_raster` to the appropriate species richness raster as,
      for example "species_richness_within_species-rich_matrix_areas_all.tif".
    - Set the percentile for threshold initialization.
    - Set the `target_coverage` value (2.5, 5, or 10).
    - Set `highest_species_richness_value` to the maximum richness value found in
      that raster.
    - Set `final_output_path` to indicate group + threshold as, for example
      "hotspots_all_5.tif".      

Only these user-input parameters vary between runs.
All other logic in the script remains identical across species groups and hotspot
definitions.
"""

import arcpy
import logging
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up environment settings
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace = r"PATH/TO/YOUR/WORKSAPCE"
arcpy.env.overwriteOutput = True

def create_valid_pixel_mask(raster, valid_value=1):
    """Create a raster mask with valid pixels set to 'valid_value'."""
    mask = arcpy.sa.Con(arcpy.sa.IsNull(raster) == 0, valid_value)
    mask_path = os.path.join(arcpy.env.workspace, "valid_pixel_mask.tif")
    mask.save(mask_path)
    return mask_path

def calculate_percentiles_and_total_valid_pixels(raster, mask, percentiles):
    """Calculate specified percentiles of pixel values and the total count of valid pixels using a mask."""
    out_table = os.path.join(arcpy.env.workspace, "percentile_value_table.dbf")
    arcpy.sa.ZonalStatisticsAsTable(mask, "VALUE", raster, out_table, "DATA", "ALL", "CURRENT_SLICE", percentiles, "AUTO_DETECT")

    percentile_values = {}
    total_valid_pixels = 0
    with arcpy.da.SearchCursor(out_table, ["PCT" + str(p) for p in percentiles] + ["COUNT"]) as cursor:
        row = next(cursor)
        for i, p in enumerate(percentiles):
            percentile_values[p] = row[i]
        total_valid_pixels = row[-1]

    arcpy.Delete_management(out_table)
    logging.info(f"Total valid pixels calculated: {total_valid_pixels}")
    return percentile_values, total_valid_pixels

def eliminate_isolated_pixels(raster):
    """Eliminate isolated pixels in the raster."""
    region_group_raster = arcpy.sa.RegionGroup(raster, "EIGHT", "WITHIN", "ADD_LINK")
    set_null_raster = arcpy.sa.SetNull(region_group_raster, raster, "Count < 1000")
    return set_null_raster

def calculate_coverage(cleaned_raster, total_valid_pixels, mask_path):
    """Calculate the coverage percentage of high richness pixels within the valid pixel mask."""
    mask = arcpy.Raster(mask_path)
    zone_table = os.path.join(arcpy.env.workspace, "coverage_table.dbf")
    arcpy.sa.ZonalStatisticsAsTable(mask, "VALUE", cleaned_raster, zone_table, "DATA", "ALL")

    high_richness_pixels = 0
    with arcpy.da.SearchCursor(zone_table, ['COUNT']) as cursor:
        for row in cursor:
            high_richness_pixels += row[0] if row[0] is not None else 0

    arcpy.Delete_management(zone_table)
    return (high_richness_pixels / float(total_valid_pixels)) * 100 if total_valid_pixels > 0 else 0

def save_final_raster(cleaned_raster):
    """Save the final raster output."""
    final_output_path = os.path.join(arcpy.env.workspace, "hotspots_all_5.tif")
    try:
        logging.info(f"Saving map at: {final_output_path}")
        cleaned_raster.save(final_output_path)
    except Exception as e:
        logging.error(f"Error saving output raster: {e}")

# Load the raster and create a mask
richness_raster = arcpy.Raster("species_richness_within_species-rich_matrix_areas_all.tif")
mask_path = create_valid_pixel_mask(richness_raster)

# Define percentiles to calculate
percentiles_to_calculate = [95]

# Calculate the percentiles and total valid pixels
percentile_values, total_valid_pixels = calculate_percentiles_and_total_valid_pixels(richness_raster, mask_path, percentiles_to_calculate)

# Use the 95th percentile to set the initial threshold
initial_threshold = int(percentile_values[95])
logging.info(f"Initial threshold set based on the 95th percentile: {initial_threshold}")

# Set parameters for finding the optimal threshold
target_coverage = 5
acceptable_range = 0.5  # How close coverage can vary
max_iterations = 5  # 5 below and 5 above the initial threshold
highest_species_richness_value = 193

# Create a range of thresholds to test, alternating up and down
threshold_range = []
threshold_range.append(initial_threshold)

for i in range(1, max_iterations + 1):
    threshold_range.append(initial_threshold + i)
    threshold_range.append(initial_threshold - i)

# Track the closest coverage
closest_coverage = float('inf')
closest_threshold = None

# List to store each threshold's results
threshold_results = []

# Test each threshold
for threshold in threshold_range:
    try:
        # Reclassify the raster using the current threshold
        reclassified_raster = arcpy.sa.Reclassify(richness_raster, "Value", arcpy.sa.RemapRange([[threshold, highest_species_richness_value, 1]]), "NODATA")
        
        # Clean the raster by removing isolated pixels
        cleaned_raster = eliminate_isolated_pixels(reclassified_raster)
        
        # Create a valid pixel mask from the cleaned raster
        iteration_mask_path = create_valid_pixel_mask(cleaned_raster)
        
        # Calculate the current coverage
        current_coverage = calculate_coverage(cleaned_raster, total_valid_pixels, iteration_mask_path)

        logging.info(f"Threshold {threshold}, Coverage {current_coverage}%")

        # Store the results in the list
        threshold_results.append((threshold, current_coverage, cleaned_raster))

        # Update the closest coverage and threshold if necessary
        if abs(current_coverage - target_coverage) < abs(closest_coverage - target_coverage):
            closest_coverage = current_coverage
            closest_threshold = threshold

    except Exception as e:
        logging.error(f"Error encountered: {e}")

# After all iterations, select the closest threshold and save the associated raster
if closest_threshold is not None:
    for t, c, r in threshold_results:
        if t == closest_threshold:
            # Save the raster corresponding to the closest threshold
            save_final_raster(r)
            break
    logging.info(f"Threshold selected based on closest coverage: {closest_threshold}")
else:
    logging.error("Threshold remained unresolved.")
