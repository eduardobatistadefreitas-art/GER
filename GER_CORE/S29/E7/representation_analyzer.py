"""
GER - Geometria Espectral Relacional
S29 - E7.5

Geometric Representation Analyzer

Evaluates candidate geometric representations for a
DynamicRegime.

The analyzer does not assume which representation is correct.
Each hypothesis is evaluated independently.

Author:
    Eduardo Batista de Freitas

Project:
    GER - Geometria Espectral Relacional
"""

from __future__ import annotations

from .model import DynamicRegime

from .representation import (
    RepresentationAnalysis,
    RepresentationEvidence,
    RepresentationType,
)


# ============================================================
# Analyzer
# ============================================================

class RepresentationAnalyzer:

    @classmethod
    def analyze(
        cls,
        regime: DynamicRegime,
    ) -> RepresentationAnalysis:

        analysis = RepresentationAnalysis()

        analysis.evidences.append(
            cls._analyze_point(
                regime
            )
        )

        analysis.evidences.append(
            cls._analyze_region(
                regime
            )
        )

        analysis.evidences.append(
            cls._analyze_trajectory(
                regime
            )
        )

        analysis.evidences.append(
            cls._analyze_set(
                regime
            )
        )

        analysis.evidences.append(
            cls._analyze_centroid(
                regime
            )
        )

        analysis.evidences.append(
            cls._analyze_manifold(
                regime
            )
        )

        supported = [

            evidence

            for evidence in analysis.evidences

            if evidence.supported

        ]

        if len(
            supported
        ) == 1:

            analysis.recommended = (
                supported[0].hypothesis
            )

        else:

            analysis.recommended = (
                RepresentationType.UNKNOWN
            )

        analysis.completed = True

        return analysis

    # ========================================================
    # H1
    # ========================================================

    @staticmethod
    def _analyze_point(
        regime: DynamicRegime,
    ) -> RepresentationEvidence:

        return RepresentationEvidence(

            hypothesis=RepresentationType.POINT,

            supported=False,

            confidence=0.0,

            reason=(
                "Not evaluated."
            ),

        )

    # ========================================================
    # H2
    # ========================================================

    @staticmethod
    def _analyze_region(
        regime: DynamicRegime,
    ) -> RepresentationEvidence:

        return RepresentationEvidence(

            hypothesis=RepresentationType.REGION,

            supported=False,

            confidence=0.0,

            reason=(
                "Not evaluated."
            ),

        )

    # ========================================================
    # H3
    # ========================================================

    @staticmethod
    def _analyze_trajectory(
        regime: DynamicRegime,
    ) -> RepresentationEvidence:

        return RepresentationEvidence(

            hypothesis=RepresentationType.TRAJECTORY,

            supported=False,

            confidence=0.0,

            reason=(
                "Not evaluated."
            ),

        )

    # ========================================================
    # H4
    # ========================================================

    @staticmethod
    def _analyze_set(
        regime: DynamicRegime,
    ) -> RepresentationEvidence:

        return RepresentationEvidence(

            hypothesis=RepresentationType.SET,

            supported=False,

            confidence=0.0,

            reason=(
                "Not evaluated."
            ),

        )

    # ========================================================
    # H5
    # ========================================================

    @staticmethod
    def _analyze_centroid(
        regime: DynamicRegime,
    ) -> RepresentationEvidence:

        return RepresentationEvidence(

            hypothesis=RepresentationType.CENTROID,

            supported=False,

            confidence=0.0,

            reason=(
                "Not evaluated."
            ),

        )

    # ========================================================
    # H6
    # ========================================================

    @staticmethod
    def _analyze_manifold(
        regime: DynamicRegime,
    ) -> RepresentationEvidence:

        return RepresentationEvidence(

            hypothesis=RepresentationType.MANIFOLD,

            supported=False,

            confidence=0.0,

            reason=(
                "Not evaluated."
            ),

        )
