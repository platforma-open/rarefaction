import pytest
from click.testing import CliRunner
import csv
import os
import random  # Used for setting seed in some test scenarios if needed

# Adjust the import path if your main.py is located differently relative to tests
# Assuming test_main.py is in a 'tests' folder and main.py is in the parent 'src_python' folder:
import sys

# Add the src_python directory to sys.path to allow importing main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import run_rarefaction, get_rarefaction_depths


@pytest.fixture
def create_tsv_file(tmp_path):
    """Fixture to create a temporary TSV file for testing."""

    def _create_tsv_file(filename, headers, data_rows):
        file_path = tmp_path / filename
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(headers)
            writer.writerows(data_rows)
        return file_path

    return _create_tsv_file


# --- Tests for get_rarefaction_depths ---

class TestGetRarefactionDepths:
    def test_empty_abundance(self):
        assert get_rarefaction_depths(0, 10) == [0]

    def test_single_abundance(self):
        assert get_rarefaction_depths(1, 10) == [1]

    def test_num_points_one(self):
        assert get_rarefaction_depths(100, 1) == [100]

    def test_num_points_two(self):
        assert get_rarefaction_depths(100, 2) == [1, 100]

    def test_num_points_zero_or_negative(self):
        assert get_rarefaction_depths(100, 0) == [100]
        assert get_rarefaction_depths(100, -5) == [100]

    def test_small_abundance_more_points_requested(self):
        # The refined function aims for approximately num_points_requested.
        # If total_abundance < num_points_requested, it should include points from 1 to total_abundance.
        assert get_rarefaction_depths(5, 10) == [1, 2, 3, 4, 5]

    def test_general_structure(self):
        total_abundance = 1000
        num_points = 10
        depths = get_rarefaction_depths(total_abundance, num_points)
        assert 1 in depths
        assert total_abundance in depths
        assert len(depths) <= num_points  # Can be less if generated depths coincide
        assert len(depths) >= 2 if num_points >= 2 and total_abundance > 1 else True
        assert all(depths[i] <= depths[i + 1] for i in range(len(depths) - 1))  # Check sorted
        assert all(0 <= d <= total_abundance for d in depths)

    def test_total_abundance_2_num_points_10(self):
        assert get_rarefaction_depths(2, 10) == [1, 2]

    def test_total_abundance_10_num_points_3(self):
        # Expected: 1, a midpoint, 10
        # num_intermediate_points = 1. num_linear_points = 1.
        # linear_step = (10-1)/(1+1) = 4.5. round(1+4.5) = 6.
        assert get_rarefaction_depths(10, 3) == [1, 6, 10]


# --- Tests for run_rarefaction CLI ---

SIMPLE_HEADER = ["pl7_app_sampleId", "clonotypeKey", "abundance"]
SIMPLE_DATA_ROWS_ONE_SAMPLE = [
    ["S1", "C1", "3"],
    ["S1", "C2", "2"],
    ["S1", "C3", "5"],  # Total S1 abundance = 10, 3 unique clonotypes
]
SIMPLE_DATA_ROWS_TWO_SAMPLES = [
    ["S1", "C1", "3"],
    ["S1", "C2", "2"],  # Total S1 = 5, Unique = 2
    ["S2", "C10", "1"],
    ["S2", "C11", "4"],
    ["S2", "C12", "1"],  # Total S2 = 6, Unique = 3
]


class TestRunRarefactionCLI:
    def test_successful_run_one_sample(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        input_file = create_tsv_file("input_one_sample.tsv", SIMPLE_HEADER, SIMPLE_DATA_ROWS_ONE_SAMPLE)
        output_file = tmp_path / "output_one_sample.tsv"

        # Using low iterations for speed and focusing on structure/determinism where possible
        result = runner.invoke(run_rarefaction, [
            str(input_file), str(output_file),
            "--num-points", "3",
            "--num-iterations", "10"  # Sufficient for deterministic results with simple data
        ])

        assert result.exit_code == 0, result.output
        assert output_file.exists()

        with open(output_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader)
            assert header == ["pl7_app_sampleId", "subsampling_depth", "mean_unique_clonotypes"]

            rows = list(reader)
            # For S1 (total abundance 10), with num-points=3, depths should be [1, 6, 10]
            expected_depths_s1 = get_rarefaction_depths(10, 3)
            assert len(rows) == len(expected_depths_s1)

            s1_rows = [row for row in rows if row[0] == "S1"]
            assert len(s1_rows) == len(expected_depths_s1)

            output_depths_s1 = sorted([int(row[1]) for row in s1_rows])
            assert output_depths_s1 == expected_depths_s1

            for row_data in s1_rows:
                assert row_data[0] == "S1"
                depth = int(row_data[1])
                mean_clonos = float(row_data[2])
                assert 0 <= mean_clonos <= 3  # Max 3 unique clonotypes in S1
                if depth == 1:
                    assert mean_clonos == 1.0
                if depth == 10:  # Total abundance for S1
                    assert mean_clonos == 3.0  # Should always find all 3 unique types

    def test_successful_run_two_samples(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        input_file = create_tsv_file("input_two_samples.tsv", SIMPLE_HEADER, SIMPLE_DATA_ROWS_TWO_SAMPLES)
        output_file = tmp_path / "output_two_samples.tsv"

        result = runner.invoke(run_rarefaction, [
            str(input_file), str(output_file),
            "--num-points", "3",
            "--num-iterations", "20"
        ])
        assert result.exit_code == 0, result.output
        assert output_file.exists()

        s1_total_abundance = 3 + 2  # 5
        s2_total_abundance = 1 + 4 + 1  # 6

        s1_expected_depths = get_rarefaction_depths(s1_total_abundance, 3)  # e.g. [1, 3, 5]
        s2_expected_depths = get_rarefaction_depths(s2_total_abundance, 3)  # e.g. [1, 3, 6] or [1,4,6]

        with open(output_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            s1_rows = [row for row in rows if row["pl7_app_sampleId"] == "S1"]
            s2_rows = [row for row in rows if row["pl7_app_sampleId"] == "S2"]

            assert len(s1_rows) == len(s1_expected_depths)
            assert len(s2_rows) == len(s2_expected_depths)

            s1_output_depths = sorted([int(r['subsampling_depth']) for r in s1_rows])
            s2_output_depths = sorted([int(r['subsampling_depth']) for r in s2_rows])

            assert s1_output_depths == s1_expected_depths
            assert s2_output_depths == s2_expected_depths

            for row in s1_rows:
                mean_clonos = float(row['mean_unique_clonotypes'])
                assert 0 <= mean_clonos <= 2  # Max 2 unique for S1
                if int(row['subsampling_depth']) == s1_total_abundance:
                    assert mean_clonos == 2.0
            for row in s2_rows:
                mean_clonos = float(row['mean_unique_clonotypes'])
                assert 0 <= mean_clonos <= 3  # Max 3 unique for S2
                if int(row['subsampling_depth']) == s2_total_abundance:
                    assert mean_clonos == 3.0

    def test_output_to_stdout(self, create_tsv_file):
        runner = CliRunner()
        input_file = create_tsv_file("input_stdout.tsv", SIMPLE_HEADER, SIMPLE_DATA_ROWS_ONE_SAMPLE)

        result = runner.invoke(run_rarefaction, [
            str(input_file), "-",
            "--num-points", "2",  # Depths 1 and 10 for S1
            "--num-iterations", "1"  # Keep it simple for stdout check
        ])
        assert result.exit_code == 0, result.output
        assert "pl7_app_sampleId\tsubsampling_depth\tmean_unique_clonotypes" in result.stdout
        assert "S1\t1\t1.00" in result.stdout
        assert f"S1\t10\t3.00" in result.stdout  # Total abundance for S1 is 10

    def test_input_file_not_found(self):
        runner = CliRunner()
        result = runner.invoke(run_rarefaction, ["non_existent_file.tsv", "output.tsv"])
        assert result.exit_code != 0
        # Click's default error for missing file path argument
        assert "Invalid value for 'INPUT_TSV_FILEPATH'" in result.output or \
               "Error: Input file not found" in result.output  # Depending on click version / OS

    def test_empty_file_after_header(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        input_file = create_tsv_file("empty_data.tsv", SIMPLE_HEADER, [])
        output_file = tmp_path / "output_empty.tsv"

        result = runner.invoke(run_rarefaction, [str(input_file), str(output_file)])
        assert result.exit_code == 1, result.output
        assert "No valid data found in the input file to process after the header." in result.output
        assert not output_file.exists()

    def test_only_header_in_file(self, tmp_path):
        runner = CliRunner()
        input_file_path = tmp_path / "only_header.tsv"
        with open(input_file_path, 'w') as f:
            f.write(f"{SIMPLE_HEADER[0]}\t{SIMPLE_HEADER[1]}\t{SIMPLE_HEADER[2]}\n")

        output_file = tmp_path / "output_only_header.tsv"
        result = runner.invoke(run_rarefaction, [str(input_file_path), str(output_file)])
        assert result.exit_code == 1, result.output
        assert "No valid data found in the input file to process after the header." in result.output
        assert not output_file.exists()

    def test_malformed_row_less_columns(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        malformed_data = [["S1", "C1"]]  # Missing abundance
        input_file = create_tsv_file("malformed_less.tsv", SIMPLE_HEADER, malformed_data)
        output_file = tmp_path / "output_malformed_less.tsv"

        result = runner.invoke(run_rarefaction, [str(input_file), str(output_file)])
        assert "Warning: Row 1 (after header): Expected at least 3 columns" in result.output
        assert "No valid data found" in result.output
        assert result.exit_code == 1

    def test_malformed_row_bad_abundance(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        malformed_data = [["S1", "C1", "not_a_number"]]
        input_file = create_tsv_file("malformed_abund.tsv", SIMPLE_HEADER, malformed_data)
        output_file = tmp_path / "output_malformed_abund.tsv"

        result = runner.invoke(run_rarefaction, [str(input_file), str(output_file)])
        assert "Warning: Row 1 (after header): Non-integer abundance 'not_a_number'" in result.output
        assert "No valid data found" in result.output
        assert result.exit_code == 1

    def test_negative_abundance_skipped(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        data = [["S1", "C1", "-5"], ["S1", "C2", "10"]]  # C1 should be skipped
        input_file = create_tsv_file("neg_abund.tsv", SIMPLE_HEADER, data)
        output_file = tmp_path / "output_neg_abund.tsv"

        result = runner.invoke(run_rarefaction, [str(input_file), str(output_file), "--num-points", "2"])
        assert result.exit_code == 0, result.output
        assert "Warning: Row 1 (after header): Negative abundance (-5) not allowed" in result.output

        with open(output_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = [row for row in reader if row["pl7_app_sampleId"] == "S1"]
            # Only C2 (abundance 10, 1 unique type) should be processed for S1
            s1_total_abundance = 10
            expected_depths = get_rarefaction_depths(s1_total_abundance, 2)
            assert len(rows) == len(expected_depths)
            for row in rows:
                assert float(row['mean_unique_clonotypes']) == 1.0

    def test_zero_abundance_clonotype_skipped(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        data = [
            ["S1", "C1", "0"],  # Should be skipped by `if abundance > 0`
            ["S1", "C2", "5"]
        ]
        input_file = create_tsv_file("zero_abund.tsv", SIMPLE_HEADER, data)
        output_file = tmp_path / "output_zero_abund.tsv"

        result = runner.invoke(run_rarefaction, [str(input_file), str(output_file), "--num-points", "2"])
        assert result.exit_code == 0, result.output

        with open(output_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = [row for row in reader if row["pl7_app_sampleId"] == "S1"]
            s1_total_abundance = 5
            expected_depths = get_rarefaction_depths(s1_total_abundance, 2)
            assert len(rows) == len(expected_depths)
            for row in rows:
                assert float(row['mean_unique_clonotypes']) == 1.0

    def test_sample_with_no_positive_abundance(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        data = [
            ["S1", "C1", "0"],
            ["S1", "C2", "-2"],  # S1 has no positive abundance clonotypes
            ["S2", "C3", "10"]  # Only S2 has valid data
        ]
        input_file = create_tsv_file("no_pos_abund_s1.tsv", SIMPLE_HEADER, data)
        output_file = tmp_path / "output_no_pos_abund_s1.tsv"

        result = runner.invoke(run_rarefaction, [str(input_file), str(output_file), "--num-points", "2"])
        assert result.exit_code == 0, result.output

        with open(output_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)
            s1_rows = [row for row in rows if row["pl7_app_sampleId"] == "S1"]
            s2_rows = [row for row in rows if row["pl7_app_sampleId"] == "S2"]

            # S1 has total abundance 0. get_rarefaction_depths(0, N) returns [0]
            assert len(s1_rows) == 1
            assert s1_rows[0]['subsampling_depth'] == '0'
            assert float(s1_rows[0]['mean_unique_clonotypes']) == 0.0

            s2_total_abundance = 10
            expected_s2_depths = get_rarefaction_depths(s2_total_abundance, 2)
            assert len(s2_rows) == len(expected_s2_depths)
            for row in s2_rows:
                assert float(row['mean_unique_clonotypes']) == 1.0

    def test_bad_header_format_warning(self, create_tsv_file, tmp_path):
        runner = CliRunner()
        bad_header = ["sampleID", "clonotype_ID", "count_val", "extra_col"]
        input_file = create_tsv_file("bad_header.tsv", bad_header, SIMPLE_DATA_ROWS_ONE_SAMPLE)
        output_file = tmp_path / "output_bad_header.tsv"

        result = runner.invoke(run_rarefaction, [str(input_file), str(output_file), "--num-points", "2"])
        assert result.exit_code == 0, result.output
        assert "Warning: Input file header" in result.output
        assert "does not look as expected" in result.output
        assert output_file.exists()

        with open(output_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)
            s1_total_abundance = 10
            expected_depths = get_rarefaction_depths(s1_total_abundance, 2)
            assert len(rows) == len(expected_depths)
            assert rows[0]['pl7_app_sampleId'] == "S1"  # Check data was processed correctly despite warning

    @pytest.mark.large_data
    def test_with_provided_test_tsv(self, tmp_path):
        runner = CliRunner()

        # Assuming test_main.py is in software/src_python/tests/
        # and test.tsv is in software/src_python/
        original_test_tsv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test.tsv'))

        if not os.path.exists(original_test_tsv_path):
            pytest.skip(f"Original test.tsv not found at {original_test_tsv_path}, skipping large data test.")

        temp_input_file = tmp_path / "temp_test_input.tsv"
        with open(original_test_tsv_path, 'r') as infile, open(temp_input_file, 'w') as outfile:
            outfile.write(infile.read())

        output_file = tmp_path / "output_large.tsv"

        result = runner.invoke(run_rarefaction, [
            str(temp_input_file),
            str(output_file),
            "--num-points", "5",
            "--num-iterations", "10"  # Low iterations for test speed
        ])

        assert result.exit_code == 0, result.output
        assert output_file.exists()

        with open(output_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader)
            assert header == ["pl7_app_sampleId", "subsampling_depth", "mean_unique_clonotypes"]

            data_rows = list(reader)
            assert len(data_rows) > 0

            expected_sample_ids_from_test_tsv = {
                "FON7HNZNV5UGBHIQIMV3W25X", "IHTLHJJJMIM3FZ3STPUEMVRO",
                "KL72Z6CBSMXEUNLJNGWZWX5V", "SJYJRXSE5WBA46GFAUCE7FJ4",
                "TNHLTI5U7BFHYPJKM3CRRX3G", "YRJVMLSSYB4UKBYZGDYBYQHZ"
            }
            output_sample_ids = set(row[0] for row in data_rows)
            assert expected_sample_ids_from_test_tsv.issubset(output_sample_ids)

            for sample_id in expected_sample_ids_from_test_tsv:
                if sample_id in output_sample_ids:
                    sample_specific_rows = [r for r in data_rows if r[0] == sample_id]
                    # Number of points can be less than num_points if total_abundance is small
                    assert 1 <= len(sample_specific_rows) <= 5  # --num-points is 5
                    for row in sample_specific_rows:
                        assert len(row) == 3
                        assert int(row[1]) >= 0
                        assert float(row[2]) >= 0.0
