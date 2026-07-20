# outline

large wildfires devastate ecosystems, being able to predict them is important

model transfer is important since powerful models cannot be trained on data scarce regimes, instead they must be transferred from data rich areas

unsupervised domain adaptaion with feature discrepancy measurers is current method to measure transferability, fails on asymmetry

this method uses transferability as a supervised training signal rather than a feature similarity proxy

this model utilized a branched encoder and bias network with a deterministic biased eucliean head

beats baselines cleanly and the representations it makes are interpretable and relate to ecological relationships

(eventually) can be used to transparently predict which models transfer well to data scarce regimes

#

Large wildfires cause severe ecological and economic damage, making their prediction essential. High performing wildfire models are typically trained on data-rich regions and must be transferred to data-scarce ones. Therefore, knowing in advance whether a model will transfer reliably between fire regimes is critical for deployment. Existing transferability estimation relies on unsupervised domain adaptation, using symmetric feature discrepancy measures as proxies for transfer quality. We instead created an empirical 34-domain transfer matrix as the supervised signal to train a model, rather than using feature similarity to approximate transferability, which struggles to model asymmetric domain transfer. The model's architecture uses a branched encoder, structured by physical subsystems (atmospheric conditions, ground state, fire behavior), to produce interpretable per-domain embeddings, paired with a bias network learning source and target quality from domain descriptors. A deterministic prediction head combines embedding distance with source and target bias terms to output predicted transferability, which forces domain representation to concentrate in the encoder. This architecture greatly outperforms feature-discrepancy baselines (0.284 kendall tau improvement), and while boosting methods reach higher raw accuracy, they yield no explainable representation space. Our model, on the other hand, produces ecologically grounded representations: bias terms correlate strongly with source and target transfer quality (0.572 kendall tau), and embedding geometry recovers externally-validated environmental structure. These results show that transferability-supervised representations offer an interpretable framework for identifying viable source models for data-scarce wildfire regimes, with potential for application to other environmental domain transfer problems.