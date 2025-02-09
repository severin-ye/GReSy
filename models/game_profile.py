"""游戏档案模型

定义游戏的基本信息和属性
"""

from typing import List

class GameProfile:
    """游戏档案类"""
    
    def __init__(
        self,
        name: str,
        types: List[str],
        platforms: List[str],
        tags: List[str]
    ):
        """初始化游戏档案
        
        Args:
            name: 游戏名称
            types: 游戏类型列表
            platforms: 游戏平台列表
            tags: 游戏标签列表
        """
        self.name = name
        self.types = types
        self.platforms = platforms
        self.tags = tags
        
    def __eq__(self, other):
        """判断两个游戏是否相同"""
        if not isinstance(other, GameProfile):
            return False
        return self.name == other.name