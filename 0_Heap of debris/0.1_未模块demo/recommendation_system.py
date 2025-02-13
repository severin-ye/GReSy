# 导入所需的库
import os
import numpy as np  # 用于数值计算和数组操作
from typing import List, Dict, Tuple  # 用于类型提示,增强代码可读性和维护性
from dataclasses import dataclass     # 用于创建数据类,简化类的定义
from sklearn.preprocessing import LabelEncoder, StandardScaler  # 用于将分类特征转换为数值,以及特征标准化
import pandas as pd                   # 用于数据处理和分析
from game_pool_loader import GameProfile, get_game_types_by_name, load_game_pool



@dataclass
class UserProfile:
    """用户档案类,存储用户的基本信息和偏好
    
    这个类使用@dataclass装饰器自动生成__init__等方法,用于高效地存储和管理用户的所有特征信息。
    每个字段都代表用户的一个特征维度,用于后续的匹配计算。
    """
    user_id: str                # 用户唯一标识符
    games: List[str]            # 用户玩的游戏列表
    gender: str                 # 用户性别
    gender_preference: List[str] # 用户性别偏好优先级列表
    play_region: str            # 用户常用游戏服务器
    play_time: str              # 用户常规游戏时间段
    mbti: str                   # 用户MBTI性格类型
    zodiac: str                 # 用户星座
    game_experience: str        # 用户游戏经验水平
    online_status: str          # 用户在线状态
    game_style: str             # 用户游戏风格
    
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
    """用户匹配系统类,实现用户间的相似度计算和匹配推荐
    
    主要功能：
    1. 多维度匹配：考虑游戏、性别、时间、区服等多个维度
    2. 权重系统：不同特征有不同权重
    3. 性别偏好优先级：支持用户设置性别偏好顺序
    4. 详细的匹配解释：提供每个特征的贡献度
    5. 调试模式：支持debug_mode查看详细计算过程
    """
    def __init__(self, debug_mode: bool = False, game_similarity_threshold: float = 0.5):
        """初始化匹配系统
        
        Args:
            debug_mode: 是否启用调试模式,启用后会打印详细的计算过程
            game_similarity_threshold: 游戏相似度阈值，用于筛选可能感兴趣的游戏
        """
        self.users: List[UserProfile] = []  # 存储系统中的所有用户
        self.debug_mode = debug_mode        # 调试模式标志
        self.game_similarity_threshold = game_similarity_threshold
        
        # 定义各特征在匹配计算中的权重（总和为1）
        # 每个特征的权重反映了该特征在匹配过程中的重要性
        self.feature_weights = {
            'game_type': 0.20,      # 游戏类型权重
            'play_region': 0.15,    # 游戏区服权重
            'play_time': 0.10,      # 游戏时间权重
            'mbti': 0.075,          # MBTI性格权重
            'zodiac': 0.025,        # 星座权重
            'game_experience': 0.075,# 游戏经验权重
            'online_status': 0.025,  # 在线状态权重
            'game_style': 0.05      # 游戏风格权重
        }
        
        # 初始化各特征的标签编码器,用于将分类特征转换为数值
        self.label_encoders = {
            'gender': LabelEncoder(),
            'gender_preference': LabelEncoder(),
            'play_region': LabelEncoder(),
            'play_time': LabelEncoder(),
            'mbti': LabelEncoder(),
            'zodiac': LabelEncoder(),
            'game_experience': LabelEncoder(),
            'online_status': LabelEncoder(),
            'game_style': LabelEncoder()
        }
        self.scaler = StandardScaler()  # 用于特征标准化的缩放器
        
    def add_user(self, user: UserProfile):
        """添加新用户到系统"""
        self.users.append(user)
        
    def _encode_categorical_features(self):
        """将分类特征编码为数值形式"""
        user_dicts = [user.to_dict() for user in self.users]
        df = pd.DataFrame(user_dicts)
        
        # 对每个分类特征进行编码
        for feature, encoder in self.label_encoders.items():
            if feature in df.columns:
                # 如果所有值都相同，则编码为1
                if len(df[feature].unique()) == 1:
                    df[feature] = 1
                else:
                    # 否则使用标签编码
                    df[feature] = encoder.fit_transform(df[feature])
        
        # 处理游戏列表
        all_games = set()
        for games in df['games']:
            all_games.update(games)
            
        for game in all_games:
            df[f'game_{game}'] = df['games'].apply(lambda x: 1 if game in x else 0)
            
        # 删除原始游戏列表列
        df = df.drop('games', axis=1)
        
        # 确保没有NaN值
        df = df.fillna(0)
        
        if self.debug_mode:
            print("\n编码后的特征:")
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
        """计算两个用户向量之间的余弦相似度
        
        使用余弦相似度计算用户特征向量间的相似程度。首先处理向量中的NaN值,
        然后计算向量的点积除以范数乘积,最后将结果映射到[0,1]区间。
        
        Args:
            user1_vector: 第一个用户的特征向量
            user2_vector: 第二个用户的特征向量
            user1: 第一个用户的完整档案
            user2: 第二个用户的完整档案
            
        Returns:
            float: 相似度分数,范围[0,1]
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
            
        # 计算余弦相似度并确保结果在[0,1]范围内
        similarity = np.dot(user1_vector, user2_vector) / norm_product
        similarity = (similarity + 1) / 2  # 将[-1,1]映射到[0,1]
        
        if self.debug_mode:
            print(f"相似度: {similarity:.4f}")
        
        return similarity
    
    def _calculate_feature_contributions(self, user1_vector: np.ndarray, user2_vector: np.ndarray, 
                                   feature_names: List[str], weights: List[float],
                                   user1: UserProfile, user2: UserProfile) -> Dict[str, float]:
        """计算每个特征对最终相似度的贡献
        
        计算过程：
        1. 计算每个特征的原始贡献度
        2. 标准化贡献度使其总和等于总匹配度
        3. 转换为百分比形式
        
        Returns:
            Dict[str, float]: 每个特征的贡献度百分比
        """
        # 初始化贡献度字典
        contributions = {}
        
        # 使用类的 feature_weights
        for i, name in enumerate(feature_names):
            if name in self.feature_weights:
                if user1_vector[i] == user2_vector[i]:
                    contributions[name] = self.feature_weights[name] * 100  # 转换为百分比
                else:
                    contributions[name] = 0.0
                    
        # 确保所有特征都有贡献度值
        for feature in self.feature_weights:
            if feature not in contributions:
                contributions[feature] = 0.0
                
        # 计算总贡献率
        total_contribution = sum(contributions.values())
        
        # 如果总贡献率大于0，将每个贡献标准化为总匹配度的一部分
        if total_contribution > 0:
            similarity = self._calculate_similarity(
                user1_vector * weights, 
                user2_vector * weights,
                user1,
                user2
            ) * 100  # 转换为百分比
            
            # 将每个贡献按比例缩放到总匹配度
            scale_factor = similarity / total_contribution
            for feature in contributions:
                contributions[feature] *= scale_factor
                
        return contributions

    def _calculate_game_type_similarity(self, user1: UserProfile, user2: UserProfile, games: List[GameProfile]) -> float:
        """计算两个用户之间的游戏类型相似度
        
        使用Jaccard相似度计算用户游戏类型的相似程度：
        相似度 = 交集大小 / 并集大小
        
        Args:
            user1: 第一个用户的完整档案
            user2: 第二个用户的完整档案
            games: 游戏档案列表
            
        Returns:
            float: 游戏类型相似度分数[0,1]
        """
        user1_types = set()
        user2_types = set()
        
        for game in user1.games:
            user1_types.update(get_game_types_by_name(game, games))
        for game in user2.games:
            user2_types.update(get_game_types_by_name(game, games))
        
        # 计算交集和并集
        intersection = user1_types.intersection(user2_types)
        union = user1_types.union(user2_types)
        
        # 计算Jaccard相似度
        if not union:
            return 0.0
        return len(intersection) / len(union)

    def _get_similar_games(self, user_games: List[str], games: List[GameProfile], similarity_threshold: float = 0.4) -> List[Tuple[str, float]]:
        """获取与用户当前游戏相似的其他游戏
        
        Args:
            user_games: 用户当前玩的游戏列表
            games: 所有游戏档案列表
            similarity_threshold: 游戏相似度阈值，只返回相似度高于此值的游戏
            
        Returns:
            List[Tuple[str, float]]: 返回(游戏名称, 相似度)的列表
        """
        user_game_types = set()
        for game in user_games:
            user_game_types.update(get_game_types_by_name(game, games))
            
        similar_games = []
        for game in games:
            if game.name not in user_games:  # 排除用户已经在玩的游戏
                game_types = set(game.types)
                # 使用Jaccard相似度计算游戏类型的相似程度
                intersection = len(user_game_types.intersection(game_types))
                union = len(user_game_types.union(game_types))
                similarity = intersection / union if union > 0 else 0
                
                if similarity >= similarity_threshold:
                    similar_games.append((game.name, similarity))
                    
        return sorted(similar_games, key=lambda x: x[1], reverse=True)

    def find_matches(self, target_user: UserProfile, games: List[GameProfile], top_n: int = 20) -> List[Tuple[UserProfile, float, Dict[str, float], List[Tuple[str, float]]]]:
        """为目标用户找到最匹配的其他用户
        
        匹配流程：
        1. 首先获取目标用户可能感兴趣的游戏
        2. 筛选出有共同游戏的用户（包括可能感兴趣的游戏）
        3. 计算用户特征的相似度
        4. 考虑性别偏好优先级
        5. 计算每个特征的贡献度
        6. 返回排序后的匹配结果
        
        Args:
            target_user: 目标用户档案
            games: 游戏档案列表
            top_n: 返回的最佳匹配数量
            
        Returns:
            List[Tuple[UserProfile, float, Dict[str, float], List[Tuple[str, float]]]]: 
            返回(匹配用户, 相似度, 特征贡献度, 推荐游戏列表)的列表
        """
        # 如果目标用户不在系统中,先添加
        if target_user not in self.users:
            self.add_user(target_user)
            
        # 获取目标用户可能感兴趣的游戏
        possible_games = self._get_similar_games(target_user.games, games, similarity_threshold=0.3)
        target_possible_games = [game for game, _ in possible_games]
        target_all_games = set(target_user.games + target_possible_games)
        
        # 筛选有共同游戏的用户
        matching_game_users = []
        for user in self.users:
            if user != target_user:
                # 检查是否有共同游戏
                if any(game in target_all_games for game in user.games):
                    matching_game_users.append(user)
                    
        if not matching_game_users:
            return []
            
        # 编码所有用户特征
        df = self._encode_categorical_features()
        
        # 删除user_id列和游戏相关列
        columns_to_keep = []
        for col in df.columns:
            if not col.startswith('game_') and col != 'user_id' and col != 'gender' and col != 'gender_preference':
                columns_to_keep.append(col)
                
        df = df[columns_to_keep]
            
        # 计算每个特征的权重
        feature_weights = []
        feature_names = []
        
        # 重新计算除游戏和性别外的特征权重总和
        total_remaining_weight = sum(weight for feature, weight in self.feature_weights.items() 
                                   if feature not in ['games', 'gender'])
        
        # 归一化剩余权重
        weight_scale = 1.0 / total_remaining_weight if total_remaining_weight > 0 else 0
        
        for col in df.columns:
            weight = self.feature_weights.get(col, 0.0) * weight_scale
            feature_weights.append(weight)
            feature_names.append(col)
            
        if self.debug_mode:
            print("\n特征权重:")
            for name, weight in zip(feature_names, feature_weights):
                print(f"{name}: {weight}")
            print("\n数据框列:", df.columns.tolist())
            
        # 确保权重数组维度与数据框匹配
        feature_weights = np.array(feature_weights)
        
        # 获取目标用户的特征向量
        target_index = self.users.index(target_user)
        target_vector = df.values[target_index]
        
        # 按性别偏好优先级计算匹配结果
        gender_queues = {gender: [] for gender in target_user.gender_preference}
        
        # 计算匹配游戏用户的相似度并按性别分类
        for user in matching_game_users:
            user_index = self.users.index(user)
            
            # 计算游戏类型相似度
            game_type_similarity = self._calculate_game_type_similarity(target_user, user, games)
            
            # 计算特征贡献度
            contributions = self._calculate_feature_contributions(
                target_vector,
                df.values[user_index],
                feature_names,
                feature_weights,
                target_user,
                user
            )
            
            # 计算加权向量
            weighted_target = target_vector * feature_weights
            weighted_other = df.values[user_index] * feature_weights
            
            # 计算总体相似度
            similarity = self._calculate_similarity(weighted_target, weighted_other, target_user, user)
            
            # 将游戏类型相似度加入总相似度
            similarity = (similarity + game_type_similarity) / 2  # 平均两种相似度
            
            # 将用户添加到对应性别的队列中
            if user.gender in gender_queues:
                gender_queues[user.gender].append((user, similarity, contributions))
        
        # 按照性别偏好顺序和相似度排序添加匹配结果
        all_matches = []
        remaining_slots = top_n
        
        for gender in target_user.gender_preference:
            if remaining_slots <= 0:
                break
                
            # 对当前性别的用户按相似度排序
            current_gender_matches = sorted(gender_queues[gender], key=lambda x: x[1], reverse=True)
            
            # 添加当前性别的匹配结果，但不超过剩余槽位
            all_matches.extend(current_gender_matches[:remaining_slots])
            remaining_slots -= len(current_gender_matches[:remaining_slots])
        
        # 修改返回结果，加入相似游戏信息
        all_matches = [(user, similarity, contributions, possible_games) 
                      for user, similarity, contributions in all_matches]
        
        return all_matches

# 示例代码
if __name__ == "__main__":
    # 创建多个不同游戏偏好的用户档案
    user1 = UserProfile(
        user_id="user1",
        games=["英雄联盟", "王者荣耀"],  # MOBA玩家
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
        games=["和平精英", "CS:GO"],  # FPS生存游戏玩家
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

    user3 = UserProfile(
        user_id="user3",
        games=["原神", "崩坏：星穹铁道"],  # RPG玩家
        gender="女",
        gender_preference=["女", "男", "赛博人"],
        play_region="国服",
        play_time="下午",
        mbti="INFJ",
        zodiac="双子座",
        game_experience="中级",
        online_status="在线",
        game_style="探索"
    )

    user4 = UserProfile(
        user_id="user4",
        games=["第五人格", "我的世界"],  # 休闲生存类玩家
        gender="男",
        gender_preference=["女", "男", "赛博人"],
        play_region="国际服",
        play_time="凌晨",
        mbti="ESTP",
        zodiac="处女座",
        game_experience="高级",
        online_status="离线",
        game_style="休闲"
    )
    
    # 创建并使用匹配系统
    matching_system = UserMatchingSystem(debug_mode=False)  # 关闭调试模式
    matching_system.add_user(user1)
    matching_system.add_user(user2)
    matching_system.add_user(user3)
    matching_system.add_user(user4)
    
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建完整的文件路径，指向 data/json 目录
    game_pool_path = os.path.join(current_dir, "data", "json", "game_pool.json")
    
    # 加载游戏池
    games = load_game_pool(game_pool_path)
    
    # 只为user1进行匹配测试
    test_user = user1
    
    # 获取当前用户可能感兴趣的游戏
    possible_games = matching_system._get_similar_games(test_user.games, games, similarity_threshold=0.3)  # 降低相似度阈值
    current_games = ', '.join(test_user.games)
    similar_games_str = ', '.join([f"{game}(可能, {sim:.2%})" 
                                 for game, sim in possible_games])
    
    print(f"\n为用户 {test_user.user_id}")
    if similar_games_str:
        print(f"当前游戏: {current_games}")
        print(f"可能感兴趣的游戏: {similar_games_str}")
    else:
        print(f"当前游戏: {current_games}")
    print("匹配结果:")
    print("=" * 50)
    
    matches = matching_system.find_matches(test_user, games)
    
    for user, similarity, contributions, _ in matches:
        print(f"总匹配度: {similarity:.2%}")
        print(f"用户ID: {user.user_id}")
        print(f"游戏: {', '.join(user.games)}")
        print(f"性别: {user.gender}")
        print(f"游玩服务器: {user.play_region} (贡献: {contributions.get('play_region', 0):.1f}%)")
        print(f"游玩时间: {user.play_time} (贡献: {contributions.get('play_time', 0):.1f}%)")
        print(f"游戏经验: {user.game_experience} (贡献: {contributions.get('game_experience', 0):.1f}%)")
        print(f"游戏风格: {user.game_style} (贡献: {contributions.get('game_style', 0):.1f}%)")
        print(f"在线状态: {user.online_status} (贡献: {contributions.get('online_status', 0):.1f}%)")
        print(f"MBTI: {user.mbti} (贡献: {contributions.get('mbti', 0):.1f}%)")
        print(f"星座: {user.zodiac} (贡献: {contributions.get('zodiac', 0):.1f}%)")
        print("-" * 50)