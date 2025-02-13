"""偏好匹配器模块

提供基于偏好的匹配逻辑
"""

from abc import ABC, abstractmethod
from typing import Dict
import os
from loaders import PoolsLoader

class PreferenceMatcher(ABC):
    """偏好匹配基类
    
    用于处理基于偏好的匹配逻辑，如MBTI匹配、星座匹配等
    """
    
    def __init__(self, preference_weight: float):
        """初始化偏好匹配器
        
        Args:
            preference_weight: 在整体匹配中的权重
        """
        self.preference_weight = preference_weight
        self.preference_data = self._load_preference_data()
        
    @abstractmethod
    def _get_pool_name(self) -> str:
        """获取数据池名称"""
        pass
        
    def _load_preference_data(self) -> Dict:
        """加载偏好数据"""
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'json')
        pools_loader = PoolsLoader(base_path)
        
        pool_name = self._get_pool_name()
        data = getattr(pools_loader, f'load_{pool_name}_data')()
        if not data:
            raise FileNotFoundError(f"偏好数据加载失败: {pool_name}")
        return data
        
    @abstractmethod
    def calculate_preference_score(self, source_value: str, target_value: str) -> float:
        """计算偏好匹配分数
        
        Args:
            source_value: 源用户的值
            target_value: 目标用户的值
            
        Returns:
            float: 匹配分数 [0,1]
        """
        pass
        
    def get_weighted_score(self, source_value: str, target_value: str) -> float:
        """获取加权后的匹配分数
        
        Args:
            source_value: 源用户的值
            target_value: 目标用户的值
            
        Returns:
            float: 加权后的匹配分数
        """
        raw_score = self.calculate_preference_score(source_value, target_value)
        return raw_score * self.preference_weight

class MBTIMatcher(PreferenceMatcher):
    """MBTI偏好匹配器"""
    
    def _get_pool_name(self) -> str:
        return 'mbti'
        
    def calculate_preference_score(self, source_mbti: str, target_mbti: str) -> float:
        """计算MBTI偏好匹配分数"""
        # 在MBTI池中查找源MBTI类型
        source_data = next(
            (item for item in self.preference_data.get('mbti_types', [])
             if item['自身mbti'] == source_mbti),
            None
        )
        
        if not source_data:
            return 0.0
            
        # 获取目标MBTI的偏好分数
        preference_score = source_data.get('偏好mbti', {}).get(target_mbti, 0)
        
        # 将分数标准化到[0,1]区间
        return preference_score / 10.0 if preference_score > 0 else 0.0

class ZodiacMatcher(PreferenceMatcher):
    """星座偏好匹配器"""
    
    def _get_pool_name(self) -> str:
        return 'constellation'
        
    def calculate_preference_score(self, source_zodiac: str, target_zodiac: str) -> float:
        """计算星座偏好匹配分数"""
        # 在星座池中查找源星座
        source_data = next(
            (item for item in self.preference_data.get('constellation_types', [])
             if item['自身星座'] == source_zodiac),
            None
        )
        
        if not source_data:
            return 0.0
            
        # 获取目标星座的偏好分数
        preference_score = source_data.get('偏好星座', {}).get(target_zodiac, 0)
        
        # 将分数标准化到[0,1]区间
        return preference_score / 10.0 if preference_score > 0 else 0.0 