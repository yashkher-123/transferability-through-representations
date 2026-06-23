# Transfer matrix creation

The transfer matrix will include domain pairs T(i,j) which represents the error of a model trained on domain i (source) and tested on domain j (target)

Everything stored per domain_id -> (scaler, [model1, model2, ...], [train_X, train_y, test_X, test_y])

scalers are fit on the domain's train data.
At training, train data X from domain i will be fed through domain i scaler, then used with train data y from domain i to train domain i models
At inference (creating T), test data X from domain j will be fed through domain i scaler, then fed into domain i model, then evaluated against domain j test data y


The following cols are not being used going further:
"latitude", "longitude", "time", "pyrome", "ecoregion", "area", "cams_frpfire", "gwis_ba_target", "gwis_ba", "gwis_ba_valid_mask", "lsm"
- gwis ba is target leakage, the actual target is log_ba
- lat/lon/time are spatiotemporal indicators, model shouldn't know this
- pyrome/ecoregion are used for defining/evaluating domain choices, not for training
- area and ba_mask and lsm are satellite indicators


### final features are as follows:
fwi_mean	lccs_class_1	lccs_class_2	lccs_class_3	lccs_class_4	lccs_class_6	lccs_class_7	ndvi
pop_dens	rel_hum	skt	ssr	ssrd	swvl1	swvl2	swvl3	swvl4	t2m_max	t2m_mean	t2m_min	tp	vpd	ws10
(though for nn, lccs_class2 (forest) was removed to avoid multicolinearity)


After making the transfer matrix for xgboost, random forest, and the neural network models, my assupmtion going into it was that there would be strong correlation between matrices since I believed that transferability was mostly domain specific and model agnostic. That was not the case, and instead the highest correlatio between transfer matrices was in-domain performance. Models disagreed on transferability out of domain.
Because of this, I changed the random seed in each of the model types and remade the 3 transfer matrices. I compared the 2 random forest matrices with each other, the two xgb matrices with each other, and the two neural net matrices with each other to see how random initialization affects the model's view of tansferability. The random forest model's transfer matrices showed the highest correlation between each other, and the neural net transfer matrices showed low orrelation between each other, showing that the random forest measured transferability consistently while the neural net (or xgboost) did not. This is important because the ground truth transfer matrix should not be affected by the chosen model's quirks, and the neural net showed that small changes in the model drastically changed its view on transferability, while the rf stayed consistent. The rf model had ~0.99 correlation for in domain performance, and  ~0.92 correlation for out of domain performance, meaning the randomly seeded models highly agreed on transferability, indicatig that it could make a strong ground truth matrix.


To create final transfer matrix, I took the average of the two random forest matrices so that one random seed doesn't dominate.

## steps:
1. go from raw fire data to domain-split csvs
2. split domains into train/test, X/y
3. fit scalers per domain
4. train models on each domain
5. test models on every domain
6. generate transfer matrix for each model type

## Files:
- xgb_t_creation.ipynb - create transfer matrix for xgboost model
- rf_t_creation.ipynb - create transfer matrix for random forest model
- nn_t_creation.ipynb - create transfer matrix for neural network model
- t_comparison.ipynb - analyze transfer matrices and make draft of final matrix
- t_analysis.ipynb - differed seeded transfer matrices comparison, made final matrix

- define_domains.ipynb - turn raw giant wildfire csv into distinct domain csvs
- get_splits.ipynb - turn per-domain csvs into train/test X/y
- get_scalers.ipynb - fit and save per-domain scalers to train_X

- scalers/ - contains scalers for each domain
- test_X/ - testing feature values for each domain
- test_y/ - testing target values for each domain
- train_X/ - training feature values for each domain
- train_y/ - training target values for each domain
- domain_csvs/ - all wildfire data for each domain

- transfer_matrix_spearman_xgb.csv - transfer matrix for xgboost model
- transfer_matrix_spearman_rf.csv - transfer matrix for random forest model
- transfer_matrix_spearman_nn.csv - transfer matrix for neural net model
- transfer_matrix.csv - draft compiled transfer matrix from rf, xgb, nn
- rf_transfer_matrix.csv - final transfer matrix