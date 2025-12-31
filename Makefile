.PHONY: all clean validated figures models report

all: report

# Create processed data directory
data/processed:
	mkdir data/processed

# Acquire raw raisin data from source
data/raw/raisin_data.csv: scripts/sc1_data_acquisition.py data/processed
	python scripts/sc1_data_acquisition.py \
		data/raisin.csv \
		data/raw/raisin_data.csv

# Clean and preprocess raw data
data/processed/raisin_cleaned.csv: scripts/sc2_data_cleaning.py data/raw/raisin_data.csv data/processed
	python scripts/sc2_data_cleaning.py \
		data/raw/raisin_data.csv \
		data/processed/raisin_cleaned.csv

# Validate cleaned training data
validated: data/processed/raisin_cleaned_train.csv scripts/sc3_data_validation.py
	python scripts/sc3_data_validation.py \
		data/processed/raisin_cleaned_train.csv

# Generate visualization plots and figures
figures: validated scripts/sc4_data_visualization.py
	python scripts/sc4_data_visualization.py \
		data/processed/raisin_cleaned_train.csv \
		results/figures

# Train and fit classification models
models: validated scripts/sc5_model_fitting.py
	python scripts/sc5_model_fitting.py \
		data/processed/raisin_cleaned_train.csv \
		data/processed/raisin_cleaned_test.csv \
		results/models/raisin_model

# Render final analysis report in HTML and PDF formats
report: data/raw/raisin_data.csv data/processed/raisin_cleaned.csv validated figures models analysis/raisin_classification_analysis.qmd analysis/raisin_classification_analysis.ipynb analysis/references.bib
	quarto render analysis/raisin_classification_analysis.qmd --to html
	quarto render analysis/raisin_classification_analysis.qmd --to pdf

# Remove all generated files and outputs
clean:
	rm -rf data/raw/* data/processed/* results/* analysis/*.html analysis/*.pdfn