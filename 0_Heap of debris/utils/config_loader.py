"""配置加载器

用于集中管理和加载所有JSON配置文件
"""

import json
import os
import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigLoader:
    """配置加载器类
    
    用于加载和管理所有JSON配置文件
    """
    
    def __init__(self):
        """初始化配置加载器"""
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'json')
        self.configs = {
            'weights': {},
            'config': {},
            'pools': {}
        }
        self._load_all_configs()
        
    def _load_json_file(self, file_path: str) -> Dict[str, Any]:
        """加载单个JSON文件
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            Dict[str, Any]: JSON数据
        """
        try:
            if not os.path.exists(file_path):
                logger.warning(f"文件不存在: {file_path}")
                return {}
                
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误 {file_path}: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"加载文件出错 {file_path}: {str(e)}")
            return {}
        
    def _load_all_configs(self):
        """加载所有配置文件"""
        # 加载权重配置
        weight_files = [
            'match_weights.json',
            'game_similarity_weights.json',
            'game_type_correlations.json',
            'time_similarity.json'
        ]
        for file_name in weight_files:
            file_path = os.path.join(self.base_path, 'weights', file_name)
            data = self._load_json_file(file_path)
            if data:
                self.configs['weights'][file_name.replace('.json', '')] = data
                
        # 加载系统配置
        config_files = [
            'platform_config.json',
            'experience_levels.json'
        ]
        for file_name in config_files:
            file_path = os.path.join(self.base_path, 'config', file_name)
            data = self._load_json_file(file_path)
            if data:
                self.configs['config'][file_name.replace('.json', '')] = data
                
        # 加载数据池配置
        pool_files = [
            'user_pool.json',
            'game_pool.json',
            'mbti_pool.json',
            'constellation_pool.json',
            'server_pool.json'
        ]
        for file_name in pool_files:
            file_path = os.path.join(self.base_path, 'pools', file_name)
            data = self._load_json_file(file_path)
            if data:
                self.configs['pools'][file_name.replace('.json', '')] = data
                    
    def get_weight_config(self, config_name: str) -> Dict[str, Any]:
        """获取权重配置
        
        Args:
            config_name: 配置名称（不含.json后缀）
            
        Returns:
            Dict[str, Any]: 配置数据
        """
        return self.configs['weights'].get(config_name)
        
    def get_system_config(self, config_name: str) -> Dict[str, Any]:
        """获取系统配置
        
        Args:
            config_name: 配置名称（不含.json后缀）
            
        Returns:
            Dict[str, Any]: 配置数据
        """
        return self.configs['config'].get(config_name)
        
    def get_pool_data(self, pool_name: str) -> Dict[str, Any]:
        """获取数据池
        
        Args:
            pool_name: 数据池名称（不含.json后缀）
            
        Returns:
            Dict[str, Any]: 数据池数据
        """
        return self.configs['pools'].get(pool_name)
        
    def get_nested_config(self, category: str, config_name: str, *keys: str) -> Any:
        """获取嵌套配置值
        
        Args:
            category: 配置类别 ('weights', 'config', 'pools')
            config_name: 配置名称
            *keys: 配置键路径
            
        Returns:
            Any: 配置值
            
        Raises:
            KeyError: 如果配置或键不存在
        """
        if category not in self.configs:
            raise KeyError(f"配置类别 {category} 不存在")
            
        if config_name not in self.configs[category]:
            raise KeyError(f"配置 {config_name} 不存在于 {category}")
            
        value = self.configs[category][config_name]
        for key in keys:
            value = value[key]
        return value

# 创建全局配置加载器实例
config_loader = ConfigLoader() 

# 测试加载权重配置
weight_config = config_loader.get_weight_config('match_weights')
print("权重配置:", weight_config)

# 测试加载系统配置
system_config = config_loader.get_system_config('platform_config')
print("系统配置:", system_config)

# 测试加载数据池
user_pool = config_loader.get_pool_data('user_pool')
print("用户池:", user_pool) 