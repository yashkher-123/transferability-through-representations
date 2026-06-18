# Data Aggregation


## Fire Dataset
### https://zenodo.org/records/13834057?preview_file=CHANGELOG_seasfire_v0.4+.pdf
Data used is the Seasfire Cube. It's a 44gb zarr file covering 20 years (2001-2021) of global wildfire data
Spatiootemporal res: 8 days, 0.25 degrees

#### Variable types (54 total variables) and examples:
-   Atmospheric - temp, humidity, windspeed, precipitation
-   Vegetation - land cover, ndvi, soil water
-   Socioeconomic - population density, settlement land cover, agriculture land cover
-   Fire descriptors - FWI, FRP, burned area


## Pyromes
### https://www.pnas.org/doi/10.1073/pnas.1211466110
This dataset defines 5 unique non-contiguous wildfire regimes
- Fires from the same regime exhibit similar dynamics, even though they may not be from the same spatial domain (regime mask)
- should find that models trained on domains from the same pyrome transfer well (close in embedding space) during eval


## Wildfire Drivers
### https://pmc.ncbi.nlm.nih.gov/articles/PMC2662419/
This study found the strognest wildfire predictor variables
- Net Primary Productivity (biomass) is the #1 characterizer of fire dynamics
- Next were seasonal temperature indicators (mean temp warmest month, mean temp wettest month, temp seasonality)
- Annual precipitation was also an important variable for predicting fires
- Human footprint surprisingly had little impact
Since most of these variables were not explicitly available in the seasfire cube, needed to be practical about choosing regime descriptors for clustering
- NDVI and NPP are both proxies for fuel load, they are just measured in different ways
- mean temp takes the place of seasonal temperatures for simplicity
- Total precipitation stayed the same
- VPD and FWI were also added as descriptors because they are strong wildfire predictors, but they were not used in the study


## On getting getting the wildfire domains:
### https://zenodo.org/records/13834057
This paper was originally going to be used to get a mask of 62 wildfire regimes globally. 
This would allow for a literature-backed way of defining a wildfire domain to create the transfer matrix. 
Domains within a single pyrome could also be tested by the embedding model to see if their locations in the embedding space are nearby. 
However, their data/mask was unavailable (the github repo link was broken and I couldn't find their data elsewhere). I tried contacting the authors, but no response. 
Because of this, I had to create my own set of wildfire domains using the WWF TEOW (~800 global ecoregions), and then cluster them based on wildfire characterizers.




## Steps:
1. Download seasfire cube dataset
2. leave it as a zip, use zarr, xarr, and other libraries to create a new subset of the original cube:
    - New subset only has fires from 2011-2021 (decreasing temporal window mitigates feature distribution shift over time)
4. for the subset dataset, apply the 5 pyrome mask to classify each cell into a pyrome (or none if the pyrome doesn't cover that cell)
5. Create 50 wildfire domains through spatially-constrained agglomerative clustering using (mean, std) from the characterizers from the wildfire drivers paper.
    - Now every cell has been mapped to a pyrome and a domain
6. Select every cell where burned area is nonzero (a fire occurred), and add that cell as a row to a csv.