"""
Validates data used for subsequent scripts

Usage:
    python 03_data_validation.py <input_path>
"""

import pandera as pa
import pandas as pd
import numpy as np
import click 

@click.command()
@click. argument('input_path', type=click.Path(exists=True))
def main(input_path: str) -> None:
    """Validate raisin dataset from INPUT_PATH."""
    
    # Validate file format
    if input_path.lower().endswith(".csv"):
        print("Correct file format")
    else:
        print("Incorrect file format")
        return
    
    # Read the CSV file
    df = pd.read_csv(input_path)
    
    # Validate columns
    expected_cols = [
        "Area", "MajorAxisLength", "MinorAxisLength", 
        "Eccentricity", "ConvexArea", "Extent", "Perimeter", "Class"
    ]
    if set(df.columns) == set(expected_cols):
        print("Column names are correct")
    else:
        print("Column names incorrect")
        print("Expected:", expected_cols)
        print("Found:", list(df.columns))
    
    # Validate data types
    schema = pa.DataFrameSchema({
        "Area": pa.Column(float),
        "MajorAxisLength": pa. Column(float),
        "MinorAxisLength": pa.Column(float),
        "Eccentricity": pa.Column(float),
        "ConvexArea": pa.Column(float),
        "Extent": pa.Column(float), 
        "Perimeter": pa.Column(float),
        "Class": pa. Column(str)
    })
    try:
        schema.validate(df)
        print("✓ Data types are correct")
    except pa.errors.SchemaError as e:
        print("✗ Data types are incorrect")
        print(e)
    
    # Validate no missing values (with threshold)
    raisin_schema = pa.DataFrameSchema({
        "Area": pa.Column(
            float,
            pa.Check(
                lambda s: s.isna().mean() <= 0.05,
                element_wise=False,
                error="Too many null values in 'Area' column."),
            nullable=True),
        "MajorAxisLength": pa.Column(
            float,
            pa. Check(
                lambda s: s.isna().mean() <= 0.05,
                element_wise=False,
                error="Too many null values in 'MajorAxisLength' column."),
            nullable=True),
        "MinorAxisLength": pa. Column(
            float,
            pa.Check(
                lambda s: s.isna().mean() <= 0.05,
                element_wise=False,
                error="Too many null values in 'MinorAxisLength' column. "),
            nullable=True),
        "Eccentricity": pa.Column(float, nullable=True),
        "ConvexArea": pa.Column(
            float,
            pa.Check(
                lambda s: s.isna().mean() <= 0.05,
                element_wise=False,
                error="Too many null values in 'ConvexArea' column."),
            nullable=True),
        "Extent": pa.Column(float, nullable=True),
        "Perimeter": pa.Column(
            float,
            pa.Check(
                lambda s: s.isna().mean() <= 0.05,
                element_wise=False,
                error="Too many null values in 'Perimeter' column."),
            nullable=True),
        "Class": pa.Column(
            str,
            pa.Check.isin(["Kecimen", "Besni"]))
    })
    try:
        raisin_schema.validate(df)
        print("✓ Missing values within acceptable threshold")
    except pa.errors. SchemaError as e:
        print("✗ Missing values validation failed")
        print(e)
    
    # Validate no duplicates
    duplicate_schema = pa.DataFrameSchema(
        columns={
            "Area": pa.Column(pa.Int, nullable=False),
            "Perimeter": pa.Column(pa.Float, nullable=False),
            "MajorAxisLength": pa.Column(pa.Float, nullable=False),
            "MinorAxisLength": pa.Column(pa.Float, nullable=False),
            "Eccentricity": pa.Column(pa. Float, nullable=False),
            "ConvexArea": pa. Column(pa.Int, nullable=False),
        }, 
        checks=[
            pa. Check(lambda df: not df. duplicated().any(), 
                    error="Duplicate rows found in the dataset.")
        ]
    )
    try:
        duplicate_schema.validate(df)
        print("No duplicate rows found")
    except pa. errors.SchemaError as e:
        print("Duplicate validation failed")
        print(e)
    
    # Validate data ranges
    range_schema = pa.DataFrameSchema(
        columns={
            'Area': pa.Column(pa.Int, pa.Check.in_range(25380, 235050), nullable=False),
            'Eccentricity': pa.Column(pa.Float, pa.Check.in_range(0.348, 0.9622), nullable=False),
            'Extent': pa.Column(pa.Float, pa.Check.in_range(0.379, 0.836), nullable=False),
            'MajorAxisLength': pa.Column(pa.Float, pa.Check.in_range(223.0, 1000), nullable=False),
            'MinorAxisLength': pa.Column(pa.Float, pa.Check.in_range(140, 495), nullable=False),
            'Perimeter': pa.Column(pa.Float, pa.Check.in_range(619, 2698), nullable=False),
            'ConvexArea': pa.Column(pa.Int, pa.Check.in_range(26138, 278218), nullable=False)
        }
    )
    try:
        range_schema. validate(df)
        print("Data ranges are valid")
    except pa.errors.SchemaError as e:
        print("Data ranges are invalid")
        print(e)
    
    # Validate high correlations between features
    corr_matrix = df. select_dtypes(include=[np.number]).corr().abs()
    upper_tri = corr_matrix.where(np. triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.9)]
    if to_drop:
        print(f"Recommend dropping highly correlated features: {to_drop}")
    else:
        print("No highly correlated features found")
    
    # Validate high target correlation
    df_encoded = df.copy()
    df_encoded['Class'] = df_encoded['Class'].astype('category').cat. codes
    corr_with_target = df_encoded.corr()['Class'].abs()
    high_corr_features = corr_with_target[corr_with_target > 0.5].index.tolist()
    if 'Class' in high_corr_features:
        high_corr_features.remove('Class')
    if high_corr_features:
        print(f"Features highly correlated with target 'Class': {high_corr_features}")
    else:
        print("No features highly correlated with target")
    
    print("\nValidation complete!")

if __name__ == "__main__":
    main()