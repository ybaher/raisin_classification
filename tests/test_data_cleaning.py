import pandas as pd
from src.data_cleaning import clean_data, split_data, scale_features


def test_clean_data():
    raw = pd.DataFrame({
        "Unnamed: 0": [0, 1],
        "Area": ["1.0", "2.0"],
        "ConvexArea": ["3.0", "4.0"],
        "Class": [1, 0]
    })

    cleaned = clean_data(raw)

    # Check if unnamed column are removed
    assert "Unnamed: 0" not in cleaned.columns

    # Check if types are converted
    assert cleaned["Area"].dtype == float
    assert cleaned["ConvexArea"].dtype == float
    assert cleaned["Class"].dtype == object

    # Check if the shape is preserved after cleaning (no NaNs)
    assert cleaned.shape[0] == 2


def test_split_data():
    df = pd.DataFrame({
        "Area": [1, 2, 3, 4, 5],
        "ConvexArea": [10, 11, 12, 13, 14],
        "Class": ["A", "A", "B", "A", "B"]
    })

    train, test = split_data(df, test_size=0.2)

    assert len(train) == 4
    assert len(test) == 1


def test_scale_features():
    train = pd.DataFrame({
        "Area": [1.0, 2.0],
        "ConvexArea": [3.0, 4.0],
        "Class": ["A", "B"]
    })

    test = pd.DataFrame({
        "Area": [5.0],
        "ConvexArea": [6.0],
        "Class": ["A"]
    })

    train_scaled, test_scaled = scale_features(train, test)

    # Check that means of scaled train features should be approx 0
    assert abs(train_scaled["Area"].mean()) < 1e-6
    assert abs(train_scaled["ConvexArea"].mean()) < 1e-6

    # Check that class column is not scaled
    assert train_scaled["Class"].dtype == object
