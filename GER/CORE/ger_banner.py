"""
=========================================================
GER CORE

Arquivo : ger_banner.py

Banner oficial do framework GER.
=========================================================
"""

from GER.VERSION import (
    FRAMEWORK_NAME,
    FRAMEWORK_VERSION,
    SCIENTIFIC_PHASE,
    STATUS,
    AUTHOR,
    LAST_UPDATE,
)


def show_banner():

    print("=" * 60)
    print("GER Environment Manager")
    print("=" * 60)
    print()

    print(FRAMEWORK_NAME)
    print()

    print(f"Version : {FRAMEWORK_VERSION}")
    print(f"Phase   : {SCIENTIFIC_PHASE}")
    print(f"Status  : {STATUS}")
    print(f"Author  : {AUTHOR}")
    print(f"Updated : {LAST_UPDATE}")

    print()
    print("=" * 60)
