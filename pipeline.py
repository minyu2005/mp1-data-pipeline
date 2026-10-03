
"""
Data Processing Pipeline - MP1 Part 2

DS 3500

Usage:
    python pipeline.py --input fixtures/sample.csv --output clean.csv
"""

import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
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
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format"
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
    """Main pipeline function."""

    args = parse_arguments()

    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, output=%s, format=%s",
        args.input,
        args.output,
        args.format
    )

    if not validate_input(args.input):
        sys.exit(1)

    try:
        data = load_data(args.input)

    except ValueError as e:
        logger.error("Failed to load data: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
