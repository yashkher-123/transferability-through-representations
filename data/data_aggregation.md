# Data Aggregation


### https://zenodo.org/records/13834057?preview_file=CHANGELOG_seasfire_v0.4+.pdf

## Fire Dataset
Data used is the Seasfire Cube. It's a 44gb zarr file covering 20 years (2001-2021) of global wildfire data
Spatiootemporal res: 8 days, 0.25 degrees

## Variable types (54 total variables) and examples:
-   Atmospheric - temp, humidity, windspeed, precipitation
-   Vegetation - land cover, ndvi, soil water
-   Socioeconomic - population density, settlement land cover, agriculture land cover
-   Fire descriptors - FWI, FRP, burned area


### https://www.nature.com/articles/s43247-023-00881-8

## Regime Mask
This dataset has created 62 different regions where they defined spatially separable wildfire regimes/domains
- ex: california chaparral, south afrcan fybnos
- each to create transfer matrix, wildfire models need to be trained on fires solely from their domain, this mask defines the domains
- need to hold out some regimes for eval later


### https://www.pnas.org/doi/10.1073/pnas.1211466110

## Pyromes
This dataset defines 5 unique non-contiguous wildfire regimes
- Fires from the same regime exhibit similar dynamics, even though they may not be from the same spatial domain (regime mask)
- should find that models trained on domains from the same pyrome transfer well (close in embedding space) during eval



## Steps:
1. Download seasfire cube dataset
2. leave it as a zip, use zarr, xarr, and other libraries to create two subsets of the entire dataset:
    - only has fires from 2011-2021 with BA/FRP>0 to train predictor models for transfer matrix
        - since this is a cube file and not just a record of wildfires, most cell are non fire, so a wildfire predictor model will perform poorly
    - only has cells from 2011-2021 to get aggregate stats per feature for inputs for encoder model
        - use data from a decade rather than full 20 years to keep sufficient window for stable per-regime statistics, a smaller timeframe mitigates drift
3. export new, filtered datasets, delete oringinal dataset to save space on computer
4. for each of the 2 subset datasets:
    - add a feature to each cell for domain using regime mask
    - add a feature to each cell for pyrome using pyrome mask