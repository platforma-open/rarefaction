import sys
import click
import csv
import random
from collections import defaultdict
import math # Import math for ceil

def get_rarefaction_depths(total_abundance, num_points_requested):
    """
    Generates a list of subsampling depths for rarefaction.
    Aims to produce approximately num_points_requested distinct depths,
    including 1 and the total_abundance.
    Uses a mix of linear and logarithmic spacing for better coverage.
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

    # Ensure num_points_requested is not excessively large for small total_abundance
    # If total_abundance is small, we might not be able to generate num_points_requested distinct points.
    # Let's aim for roughly half linear and half log-spaced points if num_points_requested > 2

    num_intermediate_points = num_points_requested - 2
    if num_intermediate_points <= 0: # Should be handled by num_points_requested == 2 case
        return sorted(list(depths))

    # Add linearly spaced points
    # Number of linear points to add (roughly half of the intermediate points)
    num_linear_points = math.ceil(num_intermediate_points / 2.0)
    if total_abundance > 1 and num_linear_points > 0:
        linear_step = (total_abundance - 1.0) / (num_linear_points + 1)
        for i in range(1, num_linear_points + 1):
            depth = round(1 + i * linear_step)
            if 1 < depth < total_abundance:
                depths.add(int(depth))

    # Add logarithmically spaced points
    # Number of log points to add (roughly the other half)
    num_log_points = num_intermediate_points - len(depths) + 2 # Adjust based on already added points
    if total_abundance > 1 and num_log_points > 0:
        # We want points from log(1) up to log(total_abundance)
        # Smallest practical depth for log spacing is 2 if 1 is already included
        log_min = math.log(max(2, depths.copy().pop() if len(depths)>2 else 2 )) # Smallest existing depth > 1 or 2
        log_max = math.log(total_abundance)
        if log_max > log_min : # Ensure there's a range to pick from
            log_step = (log_max - log_min) / (num_log_points +1)
            for i in range(1, num_log_points + 1):
                depth = round(math.exp(log_min + i * log_step))
                if 1 < depth < total_abundance: # Ensure it's an intermediate point
                    depths.add(int(depth))

    # If we still don't have enough points (e.g. total_abundance is small)
    # try to fill with more linear points if possible, up to num_points_requested
    # or up to total_abundance -1 if that's smaller
    max_possible_distinct_depths = total_abundance
    if len(depths) < num_points_requested and len(depths) < max_possible_distinct_depths:
        # Fallback to more linear points if log spacing didn't yield enough unique points
        # or if the total_abundance is small
        additional_points_needed = min(num_points_requested - len(depths), max_possible_distinct_depths - len(depths))
        if total_abundance > 1 and additional_points_needed > 0:
            # Try to pick points that are not already in depths
            potential_depths = list(range(2, total_abundance)) # exclude 1 and total_abundance
            random.shuffle(potential_depths) # Shuffle to pick diverse points
            for d in potential_depths:
                if len(depths) >= num_points_requested or len(depths) >= max_possible_distinct_depths:
                    break
                if d not in depths:
                    depths.add(d)


    final_depths = sorted(list(d for d in depths if d <= total_abundance)) # Ensure no depth > total

    # If total_abundance is very small, it's possible we get fewer than num_points_requested
    # Ensure the list is not empty if total_abundance > 0
    if total_abundance > 0 and not final_depths:
        return [total_abundance]

    return final_depths


@click.command()
@click.argument('input_tsv_filepath', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument('output_tsv_filepath', type=click.Path(dir_okay=False, writable=True, allow_dash=True))
@click.option('--num-points', type=click.INT, default=10, show_default=True,
              help="Approximate number of rarefaction depth points per sample.")
@click.option('--num-iterations', type=click.INT, default=100, show_default=True,
              help="Number of random subsamples for each rarefaction depth.")
def run_rarefaction(input_tsv_filepath, output_tsv_filepath, num_points, num_iterations):
    """
    Performs rarefaction analysis on clonotype data from a TSV file.
    The input TSV file MUST have a header row with columns:
    pl7_app_sampleId, clonotypeKey, abundance.

    It calculates the mean number of unique clonotypeKeys for various
    subsampling depths for each sample.

    The output TSV file will have columns: pl7_app_sampleId, subsampling_depth, mean_unique_clonotypes.
    Use '-' for OUTPUT_TSV_FILEPATH to print to standard output.
    """
    click.echo(f"Reading data from: {input_tsv_filepath}")
    samples_data = defaultdict(list)

    try:
        with open(input_tsv_filepath, mode='r', newline='') as infile:
            reader = csv.reader(infile, delimiter='\t')
            try:
                header = next(reader)  # Always skip header row
                click.echo(f"Skipped header row: {header}")
                # Basic header validation (optional but good practice)
                expected_headers = ["pl7_app_sampleId", "clonotypeKey", "abundance"]
                if len(header) < 3 or not all(h in header for h in expected_headers[:2]): # Check first two essential
                    click.echo(
                        f"Warning: Input file header {header} does not look as expected "
                        f"(e.g., {expected_headers}). Proceeding, but check column order.",
                        err=True
                    )
            except StopIteration:
                click.echo("Error: Input file is empty or contains only a header.", err=True)
                sys.exit(1)

            for i, row in enumerate(reader):
                if len(row) < 3:
                    click.echo(f"Warning: Row {i+1} (after header): Expected at least 3 columns, got {len(row)}. Skipping: {row}", err=True)
                    continue
                sample_id, clonotype_key, abundance_str = row[0], row[1], row[2]
                try:
                    abundance = int(abundance_str)
                    if abundance < 0:
                        click.echo(f"Warning: Row {i+1} (after header): Negative abundance ({abundance}) not allowed. Skipping: {row}", err=True)
                        continue
                    if abundance > 0:
                        samples_data[sample_id].append((clonotype_key, abundance))
                except ValueError:
                    click.echo(f"Warning: Row {i+1} (after header): Non-integer abundance '{abundance_str}'. Skipping: {row}", err=True)
                    continue
    except FileNotFoundError:
        click.echo(f"Error: Input file not found: {input_tsv_filepath}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error reading input file: {e}", err=True)
        sys.exit(1)

    if not samples_data:
        click.echo("No valid data found in the input file to process after the header.", err=True)
        sys.exit(1)

    click.echo(f"Found data for {len(samples_data)} samples.")
    click.echo(f"Performing rarefaction with ~{num_points} depth points and {num_iterations} iterations per depth...")

    rarefaction_results = []

    for sample_id, clonotypes_with_abundances in samples_data.items():
        expanded_clonotypes = []
        for key, abund in clonotypes_with_abundances:
            expanded_clonotypes.extend([key] * abund)

        total_abundance = len(expanded_clonotypes)

        # click.echo(f"  Processing sample: {sample_id} (Total Abundance: {total_abundance})")

        current_rarefaction_depths = get_rarefaction_depths(total_abundance, num_points)
        # click.echo(f"    Depths for {sample_id}: {current_rarefaction_depths}")


        for depth in current_rarefaction_depths:
            if depth == 0:
                mean_richness = 0.0
                rarefaction_results.append([sample_id, 0, f"{mean_richness:.2f}"])
                continue

            if depth > total_abundance: # Should be rare due to get_rarefaction_depths logic
                # This case might occur if total_abundance is 0 and depth is >0 (e.g. from a fixed set of depths)
                # or if get_rarefaction_depths had an edge case.
                # For a depth greater than available items, richness is max possible.
                # However, standard rarefaction usually caps depth at total_abundance.
                # Let's assume get_rarefaction_depths handles this, or we can skip.
                # For safety, if this happens, we can report the richness at total_abundance
                # or simply skip this depth point if it's an anomaly.
                # Given current get_rarefaction_depths, this should not be an issue.
                # If it were, we might do:
                # num_unique_at_max = len(set(expanded_clonotypes))
                # rarefaction_results.append([sample_id, depth, f"{float(num_unique_at_max):.2f}"])
                continue


            current_depth_richness_values = []
            if total_abundance > 0 and num_iterations > 0:
                for _ in range(num_iterations):
                    actual_k = min(depth, total_abundance)
                    if actual_k == 0 :
                        num_unique_clonotypes = 0
                    else:
                        subsample = random.sample(expanded_clonotypes, k=actual_k)
                        num_unique_clonotypes = len(set(subsample))
                    current_depth_richness_values.append(num_unique_clonotypes)

            if current_depth_richness_values:
                mean_richness = sum(current_depth_richness_values) / len(current_depth_richness_values)
            else:
                mean_richness = 0.0
                if depth > 0 and total_abundance > 0:
                    pass

            rarefaction_results.append([sample_id, depth, f"{mean_richness:.2f}"])

    click.echo(f"Writing results to: {output_tsv_filepath}")
    try:
        is_stdout = (output_tsv_filepath == '-')
        out_stream = sys.stdout if is_stdout else open(output_tsv_filepath, 'w', newline='')

        writer = csv.writer(out_stream, delimiter='\t')
        writer.writerow(["pl7_app_sampleId", "subsampling_depth", "mean_unique_clonotypes"])
        for result_row in rarefaction_results:
            writer.writerow(result_row)

        if not is_stdout:
            out_stream.close()
        click.echo("Rarefaction analysis complete.")

    except Exception as e:
        click.echo(f"Error writing output file: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    run_rarefaction()