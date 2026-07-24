"""
============================================================
GER
Hypothesis Tests Utilities
============================================================

Reusable statistical hypothesis tests.

This module centralizes statistical inference
utilities used throughout the GER framework.

Existing public functions remain fully compatible
with previous versions.

Functions
---------
kolmogorov_smirnov(...)
shapiro_wilk(...)
anderson_darling(...)
normality_report(...)

Additional utilities
--------------------
clean_numeric(...)
levene_test(...)
bartlett_test(...)
============================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats


# ============================================================
# Version
# ============================================================

HYPOTHESIS_VERSION = "2.0"


# ============================================================
# Constants
# ============================================================

DEFAULT_ALPHA = 0.05

MINIMUM_SAMPLE_SIZE = 3


# ============================================================
# Public API
# ============================================================

__all__ = [

    "kolmogorov_smirnov",

    "shapiro_wilk",

    "anderson_darling",

    "normality_report",

    "clean_numeric",

    "levene_test",

    "bartlett_test",

]


# ============================================================
# Utilities
# ============================================================

def clean_numeric(values):

    """
    Convert an iterable into a clean numeric array.

    NaN and infinite values are removed.
    """

    values = np.asarray(

        values,

        dtype=float,

    )

    return values[

        np.isfinite(values)

    ]


def _validate_sample(values):

    values = clean_numeric(values)

    if len(values) < MINIMUM_SAMPLE_SIZE:

        raise ValueError(

            f"At least {MINIMUM_SAMPLE_SIZE} observations are required."

        )

    return values


# ============================================================
# KOLMOGOROV-SMIRNOV
# ============================================================

def kolmogorov_smirnov(

    values,

    distribution,

    params,

):

    """
    One-sample Kolmogorov-Smirnov test.
    """

    values = _validate_sample(values)

    statistic, pvalue = stats.kstest(

        values,

        distribution.name,

        args=params,

    )

    return {

        "test":

            "Kolmogorov-Smirnov",

        "statistic":

            float(statistic),

        "pvalue":

            float(pvalue),

        "accepted":

            bool(

                pvalue >= DEFAULT_ALPHA

            ),

        "alpha":

            DEFAULT_ALPHA,

    }


# ============================================================
# SHAPIRO-WILK
# ============================================================

def shapiro_wilk(values):

    """
    Shapiro-Wilk normality test.
    """

    values = _validate_sample(values)

    statistic, pvalue = stats.shapiro(

        values,

    )

    return {

        "test":

            "Shapiro-Wilk",

        "statistic":

            float(statistic),

        "pvalue":

            float(pvalue),

        "accepted":

            bool(

                pvalue >= DEFAULT_ALPHA

            ),

        "alpha":

            DEFAULT_ALPHA,

    }


# ============================================================
# ANDERSON-DARLING
# ============================================================

def anderson_darling(

    values,

    distribution="norm",

):

    """
    Anderson-Darling goodness-of-fit test.
    """

    values = _validate_sample(values)

    result = stats.anderson(

        values,

        dist=distribution,

    )

    return {

        "test":

            "Anderson-Darling",

        "statistic":

            float(result.statistic),

        "critical_values":

            result.critical_values.tolist(),

        "significance_levels":

            result.significance_level.tolist(),

    }


# ============================================================
# LEVENE
# ============================================================

def levene_test(

    *groups,

):

    """
    Levene homogeneity of variance test.
    """

    groups = [

        _validate_sample(g)

        for g in groups

    ]

    statistic, pvalue = stats.levene(

        *groups,

    )

    return {

        "test":

            "Levene",

        "statistic":

            float(statistic),

        "pvalue":

            float(pvalue),

        "accepted":

            bool(

                pvalue >= DEFAULT_ALPHA

            ),

        "alpha":

            DEFAULT_ALPHA,

    }


# ============================================================
# BARTLETT
# ============================================================

def bartlett_test(

    *groups,

):

    """
    Bartlett homogeneity of variance test.
    """

    groups = [

        _validate_sample(g)

        for g in groups

    ]

    statistic, pvalue = stats.bartlett(

        *groups,

    )

    return {

        "test":

            "Bartlett",

        "statistic":

            float(statistic),

        "pvalue":

            float(pvalue),

        "accepted":

            bool(

                pvalue >= DEFAULT_ALPHA

            ),

        "alpha":

            DEFAULT_ALPHA,

    }


# ============================================================
# NORMALITY REPORT
# ============================================================

def normality_report(values):

    """
    Combined normality assessment.
    """

    values = _validate_sample(values)

    shapiro = shapiro_wilk(

        values,

    )

    anderson = anderson_darling(

        values,

    )

    return {

        "shapiro":

            shapiro,

        "anderson":

            anderson,

    }

# ============================================================
# MANN-WHITNEY
# ============================================================

def mann_whitney_test(

    sample1,

    sample2,

    alternative="two-sided",

):

    """
    Mann-Whitney U test.
    """

    sample1 = _validate_sample(sample1)

    sample2 = _validate_sample(sample2)

    statistic, pvalue = stats.mannwhitneyu(

        sample1,

        sample2,

        alternative=alternative,

    )

    return {

        "test": "Mann-Whitney",

        "statistic": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= DEFAULT_ALPHA),

        "alpha": DEFAULT_ALPHA,

    }


# ============================================================
# WILCOXON
# ============================================================

def wilcoxon_test(values1, values2):

    """
    Wilcoxon signed-rank test.
    """

    values1 = _validate_sample(values1)

    values2 = _validate_sample(values2)

    statistic, pvalue = stats.wilcoxon(

        values1,

        values2,

    )

    return {

        "test": "Wilcoxon",

        "statistic": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= DEFAULT_ALPHA),

        "alpha": DEFAULT_ALPHA,

    }


# ============================================================
# KRUSKAL-WALLIS
# ============================================================

def kruskal_test(*groups):

    """
    Kruskal-Wallis H test.
    """

    groups = [

        _validate_sample(g)

        for g in groups

    ]

    statistic, pvalue = stats.kruskal(

        *groups,

    )

    return {

        "test": "Kruskal-Wallis",

        "statistic": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= DEFAULT_ALPHA),

        "alpha": DEFAULT_ALPHA,

    }


# ============================================================
# ONE-WAY ANOVA
# ============================================================

def anova_test(*groups):

    """
    One-way ANOVA.
    """

    groups = [

        _validate_sample(g)

        for g in groups

    ]

    statistic, pvalue = stats.f_oneway(

        *groups,

    )

    return {

        "test": "ANOVA",

        "statistic": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= DEFAULT_ALPHA),

        "alpha": DEFAULT_ALPHA,

    }


# ============================================================
# CHI-SQUARE
# ============================================================

def chi_square_test(observed):

    """
    Chi-square goodness-of-fit test.
    """

    observed = clean_numeric(observed)

    statistic, pvalue = stats.chisquare(

        observed,

    )

    return {

        "test": "Chi-Square",

        "statistic": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= DEFAULT_ALPHA),

        "alpha": DEFAULT_ALPHA,

    }


# ============================================================
# PEARSON CORRELATION
# ============================================================

def pearson_test(x, y):

    """
    Pearson correlation test.
    """

    x = _validate_sample(x)

    y = _validate_sample(y)

    statistic, pvalue = stats.pearsonr(

        x,

        y,

    )

    return {

        "test": "Pearson",

        "correlation": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= DEFAULT_ALPHA),

        "alpha": DEFAULT_ALPHA,

    }


# ============================================================
# SPEARMAN CORRELATION
# ============================================================

def spearman_test(x, y):

    """
    Spearman rank correlation test.
    """

    x = _validate_sample(x)

    y = _validate_sample(y)

    statistic, pvalue = stats.spearmanr(

        x,

        y,

    )

    return {

        "test": "Spearman",

        "correlation": float(statistic),

        "pvalue": float(pvalue),

        "accepted": bool(pvalue >= DEFAULT_ALPHA),

        "alpha": DEFAULT_ALPHA,

    }


# ============================================================
# BOOTSTRAP CONFIDENCE INTERVAL
# ============================================================

def bootstrap_confidence_interval(

    values,

    statistic=np.mean,

    confidence=0.95,

    iterations=1000,

    random_state=None,

):

    """
    Bootstrap confidence interval.
    """

    values = _validate_sample(values)

    rng = np.random.default_rng(

        random_state

    )

    estimates = []

    n = len(values)

    for _ in range(iterations):

        sample = rng.choice(

            values,

            size=n,

            replace=True,

        )

        estimates.append(

            statistic(sample)

        )

    alpha = 1.0 - confidence

    lower = np.percentile(

        estimates,

        100 * alpha / 2,

    )

    upper = np.percentile(

        estimates,

        100 * (1 - alpha / 2),

    )

    return {

        "confidence": confidence,

        "lower": float(lower),

        "upper": float(upper),

        "estimate": float(statistic(values)),

    }


# ============================================================
# MULTIPLE TESTING CORRECTION
# ============================================================

def multiple_testing_correction(

    pvalues,

    alpha=DEFAULT_ALPHA,

):

    """
    Bonferroni correction.
    """

    pvalues = clean_numeric(pvalues)

    corrected = np.minimum(

        pvalues * len(pvalues),

        1.0,

    )

    return {

        "raw_pvalues": pvalues.tolist(),

        "corrected_pvalues": corrected.tolist(),

        "accepted": (

            corrected >= alpha

        ).tolist(),

    }


# ============================================================
# SUMMARY
# ============================================================

def hypothesis_summary(report):

    """
    Compact summary of hypothesis tests.
    """

    accepted = 0

    rejected = 0

    total = 0

    for result in report.values():

        if (

            isinstance(result, dict)

            and

            "accepted" in result

        ):

            total += 1

            if result["accepted"]:

                accepted += 1

            else:

                rejected += 1

    return {

        "tests": total,

        "accepted": accepted,

        "rejected": rejected,

    }


# ============================================================
# Self Test
# ============================================================

def main():

    np.random.seed(42)

    x = np.random.normal(

        size=1000,

    )

    y = np.random.normal(

        size=1000,

    )

    print("=" * 60)

    print("GER")

    print("Hypothesis Tests")

    print("=" * 60)

    print()

    report = normality_report(

        x,

    )

    print(report)

    print()

    print(

        pearson_test(

            x,

            y,

        )

    )

    print()

    print(

        bootstrap_confidence_interval(

            x,

        )

    )

    print()

    print(

        hypothesis_summary(

            report,

        )

    )


if __name__ == "__main__":

    main()
