import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw raisin dataset.
    """
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None")
    if df.type != pd.DataFrame:
        raise TypeError("Input is not a pandas DataFrame")
    df = df.drop_duplicates()
    df = df.dropna()

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df = df.copy()
    df["Area"] = df["Area"].astype(float)
    df["ConvexArea"] = df["ConvexArea"].astype(float)
    df["Class"] = df["Class"].astype(str)

    return df


def scale_features(train_df, test_df, target_col="Class"):
    """
    Scale all features except the target column.
    """
    if train_df is None or test_df is None:
        raise ValueError("Input DataFrames cannot be None")
    if train_df.empty or test_df.empty:
        raise ValueError("Input DataFrames cannot be empty")
    if target_col not in train_df.columns or target_col not in test_df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrames")
    scaler = StandardScaler()

    features = train_df.columns.drop(target_col)

    train_scaled = train_df.copy()
    test_scaled = test_df.copy()

    train_scaled[features] = scaler.fit_transform(train_df[features])
    test_scaled[features] = scaler.transform(test_df[features])

    return train_scaled, test_scaled
