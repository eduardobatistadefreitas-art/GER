"""
============================================================
GER
S26-B36

Dynamic Regime Classifier

Pipeline oficial de classificação dinâmica.

Etapas

1) Engine
2) Persistence Observatory
3) Classifier Audit
4) Classifier Robustness
5) Save Results
============================================================
"""

from pprint import pprint

from GER.CORE.ger_engine import (
    run_engine,
)

from GER_CORE.S26.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

from GER_CORE.S26.S26_B36_1_classifier_audit import (
    run_classifier_audit,
)

from GER_CORE.S26.S26_B36_2_classifier_robustness import (
    run_classifier_robustness,
)

from GER_CORE.S26.OPERATORS.result_manager import (
    save_json,
)


# ============================================================
# Runner
# ============================================================

def run_B36_classifier():

    print()
    print("=" * 70)
    print("GER")
    print("S26-B36")
    print("Dynamic Regime Classifier")
    print("=" * 70)

    # --------------------------------------------------------
    # Engine
    # --------------------------------------------------------

    print()
    print("1) Running Engine...")

    engine = run_engine(
        beta=beta,
        sigma=sigma,
        potential=potential,
        timesteps=timesteps,
        dt=dt,
    )

    print("OK")

    # --------------------------------------------------------
    # Persistence Observatory
    # --------------------------------------------------------

    print()
    print("2) Running Persistence Observatory...")

    observables = run_persistence_observatory(
        snapshots
    )

    print("OK")

    # --------------------------------------------------------
    # Time Step
    # --------------------------------------------------------

    dt = 1.0

    # --------------------------------------------------------
    # Classifier Audit
    # --------------------------------------------------------

    print()
    print("3) Running Classifier Audit...")

    classification = run_classifier_audit(
        observables,
        dt,
    )

    print("OK")

    # --------------------------------------------------------
    # Classifier Robustness
    # --------------------------------------------------------

    print()
    print("4) Running Classifier Robustness...")

    robustness = run_classifier_robustness(
        observables,
        dt,
    )

    print("OK")

    # --------------------------------------------------------
    # Classification Report
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("Classification")
    print("=" * 70)

    print()

    print(
        "Regime              :",
        classification["regime"]
    )

    print(
        "Persistence Score   :",
        classification["persistence_score"]
    )

    print(
        "Persistence Variance:",
        classification["persistence_variance"]
    )

    print()

    print("Statistics")

    pprint(
        classification["statistics"]
    )

    # --------------------------------------------------------
    # Robustness Report
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("Robustness")
    print("=" * 70)

    print()

    print(
        "Regime Changes      :",
        robustness["regime_changes"]
    )

    print(
        "Persistence Mean    :",
        robustness["persistence_mean"]
    )

    print(
        "Persistence Std     :",
        robustness["persistence_std"]
    )

    print()

    print("Base")

    pprint(
        robustness["base"]
    )

    print()

    print("Epsilon Scan")

    for item in robustness["epsilon_scan"]:

        print(item)

    print()

    print("Window Scan")

    for item in robustness["window_scan"]:

        print(item)

    # --------------------------------------------------------
    # Build Result
    # --------------------------------------------------------

    result = {
        "configuration": {
            
            "beta": beta,
            "sigma": sigma,
            "potential": potential,
            "timesteps": timesteps,
            "dt": dt,
            
        },
        
        "classification": classification,
        
        "robustness": robustness,
        
    }

    # --------------------------------------------------------
    # Save Results
    # --------------------------------------------------------

    print()
    print("5) Saving Results...")

    save_json(
        "S26_B36_classifier",
        "classifier",
        result,
    )

    print("OK")

    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("Classifier Finished")
    print("=" * 70)

    return result


# ============================================================
# Main
# ============================================================

def main():

    run_B36_classifier()


if __name__ == "__main__":

    main()
