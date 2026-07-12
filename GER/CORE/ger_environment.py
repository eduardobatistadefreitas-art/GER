"""
=========================================================
GER CORE

Arquivo : ger_environment.py

Validação do ambiente de execução do GER.
=========================================================
"""

import platform
import shutil


def validate_environment():
    """
    Valida o ambiente necessário para execução do GER.
    """

    print("Checking environment...\n")

    # Python
    print(f"[OK] Python: {platform.python_version()}")

    # Git
    if shutil.which("git"):
        print("[OK] Git detected")
    else:
        print("[FAIL] Git not found")
        return False

    # Google Colab
    try:
        import google.colab
        print("[OK] Google Colab detected")
    except ImportError:
        print("[INFO] Running outside Google Colab")

    print("\nEnvironment check passed.")

    return True
