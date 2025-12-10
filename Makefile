.PHONY: all clean validated figures models report

all: report

data/raw/raisin_data.csv: scripts/01_data_acquisition.py
	python scripts/01_data_acquisition.py \
		data/raisin.csv \
		data/raw/raisin_data.csv

data/processed/raisin_cleaned.csv: scripts/02_data_cleaning.py data/raw/raisin_data.csv
	python scripts/02_data_cleaning.py \
		data/raw/raisin_data.csv \
		data/processed/raisin_cleaned.csv

validated: data/processed/raisin_cleaned.csv scripts/03_data_validation.py
	python scripts/03_data_validation.py \
		data/processed/raisin_cleaned.csv

figures: validated scripts/04_data_visualization.py
	python scripts/04_data_visualization.py \
		data/processed/raisin_cleaned.csv 
		results/figures

models: validated scripts/05_model_fitting.py
	python scripts/05_model_fitting.py \
		data/processed/raisin_cleaned_train.csv \
		data/processed/raisin_cleaned_test.csv \
		results/models/raisin_model

report: analysis/raisin_classification_analysis.qmd \
        analysis/raisin_classification_analysis.ipynb \
        analysis/references.bib
	quarto render analysis/raisin_classification_analysis.qmd --to html
	quarto render analysis/raisin_classification_analysis.qmd --to pdf
	mv analysis/raisin_classification_analysis.html docs/analysis/index.html
	mv analysis/raisin_classification_analysis.pdf docs/analysis/index.html.pdf

clean:
	rm -rf data/raw/* data/processed/* results/* analysis/*.html analysis/*.pdf