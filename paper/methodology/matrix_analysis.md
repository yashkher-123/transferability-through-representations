## 2.3 Matrix analysis

I had to look into the transfer matrix to confirm that there was asymmetry present in domain transfer, and to show that there is a discrepancy between self vs. non-self transfer.

first, i found that the average of the diagonal of the 34x34 transfer matrix (on-diag meaning self transfer, where the source model is applied to its own domain) was 0.3997 (spearman) with a standared deviation of 0.0745. the off diagonal mean was 0.0931 with a standard deviation of 0.0828. the slightly higher std for off diagonal transfer could potentially be indicative of the variability of environments and how domain models can perform well in some areas and poorly in others. vairance in self transfer shows that some domains are simply more difficult to make wildfire predictions for.

i found that the average row maximum (disregarding the diagonal) was 0.25, which falls short of the 0.4 diagonal average but is meaningfully greater than the full off diag average. it shows that when a source model is transferred to different target domains, there is usually going to be at least 1 strong target domain.

a histogram of the transfer matrix values, colored by on diag or off diag values, show that the on/off diag values individually form normal distributions, where the distribution of the on diag values lie on the right tail of the off diag distribution.

i also made a graph of a heatmap of the transfer matrix, where higher transfer values are indicated by a deeper red hue. there is a clear line of deep red cells along the diagonal of the transfer matrix, which clearly shows the discrepancy between on and off diagonal matrix values.

this transfer matrix represents the target for the future transferability prediction model. the model is meant to take the descriptors for two domains as input, and output how well the source model will transfer into the target domain.


~~
Before training the transferability predictor, the empirical transfer matrix was analyzed to establish two properties of domain transfer: the distinction between self-transfer and cross-domain transfer, and the presence of asymmetric transfer relationships.

The mean diagonal transferability was 0.3997 (SD = 0.0745), compared with a mean off-diagonal transferability of 0.0931 (SD = 0.0828). Thus, models generally performed substantially better on their source domains than when transferred to other domains. The higher variability of off-diagonal transfer may reflect differences in how individual source models generalize across environmental regimes, while the variability in diagonal transfer indicates that some domains are intrinsically more difficult for wildfire prediction.

The mean row maximum, calculated after excluding each diagonal entry, was 0.25. Although this was below the diagonal mean of 0.3997, it was substantially greater than the overall off-diagonal mean of 0.0931. This indicates that most source domains have at least one other domain to which their trained model transfers relatively well, rather than transfer performance being uniformly poor across all non-self-transfer targets.

The distribution of transfer values further reflects the separation between self-transfer and cross-domain transfer. In a histogram separating diagonal and off-diagonal entries, both distributions were approximately bell-shaped, with the diagonal distribution shifted toward higher transferability values and occupying the upper tail of the off-diagonal distribution. A heatmap of the full transfer matrix shows the same pattern spatially, with a continuous band of high-transfer values along the diagonal.

These observations establish the empirical structure that the transferability model is intended to predict. Given the descriptors of a source and target domain, the model estimates the transferability associated with that directed source-target pair.