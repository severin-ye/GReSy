"""数值匹配器测试模块

测试数值匹配器的功能，包括：
- 游戏风格匹配
- 游戏经验匹配
- 游戏时间匹配
"""

import unittest
from models.user_profile import UserProfile
from matching.numeric_matcher import NumericMatcher

class TestNumericMatcher(unittest.TestCase):
    """数值匹配器测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.matcher = NumericMatcher()
        
        # 创建测试用户
        self.user1 = UserProfile(
            user_id="test1",
            gender="男",
            gender_preference=["女"],
            play_region="国服",
            play_time="晚上",
            mbti="INTJ",
            zodiac="天蝎座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技",
            games=["英雄联盟"]
        )
        
        self.user2 = UserProfile(
            user_id="test2",
            gender="女",
            gender_preference=["男"],
            play_region="亚服",
            play_time="晚上",
            mbti="ENFP",
            zodiac="双子座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技",
            games=["王者荣耀"]
        )
        
        self.user3 = UserProfile(
            user_id="test3",
            gender="男",
            gender_preference=["女"],
            play_region="美服",
            play_time="凌晨",
            mbti="ISTP",
            zodiac="处女座",
            game_experience="初级",
            online_status="离线",
            game_style="休闲",
            games=["CSGO"]
        )
        
    def test_match_style(self):
        """测试游戏风格匹配"""
        # 测试相同风格
        score = self.matcher.match_style(self.user1, self.user2)
        self.assertEqual(score, 1.0, "相同游戏风格应该返回1.0")
        
        # 测试不同风格
        score = self.matcher.match_style(self.user1, self.user3)
        self.assertLess(score, 0.5, "不同游戏风格应该返回较低分数")
        
    def test_match_experience(self):
        """测试游戏经验匹配"""
        # 测试相同经验等级
        score = self.matcher.match_experience(self.user1, self.user2)
        self.assertEqual(score, 1.0, "相同游戏经验应该返回1.0")
        
        # 测试差距较大的经验等级
        score = self.matcher.match_experience(self.user1, self.user3)
        self.assertLess(score, 0.5, "经验等级差距大应该返回较低分数")
        
    def test_match_time(self):
        """测试游戏时间匹配"""
        # 测试相同时间段
        score = self.matcher.match_time(self.user1, self.user2)
        self.assertEqual(score, 1.0, "相同游戏时间应该返回1.0")
        
        # 测试不同时间段
        score = self.matcher.match_time(self.user1, self.user3)
        self.assertLess(score, 0.5, "不同游戏时间应该返回较低分数")
        
    def test_get_match_result(self):
        """测试获取匹配结果"""
        # 测试高匹配度的情况
        result = self.matcher.get_match_result(self.user1, self.user2)
        self.assertIn('style', result)
        self.assertIn('experience', result)
        self.assertIn('time', result)
        
        # 验证各维度分数
        self.assertEqual(result['style'], 1.0, "相同游戏风格的分数应该为1.0")
        self.assertEqual(result['experience'], 1.0, "相同游戏经验的分数应该为1.0")
        self.assertEqual(result['time'], 1.0, "相同游戏时间的分数应该为1.0")
        
        # 测试低匹配度的情况
        result = self.matcher.get_match_result(self.user1, self.user3)
        self.assertLess(result['style'], 0.5, "不同游戏风格的分数应该较低")
        self.assertLess(result['experience'], 0.5, "差距大的游戏经验分数应该较低")
        self.assertLess(result['time'], 0.5, "不同游戏时间的分数应该较低")

if __name__ == '__main__':
    unittest.main() 