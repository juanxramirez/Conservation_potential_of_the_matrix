## Conservation_potential_of_the_matrix
This repository includes `Python` code used to reproduce the analyses for the manuscript:

**"Matrix areas reveal conservation opportunities for over half of the world’s terrestrial mammals"**

_by J.P. Ramírez-Delgado, M. Di Marco, C.J. Johnson, J.E.M. Watson, L. de Assis Barros, and O. Venter_

Manuscript in preparation.

# Requirements
Users should have `ArcGIS Pro` version **3.4.0** or higher.  
Scripts use the `ArcPy` library and require the `Spatial Analyst` extension.

# Code
`compute_species_richness.py`
Computes global species richness maps by summing binary habitat rasters for each species.  
Used for:
- all mammals  
- mammals with declining population trends  
- mammals with threatened status  
- suitable-habitat richness for the all-mammal group

### `hotspot_delineation.py`
Identifies matrix-based richness hotspots using:
- percentile-based richness thresholds  
- iterative coverage matching  
- contiguity filtering (minimum area = 10 km²)  

## Data
### **Available on Zenodo**
The species richness rasters required to run `hotspot_delineation.py` are publicly archived on Zenodo:

👉 **https://doi.org/XXXX/zenodo.XXXXXXX**  

These include:
- `species_richness_matrix_all.tif`  
- `species_richness_suitable_all.tif`  
- `species_richness_within_species-rich-matrix_areas_all.tif`  
- `species_richness_within_species-rich-matrix_areas_declining.tif`  
- `species_richness_within_species-rich-matrix_areas_threatened.tif`

These derived rasters allow users to reproduce all hotspot analyses without requiring access to the original species-level AOH and range datasets.

### **Not included in this repository**
AOH-derived species rasters and IUCN Red List range maps used to delineate the extent of suitable habitat and matrix areas for each species (i.e., the inputs for `compute_species_richness.py`) are **not included** because of size and licensing restrictions.  

Other global datasets used in the study—such as the Human Footprint (HFP) dataset and spatial data on Protected Areas (PAs) and Other Effective Area-Based Conservation Measures (OECMs)—are likewise not included here. These datasets are publicly available from their original providers, as described in the **Materials and Methods** section of the manuscript accompanying this repository.
