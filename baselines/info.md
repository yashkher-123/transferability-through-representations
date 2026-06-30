# Baseline comparison
Need to compare model performance to existing baselines that only look at statistical similarity

Now I need to validate that the model can outperform naive feature distribution predictors of transferability (or maybe it doesn’t win against baselines). To compare performance, I will use a rank-based correlation metric that purely analyzes strength of a monotonic relationship (spearman or kendall) since existing tools may not be optimized to predict the correct magnitude of the values that are in the ground truth transfer matrix.

## Baseline ideas:
- Raw distance comparison: compute distance (euclidean or cosine) between a domain pair’s 33 ecological descriptors
- Domain2vec: this was the tool meant to turn a dataset into a domain vector, not specialized for environmental processes though, and it’s unsupervised so it doesn’t use the transfer matrix as a training signal
- Maximum mean discrepancy and wasserstein distance: both are purely metrics to measure difference between two distributions
- Non-encoder architecture: takes as input [descriptor_i, descriptor_j, descriptor_i-descriptor_j] and outputs predicted transferability to see whether domain embeddings are even needed

For mmd/wasserstein: it should look at feature distribution discrepancy between base model input features, not the domain descriptors. This is because for traditional domain adaptation measurements, it's about the distance between source and target feature distributions in the input space of the model being transferred.

Raw distance calculation: should be done with the 33 feature domain descriptors. If it were done with the base model features, then it would be an ablation for mmd/wasserstein. Doing it on the domain descriptors would test whether the encoder model actually learned something meaningful about the domain descriptors or if descriptor distributions themselves are enough. Before computing raw distance, z-score normalize (more stable than linear) the descriptors. Use negative distance to create transfer matrix (greater number means lower distance means better transferability)

## Files:
- raw_distance.ipynb - generate raw distance T, compare transfer matrix to ground truth
- rawdist_matrix.csv - transfer matrix generated from raw distance calculations