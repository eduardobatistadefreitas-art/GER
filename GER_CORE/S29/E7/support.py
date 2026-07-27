from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SupportType(Enum):
    """
    Describes the observational support available for a
    DynamicRegime analysis.
    """

    SINGLE_SAMPLE = "SINGLE_SAMPLE"

    MULTIPLE_SAMPLES = "MULTIPLE_SAMPLES"

    PARAMETRIC_FAMILY = "PARAMETRIC_FAMILY"

    CONTINUOUS_FAMILY = "CONTINUOUS_FAMILY"

    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class SupportAnalysis:
    """
    Result produced by the SupportAnalyzer.

    It characterizes the observational support available
    before any geometric representation is evaluated.
    """

    support: SupportType

    sample_count: int

    parameter_count: Optional[int]

    completed: bool

    reason: str
