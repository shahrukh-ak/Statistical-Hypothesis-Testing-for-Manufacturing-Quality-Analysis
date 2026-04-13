"""
Statistical Hypothesis Testing for Manufacturing Quality Analysis
=================================================================
Applies five statistical tests to production data from a chocolate
manufacturer: one-sample t-test (weight consistency), paired t-test
(process improvement), independent t-test (sugar substitute), chi-square
test (flavour preference), and one-way ANOVA + MANOVA (shift performance
and regional satisfaction).

Datasets:
  chocolate_weight.csv
  chocolate_thickness.csv
  chocolate_sweetness.csv
  chocolate_preferences.csv
  chocolate_production.csv
  chocolate_satisfaction.csv
"""

import pandas as pd
import scipy.stats as st
from statsmodels.multivariate.manova import MANOVA


# ── Utility ───────────────────────────────────────────────────────────────────

def read_p_value(p_value: float, alpha: float):
    """Print the p-value and the hypothesis test decision."""
    print(f"  p-value : {p_value:.6f}")
    if p_value > alpha:
        print(f"  Decision: Fail to reject H0 (alpha={alpha})")
    else:
        print(f"  Decision: Reject H0 (alpha={alpha})")


# ── Test 1: One-Sample T-Test – Weight Consistency ───────────────────────────

def test_weight_consistency(filepath: str = "chocolate_weight.csv",
                            target: float = 100.0, alpha: float = 0.05):
    """
    H0: Mean bar weight = 100g
    H1: Mean bar weight != 100g  (two-tailed)
    """
    df = pd.read_csv(filepath)
    mean_weight = df["weight"].mean()
    print(f"\n[Test 1] Chocolate Bar Weight Consistency")
    print(f"  Sample mean : {mean_weight:.4f}g  |  Target : {target}g")

    t_val, p_val = st.ttest_1samp(df["weight"], target)
    print(f"  t-statistic : {t_val:.4f}")
    read_p_value(p_val, alpha)


# ── Test 2: Paired T-Test – Thickness Process Improvement ────────────────────

def test_thickness_improvement(filepath: str = "chocolate_thickness.csv",
                                alpha: float = 0.1):
    """
    H0: Process improvement has not increased chocolate thickness
    H1: Thickness after improvement > thickness before  (one-tailed)
    """
    df = pd.read_csv(filepath)
    print(f"\n[Test 2] Chocolate Thickness Process Improvement (one-tailed)")
    print(f"  Mean before : {df['before'].mean():.4f}")
    print(f"  Mean after  : {df['after'].mean():.4f}")

    t_val, p_val = st.ttest_rel(df["after"], df["before"], alternative="greater")
    print(f"  t-statistic : {t_val:.4f}")
    read_p_value(p_val, alpha)


# ── Test 3: Independent T-Test – Sugar Substitute ────────────────────────────

def test_sugar_substitute(filepath: str = "chocolate_sweetness.csv",
                           alpha: float = 0.05):
    """
    H0: Sugar substitute produces the same sweetness as regular sugar
    H1: Sweetness levels differ  (two-tailed)
    Levene's test is run first to determine whether to assume equal variances.
    """
    df = pd.read_csv(filepath)
    print(f"\n[Test 3] Sugar Substitute Sweetness Comparison")
    print(f"  Mean (sugar_substitute) : {df['sugar_substitute'].mean():.4f}")
    print(f"  Mean (regular_sugar)    : {df['regular_sugar'].mean():.4f}")

    levene_stat, levene_p = st.levene(df["sugar_substitute"], df["regular_sugar"])
    equal_var = levene_p >= alpha
    print(f"  Levene's test p-value   : {levene_p:.4f}  ->  equal_var={equal_var}")

    t_val, p_val = st.ttest_ind(
        df["sugar_substitute"], df["regular_sugar"],
        equal_var=equal_var, alternative="two-sided"
    )
    print(f"  t-statistic : {t_val:.4f}")
    read_p_value(p_val, alpha)


# ── Test 4: Chi-Square Test – Flavour Preference ─────────────────────────────

def test_flavour_preference(filepath: str = "chocolate_preferences.csv",
                             alpha: float = 0.01):
    """
    H0: No significant difference in preference between spicy cinnamon
        and cool mint
    H1: One flavour is preferred over the other
    """
    df = pd.read_csv(filepath)
    observed = df["Preference"].value_counts()
    expected = [len(df) / 2, len(df) / 2]

    print(f"\n[Test 4] Chocolate Flavour Preference (chi-square, alpha={alpha})")
    print(f"  Observed counts:\n{observed.to_string()}")

    chi2, p_val = st.chisquare(observed, expected)
    print(f"  Chi-square : {chi2:.4f}")
    read_p_value(p_val, alpha)


# ── Test 5: One-Way ANOVA – Production Shift Performance ─────────────────────

def test_shift_performance(filepath: str = "chocolate_production.csv",
                            alpha: float = 0.05):
    """
    H0: No significant difference in production between shifts A, B, and C
    H1: At least one shift differs in mean production
    """
    df = pd.read_csv(filepath)
    means = df.iloc[:, 1:].mean()
    print(f"\n[Test 5] Shift Performance – One-Way ANOVA")
    print(f"  Shift means:\n{means.to_string()}")

    f_stat, p_val = st.f_oneway(df["Chocolate_A"], df["Chocolate_B"], df["Chocolate_C"])
    print(f"  F-statistic : {f_stat:.4f}")
    read_p_value(p_val, alpha)


# ── Test 6: MANOVA – Regional Sales and Satisfaction ─────────────────────────

def test_regional_satisfaction(filepath: str = "chocolate_satisfaction.csv",
                                alpha: float = 0.05):
    """
    H0: No significant difference in sales and satisfaction across regions
    H1: At least one region differs on the combined outcome
    """
    df = pd.read_csv(filepath)
    formula = (
        "Chocolate_A_Sales + Chocolate_B_Sales + Chocolate_C_Sales + "
        "Chocolate_A_Satisfaction + Chocolate_B_Satisfaction + Chocolate_C_Satisfaction ~ Region"
    )
    manova  = MANOVA.from_formula(formula, data=df)
    result  = manova.mv_test()
    print(f"\n[Test 6] Regional Sales and Satisfaction – MANOVA")
    print(result)

    p_val = result.results["Region"]["stat"].values[1, -1]
    read_p_value(p_val, alpha)


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_weight_consistency()
    test_thickness_improvement()
    test_sugar_substitute()
    test_flavour_preference()
    test_shift_performance()
    test_regional_satisfaction()
