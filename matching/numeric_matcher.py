"""数值相似度匹配模块

处理基于数值范围的匹配逻辑，如游戏风格、游戏经验、游玩时间等
"""

import json
import os
from typing import Dict, List, Tuple
from models.user_profile import UserProfile

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
        
        # 加载时间相似度配置
        with open(os.path.join(base_path, 'time_similarity.json'), 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.time_periods = config['time_periods']
            self.time_similarity = config['time_similarity']
            
        # 加载经验等级配置
        with open(os.path.join(base_path, 'experience_levels.json'), 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.experience_levels = config['experience_levels']
            self.level_similarity = config['level_similarity']
        
    def match_time(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算时间匹配度
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 相似度分数 [0,1]
        """
        return self.time_similarity[user1.play_time][user2.play_time]
            
    def match_experience(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算游戏经验匹配度
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 相似度分数 [0,1]
        """
        level1 = self.experience_levels[user1.game_experience]
        level2 = self.experience_levels[user2.game_experience]
        
        # 计算等级差异
        level_diff = abs(level1 - level2)
        return float(self.level_similarity[str(level_diff)])
            
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