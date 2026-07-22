# ============================================================
# GER
# S26-B36
#
# Stationary Scan Audit
#
# Auditor oficial do operador Ψ.
#
# Este módulo NÃO modifica o Certificado Estrutural.
# Apenas verifica conformidade com a especificação.
# ============================================================

from GER_CORE.S26_B36_stationary_scan import (
    stationary_scan,
)


# ============================================================
# Assinatura padrão
# ============================================================

DEFAULT_SIGNATURE = {

    "diameter": 91.856401,

    "convergence": 9421.862182,

    "recurrence": 0.001282,

    "drift": 0.999926,

}


# ============================================================
# Utilitário
# ============================================================

def _audit(name, passed, details=""):

    return {

        "test": name,

        "status": "PASS" if passed else "FAIL",

        "details": details,

    }
  # ============================================================
# Auditoria Oficial
# ============================================================

def run_stationary_scan_audit(
    signature=DEFAULT_SIGNATURE,
):

    report = []

    certificate = stationary_scan(signature)

    # --------------------------------------------------------
    # Audit 01
    #
    # Estrutura do Certificado
    # --------------------------------------------------------

    expected = {

        "signature",

        "relations",

        "deductions",

        "consistency",

        "summary",

    }

    report.append(

        _audit(

            "CertificateStructure",

            set(certificate.keys()) == expected,

            str(certificate.keys()),

        )

    )

    # --------------------------------------------------------
    # Audit 02
    #
    # Número de relações
    # --------------------------------------------------------

    report.append(

        _audit(

            "RelationsCount",

            len(certificate["relations"]) == 6,

            f'{len(certificate["relations"])} relações',

        )

    )

    # --------------------------------------------------------
    # Audit 03
    #
    # Campos obrigatórios
    # --------------------------------------------------------

    required_fields = {

        "relation",

        "available",

        "eligible",

        "status",

        "evidence",

    }

    ok = True

    for relation in certificate["relations"]:

        if set(relation.keys()) != required_fields:

            ok = False

            break

    report.append(

        _audit(

            "RelationFields",

            ok,

        )

    )

    # --------------------------------------------------------
    # Audit 04
    #
    # Elegibilidade
    # --------------------------------------------------------

    eligible = sum(

        relation["eligible"]

        for relation in certificate["relations"]

    )

    report.append(

        _audit(

            "EligibilityOperator",

            eligible == 6,

            f"{eligible}/6",

        )

    )

    # --------------------------------------------------------
    # Audit 05
    #
    # Structural Operator
    # --------------------------------------------------------

    supported = sum(

        relation["status"] == "SUPPORTED"

        for relation in certificate["relations"]

    )

    report.append(

        _audit(

            "StructuralOperator",

            supported == 0,

            "Nenhuma Rule estrutural formal.",

        )

    )

    # --------------------------------------------------------
    # Audit 06
    #
    # Consistency Operator
    # --------------------------------------------------------

    report.append(

        _audit(

            "ConsistencyOperator",

            certificate["consistency"]["consistent"],

            str(certificate["consistency"]),

        )

    )

    # --------------------------------------------------------
    # Audit 07
    #
    # Reprodutibilidade
    # --------------------------------------------------------

    certificate2 = stationary_scan(signature)

    report.append(

        _audit(

            "Reproducibility",

            certificate == certificate2,

        )

    )

    return report
  # ============================================================
# Impressão
# ============================================================

def print_audit(report):

    print("=" * 60)

    print("S26-B36 STATIONARY SCAN AUDIT")

    print("=" * 60)

    print()

    passed = 0

    failed = 0

    for item in report:

        print(f"{item['test']:25s} : {item['status']}")

        if item["details"]:

            print(f"    {item['details']}")

        if item["status"] == "PASS":

            passed += 1

        else:

            failed += 1

    print()

    print("-" * 60)

    print("SUMMARY")

    print("-" * 60)

    print(f"PASS : {passed}")

    print(f"FAIL : {failed}")

    print()

    if failed == 0:

        print("RESULT : AUDIT APPROVED")

    else:

        print("RESULT : AUDIT FAILED")

    print()

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    report = run_stationary_scan_audit()

    print_audit(report)


# ============================================================

if __name__ == "__main__":

    main()
