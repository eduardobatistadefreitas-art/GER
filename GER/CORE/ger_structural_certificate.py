"""
=========================================================
GER CORE

ger_structural_certificate.py

=========================================================

Official Structural Certificate (Ψ Operator)

The implementation is independent of any experimental
series (S26, S27, S28, ...).

Only permanent structural logic belongs here.
"""

from __future__ import annotations

import math
from dataclasses import asdict

# =========================================================
# Public API
# =========================================================

__all__ = [
    "structural_certificate",
]

# =========================================================
# Version
# =========================================================

STRUCTURAL_CERTIFICATE_VERSION = "1.0"

# =========================================================
# Fundamental Geometric Operators
# =========================================================

OGF_KEYS = (
    "diameter",
    "convergence",
    "recurrence",
    "drift",
)


# =========================================================
# Fundamental Relations
# =========================================================

RELATIONS = (
    ("diameter", "convergence"),
    ("diameter", "recurrence"),
    ("diameter", "drift"),
    ("convergence", "recurrence"),
    ("convergence", "drift"),
    ("recurrence", "drift"),
)


# =========================================================
# Utilities
# =========================================================

def _make_deduction(
    rule,
    status,
    evidence,
    justification,
):

    return {

        "rule": rule,

        "status": status,

        "evidence": evidence,

        "justification": justification,

    }


# =========================================================
# Signature conversion
# =========================================================

def _signature_to_dict(signature):

    if hasattr(signature, "__dataclass_fields__"):
        return asdict(signature)

    return dict(signature)


# =========================================================
# Relations
# =========================================================

def build_relations(signature):

    relations = []

    for left, right in RELATIONS:

        relations.append({

            "relation": f"{left}↔{right}",

            "available": (

                left in signature and
                right in signature

            ),

            "eligible": False,

            "status": "UNANALYZED",

            "evidence": [],

        })

    return relations


# =========================================================
# Certificate construction
# =========================================================

def create_certificate(signature):

    return {

        "signature": signature,

        "relations": build_relations(signature),

        "deductions": [],

        "consistency": {},

        "summary": {

            "passed": 0,

            "failed": 0,

        },

    }


# =========================================================
# Signature validation
# =========================================================

def validate_signature(signature):

    if not isinstance(signature, dict):

        return False

    for key in OGF_KEYS:

        if key not in signature:

            return False

        value = signature[key]

        if value is None:

            return False

        try:

            value = float(value)

        except Exception:

            return False

        if not math.isfinite(value):

            return False

    return True


# =========================================================
# Evidence
# =========================================================

def add_relation_evidence(

    relation,

    rule,

    status,

    justification,

    data=None,

):

    if data is None:

        data = {}

    relation["status"] = status

    relation["evidence"].append({

        "rule": rule,

        "status": status,

        "justification": justification,

        "data": data,

    })


# =========================================================
# Eligibility Operator
# =========================================================

def run_eligibility_operator(certificate):

    signature = certificate["signature"]

    valid = validate_signature(signature)

    certificate["deductions"].append(

        _make_deduction(

            rule="SignatureIntegrity",

            status="PASS" if valid else "FAIL",

            evidence={

                "available_keys": list(signature.keys())

            },

            justification=(

                "The Geometric Signature is valid."

                if valid

                else

                "The Geometric Signature is invalid."

            ),

        )

    )

    if not valid:

        return

    for relation in certificate["relations"]:

        if relation["available"]:

            relation["eligible"] = True

            add_relation_evidence(

                relation,

                rule="StructuralAvailability",

                status="ELIGIBLE",

                justification=(

                    "Relation eligible for structural deduction."

                ),

            )


# =========================================================
# Structural Operator
# =========================================================

def run_structural_operator(certificate):
    """
    Reserved for future structural rules.

    According to the current RSG theory,
    no structural deductions have been
    formally established using only the
    Geometric Signature.

    Therefore this operator intentionally
    performs no deductions.
    """

    return


# =========================================================
# Consistency Operator
# =========================================================

def run_consistency_operator(certificate):

    relations = certificate["relations"]

    eligible = sum(

        relation["eligible"]

        for relation in relations

    )

    supported = sum(

        relation["status"] == "SUPPORTED"

        for relation in relations

    )

    certificate["consistency"] = {

        "eligible_relations": eligible,

        "supported_relations": supported,

        "structural_rules": 0,

        "consistent": True,

    }

    certificate["deductions"].append(

        _make_deduction(

            rule="ConsistencyCheck",

            status="PASS",

            evidence=dict(

                certificate["consistency"]

            ),

            justification=(

                "The Structural Certificate is "
                "consistent with the current "
                "state of the OGF theory."

            ),

        )

    )


# =========================================================
# Deduction Engine
# =========================================================

def run_deduction_engine(certificate):

    run_eligibility_operator(

        certificate

    )

    run_structural_operator(

        certificate

    )

    run_consistency_operator(

        certificate

    )


# =========================================================
# Public API
# =========================================================

def structural_certificate(signature):
    """
    Generates the official Structural Certificate
    from a Geometric Signature.

    Parameters
    ----------
    signature :
        Signature dataclass or dictionary.

    Returns
    -------
    dict
        Structural Certificate.
    """

    signature = _signature_to_dict(signature)

    certificate = create_certificate(signature)

    run_deduction_engine(certificate)

    summary = certificate["summary"]

    for deduction in certificate["deductions"]:

        if deduction["status"] == "PASS":

            summary["passed"] += 1

        else:

            summary["failed"] += 1

    return certificate
