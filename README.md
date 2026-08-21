# Rarefaction Analysis

Compare repertoire diversity fairly across samples sequenced to different depths. This Platforma block subsamples each library at a series of depths and plots how many unique sequences appear, producing rarefaction curves whose shape tells you whether you have captured a library's diversity or only scratched it.

Open-source analysis block for Platforma, the biologics discovery platform by MiLaboratories. For the full no-code workflow, see [platforma.bio](https://platforma.bio/).

## What it does

Unique-sequence counts are not comparable between samples of different sizes. Sequence one library twice as deeply as another and it will show more clonotypes regardless of whether it is genuinely more diverse. Rarefaction removes that confound: instead of comparing totals, it compares diversity at matched sampling depth.

The block draws random subsamples from each sample's count data at a range of depths, records the number of unique sequences at each, and repeats the draw many times per depth so the curve is a mean rather than one lucky sample. Plotted together, the curves let you read diversity directly from their shape — a curve still climbing steeply means more sequencing would keep revealing new sequences, while one that has flattened means the library's diversity is largely captured.

Extrapolation, enabled by default, extends each curve past the observed depth to estimate what deeper sequencing would yield — useful for deciding whether another run is worth it. The number of depth points and the number of iterations per depth are both configurable, trading runtime against curve smoothness.

## Inputs & outputs

* **Input:** per-sample count data for clonotypes or peptides, from any Platforma clonotyping, import, or peptide profiling block.
* **Output:** rarefaction curves per sample, as an interactive plot and as a table of expected unique sequences by depth.

## Specifications

| | |
|---|---|
| Block title in app | Rarefaction analysis |
| Modalities | Immune receptor repertoires (TCR, BCR) and peptides |
| Method | Random subsampling at multiple depths, averaged over repeated iterations |
| Extrapolation | Beyond observed depth; enabled by default |
| Parameters | Number of depth points, iterations per depth, CPU and memory |
| Views | Curves plot, results table |

## Use cases

* **Depth-fair diversity comparison:** compare richness between samples sequenced to different depths without the deeper one winning by default.
* **Sequencing sufficiency:** read curve slope to judge whether a library has been sequenced deeply enough, or whether more reads would keep finding new sequences.
* **Planning further sequencing:** use extrapolated curves to estimate what additional depth would return before committing to a run.
* **Library QC:** spot samples whose curves rise much faster or plateau much earlier than the rest of a cohort.
* **Synthetic library characterization:** assess how much of a designed library's theoretical diversity is actually present and observed.
* **Peptide libraries:** apply the same depth-corrected diversity comparison to peptide datasets.

## FAQ

### Why not just count unique sequences?

Because that count scales with sequencing depth. A sample with twice the reads will show more unique sequences even if the underlying libraries are equally diverse. Rarefaction compares at matched depth, which is what makes the comparison meaningful.

### How do I read a rarefaction curve?

By its slope at the right-hand end. Still climbing steeply means substantial unseen diversity remains — more sequencing would reveal more sequences. Flattening means most of the library's diversity has already been observed. Comparing curves at the same depth on the x-axis compares diversity fairly.

### What does extrapolation give me?

An estimate of unique sequences beyond the depth you actually sequenced, so you can judge the return on more sequencing before paying for it. It is a model-based projection, not an observation — treat it as guidance, not measurement.

### What do the iterations control?

How many random subsamples are drawn at each depth before averaging. More iterations produce smoother, more stable curves at the cost of runtime. The default is a reasonable balance; raise it when curves look noisy.

### Does it work on peptides?

Yes. Any per-sample count data works, including peptide datasets from Peptide Profiling.

## Documentation

Step-by-step guide: [Rarefaction](https://docs.platforma.bio/guides/vdj-analysis/rarefaction/)

## Part of the Platforma ecosystem

This block is part of [Platforma](https://platforma.bio/) by [MiLaboratories](https://github.com/milaboratory). Explore the other open-source blocks at [github.com/platforma-open](https://github.com/platforma-open) and the docs for V(D)J analysis at [docs.platforma.bio/biology-guides/vdj-analysis](https://docs.platforma.bio/biology-guides/vdj-analysis/).
