"""
GER - Geometria Espectral Relacional
S29 - E7.4

Relational Identity

Compares two DynamicRegime objects and determines
whether they represent the same canonical object.

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

from dataclasses import dataclass

from GER_CORE.S29.E7.model import DynamicRegime


# ============================================================
# Result
# ============================================================

@dataclass
class IdentityComparison:

    left: str
    right: str

    configuration_match: bool

    signature_match: bool

    classification_match: bool

    audit_match: bool

    canonical_identity: bool


# ============================================================
# Analyzer
# ============================================================

class IdentityAnalyzer:

    @staticmethod
    def compare(
        regime_a: DynamicRegime,
        regime_b: DynamicRegime,
        left: str = "Object A",
        right: str = "Object B",
    ) -> IdentityComparison:

        configuration_match = (

            regime_a.configuration

            ==

            regime_b.configuration

        )

        signature_match = (

            regime_a.signature

            ==

            regime_b.signature

        )

        classification_match = (

            regime_a.classification

            ==

            regime_b.classification

        )

        audit_match = (

            regime_a.audit

            ==

            regime_b.audit

        )

        canonical_identity = (

            configuration_match

            and

            signature_match

        )

        return IdentityComparison(

            left=left,

            right=right,

            configuration_match=configuration_match,

            signature_match=signature_match,

            classification_match=classification_match,

            audit_match=audit_match,

            canonical_identity=canonical_identity,

        )
