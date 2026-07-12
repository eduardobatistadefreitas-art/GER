"""
=========================================================
GER CORE

Arquivo : ger_repository.py

Validação da infraestrutura do repositório GER.

Esta biblioteca verifica se a estrutura mínima do
framework está íntegra antes da inicialização do CORE.
=========================================================
"""

from pathlib import Path


def validate_repository(root=None):
    """
    Valida a estrutura mínima do repositório GER.

    Parameters
    ----------
    root : Path ou None
        Diretório raiz do repositório.
        Se None, detecta automaticamente.

    Returns
    -------
    bool
        True se a estrutura estiver íntegra.
    """

    if root is None:
        root = Path(__file__).resolve().parents[2]

    required = [
        "GER",
        "GER_CORE",
        "start_ger.py",
        "DOCS",
        "RESULTS",
    ]

    print("================================")
    print(" GER REPOSITORY VALIDATION")
    print("================================")

    ok = True

    for item in required:

        path = root / item

        if path.exists():
            print(f"[OK] {item}")
        else:
            print(f"[FAIL] {item}")
            ok = False

    print("================================")

    if ok:
        print(" REPOSITÓRIO VALIDADO")
    else:
        print(" REPOSITÓRIO INVÁLIDO")

    print("================================")

    return ok
