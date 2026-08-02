# fire regime transfer learning

predicting whether a wildfire model trained on one region will transfer to another, without needing to actually run the transfer experiment.

## the problem

wildfire models get built for a specific region and usually break somewhere else. right now the only way to check transfer is to just run it (expensive, doesn't scale) or fall back on distribution similarity metrics like mmd/wasserstein, which miss the cases where two regions look statistically similar but behave totally differently fire-wise, or vice versa.

nobody's trained a model that predicts transfer outcomes directly from domain descriptors and gets a usable embedding space out of it. that's what this is trying to do.

## Data

seasfire cube, 2001-2021, ~50 fire and environmental vars, 8 day res, 0.25 deg. cut down to 2011-2021 to reduce temporal drift and lean into more recent trends, still keeps most of the data.

domains come from wwf teow (~800 ecoregions), way too many for a usable transfer matrix. clustered down using ndvi, mean temp, precip, vpd, fwi (mean/std), spatially constrained agglomerative clustering (regions have to physically touch, 8 neighbors, islands are the exception). landed on N=50 as a tradeoff between samples per domain and matrix size.

16 domains had too little fire data (<2000 samples), dropped. left with 34 active domains for the real matrix, 30 train / 4 held out. the dropped 16 get reused later as a secondary eval set, data-sparse target domains basically.

## building the transfer matrix

train a base rf on domain i, test on every domain j including itself, score with spearman. tried r2 first, the gap between in-domain and out-of-domain was too small to train on. spearman gave a real gap.

assumed transferability would be model agnostic going in. it wasn't. built matrices with rf, xgb, and nn and cross-model correlation was low. tried weighting the three together, scrapped it, doesn't make sense to blend disagreeing inductive biases into one signal.

switched to picking the base model by seed stability instead of performance. rf was way more consistent across seeds than xgb or nn. final matrix is an average of two rf runs, different seeds.

confirmed the matrix is asymmetric, and it's real, not noise. mattered a lot for the architecture later, can't assume T[i,j] = T[j,i].

## domain descriptors

33 features per domain, aggregated over the full seasfire window. mean/std/p90 for vpd, ws10, t2m_max, ndvi, tp, fwi, swvl1, swvl4, gwis_ba, cams_frpfire, plus fire sparsity, land cover diversity, fire season length.

grouped into 4 branches: climate drivers, fuel state, fire behavior, regime descriptors. gwis_ba and cams_frpfire only computed over fire cells on purpose, capturing intensity conditional on fire happening rather than diluted by all the zeros.

## model

goal: an encoder that turns domain descriptors into embeddings and bias terms, then compares embeddings and adds biases to predict transfer. kind of a siamese setup, but the prediction head and how the two outputs get combined is different, plus the bias net.

went through 4 versions:

- **v1**, flat mlp encoder, 8 dim embedding, head takes (e_i, e_j, e_i - e_j). worked fine but embeddings weren't very expressive on their own.
- **v2**, shifted complexity into the encoder, shrunk the head. idea was forcing more of the work onto the embeddings themselves. embeddings got slightly better, overall performance dropped a bit.
- **v3**, branched encoder, split descriptors into atmosphere/ground/fire subsystems, 3 dims each, 9 dim total. motivated by a correlation heatmap from v2 showing descriptors were smeared across all dims instead of separating cleanly by subsystem. performance landed between v1 and v2, embeddings noticeably better.
- **v4**, same branched encoder plus a separate bias network. bias net outputs a source and target bias per domain. prediction is just -‖e_i - e_j‖² + b_i_src + b_j_tgt, no learned params in the head at all, it's a fixed formula. slightly worse raw accuracy than v1-v3 but way more interpretable, and no collapse, distance term and bias term contribute roughly equally.

## baselines

mmd and wasserstein run on the actual base model feature distributions, not the descriptors, the "traditional" domain adaptation approach. beaten badly on every cut, and now it's pretty clear why, they're symmetric by construction and the ground truth matrix isn't.

xgboost sets the ceiling on raw predictive accuracy. no representation space though, can't probe it the way you can an encoder.

flat mlp (same input scheme, no intentional embedding) and raw descriptor distance both get beat too. raw distance especially, descriptors alone without any learned comparison aren't saying much.

## does the embedding space actually mean anything

this is the part that matters more than beating baselines.

- bias terms line up with real domain quality. row-average transfer correlates with source bias, column-average with target bias. model is learning something about domains individually, not just pairwise compatibility.
- pca'd each branch and checked against external labels it never saw during training: fire branch vs archibald pyromes, atmosphere vs koppen zones, ground vs lccs land cover. all three cluster well above a shuffled-label baseline. fire and atmosphere clearest, ground weaker, which tracks since there's no clean "ground zone" framework to check against in the first place.
- combined embedding distance vs ground truth transfer is a solid off-diagonal correlation, way stronger than v1/v2's standalone embedding numbers.