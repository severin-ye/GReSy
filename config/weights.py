"""特征权重配置文件

定义系统中各个特征的权重配置，用于匹配计算
"""

# 主要特征权重
FEATURE_WEIGHTS = {
    'time_region': 0.45,       # 时间和区服匹配
    'game_similarity': 0.30,   # 游戏相关性
    'online_status': 0.15,     # 在线状态
    'personality': 0.05,       # 性格特征(MBTI)
    'gender_match': 0.05       # 性别匹配
}

# 游戏相似度计算权重
GAME_SIMILARITY_WEIGHTS = {
    'type_similarity': 0.6,     # 游戏类型相似度权重
    'preference_similarity': 0.3,# 游戏偏好相似度权重
    'social_similarity': 0.1    # 游戏社交属性相似度权重
}

# MBTI维度权重
MBTI_WEIGHTS = {
    'I/E': 0.3,  # 内向/外向
    'N/S': 0.3,  # 直觉/感知
    'T/F': 0.2,  # 思考/感受
    'J/P': 0.2   # 判断/知觉
}

# 游戏类型相关性矩阵
GAME_TYPE_CORRELATIONS = {
    'MOBA': {
        'MOBA': 1.0,
        'FPS': 0.4,
        'RPG': 0.3,
        '竞技': 0.8,
        '生存': 0.3
    },
    'FPS': {
        'FPS': 1.0,
        'MOBA': 0.4,
        'RPG': 0.2,
        '竞技': 0.8,
        '生存': 0.7
    },
    'RPG': {
        'RPG': 1.0,
        'MOBA': 0.3,
        'FPS': 0.2,
        '竞技': 0.3,
        '生存': 0.4
    },
    '竞技': {
        '竞技': 1.0,
        'MOBA': 0.8,
        'FPS': 0.8,
        'RPG': 0.3,
        '生存': 0.5
    },
    '生存': {
        '生存': 1.0,
        'MOBA': 0.3,
        'FPS': 0.7,
        'RPG': 0.4,
        '竞技': 0.5
    }
}

# 游戏平台权重
PLATFORM_WEIGHTS = {
    '手游': 1.0,
    '端游': 0.8,
    '主机': 0.6
}

# 时间匹配权重
TIME_MATCH_WEIGHTS = {
    'exact': 1.0,      # 完全匹配
    'adjacent': 0.7,   # 相邻时段
    'opposite': 0.3    # 相反时段
}

# 区服匹配权重
REGION_MATCH_WEIGHTS = {
    'exact': 1.0,      # 完全匹配
    'close': 0.7,      # 相近区服
    'far': 0.3        # 远距离区服
}

# 游戏经验匹配权重
EXPERIENCE_MATCH_WEIGHTS = {
    'exact': 1.0,      # 完全匹配
    'adjacent': 0.7,   # 相邻级别
    'far': 0.3        # 差距较大
}

# 性别偏好权重缩放因子
GENDER_PREFERENCE_SCALE = 1.5  # 降低原来的差距

# 游戏相似度阈值
GAME_SIMILARITY_THRESHOLD = 0.4  # 提高阈值以匹配旧版本 