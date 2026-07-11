# Training encoder and prediction head
#

## The flow of data during inference is as follows:
1. Feed source domain description into encoder model, get embedding
2. Feed target domain description into encoder model, get embedding
3. Feed both embeddings into prediction head, get predicted spearman

Encoder model is an MLP without a formal output layer
Prediction head is an MLP that outputs predicted transferability

Backwards pass will optimize for making the model predict the correct spearman correlation between source model's predictions and target domain y data.

Model hyperparams:
After playing around with the hyperparameters of the encoder, I settled on the following:
- Input layer is dim 33 (domain descriptors)
- 2 hidden layers, each with 32 nodes
- Uses dropout of 0.2 (a fifth of neurons are randomly inactivated during training)
- Output embedding of dim 8

Similarly with the prediction head MLP, I went with this structure:
- Input layer dim 24 (e_i, e_j, e_i-e_j), the final 8 asymmetrically encode difference
-2 hidden layers each with 32 nodes
- No dropout (encoder had it to not overfit representations, head must be precise)
- Output single value of predicted performance
Final architecture uses Adam optimizer. 150 epochs and learning rate of 0.0005, batch size 64
All of this was made using pytorch.

# Versions
- v1 is encoder same size as prediction head
- v2 is encoder heavier than prediction head
- v3 is branched/modular encoder with mlp prediction head



#
Files:
- model.ipynb - training model on transfer matrix and domain descriptors, simple eval
- transfer_model.pt - pytorch model
- predicted_transfer_matrix.csv - initial model transfer 34x34 transfer matrix prediction

