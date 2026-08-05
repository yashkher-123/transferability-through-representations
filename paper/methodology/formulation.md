## 2.1 Problem formulation

Model that predicts fire regime transferability. Basically: given two different environments (domains A and B), predict how well a model trained on domain A would perform on domain B. The main idea isn't to directly predict the mae/mse that a model would get if trained on the other domain's data, but to be able to rank different models on how well they would be able to transfer to another target domain, or rank different models on how well they would be the target that a predefined source domain could transfer to. 

Model creates and compares internal domain representations to predict transfer. There is a shared embedding space where where each environmental fire domain lies as a point in the embedding space. points close together should transfer well, while points farther away should generally transfer worse. viewing the domains in the embedding space adds a layer of interpretability, as we can see exacly which aspects of the two domains are causing the transferability prediction.

Able to model asymmetric transfer, going beyond feature discrepancy as a proxy for transfer. it is not guaranteed that transfer from domain a to domain b will work in reverse, and this predictor  will be able to model that.

Expected outcomes would be seeing which models would work well on data-scarce regions that don't have enough fire data to train a strong fire prediction model. Embedding model recovers ecological similarities and relationships. Generalize framework for other environmental processes such as flooding or soil quality, which are globally heterogenous with potential asymmetric transfer.

The general process will be: Empirically map fire transferability, Train a model, Analyze representations
