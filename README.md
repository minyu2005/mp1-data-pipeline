# MP1 Data Pipeline.
This is my DS 3500 command-line data pipeline. You give it a data file and a YAML config, and it validates the data, cleans it based on the rules in the config, and saves the result as a CSV.

## How it works
- `src/data_loaders.py`: loads CSV, JSON, and YAML files
- `src/data_validator.py`: checks that the required columns exist and the numeric values make sense
- `src/data_processor.py`: drops duplicate rows, handles missing values, and removes outliers using IQR or Z-score
- `src/data_output.py`: saves the cleaned DataFrame
- `src/utils.py`: contains shared logging and file-validation helpers
- `pipeline.py`: ties everything together into one end-to-end run

Everything is controlled from `config/config.yaml`, so the validation and processing settings can be changed without changing the Python code.

## Example
```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose