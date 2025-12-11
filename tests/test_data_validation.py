"""
Test cases for data validation functions in sc3_data_validation.py. Most of these functions make dummy dataframes to test various validation scenarios.

Usage: pytest test_data_validation.py
"""

import os
import sys
import pandas as pd
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the validation functions
from src.data_validation import (
    validate_file_format,
    validate_columns,
    validate_data_types,
    validate_missing_values,
    validate_duplicates,
    validate_high_correlation,
    validate_target_correlation,
    EXPECTED_COLS
)

# Sample csv file for integration tests
DATA_FILE = "data/processed/raisin_cleaned_train.csv"

def test_validate_file_format_csv():
    assert validate_file_format("some/path/file.csv")
    assert validate_file_format("FILE.CSV") 
    assert not validate_file_format("file.txt")
    assert not validate_file_format("file.xlsx")
    assert not validate_file_format("file.json")
    assert not validate_file_format("file")
    assert not validate_file_format(".csvfile")
    assert not validate_file_format("file.csv.backup")

def test_validate_columns_exact():
    df = pd.DataFrame(columns=EXPECTED_COLS)
    assert validate_columns(df)
    df_wrong = pd.DataFrame(columns=["A", "B", "C"])
    assert not validate_columns(df_wrong)

def test_validate_data_types_correct():
    df = pd.DataFrame({col: [0.1] for col in EXPECTED_COLS[:-1]})
    df["Class"] = ["Kecimen"]
    assert validate_data_types(df)
    df["Area"] = ["not_a_float"]
    assert not validate_data_types(df)

def test_validate_missing_values():
    # change size to control missing value proportion. We have set the threshold at 5% 
    size = 20 
    df = pd.DataFrame({col: [0.1]*(size-1) + [None] for col in EXPECTED_COLS[:-1]})
    df["Class"] = ["Kecimen"] * (size//2) + ["Besni"] * (size//2)
    assert validate_missing_values(df)

def test_validate_duplicates():
    row = {col: 0.123 for col in EXPECTED_COLS[:-1]}
    row["Class"] = "Kecimen"
    df = pd.DataFrame([row, row])  # duplicate rows
    assert not validate_duplicates(df)
    df = pd.DataFrame([row, {**row, "Area": 0.456}])  # no duplicates
    assert validate_duplicates(df)

def test_validate_high_correlation():
    # Create a df where feature_1 and feature_2 are highly correlated
    df = pd.DataFrame({
        "Area": [1.0, 2.0, 3.0],
        "MajorAxisLength": [1.0, 2.0, 3.0],
        "MinorAxisLength": [3.0, 2.0, 1.0],
        "Eccentricity": [0.5, 0.3, 0.1],
        "ConvexArea": [5, 6, 7],
        "Extent": [0.5, 0.6, 0.7],
        "Perimeter": [10, 10, 10],
        "Class": ["Kecimen", "Kecimen", "Besni"]
    })
    result = validate_high_correlation(df)
    assert "MajorAxisLength" in result or "Area" in result

def test_validate_target_correlation():
    # Class column strongly correlates with Area
    df = pd.DataFrame({
        "Area": [1.0, 2.0, 3.0, 4.0],
        "MajorAxisLength": [2.1, 2.2, 2.3, 2.4],
        "MinorAxisLength": [3.1, 3.2, 3.3, 3.4],
        "Eccentricity": [0.5, 0.3, 0.1, 0.2],
        "ConvexArea": [5, 6, 7, 8],
        "Extent": [0.5, 0.6, 0.7, 0.8],
        "Perimeter": [10, 10.5, 11, 11.5],
        "Class": ["Kecimen", "Kecimen", "Besni", "Besni"]
    })
    result = validate_target_correlation(df)
    assert "Area" in result

@pytest.mark.skipif(not os.path.exists(DATA_FILE), reason="train_df.csv not found")
def test_all_on_real_file():
    df = pd.read_csv(DATA_FILE)
    assert validate_columns(df)
    assert validate_data_types(df)
    assert validate_missing_values(df)
    assert validate_duplicates(df)
    validate_high_correlation(df)
    validate_target_correlation(df)
