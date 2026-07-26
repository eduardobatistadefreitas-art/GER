"""
============================================================
GER
S26

run_B36.py

Official execution pipeline for the S26-B36 experiments.

Pipeline

run_engine
        ↓
run_persistence_observatory
        ↓
run_stationary_scan
        ↓
run_classifier_audit
        ↓
run_classifier_robustness

All results are automatically stored in Google Drive.

============================================================
"""

from __future__ import annotations

import traceback

from GER.CORE.ger_engine import run_engine

from GER_CORE.S26_B35_persistence_observatory import (
    run_persistence_observatory,
)

from GER_CORE.S26_B36_stationary_scan import (
    run_stationary_scan,
)

from GER_CORE.S26_B36_1_classifier_audit import (
    run_classifier_audit,
)

from GER_CORE.S26_B36_2_classifier_robustness import (
    run_classifier_robustness,
)

from GER_CORE.S26.OPERATORS.result_manager import (
    save_json,
)


# ============================================================
# Configuration
# ============================================================

DEFAULT_CONFIG = dict(

    n=384,
    timesteps=2000,
    dt=2.5e-4,
    beta=1.0,
    potential="A",
    snapshot_stride=50,
    sigma=0.10,

)


# ============================================================
# Runner
# ============================================================

def run_B36(**engine_kwargs):

    config = DEFAULT_CONFIG.copy()
    config.update(engine_kwargs)

    print("=" * 60)
    print("GER")
    print("S26-B36")
    print("Official Runner")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Engine
    # --------------------------------------------------------

    print("[1/5] Running Engine...")

    engine = run_engine(**config)

    snapshots = engine["snapshots"]

    dt = config["dt"]

    # --------------------------------------------------------
    # Persistence Observatory
    # --------------------------------------------------------

    print("[2/5] Persistence Observatory...")

    observables = run_persistence_observatory(
        snapshots,
        dt,
    )

    save_json(
        "S26_B36",
        "observables",
        observables,
    )

    results = {

        "engine": engine,
        "observables": observables,

    }

    # --------------------------------------------------------
    # Stationary Scan
    # --------------------------------------------------------

    print("[3/5] Stationary Scan...")

    try:

        stationary = run_stationary_scan(
            observables,
            dt,
        )

        results["stationary_scan"] = stationary

    except Exception as exc:

        print("Stationary Scan failed.")
        print(exc)

        results["stationary_scan"] = {

            "error": str(exc)

        }

    # --------------------------------------------------------
    # Classifier Audit
    # --------------------------------------------------------

    print("[4/5] Classifier Audit...")

    try:

        audit = run_classifier_audit(
            observables,
            dt,
        )

        results["classifier_audit"] = audit

    except Exception as exc:

        print("Classifier Audit failed.")
        print(exc)

        results["classifier_audit"] = {

            "error": str(exc)

        }

    # --------------------------------------------------------
    # Robustness
    # --------------------------------------------------------

    print("[5/5] Classifier Robustness...")

    try:

        robustness = run_classifier_robustness(
            observables,
            dt,
        )

        results["classifier_robustness"] = robustness

    except Exception as exc:

        print("Classifier Robustness failed.")
        print(exc)

        results["classifier_robustness"] = {

            "error": str(exc)

        }

    # --------------------------------------------------------
    # Final Report
    # --------------------------------------------------------

    save_json(
        "S26_B36",
        "full_report",
        results,
    )

    print()
    print("=" * 60)
    print("S26-B36 FINISHED")
    print("=" * 60)

    return results


# ============================================================
# Main
# ============================================================

def main():

    try:

        run_B36()

    except Exception:

        print()

        print("=" * 60)
        print("FATAL ERROR")
        print("=" * 60)

        traceback.print_exc()

        raise


if __name__ == "__main__":
    main()
