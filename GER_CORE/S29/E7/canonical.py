"""
GER - Geometria Espectral Relacional
S29 - E7.3

Canonical Object Analysis

Determines which components belong to the
canonical definition of a DynamicRegime.

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from GER_CORE.S29.E7.model import DynamicRegime


# ============================================================
# Component
# ============================================================

@dataclass
class CanonicalComponent:

    name: str
    category: str
    required: bool
    reason: str


# ============================================================
# Analysis Result
# ============================================================

@dataclass
class CanonicalAnalysis:

    components: List[CanonicalComponent] = field(default_factory=list)

    core_components: int = 0
    derived_components: int = 0
    metadata_components: int = 0
    unknown_components: int = 0


# ============================================================
# Analyzer
# ============================================================

class CanonicalObjectAnalyzer:

    CORE = "CORE"
    DERIVED = "DERIVED"
    METADATA = "METADATA"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def analyze(
        cls,
        regime: DynamicRegime,
    ) -> CanonicalAnalysis:

        result = CanonicalAnalysis()

        result.components.append(

            CanonicalComponent(

                name="Configuration",

                category=cls.CORE,

                required=True,

                reason=(
                    "Defines the physical configuration "
                    "that generated the object."
                ),

            )

        )

        result.components.append(

            CanonicalComponent(

                name="Signature",

                category=cls.CORE,

                required=True,

                reason=(
                    "Encodes the intrinsic geometry "
                    "of the object."
                ),

            )

        )

        result.components.append(

            CanonicalComponent(

                name="Classification",

                category=cls.DERIVED,

                required=False,

                reason=(
                    "Represents an interpretation "
                    "of the object."
                ),

            )

        )

        result.components.append(

            CanonicalComponent(

                name="Audit",

                category=cls.METADATA,

                required=False,

                reason=(
                    "Stores provenance and "
                    "auxiliary observations."
                ),

            )

        )

        result.core_components = sum(

            c.category == cls.CORE

            for c in result.components

        )

        result.derived_components = sum(

            c.category == cls.DERIVED

            for c in result.components

        )

        result.metadata_components = sum(

            c.category == cls.METADATA

            for c in result.components

        )

        result.unknown_components = sum(

            c.category == cls.UNKNOWN

            for c in result.components

        )

        return result
