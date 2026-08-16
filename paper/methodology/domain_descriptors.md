## 2.4 Domain descriptors setup

with the transfer matrix as the traiing signal or target variable for transferability prediction, there needs to be an input. given that the model takes two domains as input (a source and target domain) and has to output the expected transferability, the model inputs must describe the two domains. these inpt features going forward will be called domain descriptors. the domain descriptors help to define the different overarching environmental conditions in a domain.

List of variable stats that will be aggregated for domain descriptor set:

- Vpd - indicates strong drying effectg
- Windspeed - provide oxygen to fires and spread embers
- T2m_max - higher max temp increases drying and lowers activation energy
- Ndvi - fuel load/biomass indicator
- Tp - rain increases activation energy for fires
- Fwi_mean - composite of multiple fire drivers
- swvl 1 and swvl 4 - 1 is for surface dryness, 4 can indicate drought conditions
- burned area - archibald et al paper for fire regimes
- Frp - how powerful are the fires that occur

Above features will have mean, std, 90th percentile. for example, for windspeed, we aggregate all cells in the domain and pull the windspeed values, then find the mean of the values, the standard devaiotn, and the 90th percentile value. the mean is chosen to indicate the overall conditions for a region, std is used to show how vairable/erratic the conditions are, and the 90th percentile shows how extreme the conditions get, which is meant to help for long-tailed features like frp and windspeed. Use mean and std to indicate spread and general distribution of data. Use 90th percentile since most features follow power law distributions and large fires depend on extreme environmental conditions, the upper percentile provides that.


For burned area and frp, only get mean/std/90th for cells where a fire actually occurred (ba>0). All other features will have stats aggregated from all cells in the domain (fire and non-fire cells) to get an unbiased view of the domain’s environment. getting general environmental stats using fire-only events 

Also will include these variables but not in the mean/std/90th format as before, they will simply have a singular value.
fire sparsity
fire seasonality
land cover diversity

Although burned area was the target variable to create the transfer matrix, these variables are meant to characterize regimes, which is independent of the downstream prediction task.

Land cover diversity: how diverse is the land type in a domain, is it mostly forests, or shrublands, or settlements, or a mix of different types. The information was obtained using the lccs classes from the seasfire cube. These were the classes: agriculture, forest, grassland, wetlands, settlement, shrubland, sparse vegetation, water.

The way diversity is calculated is using Simpson’s species diversity index, but applied to land cover. Land cover type percentages are aggregated across all cells in a domain, and fed into the Simpson diversity formula. If a land cover type is not present in the domain, it is not included in the summation calculation. 

My reasoning behind including land cover diversity is to encode ecosystem fragmentation. When a domain’s land is diverse, a fire can’t easily spread from one land cover type to another, especially across sparse vegetation or settlement or wetlands.

For fire sparsity, it is meant to encode how much land in a domain gets burned, relative to domain size. It is calculated as (num fire cells)/(total cells), and num fire cells is burned area>0.

For fire seasonality, this dictates whether most wildfires are concentrated in certain months. This idea was obtained from the Archibald et al paper, and seasonality was one of the features they used. It is defined as “the number of months required to reach 80% of the total average annual burned area” as per the paper’s exact wording. For instance, a value of 3 means that 3 months out of the year contribute to 80% of the fires in a domain.

It’s calculated like this: for each domain, sum up the total amount of burned area per month, order by amount, keep adding top burned area months until 80% of total burned area is surpassed.


The final domain descriptors for a domain is a 33 dimensional vector (3*10 + 3). the model takes the descriptor vectors for a source and target domain, then outputs the predicted transferability.