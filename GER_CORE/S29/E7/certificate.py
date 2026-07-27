"""
GER - Geometria Espectral Relacional
S29 - E7

certificate.py

DynamicRegime Structural Certificate.

This module generates the canonical structural certificate
for a DynamicRegime.

The certificate is a pure Python dictionary and contains
no file I/O.

Author:
    Eduardo Batista de Freitas
"""

from __future__ import annotations

import math

from .model import DynamicRegime


# =============================================================================
# Helpers
# =============================================================================

def _is_finite(value) -> bool:
    """
    Return True if value is a finite number.
    """

    if not isinstance(value, (int, float)):
        return False

    return math.isfinite(value)


# =============================================================================
# Integrity
# =============================================================================

def _integrity_checks(
    regime: DynamicRegime,
) -> dict:
    """
    Execute structural integrity checks.
    """

    checks = {

        "configuration_exists":
            regime.configuration is not None,

        "signature_exists":
            regime.signature is not None,

        "classification_exists":
            regime.classification is not None,

        "audit_exists":
            regime.audit is not None,

        "positive_dt":
            regime.configuration.dt > 0,

        "positive_timesteps":
            regime.configuration.timesteps > 0,

        "finite_diameter":
            _is_finite(regime.signature.diameter),

        "finite_convergence":
            _is_finite(regime.signature.convergence),

        "finite_recurrence":
            _is_finite(regime.signature.recurrence),

        "finite_drift":
            _is_finite(regime.signature.drift),

        "finite_persistence_score":
            _is_finite(
                regime.classification.persistence_score
            ),

        "finite_persistence_variance":
            _is_finite(
                regime.classification.persistence_variance
            ),

    }

    passed = all(checks.values())

    return {

        "passed": passed,

        "checks": checks,

    }


# =============================================================================
# Public API
# =============================================================================

def generate_certificate(
    regime: DynamicRegime,
) -> dict:
    """
    Generate the canonical DynamicRegime certificate.
    """

    integrity = _integrity_checks(regime)

    certificate = {

        "configuration": {

            "beta":
                regime.configuration.beta,

            "sigma":
                regime.configuration.sigma,

            "potential":
                regime.configuration.potential,

            "timesteps":
                regime.configuration.timesteps,

            "dt":
                regime.configuration.dt,

        },

        "signature": {

            "diameter":
                regime.signature.diameter,

            "convergence":
                regime.signature.convergence,

            "recurrence":
                regime.signature.recurrence,

            "drift":
                regime.signature.drift,

        },

        "classification": {

            "regime":
                regime.classification.regime,

            "persistence_score":
                regime.classification.persistence_score,

            "persistence_variance":
                regime.classification.persistence_variance,

        },

        "audit":
            regime.audit.data
            if regime.audit is not None
            else None,

        "integrity":
            integrity,

    }

    return certificate
