import sys
import click
import csv

@click.command()
@click.argument('input_tsv_filepath', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument('output_tsv_filepath', type=click.Path(dir_okay=False, writable=True))
@click.option('--max-lines', 'max_lines', type=click.INT, default=None,
              help="Maximum number of lines to write. Processes all lines if not specified, "
                   "or if 0 or a negative value is provided.")
def process_and_write_tsv(input_tsv_filepath, output_tsv_filepath, max_lines):
    """
    Reads an input TSV file, processes it (e.g., takes a subset of lines),
    and writes the result to a new output TSV file.

    INPUT_TSV_FILEPATH: The path to the input TSV file.
    OUTPUT_TSV_FILEPATH: The path for the new output TSV file.
    MAX_LINES: [Optional] The maximum number of lines to write.
               Processes all lines if not specified, or if 0 or a negative value is provided.
    """
    click.echo(f"Processing input TSV file: {input_tsv_filepath}")
    click.echo(f"Will write output to: {output_tsv_filepath}")
    click.echo(f"Maximum lines to process: {max_lines if max_lines is not None and max_lines > 0 else 'All'}")

    line_count = 0
    lines_written = 0
    try:
        with open(input_tsv_filepath, mode='r', newline='') as infile, \
                open(output_tsv_filepath, mode='w', newline='') as outfile:

            reader = csv.reader(infile, delimiter='\t')
            writer = csv.writer(outfile, delimiter='\t')

            for row in reader:
                # If max_lines is specified and positive, and we've reached that count
                if max_lines is not None and (0 < max_lines <= line_count):
                    click.echo(f"\n--- Reached processing limit of {max_lines} lines from input ---")
                    break
                writer.writerow(row)
                lines_written += 1
                line_count += 1

        click.echo(f"Successfully wrote {lines_written} lines to {output_tsv_filepath}")

    except Exception as e:
        click.echo(f"Error during processing: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    process_and_write_tsv()