"""
Validates data used for subsequent scripts.

Usage:
    python s3_data_validation.py <input_path>
"""

import pandera as pa
import pandas as pd
import numpy as np
import click

EXPECTED_COLS = [
    "Area", "MajorAxisLength", "MinorAxisLength",
    "Eccentricity", "ConvexArea", "Extent", "Perimeter", "Class"
]

def validate_file_format(input_path: str) -> bool:
    """Check if the file format is .csv"""
    return input_path.lower().endswith(".csv")

def validate_columns(df: pd.DataFrame) -> bool:
    """Check if columns exactly match the expected columns."""
    return set(df.columns) == set(EXPECTED_COLS)

def get_type_schema() -> pa.DataFrameSchema:
    """Returns the pandera schema for data types."""
    return pa.DataFrameSchema({
        "Area": pa.Column(float),
        "MajorAxisLength": pa.Column(float),
        "MinorAxisLength": pa.Column(float),
        "Eccentricity": pa.Column(float),
        "ConvexArea": pa.Column(float),
        "Extent": pa.Column(float),
        "Perimeter": pa.Column(float),
        "Class": pa.Column(str)
    })

def validate_data_types(df: pd.DataFrame) -> bool:
    schema = get_type_schema()
    try:
        schema.validate(df)
        return True
    except pa.errors.SchemaError:
        return False

def get_missing_schema() -> pa.DataFrameSchema:
    """Returns the pandera schema for missing values (with threshold)."""
    check_nan = lambda s: s.isna().mean() <= 0.05
    return pa.DataFrameSchema({
        "Area": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "MajorAxisLength": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "MinorAxisLength": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "Eccentricity": pa.Column(float, nullable=True),
        "ConvexArea": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "Extent": pa.Column(float, nullable=True),
        "Perimeter": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "Class": pa.Column(str, pa.Check.isin(["Kecimen", "Besni"]))
    })

def validate_missing_values(df: pd.DataFrame) -> bool:
    schema = get_missing_schema()
    try:
        schema.validate(df)
        return True
    except pa.errors.SchemaError:
        return False

def get_duplicate_schema() -> pa.DataFrameSchema:
    return pa.DataFrameSchema(
        columns={
            "Area": pa.Column(int, nullable=False),
            "Perimeter": pa.Column(float, nullable=False),
            "MajorAxisLength": pa.Column(float, nullable=False),
            "MinorAxisLength": pa.Column(float, nullable=False),
            "Eccentricity": pa.Column(float, nullable=False),
            "ConvexArea": pa.Column(int, nullable=False)
        },
        checks=[
            pa.Check(lambda df: not df.duplicated().any(), error="Duplicate rows found in the dataset.")
        ]
    )

def validate_duplicates(df: pd.DataFrame) -> bool:
    # Validate no duplicates
    duplicate_schema = pa.DataFrameSchema(
        columns={
            "Area": pa.Column(pa.Float, nullable=False),
            "Perimeter": pa.Column(pa.Float, nullable=False),
            "MajorAxisLength": pa.Column(pa.Float, nullable=False),
            "MinorAxisLength": pa.Column(pa.Float, nullable=False),
            "Eccentricity": pa.Column(pa. Float, nullable=False),
            "ConvexArea": pa. Column(pa.Float, nullable=False),
        }, 
        checks=[
            pa. Check(lambda df: not df. duplicated().any(), 
                    error="Duplicate rows found in the dataset.")
        ]
    )
    try:
        duplicate_schema.validate(df)
        return True
    except pa. errors.SchemaError:
        return False

def validate_high_correlation(df: pd.DataFrame) -> list:
    """Identify features correlated >0.9 with other features."""
    corr_matrix = df.select_dtypes(include=[np.number]).corr().abs()
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.9)]
    return to_drop

def validate_target_correlation(df: pd.DataFrame) -> list:
    """Return features highly correlated (>0.5) with 'Class'."""
    df_encoded = df.copy()
    df_encoded['Class'] = df_encoded['Class'].astype('category').cat.codes
    corr_with_target = df_encoded.corr()['Class'].abs()
    high_corr_features = corr_with_target[corr_with_target > 0.5].index.tolist()
    if 'Class' in high_corr_features:
        high_corr_features.remove('Class')
    return high_corr_features

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
def main(input_path: str) -> None:
    """Validate raisin dataset from INPUT_PATH."""

    # Validate file format
    if validate_file_format(input_path):
        print("Correct file format")
    else:
        print("Incorrect file format")
        return

    # Read the CSV file
    df = pd.read_csv(input_path)

    # Validate columns
    if validate_columns(df):
        print("Column names are correct")
    else:
        print("Column names incorrect")
        print("Expected:", EXPECTED_COLS)
        print("Found:", list(df.columns))

    # Validate data types
    if validate_data_types(df):
        print("Data types are correct")
    else:
        print("Data types are incorrect")

    # Validate missing values (threshold)
    if validate_missing_values(df):
        print("Missing values within acceptable threshold")
    else:
        print("Missing values validation failed")

    # Validate duplicates
    if validate_duplicates(df):
        print("No duplicate rows found")
    else:
        print("Duplicate validation failed")

    # Validate high correlations between features
    high_corr_features = validate_high_correlation(df)
    if high_corr_features:
        print(f"Recommend dropping highly correlated features: {high_corr_features}")
    else:
        print("No highly correlated features found")

    # Validate high target correlation
    high_target_corr_features = validate_target_correlation(df)
    if high_target_corr_features:
        print(f"Features highly correlated with target 'Class': {high_target_corr_features}")
    else:
        print("No features highly correlated with target")

    print("\nValidation complete!")

if __name__ == "__main__":
    main()