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

steps:
1. go from raw fire data to domain-split csvs
2. split domains into train/test, X/y
3. fit scalers per domain
4. train models on each domain
5. test models on every domain
6. generate transfer matrix