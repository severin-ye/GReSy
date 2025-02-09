"""加载器包

提供统一的数据加载接口
"""

import os
from typing import Dict, Any
from .config_loader import ConfigLoader
from .weights_loader import WeightsLoader
from .pools_loader import PoolsLoader

class LoaderManager:
    """加载器管理类"""
    
    def __init__(self):
        """初始化加载器管理器"""
        base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'json')
        self.config_loader = ConfigLoader(base_path)
        self.weights_loader = WeightsLoader(base_path)
        self.pools_loader = PoolsLoader(base_path)
        
    def get_config(self, config_name: str) -> Dict[str, Any]:
        """获取系统配置
        
        Args:
            config_name: 配置名称
            
        Returns:
            Dict[str, Any]: 配置数据
        """
        return self.config_loader.get_config(config_name)
        
    def get_weights(self, weight_name: str) -> Dict[str, Any]:
        """获取权重配置
        
        Args:
            weight_name: 权重名称
            
        Returns:
            Dict[str, Any]: 权重数据
        """
        return self.weights_loader.get_weights(weight_name)
        
    def get_pool_data(self, pool_name: str) -> Dict[str, Any]:
        """获取原始数据池数据
        
        Args:
            pool_name: 数据池名称
            
        Returns:
            Dict[str, Any]: 数据池数据
        """
        return self.pools_loader.pools.get(pool_name, {})

# 创建全局加载器管理实例
loader_manager = LoaderManager() 