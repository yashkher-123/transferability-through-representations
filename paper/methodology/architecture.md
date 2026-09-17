## 2.5 Encoder architecture progression

the encoder model that predicts transferability is referred to as the transferability model. it takes as input the domain descriptors for a source and target domain, and has to output the predicted transferability when a source model is transferred to the target domain. not only should the model's predictions be accurate, but predictions should also be interpretable such that we can see what factors led to the transferability prediction between two domains. being able to analyze and compare internal domain structure will be able to tell us the strongest drivers of transferability overall, and provide instance-level interpretability during inference.



throughout all model iterations, i monitored the model loss curves and prediction distributions. i made sure that the train vs test loss curves did not show overfitting where test loss would rise up. for all iterations, the training loss curve lay below the test loss curve, potentially indicating that the inherent noise in the test set made it hard to predict. however, the test loss never rose during training, indicating the model did not overfit. for each iteration, i also created a hisogram of the model predctions, and overlayed it with the ground truth transfer matrix distribution. doing this helps to verify that model predictions did not collapse to the mean and that the model is able to find some signal in the data. early stopping was used to reduce unneed compute when training loss plateaued. dropout and batching needed to be included, and it will be included, for all future iterations of the model because the number of trainable parameters is likely to exceed the number of training samples. droupout and batching allows for more complex representations and slows down overfitting.

### v1

rather than taking in both domains at the same time, i wanted the transferability model to run for both domains individually, and then compare the representations created. this first version started as an encoder model connected to a prediction head. both of these modules were a neural net, and they were the same size/complexity in terms of number of layers and nodes per layer. dropout was implemented on the encoder model but not the prediction head to ensure more robust representations and more precise predictions. during a forward pass, the encoder module takes one domain as input and then outputs a domain embedding for that domain, and this is repeated so that there are embeddings for the source and target domains. these embedding vectors are concatenated and attached to a difference vector, which represents the difference between the two domain vectors. this 24 dim input (encoder embedding dim 8, times 2 for both domains, pluh 8 for difference vector) is fed into the prediction head, which outputs the predicted transferability. this model is able to handle asymmetry because a trainable prediction head neural network does not force symmetry in predictions. in fact, inputting domain descriptors i and j into the model in reverse order will cause the difference vector to become its opposite, which signals a different input to the prediction head.


### v2

this version focused on shifting the concentration of complexity of the transferability model to change from a perfect split between the encoder and prediction head to having more complexity within the encoder module. the encoder network was given more layers and nodes per layer, while the size of the prediction head was shrunk. the expectation was that representation quality would increase. it did, but at the expense of a marginal performance loss.



### v3

in this version i focused on making the encoder more interpretable. the flat mlp was exchanged for a modular one, where the mlp was split into three branches: atmospheric, ground, and fire behavior. the domain descriptor vector was split into these three environmental subsystems before being fed into the encoder. each branch mlp produced a 3-dim embedding, and the three branch embeddings were concatenated to form a 9-dim domain embedding. two domain embeddings are passed into the prediction head, like in the previous iteration. the aim was to make the representations more expressive and attributable to specific branches. for a given pair of embeddings, a source and a target, we can look into discrepancies between specific branch embeddings to see which subsystem causes the strongest transferability/pushes domains apart in embedding space. also, a branched encoder acts as an implicit regularization because it closes off connections between different types of vairables. when subsystem variables cannot interact, it makes branch embeddings more independent of each other. empricially after training, embeddings became more expressive, and embedding distance had a higher correlation with transfer quality compared to previous iterations, but this was met with marginal performance loss.


### v4

rather than attempting to encourage or hope for the learnable prediction head to identify that closer embeddings meant stronger transfer, i wanted to force this fact. in previous iterations, it was possible for the learnable prediction head to pick up the slack of less expressive embeddings. a deterministic prediction head with an inductive bias forcing strong domain representation was needed to prevent the prediction head from learning about domain representations in a way that the representations can be weaker. i removed learnability from the prediction head and replaced it with a euclidean distnce calculation between source and target domain embeddings. this explicity requires that more compatible domains cluster close together while less compatible domains are faerther apart in the embedding space. the prediction head takes the euclidean distance between embeddings and then squares and negates the value. the distance is squared for two reasons: 1, to make loss function differentiable when source embedding = target embedding, 2, to make closer embeddings cluster closer (small number squared is a smaller number) and farther embeddings even farther (large number squared is a larger number), which encourages stronger clustering. the value was negated to make greater prediction values (values closer to zero, closer embedding distance) indicative of stronger transfer, while lesser values (values that are more negative, farther distance) shoukld indicate worse transfer. the issue with simple euclidean distance is that  it falls into the same issue that feature discrepancy falls into: assuming symmetric transfer. the distance would need to be offset by a bias that gets added to the distance calculation. the prompted the creation of a bias network, where a domain descriptor is fed into an mlp and the network outputs 2 biases, a source and target bias, representing how strong that domain is as a source and as a target. in a forward pass, the source domain descriptor is passed through the branched encoder to produce a source domain embedding, and the descriptor is also passed through the bias network to produce the two biases. the same process happens with the target domain decriptor, to produce a target domain embedding and a source and target bias. the negated squared euclidean distance is taken between embeddings, and it is summed with the source bias from the source domain and the target bias from the target domain. the target bias from the source domain and the source bias from the target domain are unused in the calculation, so their gradients are zero in backpropogation. eventually the source domain would get used as a target domain in a future forward pass, which is when that bias would get used, and the opposite for the target domain.






## main notes:

as model iterations progressed, model performance decreased while representation strength increased. 









~~
2.5 Encoder architecture progression

The transferability model takes the domain descriptors of a source and target domain as input and predicts the transferability of a wildfire model trained on the source domain and applied to the target domain. In addition to predictive accuracy, the model is designed to produce interpretable domain representations. A useful representation should encode environmental structure that is relevant to transferability, allowing both the overall drivers of transferability and the factors underlying individual source-target predictions to be examined.

The transferability model was developed through four successive architectures. Across iterations, the architecture was progressively constrained to place more of the predictive structure in the domain embeddings and less in the prediction head. Model loss curves and prediction distributions were monitored throughout training. For all iterations, training loss remained below test loss, consistent with a generalization gap, but test loss did not increase during training, providing no indication of conventional overfitting. Prediction histograms were compared with the empirical transfer matrix distribution to verify that the model did not collapse toward the mean and instead reproduced variation in transferability. Early stopping was used when training loss plateaued. Dropout and mini-batch training were used throughout to regularize the comparatively high-capacity models relative to the number of training samples.

v1

The first architecture separated representation learning from transfer prediction. Rather than processing the source and target descriptors jointly, a shared encoder processed each domain independently to produce a domain embedding. The source and target embeddings were then concatenated with their element-wise difference and passed to a prediction head.

Both the encoder and prediction head were multilayer perceptrons with the same depth and width. Dropout was applied to the encoder to encourage representations that were less dependent on individual input features, while the prediction head remained unregularized to preserve its ability to model the transfer relationship. The encoder produced an 8-dimensional embedding for each domain. Concatenating the source embedding, target embedding, and their difference produced a 24-dimensional input to the prediction head, which output the predicted transferability.

This architecture can represent asymmetric transfer because the prediction head receives the ordered source and target representations rather than only a symmetric distance between them. Reversing domains (i) and (j) reverses the sign of the difference vector, producing a different input to the prediction head and therefore allowing different predictions for (i \rightarrow j) and (j \rightarrow i).

v2

The second architecture shifted model capacity from the prediction head into the encoder. The encoder was expanded by increasing its depth and width, while the prediction head was reduced in complexity. This placed greater capacity in the domain representations themselves rather than allowing the prediction head to compensate for weaker embeddings.

The resulting representations were empirically stronger, but this improvement was accompanied by a marginal decrease in predictive performance. This established an early tradeoff between the quality of the learned domain representation and the accuracy of the final transferability prediction.

v3

The third architecture introduced explicit structure into the domain representation to improve interpretability. The flat encoder was replaced with three separate branches corresponding to atmospheric conditions, ground conditions, and fire behavior. The domain descriptor vector was partitioned according to these subsystems, and each branch independently produced a 3-dimensional embedding. The three branch embeddings were concatenated to form a 9-dimensional representation for each domain.

This structure allows differences between source and target domains to be examined at the subsystem level. For a given source-target pair, the separation between the atmospheric, ground, and fire-behavior embeddings can indicate which subsystem contributes most strongly to the predicted transfer relationship. The branched structure also restricts interactions between variables assigned to different subsystems, providing an architectural form of regularization and reducing the ability of the encoder to represent arbitrary cross-subsystem interactions.

After training, the embeddings were more expressive, and the correlation between embedding distance and transfer quality increased relative to the previous architectures. This improvement in representation strength again coincided with a marginal decrease in predictive performance.

v4

The fourth architecture explicitly imposed the intended geometric interpretation of the embedding space. In the previous architectures, the prediction head remained free to learn the relationship between the two embeddings. Consequently, the prediction head could compensate for weak or poorly organized representations rather than requiring transferability to be encoded directly in the embedding geometry. V4 replaced this learnable prediction head with a deterministic distance-based function.

The source and target embeddings are compared using squared Euclidean distance. The distance is negated so that larger predicted values correspond to smaller embedding distances and therefore stronger transferability. Squaring the distance makes the function differentiable when the two embeddings coincide and changes the gradient contribution of larger distances while preserving the ordering of distances. The resulting term directly enforces the intended geometric interpretation: domains predicted to transfer well must occupy nearby locations in the embedding space, while domains predicted to transfer poorly must be separated.

A symmetric Euclidean distance alone, however, cannot represent asymmetric transfer. To preserve directionality, V4 includes a separate bias network. The bias network receives the domain descriptor vector and produces two scalar values, representing the domain's source bias and target bias. During a forward pass, the source descriptor is processed by both the branched encoder and the bias network to produce its embedding and its two directional biases. The same process is applied to the target descriptor.

For a source domain (i) and target domain (j), the prediction is formed from the negated squared Euclidean distance between their embeddings, plus the source bias associated with domain (i) and the target bias associated with domain (j). The opposite directional biases are not used in that particular prediction, so they receive no gradient from that forward pass. They become active when the corresponding domain appears in the opposite role in another source-target pair. This allows the same domain to have different effects depending on whether it is acting as a source or target while retaining a shared representation of its environmental structure.

Across the four architectures, a pattern emerged: predictive performance declined as the domain representations became more constrained and increasingly informative about transferability. In parallel, representation strength increased, as reflected by stronger relationships between embedding structure and empirical transfer quality. This tradeoff indicates that predictive accuracy and representation quality were not equivalent objectives for the transferability model, motivating the explicit geometric constraints introduced in V4.