# Repertoire Rarefaction Analysis

This block performs rarefaction analysis on immune repertoire sequencing data. It helps to compare the clonal diversity of repertoires of different sizes by estimating the number of unique clonotypes that would be observed at smaller sampling depths.

## Functionality

- **Input**: A dataset containing clonotype abundances for one or more samples.
- **Analysis**: For each sample, the block computes rarefaction curves. These curves show the expected number of unique clonotypes as a function of the number of molecules sampled. The calculation is based on an efficient analytical formula (Chao1 estimator), which avoids computationally intensive simulations.
- **Output**:
  - A graph displaying the rarefaction curves for each sample, allowing for visual comparison of clonal diversity.
  - A table with the detailed data points of the rarefaction curves.

## How to use

1.  Select an input dataset containing clonotype abundances.
2.  Set the parameters for the analysis:
    - **Number of points**: The approximate number of points to calculate for the rarefaction curve.
    - **Number of iterations**: This parameter is kept for compatibility, but the analytical method used does not require multiple iterations.
3.  Run the block. The results will be displayed in the "Graph" and "Table" tabs.

## Development

To build the block from the source code, run the following command in the block's root directory:

`pnpm build:dev`

