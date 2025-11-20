## Conservation_potential_of_the_matrix

This repository includes `Python` code used to reproduce the analyses for the manuscript:

**"Matrix areas reveal conservation opportunities for over half of the world’s terrestrial mammals"**

_by J.P. Ramírez-Delgado, M. Di Marco, C.J. Johnson, J.E.M. Watson, L. de Assis Barros, and O. Venter_

## Requirements
Users should have `ArcGIS Pro` version 3.4.0 or higher.  
Scripts use the `ArcPy` library and require the `Spatial Analyst` extension.

## Code
`Compute_species_richness.py` computes global species richness maps by summing binary habitat rasters for each species. Used for:
- All mammals  
- Mammals with declining population trends  
- Mammals with threatened status  
- Suitable-habitat richness for the all-mammal group

`Hotspot_delineation.py` identifies matrix-based richness hotspots using:
- Percentile-based richness thresholds
- Iterative coverage matching to reach target hotspot area
- Contiguity filtering (minimum area = 10 km²)

## Data
This repository includes the species richness rasters required to run `Hotspot_delineation.py`

AOH-derived species rasters and IUCN Red List range maps used to delineate the extent of suitable habitat and matrix areas for each species (i.e., the inputs for `compute_species_richness.py`) are not included because of size and licensing restrictions. Please refer to the Materials and Methods section of the manuscript accompanying this repository for full details on how these datasets were obtained, processed, and used in the analysis.

Other datasets used in the study—such as the global Human Footprint and spatial data on Protected Areas (PAs) and Other Effective Area-Based Conservation Measures (OECMs)—can be obtained from their original sources, as described in the Materials and Methods section of the manuscript.
