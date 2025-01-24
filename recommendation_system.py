# 导入所需的库
import numpy as np  # 用于数值计算和数组操作
from typing import List, Dict, Tuple  # 用于类型提示,增强代码可读性和维护性
from dataclasses import dataclass     # 用于创建数据类,简化类的定义
from sklearn.preprocessing import LabelEncoder, StandardScaler  # 用于将分类特征转换为数值,以及特征标准化
import pandas as pd                   # 用于数据处理和分析

@dataclass  # 使用dataclass装饰器自动生成特殊方法如__init__、__repr__等
class UserProfile:
    """用户档案类,存储用户的基本信息和偏好"""
    games: List[str]                    # 用户玩的游戏列表
    gender: str                         # 用户性别
    gender_preference: List[str]        # 用户性别偏好列表
    play_region: str                    # 用户常用游戏服务器
    play_time: str                      # 用户常规游戏时间段
    mbti: str                          # 用户MBTI性格类型
    zodiac: str                        # 用户星座
    game_experience: str               # 用户游戏经验水平
    
    def to_dict(self):
        """将用户档案转换为字典格式,便于后续处理"""
        return {
            'games': self.games,
            'gender': self.gender,
            'gender_preference': self.gender_preference[0] if self.gender_preference else '不限',  # 为了保持与现有编码逻辑兼容
            'play_region': self.play_region,
            'play_time': self.play_time,
            'mbti': self.mbti,
            'zodiac': self.zodiac,
            'game_experience': self.game_experience
        }

class UserMatchingSystem:
    """用户匹配系统类,实现用户间的相似度计算和匹配推荐"""
    def __init__(self, debug_mode: bool = False):
        self.users: List[UserProfile] = []  # 存储系统中的所有用户
        self.debug_mode = debug_mode  # 添加调试模式标志
        # 定义各特征在匹配计算中的权重（总和为1）
        self.feature_weights = {
            'games': 0.40,              # 游戏偏好权重最高
            'gender': 0.05,             # 性别特征权重
            'gender_preference': 0.10,   # 性别偏好权重
            'play_region': 0.15,        # 游戏区服权重
            'play_time': 0.15,          # 游戏时间权重
            'mbti': 0.075,             # MBTI性格权重
            'zodiac': 0.025,           # 星座权重最低
            'game_experience': 0.05     # 游戏经验权重
        }
        # 初始化各特征的标签编码器
        self.label_encoders = {
            'gender': LabelEncoder(),           # 性别编码器
            'gender_preference': LabelEncoder(), # 性别偏好编码器
            'play_region': LabelEncoder(),      # 游戏区服编码器
            'play_time': LabelEncoder(),        # 游戏时间编码器
            'mbti': LabelEncoder(),            # MBTI编码器
            'zodiac': LabelEncoder(),          # 星座编码器
            'game_experience': LabelEncoder()   # 游戏经验编码器
        }
        self.scaler = StandardScaler()  # 用于特征标准化的缩放器
        
    def add_user(self, user: UserProfile):
        """添加新用户到系统"""
        self.users.append(user)
        
    def _encode_categorical_features(self):
        """将分类特征编码为数值形式"""
        user_dicts = [user.to_dict() for user in self.users]
        df = pd.DataFrame(user_dicts)
        
        # 修改编码方式，处理特殊情况
        for feature, encoder in self.label_encoders.items():
            if feature in df.columns:
                unique_values = len(set(df[feature]))
                if unique_values == 1:
                    # 如果所有值都相同，则编码为1
                    df[feature] = 1.0
                else:
                    # 否则使用0到1之间的均匀分布值
                    df[feature] = encoder.fit_transform(df[feature]) / (unique_values - 1)
        
        # 游戏列表处理保持不变
        all_games = set()
        for games in df['games']:
            all_games.update(games)
            
        for game in all_games:
            df[f'game_{game}'] = df['games'].apply(lambda x: 1 if game in x else 0)
            
        df = df.drop('games', axis=1)
        
        # 确保没有NaN值
        df = df.fillna(0)  # 将任何NaN值替换为0
        
        if self.debug_mode:
            print("\n特征编码后的数据:")
            print(df)
        
        return df
    
    def _calculate_similarity(self, user1_vector: np.ndarray, user2_vector: np.ndarray) -> float:
        """计算两个用户向量之间的余弦相似度"""
        # 处理向量中的NaN值
        mask = ~(np.isnan(user1_vector) | np.isnan(user2_vector))
        user1_vector = user1_vector[mask]
        user2_vector = user2_vector[mask]
        
        # 计算向量的范数乘积,避免除零错误
        norm_product = np.linalg.norm(user1_vector) * np.linalg.norm(user2_vector)
        if norm_product == 0:
            return 0.0
            
        # 计算余弦相似度并确保结果在[0,1]范围内
        similarity = np.dot(user1_vector, user2_vector) / norm_product
        return (similarity + 1) / 2
    
    def find_matches(self, target_user: UserProfile, top_n: int = 20) -> List[Tuple[UserProfile, float]]:
        """为目标用户找到最匹配的其他用户
        
        Args:
            target_user: 目标用户档案
            top_n: 返回的最佳匹配数量
            
        Returns:
            List[Tuple[UserProfile, float]]: 返回匹配用户和相似度的列表
        """
        # 如果目标用户不在系统中,先添加
        if target_user not in self.users:
            self.add_user(target_user)
            
        # 编码所有用户特征
        df = self._encode_categorical_features()
        
        # 计算每个特征的权重
        feature_weights = []
        for col in df.columns:
            if col.startswith('game_'):
                # 平均分配游戏特征的权重
                feature_weights.append(self.feature_weights['games'] / len([c for c in df.columns if c.startswith('game_')]))
            else:
                feature_weights.append(self.feature_weights.get(col, 0.0))
        
        # 标准化特征
        normalized_df = self.scaler.fit_transform(df)
        
        # 应用特征权重
        weighted_df = normalized_df * np.array(feature_weights)
        
        if self.debug_mode:
            print("\n标准化后的数据:")
            print(pd.DataFrame(normalized_df, columns=df.columns))
            
            print("\n特征权重:")
            for col, weight in zip(df.columns, feature_weights):
                print(f"{col}: {weight}")
                
            print("\n加权后的数据:")
            print(pd.DataFrame(weighted_df, columns=df.columns))
        
        # 获取目标用户的特征向量
        target_index = self.users.index(target_user)
        target_vector = weighted_df[target_index]
        
        # 按性别偏好优先级计算匹配结果
        all_matches = []
        for gender_pref in target_user.gender_preference:
            # 计算目标用户与其他用户的相似度
            current_matches = []
            for i, user in enumerate(self.users):
                if i != target_index:  # 排除目标用户自身
                    # 检查性别是否符合当前偏好
                    if user.gender == gender_pref:
                        similarity = self._calculate_similarity(target_vector, weighted_df[i])
                        if self.debug_mode:
                            print(f"\n计算用户 {i} 的相似度:")
                            print(f"目标用户向量: {target_vector}")
                            print(f"比较用户向量: {weighted_df[i]}")
                            print(f"相似度结果: {similarity}")
                        current_matches.append((user, similarity))
            
            # 将当前性别偏好的匹配结果添加到总结果中
            all_matches.extend(current_matches)
            
            # 如果已经找到足够的匹配，就不再继续查找下一个性别偏好
            if len(all_matches) >= top_n:
                break
        
        # 如果没有找到任何匹配，返回空列表
        if not all_matches:
            return []
            
        # 按相似度排序并返回前top_n个结果
        return sorted(all_matches, key=lambda x: x[1], reverse=True)[:top_n]

# 示例代码
if __name__ == "__main__":
    # 创建示例用户档案
    user1 = UserProfile(
        games=["LOL", "PUBG"],
        gender="男",
        gender_preference=["男"],
        play_region="亚服",
        play_time="晚上",
        mbti="INTJ",
        zodiac="射手座",
        game_experience="高超"
    )
    
    user2 = UserProfile(
        games=["LOL", "CSGO"],
        gender="女",
        gender_preference=["女"],
        play_region="亚服",
        play_time="晚上",
        mbti="ENFP",
        zodiac="天蝎座",
        game_experience="初级"
    )
    
    # 创建并使用匹配系统
    matching_system = UserMatchingSystem(debug_mode=False)
    matching_system.add_user(user1)
    matching_system.add_user(user2)
    
    # 查找并打印匹配结果
    matches = matching_system.find_matches(user1)
    print("\n最终匹配结果:")
    print("-------------------")
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