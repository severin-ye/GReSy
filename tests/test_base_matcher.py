"""基础匹配器测试模块

测试基础匹配器的二元匹配功能，包括：
- 在线状态匹配
- 服务器匹配
"""

import unittest
from models.user_profile import UserProfile
from matching.base_matcher import BaseMatcher

class TestBaseMatcher(unittest.TestCase):
    """基础匹配器测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.matcher = BaseMatcher()
        
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
            game_experience="中级",
            online_status="在线",
            game_style="休闲",
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
        
    def test_match_online_status(self):
        """测试在线状态匹配"""
        # 测试两个在线用户
        self.assertTrue(
            self.matcher.match_online_status(self.user1, self.user2),
            "两个在线用户应该匹配成功"
        )
        
        # 测试一个在线一个离线的用户
        self.assertFalse(
            self.matcher.match_online_status(self.user1, self.user3),
            "在线和离线用户不应该匹配"
        )
        
    def test_match_server(self):
        """测试服务器匹配"""
        # 测试相同服务器
        score = self.matcher.match_server(self.user1, self.user1)
        self.assertEqual(score, 1.0, "相同服务器应该返回1.0")
        
        # 测试同组服务器（亚洲组）
        score = self.matcher.match_server(self.user1, self.user2)
        self.assertEqual(score, 0.7, "同组服务器应该返回0.7")
        
        # 测试不同组服务器
        score = self.matcher.match_server(self.user1, self.user3)
        self.assertEqual(score, 0.3, "不同组服务器应该返回0.3")
        
    def test_get_match_result(self):
        """测试获取匹配结果"""
        # 测试完全匹配的情况
        result = self.matcher.get_match_result(self.user1, self.user2)
        self.assertIn('online_status', result)
        self.assertIn('server', result)
        
        # 验证在线状态分数
        self.assertEqual(result['online_status'], 1.0, "两个在线用户的在线状态分数应该为1.0")
        
        # 验证服务器分数
        self.assertEqual(result['server'], 0.7, "同组服务器的分数应该为0.7")
        
        # 测试不匹配的情况
        result = self.matcher.get_match_result(self.user1, self.user3)
        self.assertEqual(result['online_status'], 0.0, "在线和离线用户的在线状态分数应该为0.0")
        self.assertEqual(result['server'], 0.3, "不同组服务器的分数应该为0.3")

if __name__ == '__main__':
    unittest.main() 