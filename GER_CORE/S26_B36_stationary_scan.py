import math

# ============================================================
# GER
# S26-B36
#
# Stationary Scan
#
# Versão: 0.3
#
# Implementação oficial do operador Ψ.
#
# O módulo transforma uma Assinatura Geométrica em um
# Certificado Estrutural através de operadores dedutivos.
#
# O módulo NÃO realiza classificação.
# ============================================================


# ============================================================
# Operadores Geométricos Fundamentais
# ============================================================

OGF_KEYS = [

    "diameter",

    "convergence",

    "recurrence",

    "drift",

]


# ============================================================
# Relações Fundamentais
# ============================================================

RELATIONS = [

    ("diameter", "convergence"),

    ("diameter", "recurrence"),

    ("diameter", "drift"),

    ("convergence", "recurrence"),

    ("convergence", "drift"),

    ("recurrence", "drift"),

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
# Construção das Relações
# ============================================================

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


# ============================================================
# Construção do Certificado
# ============================================================

def create_certificate(signature):

    return {

        "signature": dict(signature),

        "relations": build_relations(signature),

        "deductions": [],

        "consistency": {},

        "summary": {

            "passed": 0,

            "failed": 0,

        },

    }


# ============================================================
# Validação da Assinatura
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
# Registro de Evidências
# ============================================================

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


# ============================================================
# Eligibility Operator
# ============================================================

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

                "A assinatura geométrica é válida."

                if valid

                else

                "A assinatura geométrica é inválida."

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

                    "A relação é elegível para dedução "
                    "estrutural."

                ),

            )
            # ============================================================
# Structural Operator
# ============================================================

def run_structural_operator(certificate):
    """
    Structural Operator.

    Reserved for future structural deductions.

    According to the current B35 theory,
    no structural deduction has been
    formally established using only the
    Geometry Signature.

    Therefore this operator intentionally
    leaves the Structural Certificate
    unchanged.
    """
    return


# ============================================================
# Consistency Operator
# ============================================================


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

    #
    # No estado atual da teoria,
    # nenhuma Rule estrutural foi
    # oficialmente estabelecida.
    #
    # Portanto, relações elegíveis
    # sem suporte estrutural NÃO
    # representam inconsistência.
    #

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

                "O Certificado Estrutural é "
                "consistente com o estado "
                "atual da teoria do OGF. "
                "Nenhuma Rule estrutural "
                "foi formalmente estabelecida."

            ),

        )

    )


# ============================================================
# Deduction Engine
# ============================================================

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
    # ============================================================
# Stationary Scan
# ============================================================

def stationary_scan(signature):

    certificate = create_certificate(signature)

    run_deduction_engine(certificate)

    summary = certificate["summary"]

    for deduction in certificate["deductions"]:

        if deduction["status"] == "PASS":

            summary["passed"] += 1

        else:

            summary["failed"] += 1

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

    print("Relations")

    print("-" * 60)

    print()

    for relation in certificate["relations"]:

        print(

            f"{relation['relation']:28s}"

            f"{relation['status']}"

        )

        if relation["evidence"]:

            for evidence in relation["evidence"]:

                print(

                    f"    -> {evidence['rule']}"

                    f" ({evidence['status']})"

                )

    print()

    print("-" * 60)

    print("Deductions")

    print("-" * 60)

    print()

    for deduction in certificate["deductions"]:

        print(f"Rule          : {deduction['rule']}")

        print(f"Status        : {deduction['status']}")

        print(f"Evidence      : {deduction['evidence']}")

        print(f"Justification : {deduction['justification']}")

        print("-" * 60)

    print()

    print("Consistency")

    for key, value in certificate["consistency"].items():

        print(f"  {key:22s}: {value}")

    print()

    summary = certificate["summary"]

    print("Summary")

    print(f"  PASS : {summary['passed']}")

    print(f"  FAIL : {summary['failed']}")

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
