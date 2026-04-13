# Statistical Hypothesis Testing for Manufacturing Quality Analysis

A structured collection of six hypothesis tests applied to production data from a chocolate manufacturer. Each test addresses a specific business question about production quality, process improvements, customer preferences, and regional performance.

## Business Questions Addressed

| Test | Type | Question |
|------|------|----------|
| Weight Consistency | One-sample t-test (two-tailed) | Is the average bar weight statistically equal to the 100g target? |
| Thickness Improvement | Paired t-test (one-tailed) | Did the new production process increase bar thickness? |
| Sugar Substitute | Independent t-test + Levene | Does the sugar substitute produce different sweetness than regular sugar? |
| Flavour Preference | Chi-square | Is there a customer preference between spicy cinnamon and cool mint? |
| Shift Performance | One-way ANOVA | Do production shifts A, B, and C perform at the same level? |
| Regional Satisfaction | MANOVA | Do sales and satisfaction scores differ significantly across regions? |

## Datasets

| File | Contents |
|------|----------|
| `chocolate_weight.csv` | Weights of 50 randomly sampled bars |
| `chocolate_thickness.csv` | Before/after thickness measurements for 30 bars |
| `chocolate_sweetness.csv` | Sweetness scores for sugar substitute and regular sugar groups |
| `chocolate_preferences.csv` | Customer flavour preference survey results |
| `chocolate_production.csv` | Monthly production counts per shift (A, B, C) |
| `chocolate_satisfaction.csv` | Sales and satisfaction scores across regions |

## Project Structure

```
16_chocolate_statistical_testing/
├── statistical_testing.py  # All six tests in a single script
├── requirements.txt
└── README.md
```

## Requirements

```
pandas
scipy
statsmodels
```

Install with:

```bash
pip install -r requirements.txt
```

## Usage

Place all six CSV files in the same directory and run:

```bash
python statistical_testing.py
```

All results are printed to stdout with the p-value and a plain-language hypothesis test decision for each test.

## Significance Levels

- Tests 1, 3, 5, 6: alpha = 0.05 (95% confidence)
- Test 2: alpha = 0.10 (90% confidence)
- Test 4: alpha = 0.01 (99% confidence)
