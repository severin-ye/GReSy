"""数据加载器模块

负责从各种数据源加载用户和游戏数据
"""

import json
from typing import List, Dict, Set
from models.user_profile import UserProfile
from models.game_profile import GameProfile

class DataLoader:
    """数据加载器类"""
    
    @staticmethod
    def load_user_pool(file_path: str) -> List[UserProfile]:
        """从JSON文件加载用户池数据
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            List[UserProfile]: 用户档案列表
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
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
    def load_game_pool(file_path: str) -> List[GameProfile]:
        """从JSON文件加载游戏池数据
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            List[GameProfile]: 游戏档案列表
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            games = []
            for game_data in data['game_types']:
                game = GameProfile(
                    name=game_data['游戏名字'],
                    types=game_data['游戏类型'],
                    platforms=[],  # 在当前JSON中没有这个字段
                    tags=[]       # 在当前JSON中没有这个字段
                )
                games.append(game)
            return games
            
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