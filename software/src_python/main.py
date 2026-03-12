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


def rarefy(unique_ni: np.ndarray, ni_counts: np.ndarray, s_obs: int, total_abundance: int, depth: int) -> float:
    """
    Perform analytical rarefaction (interpolation) using the combinatorial formula.
    """
    if depth >= total_abundance:
        return float(s_obs)
    if depth == 0:
        return 0.0

    sum_p_miss = 0.0
    for ni, count in zip(unique_ni, ni_counts):
        if depth > total_abundance - ni:
            p_miss = 0.0
        else:
            log_p_miss = (
                lgamma(total_abundance - ni + 1) - lgamma(total_abundance - ni - depth + 1) -
                lgamma(total_abundance + 1) +
                lgamma(total_abundance - depth + 1)
            )
            p_miss = exp(log_p_miss)
        sum_p_miss += (p_miss * count)

    return s_obs - sum_p_miss


def extrapolate(s_obs: int, f1: int, f2: int, total_abundance: int, depth: int) -> float:
    """
    Perform analytical extrapolation to a given depth using the Chao1 formula.
    """
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
    num_iterations: int,
    extrapolation: bool
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

    print(f"Read {len(df)} rows from input TSV.")
    print(f"Parameters: num_points={num_points}, num_iterations={num_iterations}, extrapolation={extrapolation}")
    print("Pre-computing sample frequencies...")

    # Pre-computation pass to find max abundance and store sample data
    sample_data = {}
    max_abundance = 0
    grouped = df.group_by("sample_id")
    for sample_id_val, sample_df in grouped:
        sample_id = sample_id_val[0] if isinstance(
            sample_id_val, tuple) else sample_id_val
        abundances = sample_df["abundance"].to_numpy()
        total_abundance = int(abundances.sum())
        s_obs = len(abundances)
        
        # Calculate frequency values to avoid iterating over all counts
        unique_ni, ni_counts = np.unique(abundances, return_counts=True)
        
        f1 = 0
        f2 = 0
        for val, count in zip(unique_ni, ni_counts):
            if val == 1:
                f1 = int(count)
            elif val == 2:
                f2 = int(count)
        
        sample_data[sample_id] = (unique_ni, ni_counts, s_obs, f1, f2, total_abundance)
        if total_abundance > max_abundance:
            max_abundance = total_abundance

    print(f"Found {len(sample_data)} samples. Maximum sample abundance is {max_abundance}.")
    print("Running rarefaction analysis...")

    results = []
    total_samples = len(sample_data)
    for sample_index, (sample_id, (unique_ni, ni_counts, s_obs, f1, f2, total_abundance)) in enumerate(sample_data.items()):
        if total_abundance == 0:
            results.append({
                "pl7_app_sampleId": sample_id,
                "subsampling_depth": 0,
                "mean_unique_clonotypes": "0.00",
                "type": "Interpolation"
            })
            continue

        depths = get_rarefaction_depths(
            total_abundance, max_abundance, num_points)

        total_depths = len(depths)
        for depth_index, depth in enumerate(depths):
            if depth <= total_abundance:
                mean_richness = rarefy(unique_ni, ni_counts, s_obs, total_abundance, depth)
                point_type = "Interpolation"
            else:
                if extrapolation:
                    mean_richness = extrapolate(s_obs, f1, f2, total_abundance, depth)
                    point_type = "Extrapolation"
                else:
                    continue

            results.append({
                "pl7_app_sampleId": sample_id,
                "subsampling_depth": depth,
                "mean_unique_clonotypes": f"{mean_richness:.2f}",
                "type": point_type
            })

            # Print progress periodically (every 10%, or at least every 10 iterations)
            progress_step = max(1, total_depths // 10)
            if (depth_index + 1) % progress_step == 0 or (depth_index + 1) == total_depths:
                progress_percent = int(((depth_index + 1) / total_depths) * 100)
                print(f"Processed sample {sample_index + 1}/{total_samples}): {progress_percent}% complete", flush=True)

    no_data = len(results) == 0

    try:
        if results:
            results_df = pl.from_dicts(results)
        else:
            print("Warning: No clonotypes found in input. Writing empty output.", file=sys.stderr)
            results_df = pl.DataFrame(schema={
                "pl7_app_sampleId": pl.String,
                "subsampling_depth": pl.Int64,
                "mean_unique_clonotypes": pl.String,
                "type": pl.String,
            })
        results_df.write_csv(output_tsv_filepath, separator='\t')
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

    with open("noData.txt", "w") as f:
        f.write("true" if no_data else "false")

    print(f"Successfully wrote {len(results_df)} points to {output_tsv_filepath}.")
    print("Rarefaction analysis complete.")


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Usage: python main.py <input_tsv> <output_tsv> <num_points> <num_iterations> <extrapolation>", file=sys.stderr)
        sys.exit(1)

    input_tsv = sys.argv[1]
    output_tsv = sys.argv[2]
    try:
        num_points = int(sys.argv[3])
        num_iterations = int(sys.argv[4])
        extrapolation = sys.argv[5].lower() == 'true'
    except ValueError:
        print("Error: num_points and num_iterations must be integers.", file=sys.stderr)
        sys.exit(1)

    run_rarefaction(input_tsv, output_tsv, num_points,
                    num_iterations, extrapolation)
