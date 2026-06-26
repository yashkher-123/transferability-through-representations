# Encoder input generation, aggregating domain descriptors

List of variable stats that will be aggregated for domain descriptor set:

- Vpd - indicates strong drying effectg
- Windspeed - provide oxygen to fires and spread embers
- T2m_max - higher max temp increases drying and lowers activation energy
- Ndvi - fuel load/biomass indicator
- Tp - rain increases activation energy for fires
- Fwi_mean - composite of multiple fire drivers
- swvl 1 and 4 - 1 is for surface dryness, 4 can indicate drought conditions
- burned area - archibald et al paper for fire regimes
- Frp - how powerful are the fires that occur

Above features will have mean, std, 90th percentile


For burned area and frp, only get mean/std/90th for cells where a fire actually occurred (ba>0). All other features will have stats aggregated from all cells in the domain (fire and non-fire cells) to get an unbiased view of the domain’s environment.

Use mean and std to indicate spread and general distribution of data. Use 90th percentile since most features follow power law distributions and large fires depend on extreme environmental conditions, the upper percentile provides that.

Also will include these variables but not in the mean/std/90th format as before
- fire sparsity
- fire seasonality
- land cover diversity

Above features will have a single value


Although burned area was the target variable to create the transfer matrix, these variables are meant to characterize regimes, which is independent of the downstream prediction task.

#
The way diversity is calculated is using Simpson’s species diversity index, but applied to land cover. Land cover type percentages are aggregated across all cells in a domain, and fed into the Simpson diversity formula. If a land cover type is not present in the domain, it is not included in the summation calculation. 

For fire sparsity, it is meant to encode how much land in a domain gets burned, relative to domain size. It is calculated as (num fire cells)/(total cells), and num fire cells is burned area>0.
#
For fire seasonality, this dictates whether most wildfires are concentrated in certain months. This idea was obtained from the Archibald et al paper, and seasonality was one of the features they used. It is defined as “the number of months required to reach 80% of the total average annual burned area” as per the paper’s exact wording. For instance, a value of 3 means that 3 months out of the year contribute to 80% of the fires in a domain.
#
Files:

- domain_descriptors.ipynb - identify which features to use for domain descriptors
- domain_stats_simple.ipynb - get per-domain stats for simple features (mean, std, 90th)
- domain_stats_complex.ipynb - get per-domain stats for complex features (sparsity, diversity, seasonality)

- simple_domain_stats.csv - mean,std,90th for simple features per-domain
- domain_descriptions.csv - full dataset of all per-domain stats