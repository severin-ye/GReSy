"""游戏档案模型

定义游戏相关的数据结构
"""

from dataclasses import dataclass
from typing import List

@dataclass
class GameProfile:
    """游戏档案类，存储游戏的基本信息"""
    name: str           # 游戏名称
    types: List[str]    # 游戏类型列表
    platforms: List[str] # 支持的平台
    tags: List[str]     # 游戏标签
    
    def to_dict(self) -> dict:
        """将游戏档案转换为字典格式"""
        return {
            'name': self.name,
            'types': self.types,
            'platforms': self.platforms,
            'tags': self.tags
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'GameProfile':
        """从字典创建游戏档案实例
        
        Args:
            data: 游戏数据字典
            
        Returns:
            GameProfile: 游戏档案实例
        """
        return cls(
            name=data['name'],
            types=data.get('types', []),
            platforms=data.get('platforms', []),
            tags=data.get('tags', [])
        )