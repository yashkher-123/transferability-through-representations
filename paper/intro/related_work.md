## 1.2 Related work

There have been approaches that utilize a transferability matrix, basically a N x N table of N domains, where each (i,j) entry represents the accuracy of a model trained on domain i and applied to domain j. No work has been done to use the transfer matrix as training data for a model, they focus on clustering regions of the matrix and analyzing them. 

Generating a full transfer matrix also requires N models to be trained and N^2 evaluation loops. As will be further shown, transferability is not model-agnostic, meaning the inductive biases of model used to generate the matrix will be present in the transferability rankings it generates. This approach also inherentlydoes not generalize, since to add a new domain, an extra model will need to be trained and 2N+1 evaluation loops will need to be ran.

Taking a step back, one way to sidestep the 'model dependent' nature of a transfer matrix is through unsupervised domain adaptation. Existing feature discrepancy methods like mean maximum discrepancy or wasserstein distance are a proxy for transferability by measuring feature similarity between domains. This has been not only been disproven to be a strong measure of transferability, but it also assumes symmetric transfer due to feature distance being a symmetric measure.

Tools like Domain2Vec predict feature transferability specifically for image data. There has not been a generalized framework for predicting domain transferability using tabular data. This paper attempts to apply a generalizable framework to wildfires, though these same ideas can be reused for globally heterogenous environmental processes such as flodding and drought prediction.

Wildfire Genome and GEOSPOT are systems that also generate soemthing along the lines of a transfer matrix, so does sangiorini (mispell) et al. but they nevr specifically train on the transfer matrix, let alone generate environmental embedddings because of it.