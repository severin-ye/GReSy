"""特征处理模块

负责用户特征的编码、标准化和处理
"""

import pandas as pd
import numpy as np
from typing import List, Dict
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
        
        # 对每个分类特征进行编码
        for feature, encoder in self.label_encoders.items():
            if feature in df.columns:
                if len(df[feature].unique()) == 1:
                    df[feature] = 1
                else:
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