"""数据加载器模块

负责从各种数据源加载用户和游戏数据
"""

import json
import os
from typing import List, Dict, Set, Any
from models.user_profile import UserProfile
from models.game_profile import GameProfile
from utils.config_loader import config_loader

class DataLoader:
    """数据加载器类"""
    
    @staticmethod
    def load_user_pool() -> List[UserProfile]:
        """从JSON文件加载用户池数据
        
        Returns:
            List[UserProfile]: 用户档案列表
        """
        data = config_loader.get_pool_data('user_pool')
        if not data:
            return []
            
        users = []
        for user_data in data['users']:
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
            
    @staticmethod
    def load_game_pool() -> List[GameProfile]:
        """从JSON文件加载游戏池数据
        
        Returns:
            List[GameProfile]: 游戏档案列表
        """
        data = config_loader.get_pool_data('game_pool')
        if not data:
            return []
            
        games = []
        for game_data in data['game_types']:
            game = GameProfile(
                name=game_data['游戏名字'],
                types=game_data['游戏类型'],
                platforms=game_data.get('platforms', []),
                tags=game_data.get('tags', [])
            )
            games.append(game)
        return games
            
    @staticmethod
    def load_mbti_data() -> Dict[str, Any]:
        """加载MBTI数据
        
        Returns:
            Dict[str, Any]: MBTI配置数据
        """
        return config_loader.get_pool_data('mbti_pool') or {}
        
    @staticmethod
    def load_constellation_data() -> Dict[str, Any]:
        """加载星座数据
        
        Returns:
            Dict[str, Any]: 星座配置数据
        """
        return config_loader.get_pool_data('constellation_pool') or {}
        
    @staticmethod
    def load_server_groups() -> Dict[str, Set[str]]:
        """加载服务器组配置
        
        Returns:
            Dict[str, Set[str]]: 服务器组配置
        """
        data = config_loader.get_pool_data('server_pool')
        if not data or 'server_groups' not in data:
            return {}
            
        return {
            group_name: set(servers)
            for group_name, servers in data['server_groups'].items()
        }
            
    @staticmethod
    def get_game_types_by_name(game_name: str, games: List[GameProfile]) -> Set[str]:
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