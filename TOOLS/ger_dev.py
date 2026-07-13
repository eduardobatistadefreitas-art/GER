"""
GER Development Utilities

Versão: 0.1

Objetivo:
Permitir que módulos completos sejam enviados em blocos
pelo ChatGPT e gravados automaticamente no projeto.
"""

from pathlib import Path

_current_path = None
_buffer = []


def begin_update(path):

    global _current_path
    global _buffer

    _current_path = Path(path)
    _buffer = []

    print(f"Atualizando: {_current_path}")


def append(text):

    global _buffer

    _buffer.append(text)

    print(
        f"Blocos armazenados: {len(_buffer)}"
    )


def finish_update():

    global _current_path
    global _buffer

    if _current_path is None:
        raise RuntimeError(
            "begin_update() não foi chamado."
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
