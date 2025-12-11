"""
Validates data used for subsequent scripts.

Usage:
    python s3_data_validation.py <input_path>
"""
import sys
import os
import pandas as pd
import click
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_validation import validate_file_format, validate_columns, validate_data_types, validate_missing_values, validate_duplicates, validate_high_correlation, validate_target_correlation

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
def main(input_path: str) -> None:
    click.echo("Starting data validation...")
    #1. Validate file format
    if not validate_file_format(input_path):
        click.echo(f"Error: The file {input_path} is not in CSV format.")
        return
    else:
        click.echo("File format validation passed.")
    
    #2. Validate columns
    if not validate_columns(pd.read_csv(input_path, nrows=0)):
        click.echo("Error: The dataset does not have the expected columns.")
        return
    else:
        click.echo("Column validation passed.")
        
    #3. Validate data types
    if not validate_data_types(pd.read_csv(input_path)):
        click.echo("Error: The dataset has incorrect data types.")
        return
    else:
        click.echo("Data type validation passed.")
    
    #4. Validate missing values
    if not validate_missing_values(pd.read_csv(input_path)):
        click.echo("Error: The dataset has too many missing values.")
        return
    else:
        click.echo("Missing value validation passed.")
    #5. Validate duplicates
    if not validate_duplicates(pd.read_csv(input_path)):
        click.echo("Error: The dataset contains duplicate rows.")
        return
    else:
        click.echo("Duplicate row validation passed.")
    
    #6. Validate high correlation
    print(f"High correlation features: {validate_high_correlation(pd.read_csv(input_path))}")

    #7. Validate target correlation
    print(f"Target correlation features: {validate_target_correlation(pd.read_csv(input_path))}")
    
if __name__ == "__main__":
    main()