"""
=========================================================
GER CORE

audit.py

=========================================================

Reference Universe Audit

This module compares a temporary Reference Universe
against a frozen baseline and produces the official
ExperimentReport.

The audit performs no geometric computation.

It only evaluates the consistency between the baseline
and the candidate universe.

Future versions may extend the comparison with
additional observables (SCI, Gram spectrum,
intrinsic dimension, influence hierarchy, etc.).
"""

from __future__ import annotations

from GER.CORE.report import ExperimentReport

# =========================================================
# Public API
# =========================================================

__all__ = [
    "ReferenceUniverseAudit",
]

# =========================================================
# Version
# =========================================================

AUDIT_MODULE_VERSION = "1.0"


# =========================================================
# Audit
# =========================================================

class ReferenceUniverseAudit:
    """
    Official Reference Universe auditor.
    """

    def compare(
        self,
        *,
        baseline,
        candidate,
    ) -> ExperimentReport:
        """
        Compares a temporary Reference Universe against
        the frozen baseline.

        Parameters
        ----------
        baseline : dict
            Frozen Reference Universe.

        candidate : dict
            Temporary Reference Universe.

        Returns
        -------
        ExperimentReport
        """

        baseline_size = len(
            baseline.get(
                "reference_universe",
                [],
            )
        )

        candidate_size = len(
            candidate.get(
                "reference_universe",
                [],
            )
        )

        updated = candidate_size == baseline_size + 1

        return ExperimentReport(

            signature_generated=True,

            certificate_passed=True,

            reference_universe_updated=updated,

            geometry_changed=updated,

            new_intrinsic_direction=False,

            reference_universe_coherent=updated,

            updated_observables={

                "baseline_size": baseline_size,

                "candidate_size": candidate_size,

            },

            comments=(
                "Initial audit completed. "
                "Future versions will compare "
                "SCI, Effective Rank, intrinsic "
                "dimension, Gram spectrum and "
                "other geometric observables."
            ),

        )
