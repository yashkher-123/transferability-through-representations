# info for probing embedding space

The goal of probing is to show that the embedding space is able to recover larger wildfire regimes.

Because the 33 domain descriptors get bottlenecked into an 8 dim embedding space before entering prediction head, my hope is that similar domains have similar embeddings 
or are located close together in the embedding space. I want to map each domain to each of the 5 pyromes from the archibald framework, and see if domains from the same pyrome 
cluster together in a flattened view of the space (pca).
#
Files:
- performance_deep_eval.ipynb - measure correlation between predicted transfer matrix and ground truth transfer matrix. Look at diag vs off-diag and overall vs test set correlation
- shap_analysis.ipynb - apply shap to entire model (encoder + prediction head) to see which domain descriptors are the biggest drivers of transferability