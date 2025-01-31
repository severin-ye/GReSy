"""相似度计算模块

提供各种相似度计算方法
"""

import numpy as np
from typing import List, Set, Dict
from models.user_profile import UserProfile
from models.game_profile import GameProfile
from config.weights import (
    GAME_TYPE_CORRELATIONS,
    TIME_MATCH_WEIGHTS,
    REGION_MATCH_WEIGHTS,
    EXPERIENCE_MATCH_WEIGHTS,
    GENDER_PREFERENCE_SCALE,
    MBTI_WEIGHTS
)

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
    vector1, vector2 = vector1[mask], vector2[mask]
    
    # 计算向量的范数乘积
    norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    if norm_product == 0:
        return 0.0
        
    # 计算余弦相似度并映射到[0,1]区间
    similarity = np.dot(vector1, vector2) / norm_product
    return (similarity + 1) / 2

def calculate_game_type_similarity(user1_types: Set[str], user2_types: Set[str]) -> float:
    """计算游戏类型相似度，考虑类型间的相关性"""
    if not user1_types or not user2_types:
        return 0.0
        
    total_correlation = 0.0
    count = 0
    
    for type1 in user1_types:
        for type2 in user2_types:
            if type1 in GAME_TYPE_CORRELATIONS and type2 in GAME_TYPE_CORRELATIONS[type1]:
                total_correlation += GAME_TYPE_CORRELATIONS[type1][type2]
                count += 1
            elif type1 == type2:
                total_correlation += 1.0
                count += 1
            else:
                total_correlation += 0.1  # 默认相关性
                count += 1
                
    return total_correlation / count if count > 0 else 0.0

def calculate_time_similarity(time1: str, time2: str) -> float:
    """计算时间匹配度"""
    time_periods = ['早上', '中午', '下午', '晚上', '凌晨']
    if time1 == time2:
        return TIME_MATCH_WEIGHTS['exact']
        
    idx1 = time_periods.index(time1)
    idx2 = time_periods.index(time2)
    
    # 计算时间段距离
    distance = min(abs(idx1 - idx2), len(time_periods) - abs(idx1 - idx2))
    
    if distance == 1:
        return TIME_MATCH_WEIGHTS['adjacent']
    return TIME_MATCH_WEIGHTS['opposite']

def calculate_region_similarity(region1: str, region2: str) -> float:
    """计算区服匹配度"""
    if region1 == region2:
        return REGION_MATCH_WEIGHTS['exact']
        
    # 定义区服组
    asia_servers = {'国服', '亚服'}
    western_servers = {'美服', '欧服'}
    
    if (region1 in asia_servers and region2 in asia_servers) or \
       (region1 in western_servers and region2 in western_servers):
        return REGION_MATCH_WEIGHTS['close']
        
    return REGION_MATCH_WEIGHTS['far']

def calculate_experience_similarity(exp1: str, exp2: str) -> float:
    """计算游戏经验匹配度"""
    if exp1 == exp2:
        return EXPERIENCE_MATCH_WEIGHTS['exact']
        
    experience_levels = ['初级', '中级', '高级', '高超']
    idx1 = experience_levels.index(exp1)
    idx2 = experience_levels.index(exp2)
    
    if abs(idx1 - idx2) == 1:
        return EXPERIENCE_MATCH_WEIGHTS['adjacent']
    return EXPERIENCE_MATCH_WEIGHTS['far']

def calculate_mbti_similarity(mbti1: str, mbti2: str) -> float:
    """计算MBTI性格匹配度"""
    if mbti1 == mbti2:
        return 1.0
        
    similarity = 0.0
    for i, (dim, weight) in enumerate(MBTI_WEIGHTS.items()):
        if mbti1[i] == mbti2[i]:
            similarity += weight
            
    return similarity

def calculate_gender_preference_weight(user1: UserProfile, user2: UserProfile) -> float:
    """计算性别偏好权重"""
    if not user1.gender_preference or not user2.gender_preference:
        return 1.0
        
    # 计算双向性别偏好
    try:
        u1_preference = user1.gender_preference.index(user2.gender)
        u2_preference = user2.gender_preference.index(user1.gender)
        
        # 使用几何平均和较小的缩放因子
        u1_weight = GENDER_PREFERENCE_SCALE ** (len(user1.gender_preference) - 1 - u1_preference)
        u2_weight = GENDER_PREFERENCE_SCALE ** (len(user2.gender_preference) - 1 - u2_preference)
        
        return (u1_weight * u2_weight) ** 0.5
        
    except ValueError:
        return 0.5  # 如果性别不在偏好列表中，给予中等权重

def calculate_game_social_similarity(user1: UserProfile, user2: UserProfile) -> float:
    """计算游戏社交属性相似度"""
    # 计算在线状态匹配度
    online_match = 1.0 if user1.online_status == user2.online_status else 0.5
    
    # 计算游戏风格匹配度
    style_match = 1.0 if user1.game_style == user2.game_style else 0.5
    
    # 计算游戏经验匹配度
    exp_match = calculate_experience_similarity(user1.game_experience, user2.game_experience)
    
    return (online_match * 0.3 + style_match * 0.3 + exp_match * 0.4) 