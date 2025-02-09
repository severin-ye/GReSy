"""匹配系统测试模块

测试匹配系统的各个功能
"""

import unittest
from typing import List
from models.user_profile import UserProfile
from models.game_profile import GameProfile
from matching.matching_system import MatchingSystem

class TestMatchingSystem(unittest.TestCase):
    """匹配系统测试类"""
    
    def setUp(self):
        """测试初始化"""
        print("\n=== 初始化测试环境 ===")
        # 创建测试用的游戏档案
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
                name="星际争霸",
                types=["RTS"],
                platforms=["端游"],
                tags=["竞技", "策略"]
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
        print("已创建测试游戏档案：", [game.name for game in self.games])
        
        # 创建匹配系统
        self.matching_system = MatchingSystem(self.games)
        print("已初始化匹配系统")
        
        # 创建测试用户
        self.user1 = UserProfile(
            user_id="test_user1",
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
        
        self.user2 = UserProfile(
            user_id="test_user2",
            gender="女",
            gender_preference=["男"],
            play_region="国服",
            play_time="晚上",
            mbti="ENFP",
            zodiac="双子座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技",
            games=["王者荣耀", "原神"]
        )
        
        self.user3 = UserProfile(
            user_id="test_user3",
            gender="男",
            gender_preference=["女"],
            play_region="亚服",
            play_time="凌晨",
            mbti="ISTP",
            zodiac="处女座",
            game_experience="中级",
            online_status="离线",
            game_style="休闲",
            games=["CSGO", "原神"]
        )
        print("已创建测试用户：", [user.user_id for user in [self.user1, self.user2, self.user3]])
        
    def test_match_users_high_compatibility(self):
        """测试高匹配度的用户匹配"""
        print("\n=== 测试高匹配度用户 ===")
        print(f"比较用户 {self.user1.user_id} 和 {self.user2.user_id}")
        
        # user1和user2应该有较高的匹配度，因为他们有：
        # 1. 相同的在线状态和服务器
        # 2. 相同的时间段和游戏经验
        # 3. 互补的性别偏好
        # 4. 共同的游戏（王者荣耀）
        scores = self.matching_system.match_users(self.user1, self.user2)
        
        print("\n匹配分数详情：")
        for dimension, score in scores.items():
            print(f"- {dimension}: {score:.2f}")
        
        # 验证总分
        self.assertGreater(scores['total_score'], 0.7)
        print(f"\n总分 {scores['total_score']:.2f} > 0.7 ✓")
        
        # 验证各维度分数
        self.assertEqual(scores['online_status'], 1.0)
        self.assertEqual(scores['server'], 1.0)
        self.assertEqual(scores['time'], 1.0)
        self.assertEqual(scores['experience'], 1.0)
        self.assertEqual(scores['style'], 1.0)
        print("所有基础维度完全匹配 ✓")
        
    def test_match_users_low_compatibility(self):
        """测试低匹配度的用户匹配"""
        print("\n=== 测试低匹配度用户 ===")
        print(f"比较用户 {self.user1.user_id} 和 {self.user3.user_id}")
        
        # user1和user3应该有较低的匹配度，因为他们有：
        # 1. 不同的在线状态和服务器
        # 2. 不同的时间段和游戏经验
        # 3. 没有共同游戏
        scores = self.matching_system.match_users(self.user1, self.user3)
        
        print("\n匹配分数详情：")
        for dimension, score in scores.items():
            print(f"- {dimension}: {score:.2f}")
        
        # 验证总分
        self.assertLess(scores['total_score'], 0.5)
        print(f"\n总分 {scores['total_score']:.2f} < 0.5 ✓")
        
        # 验证各维度分数
        self.assertEqual(scores['online_status'], 0.0)
        print("在线状态不匹配 ✓")
        
        self.assertLess(scores['server'], 1.0)
        print("服务器跨区 ✓")
        
        self.assertLess(scores['time'], 0.5)
        print("时间段差异大 ✓")
        
        self.assertLess(scores['experience'], 1.0)
        print("游戏经验等级不同 ✓")
        
        self.assertNotEqual(scores['style'], 1.0)
        print("游戏风格不同 ✓")
        
    def test_find_best_matches(self):
        """测试最佳匹配查找"""
        print("\n=== 测试最佳匹配查找 ===")
        user_pool = [self.user1, self.user2, self.user3]
        print(f"用户池大小: {len(user_pool)}")
        
        # 为user1找到最佳匹配
        print(f"\n为用户 {self.user1.user_id} 查找最佳匹配")
        matches = self.matching_system.find_best_matches(
            self.user1,
            user_pool,
            top_n=2
        )
        
        # 验证返回的匹配数量
        self.assertEqual(len(matches), 2)
        print(f"返回匹配数量: {len(matches)} ✓")
        
        # 验证匹配排序（user2应该排在user3前面）
        self.assertEqual(matches[0][0].user_id, "test_user2")
        self.assertEqual(matches[1][0].user_id, "test_user3")
        print("\n匹配结果排序：")
        for user, scores in matches:
            print(f"- {user.user_id}: {scores['total_score']:.2f}")
        
        # 验证分数降序排序
        self.assertGreater(
            matches[0][1]['total_score'],
            matches[1][1]['total_score']
        )
        print("分数正确降序排序 ✓")
        
    def test_get_match_explanation(self):
        """测试匹配解释生成"""
        print("\n=== 测试匹配解释生成 ===")
        # 获取user1和user2的匹配分数
        scores = self.matching_system.match_users(self.user1, self.user2)
        
        # 获取匹配解释
        explanations = self.matching_system.get_match_explanation(scores)
        
        print("\n匹配解释详情：")
        # 验证解释的格式
        for dimension, score, explanation in explanations:
            print(f"- {dimension}: {score:.2f} ({explanation})")
            # 验证维度名称是否存在
            self.assertIn(dimension, scores)
            
            # 验证分数范围
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
            
            # 验证解释文本
            self.assertIsInstance(explanation, str)
            self.assertGreater(len(explanation), 0)
            
        # 验证解释是否按分数降序排序
        scores_only = [score for _, score, _ in explanations]
        self.assertEqual(scores_only, sorted(scores_only, reverse=True))
        print("\n解释正确按分数降序排序 ✓")
        
    def test_edge_cases(self):
        """测试边界情况"""
        print("\n=== 测试边界情况 ===")
        # 创建一个没有游戏的用户
        empty_user = UserProfile(
            user_id="empty_user",
            gender="男",
            gender_preference=["女"],
            play_region="国服",
            play_time="晚上",
            mbti="INTJ",
            zodiac="天蝎座",
            game_experience="初级",
            online_status="在线",
            game_style="休闲",
            games=[]
        )
        print("创建了一个没有游戏的用户:", empty_user.user_id)
        
        # 测试与没有游戏的用户匹配
        print(f"\n将用户 {self.user1.user_id} 与空游戏列表用户匹配")
        scores = self.matching_system.match_users(self.user1, empty_user)
        
        print("\n匹配分数详情：")
        for dimension, score in scores.items():
            print(f"- {dimension}: {score:.2f}")
        
        # 验证游戏相关的分数应该很低
        self.assertEqual(scores['game_preference'], 0.0)
        print("游戏偏好分数为0 ✓")
        
        self.assertLess(scores['game_type'], 0.5)
        print("游戏类型相似度较低 ✓")
        
        # 但其他维度应该正常计算
        self.assertEqual(scores['online_status'], 1.0)
        self.assertEqual(scores['server'], 1.0)
        self.assertEqual(scores['time'], 1.0)
        print("其他维度正常计算 ✓")

if __name__ == '__main__':
    unittest.main(verbosity=2) 