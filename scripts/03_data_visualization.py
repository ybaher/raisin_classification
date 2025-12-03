import click
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import altair as alt

@click.command()
@click.option('--processed-training-data', type=str, help="Path to processed training data")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")

def main(processed_training_data, plot_to):
    """
    Reads raw data, cleans it, transforms it, splits it,
    and writes processed train/test sets.
    """

    # -----------------------------
    # 1. READ CLEAN DATA
    # -----------------------------
    df = pd.read_csv(processed_training_data)

    # -----------------------------
    # 2. SPLIT DATA
    # -----------------------------
    X = df.drop(columns=['Class'])
    y = df['Class']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=123
    )
    
    # Train model for confusion matrix
    clf = LogisticRegression(max_iter=2000)
    clf.fit(X_train, y_train) 

    # -----------------------------
    # 3. SCATTER PLOT
    # -----------------------------
    df = pd.concat([X, y], axis=1)
    df["Class"] = df["Class"].astype(str)

    axis_length_scatterplot = alt.Chart(df).mark_circle(size=60).encode(
        x='MajorAxisLength:Q',
        y='MinorAxisLength:Q',
        color='Class:N',
        tooltip=['Class', 'Area', 'Perimeter']
    ).properties(title = 'Minor Axis vs. Major Axis Length')

    # -----------------------------
    # 4. HEAT MAP
    # -----------------------------
    correlation_matrix = X.corr().stack().reset_index()
    correlation_matrix.columns = ['Feature1', 'Feature2', 'Correlation']
    correlation_heatmap = alt.Chart(correlation_matrix).mark_rect().encode(
        x='Feature1:N',
        y='Feature2:N',
        color=alt.Color('Correlation:Q', scale=alt.Scale(range='diverging'), title='Correlation')
    ).properties(
        width=400,
        height=400
    )
    annotations = alt.Chart(correlation_matrix).mark_text(baseline='middle').encode(
        x='Feature1:N',
        y='Feature2:N',
        text=alt.Text('Correlation:Q', format='.2f'),
        color=alt.condition(
            alt.datum.Correlation > 0.5,
            alt.value('white'),
            alt.value('black')
        )
    )
    correlation_heatmap = (correlation_heatmap + annotations).properties(title = 'Pearson Correlation Matrix')

    # -----------------------------
    # 5. CONFUSION MATRIX
    # -----------------------------
    cm_display = ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test)

    # -----------------------------
    # 6. SAVE OUTPUT FILES
    # -----------------------------
    
    axis_length_scatterplot.save(os.path.join(plot_to, "scatter_plot.png"),
              scale_factor=2.0)
    correlation_heatmap.save(os.path.join(plot_to, "heat_map.png"),
              scale_factor=2.0)
    cm_display.save(os.path.join(plot_to, "confusion_matrix.png"),
              scale_factor=2.0)
    
    click.echo("Processed data visualization saved.")


if __name__ == "__main__":
    main()
