"""
============================================================
GER
Distribution Fitting Utilities
============================================================

Reusable probability distribution fitting utilities.

Functions
---------
fit_distribution(...)
fit_all_distributions(...)
best_distribution(...)
============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy import stats


# ============================================================
# DEFAULT DISTRIBUTIONS
# ============================================================

DEFAULT_DISTRIBUTIONS = [

    stats.norm,

    stats.expon,

    stats.gamma,

    stats.lognorm,

    stats.weibull_min,

]


# ============================================================
# FIT SINGLE DISTRIBUTION
# ============================================================

def fit_distribution(values, distribution):

    values = np.asarray(values, dtype=float)

    params = distribution.fit(values)

    loglikelihood = np.sum(

        distribution.logpdf(
            values,
            *params,
        )

    )

    k = len(params)

    n = len(values)

    aic = 2 * k - 2 * loglikelihood

    bic = np.log(n) * k - 2 * loglikelihood

    ks, pvalue = stats.kstest(

        values,

        distribution.name,

        args=params,

    )

    return {

        "Distribution": distribution.name,

        "AIC": float(aic),

        "BIC": float(bic),

        "KS": float(ks),

        "KS p-value": float(pvalue),

        "Accepted": bool(pvalue >= 0.05),

        "Parameters": params,

    }


# ============================================================
# FIT MULTIPLE DISTRIBUTIONS
# ============================================================

def fit_all_distributions(

    values,

    distributions=None,

):

    if distributions is None:

        distributions = DEFAULT_DISTRIBUTIONS

    results = []

    for distribution in distributions:

        try:

            results.append(

                fit_distribution(

                    values,

                    distribution,

                )

            )

        except Exception:

            continue

    if len(results) == 0:

        return pd.DataFrame()

    return (

        pd.DataFrame(results)

        .sort_values("AIC")

        .reset_index(drop=True)

    )


# ============================================================
# BEST MODEL
# ============================================================

def best_distribution(results):

    if len(results) == 0:

        return None

    return results.iloc[0].to_dict()


# ============================================================
# ACCEPTED MODELS
# ============================================================

def accepted_distributions(results):

    if len(results) == 0:

        return results

    return (

        results

        .loc[results["Accepted"]]

        .reset_index(drop=True)

    )


# ============================================================
# REJECTED MODELS
# ============================================================

def rejected_distributions(results):

    if len(results) == 0:

        return results

    return (

        results

        .loc[~results["Accepted"]]

        .reset_index(drop=True)

    )
