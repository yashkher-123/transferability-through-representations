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





~~
The empirical transfer matrix provides the target for transferability prediction, but predicting transfer between two domains requires a representation of the environmental conditions within each domain. We therefore characterize each domain using a set of domain descriptors that summarize its underlying fire regime and environmental variability. For a source domain A and target domain B, the transferability model receives the corresponding descriptor vectors and predicts the expected transferability of a model trained on A and applied to B.

Ten continuous variables were selected to describe the environmental and fire characteristics of each domain: vapor pressure deficit (VPD), wind speed, maximum 2 m air temperature (T2m_max), normalized difference vegetation index (NDVI), total precipitation (Tp), mean fire weather index (FWI), soil water volume at levels 1 and 4 (SWVL1 and SWVL4), burned area, and fire radiative power (FRP). These variables capture complementary drivers and properties of wildfire regimes. VPD represents atmospheric drying, wind speed affects fire spread and ember transport, maximum temperature captures thermal and drying conditions, and NDVI provides an indicator of available vegetation. Precipitation generally reduces fire-conducive conditions, while FWI summarizes multiple meteorological drivers of fire potential. SWVL1 represents near-surface moisture conditions, while SWVL4 provides information about deeper soil moisture and longer-term drought conditions. Burned area characterizes the occurrence and extent of fire, while FRP characterizes the intensity of fires when they occur. Burned area was also included as a regime descriptor even though it was used to identify fire events and construct the empirical transfer matrix, because its role here is to characterize the source and target environments rather than serve as a downstream prediction target.

For each of the ten variables, the mean, standard deviation, and 90th percentile were calculated across the domain, producing 30 descriptors. The mean captures the general conditions of the domain, while the standard deviation captures spatial variability in those conditions. The 90th percentile captures the upper tail of each variable, which is particularly relevant for variables with strongly skewed or heavy-tailed distributions and for wildfire processes that can be influenced disproportionately by extreme environmental conditions.

Burned area and FRP were aggregated only over cells where a fire occurred, defined as cells with burned area greater than zero. This ensures that these descriptors characterize the properties of fires that actually occur within a domain rather than being dominated by the large number of non-fire cells. All other environmental variables were aggregated across both fire and non-fire cells to characterize the environmental conditions of the domain as a whole. Restricting these variables to fire-only cells would bias the descriptors toward conditions associated with observed fires rather than representing the underlying environment in which fires may or may not occur.

Three additional descriptors were included as single-value measures: fire sparsity, fire seasonality, and land cover diversity. Fire sparsity represents the proportion of the domain in which fire events occur and is calculated as the number of fire cells divided by the total number of cells in the domain, where a fire cell has burned area greater than zero. Fire seasonality measures the concentration of burning throughout the year. Following the definition used by Archibald et al., it is defined as the number of months required to account for 80% of the total average annual burned area. For each domain, burned area is summed by month, the months are ranked by total burned area, and the highest-contributing months are added until their cumulative contribution exceeds 80% of the annual total. A lower value therefore indicates that fire activity is concentrated into a smaller number of months.

Land cover diversity characterizes the heterogeneity of land cover within a domain. The calculation uses the LCCS classes available in the SEASFire Cube: agriculture, forest, grassland, wetlands, settlement, shrubland, sparse vegetation, and water. The proportion of each land cover class is calculated across all cells in the domain and used to compute Simpson's diversity index, excluding classes that are absent. Higher diversity indicates a greater mixture of land cover types within the domain. This descriptor was included to capture ecosystem heterogeneity because fires may encounter substantially different fuel structures and barriers to spread across heterogeneous landscapes, particularly where sparse vegetation, wetlands, or settlements interrupt otherwise continuous fuel.

Together, the ten variables summarized by three statistics and the three additional single-value descriptors produce a 33-dimensional descriptor vector for each domain. The transferability model uses the descriptor vectors of a source and target domain as its input and predicts the transferability associated with that directed domain pair.