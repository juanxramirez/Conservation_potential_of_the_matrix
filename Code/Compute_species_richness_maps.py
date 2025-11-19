"""
Compute species richness maps
(Ramírez-Delgado et al. 2025, PNAS)

This script was used to generate global species richness rasters by summing
binary species layers using ArcPy's CellStatistics function. Each species is
represented by a binary raster indicating presence (1) or absence (0) in each
pixel.

Use cases in the paper:

1) Matrix richness (unsuitable habitat) for three groups:
   - all mammals
   - mammals with declining population trends
   - mammals with threatened status

   To generate matrix richness maps:
     - Set `input_folder` to the folder containing the group's matrix rasters.
     - Set `temp_folder` and `output_folder` accordingly.
     - The processing logic (batch size, SUM, ignore_nodata="DATA") remains the same.

2) Suitable-habitat richness (all-mammal group only):
   - Set `input_folder` to the folder containing suitable-habitat AOH rasters.
   - Use the same batching and CellStatistics workflow.
   - Save the output as, for example: "species_richness_suitable_all.tif".

No other changes to the script logic are required between use cases. Only the
input/output folder paths and final output filename differ.

Note on input data:
-------------------
The species-specific binary habitat rasters used as inputs to generate species
richness maps are too large to host within this repository. These rasters can be
downloaded or generated directly from publicly available Area of Habitat (AOH)
maps and IUCN range data, as described in the Methods section of the paper.
Users should place these rasters in the folder specified by `input_folder` in
the USER INPUTS section below.
"""

import arcpy
arcpy.CheckOutExtension("Spatial")
from arcpy import env
from arcpy.ia import CellStatistics
import os
from multiprocessing import Pool

# Define a function to calculate species richness for a batch
def calculate_species_richness(species_tifs_batch, temp_folder, batch_index):
    processed_species = []  # Initialize an empty list to store processed species
    with arcpy.EnvManager(outputCoordinateSystem='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]', extent='-20037507.0671618 -8285884.04056101 20037507.0671618 18422517.1617313 PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'):
        species_layers = [arcpy.Raster(species_tif) for species_tif in species_tifs_batch]
        species_richness_batch = arcpy.sa.CellStatistics(
            in_rasters_or_constants=species_layers,
            statistics_type="SUM",
            ignore_nodata="DATA",
            process_as_multiband="SINGLE_BAND",
            percentile_value=90,
            percentile_interpolation_type="AUTO_DETECT"
        )
        output_filename = f"species_richness_batch_{batch_index}.tif"
        output_path = os.path.join(temp_folder, output_filename)
        species_richness_batch.save(output_path)
        
        # Append the names of processed species to the list
        processed_species.extend([os.path.basename(species_tif) for species_tif in species_tifs_batch])

    # Write the list of species processed by this batch to a .txt file
    with open(os.path.join(temp_folder, f"batch_{batch_index}_species.txt"), "w") as species_file:
        species_file.write("\n".join(processed_species))

if __name__ == "__main__":
     """
    USER INPUTS

    Adjust the paths below according to:
        - the species group you want to process (all, declining, threatened)
        - whether you are generating richness for matrix (unsuitable habitat)
          or for suitable habitat (all-mammal group only)

    For each run:
        - input_folder: folder containing binary species .tif layers
        - temp_folder: folder for intermediate batch outputs
        - output_folder: folder where final richness raster will be saved
        - output_filename: name of the final richness raster
    """
    
    # Folder containing species-specific binary .tif layers
    # Examples:
    #   Matrix richness (unsuitable): ".../unsuitable_species_tifs/"
    #   Suitable richness (all mammals): ".../suitable_species_tifs/"
    input_folder = r"PATH/TO/YOUR/SPECIES_RASTERS"
    
    # Temporary folder for intermediate batch outputs
    temp_folder = r"PATH/TO/TEMP/FOLDER"
    
    # Folder to store the final species richness raster
    output_folder = r"PATH/TO/OUTPUT/FOLDER"

    # Name of the final species richness raster to be saved
    # Examples:
    #   "species_richness_unsuitable_all.tif"
    #   "species_richness_unsuitable_declining.tif"
    #   "species_richness_unsuitable_threatened.tif"
    #   "species_richness_suitable_all.tif"
     output_filename = "species_richness.tif"
    
    # Get a list of species-specific .tif files
    species_tifs = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith(".tif")]
    
    # Divide species_tifs into batches
    batch_size = 150  # Number of files to process in each batch
    num_batches = len(species_tifs) // batch_size + (len(species_tifs) % batch_size > 0)
    batches = [species_tifs[i:i + batch_size] for i in range(0, len(species_tifs), batch_size)]

    # Set up parallel processing using the Pool class
    num_processors = 5  # Number of CPU cores to use
    with Pool(num_processors) as pool:
        # Pass batch index as an additional argument to the function using starmap
        pool.starmap(calculate_species_richness, [(batch, temp_folder, idx) for idx, batch in enumerate(batches)])

    # Get a list of all the .tif files in the temp_folder
    temp_output_files = [os.path.join(temp_folder, filename) for filename in os.listdir(temp_folder) if filename.endswith(".tif")]

    # Calculate final species richness using Cell Statistics
    with arcpy.EnvManager():
        final_species_richness = arcpy.sa.CellStatistics(temp_output_files, "SUM", "DATA")
    
    # Save the final species richness map
    final_output_path = os.path.join(output_folder, output_filename)
    final_species_richness.save(final_output_path)
