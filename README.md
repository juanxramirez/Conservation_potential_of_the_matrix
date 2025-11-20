## Conservation_potential_of_the_matrix
This repository includes `Python` code used to reproduce the main analyses for the manuscript:

**"Matrix areas reveal conservation opportunities for over half of the world’s terrestrial mammals"**

_by J.P. Ramírez-Delgado, M. Di Marco, C.J. Johnson, J.E.M. Watson, L. de Assis Barros, and O. Venter_

**Manuscript in preparation.**

### Requirements
Users should have `ArcGIS Pro` version 3.4.0 or higher.  
The script uses the `ArcPy` library and requires the `Spatial Analyst` extension.

### Code
#### `Hotspot_delineation.py`
This script identifies matrix-based richness hotspots using:
- richness thresholds initialized using percentiles
- iterative threshold adjustment to match hotspot area targets (2.5%, 5%, 10%)
- contiguity filtering (minimum area = 10 km²)  

### Data
Derived species richness rasters required to run `hotspot_delineation.py` are publicly available at:

<a href="https://doi.org/10.5281/zenodo.17664172"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.17664172.svg" alt="DOI"></a>

These include:
- `species_richness_within_species-rich-matrix_areas_all.tif`  
- `species_richness_within_species-rich-matrix_areas_declining.tif`  
- `species_richness_within_species-rich-matrix_areas_threatened.tif`

These rasters represent species richness within species-rich matrix areas for each species group analyzed in the manuscript and provide the required inputs for reproducing all hotspot analyses.

### Data not included
Raw spatial datasets used in this study (AOH maps, IUCN range polygons, HFP data, and global PA/OECM layers) cannot be redistributed in this repository due to size and licensing restrictions. These datasets are publicly available from their original sources and are fully described in the Materials and Methods section of the manuscript.
