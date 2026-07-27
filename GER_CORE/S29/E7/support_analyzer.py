from .model import DynamicRegime
from .support import (
    SupportAnalysis,
    SupportType,
)


class SupportAnalyzer:
    """
    Determines the observational support associated with a
    DynamicRegime.

    This layer precedes the representation analysis.
    """

    @staticmethod
    def analyze(
        regime: DynamicRegime,
    ) -> SupportAnalysis:
        """
        Analyze the observational support.

        Version 1.0

        A DynamicRegime represents one certified realization.
        """

        return SupportAnalysis(
            support=SupportType.SINGLE_SAMPLE,
            sample_count=1,
            parameter_count=None,
            completed=True,
            reason=(
                "DynamicRegime represents one certified realization."
            ),
        )
