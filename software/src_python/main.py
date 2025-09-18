import sys
import polars as pl
import numpy as np
import json
import math
from typing import List, Dict, Tuple


def get_rarefaction_depths(total_abundance: int, num_points_requested: int) -> List[int]:
    """
    Generates a list of subsampling depths for rarefaction.
    """
    if total_abundance == 0:
        return [0]
    if total_abundance == 1:
        return [1]

    if num_points_requested <= 0:
        num_points_requested = 1
    if num_points_requested == 1:
        return [total_abundance]
    if num_points_requested == 2:
        return sorted(list({1, total_abundance}))

    depths = {1, total_abundance}
    num_intermediate_points = num_points_requested - 2

    if num_intermediate_points > 0:
        # Logarithmic spacing
        log_min = np.log10(2)
        log_max = np.log10(total_abundance)
        if log_max > log_min:
            log_spaced = np.logspace(
                log_min, log_max, num=num_intermediate_points)
            for d in log_spaced:
                depth = int(round(d))
                if 1 < depth < total_abundance:
                    depths.add(depth)

    # Ensure we have enough points, falling back to linear if needed
    if len(depths) < num_points_requested:
        additional_points_needed = num_points_requested - len(depths)
        linear_spaced = np.linspace(
            1, total_abundance, num=additional_points_needed + 2)
        for d in linear_spaced:
            depth = int(round(d))
            if 1 < depth < total_abundance:
                depths.add(depth)
                if len(depths) >= num_points_requested:
                    break

    return sorted(list(depths))


def rarefy(
    counts: np.ndarray,
    depth: int,
) -> int:
    """
    Perform a single rarefaction to a given depth.
    """
    if depth == 0:
        return 0

    total_abundance = counts.sum()
    if depth >= total_abundance:
        return len(counts)

    # Chao's formula for rarefaction
    n = total_abundance
    n_k = counts
    term = np.log(1.0 - depth / n)
    s_obs = len(n_k)
    f_k = np.bincount(n_k)[1:]

    s_est = s_obs
    for k in range(1, len(f_k) + 1):
        s_est -= f_k[k-1] * (1 - depth/n)**k

    return s_est


def run_rarefaction(
    input_tsv_filepath: str,
    output_tsv_filepath: str,
    num_points: int,
    num_iterations: int
):
    """
    Performs rarefaction analysis on clonotype data from a TSV file.
    """
    try:
        df = pl.read_csv(input_tsv_filepath, separator='\t')
        df = df.rename({
            "pl7_app_sampleId": "sample_id",
            "clonotypeKey": "clonotype_key"
        })
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    results = []

    for sample_id_val, sample_df in df.group_by("sample_id"):
        sample_id = sample_id_val[0] if isinstance(
            sample_id_val, tuple) else sample_id_val
        abundances = sample_df["abundance"].to_numpy()
        total_abundance = abundances.sum()

        if total_abundance == 0:
            results.append({
                "pl7_app_sampleId": sample_id,
                "subsampling_depth": 0,
                "mean_unique_clonotypes": "0.00"
            })
            continue

        depths = get_rarefaction_depths(total_abundance, num_points)

        for depth in depths:
            richness_values = []
            if num_iterations > 0:
                # Analytical rarefaction does not require iterations,
                # but we keep the loop structure in case a stochastic method is chosen later.
                # For Chao's formula, one calculation is enough.
                mean_richness = rarefy(abundances, depth)
            else:
                mean_richness = 0.0

            results.append({
                "pl7_app_sampleId": sample_id,
                "subsampling_depth": depth,
                "mean_unique_clonotypes": f"{mean_richness:.2f}"
            })

    try:
        results_df = pl.from_dicts(results)
        results_df.write_csv(output_tsv_filepath, separator='\t')
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

    print("Rarefaction analysis complete.")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python main.py <input_tsv> <output_tsv> <num_points> <num_iterations>", file=sys.stderr)
        sys.exit(1)

    input_tsv = sys.argv[1]
    output_tsv = sys.argv[2]
    try:
        num_points = int(sys.argv[3])
        num_iterations = int(sys.argv[4])
    except ValueError:
        print("Error: num_points and num_iterations must be integers.", file=sys.stderr)
        sys.exit(1)

    run_rarefaction(input_tsv, output_tsv, num_points, num_iterations)
