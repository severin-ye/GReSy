"""偏好列表匹配模块(强制顺位)

处理基于列表顺位依次匹配的逻辑，如性别匹配
"""

from typing import Dict, List, Tuple
from models.user_profile import UserProfile

class OrderedMatcher:
    """强制顺位匹配器
    
    处理基于列表顺位依次匹配的逻辑
    """
    
    def __init__(self):
        """初始化强制顺位匹配器"""
        # 定义性别偏好权重衰减因子
        self.preference_scale = 0.7
        
    def match_gender(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算性别偏好权重
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 匹配权重 [0,1]
        """
        # 如果任一用户没有性别偏好，返回很低分数
        if not user1.gender_preference or not user2.gender_preference:
            return 0.2
            
        try:
            # 计算双向性别偏好权重
            u1_preference = user1.gender_preference.index(user2.gender)
            u2_preference = user2.gender_preference.index(user1.gender)
            
            # 使用几何平均计算综合权重
            u1_weight = self.preference_scale ** (len(user1.gender_preference) - 1 - u1_preference)
            u2_weight = self.preference_scale ** (len(user2.gender_preference) - 1 - u2_preference)
            
            # 如果任一方的偏好不是第一位，降低分数
            if u1_preference > 0 or u2_preference > 0:
                return min((u1_weight * u2_weight) ** 0.5, 0.7)
            
            return (u1_weight * u2_weight) ** 0.5
            
        except ValueError:
            # 如果性别不在偏好列表中，返回很低分数
            return 0.2
            
    def get_match_result(self, user1: UserProfile, user2: UserProfile) -> Dict[str, float]:
        """获取强制顺位匹配结果
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            Dict[str, float]: 包含各维度匹配分数的字典
        """
        return {
            'gender': self.match_gender(user1, user2)
        } 