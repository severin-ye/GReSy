"""特征处理模块

负责用户特征的编码、标准化和处理
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from sklearn.preprocessing import LabelEncoder, StandardScaler
from models.user_profile import UserProfile

class FeatureProcessor:
    """特征处理器类
    
    负责：
    1. 分类特征编码
    2. 特征标准化
    3. 特征向量生成
    """
    
    def __init__(self):
        """初始化特征处理器"""
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
        self.scaler = StandardScaler()
        
    def _encode_mbti(self, mbti: str) -> List[float]:
        """编码MBTI特征为数值向量"""
        dimensions = {
            'I/E': [0, 1],  # 内向/外向
            'N/S': [0, 1],  # 直觉/感知
            'T/F': [0, 1],  # 思考/感受
            'J/P': [0, 1]   # 判断/知觉
        }
        return [dimensions[dim][0 if mbti[i] in 'ISTJ' else 1] 
                for i, dim in enumerate(['I/E', 'N/S', 'T/F', 'J/P'])]
                
    def _encode_time_period(self, time: str) -> List[float]:
        """将时间段编码为循环特征"""
        time_periods = ['早上', '中午', '下午', '晚上', '凌晨']
        idx = time_periods.index(time)
        angle = 2 * np.pi * idx / len(time_periods)
        return [np.cos(angle), np.sin(angle)]
        
    def _encode_game_experience(self, exp: str) -> float:
        """将游戏经验编码为数值"""
        experience_levels = {
            '初级': 0.25,
            '中级': 0.5,
            '高级': 0.75,
            '高超': 1.0
        }
        return experience_levels.get(exp, 0.0)
        
    def encode_categorical_features(self, users: List[UserProfile]) -> pd.DataFrame:
        """将分类特征编码为数值形式
        
        Args:
            users: 用户档案列表
            
        Returns:
            pd.DataFrame: 编码后的特征数据框
        """
        # 转换用户档案为数据框
        user_dicts = [user.to_dict() for user in users]
        df = pd.DataFrame(user_dicts)
        
        # 删除不需要编码的列
        columns_to_drop = ['user_id']
        df = df.drop(columns=columns_to_drop, errors='ignore')
        
        # 处理MBTI特征
        mbti_features = ['mbti_IE', 'mbti_NS', 'mbti_TF', 'mbti_JP']
        mbti_vectors = [self._encode_mbti(mbti) for mbti in df['mbti']]
        for i, feature in enumerate(mbti_features):
            df[feature] = [vector[i] for vector in mbti_vectors]
        df = df.drop('mbti', axis=1)
        
        # 处理时间特征
        time_features = ['time_cos', 'time_sin']
        time_vectors = [self._encode_time_period(time) for time in df['play_time']]
        for i, feature in enumerate(time_features):
            df[feature] = [vector[i] for vector in time_vectors]
        df = df.drop('play_time', axis=1)
        
        # 处理游戏经验
        df['game_experience'] = df['game_experience'].apply(self._encode_game_experience)
        
        # 处理其他分类特征
        categorical_features = ['gender', 'gender_preference', 'play_region', 
                              'online_status', 'game_style']
        for feature in categorical_features:
            if feature in df.columns:
                if len(df[feature].unique()) == 1:
                    df[feature] = 1
                else:
                    df[feature] = self.label_encoders[feature].fit_transform(df[feature])
        
        # 处理游戏列表
        all_games = set()
        for games in df['games']:
            all_games.update(games)
            
        for game in all_games:
            df[f'game_{game}'] = df['games'].apply(lambda x: 1 if game in x else 0)
            
        # 删除原始游戏列表列
        df = df.drop('games', axis=1)
        
        # 确保没有NaN值
        return df.fillna(0)
        
    def get_feature_vector(self, df: pd.DataFrame, user_index: int) -> np.ndarray:
        """获取指定用户的特征向量
        
        Args:
            df: 编码后的特征数据框
            user_index: 用户索引
            
        Returns:
            np.ndarray: 用户特征向量
        """
        return df.iloc[user_index].values
        
    def normalize_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化特征值
        
        Args:
            df: 原始特征数据框
            
        Returns:
            pd.DataFrame: 标准化后的特征数据框
        """
        # 只对数值列进行标准化
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if not numeric_columns.empty:
            df[numeric_columns] = self.scaler.fit_transform(df[numeric_columns])
        return df 