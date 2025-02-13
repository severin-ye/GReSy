"""数据池加载器

负责加载用户、游戏等数据池
"""

import json
import os
import logging
from typing import Dict, Any, List, Set
from models.user_profile import UserProfile
from models.game_profile import GameProfile

logger = logging.getLogger(__name__)

class PoolsLoader:
    """数据池加载器类"""
    
    def __init__(self, base_path: str):
        """初始化数据池加载器
        
        Args:
            base_path: 基础路径
        """
        self.pools_path = os.path.join(base_path, 'pools')  # 从pools子目录加载数据
        self.pools = {}
        self._load_pools()
        
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
            
    def _load_pools(self):
        """加载所有数据池"""
        pool_files = [
            'user_pool.json',
            'game_pool.json',
            'mbti_pool.json',
            'constellation_pool.json',
            'server_pool.json'
        ]
        
        for file_name in pool_files:
            file_path = os.path.join(self.pools_path, file_name)
            data = self._load_json_file(file_path)
            if data:
                self.pools[file_name.replace('.json', '')] = data
                
    def load_user_pool(self) -> List[UserProfile]:
        """加载用户池数据
        
        Returns:
            List[UserProfile]: 用户档案列表
        """
        data = self.pools.get('user_pool', {})
        if not data:
            return []
            
        users = []
        for user_data in data.get('users', []):
            user = UserProfile(
                user_id=user_data['id'],
                games=user_data['游戏'],
                gender=user_data['性别'],
                gender_preference=user_data['性别倾向'],
                play_region=user_data['游玩服务器'],
                play_time=user_data['游玩固定时间'],
                mbti=user_data['MBTI'],
                zodiac=user_data['星座'],
                game_experience=user_data['游戏经验'],
                online_status=user_data['在线状态'],
                game_style=user_data['游戏风格']
            )
            users.append(user)
        return users
        
    def load_game_pool(self) -> List[GameProfile]:
        """加载游戏池数据
        
        Returns:
            List[GameProfile]: 游戏档案列表
        """
        data = self.pools.get('game_pool', {})
        if not data:
            return []
            
        games = []
        for game_data in data.get('game_types', []):
            game = GameProfile(
                name=game_data['游戏名字'],
                types=game_data['游戏类型'],
                platforms=game_data.get('platforms', []),
                tags=game_data.get('tags', [])
            )
            games.append(game)
        return games
        
    def load_mbti_data(self) -> Dict[str, Any]:
        """加载MBTI数据
        
        Returns:
            Dict[str, Any]: MBTI配置数据
        """
        return self.pools.get('mbti_pool', {})
        
    def load_constellation_data(self) -> Dict[str, Any]:
        """加载星座数据
        
        Returns:
            Dict[str, Any]: 星座配置数据
        """
        return self.pools.get('constellation_pool', {})
        
    def load_server_groups(self) -> Dict[str, Set[str]]:
        """加载服务器组配置
        
        Returns:
            Dict[str, Set[str]]: 服务器组配置
        """
        data = self.pools.get('server_pool', {})
        if not data or 'server_groups' not in data:
            return {}
            
        return {
            group_name: set(servers)
            for group_name, servers in data['server_groups'].items()
        }
        
    def get_game_types_by_name(self, game_name: str, games: List[GameProfile]) -> Set[str]:
        """根据游戏名称获取游戏类型
        
        Args:
            game_name: 游戏名称
            games: 游戏档案列表
            
        Returns:
            Set[str]: 游戏类型集合
        """
        for game in games:
            if game.name == game_name:
                return set(game.types)
        return set() 