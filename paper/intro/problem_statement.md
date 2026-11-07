## 1.1 Problem statement


Wildfires are becoming uncontrollable in recent years. Being able to predict when large wildfires will occur is incredibly important for both ecosystem and infrastructure health. However, most wildfire models are trained on data from western regions and deployed in western regions, as most reliable data collection occurrs there. These models aren't typically utilized on a globl scale because of ecosystem heterogenity.

A model trained on one region of the world cannot be guaranteed to perform equally or meaningfully well on another region with a different environmental 'fingerprint'. Regions that have similar climates, fuel sources, and fire patterns can expect strong fire model transfer performance.

Spatial generalization is treated as a post-hoc check, seeing whether a model trained on one region can transfer well to other regions does not have a consistent, generalizable system. 

Existing methods to measure and predict transferability between domains utilized unsupervised domain adaptation, often through feature discrepancy. This assumes symmetric transfer, where transfer from one domain to another will work equally well in reverse. This is possible due to one domain being a subset of another domain's environmental conditions, in which the 'contained' domain's model has to extrapolate to conditions of the 'outer' domain, while the outer domain simply has to interpolate within its own subset.

Transfer matrices have been used as an approach, but they simply use it as a tool for analysis rather than a supervised signal.

This paper addresses the supervised prediction of fire regime transferability without the need to actually train and deploy models on either regime.

~~
Large wildfires can cause substantial damage to ecosystems, infrastructure, and communities, making reliable wildfire prediction an important research problem. However, wildfire data are unevenly distributed across the world, with many of the most developed datasets concentrated in a limited set of regions. As a result, a wildfire model trained in one region may need to be applied in another region where less training data are available.

A model that performs well in one region cannot be assumed to perform equally well elsewhere. Different regions have distinct combinations of climate, vegetation, terrain, and fire behavior. These differences can determine how well patterns learned in one region carry over to another. Regions with similar environmental and fire characteristics may therefore support stronger transfer than regions with substantially different conditions.

Spatial generalization is typically evaluated after a model has already been developed by testing whether it performs well in another region. This provides a useful check for an individual model, but it does not provide a general way to predict transferability before the model is deployed. Existing approaches to estimating transferability often use differences between the data distributions of two regions as a proxy for how well a model will transfer. These approaches generally treat transfer as symmetric, meaning that if a model transfers well from one region to another, it should also transfer well in the reverse direction.

Transfer is not necessarily symmetric. Consider two regions where the environmental conditions of one region are largely contained within the range of conditions found in the other. A model trained in the narrower region may encounter unfamiliar conditions when applied to the broader region, while a model trained in the broader region may already have learned patterns that apply to the narrower region. The two directions can therefore produce different transfer performance even when the difference between the regions is the same.

Transfer matrices provide a way to measure these pairwise differences by recording how well models trained in each region perform when applied to every other region. However, such matrices have primarily been used to analyze transfer after the models have already been trained and tested. They do not provide a way to predict transferability from information about the regions themselves.

This paper develops a supervised approach for predicting wildfire model transferability from the characteristics of two regions, without first training and testing a wildfire model across that pair. The goal is to estimate which regional transfers are likely to be stronger or weaker based on the environmental and fire characteristics of the regions involved.

