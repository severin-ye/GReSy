"""配置加载器

用于集中管理和加载所有JSON配置文件
"""

import json
import os
from typing import Dict, Any

class ConfigLoader:
    """配置加载器类
    
    用于加载和管理所有JSON配置文件
    """
    
    def __init__(self):
        """初始化配置加载器"""
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'json')
        self.configs = {}
        self._load_all_configs()
        
    def _load_all_configs(self):
        """加载所有配置文件"""
        config_files = [
            'game_type_correlations.json',
            'time_similarity.json',
            'experience_levels.json',
            'game_similarity_weights.json',
            'platform_config.json',
            'match_weights.json'
        ]
        
        for file_name in config_files:
            file_path = os.path.join(self.base_path, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.configs[file_name.replace('.json', '')] = json.load(f)
                    
    def get_config(self, config_name: str) -> Dict[str, Any]:
        """获取指定配置
        
        Args:
            config_name: 配置名称（不含.json后缀）
            
        Returns:
            Dict[str, Any]: 配置数据
            
        Raises:
            KeyError: 如果配置不存在
        """
        if config_name not in self.configs:
            raise KeyError(f"配置 {config_name} 不存在")
        return self.configs[config_name]
        
    def get_nested_config(self, config_name: str, *keys: str) -> Any:
        """获取嵌套配置值
        
        Args:
            config_name: 配置名称
            *keys: 配置键路径
            
        Returns:
            Any: 配置值
            
        Raises:
            KeyError: 如果配置或键不存在
        """
        value = self.get_config(config_name)
        for key in keys:
            value = value[key]
        return value
        
# 创建全局配置加载器实例
config_loader = ConfigLoader() 