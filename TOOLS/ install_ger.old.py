#!/usr/bin/env python3
"""
=========================================================
GER Framework

Official Repository Installer

Instala ou sincroniza automaticamente o
repositório oficial do GER.

=========================================================
"""

from pathlib import Path
import subprocess
import shutil
import sys


# ==========================================================
# Configuração
# ==========================================================

REPOSITORY_URL = "https://github.com/eduardobatistadefreitas-art/GER.git"

INSTALL_ROOT = Path("/content")

REPOSITORY_NAME = "GER"


# ==========================================================
# Utilitário
# ==========================================================

def run(command):

    subprocess.run(command, check=True)


# ==========================================================
# Instalação
# ==========================================================

def install():

    repository = INSTALL_ROOT / REPOSITORY_NAME

    print("=" * 60)
    print("GER Installer v1.0")
    print("=" * 60)
    print()

    # ------------------------------------------------------

    if not shutil.which("git"):

        print("[FAIL] Git não encontrado.")

        sys.exit(1)

    print("[OK] Git encontrado.")

    print()

    # ------------------------------------------------------

    if repository.exists():

        print("Repository encontrado.")
        print("Atualizando...\n")

        run([
            "git",
            "-C",
            str(repository),
            "pull"
        ])

    else:

        print("Repository não encontrado.")
        print("Clonando repositório oficial...\n")

        run([
            "git",
            "clone",
            REPOSITORY_URL,
            str(repository)
        ])

    # ------------------------------------------------------

    print()

    print("=" * 60)
    print("Repository sincronizado.")
    print("=" * 60)
    print()

    print("Próximo passo:\n")

    print("%cd /content/GER")

    print("!python start_ger.py")

    print()


# ==========================================================
# Execução
# ==========================================================

if __name__ == "__main__":

    install()
