
"""
Data Processing Pipeline - MP1 Part 3

DS 3500

Usage:
    python pipeline.py --input fixtures/sample.csv --output cleaned_data.csv --config config.yaml --verbose
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from data_loaders import load_data
from data_processor import (
    process_data,
    create_cleaning_report
)


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Command-line data processing pipeline"
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input file"
    )

    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to the output file"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the YAML configuration file"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""

    if Path(filepath).is_file():
        logger.info("Input file validated: %s", filepath)
        return True

    logger.error("Input file not found: %s", filepath)
    return False


def main():
    """Main pipeline workflow."""

    # 1. Parse arguments
    args = parse_arguments()

    # 2. Set up logging
    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, output=%s, config=%s",
        args.input,
        args.output,
        args.config
    )

    # 3. Validate input and config files
    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    # 4. Load data and configuration
    try:
        data = load_data(args.input)
        config = load_data(args.config)

    except ValueError as e:
        logger.error("Loading failed: %s", e)
        sys.exit(1)

    # 5. Check that the input is tabular data
    if not isinstance(data, pd.DataFrame):
        logger.error("Input data must be a CSV DataFrame")
        sys.exit(1)

    # 6. Keep a copy of the original data
    original_data = data.copy()

    # 7. Process data
    try:
        cleaned_data = process_data(data, config)

    except ValueError as e:
        logger.error("Processing failed: %s", e)
        sys.exit(1)

    # 8. Generate cleaning report
    report = create_cleaning_report(
        original_data,
        cleaned_data
    )

    print(report)

    # 9. Log the processing results
    logger.info(
        "Processing complete: %d -> %d rows",
        len(original_data),
        len(cleaned_data)
    )

    # 10. Save cleaned data
    cleaned_data.to_csv(
        args.output,
        index=False
    )

    logger.info(
        "Saved cleaned data to %s",
        args.output
    )


if __name__ == "__main__":
    main()
