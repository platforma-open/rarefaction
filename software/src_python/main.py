import sys
import click
import csv

@click.command()
@click.argument('tsv_filepath', type=click.Path(exists=True, dir_okay=False, readable=True))
def print_tsv_content(tsv_filepath):
    """
    Reads a TSV file and prints its content to standard output.
    TSV_FILEPATH: The path to the TSV file.
    """
    try:
        with open(tsv_filepath, mode='r', newline='') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                # Join the columns back with a tab for printing,
                # or handle rows as needed (e.g., print(row) to see the list)
                print('\t'.join(row))
    except Exception as e:
        click.echo(f"Error processing file {tsv_filepath}: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    print_tsv_content()