.PHONY: all clean validated figures models report

all: report

data/processed:
	mkdir data/processed

data/raw/raisin_data.csv: scripts/sc1_data_acquisition.py data/processed
	python scripts/sc1_data_acquisition.py \
		data/raisin.csv \
		data/raw/raisin_data.csv

data/processed/raisin_cleaned.csv: scripts/sc2_data_cleaning.py data/raw/raisin_data.csv data/processed
	python scripts/sc2_data_cleaning.py \
		data/raw/raisin_data.csv \
        data/processed/raisin_cleaned.csv


validated: data/processed/raisin_cleaned_train.csv scripts/sc3_data_validation.py
	python scripts/sc3_data_validation.py \
		data/processed/raisin_cleaned_train.csv

figures: validated scripts/sc4_data_visualization.py
	python scripts/sc4_data_visualization.py \
		data/processed/raisin_cleaned_train.csv \
		results/figures

models: validated scripts/sc5_model_fitting.py
	python scripts/sc5_model_fitting.py \
		data/processed/raisin_cleaned_train.csv \
		data/processed/raisin_cleaned_test.csv \
		results/models/raisin_model

report: data/raw/raisin_data.csv data/processed/raisin_cleaned.csv validated figures models analysis/raisin_classification_analysis.qmd analysis/raisin_classification_analysis.ipynb analysis/references.bib
	quarto render analysis/raisin_classification_analysis.qmd --to html
	quarto render analysis/raisin_classification_analysis.qmd --to pdf

clean:
	rm -rf data/raw/* data/processed/* results/* analysis/*.html analysis/*.pdfn