"""
Test cases for data visualization functions in sc4_data_visualization.py
"""

import os
import sys
import pandas as pd
import pytest
import altair as alt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_visualization import (
    create_scatter_plot,
    create_correlation_heatmap,
    create_class_distribution
)

from scripts.sc4_data_visualization import main

DATA_FILE = "data/processed/raisin_cleaned_train.csv"

TEST_DF = pd.DataFrame({
    "Area": [1.0, 2.0, 3.0],
    "MajorAxisLength": [1.5, 2.5, 3.5],
    "MinorAxisLength": [0.5, 1.5, 2.5],
    "Eccentricity": [0.1, 0.2, 0.3],
    "ConvexArea": [1.1, 2.1, 3.1],
    "Extent": [0.8, 0.9, 1.0],
    "Perimeter": [4.0, 5.0, 6.0],
    "Class": ["A", "B", "A"]
})

def test_create_scatter_plot_type():
    chart = create_scatter_plot(TEST_DF, 'MajorAxisLength', 'MinorAxisLength', 'Class')
    assert isinstance(chart, alt.Chart)

def test_create_correlation_heatmap_type():
    chart = create_correlation_heatmap(TEST_DF)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))

def test_create_class_distribution_type():
    chart = create_class_distribution(TEST_DF, 'Class')
    assert isinstance(chart, alt.Chart)

def test_invalid_input_scatter():
    with pytest.raises(TypeError):
        create_scatter_plot(None, 'MajorAxisLength', 'MinorAxisLength', 'Class')

def test_missing_column_scatter():
    with pytest.raises(KeyError):
        create_scatter_plot(TEST_DF.drop(columns=['MajorAxisLength']), 'MajorAxisLength', 'MinorAxisLength', 'Class')

def test_missing_column_distribution():
    with pytest.raises(KeyError):
        create_class_distribution(TEST_DF.drop(columns=['Class']), 'Class')

def test_non_numeric_scatter():
    df = TEST_DF.copy()
    df['MajorAxisLength'] = ['a', 'b', 'c']
    with pytest.raises(TypeError):
        create_scatter_plot(df, 'MajorAxisLength', 'MinorAxisLength', 'Class')

@pytest.mark.skipif(not os.path.exists(DATA_FILE), reason="train CSV file not found")
def test_all_on_real_file():
    df = pd.read_csv(DATA_FILE)
    chart1 = create_scatter_plot(df, 'MajorAxisLength', 'MinorAxisLength', 'Class')
    chart2 = create_correlation_heatmap(df)
    chart3 = create_class_distribution(df, 'Class')
    assert isinstance(chart1, alt.Chart)
    assert isinstance(chart2, alt.Chart)
    assert isinstance(chart3, alt.Chart)
