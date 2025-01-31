"""核心匹配器模块

实现用户匹配的核心逻辑
"""

from typing import List, Tuple, Dict, Set
import numpy as np
from models.user_profile import UserProfile
from models.game_profile import GameProfile
from matching.feature_processor import FeatureProcessor
from matching.similarity_calculator import (
    calculate_cosine_similarity,
    calculate_game_type_similarity,
    calculate_gender_preference_weight
)
from config.weights import FEATURE_WEIGHTS, GAME_SIMILARITY_THRESHOLD
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
            user_game_types.update(
                DataLoader.get_game_types_by_name(game, games)
            )
            
        similar_games = []
        for game in games:
            if game.name not in user_games:
                game_types = set(game.types)
                similarity = calculate_game_type_similarity(
                    user_game_types,
                    game_types
                )
                
                if similarity >= similarity_threshold:
                    similar_games.append((game.name, similarity))
                    
        return sorted(similar_games, key=lambda x: x[1], reverse=True)
        
    def find_matches(
        self,
        target_user: UserProfile,
        games: List[GameProfile],
        top_n: int = 20
    ) -> List[Tuple[UserProfile, float, Dict[str, float], List[Tuple[str, float]]]]:
        """为目标用户找到最匹配的其他用户
        
        Args:
            target_user: 目标用户档案
            games: 游戏档案列表
            top_n: 返回的最佳匹配数量
            
        Returns:
            List[Tuple[UserProfile, float, Dict[str, float], List[Tuple[str, float]]]]:
            返回(匹配用户, 相似度, 特征贡献度, 推荐游戏列表)的列表
        """
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
            
        # 处理用户特征
        df = self.feature_processor.encode_categorical_features(self.users)
        df = self.feature_processor.normalize_features(df)
        
        # 获取目标用户的特征向量
        target_index = self.users.index(target_user)
        target_vector = self.feature_processor.get_feature_vector(df, target_index)
        
        # 按性别偏好优先级计算匹配结果
        matches = []
        for user in matching_game_users:
            user_index = self.users.index(user)
            user_vector = self.feature_processor.get_feature_vector(df, user_index)
            
            # 计算特征相似度
            similarity = calculate_cosine_similarity(target_vector, user_vector)
            
            # 计算游戏类型相似度
            user_game_types = set()
            target_game_types = set()
            for game in user.games:
                user_game_types.update(DataLoader.get_game_types_by_name(game, games))
            for game in target_user.games:
                target_game_types.update(DataLoader.get_game_types_by_name(game, games))
                
            game_similarity = calculate_game_type_similarity(
                target_game_types,
                user_game_types
            )
            
            # 计算性别偏好权重
            gender_weight = calculate_gender_preference_weight(target_user, user)
            
            # 计算最终相似度
            final_similarity = (similarity + game_similarity) / 2 * gender_weight
            
            # 计算特征贡献度
            contributions = self._calculate_feature_contributions(
                target_vector,
                user_vector,
                df.columns,
                final_similarity
            )
            
            matches.append((user, final_similarity, contributions))
            
        # 按相似度排序并返回前top_n个结果
        matches.sort(key=lambda x: x[1], reverse=True)
        return [(user, sim, contrib, possible_games) 
                for user, sim, contrib in matches[:top_n]]
                
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