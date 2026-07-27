"""
GER - Geometria Espectral Relacional
S29 - E7

exceptions.py

Custom exceptions for the Dynamic Regime Builder.

These exceptions isolate E7 from generic Python exceptions,
making failures explicit and easier to diagnose.

Author:
    Eduardo Batista de Freitas

Project:
    GER - Geometria Espectral Relacional
"""


# ---------------------------------------------------------------------
# Base Exception
# ---------------------------------------------------------------------

class DynamicRegimeError(Exception):
    """
    Base exception for all E7 errors.
    """
    pass


# ---------------------------------------------------------------------
# Missing Files
# ---------------------------------------------------------------------

class MissingStationaryScanError(DynamicRegimeError):
    """
    Raised when stationary_scan.json cannot be found.
    """
    pass


class MissingClassifierError(DynamicRegimeError):
    """
    Raised when classifier.json cannot be found.
    """
    pass


class MissingClassifierAuditError(DynamicRegimeError):
    """
    Raised when classifier_audit.json cannot be found.
    """
    pass


# ---------------------------------------------------------------------
# Invalid Files
# ---------------------------------------------------------------------

class InvalidStationaryScanError(DynamicRegimeError):
    """
    Raised when stationary_scan.json is malformed or incomplete.
    """
    pass


class InvalidClassifierError(DynamicRegimeError):
    """
    Raised when classifier.json is malformed or incomplete.
    """
    pass


class InvalidClassifierAuditError(DynamicRegimeError):
    """
    Raised when classifier_audit.json is malformed or incomplete.
    """
    pass


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

class DynamicRegimeValidationError(DynamicRegimeError):
    """
    Raised when the assembled DynamicRegime does not satisfy
    the required scientific contract.
    """
    pass


# ---------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------

class DynamicRegimeBuilderError(DynamicRegimeError):
    """
    Raised when the Builder cannot assemble a valid
    DynamicRegime instance.
    """
    pass
