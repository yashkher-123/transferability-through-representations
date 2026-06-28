# Training encoder and prediction head
#

## The flow of data during inference is as follows:
1. Feed source domain description into encoder model, get embedding
2. Feed target domain description into encoder model, get embedding
3. Feed both embeddings into prediction head, get predicted spearman

Encoder model is an MLP without a formal output layer
Prediction head is an MLP that outputs predicted transferability

Backwards pass will optimize for making the model predict the correct spearman

#
Files:
- model.ipynb - training model on transfer matrix and domain descriptors, simple eval
- transfer_model.pt - pytorch model
- predicted_transfer_matrix.csv - initial model transfer 34x34 transfer matrix prediction