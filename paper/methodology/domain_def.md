## domain definition

I had to define multiple spatially contiguous wildfire domains around the globe. this would provide the regions needed to train the models that will be cross-tested to create the transfer matrix. 

i originally wanted to use a paper that defined 15 global fire regimes, then divided them into a total of 62 contiguous wildfire domains. this would have been perfect, but their data was not made available due to a github 404. i emailed the authors with no response. i instead had to recreate domains from scratch.

their approach was to create 15 overarching domains and then go more granular. i could not do this since there is not a coarse wildfire regime mapping (the archibald 5 pyromes is discontiguous and does not span the entire globe). i instead had to start granular and build up to coarser domains. i used the wwf teow which had around 800 spatially contiguous environmental domains, then used spatially constrained multivariate clustering (agglomerative clustering in this case) to merge together domains that have similar 'wildfire' environments, which meant using ndvi, precip, mean temp, vpd, fwi as features to compare domains.

i used this clustering algorithm to define 50 spatially-contiguous wildfire domains across the globe. i then found all the cells in each domain where the burned area was greater than zero, indicating a fire event. there were 16 domains that had fewer than 2000 fire events, and those domains were dropped. this reveals a tradeoff that increasing the domain count will yeild more values in the transfer matrix, but it will decrease the number of fire events in each domain. the 16 domains were dropped due to insufficient data, adding them into a transfer matrix would introduce noise and not supply a strong transferability signal.

this resulted in a final count of 34 domains. 4 domains will be completely held out for testing. the training set will be a 30x30 matrix, and the testing set will be the rest of the 256 cells. 