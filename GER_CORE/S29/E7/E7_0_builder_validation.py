"""
GER - Geometria Espectral Relacional
S29 - E7.0.1

DynamicRegimeBuilder Validation

Objective
---------
Validate the complete E7 infrastructure by building a
DynamicRegime from real S26 outputs.

This is an infrastructure validation only.
No scientific analysis is performed.

Author:
    Eduardo Batista de Freitas
"""

from pathlib import Path

from GER_CORE.S29.E7.E7_builder import DynamicRegimeBuilder


# =============================================================================
# Configuration
# =============================================================================

RESULTS_ROOT = Path("/content/drive/MyDrive/GER_RESULTS/S26")

STATIONARY_SCAN = (
    RESULTS_ROOT
    / "S26_B36_stationary_scan"
)

CLASSIFIER = (
    RESULTS_ROOT
    / "S26_B36_classifier"
)

CLASSIFIER_AUDIT = (
    RESULTS_ROOT
    / "S26_B36_1_classifier_audit"
)


# =============================================================================
# Helpers
# =============================================================================

def latest_json(folder: Path, filename: str) -> Path:

    runs = sorted(
        [
            p
            for p in folder.iterdir()
            if p.is_dir()
        ]
    )

    if not runs:
        raise RuntimeError(
            f"No executions found in {folder}"
        )

    return runs[-1] / filename


# =============================================================================
# Main
# =============================================================================

def main():

    print("=" * 80)
    print("GER")
    print("S29-E7.0.1")
    print("DynamicRegimeBuilder Validation")
    print("=" * 80)
    print()

    stationary_scan = latest_json(
        STATIONARY_SCAN,
        "stationary_scan.json",
    )

    classifier = latest_json(
        CLASSIFIER,
        "classifier.json",
    )

    classifier_audit = latest_json(
        CLASSIFIER_AUDIT,
        "classifier_audit.json",
    )

    print("Loading")
    print("-" * 80)

    print(f"✓ {stationary_scan}")
    print(f"✓ {classifier}")
    print(f"✓ {classifier_audit}")
    print()

    print("Building DynamicRegime...")
    print()

    regime = DynamicRegimeBuilder.build(
        stationary_scan_path=stationary_scan,
        classifier_path=classifier,
        classifier_audit_path=classifier_audit,
    )

    print("=" * 80)
    print("DynamicRegime Summary")
    print("=" * 80)
    print()

    print("Configuration")
    print("-" * 80)

    print(f"beta        : {regime.configuration.beta}")
    print(f"sigma       : {regime.configuration.sigma}")
    print(f"potential   : {regime.configuration.potential}")
    print(f"timesteps   : {regime.configuration.timesteps}")
    print(f"dt          : {regime.configuration.dt}")

    print()

    print("Signature")
    print("-" * 80)

    print(f"diameter       : {regime.signature.diameter}")
    print(f"convergence    : {regime.signature.convergence}")
    print(f"recurrence     : {regime.signature.recurrence}")
    print(f"drift          : {regime.signature.drift}")

    print()

    print("Classification")
    print("-" * 80)

    print(f"regime                 : {regime.classification.regime}")
    print(
        f"persistence_score      : "
        f"{regime.classification.persistence_score}"
    )
    print(
        f"persistence_variance   : "
        f"{regime.classification.persistence_variance}"
    )

    print()

    print("Audit")
    print("-" * 80)

    print(
        f"loaded : {regime.audit is not None}"
    )

    print()

    print("=" * 80)
    print("RESULT")
    print("=" * 80)

    print()
    print("DynamicRegime successfully created.")
    print("Infrastructure validation PASSED.")
    print()


# =============================================================================

if __name__ == "__main__":
    main()
