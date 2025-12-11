"""
Cleans and processes raw data and outputs train/test CSV files.

Usage:
    python s2_data_cleanning.py <input_path> <output_path>
"""

import sys
import os
import click
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_cleaning import clean_data, split_data, scale_features


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def main(input_path, output_path):
    # 1. Read data
    df = pd.read_csv(input_path)

    # 2. Clean data
    df = clean_data(df)

    # 3. Split data
    train, test = split_data(df)

    # 4. Scale features
    train_scaled, test_scaled = scale_features(train, test)

    # 5. Save outputs
    train_scaled.to_csv(output_path.replace(".csv", "_train.csv"), index=False)
    test_scaled.to_csv(output_path.replace(".csv", "_test.csv"), index=False)

    click.echo("Processed train and test files saved.")


if __name__ == "__main__":
    main()
