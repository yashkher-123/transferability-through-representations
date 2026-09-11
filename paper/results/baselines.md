## 3.1 Baselines

all baselines + transferability model transfer matrices get compared to ground truth rf transfer matrix. the baselines are maximum mean discrepancy, wasserstein distance, descriptor distance, xgboost, linear regression. embedding distance is also added to the graph, where for an (i,j) cell, we take the distance between the 9-dim domain embeddings and negate it.

the transferability model cleanly beat mmd, wasserstein distance, descriptor distance, and linear regression. embedding distance beat all of these previously listed except for linear regression, showing that the model representations alone can beat distribution distance proxies, while the final prediction layer on top of the representations provides the final increase in accuracy.

the xgboost model beats out all other baselines and the transferability model, which was expected since xgboost models typically outperform neural net-based models on small tabular datasets. the transferability model also suffers from an information bottleneck in order to maintain interpretability: compressing the domain representation into a 9-dim embedding + 2 biases limts the amount of information that can be passed into the prediction head, but keeping a low-dim representation space allows for more compressed and expressive embeddings, as will be explored in a later section.

overall, this shows that simply applynig a predictive layer, even a simple one, on top of model transferability will beat out feature discrepancy proxies for transferability prediction.



~~
All baseline transfer matrices and the transferability model were evaluated against the empirical random forest transfer matrix using Kendall tau-b. In addition to the five baseline methods described previously, embedding distance was evaluated directly by taking the Euclidean distance between the 9-dimensional source and target embeddings and negating it to produce a transferability score.

The transferability model outperformed MMD, Wasserstein distance, descriptor distance, and linear regression. Embedding distance alone also outperformed these discrepancy-based methods, with the exception of linear regression. This indicates that the learned domain representations contain more information about transferability than direct measures of distributional or descriptor-level similarity. The improvement from embedding distance to the full transferability model further shows that the prediction layer extracts additional information from the learned representations beyond their geometric proximity.

XGBoost achieved the highest predictive agreement with the empirical transfer matrix, outperforming both the transferability model and the other baselines. This result is consistent with the strength of tree-based models on small tabular datasets, but it also exposes a tradeoff imposed by the transferability model's interpretability constraints. The encoder compresses each domain into a 9-dimensional representation and the directional bias terms provide only two additional scalars, restricting the information available to the final prediction function. This bottleneck limits predictive capacity, but produces a compact representation that can be directly analyzed for environmental structure, which is examined in the following sections.

Overall, the results show that learned predictive representations provide a stronger basis for transferability estimation than treating domain discrepancy alone as a proxy for transfer.