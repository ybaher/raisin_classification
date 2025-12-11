import pandera.pandas as pa
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

def validate_data_types(df: pd.DataFrame) -> bool:
    schema = pa.DataFrameSchema({
        "Area": pa.Column(float),
        "MajorAxisLength": pa.Column(float),
        "MinorAxisLength": pa.Column(float),
        "Eccentricity": pa.Column(float),
        "ConvexArea": pa.Column(float),
        "Extent": pa.Column(float),
        "Perimeter": pa.Column(float),
        "Class": pa.Column(str)
    })
    try:
        schema.validate(df)
        return True
    except pa.errors.SchemaError:
        return False

def check_nan(series: pd.Series) -> bool:
    """Check if series has no NaN values"""
    return ~series.isna().any()
    
def validate_missing_values(df: pd.DataFrame) -> bool:
    schema = pa.DataFrameSchema({
        "Area": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "MajorAxisLength": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "MinorAxisLength": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "Eccentricity": pa.Column(float, nullable=True),
        "ConvexArea": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "Extent": pa.Column(float, nullable=True),
        "Perimeter": pa.Column(float, pa.Check(check_nan, element_wise=False), nullable=True),
        "Class": pa.Column(str, pa.Check.isin(["Kecimen", "Besni"]))
    })
    try:
        schema.validate(df)
        return True
    except pa.errors.SchemaError:
        return False
    
    
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
