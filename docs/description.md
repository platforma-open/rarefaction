# Overview

Rarefaction is a technique used in ecology to assess species richness from the results of sampling. In the context of immunoinformatics, it is used to compare the clonal diversity of immune repertoires of different sizes.

This block performs rarefaction analysis on clonotype data. It calculates the mean number of unique clonotypes for various subsampling depths for each sample, providing insight into the clonal richness of the repertoires.

## How it works

The analysis proceeds as follows:

1.  **Input Data**: The block takes a dataset of clonotypes with abundance information for one or more samples.
2.  **Subsampling**: For each sample, the clonotypes are repeatedly subsampled at various depths (i.e., different numbers of clonotypes).
3.  **Counting Unique Clonotypes**: At each subsampling depth, the number of unique clonotypes is counted.
4.  **Averaging**: This process is repeated multiple times (iterations) for each depth to obtain a stable estimate of the mean number of unique clonotypes.
5.  **Output**: The block outputs a table and a graph showing the rarefaction curves for each sample. A rarefaction curve plots the number of unique clonotypes as a function of the number of sampled clonotypes.

A steeper rarefaction curve indicates a higher clonal diversity. If the curve reaches a plateau, it suggests that further sequencing would be unlikely to detect new clonotypes.
