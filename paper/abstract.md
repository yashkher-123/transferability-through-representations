# outline

large wildfires devastate ecosystems, being able to predict them is important

model transfer is important since powerful models cannot be trained on data scarce regimes, instead they must be transferred from data rich areas

unsupervised domain adaptaion with feature discrepancy measurers is current method to measure transferability, fails on asymmetry

this method uses transferability as a supervised training signal rather than a feature similarity proxy

this model utilized a branched encoder and bias network with a deterministic biased eucliean head

beats baselines cleanly and the representations it makes are interpretable and relate to ecological relationships

(eventually) can be used to transparently predict which models transfer well to data scarce regimes

#

Large wildfires cause severe ecological and economic damage, making the prediction of fire spread essential. Wildfire models are trained using historical fire data that may be abundant in some regions and sparse in others, and transferring a model to a different fire regime may not preserve accuracy. Therefore, quantifying and predicting a model's transferability between fire regimes is critical for deployment. Existing transferability estimation methods measure how similar the input features of two domains are as a proxy for transfer quality. However, these metrics are symmetric, meaning they view source-to-target and target-to-source transfer as equivalent. Instead, we treated transferability as a supervised learning target. We built an empirical domain transfer matrix by training a separate model on each of 34 spatially-clustered ecoregions and scoring it when applied to every other domain, giving a direct transfer score for each source-target pair rather than an approximated one. This matrix reveals that transfer is asymmetric: a model's performance moving from one domain to another differs in reverse, an effect that symmetric feature-discrepancy measures cannot capture. The model's architecture has a branched encoder, structured by environmental subsystems, to produce interpretable per-domain embeddings. It is paired with a bias network that learns source and target quality from domain descriptors. A deterministic prediction head combines embedding distance with source and target biases to output predicted transferability. Because the prediction head has no learnable parameters, all domain representation is captured by the encoder and bias network rather than the head itself. This architecture outperforms feature-discrepancy baselines (Maximum Mean Discrepancy and Wasserstein distance) with a 0.284 Kendall tau improvement, and while XGBoost reached higher accuracy, boosting methods have no explainable representation space. Our model, on the other hand, produces ecologically grounded representations: source and target bias terms each correlate with their corresponding transfer quality (kendall tau 0.544 and 0.601, respectively), and the embeddings recover externally-validated environmental structure, such as pyromes and climate zones. These results show that transferability-supervised representations provide an interpretable framework for identifying viable source models for data-scarce wildfire regimes.
