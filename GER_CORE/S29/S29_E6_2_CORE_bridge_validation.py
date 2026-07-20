"""
============================================================
GER
S29

E6.2

CORE Bridge Validation
============================================================

Objective
---------
Validate the complete official CORE pipeline.

    run_engine()
            ↓
       snapshots
            ↓
run_persistence_observatory()
            ↓
      observables
            ↓
run_signature_pipeline()
            ↓
 Signature + Certificate

This experiment performs no scientific discovery.

Its sole purpose is validating that the public
interfaces of the GER CORE are correctly connected.

Author
------
GER Project
"""

from __future__ import annotations

import os
import json
import traceback
from pathlib import Path

import numpy as np

from IPython.display import clear_output

# ============================================================
# CORE Bootstrap
# ============================================================

from GER.CORE.bootstrap import initialize

# ============================================================
# Numerical Engine
# ============================================================

from GER.CORE.ger_engine import run_engine

# ============================================================
# Signature Pipeline
# ============================================================

from GER.CORE.experiment_pipeline import (
    run_signature_pipeline,
)

# ============================================================
# B35 Observatory
# ============================================================

from GER_CORE.S26_B35_persistence_metrics import (
    run_persistence_observatory,
)

# ============================================================
# Configuration
# ============================================================

OUTPUT_DIRECTORY = Path(
    "RESULTS/S29_E6_2_CORE_bridge_validation"
)

OUTPUT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

ENGINE_CONFIGURATION = dict(

    n=384,

    timesteps=2000,

    dt=2.5e-4,

    beta=1.0,

    potential="A",

    snapshot_stride=50,

    sigma=0.10,

)

# ============================================================
# Dashboard
# ============================================================

class Dashboard:

    def __init__(self):

        self.stage = ""

    def show(self):

        clear_output(wait=True)

        print("=" * 60)
        print("GER")
        print("S29-E6.2")
        print("CORE Bridge Validation")
        print("=" * 60)
        print()

        print(f"Stage : {self.stage}")

        print()

# ============================================================
# Validator
# ============================================================

class COREBridgeValidator:

    def __init__(self):

        self.dashboard = Dashboard()

        initialize()

    # --------------------------------------------------------

    def _stage(self, text):

        self.dashboard.stage = text
        self.dashboard.show()

    # --------------------------------------------------------

    def execute_engine(self):

        self._stage("Running official GER engine")

        result = run_engine(
            **ENGINE_CONFIGURATION
        )

        if not isinstance(result, dict):

            raise RuntimeError(
                "run_engine() did not return a dictionary."
            )

        return result

    # --------------------------------------------------------

    @staticmethod
    def validate_engine_output(result):

        required = [

            "configuration",

            "initial",

            "final",

            "snapshots",

            "gamma",

            "laplacian",

            "eigenvalues",

            "eigenvectors",

            "diverged",

        ]

        missing = [

            key
            for key in required
            if key not in result
        ]

        if missing:

            raise RuntimeError(

                "Engine output missing keys:\n"

                + "\n".join(missing)

            )

        return True

    # --------------------------------------------------------

    @staticmethod
    def validate_snapshots(result):

        snapshots = result["snapshots"]

        if len(snapshots) == 0:

            raise RuntimeError(
                "No snapshots produced."
            )

        first = snapshots[0]

        required = [

            "gamma",

            "probability",

            "participation_ratio",

            "modal_center",

        ]

        missing = [

            key
            for key in required
            if key not in first
        ]

        if missing:

            raise RuntimeError(

                "Snapshot missing:\n"

                + "\n".join(missing)

            )

        return snapshots
          # --------------------------------------------------------

    def execute_observatory(
        self,
        snapshots,
    ):

        self._stage(
            "Running Persistence Observatory"
        )

        dt = ENGINE_CONFIGURATION["dt"]

        observables = (
            run_persistence_observatory(
                snapshots,
                dt,
            )
        )

        return observables

    # --------------------------------------------------------

    @staticmethod
    def validate_observables(
        observables,
    ):

        required = [

            "Rloc",

            "Dspec",

            "Hshape",

            "Cauto",

            "Rmacro",

            "entropy",

        ]

        missing = [

            key
            for key in required
            if key not in observables
        ]

        if missing:

            raise RuntimeError(

                "Observatory missing:\n"

                + "\n".join(missing)

            )

        lengths = {

            key: len(observables[key])

            for key in required

        }

        expected = next(
            iter(lengths.values())
        )

        for key, value in lengths.items():

            if value != expected:

                raise RuntimeError(

                    "Observable lengths differ:\n"

                    f"{lengths}"

                )

        return True

    # --------------------------------------------------------

    def execute_signature_pipeline(
        self,
        observables,
    ):

        self._stage(
            "Running Signature Pipeline"
        )

        dt = ENGINE_CONFIGURATION["dt"]

        result = run_signature_pipeline(
            observables,
            dt,
        )

        if not isinstance(result, dict):

            raise RuntimeError(
                "Pipeline returned invalid object."
            )

        if "signature" not in result:

            raise RuntimeError(
                "Signature missing."
            )

        if "certificate" not in result:

            raise RuntimeError(
                "Certificate missing."
            )

        return result

    # --------------------------------------------------------

    @staticmethod
    def validate_signature(
        signature,
    ):

        fields = [

            "diameter",

            "convergence",

            "recurrence",

            "drift",

        ]

        signature_dict = signature.to_dict()

        missing = [

            key

            for key in fields

            if key not in signature_dict

        ]

        if missing:

            raise RuntimeError(

                "Signature incomplete:\n"

                + "\n".join(missing)

            )

        return signature_dict

    # --------------------------------------------------------

    @staticmethod
    def validate_certificate(
        certificate,
    ):

        if "summary" not in certificate:

            raise RuntimeError(
                "Certificate summary missing."
            )

        summary = certificate["summary"]

        if "passed" not in summary:

            raise RuntimeError(
                "Certificate missing PASS count."
            )

        if "failed" not in summary:

            raise RuntimeError(
                "Certificate missing FAIL count."
            )

        return summary

    # --------------------------------------------------------

    @staticmethod
    def save_results(
        engine,
        observables,
        signature,
        certificate,
    ):

        signature_dict = (
            signature.to_dict()
        )

        with open(

            OUTPUT_DIRECTORY /
            "signature.json",

            "w",

            encoding="utf-8",

        ) as fp:

            json.dump(

                signature_dict,

                fp,

                indent=4,

            )

        with open(

            OUTPUT_DIRECTORY /
            "certificate.json",

            "w",

            encoding="utf-8",

        ) as fp:

            json.dump(

                certificate,

                fp,

                indent=4,

            )

        with open(

            OUTPUT_DIRECTORY /
            "observables.json",

            "w",

            encoding="utf-8",

        ) as fp:

            json.dump(

                {

                    k: list(
                        np.asarray(v)
                    )

                    for k, v in observables.items()

                },

                fp,

                indent=4,

            )

        with open(

            OUTPUT_DIRECTORY /
            "engine_summary.json",

            "w",

            encoding="utf-8",

        ) as fp:

            json.dump(

                {

                    "configuration":
                        engine["configuration"],

                    "initial":
                        engine["initial"],

                    "final":
                        engine["final"],

                    "diverged":
                        engine["diverged"],

                    "snapshots":
                        len(engine["snapshots"]),

                },

                fp,

                indent=4,

          )
              # --------------------------------------------------------

    def run(self):

        self._stage(
            "Executing official CORE pipeline"
        )

        engine = self.execute_engine()

        self.validate_engine_output(
            engine
        )

        snapshots = self.validate_snapshots(
            engine
        )

        observables = self.execute_observatory(
            snapshots
        )

        self.validate_observables(
            observables
        )

        pipeline = self.execute_signature_pipeline(
            observables
        )

        signature = pipeline["signature"]

        certificate = pipeline["certificate"]

        signature_dict = self.validate_signature(
            signature
        )

        summary = self.validate_certificate(
            certificate
        )

        self.save_results(

            engine,

            observables,

            signature,

            certificate,

        )

        self._stage(
            "Validation completed"
        )

        print()
        print("=" * 60)
        print("CORE BRIDGE VALIDATION")
        print("=" * 60)
        print()

        print("Engine")
        print("-" * 60)
        print(
            f"Snapshots : {len(snapshots)}"
        )
        print(
            f"Diverged : {engine['diverged']}"
        )

        print()
        print("Observatory")
        print("-" * 60)

        for key in [

            "Rloc",

            "Dspec",

            "Hshape",

            "Cauto",

            "Rmacro",

            "entropy",

        ]:

            print(
                f"{key:12s}: "
                f"{len(observables[key])}"
            )

        print()
        print("Signature")
        print("-" * 60)

        for key, value in signature_dict.items():

            print(
                f"{key:15s}: "
                f"{value:.12f}"
            )

        print()
        print("Certificate")
        print("-" * 60)

        print(
            f"Passed : {summary['passed']}"
        )

        print(
            f"Failed : {summary['failed']}"
        )

        print()

        print(
            "Results saved to:"
        )

        print(
            OUTPUT_DIRECTORY
        )

        print()
        print("=" * 60)
        print("STATUS : PASS")
        print("=" * 60)

        return {

            "engine": engine,

            "observables": observables,

            "signature": signature,

            "certificate": certificate,

        }


# ============================================================
# Main
# ============================================================

def main():

    try:

        validator = COREBridgeValidator()

        validator.run()

    except Exception:

        print()

        print("=" * 60)
        print("STATUS : FAIL")
        print("=" * 60)

        print()

        traceback.print_exc()

        raise


# ============================================================

if __name__ == "__main__":

    main()
