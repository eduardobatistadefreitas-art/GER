import math

# ============================================================
# GER
# S26-B36
#
# Stationary Scan
#
# MVP v0.1
#
# Implementação mínima do operador Ψ
#
# Entrada:
#     Assinatura Geométrica
#
# Saída:
#     Certificado Estrutural
#
# Este módulo NÃO classifica regimes.
# ============================================================


OGF_KEYS = [
    "diameter",
    "convergence",
    "recurrence",
    "drift",
]


# ============================================================
# Utilidades
# ============================================================

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


# ============================================================
# Validação básica
# ============================================================

def validate_signature(signature):

    if not isinstance(signature, dict):
        return False

    for key in OGF_KEYS:

        if key not in signature:
            return False

        value = signature[key]

        if value is None:
            return False

        if not math.isfinite(float(value)):
            return False

    return True


# ============================================================
# Rule 001
#
# Signature Integrity
# ============================================================

def rule_signature_integrity(signature):

    ok = validate_signature(signature)

    return _make_deduction(

        rule="SignatureIntegrity",

        status="PASS" if ok else "FAIL",

        evidence={
            "available_keys": list(signature.keys())
        },

        justification=(
            "Todos os Operadores Geométricos "
            "Fundamentais estão presentes "
            "e possuem valores finitos."
            if ok
            else
            "Assinatura inválida."
        ),

    )


# ============================================================
# Rule 002
#
# OGF Compliance
# ============================================================

def rule_ogf_compliance(signature):

    ok = set(signature.keys()) >= set(OGF_KEYS)

    return _make_deduction(

        rule="OGFCompliance",

        status="PASS" if ok else "FAIL",

        evidence={
            "required": OGF_KEYS,
        },

        justification=(
            "A assinatura contém os quatro "
            "Operadores Geométricos Fundamentais."
            if ok
            else
            "Assinatura incompatível com o OGF."
        ),

    )
    # ============================================================
# Rule 003
#
# Structural Validity
# ============================================================

def rule_structural_validity(signature):

    if not validate_signature(signature):

        return _make_deduction(

            rule="StructuralValidity",

            status="FAIL",

            evidence={},

            justification=(
                "A assinatura não pode ser utilizada "
                "pelo Stationary Scan."
            ),

        )

    evidence = {

        "diameter": signature["diameter"],

        "convergence": signature["convergence"],

        "recurrence": signature["recurrence"],

        "drift": signature["drift"],

    }

    return _make_deduction(

        rule="StructuralValidity",

        status="PASS",

        evidence=evidence,

        justification=(
            "A assinatura é estruturalmente válida "
            "para aplicação do operador Ψ."
        ),

    )


# ============================================================
# Stationary Scan
# ============================================================

def stationary_scan(signature):

    certificate = {

        "signature": dict(signature),

        "deductions": [],

        "summary": {

            "passed": 0,

            "failed": 0,

        }

    }

    rules = [

        rule_signature_integrity,

        rule_ogf_compliance,

        rule_structural_validity,

    ]

    for rule in rules:

        deduction = rule(signature)

        certificate["deductions"].append(deduction)

        if deduction["status"] == "PASS":

            certificate["summary"]["passed"] += 1

        else:

            certificate["summary"]["failed"] += 1

    return certificate


# ============================================================
# Impressão
# ============================================================

def print_certificate(certificate):

    print("=" * 60)

    print("STRUCTURAL CERTIFICATE")

    print("=" * 60)

    print()

    print("Geometry Signature")

    for key, value in certificate["signature"].items():

        print(f"  {key:15s}: {value}")

    print()

    print("-" * 60)

    print("Deductions")

    print("-" * 60)

    print()

    for d in certificate["deductions"]:

        print(f"Rule          : {d['rule']}")

        print(f"Status        : {d['status']}")

        print(f"Evidence      : {d['evidence']}")

        print(f"Justification : {d['justification']}")

        print("-" * 60)

    s = certificate["summary"]

    print()

    print("Summary")

    print(f"  PASS : {s['passed']}")

    print(f"  FAIL : {s['failed']}")

    print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    signature = {

        "diameter": 91.856401,

        "convergence": 9421.862182,

        "recurrence": 0.001282,

        "drift": 0.999926,

    }

    certificate = stationary_scan(signature)

    print_certificate(certificate)


# ============================================================

if __name__ == "__main__":

    main()
