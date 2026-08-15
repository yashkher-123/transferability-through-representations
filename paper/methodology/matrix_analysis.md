## 2.3 Matrix analysis

I had to look into the transfer matrix to confirm that there was asymmetry present in domain transfer, and to show that there is a discrepancy between self vs. non-self transfer.

first, i found that the average of the diagonal of the 34x34 transfer matrix (on-diag meaning self transfer, where the source model is applied to its own domain) was 0.3997 (spearman) with a standared deviation of 0.0745. the off diagonal mean was 0.0931 with a standard deviation of 0.0828. the slightly higher std for off diagonal transfer could potentially be indicative of the variability of environments and how domain models can perform well in some areas and poorly in others. vairance in self transfer shows that some domains are simply more difficult to make wildfire predictions for.

i found that the average row maximum (disregarding the diagonal) was 0.25, which falls short of the 0.4 diagonal average but is meaningfully greater than the full off diag average. it shows that when a source model is transferred to different target domains, there is usually going to be at least 1 strong target domain.

a histogram of the transfer matrix values, colored by on diag or off diag values, show that the on/off diag values individually form normal distributions, where the distribution of the on diag values lie on the right tail of the off diag distribution.

i also made a graph of a heatmap of the transfer matrix, where higher transfer values are indicated by a deeper red hue. there is a clear line of deep red cells along the diagonal of the transfer matrix, which clearly shows the discrepancy between on and off diagonal matrix values.