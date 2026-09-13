## 3.6 Ecological validation

I first of all found that:
atmospheric branch sq dist vs transfer, off-diag spearman: 0.4891
ground branch sq dist vs transfer, off-diag spearman: 0.4396
fire branch sq dist vs transfer, off-diag spearman: 0.4497

essentially for every i,j domain pair, i separated the domain encodings by branch, then took the sqaured euclidean distances between corresponding branch embeddings. this tells us that all three 
branches contributed almost equally to the final embedding distance, and the encoder did not collapse onto a single branch, no single set of features dominated.


I wanted to see if the model could recover affinity through its representations. i computed affinity as off-diag row averages, making source quality a measurement of affinity. i then made a pca graph of all 34 domain embeddings, and colored them by transfer affinity.
I found (pc1: r = 0.275 p = 0.114) and (pc2: r = -0.610 p = 0.00012), so one dim of the pca could capture the embedding dist variance well.

And I can see that as pc2 increases, affinity decreases (colors get darker). This is better than one of the last iterations when the model wasn’t able to capture affinity very well. Though, I can’t completely discount that since I computed affinity wrong that time.


i then went into validating each of the embedding branches against external ecological frameworks. the three branches, again, are fire, ground, and atmosphere. for each branch, i pulled all the embedding pieces out of the full domain embedding, then created a pca graph of it. points were labeled by an external framework. for the fire branch, points were colored by which pyrome they fell into. since the pyrome framework puts discontiguous regions into the same pyromes, i defined a domain's pyrome by the most dominant pyrome situated within the domain. for the atmosphere branch, i colored each domain by the most dominant koppen climate zone, as found in NOAA, found in the domain. for the ground branch, i labeled each domain by the most dominant land cover class, as defined by the United Nations Food and Agriculture Organization, found in each domain. i got these results:
I ran a nearest-neighbors test on each of the pca graphs, where every point would look at the 3 nearest neighbors and see if it shares the same local classes/clustering. I got these results for each branch:
atmo:
mean fraction of 3 nearest neighbors with same label: 0.4902
baseline mean: 0.2455, std: 0.0520
z-scored frac nearest neighbor: 4.70
ground:
mean fraction of 3 nearest neighbors with same label: 0.4118
baseline mean: 0.2618, std: 0.0517
z-scored frac nearest neighbor: 2.90
fire:
mean fraction of 3 nearest neighbors with same label: 0.4804
baseline mean: 0.2357, std: 0.0516
z-scored frac nearest neighbor: 4.74

(frac of x means for any given point, an average of x*3 points share the same label)
The class imbalance in colors/zones/pyromes/classes in the pca could artificially bring up the frac, so I shuffled the labels around (keep the points fixed, just randomly assign which point gets which label), and recompute the same nearest-neighbor score, do that 1000 times and avg/std to get baseline. Basically, the baseline mean is what to expect from pure chance given class sizes, and std is the standard deviation of these samples.

For all of these pca’s the z-score of the fraction was very high, meaning it’s near impossible that the clustering of this strength occurred due to chance alone. This is especially true for the fire and atmosphere branches, but the ground branch clustering wasn’t as strong (but still strong in absolute terms). Overall, external labels really do cluster locally more than chance.
