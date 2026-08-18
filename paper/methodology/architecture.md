## 2.5 Encoder architecture progression

the encoder model that predicts transferability is referred to as the transferability model. it takes as input the domain descriptors for a source and target domain, and has to output the predicted transferability when a source model is transferred to the target domain. not only should the model's predictions be accurate, but predictions should also be interpretable such that we can see what factors led to the transferability prediction between two domains. being able to analyze and compare internal domain structure will be able to tell us the strongest drivers of transferability overall, and provide instance-level interpretability during inference.



throughout all model iterations, i monitored the model loss curves and prediction distributions. i made sure that the train vs test loss curves did not show overfitting where test loss would rise up. for all iterations, the training loss curve lay below the test loss curve, potentially indicating that the inherent noise in the test set made it hard to predict. however, the test loss never rose during training, indicating the model did not overfit. for each iteration, i also created a hisogram of the model predctions, and overlayed it with the ground truth transfer matrix distribution. doing this helps to verify that model predictions did not collapse to the mean and that the model is able to find some signal in the data. early stopping was used to reduce unneed compute when training loss plateaued. dropout and batching needed to be included, and it will be included, for all future iterations of the model because the number of trainable parameters is likely to exceed the number of training samples. droupout and batching allows for more complex representations and slows down overfitting.

### v1

rather than taking in both domains at the same time, i wanted the transferability model to run for both domains individually, and then compare the representations created. this first version started as an encoder model connected to a prediction head. both of these modules were a neural net, and they were the same size/complexity in terms of number of layers and nodes per layer. dropout was implemented on the encoder model but not the prediction head to ensure more robust representations and more precise predictions. during a forward pass, the encoder module takes one domain as input and then outputs a domain embedding for that domain, and this is repeated so that there are embeddings for the source and target domains. these embedding vectors are concatenated and attached to a difference vector, which represents the difference between the two domain vectors. this 24 dim input (encoder embedding dim 8, times 2 for both domains, pluh 8 for difference vector) is fed into the prediction head, which outputs the predicted transferability. this model is able to handle asymmetry because a trainable prediction head neural network does not force symmetry in predictions. in fact, inputting domain descriptors i and j into the model in reverse order will cause the difference vector to become its opposite, which signals a different input to the prediction head.


### v2

this version focused on shifting the concentration of complexity of the transferability model to change from a perfect split between the encoder and prediction head to having more complexity within the encoder module. the encoder network was given more layers and nodes per layer, while the size of the prediction head was shrunk. the expectation was that representation quality would increase. it did, but at the expense of a marginal performance loss.



### v3





### v4