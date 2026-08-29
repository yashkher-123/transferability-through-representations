## 3.1 Baselines

all baselines + transferability model transfer matrices get compared to ground truth rf transfer matrix. the baselines are maximum mean discrepancy, wasserstein distance, descriptor distance, xgboost, linear regression. embedding distance is also added to the graph, where for an (i,j) cell, we take the distance between the 9-dim domain embeddings and negate it.

the transferability model cleanly beat mmd, wasserstein distance, descriptor distance, and linear regression. embedding distance beat all of these previously listed except for linear regression, showing that the model representations alone can beat distribution distance proxies, while the final prediction layer on top of the representations provides the final increase in accuracy.

the xgboost model beats out all other baselines and the transferability model, which was expected since xgboost models typically outperform neural net-based models on small tabular datasets. the transferability model also suffers from an information bottleneck in order to maintain interpretability: compressing the domain representation into a 9-dim embedding + 2 biases limts the amount of information that can be passed into the prediction head, but keeping a low-dim representation space allows for more compressed and expressive embeddings, as will be explored in a later section.

overall, this shows that simply applynig a predictive layer, even a simple one, on top of model transferability will beat out feature discrepancy proxies for transferability prediction.