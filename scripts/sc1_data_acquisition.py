"""
Downloads data from URL or reads from local path and saves it locally. 

Usage:
    python s1_data_acquisition.py <input_path_or_url> <output_path>
"""
import click
import pandas as pd
import requests
from pathlib import Path

@click.command()
@click.argument("input_path", type=str)
@click.argument("output_path", type=click.Path())
def main(input_path, output_path):
    # Check if input is a URL
    if input_path.startswith('http://') or input_path.startswith('https://'):
        click.echo(f"Downloading data from {input_path}...")
        response = requests.get(input_path)
        response.raise_for_status()
        
        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        with open(output_path, 'wb') as f:
            f.write(response. content)
        click.echo(f"Data downloaded and saved to {output_path}")
    else:
        # Read from local path
        click.echo(f"Reading data from {input_path}...")
        df = pd.read_csv(input_path)
        
        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save to new location
        df.to_csv(output_path, index=False)
        click.echo(f"Data copied to {output_path}")

if __name__ == "__main__":
    main()
