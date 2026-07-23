# ============================================================
# GER
#
# S27-E6
#
# Signature Geometry Map
#
# Exploratory analysis of the geometric space formed
# by the external Geometric Signatures generated during
# the S27-R validation campaign.
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from itertools import combinations


# ============================================================
# Reference Signatures
# ============================================================

SIGNATURES = {

    "Harmonic": {
        "diameter": 1.9921147013144778,
        "convergence": 0.08300477922143658,
        "recurrence": 0.022108843537414966,
    },

    "Damped": {
        "diameter": 1.9998041350423283,
        "convergence": 0.6184311298641284,
        "recurrence": 0.027210884353741496,
    },

    "Van der Pol": {
        "diameter": 1.5608913946393885,
        "convergence": 0.2914078484866824,
        "recurrence": 0.03571428571428571,
    },

    "Logistic": {
        "diameter": 0.010716857466728347,
        "convergence": 0.003313136757680963,
        "recurrence": 1.0,
    },

    "Lorenz": {
        "diameter": 0.4193130263391729,
        "convergence": 0.07938585810719678,
        "recurrence": 0.1377551020408163,
    },

    "Double Pendulum": {
        "diameter": 1.3014988554324796,
        "convergence": 0.38899464593629496,
        "recurrence": 0.06972789115646258,
    }

}


# ============================================================
# DataFrame
# ============================================================

def build_dataframe():

    rows = []

    for name, sig in SIGNATURES.items():

        rows.append({

            "System": name,

            "Diameter": sig["diameter"],

            "Convergence": sig["convergence"],

            "Recurrence": sig["recurrence"],

        })

    return pd.DataFrame(rows)


# ============================================================
# Signature vectors
# ============================================================

def signature_vector(name):

    s = SIGNATURES[name]

    return np.array([

        s["diameter"],

        s["convergence"],

        s["recurrence"]

    ])


# ============================================================
# Euclidean distance
# ============================================================

def distance(a, b):

    return np.linalg.norm(

        signature_vector(a)

        -

        signature_vector(b)

    )


# ============================================================
# Distance Matrix
# ============================================================

def build_distance_matrix():

    names = list(SIGNATURES.keys())

    matrix = np.zeros((len(names), len(names)))

    for i, a in enumerate(names):

        for j, b in enumerate(names):

            matrix[i, j] = distance(a, b)

    return pd.DataFrame(

        matrix,

        index=names,

        columns=names,

    )


# ============================================================
# Nearest Neighbour
# ============================================================

def nearest_neighbors():

    names = list(SIGNATURES.keys())

    results = {}

    for a in names:

        best = None

        best_distance = np.inf

        for b in names:

            if a == b:

                continue

            d = distance(a, b)

            if d < best_distance:

                best_distance = d

                best = b

        results[a] = (best, best_distance)

    return results


# ============================================================
# Automatic Summary
# ============================================================

def automatic_summary():

    names = list(SIGNATURES.keys())

    distances = []

    duplicated = False

    for a, b in combinations(names, 2):

        d = distance(a, b)

        distances.append(d)

        if np.isclose(d, 0):

            duplicated = True

    print()

    print("=" * 60)

    print("Automatic Summary")

    print("=" * 60)

    print()

    print(f"Number of signatures : {len(names)}")

    print(f"Minimum distance     : {min(distances):.6f}")

    print(f"Maximum distance     : {max(distances):.6f}")

    print(f"Mean distance        : {np.mean(distances):.6f}")

    print()

    if duplicated:

        print("Duplicated signatures detected.")

    else:

        print("No duplicated signatures detected.")

    print()

    print("Nearest neighbours")

    print("-" * 60)

    for system, (neighbor, d) in nearest_neighbors().items():

        print(

            f"{system:<20}"

            f"{neighbor:<20}"

            f"{d:.6f}"

  )
      # ============================================================
# Table
# ============================================================

def print_table():

    print("=" * 60)
    print("Reference Signatures")
    print("=" * 60)
    print()

    df = build_dataframe()

    print(df.to_string(index=False))

    print()


# ============================================================
# Distance Matrix
# ============================================================

def print_distance_matrix():

    print("=" * 60)
    print("Euclidean Distance Matrix")
    print("=" * 60)
    print()

    matrix = build_distance_matrix()

    print(matrix.round(6))

    print()


# ============================================================
# Plot utilities
# ============================================================

def save_figure(name):

    plt.tight_layout()

    plt.savefig(

        f"RESULTS/{name}.png",

        dpi=300,

        bbox_inches="tight",

    )

    plt.close()


# ============================================================
# Diameter × Convergence
# ============================================================

def plot_diameter_convergence():

    plt.figure(figsize=(7,6))

    for name, s in SIGNATURES.items():

        plt.scatter(

            s["diameter"],

            s["convergence"],

            s=80,

        )

        plt.text(

            s["diameter"],

            s["convergence"],

            " "+name,

            fontsize=9,

        )

    plt.xlabel("Diameter")

    plt.ylabel("Convergence")

    plt.title("Signature Geometry Map\n(Diameter × Convergence)")

    plt.grid(True)

    save_figure("S27_E6_Diameter_Convergence")


# ============================================================
# Diameter × Recurrence
# ============================================================

def plot_diameter_recurrence():

    plt.figure(figsize=(7,6))

    for name, s in SIGNATURES.items():

        plt.scatter(

            s["diameter"],

            s["recurrence"],

            s=80,

        )

        plt.text(

            s["diameter"],

            s["recurrence"],

            " "+name,

            fontsize=9,

        )

    plt.xlabel("Diameter")

    plt.ylabel("Recurrence")

    plt.title("Signature Geometry Map\n(Diameter × Recurrence)")

    plt.grid(True)

    save_figure("S27_E6_Diameter_Recurrence")


# ============================================================
# Convergence × Recurrence
# ============================================================

def plot_convergence_recurrence():

    plt.figure(figsize=(7,6))

    for name, s in SIGNATURES.items():

        plt.scatter(

            s["convergence"],

            s["recurrence"],

            s=80,

        )

        plt.text(

            s["convergence"],

            s["recurrence"],

            " "+name,

            fontsize=9,

        )

    plt.xlabel("Convergence")

    plt.ylabel("Recurrence")

    plt.title("Signature Geometry Map\n(Convergence × Recurrence)")

    plt.grid(True)

    save_figure("S27_E6_Convergence_Recurrence")


# ============================================================
# 3D Geometry
# ============================================================

def plot_signature_space():

    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(8,7))

    ax = fig.add_subplot(
        111,
        projection="3d"
    )

    for name, s in SIGNATURES.items():

        ax.scatter(

            s["diameter"],

            s["convergence"],

            s["recurrence"],

            s=80,

        )

        ax.text(

            s["diameter"],

            s["convergence"],

            s["recurrence"],

            name,

            fontsize=8,

        )

    ax.set_xlabel("Diameter")

    ax.set_ylabel("Convergence")

    ax.set_zlabel("Recurrence")

    ax.set_title("GER Signature Space")

    plt.tight_layout()

    plt.savefig(

        "RESULTS/S27_E6_Signature_Space_3D.png",

        dpi=300,

        bbox_inches="tight",

    )

    plt.close()


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("GER")
    print("S27-E6")
    print("Signature Geometry Map")
    print("=" * 60)
    print()

    print_table()

    print_distance_matrix()

    plot_diameter_convergence()

    plot_diameter_recurrence()

    plot_convergence_recurrence()

    plot_signature_space()

    automatic_summary()

    print()

    print("=" * 60)
    print("Generated figures")
    print("=" * 60)
    print()

    print("RESULTS/S27_E6_Diameter_Convergence.png")
    print("RESULTS/S27_E6_Diameter_Recurrence.png")
    print("RESULTS/S27_E6_Convergence_Recurrence.png")
    print("RESULTS/S27_E6_Signature_Space_3D.png")

    print()

    print("=" * 60)
    print("STATUS : SIGNATURE SPACE GENERATED")
    print("=" * 60)


if __name__ == "__main__":

    main()
