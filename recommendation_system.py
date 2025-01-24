# 导入所需的库
import numpy as np
from typing import List, Dict, Tuple  # 用于类型提示
from dataclasses import dataclass     # 用于创建数据类
from sklearn.preprocessing import LabelEncoder, StandardScaler  # 用于特征编码和归一化
import pandas as pd                   # 用于数据处理

@dataclass
class UserProfile:
    """用户档案类,存储用户的基本信息"""
    games: List[str]                    # 游戏列表
    gender: str                         # 性别
    gender_preference: str              # 性别倾向
    play_region: str                    # 游玩地区
    play_time: str                      # 游玩时间
    mbti: str                          # MBTI性格类型
    zodiac: str                        # 星座
    game_experience: str               # 游戏经验（改为字符串类型）
    
    def to_dict(self):
        """将用户档案转换为字典格式"""
        return {
            'games': self.games,
            'gender': self.gender,
            'gender_preference': self.gender_preference,
            'play_region': self.play_region,
            'play_time': self.play_time,
            'mbti': self.mbti,
            'zodiac': self.zodiac,
            'game_experience': self.game_experience
        }

class UserMatchingSystem:
    """用户匹配系统类"""
    def __init__(self):
        self.users: List[UserProfile] = []
        # 定义特征权重
        self.feature_weights = {
            'games': 0.25,
            'gender': 0.1,
            'gender_preference': 0.15,
            'play_region': 0.2,
            'play_time': 0.15,
            'mbti': 0.075,
            'zodiac': 0.025,
            'game_experience': 0.05
        }
        # 初始化编码器
        self.label_encoders = {
            'gender': LabelEncoder(),
            'gender_preference': LabelEncoder(),
            'play_region': LabelEncoder(),
            'play_time': LabelEncoder(),
            'mbti': LabelEncoder(),
            'zodiac': LabelEncoder(),
            'game_experience': LabelEncoder()
        }
        self.scaler = StandardScaler()
        
    def add_user(self, user: UserProfile):
        """添加新用户到系统"""
        self.users.append(user)
        
    def _encode_categorical_features(self):
        """将分类特征编码为数值形式"""
        user_dicts = [user.to_dict() for user in self.users]
        df = pd.DataFrame(user_dicts)
        
        # 对分类特征进行编码
        for feature, encoder in self.label_encoders.items():
            if feature in df.columns:
                df[feature] = encoder.fit_transform(df[feature])
        
        # 处理游戏列表（One-Hot编码）
        all_games = set()
        for games in df['games']:
            all_games.update(games)
            
        for game in all_games:
            df[f'game_{game}'] = df['games'].apply(lambda x: 1 if game in x else 0)
            
        df = df.drop('games', axis=1)
        return df
    
    def _calculate_similarity(self, user1_vector: np.ndarray, user2_vector: np.ndarray) -> float:
        """计算两个用户向量之间的余弦相似度"""
        # 避免除零错误
        norm_product = np.linalg.norm(user1_vector) * np.linalg.norm(user2_vector)
        if norm_product == 0:
            return 0.0
        return np.dot(user1_vector, user2_vector) / norm_product
    
    def find_matches(self, target_user: UserProfile, top_n: int = 5) -> List[Tuple[UserProfile, float]]:
        """为目标用户找到最匹配的其他用户"""
        if target_user not in self.users:
            self.add_user(target_user)
            
        # 编码特征
        df = self._encode_categorical_features()
        
        # 计算特征权重
        feature_weights = []
        for col in df.columns:
            if col.startswith('game_'):
                feature_weights.append(self.feature_weights['games'] / len([c for c in df.columns if c.startswith('game_')]))
            else:
                feature_weights.append(self.feature_weights.get(col, 0.0))
        
        # 标准化特征
        normalized_df = self.scaler.fit_transform(df)
        
        # 应用权重
        weighted_df = normalized_df * np.array(feature_weights)
        
        # 获取目标用户向量
        target_index = self.users.index(target_user)
        target_vector = weighted_df[target_index]
        
        # 计算相似度
        similarities = []
        for i, user in enumerate(self.users):
            if i != target_index:
                similarity = self._calculate_similarity(target_vector, weighted_df[i])
                similarities.append((user, similarity))
        
        # 返回最匹配的用户
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]

# 示例代码
if __name__ == "__main__":
    # 创建示例用户档案
    user1 = UserProfile(
        games=["LOL", "PUBG"],
        gender="男",
        gender_preference="男",
        play_region="亚服",
        play_time="晚上",
        mbti="INTJ",
        zodiac="射手座",
        game_experience="5年"
    )
    
    user2 = UserProfile(
        games=["LOL", "CSGO"],
        gender="女",
        gender_preference="女",
        play_region="亚服",
        play_time="晚上",
        mbti="ENFP",
        zodiac="天蝎座",
        game_experience="3年"
    )
    
    # 创建并使用匹配系统
    matching_system = UserMatchingSystem()
    matching_system.add_user(user1)
    matching_system.add_user(user2)
    
    # 查找并打印匹配结果
    matches = matching_system.find_matches(user1)
    for user, similarity in matches:
        print(f"匹配度: {similarity:.2f}")
        print(f"游戏: {user.games}")
        print(f"性别: {user.gender}")
        print(f"性别倾向: {user.gender_preference}")
        print(f"游玩地区: {user.play_region}")
        print(f"游玩时间: {user.play_time}")
        print(f"MBTI: {user.mbti}")
        print(f"星座: {user.zodiac}")
        print(f"游戏经验: {user.game_experience}")
        print("-------------------") 
    
    