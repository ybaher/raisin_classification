"""
Fit a logistic regression model and generate model evaluation artifacts.

Usage:
    python 04_model_fitting.py <train_data_path> <test_data_path> <output_prefix>
"""

import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn. metrics import ConfusionMatrixDisplay, classification_report, accuracy_score
import pickle


def fit_model(X_train, y_train):
    """Fit a logistic regression model."""
    y_train = np.array(y_train)
    clf = LogisticRegression(max_iter=2000, random_state=123)
    clf.fit(X_train, y_train)
    return clf


def save_confusion_matrix(clf, X_test, y_test, output_prefix):
    """Generate and save confusion matrix visualization."""
    y_test = np.array(y_test)
    
    cm_display = ConfusionMatrixDisplay.from_estimator(
        clf, X_test, y_test, cmap='Blues'
    )
    
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_confusion_matrix.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Confusion matrix saved to {output_prefix}_confusion_matrix.png")


def save_classification_report(clf, X_test, y_test, output_prefix):
    """Generate and save classification metrics table."""
    y_test = np.array(y_test)
    y_pred = clf.predict(X_test)
    
    # Get classification report as dictionary
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    
    # Save as CSV
    report_df.to_csv(f"{output_prefix}_classification_report.csv")
    
    # Also save accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    with open(f"{output_prefix}_model_summary.txt", 'w') as f:
        f.write(f"Model: Logistic Regression\n")
        f.write(f"Accuracy: {accuracy:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(classification_report(y_test, y_pred))
    
    print(f"Classification report saved to {output_prefix}_classification_report.csv")
    print(f"Model summary saved to {output_prefix}_model_summary.txt")
    print(f"  Accuracy: {accuracy:.4f}")


def save_feature_importance(clf, feature_names, output_prefix):
    """Generate and save feature importance plot (coefficients)."""
    
    # Get coefficients (for binary classification)
    if clf.coef_. shape[0] == 1:
        coefficients = clf. coef_[0]
    else:
        # For multiclass, use the average absolute coefficient
        coefficients = np. mean(np.abs(clf.coef_), axis=0)
    
    # Create DataFrame
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'coefficient': coefficients
    }). sort_values('coefficient', key=abs, ascending=False)
    
    # Save as CSV
    importance_df.to_csv(f"{output_prefix}_feature_importance.csv", index=False)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    top_features = importance_df.head(15)
    plt.barh(top_features['feature'], top_features['coefficient'])
    plt.xlabel('Coefficient Value')
    plt.title('Top 15 Feature Importances (Logistic Regression Coefficients)')
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_feature_importance.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Feature importance saved to {output_prefix}_feature_importance.[csv|png]")


@click.command()
@click. argument("train_data_path", type=click.Path(exists=True))
@click.argument("test_data_path", type=click.Path(exists=True))
@click.argument("output_prefix", type=str)
def main(train_data_path, test_data_path, output_prefix):
    """
    Train a logistic regression model and generate evaluation artifacts.
    
    TRAIN_DATA_PATH: Path to the training data CSV
    TEST_DATA_PATH: Path to the test data CSV
    OUTPUT_PREFIX: Prefix for output files (e.g., results/model_results)
    """
    
    # Create output directory if needed
    output_dir = Path(output_prefix).parent
    output_dir. mkdir(parents=True, exist_ok=True)
    
    click.echo("=" * 60)
    click. echo("MODEL FITTING AND EVALUATION")
    click.echo("=" * 60)
    
    # -----------------------------
    # 1.  LOAD DATA
    # -----------------------------
    click.echo(f"\n1. Loading data...")
    train_df = pd.read_csv(train_data_path)
    test_df = pd.read_csv(test_data_path)
    
    click.echo(f"   Training set: {len(train_df)} rows")
    click.echo(f"   Test set: {len(test_df)} rows")
    
    # Separate features and target
    X_train = train_df.drop(columns=['Class'])
    y_train = train_df['Class']
    X_test = test_df.drop(columns=['Class'])
    y_test = test_df['Class']
    
    # -----------------------------
    # 2.  SCALE FEATURES
    # -----------------------------
    click.echo(f"\n2. Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # -----------------------------
    # 3. TRAIN MODEL
    # -----------------------------
    click.echo(f"\n3. Training logistic regression model...")
    clf = fit_model(X_train_scaled, y_train)
    click.echo(f"Model training complete")
    
    # -----------------------------
    # 4. SAVE MODEL
    # -----------------------------
    model_path = f"{output_prefix}_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump({'model': clf, 'scaler': scaler}, f)
    click.echo(f"Model saved to {model_path}")
    
    # -----------------------------
    # 5. GENERATE EVALUATION ARTIFACTS
    # -----------------------------
    click.echo(f"\n4. Generating evaluation artifacts...")
    
    save_confusion_matrix(clf, X_test_scaled, y_test, output_prefix)
    save_classification_report(clf, X_test_scaled, y_test, output_prefix)
    save_feature_importance(clf, X_train. columns. tolist(), output_prefix)
    
    click.echo("\n" + "=" * 60)
    click.echo("MODEL EVALUATION COMPLETE")
    click.echo("=" * 60)


if __name__ == "__main__":
    main()