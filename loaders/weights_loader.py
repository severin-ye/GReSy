"""权重加载器

负责加载各种匹配权重配置
"""

import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WeightsLoader:
    """权重加载器类"""
    
    def __init__(self, base_path: str):
        """初始化权重加载器
        
        Args:
            base_path: 基础路径
        """
        self.weights_path = os.path.join(base_path, 'weights')
        self.weights = {}
        self._load_weights()
        
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
            
    def _load_weights(self):
        """加载所有权重配置"""
        weight_files = [
            'match_weights.json',
            'game_similarity_weights.json',
            'game_type_correlations.json',
            'time_similarity.json'
        ]
        
        for file_name in weight_files:
            file_path = os.path.join(self.weights_path, file_name)
            data = self._load_json_file(file_path)
            if data:
                self.weights[file_name.replace('.json', '')] = data
                
    def get_weights(self, weight_name: str) -> Dict[str, Any]:
        """获取权重配置
        
        Args:
            weight_name: 权重配置名称（不含.json后缀）
            
        Returns:
            Dict[str, Any]: 权重配置数据
        """
        return self.weights.get(weight_name, {}) 