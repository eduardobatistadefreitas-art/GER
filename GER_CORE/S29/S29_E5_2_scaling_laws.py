#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==========================================================================
GER
S29-E5.2
Scaling Laws of the Stability Region Space
==========================================================================

Objective
---------
Automatically discover empirical scaling laws between all geometric
observables of the Stability Region Space.

For every observable pair the experiment evaluates:

    • Linear
    • Quadratic
    • Power Law
    • Exponential
    • Logarithmic

For every fitted model:

    • Equation
    • R²
    • RMSE
    • MAE
    • AIC
    • BIC

Outputs
-------
best_models.csv
all_models.csv
law_ranking.csv
pairwise_fits.json
plots/
summary.txt

Author
------
GER Scientific Framework
"""

import os
import json
import warnings
import itertools

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.stats import linregress

from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)

warnings.filterwarnings("ignore")

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = "/content/GER"

DATABASE = os.path.join(
    PROJECT_ROOT,
    "GER_CORE",
    "S29",
    "geometric_database",
    "region_database"
)

INPUT_TABLE = os.path.join(
    DATABASE,
    "correlation_table.csv"
)

RESULTS = "/content/drive/MyDrive/GER_RESULTS/S29_E5.2"

PLOTS = os.path.join(
    RESULTS,
    "plots"
)

os.makedirs(
    RESULTS,
    exist_ok=True
)

os.makedirs(
    PLOTS,
    exist_ok=True
)

# ============================================================
# PRINT
# ============================================================

def line():
    print("=" * 70)


def header():

    line()

    print("GER")

    print("S29-E5.2")

    print("Scaling Laws of the Stability Region Space")

    line()

# ============================================================
# LOAD
# ============================================================

def load_database():

    if not os.path.exists(INPUT_TABLE):

        raise FileNotFoundError(
            INPUT_TABLE
        )

    df = pd.read_csv(
        INPUT_TABLE
    )

    return df

# ============================================================
# CLEAN DATABASE
# ============================================================

def clean_database(df):

    print()

    print("Cleaning observables...")

    numeric = df.select_dtypes(
        include=np.number
    ).copy()

    removed = []

    # -----------------------------
    # Remove NaN columns
    # -----------------------------

    for c in list(numeric.columns):

        if numeric[c].isna().all():

            removed.append(c)

            numeric.drop(
                columns=c,
                inplace=True
            )

    # -----------------------------
    # Remove constant columns
    # -----------------------------

    for c in list(numeric.columns):

        if numeric[c].nunique() <= 1:

            removed.append(c)

            numeric.drop(
                columns=c,
                inplace=True
            )

    # -----------------------------
    # Remove Inf
    # -----------------------------

    numeric.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    numeric.dropna(
        axis=1,
        how="any",
        inplace=True
    )

    print()

    print(f"Remaining observables : {len(numeric.columns)}")

    print(f"Removed observables   : {len(removed)}")

    with open(

        os.path.join(
            RESULTS,
            "removed_observables.txt"
        ),

        "w"

    ) as f:

        for r in removed:

            f.write(r + "\n")

    return numeric

# ============================================================
# MATHEMATICAL MODELS
# ============================================================

def linear_model(
    x,
    a,
    b
):

    return a * x + b


def quadratic_model(
    x,
    a,
    b,
    c
):

    return a*x*x + b*x + c


def power_model(
    x,
    a,
    b
):

    return a * np.power(
        x,
        b
    )


def exponential_model(
    x,
    a,
    b
):

    return a * np.exp(
        b*x
    )


def logarithmic_model(
    x,
    a,
    b
):

    return a + b*np.log(x)

# ============================================================
# METRICS
# ============================================================

def compute_metrics(
    y,
    prediction,
    parameters
):

    n = len(y)

    k = parameters

    rss = np.sum(
        (y-prediction)**2
    )

    rmse = np.sqrt(
        mean_squared_error(
            y,
            prediction
        )
    )

    mae = mean_absolute_error(
        y,
        prediction
    )

    r2 = r2_score(
        y,
        prediction
    )

    if rss <= 0:

        rss = 1e-12

    aic = (

        n*np.log(rss/n)

        +

        2*k

    )

    bic = (

        n*np.log(rss/n)

        +

        k*np.log(n)

    )

    return {

        "R2": r2,
        "RMSE": rmse,
        "MAE": mae,
        "AIC": aic,
        "BIC": bic

    }

# ============================================================
# SAFE CURVE FIT
# ============================================================

def safe_fit(
    model,
    x,
    y,
    p0=None
):

    try:

        params, _ = curve_fit(

            model,

            x,

            y,

            p0=p0,

            maxfev=50000

        )

        prediction = model(
            x,
            *params
        )

        return params, prediction

    except Exception:

        return None, None
      # ============================================================
# FITTERS
# ============================================================

def fit_linear(x, y):

    slope, intercept, _, _, _ = linregress(x, y)

    prediction = linear_model(
        x,
        slope,
        intercept
    )

    metrics = compute_metrics(
        y,
        prediction,
        2
    )

    equation = (
        f"y = {slope:.8f} * x + {intercept:.8f}"
    )

    return {

        "Model": "Linear",
        "Equation": equation,
        "Parameters": [slope, intercept],
        "Prediction": prediction,
        **metrics

    }


def fit_quadratic(x, y):

    params, prediction = safe_fit(

        quadratic_model,

        x,

        y

    )

    if params is None:

        return None

    metrics = compute_metrics(

        y,

        prediction,

        3

    )

    equation = (

        f"y = {params[0]:.8f}*x² + "

        f"{params[1]:.8f}*x + "

        f"{params[2]:.8f}"

    )

    return {

        "Model": "Quadratic",
        "Equation": equation,
        "Parameters": params.tolist(),
        "Prediction": prediction,
        **metrics

    }


def fit_power(x, y):

    if np.any(x <= 0):

        return None

    if np.any(y <= 0):

        return None

    params, prediction = safe_fit(

        power_model,

        x,

        y,

        p0=[1.0, 1.0]

    )

    if params is None:

        return None

    metrics = compute_metrics(

        y,

        prediction,

        2

    )

    equation = (

        f"y = {params[0]:.8f}"

        f" * x^{params[1]:.8f}"

    )

    return {

        "Model": "Power",
        "Equation": equation,
        "Parameters": params.tolist(),
        "Prediction": prediction,
        **metrics

    }


def fit_exponential(x, y):

    if np.any(y <= 0):

        return None

    params, prediction = safe_fit(

        exponential_model,

        x,

        y,

        p0=[1.0, 0.01]

    )

    if params is None:

        return None

    metrics = compute_metrics(

        y,

        prediction,

        2

    )

    equation = (

        f"y = {params[0]:.8f}"

        f" * exp({params[1]:.8f} x)"

    )

    return {

        "Model": "Exponential",
        "Equation": equation,
        "Parameters": params.tolist(),
        "Prediction": prediction,
        **metrics

    }


def fit_logarithmic(x, y):

    if np.any(x <= 0):

        return None

    params, prediction = safe_fit(

        logarithmic_model,

        x,

        y,

        p0=[1.0, 1.0]

    )

    if params is None:

        return None

    metrics = compute_metrics(

        y,

        prediction,

        2

    )

    equation = (

        f"y = {params[0]:.8f}"

        f" + {params[1]:.8f} ln(x)"

    )

    return {

        "Model": "Logarithmic",
        "Equation": equation,
        "Parameters": params.tolist(),
        "Prediction": prediction,
        **metrics

    }

# ============================================================
# ALL FITTERS
# ============================================================

FITTERS = [

    fit_linear,

    fit_quadratic,

    fit_power,

    fit_exponential,

    fit_logarithmic

]

# ============================================================
# MODEL QUALITY
# ============================================================

def classify_model(r2):

    if r2 >= 0.99:

        return "Excellent"

    if r2 >= 0.95:

        return "Strong"

    if r2 >= 0.85:

        return "Moderate"

    if r2 >= 0.70:

        return "Weak"

    return "Poor"

# ============================================================
# PAIR GENERATOR
# ============================================================

def generate_pairs(columns):

    return list(

        itertools.combinations(

            columns,

            2

        )

    )
  # ============================================================
# DISCOVER SCALING LAWS
# ============================================================

def discover_scaling_laws(df):

    print()

    print("Searching scaling laws...")

    all_models = []

    best_models = []

    pairwise = {}

    pairs = generate_pairs(

        df.columns

    )

    print(

        f"Observable pairs : {len(pairs)}"

    )

    # --------------------------------------------------------

    for index, (x_name, y_name) in enumerate(pairs):

        print(

            f"[{index+1:4d}/{len(pairs)}] "

            f"{x_name}  <->  {y_name}"

        )

        x = df[x_name].values.astype(float)

        y = df[y_name].values.astype(float)

        local_results = []

        for fitter in FITTERS:

            result = fitter(

                x,

                y

            )

            if result is None:

                continue

            result["X"] = x_name
            result["Y"] = y_name

            result["Quality"] = classify_model(

                result["R2"]

            )

            local_results.append(

                result

            )

            all_models.append(

                {

                    "X": x_name,

                    "Y": y_name,

                    "Model": result["Model"],

                    "Equation": result["Equation"],

                    "R2": result["R2"],

                    "RMSE": result["RMSE"],

                    "MAE": result["MAE"],

                    "AIC": result["AIC"],

                    "BIC": result["BIC"],

                    "Quality": result["Quality"]

                }

            )

        if len(local_results) == 0:

            continue

        best = max(

            local_results,

            key=lambda r: r["R2"]

        )

        best_models.append(

            {

                "X": x_name,

                "Y": y_name,

                "BestModel": best["Model"],

                "Equation": best["Equation"],

                "R2": best["R2"],

                "RMSE": best["RMSE"],

                "MAE": best["MAE"],

                "AIC": best["AIC"],

                "BIC": best["BIC"],

                "Quality": best["Quality"]

            }

        )

        pairwise[
            f"{x_name}__{y_name}"
        ] = {

            r["Model"]: {

                "Equation": r["Equation"],

                "R2": float(r["R2"]),

                "RMSE": float(r["RMSE"]),

                "MAE": float(r["MAE"]),

                "AIC": float(r["AIC"]),

                "BIC": float(r["BIC"]),

                "Quality": r["Quality"]

            }

            for r in local_results

        }

    all_df = pd.DataFrame(

        all_models

    )

    best_df = pd.DataFrame(

        best_models

    )

    all_df.to_csv(

        os.path.join(

            RESULTS,

            "all_models.csv"

        ),

        index=False

    )

    best_df.to_csv(

        os.path.join(

            RESULTS,

            "best_models.csv"

        ),

        index=False

    )

    with open(

        os.path.join(

            RESULTS,

            "pairwise_fits.json"

        ),

        "w"

    ) as f:

        json.dump(

            pairwise,

            f,

            indent=4

        )

    return all_df, best_df


# ============================================================
# LAW RANKING
# ============================================================

def build_ranking(best_models):

    ranking = best_models.sort_values(

        by=[

            "R2",

            "RMSE"

        ],

        ascending=[

            False,

            True

        ]

    )

    ranking.to_csv(

        os.path.join(

            RESULTS,

            "law_ranking.csv"

        ),

        index=False

    )

    return ranking


# ============================================================
# PLOT
# ============================================================

def plot_best_fit(

    x,

    y,

    prediction,

    xlabel,

    ylabel,

    model,

    filename

):

    plt.figure(

        figsize=(7,6)

    )

    order = np.argsort(x)

    plt.scatter(

        x,

        y,

        s=50

    )

    plt.plot(

        x[order],

        prediction[order],

        linewidth=2

    )

    plt.xlabel(

        xlabel

    )

    plt.ylabel(

        ylabel

    )

    plt.title(

        model

    )

    plt.tight_layout()

    plt.savefig(

        filename,

        dpi=300

    )

    plt.close()
  # ============================================================
# GENERATE FIGURES
# ============================================================

def generate_figures(

    df,

    ranking

):

    print()

    print("Generating scaling-law figures...")

    generated = 0

    for _, row in ranking.iterrows():

        if generated >= 25:

            break

        x_name = row["X"]
        y_name = row["Y"]
        model = row["BestModel"]

        x = df[x_name].values.astype(float)
        y = df[y_name].values.astype(float)

        try:

            if model == "Linear":

                p, prediction = safe_fit(

                    linear_model,

                    x,

                    y

                )

            elif model == "Quadratic":

                p, prediction = safe_fit(

                    quadratic_model,

                    x,

                    y

                )

            elif model == "Power":

                p, prediction = safe_fit(

                    power_model,

                    x,

                    y,

                    p0=[1.0,1.0]

                )

            elif model == "Exponential":

                p, prediction = safe_fit(

                    exponential_model,

                    x,

                    y,

                    p0=[1.0,0.01]

                )

            elif model == "Logarithmic":

                p, prediction = safe_fit(

                    logarithmic_model,

                    x,

                    y,

                    p0=[1.0,1.0]

                )

            else:

                continue

            if prediction is None:

                continue

            filename = os.path.join(

                PLOTS,

                f"{generated+1:03d}_{x_name}_{y_name}.png"

            )

            plot_best_fit(

                x,

                y,

                prediction,

                x_name,

                y_name,

                model,

                filename

            )

            generated += 1

        except Exception:

            continue

    print()

    print(f"Figures generated : {generated}")

# ============================================================
# SUMMARY
# ============================================================

def write_summary(

    ranking,

    all_models

):

    report = []

    report.append(
        "GER S29-E5.2"
    )

    report.append("")

    report.append(
        f"Observable pairs : {len(ranking)}"
    )

    report.append(
        f"Models evaluated : {len(all_models)}"
    )

    report.append("")

    report.append(
        "Top 20 Scaling Laws"
    )

    report.append("")

    top = ranking.head(20)

    for _, row in top.iterrows():

        report.append(
            f"{row['X']}  <->  {row['Y']}"
        )

        report.append(
            f"Model : {row['BestModel']}"
        )

        report.append(
            f"Equation : {row['Equation']}"
        )

        report.append(
            f"R2 : {row['R2']:.6f}"
        )

        report.append(
            f"RMSE : {row['RMSE']:.6f}"
        )

        report.append(
            f"MAE : {row['MAE']:.6f}"
        )

        report.append(
            f"Quality : {row['Quality']}"
        )

        report.append("")

    with open(

        os.path.join(

            RESULTS,

            "summary.txt"

        ),

        "w"

    ) as f:

        f.write(

            "\n".join(report)

        )

# ============================================================
# MAIN
# ============================================================

def main():

    header()

    dataframe = load_database()

    dataframe = clean_database(

        dataframe

    )

    all_models, best_models = discover_scaling_laws(

        dataframe

    )

    ranking = build_ranking(

        best_models

    )

    generate_figures(

        dataframe,

        ranking

    )

    write_summary(

        ranking,

        all_models

    )

    print()

    line()

    print("Scaling-law discovery completed.")

    print()

    print("Results saved to:")

    print(RESULTS)

    line()

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
