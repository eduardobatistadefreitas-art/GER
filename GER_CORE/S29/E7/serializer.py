"""
============================================================
GER

S29 — E7

Dynamic Regime Serializer

============================================================

Converte objetos do modelo da E7 em estruturas
serializáveis (dict/JSON).

Este módulo não realiza gravação em disco.

============================================================
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Any

from .model import DynamicRegime


# ============================================================
# Dynamic Regime
# ============================================================

def dynamic_regime_to_dict(
    regime: DynamicRegime,
) -> Dict[str, Any]:
    """
    Converte um DynamicRegime em um dicionário.
    """

    return asdict(regime)


# ============================================================
# Configuration
# ============================================================

def configuration_to_dict(
    regime: DynamicRegime,
) -> Dict[str, Any]:
    """
    Retorna apenas a configuração.
    """

    return asdict(regime.configuration)


# ============================================================
# Signature
# ============================================================

def signature_to_dict(
    regime: DynamicRegime,
) -> Dict[str, Any]:
    """
    Retorna apenas a assinatura geométrica.
    """

    return asdict(regime.signature)


# ============================================================
# Classification
# ============================================================

def classification_to_dict(
    regime: DynamicRegime,
) -> Dict[str, Any]:
    """
    Retorna apenas a classificação.
    """

    return asdict(regime.classification)


# ============================================================
# Audit
# ============================================================

def audit_to_dict(
    regime: DynamicRegime,
) -> Dict[str, Any]:
    """
    Retorna apenas a auditoria.
    """

    return asdict(regime.audit)
