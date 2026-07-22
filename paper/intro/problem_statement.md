## 1.1 Problem statement


Wildfires are becoming uncontrollable in recent years. Being able to predict when large wildfires will occur is incredibly important for both ecosystem and infrastructure health. However, most wildfire models are trained on data from western regions and deployed in western regions, as most reliable data collection occurrs there. These models aren't typically utilized on a globl scale because of ecosystem heterogenity.

A model trained on one region of the world cannot be guaranteed to perform equally or meaningfully well on another region with a different environmental 'fingerprint'. Regions that have similar climates, fuel sources, and fire patterns can expect strong fire model transfer performance.

Spatial generalization is treated as a post-hoc check, seeing whether a model trained on one region can transfer well to other regions does not have a consistent, generalizable system. 

Existing methods to measure and predict transferability between domains utilized unsupervised domain adaptation, often through feature discrepancy. This assumes symmetric transfer, where transfer from one domain to another will work equally well in reverse. This is possible due to one domain being a subset of another domain's environmental conditions, in which the 'contained' domain's model has to extrapolate to conditions of the 'outer' domain, while the outer domain simply has to interpolate within its own subset.

This paper addresses the supervised prediction of fire regime transferability without the need to actually train and deploy models on either regime.