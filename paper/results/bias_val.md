## 3.5 Bias term validation

the bias terms are learned by the network, and they are meant to correspond to how good a domain is as a source vs as a target. a higher bias term will raise the final transferability prediction, indicating stronger transfer. a domain can have a high source bias but a low target bias or vice versa, meaning that the domain may be strong on only one side of the transfer.

source bias terms correspond with how good a domain is as a source. from the ground truth transfer matrix, we can approximate how good the domain is as a source by taking row-averages (excluding the diagonal), where the i in (i,j) stays constant. taking the average generally shows how good the domain is when it is used as the source domain in 33 other transfers.

target bias terms correspond with how good a domain is as a target. alternately from the source bias, we take column-averages (excluding diagonal), where j stays constant so we can observe target quality across 33 other transfer applications. diagonal entries are discarded since self-transfer conflates the definition of a 'strong source' or 'strong target' domain.

i found that row avg transfer vs src bias kendal tau was 0.5437, and target: col avg transfer vs tgt bias kendall tau was 0.6007. There was strong correlation, indicating the model learned how to identify domains as good sources or targets.



~~
The V4 bias network produces two separate values for each domain: a source bias and a target bias. The source bias represents how favorable a domain is as a source of transferable models, while the target bias represents how favorable it is as a target for models trained elsewhere. Because these biases are added directly to the predicted transferability, a higher bias increases the predicted transfer score. The two biases are learned independently, so a domain can be a strong source but a weak target, or the reverse.

To test whether the learned biases captured these intended meanings, source and target quality were estimated directly from the empirical transfer matrix. Source quality was approximated using the mean of each row after removing the diagonal entry. For a given source domain, this averages its transferability to the other 33 domains and therefore measures how well models trained in that domain tend to transfer elsewhere. This row average was compared with the learned source bias for the same domain.

Target quality was estimated analogously using column averages after removing the diagonal. For a given target domain, the column average measures how well models trained in the other 33 domains tend to transfer into it. The diagonal was excluded in both cases because self-transfer reflects in-domain performance and would confound the distinction between being a strong source and being a strong target.

The learned biases showed strong agreement with these empirical measures. The Kendall tau between source-domain row-average transferability and source bias was 0.5437, while the Kendall tau between target-domain column-average transferability and target bias was 0.6007. Thus, domains that empirically transfer well as sources generally received higher source biases, and domains that receive strong transfers generally received higher target biases. This provides direct evidence that the bias network learned distinct source- and target-specific properties of the domains rather than using the bias terms as arbitrary corrections to the embedding-distance component.