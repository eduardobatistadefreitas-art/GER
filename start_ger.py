"""
=========================================================
GER Environment Manager

Inicializador oficial do framework GER.

Responsabilidades:
- Preparar o ambiente.
- Inicializar o framework.
- Validar a instalação.

Não executa experimentos científicos.
=========================================================
"""

import os
import platform
import shutil
import subprocess


def banner():
    print("=" * 60)
    print("GER Environment Manager v1.0")
    print("=" * 60)
    print()


def check_environment():

    print("Checking environment...\n")

    # Python
    print(f"[OK] Python: {platform.python_version()}")

    # Git
    try:
        subprocess.run(
            ["git", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("[OK] Git detected")
    except Exception:
        raise RuntimeError("Git not found.")

    # Colab
    if "COLAB_RELEASE_TAG" in os.environ:
        print("[OK] Google Colab detected")
    else:
        print("[INFO] Google Colab not detected")

    print("\nEnvironment check passed.\n")


def main():

    banner()

    check_environment()


if __name__ == "__main__":
    main()
