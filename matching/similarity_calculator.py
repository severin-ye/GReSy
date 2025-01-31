"""相似度计算模块

提供各种相似度计算方法
"""

import numpy as np
from typing import List, Set
from models.user_profile import UserProfile
from models.game_profile import GameProfile

def calculate_cosine_similarity(vector1: np.ndarray, vector2: np.ndarray) -> float:
    """计算两个向量的余弦相似度
    
    Args:
        vector1: 第一个特征向量
        vector2: 第二个特征向量
        
    Returns:
        float: 相似度分数[0,1]
    """
    # 处理向量中的NaN值
    mask = ~(np.isnan(vector1) | np.isnan(vector2))
    vector1 = vector1[mask]
    vector2 = vector2[mask]
    
    # 计算向量的范数乘积
    norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    if norm_product == 0:
        return 0.0
        
    # 计算余弦相似度并映射到[0,1]区间
    similarity = np.dot(vector1, vector2) / norm_product
    return (similarity + 1) / 2

def calculate_game_type_similarity(user1_types: Set[str], user2_types: Set[str]) -> float:
    """计算两个用户的游戏类型相似度
    
    使用Jaccard相似度计算用户游戏类型的相似程度
    
    Args:
        user1_types: 第一个用户的游戏类型集合
        user2_types: 第二个用户的游戏类型集合
        
    Returns:
        float: 游戏类型相似度分数[0,1]
    """
    if not user1_types or not user2_types:
        return 0.0
        
    intersection = user1_types.intersection(user2_types)
    union = user1_types.union(user2_types)
    
    return len(intersection) / len(union)

def calculate_gender_preference_weight(user1: UserProfile, user2: UserProfile) -> float:
    """计算基于性别偏好的权重
    
    Args:
        user1: 第一个用户的档案（当前用户）
        user2: 第二个用户的档案（被匹配用户）
        
    Returns:
        float: 性别偏好权重值
    """
    from config.weights import GENDER_PREFERENCE_WEIGHT_SCALE
    
    if not user1.gender_preference:
        return 1.0
        
    try:
        preference_index = user1.gender_preference.index(user2.gender)
        return GENDER_PREFERENCE_WEIGHT_SCALE ** (len(user1.gender_preference) - 1 - preference_index)
    except ValueError:
        return 1.0 