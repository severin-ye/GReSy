"""偏好匹配器测试模块"""

import unittest
import os
import sys
import json
from unittest.mock import patch, mock_open

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matching.preference_matcher import PreferenceMatcher, MBTIMatcher, ZodiacMatcher

class MockPreferenceMatcher(PreferenceMatcher):
    """用于测试的模拟偏好匹配器"""
    
    def _get_data_file_path(self) -> str:
        return "mock_path.json"
        
    def calculate_preference_score(self, source_value: str, target_value: str) -> float:
        return 0.5 if source_value == target_value else 0.0

class TestPreferenceMatcher(unittest.TestCase):
    """测试偏好匹配器基类"""
    
    def setUp(self):
        """测试前准备"""
        self.mock_data = {
            "test_types": [
                {
                    "type": "A",
                    "preference": {"B": 5}
                }
            ]
        }
        # 设置文件操作的mock
        self.file_patcher = patch('builtins.open', mock_open(read_data=json.dumps(self.mock_data)))
        self.mock_file = self.file_patcher.start()
        
        # 设置文件存在检查的mock
        self.path_patcher = patch('os.path.exists', return_value=True)
        self.mock_exists = self.path_patcher.start()
        
    def tearDown(self):
        """测试后清理"""
        self.file_patcher.stop()
        self.path_patcher.stop()
        
    def test_weight_calculation(self):
        """测试权重计算"""
        matcher = MockPreferenceMatcher(0.5)
        score = matcher.get_weighted_score("same", "same")
        self.assertEqual(score, 0.25)  # 0.5 * 0.5 = 0.25
            
    def test_file_not_found(self):
        """测试文件不存在的情况"""
        # 修改mock返回值，模拟文件不存在
        self.mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            matcher = MockPreferenceMatcher(0.5)
        # 恢复mock返回值
        self.mock_exists.return_value = True
            
class TestMBTIMatcher(unittest.TestCase):
    """测试MBTI匹配器"""
    
    def setUp(self):
        """测试前准备"""
        self.matcher = MBTIMatcher(0.5)
        
    def test_mbti_matching(self):
        """测试MBTI匹配计算"""
        # 测试最佳匹配 - 从mbti_pool.json中的实际数据
        score = self.matcher.calculate_preference_score("INTJ", "ENFP")
        self.assertEqual(score, 0.9)  # 9/10 = 0.9
        
        # 测试次佳匹配
        score = self.matcher.calculate_preference_score("INTJ", "ENTP")
        self.assertEqual(score, 0.8)  # 8/10 = 0.8
        
        # 测试无匹配关系
        score = self.matcher.calculate_preference_score("INTJ", "ISFP")
        self.assertEqual(score, 0.0)
        
        # 测试未知MBTI类型
        score = self.matcher.calculate_preference_score("UNKNOWN", "ENFP")
        self.assertEqual(score, 0.0)
        
    def test_weighted_mbti_matching(self):
        """测试加权MBTI匹配计算"""
        # 测试加权分数
        score = self.matcher.get_weighted_score("INTJ", "ENFP")
        self.assertEqual(score, 0.45)  # 0.9 * 0.5 = 0.45

class TestZodiacMatcher(unittest.TestCase):
    """测试星座匹配器"""
    
    def setUp(self):
        """测试前准备"""
        self.matcher = ZodiacMatcher(0.3)
        
    def test_zodiac_matching(self):
        """测试星座匹配计算"""
        # 从constellation_pool.json中获取实际数据进行测试
        score = self.matcher.calculate_preference_score("天蝎座", "双子座")
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 1)
        
        # 测试未知星座
        score = self.matcher.calculate_preference_score("未知星座", "双子座")
        self.assertEqual(score, 0.0)
        
    def test_weighted_zodiac_matching(self):
        """测试加权星座匹配计算"""
        score = self.matcher.get_weighted_score("天蝎座", "双子座")
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 0.3)  # 权重为0.3，所以最大值不超过0.3

if __name__ == '__main__':
    unittest.main() 