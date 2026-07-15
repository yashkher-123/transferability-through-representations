# outline

large wildfires devastate ecosystems, being able to predict them is important

model transfer is important since powerful models cannot be trained on data scarce regimes, instead they must be transferred from data rich areas

unsupervised domain adaptaion with feature discrepancy measurers is current method to measure transferability, fails on asymmetry

this method uses transferability as a supervised training signal rather than a feature similarity proxy

this model utilized a branched encoder and bias network with a deterministic biased eucliean head

beats baselines cleanly and the representations it makes are interpretable and relate to ecological relationships

(eventually) can be used to transparently predict which models transfer well to data scarce regimes

#