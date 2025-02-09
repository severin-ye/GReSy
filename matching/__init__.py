"""匹配模块包

包含所有匹配相关的模块
"""

from .base_matcher import BaseMatcher
from .numeric_matcher import NumericMatcher
from .preference_matcher import PreferenceMatcher, MBTIMatcher, ZodiacMatcher
from .ordered_matcher import OrderedMatcher
from .game_matcher import GameMatcher
from .matching_system import MatchingSystem

__all__ = [
    'BaseMatcher',
    'NumericMatcher',
    'PreferenceMatcher',
    'MBTIMatcher',
    'ZodiacMatcher',
    'OrderedMatcher',
    'GameMatcher',
    'MatchingSystem'
] 