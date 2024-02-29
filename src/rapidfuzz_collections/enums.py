
from enum import Enum


class ScorerType(Enum):
    """
    Type of Rapidfuzz Scorer:
        DISTANCE: lower number - more similar
        SIMILARITY: higher number - more similar
    Interprets the evaluation score.
    """
    DISTANCE = 0
    SIMILARITY = 1


class Strategy(Enum):
    """
    Strategy for returning value:
        FIRST_FROM_BEST: return the first value from best scoring results
        BEST_ONLY_ONE: return best value if there are no other values with same score
        FIRST: return the first similar value (it may be not the best)
    """
    FIRST_FROM_BEST = 1
    BEST_ONLY_ONE = 2
    FIRST = 3
