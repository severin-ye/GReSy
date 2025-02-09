"""强制顺位匹配器测试模块

测试强制顺位匹配器的功能，主要用于：
- 性别偏好匹配
"""

import unittest
from models.user_profile import UserProfile
from matching.ordered_matcher import OrderedMatcher

class TestOrderedMatcher(unittest.TestCase):
    """强制顺位匹配器测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.matcher = OrderedMatcher()
        
        # 创建测试用户
        self.male_user = UserProfile(
            user_id="test1",
            gender="男",
            gender_preference=["女", "男"],  # 优先女性，其次男性
            play_region="国服",
            play_time="晚上",
            mbti="INTJ",
            zodiac="天蝎座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技",
            games=["英雄联盟"]
        )
        
        self.female_user = UserProfile(
            user_id="test2",
            gender="女",
            gender_preference=["男"],  # 只接受男性
            play_region="亚服",
            play_time="晚上",
            mbti="ENFP",
            zodiac="双子座",
            game_experience="中级",
            online_status="在线",
            game_style="休闲",
            games=["王者荣耀"]
        )
        
        self.male_user2 = UserProfile(
            user_id="test3",
            gender="男",
            gender_preference=["男"],  # 只接受男性
            play_region="美服",
            play_time="凌晨",
            mbti="ISTP",
            zodiac="处女座",
            game_experience="初级",
            online_status="离线",
            game_style="休闲",
            games=["CSGO"]
        )
        
    def test_match_gender(self):
        """测试性别偏好匹配"""
        # 测试互相接受的情况
        score = self.matcher.match_gender(self.male_user, self.female_user)
        self.assertGreater(score, 0.8, "男女双方互相接受应该返回较高分数")
        
        # 测试单向接受的情况
        score = self.matcher.match_gender(self.male_user, self.male_user2)
        self.assertLess(score, 0.8, "单向接受应该返回较低分数")
        
        # 测试互相不接受的情况
        score = self.matcher.match_gender(self.female_user, self.female_user)
        self.assertLess(score, 0.3, "互相不接受应该返回很低分数")
        
    def test_get_match_result(self):
        """测试获取匹配结果"""
        # 测试完全匹配的情况
        result = self.matcher.get_match_result(self.male_user, self.female_user)
        self.assertIn('gender', result)
        self.assertGreater(result['gender'], 0.8, "互相接受的性别偏好分数应该较高")
        
        # 测试部分匹配的情况
        result = self.matcher.get_match_result(self.male_user, self.male_user2)
        self.assertLess(result['gender'], 0.8, "单向接受的性别偏好分数应该较低")
        
        # 测试不匹配的情况
        result = self.matcher.get_match_result(self.female_user, self.female_user)
        self.assertLess(result['gender'], 0.3, "互相不接受的性别偏好分数应该很低")
        
    def test_edge_cases(self):
        """测试边界情况"""
        # 创建一个没有性别偏好的用户
        no_preference_user = UserProfile(
            user_id="test4",
            gender="男",
            gender_preference=[],  # 空偏好列表
            play_region="国服",
            play_time="晚上",
            mbti="INTJ",
            zodiac="天蝎座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技",
            games=["英雄联盟"]
        )
        
        # 测试空偏好列表的情况
        result = self.matcher.get_match_result(no_preference_user, self.female_user)
        self.assertLess(result['gender'], 0.3, "空偏好列表应该返回很低分数")
        
        # 测试与自己匹配的情况
        result = self.matcher.get_match_result(self.male_user, self.male_user)
        self.assertLess(result['gender'], 0.8, "与自己匹配应该返回较低分数")

if __name__ == '__main__':
    unittest.main() 