"""测试特征处理模块

测试特征处理器的各项功能，包括：
- MBTI编码
- 时间段编码
- 游戏经验编码
- 分类特征编码
- 特征向量获取
- 特征标准化
"""

import unittest
import numpy as np
import pandas as pd
from matching.feature_processor import FeatureProcessor
from models.user_profile import UserProfile

class TestFeatureProcessor(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.processor = FeatureProcessor()
        self.test_user = UserProfile(
            user_id="test_user",
            gender="男",
            gender_preference="女",
            play_region="亚服",
            play_time="晚上",
            mbti="INTJ",
            zodiac="天蝎座",
            game_experience="高级",
            online_status="在线",
            game_style="休闲",
            games=["英雄联盟", "APEX"]
        )

    def test_encode_mbti(self):
        """测试MBTI编码功能"""
        mbti_vector = self.processor._encode_mbti("INTJ")
        self.assertEqual(len(mbti_vector), 4)
        self.assertEqual(mbti_vector, [0, 1, 0, 0])  # I=0, N=1, T=0, J=0

        mbti_vector = self.processor._encode_mbti("ESFP")
        self.assertEqual(mbti_vector, [1, 0, 1, 1])  # E=1, S=0, F=1, P=1

    def test_encode_time_period(self):
        """测试时间段编码功能"""
        time_vector = self.processor._encode_time_period("早上")
        self.assertEqual(len(time_vector), 2)
        self.assertAlmostEqual(time_vector[0]**2 + time_vector[1]**2, 1, places=5)

    def test_encode_game_experience(self):
        """测试游戏经验编码功能"""
        self.assertEqual(self.processor._encode_game_experience("初级"), 0.25)
        self.assertEqual(self.processor._encode_game_experience("中级"), 0.5)
        self.assertEqual(self.processor._encode_game_experience("高级"), 0.75)
        self.assertEqual(self.processor._encode_game_experience("高超"), 1.0)
        self.assertEqual(self.processor._encode_game_experience("未知"), 0.0)

    def test_encode_categorical_features(self):
        """测试分类特征编码功能"""
        users = [self.test_user]
        df = self.processor.encode_categorical_features(users)
        
        # 检查基本属性
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue('user_id' not in df.columns)
        self.assertTrue('mbti' not in df.columns)
        self.assertTrue('play_time' not in df.columns)
        
        # 检查MBTI特征
        self.assertTrue(all(f in df.columns for f in ['mbti_IE', 'mbti_NS', 'mbti_TF', 'mbti_JP']))
        
        # 检查时间特征
        self.assertTrue(all(f in df.columns for f in ['time_cos', 'time_sin']))
        
        # 检查游戏特征
        self.assertTrue('game_英雄联盟' in df.columns)
        self.assertTrue('game_APEX' in df.columns)

    def test_normalize_features(self):
        """测试特征标准化功能"""
        # 创建测试数据
        test_df = pd.DataFrame({
            'numeric_col': [1, 2, 3, 4, 5],
            'categorical_col': ['A', 'B', 'A', 'B', 'A']
        })
        
        # 标准化特征
        normalized_df = self.processor.normalize_features(test_df)
        
        # 检查数值列是否被标准化（均值应接近0，标准差应接近1）
        numeric_col = normalized_df['numeric_col'].values
        self.assertAlmostEqual(np.mean(numeric_col), 0, places=1)
        self.assertAlmostEqual(np.std(numeric_col), 1, places=1)
        
        # 检查分类列是否保持不变
        self.assertTrue(all(normalized_df['categorical_col'] == test_df['categorical_col']))

    def test_get_feature_vector(self):
        """测试特征向量获取功能"""
        test_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6]
        })
        vector = self.processor.get_feature_vector(test_df, 0)
        self.assertTrue(np.array_equal(vector, np.array([1, 4])))

if __name__ == '__main__':
    unittest.main() 