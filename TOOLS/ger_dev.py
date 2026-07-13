"""
GER Development Utilities

Versão: 0.2
"""

from pathlib import Path

_current_path = None
_buffer = []


def begin_update(path):

    """
    Inicia a criação de um novo arquivo.

    O arquivo existente será totalmente substituído
    quando finish_update() for chamado.
    """

    global _current_path
    global _buffer

    _current_path = Path(path)
    _buffer = []

    print(f"Atualizando: {_current_path}")


def begin_replace(path):
    """
    Alias semântico de begin_update().

    Utilizar quando a intenção é regenerar
    completamente um módulo existente.
    """

    begin_update(path)


def append(text):

    global _buffer

    _buffer.append(text)

    print(f"Blocos armazenados: {len(_buffer)}")


def finish_update():

    global _current_path
    global _buffer

    if _current_path is None:
        raise RuntimeError(
            "Nenhuma atualização iniciada."
        )

    content = "".join(_buffer)

    _current_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    _current_path.write_text(
        content,
        encoding="utf-8",
    )

    print()

    print("=" * 60)
    print("GER DEV")
    print("=" * 60)
    print(f"Arquivo : {_current_path}")
    print(f"Blocos  : {len(_buffer)}")
    print(f"Tamanho : {len(content)} caracteres")
    print("=" * 60)

    _current_path = None
    _buffer = []


def abort_update():

    global _current_path
    global _buffer

    _current_path = None
    _buffer = []

    print("Atualização cancelada.")
