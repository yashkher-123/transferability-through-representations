## 3.5 Bias term validation

the bias terms are learned by the network, and they are meant to correspond to how good a domain is as a source vs as a target. a higher bias term will raise the final transferability prediction, indicating stronger transfer. a domain can have a high source bias but a low target bias or vice versa, meaning that the domain may be strong on only one side of the transfer.

source bias terms correspond with how good a domain is as a source. from the ground truth transfer matrix, we can approximate how good the domain is as a source by taking row-averages (excluding the diagonal), where the i in (i,j) stays constant. taking the average generally shows how good the domain is when it is used as the source domain in 33 other transfers.

target bias terms correspond with how good a domain is as a target. alternately from the source bias, we take column-averages (excluding diagonal), where j stays constant so we can observe target quality across 33 other transfer applications. diagonal entries are discarded since self-transfer conflates the definition of a 'strong source' or 'strong target' domain.

i found that row avg transfer vs src bias kendal tau was 0.5437, and target: col avg transfer vs tgt bias kendall tau was 0.6007. There was strong correlation, indicating the model learned how to identify domains as good sources or targets.
