"""特征权重配置文件

定义系统中各个特征的权重配置，用于匹配计算
"""

FEATURE_WEIGHTS = {
    'game_type': 0.20,      # 游戏类型权重
    'play_region': 0.15,    # 游戏区服权重
    'play_time': 0.10,      # 游戏时间权重
    'mbti': 0.075,          # MBTI性格权重
    'zodiac': 0.025,        # 星座权重
    'game_experience': 0.075,# 游戏经验权重
    'online_status': 0.025,  # 在线状态权重
    'game_style': 0.05      # 游戏风格权重
}

# 游戏相似度阈值配置
GAME_SIMILARITY_THRESHOLD = 0.5

# 性别偏好权重配置
GENDER_PREFERENCE_WEIGHT_SCALE = 10  # 每个优先级级别的权重倍数 