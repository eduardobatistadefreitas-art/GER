"""
======================================================================
GER
S29-E5.3
Massive Geometric Law Validation
======================================================================

Scientific objective
--------------------

Validate the empirical scaling laws discovered in E5.2 through
massive statistical resampling.

Unlike E5.2, this experiment is NOT intended to discover laws.

Its purpose is to estimate:

    • robustness
    • reproducibility
    • parameter stability
    • model-selection stability

The experiment is fully restartable.

If Colab disconnects,
running this file again automatically resumes from the last checkpoint.

======================================================================
"""

import os
import json
import time
import random
import warnings

import numpy as np
import pandas as pd

from pathlib import Path

from scipy.optimize import curve_fit

warnings.filterwarnings("ignore")

# ============================================================
# CONFIGURATION
# ============================================================

BOOTSTRAP_ITERATIONS = 500000

CHECKPOINT_EVERY = 1000

RANDOM_SEED = 12345

np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# ------------------------------------------------------------
# STORAGE
# ------------------------------------------------------------

DRIVE_ROOT = Path(
    "/content/drive/MyDrive"
)

if not DRIVE_ROOT.exists():

    raise RuntimeError(

        "\nGoogle Drive is not mounted.\n\n"
        "Massive experiments are not allowed to run "
        "without persistent storage."

    )

print("[OK] Google Drive detected.")

BASE = (
    DRIVE_ROOT /
    "GER_RESULTS" /
    "S29_E5.3"
)

OUTPUT = BASE / "massive_validation"

OUTPUT.mkdir(

    parents=True,

    exist_ok=True

)

CHECKPOINT = OUTPUT / "checkpoint.json"

RESULTS_FILE = OUTPUT / "bootstrap_results.jsonl"

SUMMARY_FILE = OUTPUT / "summary.txt"

print(f"[OK] Output directory : {OUTPUT}")

# ============================================================
# LOAD DATABASE
# ============================================================
print("=" * 70)
print("GER")
print("S29-E5.3")
print("Massive Geometric Law Validation")
print("=" * 70)

table = pd.read_csv(BASE / "correlation_table.csv")

# ------------------------------------------------------------
# remove constants
# ------------------------------------------------------------

valid_columns = []

for c in table.columns:

    if np.issubdtype(table[c].dtype, np.number):

        if table[c].nunique() > 1:

            valid_columns.append(c)

table = table[valid_columns]

print()
print("Observables :", len(valid_columns))
print("Regions     :", len(table))
print()

# ============================================================
# MODEL DEFINITIONS
# ============================================================

def linear(x, a, b):
    return a * x + b


def quadratic(x, a, b, c):
    return a * x ** 2 + b * x + c


def power(x, a, b):
    return a * np.power(x, b)


def exponential(x, a, b):
    return a * np.exp(b * x)


def logarithmic(x, a, b):
    return a * np.log(x) + b


MODELS = {
    "Linear": linear,
    "Quadratic": quadratic,
    "Power": power,
    "Exponential": exponential,
    "Logarithmic": logarithmic,
}

# ============================================================
# METRICS
# ============================================================

def metrics(y, yp):

    rss = np.sum((y - yp) ** 2)

    tss = np.sum((y - np.mean(y)) ** 2)

    if tss == 0:
        r2 = 0

    else:
        r2 = 1 - rss / tss

    rmse = np.sqrt(np.mean((y - yp) ** 2))

    mae = np.mean(np.abs(y - yp))

    return r2, rmse, mae


# ============================================================
# SAFE FIT
# ============================================================

def safe_fit(model, x, y):

    try:

        if model == "Power":

            if np.any(x <= 0):
                return None

        if model == "Logarithmic":

            if np.any(x <= 0):
                return None

        popt, _ = curve_fit(

            MODELS[model],
            x,
            y,
            maxfev=10000

        )

        yp = MODELS[model](x, *popt)

        r2, rmse, mae = metrics(y, yp)

        return {

            "model": model,

            "params": popt.tolist(),

            "r2": float(r2),

            "rmse": float(rmse),

            "mae": float(mae)

        }

    except Exception:

        return None
      # ============================================================
# PAIR GENERATION
# ============================================================

pairs = []

columns = list(table.columns)

for i in range(len(columns)):
    for j in range(i + 1, len(columns)):
        pairs.append((columns[i], columns[j]))

print("Observable pairs :", len(pairs))
print()

# ============================================================
# CHECKPOINT
# ============================================================

if CHECKPOINT.exists():

    with open(CHECKPOINT, "r") as f:
        checkpoint = json.load(f)

    completed = set(tuple(x) for x in checkpoint["completed"])

    print("Checkpoint detected.")
    print("Completed pairs :", len(completed))

else:

    checkpoint = {
        "completed": []
    }

    completed = set()

# ============================================================
# RESULT WRITER
# ============================================================

def append_result(record):

    with open(RESULTS_FILE, "a") as f:

        json.dump(record, f)

        f.write("\n")


# ============================================================
# BOOTSTRAP
# ============================================================

def bootstrap_pair(x, y):

    n = len(x)

    winners = {
        m: 0
        for m in MODELS
    }

    parameter_history = {
        m: []
        for m in MODELS
    }

    r2_history = {
        m: []
        for m in MODELS
    }

    rmse_history = {
        m: []
        for m in MODELS
    }

    mae_history = {
        m: []
        for m in MODELS
    }

    start = time.time()

    for iteration in range(BOOTSTRAP_ITERATIONS):

        idx = np.random.randint(0, n, n)

        xb = x[idx]

        yb = y[idx]

        best_model = None

        best_r2 = -1e9

        for model in MODELS:

            result = safe_fit(model, xb, yb)

            if result is None:
                continue

            parameter_history[model].append(result["params"])

            r2_history[model].append(result["r2"])

            rmse_history[model].append(result["rmse"])

            mae_history[model].append(result["mae"])

            if result["r2"] > best_r2:

                best_r2 = result["r2"]

                best_model = model

        if best_model is not None:

            winners[best_model] += 1

        # ----------------------------------------------------
        # periodic checkpoint
        # ----------------------------------------------------

        if (iteration + 1) % CHECKPOINT_EVERY == 0:

            elapsed = time.time() - start

            rate = (iteration + 1) / elapsed

            remaining = (
                BOOTSTRAP_ITERATIONS
                - iteration
                - 1
            ) / rate

            print(
                f"    {iteration+1:,}/{BOOTSTRAP_ITERATIONS:,}   "
                f"{rate:.1f} it/s   "
                f"ETA {remaining/3600:.2f} h"
            )

    return {

        "winner_frequency": winners,

        "parameters": parameter_history,

        "r2": r2_history,

        "rmse": rmse_history,

        "mae": mae_history

    }


# ============================================================
# PARAMETER STATISTICS
# ============================================================

def parameter_statistics(history):

    stats = {}

    for model, values in history.items():

        if len(values) == 0:
            continue

        arr = np.array(values)

        model_stats = []

        for k in range(arr.shape[1]):

            p = arr[:, k]

            model_stats.append({

                "mean": float(np.mean(p)),
                "std": float(np.std(p)),
                "median": float(np.median(p)),
                "q025": float(np.quantile(p, 0.025)),
                "q975": float(np.quantile(p, 0.975))

            })

        stats[model] = model_stats

    return stats


# ============================================================
# METRIC STATISTICS
# ============================================================

def metric_statistics(history):

    stats = {}

    for model, values in history.items():

        if len(values) == 0:
            continue

        arr = np.array(values)

        stats[model] = {

            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "median": float(np.median(arr)),
            "q025": float(np.quantile(arr, 0.025)),
            "q975": float(np.quantile(arr, 0.975))

        }

    return stats
  # ============================================================
# MAIN LOOP
# ============================================================

summary = []

total_pairs = len(pairs)

for pair_index, (x_name, y_name) in enumerate(pairs, start=1):

    if (x_name, y_name) in completed:

        print(
            f"[{pair_index:2d}/{total_pairs}] "
            f"{x_name} <-> {y_name}   (already processed)"
        )

        continue

    print()
    print("=" * 70)
    print(
        f"[{pair_index:2d}/{total_pairs}] "
        f"{x_name}  <->  {y_name}"
    )
    print("=" * 70)

    x = table[x_name].values.astype(float)
    y = table[y_name].values.astype(float)

    result = bootstrap_pair(x, y)

    parameter_stats = parameter_statistics(
        result["parameters"]
    )

    r2_stats = metric_statistics(
        result["r2"]
    )

    rmse_stats = metric_statistics(
        result["rmse"]
    )

    mae_stats = metric_statistics(
        result["mae"]
    )

    winner = max(
        result["winner_frequency"],
        key=result["winner_frequency"].get
    )

    probability = (
        result["winner_frequency"][winner]
        / BOOTSTRAP_ITERATIONS
    )

    record = {

        "X": x_name,

        "Y": y_name,

        "bootstrap_iterations": BOOTSTRAP_ITERATIONS,

        "winner_frequency": result["winner_frequency"],

        "winner_model": winner,

        "winner_probability": probability,

        "parameter_statistics": parameter_stats,

        "r2_statistics": r2_stats,

        "rmse_statistics": rmse_stats,

        "mae_statistics": mae_stats

    }

    append_result(record)

    summary.append({

        "X": x_name,

        "Y": y_name,

        "Winner": winner,

        "Probability": probability

    })

    checkpoint["completed"].append(
        [x_name, y_name]
    )

    with open(CHECKPOINT, "w") as f:

        json.dump(
            checkpoint,
            f,
            indent=4
        )

# ============================================================
# FINAL SUMMARY
# ============================================================

summary_df = pd.DataFrame(summary)

if len(summary_df):

    summary_df = summary_df.sort_values(
        "Probability",
        ascending=False
    )

summary_df.to_csv(

    OUTPUT / "winner_probability.csv",

    index=False

)

# ============================================================
# HUMAN REPORT
# ============================================================

with open(SUMMARY_FILE, "w") as f:

    f.write(
        "GER S29-E5.3\n"
    )

    f.write(
        "Massive Geometric Law Validation\n\n"
    )

    f.write(
        f"Bootstrap iterations : "
        f"{BOOTSTRAP_ITERATIONS:,}\n"
    )

    f.write(
        f"Observable pairs      : "
        f"{len(pairs)}\n\n"
    )

    f.write(
        "Model Stability Ranking\n\n"
    )

    if len(summary_df):

        for _, row in summary_df.iterrows():

            f.write(
                f"{row.X}"
                "  <->  "
                f"{row.Y}\n"
            )

            f.write(
                f"Winner : "
                f"{row.Winner}\n"
            )

            f.write(
                f"Selection Probability : "
                f"{100*row.Probability:.3f}%\n\n"
            )

print()
print("=" * 70)
print("Massive validation finished.")
print("=" * 70)
print()

print("Results")

print(" ", OUTPUT / "bootstrap_results.jsonl")
print(" ", OUTPUT / "winner_probability.csv")
print(" ", OUTPUT / "summary.txt")

print()
print("Experiment completed.")

# ============================================================
# END
# ============================================================
