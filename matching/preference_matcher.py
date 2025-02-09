"""偏好匹配器模块

提供基于偏好的匹配逻辑
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
import json
import os

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
    def _get_data_file_path(self) -> str:
        """获取偏好数据文件路径"""
        pass
        
    def _load_preference_data(self) -> Dict:
        """加载偏好数据"""
        file_path = self._get_data_file_path()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"偏好数据文件不存在: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
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
    
    def _get_data_file_path(self) -> str:
        return os.path.join('data', 'json', 'mbti_pool.json')
        
    def calculate_preference_score(self, source_mbti: str, target_mbti: str) -> float:
        """计算MBTI偏好匹配分数"""
        # 在MBTI池中查找源MBTI类型
        source_data = next(
            (item for item in self.preference_data['mbti_types'] 
             if item['自身mbti'] == source_mbti),
            None
        )
        
        if not source_data:
            return 0.0
            
        # 获取目标MBTI的偏好分数
        preference_score = source_data['偏好mbti'].get(target_mbti, 0)
        
        # 将分数标准化到[0,1]区间
        return preference_score / 10.0 if preference_score > 0 else 0.0

class ZodiacMatcher(PreferenceMatcher):
    """星座偏好匹配器"""
    
    def _get_data_file_path(self) -> str:
        return os.path.join('data', 'json', 'constellation_pool.json')
        
    def calculate_preference_score(self, source_zodiac: str, target_zodiac: str) -> float:
        """计算星座偏好匹配分数"""
        # 在星座池中查找源星座
        source_data = next(
            (item for item in self.preference_data['constellation_types'] 
             if item['自身星座'] == source_zodiac),
            None
        )
        
        if not source_data:
            return 0.0
            
        # 获取目标星座的偏好分数
        preference_score = source_data['偏好星座'].get(target_zodiac, 0)
        
        # 将分数标准化到[0,1]区间
        return preference_score / 10.0 if preference_score > 0 else 0.0 