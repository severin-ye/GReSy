"""配置加载器

负责加载系统配置文件
"""

import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ConfigLoader:
    """配置加载器类"""
    
    def __init__(self, base_path: str):
        """初始化配置加载器
        
        Args:
            base_path: 基础路径
        """
        self.config_path = os.path.join(base_path, 'config')
        self.configs = {}
        self._load_configs()
        
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
            
    def _load_configs(self):
        """加载所有配置文件"""
        config_files = [
            'platform_config.json',
            'experience_levels.json'
        ]
        
        for file_name in config_files:
            file_path = os.path.join(self.config_path, file_name)
            data = self._load_json_file(file_path)
            if data:
                self.configs[file_name.replace('.json', '')] = data
                
    def get_config(self, config_name: str) -> Dict[str, Any]:
        """获取配置
        
        Args:
            config_name: 配置名称（不含.json后缀）
            
        Returns:
            Dict[str, Any]: 配置数据
        """
        return self.configs.get(config_name, {}) 