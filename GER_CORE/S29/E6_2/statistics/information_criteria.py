"""
============================================================
GER
Information Criteria Utilities
============================================================

Reusable information criteria for statistical
model selection.

Existing public functions remain fully compatible.

Functions
---------
log_likelihood(...)
aic(...)
bic(...)
aicc(...)
information_summary(...)

Additional utilities
--------------------
validate_parameters(...)
parameter_penalty(...)
sample_penalty(...)
hqic(...)
caic(...)
============================================================
"""

from __future__ import annotations

import numpy as np


# ============================================================
# Version
# ============================================================

INFORMATION_CRITERIA_VERSION = "2.0"


# ============================================================
# Constants
# ============================================================

EPSILON = 1e-12


# ============================================================
# Public API
# ============================================================

__all__ = [

    "log_likelihood",

    "aic",

    "bic",

    "aicc",

    "hqic",

    "caic",

    "information_summary",

    "validate_parameters",

    "parameter_penalty",

    "sample_penalty",

]


# ============================================================
# Validation
# ============================================================

def validate_parameters(

    n,

    k,

):

    """
    Validate model dimensions.
    """

    if n <= 0:

        raise ValueError(

            "Sample size must be positive."

        )

    if k < 0:

        raise ValueError(

            "Number of parameters must be non-negative."

        )


# ============================================================
# Penalties
# ============================================================

def parameter_penalty(

    k,

):

    """
    Akaike parameter penalty.
    """

    return float(

        2 * k

    )


def sample_penalty(

    n,

    k,

):

    """
    Bayesian sample penalty.
    """

    validate_parameters(

        n,

        k,

    )

    return float(

        np.log(n) * k

    )


# ============================================================
# LOG-LIKELIHOOD
# ============================================================

def log_likelihood(

    logpdf_values,

):

    """
    Compute total log-likelihood from
    log-density values.
    """

    logpdf_values = np.asarray(

        logpdf_values,

        dtype=float,

    )

    return float(

        np.sum(

            logpdf_values

        )

    )


# ============================================================
# AIC
# ============================================================

def aic(

    k,

    loglikelihood,

):

    """
    Akaike Information Criterion.
    """

    return float(

        parameter_penalty(

            k,

        )

        -

        2 * loglikelihood

    )


# ============================================================
# BIC
# ============================================================

def bic(

    n,

    k,

    loglikelihood,

):

    """
    Bayesian Information Criterion.
    """

    validate_parameters(

        n,

        k,

    )

    return float(

        sample_penalty(

            n,

            k,

        )

        -

        2 * loglikelihood

    )


# ============================================================
# AICc
# ============================================================

def aicc(

    n,

    k,

    loglikelihood,

):

    """
    Small-sample corrected AIC.
    """

    validate_parameters(

        n,

        k,

    )

    base = aic(

        k,

        loglikelihood,

    )

    if n <= k + 1:

        return float(

            "inf"

        )

    correction = (

        2

        * k

        * (k + 1)

    ) / (

        n - k - 1

    )

    return float(

        base + correction

    )


# ============================================================
# HQIC
# ============================================================

def hqic(

    n,

    k,

    loglikelihood,

):

    """
    Hannan-Quinn Information Criterion.
    """

    validate_parameters(

        n,

        k,

    )

    if n <= 1:

        return float(

            "inf"

        )

    penalty = (

        2

        * k

        * np.log(

            np.log(

                n

            )

        )

    )

    return float(

        penalty

        -

        2 * loglikelihood

    )


# ============================================================
# CAIC
# ============================================================

def caic(

    n,

    k,

    loglikelihood,

):

    """
    Consistent Akaike Information Criterion.
    """

    validate_parameters(

        n,

        k,

    )

    penalty = (

        k

        * (

            np.log(

                n

            )

            + 1

        )

    )

    return float(

        penalty

        -

        2 * loglikelihood

    )


# ============================================================
# INFORMATION SUMMARY
# ============================================================

def information_summary(

    n,

    k,

    loglikelihood,

):

    """
    Return all supported information criteria.
    """

    validate_parameters(

        n,

        k,

    )

    return {

        "loglikelihood":

            float(

                loglikelihood

            ),

        "AIC":

            aic(

                k,

                loglikelihood,

            ),

        "AICc":

            aicc(

                n,

                k,

                loglikelihood,

            ),

        "BIC":

            bic(

                n,

                k,

                loglikelihood,

            ),

        "HQIC":

            hqic(

                n,

                k,

                loglikelihood,

            ),

        "CAIC":

            caic(

                n,

                k,

                loglikelihood,

            ),

    }

# ============================================================
# EBIC
# ============================================================

def ebic(

    n,

    k,

    loglikelihood,

    gamma=0.5,

):

    """
    Extended Bayesian Information Criterion.
    """

    validate_parameters(

        n,

        k,

    )

    penalty = (

        np.log(n)

        +

        2.0 * gamma * np.log(max(n, 2))

    ) * k

    return float(

        penalty

        -

        2.0 * loglikelihood

    )


# ============================================================
# DELTA CRITERION
# ============================================================

def delta_information_criterion(

    values,

):

    """
    Difference from the best model.
    """

    values = np.asarray(

        values,

        dtype=float,

    )

    if len(values) == 0:

        return np.array([])

    return values - np.min(values)


# ============================================================
# AKAIKE WEIGHTS
# ============================================================

def akaike_weights(

    aic_values,

):

    """
    Akaike model weights.
    """

    delta = delta_information_criterion(

        aic_values,

    )

    weights = np.exp(

        -0.5 * delta

    )

    weights /= np.sum(weights)

    return weights


# ============================================================
# MODEL PROBABILITIES
# ============================================================

def model_probability(

    aic_values,

):

    """
    Alias for Akaike weights.
    """

    return akaike_weights(

        aic_values

    )


# ============================================================
# LIKELIHOOD RATIO
# ============================================================

def likelihood_ratio(

    loglikelihood_a,

    loglikelihood_b,

):

    """
    Likelihood ratio statistic.
    """

    return float(

        2.0

        *

        (

            loglikelihood_b

            -

            loglikelihood_a

        )

    )


# ============================================================
# BEST MODEL
# ============================================================

def best_model(

    models,

    criterion="AIC",

):

    """
    Return the best model according to the
    selected information criterion.
    """

    if len(models) == 0:

        return None

    index = models[criterion].idxmin()

    return models.loc[index].to_dict()


# ============================================================
# RANK MODELS
# ============================================================

def rank_models(

    models,

    criterion="AIC",

):

    """
    Rank models according to a criterion.
    """

    if len(models) == 0:

        return models

    return (

        models

        .sort_values(

            criterion,

            ascending=True,

        )

        .reset_index(

            drop=True,

        )

    )


# ============================================================
# COMPARE MODELS
# ============================================================

def compare_models(

    models,

    criterion="AIC",

):

    """
    Add delta criterion and Akaike weights.
    """

    models = rank_models(

        models,

        criterion,

    ).copy()

    if len(models) == 0:

        return models

    delta = delta_information_criterion(

        models[criterion]

    )

    weights = akaike_weights(

        models[criterion]

    )

    models["Delta"] = delta

    models["Weight"] = weights

    return models


# ============================================================
# SELF TEST
# ============================================================

def main():

    import pandas as pd

    print("=" * 60)

    print("GER")

    print("Information Criteria")

    print("=" * 60)

    print()

    ll = -135.82

    summary = information_summary(

        n=500,

        k=4,

        loglikelihood=ll,

    )

    for key, value in summary.items():

        print(

            f"{key:15s}: {value}"

        )

    print()

    models = pd.DataFrame(

        {

            "Model": [

                "Normal",

                "Gamma",

                "LogNormal",

                "Weibull",

            ],

            "AIC": [

                285.4,

                289.8,

                286.7,

                291.1,

            ],

        }

    )

    comparison = compare_models(

        models,

    )

    print(comparison)

    print()

    print(

        "Best model:"

    )

    print(

        best_model(

            comparison

        )

    )


if __name__ == "__main__":

    main()
