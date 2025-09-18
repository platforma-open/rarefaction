import sys
import polars as pl
import numpy as np
from math import lgamma, exp
from typing import List, Dict, Tuple


def get_rarefaction_depths(total_abundance: int, max_abundance: int, num_points_requested: int) -> List[int]:
    """
    Generates a list of subsampling depths for rarefaction and extrapolation.
    """
    if total_abundance == 0:
        return [0]

    depths = {1, total_abundance}

    # Interpolation points (log-spaced up to total_abundance)
    # Scale number of points based on sample size relative to max
    inter_ratio = total_abundance / max_abundance
    num_inter_points = max(0, int(num_points_requested * inter_ratio) - 2)

    if total_abundance > 1 and num_inter_points > 0:
        log_min = np.log10(2)
        log_max = np.log10(total_abundance)
        if log_max > log_min:
            log_spaced = np.logspace(log_min, log_max, num=num_inter_points)
            for d in log_spaced:
                depth = int(round(d))
                if 1 < depth < total_abundance:
                    depths.add(depth)

    # Extrapolation points (linearly spaced from total_abundance to max_abundance)
    num_extra_points = num_points_requested - len(depths)
    if num_extra_points > 0 and max_abundance > total_abundance:
        extra_depths = np.linspace(
            total_abundance, max_abundance, num=num_extra_points)
        for d in extra_depths:
            depth = int(round(d))
            if depth > total_abundance:
                depths.add(depth)

    return sorted(list(depths))


def rarefy(counts: np.ndarray, depth: int) -> float:
    """
    Perform analytical rarefaction (interpolation) using the combinatorial formula.
    """
    total_abundance = int(counts.sum())
    s_obs = len(counts)

    if depth >= total_abundance:
        return float(s_obs)
    if depth == 0:
        return 0.0

    sum_p_miss = 0.0
    for ni in counts:
        if depth > total_abundance - ni:
            p_miss = 0.0
        else:
            log_p_miss = (
                lgamma(total_abundance - ni + 1) - lgamma(total_abundance - ni - depth + 1) -
                lgamma(total_abundance + 1) +
                lgamma(total_abundance - depth + 1)
            )
            p_miss = exp(log_p_miss)
        sum_p_miss += p_miss

    return s_obs - sum_p_miss


def extrapolate(counts: np.ndarray, depth: int) -> float:
    """
    Perform analytical extrapolation to a given depth using the Chao1 formula.
    """
    total_abundance = int(counts.sum())
    s_obs = len(counts)
    f1 = np.sum(counts == 1)
    f2 = np.sum(counts == 2)

    if depth <= total_abundance:
        return float(s_obs)

    # Chao1 estimator for number of unseen species
    f0_hat = 0
    if f2 > 0:
        f0_hat = ((total_abundance - 1) / total_abundance) * (f1**2) / (2 * f2)
    else:
        # bias-corrected version for f2=0
        f0_hat = ((total_abundance - 1) / total_abundance) * \
            (f1 * (f1 - 1)) / 2

    t = depth - total_abundance

    # Chao et al. 2014 extrapolation formula
    if f1 > 0 and f0_hat > 0:
        s_extrapolated = s_obs + f0_hat * \
            (1 - (1 - f1 / (total_abundance * f0_hat + f1))**t)
        return s_extrapolated
    else:
        # Cannot extrapolate without singletons, return observed richness
        return float(s_obs)


def run_rarefaction(
    input_tsv_filepath: str,
    output_tsv_filepath: str,
    num_points: int,
    num_iterations: int
):
    """
    Performs rarefaction and extrapolation analysis on clonotype data from a TSV file.
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

    # Pre-computation pass to find max abundance and store sample data
    sample_data = {}
    max_abundance = 0
    grouped = df.group_by("sample_id")
    for sample_id_val, sample_df in grouped:
        sample_id = sample_id_val[0] if isinstance(
            sample_id_val, tuple) else sample_id_val
        abundances = sample_df["abundance"].to_numpy()
        total_abundance = int(abundances.sum())
        sample_data[sample_id] = (abundances, total_abundance)
        if total_abundance > max_abundance:
            max_abundance = total_abundance

    results = []
    for sample_id, (abundances, total_abundance) in sample_data.items():
        if total_abundance == 0:
            results.append({
                "pl7_app_sampleId": sample_id,
                "subsampling_depth": 0,
                "mean_unique_clonotypes": "0.00"
            })
            continue

        depths = get_rarefaction_depths(
            total_abundance, max_abundance, num_points)

        for depth in depths:
            if depth <= total_abundance:
                mean_richness = rarefy(abundances, depth)
            else:
                mean_richness = extrapolate(abundances, depth)

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
