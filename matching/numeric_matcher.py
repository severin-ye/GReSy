"""数值相似度匹配模块

处理基于数值范围的匹配逻辑，如游戏风格、游戏经验、游玩时间等
"""

from typing import Dict, List, Tuple
from models.user_profile import UserProfile

class NumericMatcher:
    """数值相似度匹配器
    
    处理基于数值范围的匹配逻辑
    """
    
    def __init__(self):
        """初始化数值相似度匹配器"""
        # 定义时间段及其权重
        self.time_periods = ['凌晨', '早上', '中午', '下午', '晚上']
        
        # 定义时间段相似度矩阵
        self.time_similarity = {
            '凌晨': {'凌晨': 1.0, '早上': 0.7, '中午': 0.3, '下午': 0.3, '晚上': 0.3},
            '早上': {'凌晨': 0.7, '早上': 1.0, '中午': 0.7, '下午': 0.3, '晚上': 0.3},
            '中午': {'凌晨': 0.3, '早上': 0.7, '中午': 1.0, '下午': 0.7, '晚上': 0.3},
            '下午': {'凌晨': 0.3, '早上': 0.3, '中午': 0.7, '下午': 1.0, '晚上': 0.7},
            '晚上': {'凌晨': 0.3, '早上': 0.3, '中午': 0.3, '下午': 0.7, '晚上': 1.0}
        }
        
        # 定义游戏经验等级
        self.experience_levels = {
            '初级': 1,
            '中级': 2,
            '高级': 3,
            '高超': 4
        }
        
    def calculate_time_similarity(self, time1: str, time2: str) -> float:
        """计算时间匹配度
        
        Args:
            time1: 第一个时间段
            time2: 第二个时间段
            
        Returns:
            float: 相似度分数 [0,1]
        """
        return self.time_similarity[time1][time2]
            
    def calculate_experience_similarity(self, exp1: str, exp2: str) -> float:
        """计算游戏经验匹配度
        
        Args:
            exp1: 第一个经验等级
            exp2: 第二个经验等级
            
        Returns:
            float: 相似度分数 [0,1]
        """
        level1 = self.experience_levels[exp1]
        level2 = self.experience_levels[exp2]
        
        # 计算等级差异
        level_diff = abs(level1 - level2)
        
        if level_diff == 0:
            return 1.0
        elif level_diff == 1:
            return 0.7
        else:
            return 0.3
            
    def calculate_style_similarity(self, style1: str, style2: str) -> float:
        """计算游戏风格匹配度
        
        Args:
            style1: 第一个游戏风格
            style2: 第二个游戏风格
            
        Returns:
            float: 相似度分数 [0,1]
        """
        return 1.0 if style1 == style2 else 0.3
        
    def get_match_result(self, user1: UserProfile, user2: UserProfile) -> Dict[str, float]:
        """获取数值相似度匹配结果
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            Dict[str, float]: 包含各维度匹配分数的字典
        """
        return {
            'time': self.calculate_time_similarity(user1.play_time, user2.play_time),
            'experience': self.calculate_experience_similarity(
                user1.game_experience, 
                user2.game_experience
            ),
            'style': self.calculate_style_similarity(user1.game_style, user2.game_style)
        } 