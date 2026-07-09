%%writefile GER_CORE/bootstrap.py

"""
=========================================================
GER CORE
Arquivo : bootstrap.py
=========================================================

Inicializador oficial da Geometria Espectral Relacional.

Uso:

    python bootstrap.py

ou no Google Colab:

    %run GER_CORE/bootstrap.py


Carrega:

- geometria
- potenciais
- métricas
- análise modal
- snapshots
- motor temporal

e executa validação automática.
"""



# =========================================================
# Imports principais
# =========================================================

from ger_engine import (
    run_engine
)


from ger_validation import (
    validate_GER_CORE
)



# =========================================================
# Inicialização
# =========================================================

def initialize():

    print(
        "================================"
    )

    print(
        " INICIANDO GER CORE v1"
    )

    print(
        "================================"
    )


    validate_GER_CORE()


    print(
        ""
    )

    print(
        "GER CORE pronto para experimentos."
    )

    print(
        "================================"
    )


    return True



# =========================================================
# Execução direta
# =========================================================

if __name__ == "__main__":

    initialize()
