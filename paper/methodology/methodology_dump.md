# Write down all steps in completing the project

## prep fire data
- seasfire cube dataset - fires from 2001-2021 with 50+ different fire and environmental variables, 8 day temporal resolution and 0.25 degree spatial res. this dataset compiled harmonized data from multiple different sources, so i can ensure its validity
- dataset was cut in half temporally to only include fires from 2011-2021 in order to reduce temporal variable shift - a single spatial area should exhibit homogenous patterns so best to cut temporal range in a way that still keeps most of data. also favors more recent environmental trends.
- got dataset of wwf teow, ~800 ecoregions on all land cover.


## define domains
- if i used N=800 to generate the transfer matrix, each domain would have too little data
- used a paper on strongest drivers of fire behavior, settled on using [ndvi, mean temp, precipitation, vpd, fwi] as a way to cluster ecoregions
- i used spatially constrained agglomerative clustering, where two similar ecoregions (similar by above variables) would get merged into one. kind of like when holding bubbles in hand, 
some bubbles merge together to form a larger one. spatially constrained means each region looks at 8 neighbors to choose which to merge with.
merging regions must be physically touching (with the exception of islands, which look for nearest neighbors)
- chose N=50 to balance number of fire samples per domain with size of transfer matrix.

## generate transfer matrix
- i went back into the seasfire cube dataset and pinpointed all cells where a fire occurred (gwis burned area greater than 0) and mapped each cell to a its domain. i found that 16 of the domains had insufficient
(less than 2000 fire samples) fire data, so including this in the transfer matrix would only introduce noise. because of this, these 16 domains would be cut out of the final matrix, leaving 34 domains
- i completely dropped the following variables from the dataset: biomes (base models will anyways train on a single domain, so likely part of same biome), cams_co2fire (two thirds of the values are missing), 
drought_code max and mean (precipitation and temp are the inputs for dc, so it's unnecessary), fcci_ba (opting for gwis_ba rather than fcci since fcci is monthly res), fwi_max 
(anyways have mean, and max will be noisy, mean is more stable), lai (ndvi does a better job for vegetation load), lst_day (anyways have temp), sst (anyways have temp), lsm (land sea mask 
won’t tell anything since fires are on land)
- i had to deal w the rest of the missing values in the dataset, namely soil water, ndvi, pop den, fwi, ssrd. i used knn imputation for swvl using precip, humidity, and temp as features since those directly 
affect soil water content. i used temporal imputation for ndvi since it doesn't change too much over time, and i simply dropped cells for the rest since the missing rows made up less than 1% of the dataset.
- for any base model used to generate the transfer matrix, these variables were used as features: fwi_mean lccs_class_1 lccs_class_2 lccs_class_3 lccs_class_4	lccs_class_6 lccs_class_7 ndvi pop_dens	rel_hum	skt 
ssr	ssrd swvl1 swvl2 swvl3 swvl4 t2m_max t2m_mean t2m_min tp vpd ws10
- for each domain, i pulled each cell's input X (above) and target y (log scaled gwis burned area [log scaled for stable training]) and aggregated them into X and y datasets. they were further split into train and 
test sets, with a 75-25 split. a standard scaler for each domain was fit onto the train X for each domain
- generating the transfer matrix would go like this: select domain i. train a base model on domain i's train x (scaled by domain i's scaler). for each domain (including itself) as j: take domain j's test data and 
scale it using domain i's scaler (using i's so that data is projected into a space the model understands), then feed scaled data into domain i's model. get transfer score (performance of model).
- by score, it meant i had to choose a metric by which to evaluate the model's performance. it had to be target-variance indifferet, relative/comparable, and show strong distinguishability between on and off diag 
cells in the transfer matrix. mse/mae were ruled out due to scaling issues, and r2 had too little variance between on/off diag. i ended up going with spearman.
- my initial assumption was that transferability was model agnositic, in other words it wouldn't matter which model class i chose to be the base model. i tried making a transfer matrix with rf, xgb, and nn, and 
instead found that they were uncorrelated (though xgb and rf had relatively higher correlation likely due to being tree ensembles). one idea i had was to take a weighted average of the 3 matrices, but that would 
only result in the weird molding of each model's unique inductive biases in a way that muddles transfer signal due to model disagreement.
- i then ran a seed stability test where i made another transfer matrix for each of the three model classes, but this time changing the random seed used to init/train the model. i found that xgb and nn had low 
correlation across their own seeds, while rf had high seed stability, meaning it could settle on a consistent definition of transferability. thus the final transfer matrix i made was simply an average of the two 
seeds of the rf transfer matrices.
- also analyzed the transfer matrix to confirm asymmetry and show on vs off diag variance and distribution of values.





## model iterations
- the main goal was to have an encoder model that could turn domains into embeddings, then compare those embeddings to output transferability. this would allow for embeddings to be analyzed and provide more model interpretability. this structure is reminiscent of a siamese network, except it is different in the prediction head and how the outputs of the twin neworks are handled.
- i had to set up the train, test, x, and y data. The x data is domain descriptors, basically top-level stats of each domain including the mean, std, and std of carefully-selected environmental descriptors. it also covered land cover diversity, fire seasonality, and fire sparsity. each domain had a set of 33 input features. this data was normalized with standard scaler, fit on train domains, applied to all domains. the y data was the i,j transferability score in the ground truth rf transfer matrix. the train data was a 30x30 matrix, and the test set was the rest 256 pairs, which included the 4 heldout domains. 
- in a forward pass (predicting transfer score for an i,j pair), the domain descriptors for domain i and domain j is fed into the model, and the output is a transferability prediction.
- across all iterations, dropout and batching was used in the encoder model to prevent overfitting, especially since there were only 900 training samples. also, in every iteration, analyzing the loss curves showed that both train and test lossed plateaued and test loss never rebounded up, but train loss always hung lower than test loss, likely due to noise/difficulty of test set. the first iteration was an mlp encoder that made an 8 dim embedding, and the two embeddings would get fed into another mlp in the form (e_i,e_j,e_i-e_j) and that would output transferability. the difference vector was added to encourage asymmetry and show the model differences in the embeddings. the embeddings it created were not very expressive, as shown through an embedding dist transfer matrix created using the first iteration's encoder model not having strong correlation with the ground truth transfer matrix. the second iteration shifted the model to having more of it's complexity concentrated in the encoder, whereas last time the size of the encoder and prediction head mlp's were the same. the assumption was that a more complex encoder and less complex prediction head would force embddings to be more expressive since the prediction head has less capacity to learn how embeddings relate. this did show up, but overall model performance decreased marginally compared to the first iteration. version 3 saw a branched encoder model, which split domain descriptors into 3 distinct physical subsystems: atmosphere, ground, and fire. each branch contributed 3 dims to the embedding, making the final concatenated embedding dimension 9. this model's performance was in between that of the first and second iterations, and embeddings seemed to be more closely related to the transfer signal. the final iteration 


## validation