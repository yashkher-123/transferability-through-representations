## 2.1 Problem formulation

Model that predicts fire regime transferability. Basically: given two different environments (domains A and B), predict how well a model trained on domain A would perform on domain B. The main idea isn't to directly predict the mae/mse that a model would get if trained on the other domain's data, but to be able to rank different models on how well they would be able to transfer to another target domain, or rank different models on how well they would be the target that a predefined source domain could transfer to. 

Model creates and compares internal domain representations to predict transfer. There is a shared embedding space where where each environmental fire domain lies as a point in the embedding space. points close together should transfer well, while points farther away should generally transfer worse. viewing the domains in the embedding space adds a layer of interpretability, as we can see exacly which aspects of the two domains are causing the transferability prediction.

Able to model asymmetric transfer, going beyond feature discrepancy as a proxy for transfer. it is not guaranteed that transfer from domain a to domain b will work in reverse, and this predictor  will be able to model that.

Expected outcomes would be seeing which models would work well on data-scarce regions that don't have enough fire data to train a strong fire prediction model. Embedding model recovers ecological similarities and relationships. Generalize framework for other environmental processes such as flooding or soil quality, which are globally heterogenous with potential asymmetric transfer.

The general process will be: Empirically map fire transferability, Train a model, Analyze representations

To start, i used the seasfire cube dataset, which is a zarr dataset data from 2001-2021, global range at 8-day, 0.25deg resolution. given the cubic nature of the dataset, it includes environmental data from both fire and non-fire events. the dataset has vegtation, atmospheric, socioeconomic, and wildfire-based variables and pulls its data from many reputable sources, making the data valid. the following variables were dropped from the dataset for the following reasons:
biomes (base models will anyways train on a single domain, so likely part of same biome), cams_co2fire (two thirds of the values are missing), drought_code max and mean (precipitation and temp are the inputs for dc, so it's unnecessary), fcci_ba (opting for gwis_ba rather than fcci since fcci is monthly res), fwi_max (anyways have mean, and max will be noisy, mean is more stable), lai (ndvi does a better job for vegetation load), lst_day (anyways have temp), sst (anyways have temp), lsm (land sea mask won't tell anything since fires are on land)
