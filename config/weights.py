"""权重配置文件

定义各个维度的权重配置
"""

# 游戏类型相关性矩阵
GAME_TYPE_CORRELATIONS = {
    'MOBA': {
        'MOBA': 1.0,
        'RTS': 0.8,
        'FPS': 0.6,
        'RPG': 0.4,
        'CASUAL': 0.2
    },
    'RTS': {
        'MOBA': 0.8,
        'RTS': 1.0,
        'FPS': 0.6,
        'RPG': 0.4,
        'CASUAL': 0.2
    },
    'FPS': {
        'MOBA': 0.6,
        'RTS': 0.6,
        'FPS': 1.0,
        'RPG': 0.4,
        'CASUAL': 0.2
    },
    'RPG': {
        'MOBA': 0.4,
        'RTS': 0.4,
        'FPS': 0.4,
        'RPG': 1.0,
        'CASUAL': 0.6
    },
    'CASUAL': {
        'MOBA': 0.2,
        'RTS': 0.2,
        'FPS': 0.2,
        'RPG': 0.6,
        'CASUAL': 1.0
    }
}

# 游戏相似度权重
GAME_SIMILARITY_WEIGHTS = {
    'type_similarity': 0.4,      # 游戏类型相似度权重
    'preference_similarity': 0.4, # 游戏偏好相似度权重
    'social_similarity': 0.2      # 社交属性相似度权重
}

# 时间匹配权重
TIME_MATCH_WEIGHTS = {
    'exact': 1.0,    # 完全匹配
    'adjacent': 0.7, # 相邻时间段
    'opposite': 0.3  # 其他情况
}

# 区服匹配权重
REGION_MATCH_WEIGHTS = {
    'exact': 1.0,  # 完全匹配
    'close': 0.7,  # 同区域组
    'far': 0.3     # 跨区域组
}

# 游戏经验匹配权重
EXPERIENCE_MATCH_WEIGHTS = {
    'exact': 1.0,    # 完全匹配
    'adjacent': 0.7, # 相邻等级
    'far': 0.3       # 差距较大
}

# MBTI维度权重
MBTI_WEIGHTS = {
    'I/E': 0.3,  # 内向/外向
    'N/S': 0.2,  # 直觉/感知
    'T/F': 0.3,  # 思考/感受
    'J/P': 0.2   # 判断/知觉
}

# 性别偏好权重衰减因子
GENDER_PREFERENCE_SCALE = 0.7

# 各维度在总分中的权重
DIMENSION_WEIGHTS = {
    # 基础匹配维度
    'online_status': 5,  # 在线状态
    'server': 10,        # 服务器
    
    # 数值相似度维度
    'time': 15,         # 时间匹配
    'experience': 10,    # 经验匹配
    'style': 10,        # 风格匹配
    
    # 偏好匹配维度
    'mbti': 10,         # MBTI匹配
    'zodiac': 5,        # 星座匹配
    'gender': 10,       # 性别偏好
    
    # 游戏匹配维度
    'game_type': 10,        # 游戏类型
    'game_preference': 10,  # 游戏偏好
    'game_social': 5        # 游戏社交
}

# 游戏平台权重
PLATFORM_WEIGHTS = {
    '手游': 1.0,
    '端游': 0.8,
    '主机': 0.6
}

# 游戏相似度阈值
GAME_SIMILARITY_THRESHOLD = 0.4  # 提高阈值以匹配旧版本 