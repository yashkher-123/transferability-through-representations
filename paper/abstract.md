# outline

large wildfires devastate ecosystems, being able to predict them is important

model transfer is important since powerful models cannot be trained on data scarce regimes, instead they must be transferred from data rich areas

unsupervised domain adaptaion with feature discrepancy measurers is current method to measure transferability, fails on asymmetry

this method uses transferability as a supervised training signal rather than a feature similarity proxy

this model utilized a branched encoder and bias network with a deterministic biased eucliean head

beats baselines cleanly and the representations it makes are interpretable and relate to ecological relationships

(eventually) can be used to transparently predict which models transfer well to data scarce regimes

#

Large wildfires cause severe ecological and economic damage, making their prediction essential. Wildfire models are trained using historical fire data that may be abundant in some regions and sparse in others, and transferring a model to a different fire regime may not preserve accuracy. Therefore, knowing whether a model will transfer reliably between fire regimes is critical for deployment. Existing transferability estimation utilizes unsupervised domain adaptation through symmetric feature-discrepancy as a proxy for transfer quality. We instead created an empirical 34-domain transfer matrix as the supervised signal to train a model, rather than using feature similarity to approximate transferability, which struggles to model asymmetric transfer. The model's architecture has a branched encoder, structured by environmental subsystems (atmospheric conditions, ground state, fire behavior), to produce interpretable per-domain embeddings, along with a bias network that learns source and target quality from domain descriptors. A deterministic prediction head combines embedding distance with source and target biases to output predicted transferability, which forces domain representation to concentrate in the encoder. This architecture greatly outperforms feature-discrepancy baselines (0.284 kendall tau improvement), and while boosting methods reach higher accuracy, they have no explainable representation space. Our model, on the other hand, produces ecologically grounded representations: bias terms correlate strongly with source and target transfer quality (0.572 kendall tau), and the embeddings recover externally-validated environmental structure. These results show that transferability-supervised representations provide an interpretable framework for identifying viable source models for data-scarce wildfire regimes, with potential application to other environmental domain transfer problems.
