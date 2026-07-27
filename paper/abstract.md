# outline

large wildfires devastate ecosystems, being able to predict them is important

model transfer is important since powerful models cannot be trained on data scarce regimes, instead they must be transferred from data rich areas

unsupervised domain adaptaion with feature discrepancy measurers is current method to measure transferability, fails on asymmetry

this method uses transferability as a supervised training signal rather than a feature similarity proxy

this model utilized a branched encoder and bias network with a deterministic biased eucliean head

beats baselines cleanly and the representations it makes are interpretable and relate to ecological relationships

(eventually) can be used to transparently predict which models transfer well to data scarce regimes

#

Large wildfires cause severe ecological and economic damage, making accurate fire spread prediction essential. Wildfire models are trained on region-specific data, so transferring a model to different fire regimes may not preserve accuracy. Existing methods use feature similarity between domains as a proxy for transfer quality, but these metrics are symmetric, treating source-to-target and target-to-source transfer as equivalent. Instead, we viewed transferability as a supervised learning target. An empirical domain transfer matrix was built by training a separate model on each of 34 ecoregion clusters and scoring it on every other domain, giving a direct score per domain pair rather than an approximation. This matrix demonstrates asymmetric transfer: performance differs depending on transfer direction, which feature-discrepancy cannot capture. A model was trained on the transfer matrix, with its architecture having a branched encoder, structured by environmental subsystems, to produce per-domain embeddings. It is paired with a bias network that learns source and target quality. A deterministic prediction head combines embedding distance with source and target biases to predict transferability. This architecture outperforms feature-discrepancy baselines (Maximum Mean Discrepancy and Wasserstein distance) with a 0.284 Kendall tau improvement. While XGBoost reached higher accuracy, boosting methods have no explainable representation space. Our model produces ecologically grounded representations: source and target biases correlate with corresponding transfer quality (Kendall tau 0.544 and 0.601, respectively), and embeddings recover environmental structures like pyromes and climate zones. These results show transferability-supervised representations provide a framework for identifying viable source models for data-scarce wildfire regimes.
