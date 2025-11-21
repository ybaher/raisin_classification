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

Wijayabahu, A.T., Waugh, S.G., Ukhanova, M. et al. Dietary raisin intake has limited effect on gut microbiota composition in adult volunteers. Nutr J 18, 14 (2019). https://doi.org/10.1186/s12937-019-0439-1

Rodrigo-Gonzalo, M.J., Recio-Rodríguez, J.I., Méndez-Sánchez, R. et al. Effect of including a dietary supplement of raisins, a food rich in polyphenols, on cognitive function in healthy older adults; a study protocol for a randomized clinical trial. BMC Geriatr 23, 182 (2023). https://doi.org/10.1186/s12877-023-03882-6

Chibuluzo, S., Pitt, T. Raisin allergy in an 8 year old patient. All Asth Clin Immun 10 (Suppl 2), A6 (2014). https://doi.org/10.1186/1710-1492-10-S2-A6

Charvet, A., Brogan Hartlieb, K., Yeh, Y. et al. A comparison of snack serving sizes to USDA guidelines in healthy weight and overweight minority preschool children enrolled in Head Start. BMC Obes 3, 36 (2016). https://doi.org/10.1186/s40608-016-0116-2

Chebil, S., Rjiba-Bahri, W., Oueslati, S. et al. Ochratoxigenic fungi and Ochratoxin A determination in dried grapes marketed in Tunisia. Ann Microbiol 70, 38 (2020). https://doi.org/10.1186/s13213-020-01584-7
