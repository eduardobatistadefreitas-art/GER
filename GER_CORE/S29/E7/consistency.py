"""
============================================================
GER

S29 — E7.2

Structural Consistency

============================================================

Consistency analysis for DynamicRegime.

This module performs structural validation of the
canonical DynamicRegime representation.

It does not explain inconsistencies.
It only detects and reports them.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import DynamicRegime


# ============================================================
# Data structures
# ============================================================

@dataclass(frozen=True)
class StructuralConflict:

    field: str

    primary_value: object

    secondary_value: object

    description: str


@dataclass(frozen=True)
class StructuralWarning:

    field: str

    description: str


@dataclass
class ConsistencyResult:

    passed: bool = True

    conflicts: list[StructuralConflict] = field(
        default_factory=list
    )

    warnings: list[StructuralWarning] = field(
        default_factory=list
    )

    checked_fields: int = 0


# ============================================================
# Analyzer
# ============================================================

class StructuralConsistencyAnalyzer:

    """
    Analyze the internal consistency of a DynamicRegime.
    """

    @staticmethod
    def analyze(
        regime: DynamicRegime,
    ) -> ConsistencyResult:

        result = ConsistencyResult()

        # ----------------------------------------------------
        # Classification consistency
        # ----------------------------------------------------

        result.checked_fields += 1

        primary = regime.classification.regime

        secondary = regime.audit.data.get(
            "regime"
        )

        if (
            secondary is not None
            and
            primary != secondary
        ):

            result.passed = False

            result.conflicts.append(

                StructuralConflict(

                    field="classification.regime",

                    primary_value=primary,

                    secondary_value=secondary,

                    description=(
                        "Primary classification "
                        "differs from audit "
                        "classification."
                    ),

                )

            )

        # ----------------------------------------------------
        # Persistence score
        # ----------------------------------------------------

        result.checked_fields += 1

        p1 = regime.classification.persistence_score

        p2 = regime.audit.data.get(
            "persistence_score"
        )

        if p2 is not None:

            delta = abs(p1 - p2)

            if delta > 0.001:

                result.warnings.append(

                    StructuralWarning(

                        field="persistence_score",

                        description=(
                            f"Difference detected "
                            f"({delta:.6f})."
                        ),

                    )

                )

        # ----------------------------------------------------
        # Persistence variance
        # ----------------------------------------------------

        result.checked_fields += 1

        v1 = regime.classification.persistence_variance

        v2 = regime.audit.data.get(
            "persistence_variance"
        )

        if v2 is not None:

            delta = abs(v1 - v2)

            if delta > 1e-5:

                result.warnings.append(

                    StructuralWarning(

                        field="persistence_variance",

                        description=(
                            f"Difference detected "
                            f"({delta:.6e})."
                        ),

                    )

                )

        return result
