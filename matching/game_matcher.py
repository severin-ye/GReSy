"""多维度综合匹配模块

处理游戏匹配的三个维度：
1. 游戏类型相似度
2. 游戏偏好相似度
3. 社交属性相似度
"""

import os
from typing import Dict, List, Set, Tuple
from models.user_profile import UserProfile
from models.game_profile import GameProfile
from utils.loaders import ConfigLoader, WeightsLoader

class GameMatcher:
    """游戏多维度匹配器
    
    处理需要多个维度综合考虑的复杂匹配逻辑
    """
    
    def __init__(self, games: List[GameProfile]):
        """初始化游戏匹配器
        
        Args:
            games: 游戏档案列表
        """
        self.games = games
        self._load_configs()
        
    def _load_configs(self):
        """加载配置文件"""
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'json')
        
        # 初始化加载器
        weights_loader = WeightsLoader(base_path)
        config_loader = ConfigLoader(base_path)
        
        # 加载游戏类型相关性
        game_type_data = weights_loader.get_weights('game_type_correlations')
        self.game_type_correlations = game_type_data.get('game_type_correlations', {})
            
        # 加载游戏相似度权重
        similarity_data = weights_loader.get_weights('game_similarity_weights')
        self.game_similarity_weights = similarity_data.get('game_similarity_weights', {})
        self.social_weights = similarity_data.get('social_weights', {})
            
        # 加载经验等级配置
        experience_data = config_loader.get_config('experience_levels')
        self.experience_levels = experience_data.get('experience_levels', {})
        self.level_similarity = experience_data.get('level_similarity', {})
        
    def match_type(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算游戏类型相似度
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 相似度分数 [0,1]
        """
        # 获取用户的游戏类型集合
        user1_types = set()
        user2_types = set()
        
        for game in user1.games:
            game_profile = next((g for g in self.games if g.name == game), None)
            if game_profile:
                user1_types.update(game_profile.types)
                
        for game in user2.games:
            game_profile = next((g for g in self.games if g.name == game), None)
            if game_profile:
                user2_types.update(game_profile.types)
                
        if not user1_types or not user2_types:
            return 0.0
            
        # 计算类型相关性
        total_correlation = 0.0
        count = 0
        
        for type1 in user1_types:
            for type2 in user2_types:
                if type1 in self.game_type_correlations and type2 in self.game_type_correlations[type1]:
                    total_correlation += self.game_type_correlations[type1][type2]
                    count += 1
                elif type1 == type2:
                    total_correlation += 1.0
                    count += 1
                else:
                    total_correlation += 0.1
                    count += 1
                    
        return total_correlation / count if count > 0 else 0.0
        
    def match_preference(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算游戏偏好相似度
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 相似度分数 [0,1]
        """
        # 计算共同游戏数量
        common_games = set(user1.games).intersection(set(user2.games))
        
        # 如果用户没有游戏，返回0
        if not user1.games or not user2.games:
            return 0.0
            
        # 计算Jaccard相似度
        return len(common_games) / len(set(user1.games).union(set(user2.games)))
        
    def match_social(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算社交属性相似度
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 相似度分数 [0,1]
        """
        # 计算在线状态匹配度
        online_match = 1.0 if user1.online_status == user2.online_status else 0.5
        
        # 计算游戏风格匹配度
        style_match = 1.0 if user1.game_style == user2.game_style else 0.5
        
        # 计算游戏经验匹配度
        level1 = self.experience_levels[user1.game_experience]
        level2 = self.experience_levels[user2.game_experience]
        level_diff = abs(level1 - level2)
        exp_match = float(self.level_similarity[str(level_diff)])
                             
        return (online_match * self.social_weights['online_status'] + 
                style_match * self.social_weights['game_style'] + 
                exp_match * self.social_weights['experience'])
        
    def get_match_result(self, user1: UserProfile, user2: UserProfile) -> Dict[str, float]:
        """获取游戏匹配结果
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            Dict[str, float]: 包含各维度匹配分数的字典
        """
        type_similarity = self.match_type(user1, user2)
        preference_similarity = self.match_preference(user1, user2)
        social_similarity = self.match_social(user1, user2)
        
        # 使用配置的权重计算加权分数
        weighted_score = (
            type_similarity * self.game_similarity_weights['type_similarity'] +
            preference_similarity * self.game_similarity_weights['preference_similarity'] +
            social_similarity * self.game_similarity_weights['social_similarity']
        )
        
        return {
            'game_type': type_similarity,
            'game_preference': preference_similarity,
            'social': social_similarity,
            'weighted_score': weighted_score
        } 