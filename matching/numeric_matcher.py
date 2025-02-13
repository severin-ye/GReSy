"""数值相似度匹配模块

处理基于数值范围的匹配逻辑，如游戏风格、游戏经验、游玩时间等
"""

import os
from typing import Dict
from models.user_profile import UserProfile
from utils.loaders import WeightsLoader, ConfigLoader

class NumericMatcher:
    """数值相似度匹配器
    
    处理基于数值范围的匹配逻辑
    """
    
    def __init__(self):
        """初始化数值相似度匹配器"""
        self._load_configs()
        
    def _load_configs(self):
        """加载配置文件"""
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'json')
        
        # 初始化加载器
        weights_loader = WeightsLoader(base_path)
        config_loader = ConfigLoader(base_path)
        
        # 加载时间相似度配置
        time_data = weights_loader.get_weights('time_similarity')
        self.time_periods = time_data.get('time_periods', {})
        self.time_similarity = time_data.get('time_similarity', {})
            
        # 加载经验等级配置
        experience_data = config_loader.get_config('experience_levels')
        self.experience_levels = experience_data.get('experience_levels', {})
        self.level_similarity = experience_data.get('level_similarity', {})
        
    def match_time(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算时间匹配度
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 相似度分数 [0,1]
        """
        if not self.time_similarity or user1.play_time not in self.time_similarity or user2.play_time not in self.time_similarity[user1.play_time]:
            return 0.0
        return self.time_similarity[user1.play_time][user2.play_time]
            
    def match_experience(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算游戏经验匹配度
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 相似度分数 [0,1]
        """
        if not self.experience_levels or user1.game_experience not in self.experience_levels or user2.game_experience not in self.experience_levels:
            return 0.0
            
        level1 = self.experience_levels[user1.game_experience]
        level2 = self.experience_levels[user2.game_experience]
        
        # 计算等级差异
        level_diff = abs(level1 - level2)
        return float(self.level_similarity.get(str(level_diff), 0.0))
            
    def match_style(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算游戏风格匹配度
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 相似度分数 [0,1]
        """
        return 1.0 if user1.game_style == user2.game_style else 0.3
        
    def get_match_result(self, user1: UserProfile, user2: UserProfile) -> Dict[str, float]:
        """获取数值相似度匹配结果
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            Dict[str, float]: 包含各维度匹配分数的字典
        """
        return {
            'time': self.match_time(user1, user2),
            'experience': self.match_experience(user1, user2),
            'style': self.match_style(user1, user2)
        } 