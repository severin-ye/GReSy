"""综合匹配系统

整合所有匹配器，提供完整的匹配功能
"""

import os
from typing import Dict, List, Tuple
from models.user_profile import UserProfile
from models.game_profile import GameProfile
from matching.base_matcher import BaseMatcher
from matching.numeric_matcher import NumericMatcher
from matching.preference_matcher import PreferenceMatcher, MBTIMatcher, ZodiacMatcher
from matching.ordered_matcher import OrderedMatcher
from matching.game_matcher import GameMatcher
from loaders import WeightsLoader

class MatchingSystem:
    """综合匹配系统
    
    整合所有匹配器，提供完整的用户匹配功能
    """
    
    def __init__(self, games: List[GameProfile]):
        """初始化匹配系统
        
        Args:
            games: 游戏档案列表
        """
        # 加载维度权重
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'json')
        weights_loader = WeightsLoader(base_path)
        weights_data = weights_loader.get_weights('match_weights')
        self.dimension_weights = weights_data.get('dimension_weights', {})
        
        # 初始化各个匹配器
        self.base_matcher = BaseMatcher()
        self.numeric_matcher = NumericMatcher()
        self.mbti_matcher = MBTIMatcher(preference_weight=0.7)
        self.zodiac_matcher = ZodiacMatcher(preference_weight=0.3)
        self.ordered_matcher = OrderedMatcher()
        self.game_matcher = GameMatcher(games)
        
    def match_users(self, user1: UserProfile, user2: UserProfile) -> Dict[str, float]:
        """匹配两个用户
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            Dict[str, float]: 包含各维度匹配分数和总分的字典
        """
        # 获取各个维度的匹配结果
        base_results = self.base_matcher.get_match_result(user1, user2)
        numeric_results = self.numeric_matcher.get_match_result(user1, user2)
        mbti_score = self.mbti_matcher.get_weighted_score(user1.mbti, user2.mbti)
        zodiac_score = self.zodiac_matcher.get_weighted_score(user1.zodiac, user2.zodiac)
        ordered_results = self.ordered_matcher.get_match_result(user1, user2)
        game_results = self.game_matcher.get_match_result(user1, user2)
        
        # 合并所有结果
        match_scores = {
            # 基础匹配分数
            'online_status': base_results['online_status'],
            'server': base_results['server'],
            
            # 数值相似度分数
            'time': numeric_results['time'],
            'experience': numeric_results['experience'],
            'style': numeric_results['style'],
            
            # 偏好匹配分数
            'mbti': mbti_score,
            'zodiac': zodiac_score,
            'gender': ordered_results['gender'],
            
            # 游戏匹配分数
            'game_type': game_results['game_type'],
            'game_preference': game_results['game_preference'],
            'game_social': game_results['social']
        }
        
        # 计算加权总分
        total_score = sum(
            score * self.dimension_weights.get(dimension, 1.0)
            for dimension, score in match_scores.items()
        ) / sum(self.dimension_weights.values())
        
        # 添加总分
        match_scores['total_score'] = total_score
        
        return match_scores
        
    def find_best_matches(
        self,
        target_user: UserProfile,
        user_pool: List[UserProfile],
        top_n: int = 10
    ) -> List[Tuple[UserProfile, Dict[str, float]]]:
        """为目标用户找到最佳匹配
        
        Args:
            target_user: 目标用户
            user_pool: 用户池
            top_n: 返回的最佳匹配数量
            
        Returns:
            List[Tuple[UserProfile, Dict[str, float]]]: 
            (匹配用户, 匹配分数)列表，按总分降序排序
        """
        # 计算目标用户与用户池中所有用户的匹配分数
        matches = []
        for user in user_pool:
            if user != target_user:
                match_scores = self.match_users(target_user, user)
                matches.append((user, match_scores))
                
        # 按总分降序排序
        matches.sort(key=lambda x: x[1]['total_score'], reverse=True)
        
        return matches[:top_n]
        
    def get_match_explanation(
        self,
        match_scores: Dict[str, float]
    ) -> List[Tuple[str, float, str]]:
        """获取匹配解释
        
        Args:
            match_scores: 匹配分数字典
            
        Returns:
            List[Tuple[str, float, str]]: 
            (维度名称, 分数, 解释)列表，按分数降序排序
        """
        explanations = []
        
        # 定义分数区间对应的解释
        score_explanations = {
            (0.8, 1.0): "非常匹配",
            (0.6, 0.8): "比较匹配",
            (0.4, 0.6): "一般匹配",
            (0.2, 0.4): "较差匹配",
            (0.0, 0.2): "不匹配"
        }
        
        # 为每个维度生成解释
        for dimension, score in match_scores.items():
            if dimension != 'total_score':
                # 获取对应分数区间的解释
                explanation = next(
                    desc for (low, high), desc in score_explanations.items()
                    if low <= score <= high
                )
                explanations.append((dimension, score, explanation))
                
        # 按分数降序排序
        explanations.sort(key=lambda x: x[1], reverse=True)
        
        return explanations 