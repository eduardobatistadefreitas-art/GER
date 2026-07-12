"""
=========================================================
GER Environment Manager

Start oficial do framework GER.

Responsabilidade:
- Preparar o ambiente.
- Inicializar o framework.
- Validar a instalação.

Não executa experimentos científicos.
=========================================================
"""

from GER.VERSION import (
    FRAMEWORK_NAME,
    FRAMEWORK_VERSION,
    ENVIRONMENT_MANAGER_VERSION,
    SCIENTIFIC_PHASE,
    STATUS,
    AUTHOR,
    LAST_UPDATE,
)


def banner():
    print("=" * 60)
    print(FRAMEWORK_NAME)
    print()
    print(f"Framework Version      : {FRAMEWORK_VERSION}")
    print(f"Environment Manager    : {ENVIRONMENT_MANAGER_VERSION}")
    print(f"Scientific Phase       : {SCIENTIFIC_PHASE}")
    print(f"Status                 : {STATUS}")
    print(f"Author                 : {AUTHOR}")
    print(f"Last Update            : {LAST_UPDATE}")
    print("=" * 60)
    print()


def main():
    banner()


if __name__ == "__main__":
    main()
