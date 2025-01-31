"""核心匹配器模块

实现用户匹配的核心逻辑
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple, Dict, Set
import numpy as np
from models.user_profile import UserProfile
from models.game_profile import GameProfile
from matching.feature_processor import FeatureProcessor
from matching.similarity_calculator import (
    calculate_cosine_similarity,
    calculate_game_type_similarity,
    calculate_gender_preference_weight,
    calculate_time_similarity,
    calculate_region_similarity,
    calculate_experience_similarity,
    calculate_mbti_similarity,
    calculate_game_social_similarity
)
from config.weights import (
    FEATURE_WEIGHTS,
    GAME_SIMILARITY_WEIGHTS,
    GAME_SIMILARITY_THRESHOLD
)
from utils.data_loaders import DataLoader

class UserMatcher:
    """用户匹配器类
    
    负责：
    1. 用户特征处理
    2. 相似度计算
    3. 匹配结果生成
    """
    
    def __init__(self, debug_mode: bool = False):
        """初始化匹配器
        
        Args:
            debug_mode: 是否启用调试模式
        """
        self.users: List[UserProfile] = []
        self.debug_mode = debug_mode
        self.feature_processor = FeatureProcessor()
        
    def add_user(self, user: UserProfile) -> None:
        """添加用户到匹配系统"""
        self.users.append(user)
        
    def _calculate_game_similarity(
        self,
        user1: UserProfile,
        user2: UserProfile,
        games: List[GameProfile]
    ) -> float:
        """计算游戏相似度"""
        # 获取用户游戏类型
        user1_types = set()
        user2_types = set()
        for game in user1.games:
            user1_types.update(DataLoader.get_game_types_by_name(game, games))
        for game in user2.games:
            user2_types.update(DataLoader.get_game_types_by_name(game, games))
            
        # 计算类型相似度
        type_similarity = calculate_game_type_similarity(user1_types, user2_types)
        
        # 计算游戏偏好相似度（基于共同游戏）
        common_games = set(user1.games).intersection(set(user2.games))
        preference_similarity = len(common_games) / max(len(user1.games), len(user2.games)) \
                              if user1.games and user2.games else 0.0
                              
        # 计算社交属性相似度
        social_similarity = calculate_game_social_similarity(user1, user2)
        
        # 加权组合三种相似度:
        # 1. type_similarity: 游戏类型相似度,考虑游戏类型(如MOBA、FPS等)的匹配程度
        # 2. preference_similarity: 游戏偏好相似度,基于用户共同游戏的比例
        # 3. social_similarity: 社交属性相似度,考虑用户的游戏社交特征
        # 
        # 使用GAME_SIMILARITY_WEIGHTS中定义的权重进行加权:
        # - type_similarity权重: 游戏类型匹配的重要程度
        # - preference_similarity权重: 共同游戏偏好的重要程度  
        # - social_similarity权重: 社交属性匹配的重要程度
        return (type_similarity * GAME_SIMILARITY_WEIGHTS['type_similarity'] +
                preference_similarity * GAME_SIMILARITY_WEIGHTS['preference_similarity'] + 
                social_similarity * GAME_SIMILARITY_WEIGHTS['social_similarity'])
    def _calculate_personality_similarity(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算性格相似度"""
        # 计算MBTI匹配度
        mbti_similarity = calculate_mbti_similarity(user1.mbti, user2.mbti)
        
        # 计算游戏风格匹配度
        style_similarity = 1.0 if user1.game_style == user2.game_style else 0.5
        
        return (mbti_similarity * 0.7 + style_similarity * 0.3)
        
    def _calculate_time_region_similarity(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算时间和区服匹配度"""
        # 计算时间匹配度
        time_similarity = calculate_time_similarity(user1.play_time, user2.play_time)
        
        # 计算区服匹配度
        region_similarity = calculate_region_similarity(user1.play_region, user2.play_region)
        
        return (time_similarity * 0.5 + region_similarity * 0.5)
        
    def _get_similar_games(
        self,
        user_games: List[str],
        games: List[GameProfile],
        similarity_threshold: float = GAME_SIMILARITY_THRESHOLD
    ) -> List[Tuple[str, float]]:
        """获取与用户当前游戏相似的其他游戏
        
        Args:
            user_games: 用户当前玩的游戏列表
            games: 所有游戏档案列表
            similarity_threshold: 游戏相似度阈值
            
        Returns:
            List[Tuple[str, float]]: (游戏名称, 相似度)的列表
        """
        user_game_types = set()
        for game in user_games:
            user_game_types.update(DataLoader.get_game_types_by_name(game, games))
            
        similar_games = []
        for game in games:
            if game.name not in user_games:
                game_types = set(game.types)
                similarity = calculate_game_type_similarity(user_game_types, game_types)
                
                if similarity >= similarity_threshold:
                    similar_games.append((game.name, similarity))
                    
        return sorted(similar_games, key=lambda x: x[1], reverse=True)
        
    def find_matches(
        self,
        target_user: UserProfile,
        games: List[GameProfile],
        top_n: int = 20
    ) -> List[Tuple[UserProfile, float, Dict[str, float], List[Tuple[str, float]]]]:
        """为目标用户找到最匹配的其他用户"""
        if target_user not in self.users:
            self.add_user(target_user)
            
        # 获取目标用户可能感兴趣的游戏
        possible_games = self._get_similar_games(target_user.games, games)
        target_possible_games = [game for game, _ in possible_games]
        target_all_games = set(target_user.games + target_possible_games)
        
        # 筛选有共同游戏的用户
        matching_game_users = [
            user for user in self.users
            if user != target_user and any(game in target_all_games for game in user.games)
        ]
        
        if not matching_game_users:
            return []
            
        # 计算匹配结果
        matches = []
        for user in matching_game_users:
            # 计算各维度得分
            time_match = 1.0 if user.play_time == target_user.play_time else 0.3
            region_match = 1.0 if user.play_region == target_user.play_region else \
                          0.7 if (user.play_region in ['国服', '亚服'] and target_user.play_region in ['国服', '亚服']) else 0.3
            online_match = 1.0 if user.online_status == target_user.online_status else 0.5
            game_similarity = self._calculate_game_similarity(target_user, user, games)
            zodiac_match = 1.0 if user.zodiac == target_user.zodiac else 0.3
            mbti_match = calculate_mbti_similarity(user.mbti, target_user.mbti)
            experience_match = 1.0 if user.game_experience == target_user.game_experience else 0.5
            style_match = 1.0 if user.game_style == target_user.game_style else 0.0
            
            # 计算每个维度的实际贡献度
            contributions = {
                'play_time': time_match * 35.9,     # 时间匹配
                'play_region': region_match * 25.6,   # 区服匹配
                'online_status': online_match * 7.7,  # 在线状态
                'game_similarity': game_similarity * 10.8,  # 游戏相似度
                'zodiac': zodiac_match * 5.0,         # 星座匹配
                'mbti': mbti_match * 5.0,           # MBTI匹配
                'game_experience': experience_match * 5.0, # 游戏经验
                'game_style': style_match * 5.0      # 游戏风格
            }
            
            # 计算总匹配度（使用固定权重）
            final_similarity = sum(contributions.values()) / 100  # 除以100转换为0-1的范围
            
            # 性别偏好调整
            if user.gender in target_user.gender_preference and target_user.gender in user.gender_preference:
                final_similarity *= 1.0
            else:
                final_similarity *= 0.5
                # 同时调整所有贡献度
                for key in contributions:
                    contributions[key] *= 0.5
            
            matches.append((user, final_similarity, contributions, possible_games))
            
        # 按相似度排序并返回前top_n个结果
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_n]
                
    def _calculate_feature_contributions(
        self,
        vector1: np.ndarray,
        vector2: np.ndarray,
        feature_names: List[str],
        total_similarity: float
    ) -> Dict[str, float]:
        """计算每个特征对最终相似度的贡献
        
        Args:
            vector1: 第一个特征向量
            vector2: 第二个特征向量
            feature_names: 特征名称列表
            total_similarity: 总相似度
            
        Returns:
            Dict[str, float]: 每个特征的贡献度
        """
        contributions = {}
        
        for i, name in enumerate(feature_names):
            if name in FEATURE_WEIGHTS:
                if vector1[i] == vector2[i]:
                    contributions[name] = FEATURE_WEIGHTS[name] * 100
                else:
                    contributions[name] = 0.0
                    
        # 确保所有特征都有贡献度值
        for feature in FEATURE_WEIGHTS:
            if feature not in contributions:
                contributions[feature] = 0.0
                
        # 标准化贡献度
        total_contribution = sum(contributions.values())
        if total_contribution > 0:
            scale_factor = total_similarity * 100 / total_contribution
            for feature in contributions:
                contributions[feature] *= scale_factor
                
        return contributions 