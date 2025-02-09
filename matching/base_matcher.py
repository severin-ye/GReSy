"""基础匹配模块

处理简单的二元匹配逻辑，如在线状态和服务器匹配
"""

from typing import Dict, List, Tuple
from models.user_profile import UserProfile

class BaseMatcher:
    """基础匹配器
    
    处理需要完全匹配/不匹配的二元匹配逻辑
    """
    
    def __init__(self):
        """初始化基础匹配器"""
        # 定义服务器组
        self.server_groups = {
            'asia': {'国服', '亚服'},
            'western': {'美服', '欧服'}
        }
        
    def match_online_status(self, user1: UserProfile, user2: UserProfile) -> bool:
        """匹配在线状态
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            bool: 是否匹配
        """
        return user1.online_status == user2.online_status
        
    def match_server(self, user1: UserProfile, user2: UserProfile) -> float:
        """匹配服务器
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            float: 匹配程度 [0,1]
            1.0: 完全匹配（相同服务器）
            0.7: 组内匹配（同属亚洲或西方服务器组）
            0.3: 不匹配（跨组）
        """
        if user1.play_region == user2.play_region:
            return 1.0
            
        # 检查是否属于同一服务器组
        for group in self.server_groups.values():
            if user1.play_region in group and user2.play_region in group:
                return 0.7
                
        return 0.3
        
    def get_match_result(self, user1: UserProfile, user2: UserProfile) -> Dict[str, float]:
        """获取基础匹配结果
        
        Args:
            user1: 第一个用户
            user2: 第二个用户
            
        Returns:
            Dict[str, float]: 包含各维度匹配分数的字典
        """
        return {
            'online_status': 1.0 if self.match_online_status(user1, user2) else 0.0,
            'server': self.match_server(user1, user2)
        } 