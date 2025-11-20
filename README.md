# Raisin Classification

Authors: Shreya Kakachery, Eric Wong, Yasaman Baher

## About

Analyzing images of raisins in order to classify them as Kecimen or Besni variety

## Usage

Follow the instructions below to reproduce the analysis.

# Setup

1. Clone this GitHub repository
2. To run the scripts in this repository, we recommend using the provided environment:
```python
   conda env create -f environment.yml
```
## Report

The final report can be found at this [link](https://github.com/ybaher/raisin_classification/blob/main/crazy_raisins.ipynb).

## Dependencies

name: craisins
channels:
  - conda-forge
dependencies:
  - python=3.9
  - pandas
  - altair
  - numpy
  - ipykernel
  - scikit-learn
  - matplotlib
  - pip:
      - ucimlrepo

## License

The Raisin Classification report is licensed under the
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
See [the license file](LICENSE.md) for more information. . If
re-using/re-mixing please provide attribution and link to this webpage.
The software code contained within this repository is licensed under the
MIT license. See [the license file](LICENSE.md) for more information.

## References

Olmo-Cunillera, Alexandra et al. “Is Eating Raisins Healthy?.” Nutrients vol. 12,1 54. 24 Dec. 2019, doi:10.3390/nu12010054

Wijayabahu, A.T., Waugh, S.G., Ukhanova, M. et al. Dietary raisin intake has limited effect on gut microbiota composition in adult volunteers. Nutr J 18, 14 (2019). <https://doi.org/10.1186/s12937-019-0439-1>
