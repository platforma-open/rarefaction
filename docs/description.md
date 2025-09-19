# Overview

Rarefaction is a technique used to assess species richness from the results of sampling. Specifically, it is used to compare the clonal diversity of immune repertoires of different sizes.

This block performs rarefaction analysis on clonotype data. It calculates the mean number of unique clonotypes for various subsampling depths for each sample, providing insight into the clonal richness of the repertoires.

The analysis is based on a random subsampling of clonotypes from each repertoire at different depths. At each depth, the number of unique clonotypes is recorded. This process is repeated multiple times to generate a smooth rarefaction curve, which represents the expected number of unique clonotypes as a function of the number of sampled clonotypes. The shape of the curve can be used to compare the diversity of different repertoires. For example, a steeper curve indicates a higher diversity.
