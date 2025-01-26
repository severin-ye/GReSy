# 导入所需的库
import numpy as np  # 用于数值计算和数组操作
from typing import List, Dict, Tuple  # 用于类型提示,增强代码可读性和维护性
from dataclasses import dataclass     # 用于创建数据类,简化类的定义
from sklearn.preprocessing import LabelEncoder, StandardScaler  # 用于将分类特征转换为数值,以及特征标准化
import pandas as pd                   # 用于数据处理和分析



@dataclass  # 使用dataclass装饰器自动生成特殊方法如__init__、__repr__等
class UserProfile:
    """用户档案类,存储用户的基本信息和偏好"""
    user_id: str                        # 用户唯一标识符
    games: List[str]                    # 用户玩的游戏列表
    gender: str                         # 用户性别
    gender_preference: List[str]        # 用户性别偏好列表
    play_region: str                    # 用户常用游戏服务器
    play_time: str                      # 用户常规游戏时间段
    mbti: str                          # 用户MBTI性格类型
    zodiac: str                        # 用户星座
    game_experience: str               # 用户游戏经验水平
    online_status: str                 # 用户在线状态
    game_style: str                    # 用户游戏风格
    
    def to_dict(self):
        """将用户档案转换为字典格式,便于后续处理"""
        return {
            'user_id': self.user_id,
            'games': self.games,
            'gender': self.gender,
            'gender_preference': self.gender_preference[0] if self.gender_preference else '不限',  # 为了保持与现有编码逻辑兼容
            'play_region': self.play_region,
            'play_time': self.play_time,
            'mbti': self.mbti,
            'zodiac': self.zodiac,
            'game_experience': self.game_experience,
            'online_status': self.online_status,
            'game_style': self.game_style
        }

class UserMatchingSystem:
    """用户匹配系统类,实现用户间的相似度计算和匹配推荐"""
    def __init__(self, debug_mode: bool = False):
        self.users: List[UserProfile] = []  # 存储系统中的所有用户
        self.debug_mode = debug_mode  # 添加调试模式标志
        # 定义各特征在匹配计算中的权重（总和为1）
        self.feature_weights = {
            'games': 0.35,              # 游戏偏好权重
            'gender': 0.20,             # 性别特征权重
            'play_region': 0.15,        # 游戏区服权重
            'play_time': 0.10,          # 游戏时间权重
            'mbti': 0.075,             # MBTI性格权重
            'zodiac': 0.025,           # 星座权重
            'game_experience': 0.075,   # 游戏经验权重
            'online_status': 0.025,     # 在线状态权重
            'game_style': 0.05          # 游戏风格权重
        }
        # 初始化各特征的标签编码器
        self.label_encoders = {
            'gender': LabelEncoder(),
            'gender_preference': LabelEncoder(),
            'play_region': LabelEncoder(),
            'play_time': LabelEncoder(),
            'mbti': LabelEncoder(),
            'zodiac': LabelEncoder(),
            'game_experience': LabelEncoder(),
            'online_status': LabelEncoder(),    # 添加在线状态编码器
            'game_style': LabelEncoder()        # 添加游戏风格编码器
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
    
    def _calculate_gender_preference_weight(self, user1: UserProfile, user2: UserProfile) -> float:
        """计算基于性别偏好的权重

        Args:
            user1: 第一个用户的完整档案（当前用户）
            user2: 第二个用户的完整档案（被匹配用户）

        Returns:
            float: 性别偏好权重值
        """
        if not user1.gender_preference:  # 如果用户没有性别偏好
            return 1.0

        try:
            # 获取被匹配用户的性别在当前用户性别偏好列表中的位置
            preference_index = user1.gender_preference.index(user2.gender)
            # 根据位置计算权重：第一名是第二名的10倍，第二名是第三名的10倍
            weight = 10 ** (len(user1.gender_preference) - 1 - preference_index)
            
            if self.debug_mode:
                print(f"性别偏好权重: {weight}")
            return weight
            
        except ValueError:
            # 如果被匹配用户的性别不在偏好列表中，权重为1
            if self.debug_mode:
                print("性别不在偏好列表中，权重为1")
            return 1.0

    def _calculate_similarity(self, user1_vector: np.ndarray, user2_vector: np.ndarray, user1: UserProfile, user2: UserProfile) -> float:
        """计算两个用户向量之间的余弦相似度，并根据性别偏好顺序调整权重
        
        Args:
            user1_vector: 第一个用户的特征向量
            user2_vector: 第二个用户的特征向量
            user1: 第一个用户的完整档案
            user2: 第二个用户的完整档案
            
        Returns:
            float: 调整后的相似度分数
        """
        if self.debug_mode:
            print("\n计算相似度:")
            print(f"用户1 ID: {user1.user_id}")
            print(f"用户2 ID: {user2.user_id}")
            print(f"用户1向量: {user1_vector}")
            print(f"用户2向量: {user2_vector}")
        
        # 处理向量中的NaN值
        mask = ~(np.isnan(user1_vector) | np.isnan(user2_vector))
        user1_vector = user1_vector[mask]
        user2_vector = user2_vector[mask]
        
        # 计算向量的范数乘积,避免除零错误
        norm_product = np.linalg.norm(user1_vector) * np.linalg.norm(user2_vector)
        if norm_product == 0:
            return 0.0
            
        # 计算基础余弦相似度并确保结果在[0,1]范围内
        base_similarity = np.dot(user1_vector, user2_vector) / norm_product
        base_similarity = (base_similarity + 1) / 2  # 将[-1,1]映射到[0,1]
        
        if self.debug_mode:
            print(f"基础相似度: {base_similarity:.4f}")
        
        # 获取性别偏好权重
        gender_preference_weight = self._calculate_gender_preference_weight(user1, user2)
        
        final_similarity = base_similarity * gender_preference_weight
        
        if self.debug_mode:
            print(f"最终相似度: {final_similarity:.4f}")
        
        return final_similarity
    
    def _calculate_feature_contributions(self, user1_vector: np.ndarray, user2_vector: np.ndarray, 
                                   feature_names: List[str], weights: List[float],
                                   user1: UserProfile, user2: UserProfile) -> Dict[str, float]:
        """计算每个特征对最终相似度的贡献
        
        Args:
            user1_vector: 第一个用户的特征向量
            user2_vector: 第二个用户的特征向量
            feature_names: 特征名称列表
            weights: 特征权重列表
            user1: 第一个用户的完整档案
            user2: 第二个用户的完整档案
            
        Returns:
            Dict[str, float]: 每个特征的贡献度字典
        """
        contributions = {}
        total_contribution = 0
        
        # 计算每个特征的贡献
        for i, (name, weight) in enumerate(zip(feature_names, weights)):
            if name == 'gender':
                # 使用新的性别偏好权重计算函数
                gender_weight = self._calculate_gender_preference_weight(user1, user2)
                contributions[name] = weight * gender_weight
                total_contribution += contributions[name]
            else:
                # 其他特征的贡献
                if user1_vector[i] == user2_vector[i] and user1_vector[i] != 0:
                    contributions[name] = weight
                    total_contribution += weight
                else:
                    contributions[name] = 0
        
        # 标准化贡献值，使总和为1
        if total_contribution > 0:
            for name in contributions:
                contributions[name] = contributions[name] / total_contribution
        
        return contributions

    def find_matches(self, target_user: UserProfile, top_n: int = 20) -> List[Tuple[UserProfile, float, Dict[str, float]]]:
        """为目标用户找到最匹配的其他用户
        
        Args:
            target_user: 目标用户档案
            top_n: 返回的最佳匹配数量
            
        Returns:
            List[Tuple[UserProfile, float, Dict[str, float]]]: 返回匹配用户、相似度和特征贡献度的列表
        """
        # 如果目标用户不在系统中,先添加
        if target_user not in self.users:
            self.add_user(target_user)
            
        # 编码所有用户特征
        df = self._encode_categorical_features()
        
        # 删除user_id列，因为它不应该参与相似度计算
        if 'user_id' in df.columns:
            df = df.drop('user_id', axis=1)
            
        # 计算每个特征的权重
        feature_weights = []
        feature_names = []
        for col in df.columns:
            if col.startswith('game_'):
                # 平均分配游戏特征的权重
                weight = self.feature_weights['games'] / len([c for c in df.columns if c.startswith('game_')])
                feature_weights.append(weight)
                feature_names.append(col)
            else:
                feature_weights.append(self.feature_weights.get(col, 0.0))
                feature_names.append(col)
        
        # 直接应用特征权重，不进行标准化
        weighted_df = df.values * np.array(feature_weights)
        
        # 获取目标用户的特征向量
        target_index = self.users.index(target_user)
        target_vector = weighted_df[target_index]
        
        # 按性别偏好优先级计算匹配结果
        all_matches = []
        for gender_pref in target_user.gender_preference:
            current_matches = []
            for i, user in enumerate(self.users):
                if i != target_index:  # 排除目标用户自身
                    if user.gender == gender_pref:
                        # 计算特征贡献度
                        contributions = self._calculate_feature_contributions(
                            df.values[target_index], 
                            df.values[i], 
                            feature_names,
                            feature_weights,
                            target_user,
                            user
                        )
                        # 计算相似度
                        similarity = self._calculate_similarity(target_vector, weighted_df[i], target_user, user)
                        current_matches.append((user, similarity, contributions))
            
            all_matches.extend(current_matches)
            if len(all_matches) >= top_n:
                break
        
        if not all_matches:
            return []
            
        return sorted(all_matches, key=lambda x: x[1], reverse=True)[:top_n]

# 示例代码
if __name__ == "__main__":
    # 创建示例用户档案
    user1 = UserProfile(
        user_id="user1",
        games=["LOL"],
        gender="男",
        gender_preference=["女", "男", "赛博人"],
        play_region="亚服",
        play_time="晚上",
        mbti="INTJ",
        zodiac="射手座",
        game_experience="高超",
        online_status="在线",
        game_style="激进"
    )
    
    user2 = UserProfile(
        user_id="user2",
        games=["LOL"],
        gender="女",
        gender_preference=["男", "女", "赛博人"],
        play_region="亚服",
        play_time="晚上",
        mbti="ENFP",
        zodiac="天蝎座",
        game_experience="初级",
        online_status="在线",
        game_style="保守"
    )
    
    # 创建并使用匹配系统
    matching_system = UserMatchingSystem(debug_mode=False)
    matching_system.add_user(user1)
    matching_system.add_user(user2)
    
    # 查找并打印匹配结果
    matches = matching_system.find_matches(user1)
    print("\n匹配结果:")
    print("=" * 50)
    for user, similarity, contributions in matches:
        print(f"总匹配度: {similarity:.2%}")
        print(f"用户ID: {user.user_id}")
        print(f"游戏: {', '.join(user.games)} (贡献: {contributions.get('game_' + user.games[0], 0):.1%})")
        print(f"性别: {user.gender} (贡献: {contributions.get('gender', 0):.1%})")
        print(f"游玩服务器: {user.play_region} (贡献: {contributions.get('play_region', 0):.1%})")
        print(f"游玩时间: {user.play_time} (贡献: {contributions.get('play_time', 0):.1%})")
        print(f"游戏经验: {user.game_experience} (贡献: {contributions.get('game_experience', 0):.1%})")
        print(f"游戏风格: {user.game_style} (贡献: {contributions.get('game_style', 0):.1%})")
        print(f"在线状态: {user.online_status} (贡献: {contributions.get('online_status', 0):.1%})")
        print(f"MBTI: {user.mbti} (贡献: {contributions.get('mbti', 0):.1%})")
        print(f"星座: {user.zodiac} (贡献: {contributions.get('zodiac', 0):.1%})")
        print("=" * 50) 