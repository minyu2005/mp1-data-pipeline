"""
DS 3500 - MP1
Complete command-line data processing pipeline.

Example:
    python pipeline.py \
        --input fixtures/sample_data.csv \
        --output output/clean.csv \
        --config config/config.yaml \
        --verbose
"""

import argparse
import logging
import sys

import pandas as pd

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Command-line data processing pipeline"
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input CSV file"
    )

    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to the output CSV file"
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


def main():
    """Run the complete data-processing pipeline."""

    args = parse_arguments()

    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, output=%s, config=%s",
        args.input,
        args.output,
        args.config
    )

    # Validate paths
    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    # Load data and config
    try:
        data = load_data(args.input)
        config = load_data(args.config)

    except ValueError as error:
        logger.error("Loading failed: %s", error)
        sys.exit(1)

    if not isinstance(data, pd.DataFrame):
        logger.error("Input data must be a CSV DataFrame")
        sys.exit(1)

    # Validation settings
    validation_config = config["validation"]

    required_columns = validation_config["required_columns"]
    numeric_columns = validation_config["numeric_columns"]

    # Validate DataFrame
    rows_before_validation = len(data)

    try:
        validated_data = validate_dataframe(
            data,
            required_columns,
            numeric_columns
        )

    except ValueError as error:
        logger.error("Validation failed: %s", error)
        sys.exit(1)

    logger.info(
        "Validation complete: %d -> %d rows",
        rows_before_validation,
        len(validated_data)
    )

    # Keep copy before cleaning
    original_data = validated_data.copy()

    # Process data
    try:
        cleaned_data = process_data(
            validated_data,
            config
        )

    except ValueError as error:
        logger.error("Processing failed: %s", error)
        sys.exit(1)

    logger.info(
        "Processing complete: %d -> %d rows",
        len(original_data),
        len(cleaned_data)
    )

    # Create report
    report = create_cleaning_report(
        original_data,
        cleaned_data
    )

    # Save output
    output_path = save_data(
        cleaned_data,
        args.output
    )

    logger.info(
        "Saved cleaned data to %s",
        output_path
    )

    print("\nCleaning report:")
    print(report)


if __name__ == "__main__":
    main()