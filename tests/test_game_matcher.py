"""游戏匹配器测试模块

测试游戏匹配器的功能，包括：
- 游戏类型相似度
- 游戏偏好相似度
- 社交属性相似度
"""

import unittest
from models.user_profile import UserProfile
from models.game_profile import GameProfile
from matching.game_matcher import GameMatcher

class TestGameMatcher(unittest.TestCase):
    """游戏匹配器测试类"""
    
    def setUp(self):
        """测试初始化"""
        # 创建测试游戏
        self.games = [
            GameProfile(
                name="英雄联盟",
                types=["MOBA"],
                platforms=["端游"],
                tags=["竞技", "团队"]
            ),
            GameProfile(
                name="王者荣耀",
                types=["MOBA"],
                platforms=["手游"],
                tags=["竞技", "团队"]
            ),
            GameProfile(
                name="CSGO",
                types=["FPS"],
                platforms=["端游"],
                tags=["竞技", "射击"]
            ),
            GameProfile(
                name="原神",
                types=["RPG"],
                platforms=["手游"],
                tags=["冒险", "开放世界"]
            )
        ]
        
        # 初始化匹配器
        self.matcher = GameMatcher(self.games)
        
        # 创建测试用户
        self.moba_user = UserProfile(
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
            games=["英雄联盟", "王者荣耀"]
        )
        
        self.fps_user = UserProfile(
            user_id="test2",
            gender="女",
            gender_preference=["男"],
            play_region="亚服",
            play_time="晚上",
            mbti="ENFP",
            zodiac="双子座",
            game_experience="中级",
            online_status="在线",
            game_style="竞技",
            games=["CSGO"]
        )
        
        self.rpg_user = UserProfile(
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
            games=["原神"]
        )
        
    def test_match_type(self):
        """测试游戏类型匹配"""
        # 测试相同类型（MOBA玩家）
        score = self.matcher.match_type(self.moba_user, self.moba_user)
        self.assertEqual(score, 1.0, "相同游戏类型应该返回1.0")
        
        # 测试不同类型（MOBA vs FPS）
        score = self.matcher.match_type(self.moba_user, self.fps_user)
        self.assertLess(score, 1.0, "不同游戏类型应该返回较低分数")
        
        # 测试完全不同类型（MOBA vs RPG）
        score = self.matcher.match_type(self.moba_user, self.rpg_user)
        self.assertLess(score, 0.5, "完全不同的游戏类型应该返回更低分数")
        
    def test_match_preference(self):
        """测试游戏偏好匹配"""
        # 测试有共同游戏
        user1 = UserProfile(
            user_id="test4",
            gender="男",
            gender_preference=["女"],
            play_region="国服",
            play_time="晚上",
            mbti="INTJ",
            zodiac="天蝎座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技",
            games=["英雄联盟", "王者荣耀"]
        )
        
        user2 = UserProfile(
            user_id="test5",
            gender="女",
            gender_preference=["男"],
            play_region="亚服",
            play_time="晚上",
            mbti="ENFP",
            zodiac="双子座",
            game_experience="中级",
            online_status="在线",
            game_style="竞技",
            games=["王者荣耀", "原神"]
        )
        
        score = self.matcher.match_preference(user1, user2)
        self.assertGreater(score, 0.0, "有共同游戏应该返回大于0的分数")
        
        # 测试没有共同游戏
        score = self.matcher.match_preference(self.moba_user, self.rpg_user)
        self.assertEqual(score, 0.0, "没有共同游戏应该返回0.0")
        
    def test_match_social(self):
        """测试社交属性匹配"""
        # 测试相似的社交属性（都是竞技风格）
        score = self.matcher.match_social(self.moba_user, self.fps_user)
        self.assertGreater(score, 0.7, "相似的社交属性应该返回较高分数")
        
        # 测试不同的社交属性
        score = self.matcher.match_social(self.moba_user, self.rpg_user)
        self.assertLess(score, 0.5, "不同的社交属性应该返回较低分数")
        
    def test_get_match_result(self):
        """测试获取匹配结果"""
        # 测试高匹配度的情况
        result = self.matcher.get_match_result(self.moba_user, self.moba_user)
        self.assertIn('game_type', result)
        self.assertIn('game_preference', result)
        self.assertIn('social', result)
        
        # 验证各维度分数
        self.assertEqual(result['game_type'], 1.0, "相同游戏类型的分数应该为1.0")
        self.assertGreater(result['game_preference'], 0.0, "有共同游戏的偏好分数应该大于0")
        self.assertGreater(result['social'], 0.7, "相似社交属性的分数应该较高")
        
        # 测试低匹配度的情况
        result = self.matcher.get_match_result(self.moba_user, self.rpg_user)
        self.assertLess(result['game_type'], 0.5, "不同游戏类型的分数应该较低")
        self.assertEqual(result['game_preference'], 0.0, "没有共同游戏的偏好分数应该为0")
        self.assertLess(result['social'], 0.5, "不同社交属性的分数应该较低")

if __name__ == '__main__':
    unittest.main() 