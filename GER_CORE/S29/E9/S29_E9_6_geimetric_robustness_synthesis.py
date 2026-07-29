"""
===============================================================================
S29_E9_6_GEOMETRIC_ROBUSTNESS_SYNTHESIS.py
===============================================================================

Síntese de Robustez Geométrica

Integra quantitativamente os resultados obtidos em:

E9.1  Manifold Reconstruction
E9.2  Local Manifold Atlas
E9.3  Multi-Scale Metric Reconstruction
E9.4  Curvature Field
E9.5  Discrete Connection

Produz um certificado global de robustez geométrica.

===============================================================================
"""

from __future__ import annotations

import json

from pathlib import Path

import pandas as pd


# =============================================================================
# CAMINHOS
# =============================================================================

BASE = Path("/content/drive/MyDrive/GER_RESULTS")

INPUT_E91 = (
    BASE
    / "S29"
    / "S29_E9_1_MANIFOLD_RECONSTRUCTION"
)

INPUT_E92 = (
    BASE
    / "S29"
    / "S29_E9_2_LOCAL_MANIFOLD_ATLAS"
)

INPUT_E93 = (
    BASE
    / "S29"
    / "S29_E9_3_MULTI_SCALE_METRIC_RECONSTRUCTION"
)

INPUT_E94 = (
    BASE
    / "S29"
    / "S29_E9_4_CURVATURE_FIELD"
)

INPUT_E95 = (
    BASE
    / "S29"
    / "S29_E9_5_DISCRETE_CONNECTION"
)

OUTPUT = (
    BASE
    / "S29"
    / "S29_E9_6_GEOMETRIC_ROBUSTNESS_SYNTHESIS"
)

OUTPUT.mkdir(
    parents=True,
    exist_ok=True
)


# =============================================================================
# AUDITORIA DAS ENTRADAS
# =============================================================================

def audit_inputs():

    print()
    print("=" * 80)
    print("INPUT AUDIT")
    print("=" * 80)

    required = {

        "E9.1":

            INPUT_E91 / "manifold_certificate.json",

        "E9.2":

            INPUT_E92 / "atlas_certificate.json",

        "E9.3":

            INPUT_E93 / "certificate.json",

        "E9.4":

            INPUT_E94 / "curvature_certificate.json",

        "E9.5":

            INPUT_E95 / "connection_certificate.json"

    }

    for experiment, path in required.items():

        if not path.exists():

            raise FileNotFoundError(path)

        print(f"{experiment:6s} ✓ {path.name}")

    print()

    print("All required certificates found.")


# =============================================================================
# CARREGAMENTO
# =============================================================================

def load_json(path):

    with open(

        path,

        encoding="utf-8"

    ) as f:

        return json.load(f)


def load_certificates():

    print()
    print("=" * 80)
    print("LOADING CERTIFICATES")
    print("=" * 80)

    certificates = {

        "E91":

            load_json(

                INPUT_E91
                /
                "manifold_certificate.json"

            ),

        "E92":

            load_json(

                INPUT_E92
                /
                "atlas_certificate.json"

            ),

        "E93":

            load_json(

                INPUT_E93
                /
                "certificate.json"

            ),

        "E94":

            load_json(

                INPUT_E94
                /
                "curvature_certificate.json"

            ),

        "E95":

            load_json(

                INPUT_E95
                /
                "connection_certificate.json"

            )

    }

    print()

    for key in certificates:

        print(

            f"{key} loaded."

        )

    return certificates


# =============================================================================
# CERTIFICATE VALIDATION
# =============================================================================

def validate_certificates(certificates):

    print()
    print("=" * 80)
    print("CERTIFICATE VALIDATION")
    print("=" * 80)

    e91 = certificates["E91"]
    e92 = certificates["E92"]
    e93 = certificates["E93"]
    e94 = certificates["E94"]

    checks = [

        {

            "check": "E9.1 vs E9.2 samples",

            "left": e91["trajectory_samples"],

            "right": e92["points"],

            "passed": (

                e91["trajectory_samples"]

                ==

                e92["points"]

            )

        },

        {

            "check": "E9.2 vs E9.4 points",

            "left": e92["points"],

            "right": e94["points"],

            "passed": (

                e92["points"]

                ==

                e94["points"]

            )

        },

        {

            "check": "E9.3 multiscale",

            "left": e93["samples"],

            "right": (

                e93["scales"]

                *

                e92["points"]

            ),

            "passed": (

                e93["samples"]

                ==

                e93["scales"]

                *

                e92["points"]

            )

        }

    ]

    checks = pd.DataFrame(checks)

    print()
    print(checks)

    if not checks["passed"].all():

        raise RuntimeError(

            "Input certificates are inconsistent."

        )

    print()
    print("All consistency checks passed.")

# =============================================================================
# ROBUSTNESS SUMMARY
# =============================================================================

def build_robustness_summary(certificates):

    print()
    print("=" * 80)
    print("ROBUSTNESS SUMMARY")
    print("=" * 80)

    e91 = certificates["E91"]
    e92 = certificates["E92"]
    e93 = certificates["E93"]
    e94 = certificates["E94"]
    e95 = certificates["E95"]

    summary = [

        {

            "component": "MANIFOLD",

            "experiment": "E9.1",

            "metric": "Embedding Score",

            "value": e91["score"]

        },

        {

            "component": "MANIFOLD",

            "experiment": "E9.1",

            "metric": "Distance Correlation",

            "value": e91["distance_correlation"]

        },

        {

            "component": "MANIFOLD",

            "experiment": "E9.1",

            "metric": "Neighbor Preservation",

            "value": e91["neighbor_preservation"]

        },

        {

            "component": "LOCAL_GEOMETRY",

            "experiment": "E9.2",

            "metric": "Mean Local Dimension",

            "value": e92["mean_local_dimension"]

        },

        {

            "component": "LOCAL_GEOMETRY",

            "experiment": "E9.2",

            "metric": "Mean Anisotropy",

            "value": e92["mean_anisotropy"]

        },

        {

            "component": "LOCAL_GEOMETRY",

            "experiment": "E9.2",

            "metric": "Mean Density",

            "value": e92["mean_density"]

        },

        {

            "component": "MULTISCALE",

            "experiment": "E9.3",

            "metric": "Mean Dimension",

            "value": e93["mean_dimension"]

        },

        {

            "component": "MULTISCALE",

            "experiment": "E9.3",

            "metric": "Mean Stability",

            "value": e93["mean_stability"]

        },

        {

            "component": "MULTISCALE",

            "experiment": "E9.3",

            "metric": "Orientation Change",

            "value": e93["mean_orientation_change_deg"]

        },

        {

            "component": "CURVATURE",

            "experiment": "E9.4",

            "metric": "Mean Curvature",

            "value": e94["mean_curvature"]

        },

        {

            "component": "CURVATURE",

            "experiment": "E9.4",

            "metric": "Singularity Fraction",

            "value": e94["singularity_fraction"]

        },

        {

            "component": "CURVATURE",

            "experiment": "E9.4",

            "metric": "Mean Gradient",

            "value": e94["mean_gradient"]

        },

        {

            "component": "CONNECTION",

            "experiment": "E9.5",

            "metric": "Mean Strength",

            "value": e95["statistics"]["mean_strength"]

        },

        {

            "component": "CONNECTION",

            "experiment": "E9.5",

            "metric": "Singularity Fraction",

            "value": e95["structure"]["singularity_fraction"]

        },

        {

            "component": "CONNECTION",

            "experiment": "E9.5",

            "metric": "Mean Gradient",

            "value": e95["consistency"]["mean_gradient"]

        }

    ]

    summary = pd.DataFrame(summary)

    print(summary)

    return summary


# =============================================================================
# COMPONENT OVERVIEW
# =============================================================================

def build_component_overview(summary):

    print()
    print("=" * 80)
    print("COMPONENT OVERVIEW")
    print("=" * 80)

    overview = (

        summary

        .groupby(

            "component"

        )

        .size()

        .reset_index(

            name="metrics"

        )

    )

    print()

    print(overview)

    return overview

# =============================================================================
# ROBUSTNESS SCORES
# =============================================================================

def build_robustness_scores(certificates):

    print()
    print("=" * 80)
    print("ROBUSTNESS SCORES")
    print("=" * 80)

    e91 = certificates["E91"]
    e92 = certificates["E92"]
    e93 = certificates["E93"]
    e94 = certificates["E94"]
    e95 = certificates["E95"]

    scores = [

        {

            "component":

                "MANIFOLD",

            "experiment":

                "E9.1",

            "score":

                float(

                    e91["score"]

                ),

            "status":

                "PASS"

                if e91["score"] >= 0.90

                else "WARNING"

        },

        {

            "component":

                "LOCAL_GEOMETRY",

            "experiment":

                "E9.2",

            "score":

                float(

                    e92["mean_anisotropy"]

                ),

            "status":

                "PASS"

                if e92["mean_anisotropy"] >= 0.90

                else "WARNING"

        },

        {

            "component":

                "MULTISCALE",

            "experiment":

                "E9.3",

            "score":

                float(

                    e93["mean_stability"]

                ),

            "status":

                "PASS"

                if e93["mean_stability"] >= 0.50

                else "WARNING"

        },

        {

            "component":

                "CURVATURE",

            "experiment":

                "E9.4",

            "score":

                float(

                    1.0

                    -

                    e94["singularity_fraction"]

                ),

            "status":

                "PASS"

                if e94["singularity_fraction"] <= 0.05

                else "WARNING"

        },

        {

            "component":

                "CONNECTION",

            "experiment":

                "E9.5",

            "score":

                float(

                    1.0

                    -

                    e95["structure"]["singularity_fraction"]

                ),

            "status":

                "PASS"

                if

                e95["structure"]["singularity_fraction"]

                <=

                0.05

                else

                "WARNING"

        }

    ]

    scores = pd.DataFrame(

        scores

    )

    print()

    print(scores)

    return scores


# =============================================================================
# GLOBAL ROBUSTNESS
# =============================================================================

def build_global_robustness(scores):

    print()
    print("=" * 80)
    print("GLOBAL ROBUSTNESS")
    print("=" * 80)

    global_score = float(

        scores["score"].mean()

    )

    passed = int(

        (scores["status"] == "PASS").sum()

    )

    robustness = {

        "components":

            len(scores),

        "passed":

            passed,

        "warnings":

            len(scores) - passed,

        "global_score":

            global_score

    }

    if global_score >= 0.90:

        robustness["classification"] = "VERY_HIGH"

    elif global_score >= 0.75:

        robustness["classification"] = "HIGH"

    elif global_score >= 0.50:

        robustness["classification"] = "MODERATE"

    else:

        robustness["classification"] = "LOW"

    print()

    for key, value in robustness.items():

        print(f"{key:20s}: {value}")

    return robustness

# =============================================================================
# CONSISTENCY MATRIX
# =============================================================================

def build_consistency_matrix(certificates):

    print()
    print("=" * 80)
    print("CONSISTENCY MATRIX")
    print("=" * 80)

    e91 = certificates["E91"]
    e92 = certificates["E92"]
    e93 = certificates["E93"]
    e94 = certificates["E94"]
    e95 = certificates["E95"]

    matrix = []

    # -------------------------------------------------------------------------
    # Dimensão
    # -------------------------------------------------------------------------

    dim_difference = abs(

        e92["mean_local_dimension"]

        -

        e93["mean_dimension"]

    )

    matrix.append({

        "comparison":

            "Dimension (E9.2 ↔ E9.3)",

        "metric":

            "dimension_difference",

        "value":

            float(dim_difference),

        "passed":

            dim_difference < 0.25

    })

    # -------------------------------------------------------------------------
    # Curvatura vs Conexão
    # -------------------------------------------------------------------------

    curvature_fraction = e94["singularity_fraction"]

    connection_fraction = (

        e95["structure"]["singularity_fraction"]

    )

    matrix.append({

        "comparison":

            "Curvature ↔ Connection",

        "metric":

            "singularity_fraction_difference",

        "value":

            float(

                abs(

                    curvature_fraction

                    -

                    connection_fraction

                )

            ),

        "passed":

            abs(

                curvature_fraction

                -

                connection_fraction

            ) < 0.05

    })

    # -------------------------------------------------------------------------
    # Estabilidade × Curvatura
    # -------------------------------------------------------------------------

    matrix.append({

        "comparison":

            "Metric Stability ↔ Curvature",

        "metric":

            "stable_metric",

        "value":

            float(

                e93["mean_stability"]

            ),

        "passed":

            e93["mean_stability"] >= 0.50

    })

    # -------------------------------------------------------------------------
    # Curvatura × Gradiente
    # -------------------------------------------------------------------------

    matrix.append({

        "comparison":

            "Curvature Gradient",

        "metric":

            "mean_gradient",

        "value":

            float(

                e94["mean_gradient"]

            ),

        "passed":

            e94["mean_gradient"] < 0.05

    })

    # -------------------------------------------------------------------------
    # Conexão × Gradiente
    # -------------------------------------------------------------------------

    matrix.append({

        "comparison":

            "Connection Gradient",

        "metric":

            "mean_gradient",

        "value":

            float(

                e95["consistency"]["mean_gradient"]

            ),

        "passed":

            e95["consistency"]["mean_gradient"] < 0.05

    })

    matrix = pd.DataFrame(

        matrix

    )

    print()

    print(matrix)

    return matrix


# =============================================================================
# GLOBAL CONSISTENCY
# =============================================================================

def evaluate_global_consistency(matrix):

    print()
    print("=" * 80)
    print("GLOBAL CONSISTENCY")
    print("=" * 80)

    passed = int(

        matrix["passed"].sum()

    )

    total = len(matrix)

    ratio = passed / total

    if ratio == 1.0:

        status = "CONSISTENT"

    elif ratio >= 0.80:

        status = "MOSTLY_CONSISTENT"

    else:

        status = "INCONSISTENT"

    consistency = {

        "tests":

            total,

        "passed":

            passed,

        "failed":

            total - passed,

        "consistency_ratio":

            ratio,

        "status":

            status

    }

    print()

    for key, value in consistency.items():

        print(

            f"{key:20s}: {value}"

        )

    return consistency

# =============================================================================
# EXPORT
# =============================================================================

def export_results(summary,
                   overview,
                   scores,
                   robustness,
                   consistency_matrix,
                   global_consistency):

    print()
    print("=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)

    summary.to_csv(
        OUTPUT / "robustness_summary.csv",
        index=False
    )

    overview.to_csv(
        OUTPUT / "component_overview.csv",
        index=False
    )

    scores.to_csv(
        OUTPUT / "robustness_scores.csv",
        index=False
    )

    consistency_matrix.to_csv(
        OUTPUT / "consistency_matrix.csv",
        index=False
    )

    certificate = {

        "robustness": robustness,

        "global_consistency": global_consistency,

        "scores": scores.to_dict(
            orient="records"
        )

    }

    with open(

        OUTPUT / "geometric_certificate.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            certificate,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("Export complete.")


# =============================================================================
# REPORT
# =============================================================================

def build_report(robustness,
                 global_consistency):

    lines = [

        "=" * 80,
        "S29 E9.6",
        "GEOMETRIC ROBUSTNESS SYNTHESIS",
        "=" * 80,
        "",

        f"Components               : {robustness['components']}",
        f"Passed                   : {robustness['passed']}",
        f"Warnings                 : {robustness['warnings']}",
        f"Global Score             : {robustness['global_score']:.6f}",
        f"Robustness               : {robustness['classification']}",
        "",

        f"Consistency Tests        : {global_consistency['tests']}",
        f"Passed                   : {global_consistency['passed']}",
        f"Failed                   : {global_consistency['failed']}",
        f"Consistency Ratio        : {global_consistency['consistency_ratio']:.6f}",
        f"Overall Consistency      : {global_consistency['status']}",
        "",

        "=" * 80,
        "END OF REPORT",
        "=" * 80

    ]

    report = "\n".join(lines)

    print()
    print(report)

    with open(

        OUTPUT / "report.txt",

        "w",

        encoding="utf-8"

    ) as f:

        f.write(report)


# =============================================================================
# MAIN
# =============================================================================

def main():

    print()
    print("=" * 80)
    print("S29 E9.6")
    print("GEOMETRIC ROBUSTNESS SYNTHESIS")
    print("=" * 80)

    audit_inputs()

    certificates = load_certificates()

    validate_certificates(
        certificates
    )

    summary = build_robustness_summary(
        certificates
    )

    overview = build_component_overview(
        summary
    )

    scores = build_robustness_scores(
        certificates
    )

    robustness = build_global_robustness(
        scores
    )

    consistency_matrix = build_consistency_matrix(
        certificates
    )

    global_consistency = evaluate_global_consistency(
        consistency_matrix
    )

    export_results(

        summary,

        overview,

        scores,

        robustness,

        consistency_matrix,

        global_consistency

    )

    build_report(

        robustness,

        global_consistency

    )

    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    main()
