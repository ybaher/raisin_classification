"""
Creates exploratory data visualizations from processed training data.  

Usage:
    python s4_data_visualization.py <input_path> <output_dir>
"""
import click
import os
import pandas as pd
from pathlib import Path
import altair as alt

@click.command()
@click.argument('input_path', type=click. Path(exists=True))
@click.argument('output_dir', type=click.Path())
def main(input_path, output_dir):
    """
    Reads processed training data and creates EDA visualizations.
    
    INPUT_PATH: Path to processed training data
    OUTPUT_DIR: Directory where plots will be saved
    """

    # -----------------------------
    # 1. READ CLEAN DATA
    # -----------------------------
    click.echo(f"Reading processed data from {input_path}...")
    df = pd.read_csv(input_path)
    click.echo(f"Loaded {len(df)} rows with {len(df.columns)} columns")

    # -----------------------------
    # 2.  SCATTER PLOT
    # -----------------------------
    click.echo("Creating scatter plot...")
    df["Class"] = df["Class"].astype(str)

    axis_length_scatterplot = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X('MajorAxisLength:Q', title='Major Axis Length'),
        y=alt.Y('MinorAxisLength:Q', title='Minor Axis Length'),
        color=alt. Color('Class:N', title='Class'),
        tooltip=['Class', 'Area', 'Perimeter']
    ).properties(
        title='Minor Axis vs.  Major Axis Length by Class',
        width=500,
        height=400
    )

    # -----------------------------
    # 3.  CORRELATION HEAT MAP
    # -----------------------------
    click.echo("Creating correlation heatmap...")
    
    # Separate features and target
    X = df.drop(columns=['Class'])
    X_numeric = X.select_dtypes(include=['number'])  # <-- only numeric columns
    correlation_matrix = X_numeric.corr().stack().reset_index()
    correlation_matrix.columns = ['Feature1', 'Feature2', 'Correlation']
    
    correlation_heatmap = alt. Chart(correlation_matrix).mark_rect().encode(
        x=alt.X('Feature1:N', title=''),
        y=alt.Y('Feature2:N', title=''),
        color=alt.Color('Correlation:Q', 
                       scale=alt.Scale(scheme='redblue', domain=[-1, 1]), 
                       title='Correlation')
    ).properties(
        width=400,
        height=400
    )
    
    annotations = alt.Chart(correlation_matrix).mark_text(baseline='middle').encode(
        x='Feature1:N',
        y='Feature2:N',
        text=alt.Text('Correlation:Q', format='.2f'),
        color=alt. condition(
            abs(alt.datum.Correlation) > 0.5,
            alt.value('white'),
            alt.value('black')
        )
    )
    
    correlation_heatmap = (correlation_heatmap + annotations). properties(
        title='Feature Correlation Matrix'
    )

    # -----------------------------
    # 4. CLASS DISTRIBUTION
    # -----------------------------
    click.echo("Creating class distribution plot...")
    
    class_counts = df['Class']. value_counts().reset_index()
    class_counts.columns = ['Class', 'Count']
    
    class_distribution = alt.Chart(class_counts).mark_bar().encode(
        x=alt.X('Class:N', title='Class'),
        y=alt.Y('Count:Q', title='Count'),
        color=alt.Color('Class:N', legend=None)
    ). properties(
        title='Class Distribution',
        width=400,
        height=300
    )

    # -----------------------------
    # 5. SAVE OUTPUT FILES
    # -----------------------------
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save as png files (no additional dependencies required)
    scatter_path = os.path.join(output_dir, "eda_scatter_plot.png")
    heatmap_path = os.path.join(output_dir, "eda_correlation_heatmap.png")
    distribution_path = os.path.join(output_dir, "eda_class_distribution.png")
    
    axis_length_scatterplot.save(scatter_path)
    correlation_heatmap.save(heatmap_path)
    class_distribution.save(distribution_path)
    
    click.echo(f"Scatter plot saved to {scatter_path}")
    click.echo(f"Correlation heatmap saved to {heatmap_path}")
    click. echo(f"Class distribution saved to {distribution_path}")


if __name__ == "__main__":
    main()