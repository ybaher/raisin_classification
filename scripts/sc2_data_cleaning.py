"""
Cleans and processes raw data and outputs clean data

Usage:
    python s2_data_cleanning.py <input_path> <output_path>
"""

import click
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def main(input_path, output_path):
    """
    Reads raw data, cleans it, transforms it, splits it,
    and writes processed train/test sets.
    """

    # -----------------------------
    # 1. READ RAW DATA
    # -----------------------------
    df = pd.read_csv(input_path)

    # -----------------------------
    # 2. CLEAN DATA
    # -----------------------------
    df = df.drop_duplicates()
    df = df.dropna()
    df = df.drop(columns=["Unnamed: 0"])
    df["Area"] = df["Area"].astype(float)
    df["ConvexArea"] = df["ConvexArea"].astype(float)
    df["Class"] = df["Class"].astype(str)

    # -----------------------------
    # 3. SPLIT DATA
    # -----------------------------
    train, test = train_test_split(df, test_size=0.2, random_state=123)

    # -----------------------------
    # 4. SCALE FEATURES
    # -----------------------------
    scaler = StandardScaler()
    features = df.columns.drop("Class")

    train[features] = scaler.fit_transform(train[features])

    test[features] = scaler.transform(test[features])

    # -----------------------------
    # 5. SAVE OUTPUT FILES
    # -----------------------------
    train.to_csv(output_path.replace(".csv", "_train.csv"), index=False)
    test.to_csv(output_path.replace(".csv", "_test.csv"), index=False)

    click.echo("Processed train and test files saved.")


if __name__ == "__main__":
    main()
