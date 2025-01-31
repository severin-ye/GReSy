"""相似度计算测试模块

测试匹配系统中的相似度计算功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_profile import UserProfile
from models.game_profile import GameProfile
from matching.matcher import UserMatcher

def test_game_similarity():
    """测试游戏相似度计算"""
    print("\n测试游戏相似度计算:")
    print("=" * 50)
    
    # 创建测试用户
    user1 = UserProfile(
        user_id="test1",
        gender="男",
        gender_preference=["女"],
        games=["英雄联盟", "王者荣耀"],  # 端游MOBA + 手游MOBA
        play_time="晚上",
        play_region="国服",
        mbti="ISTJ",
        zodiac="天秤座",
        game_experience="高级",
        online_status="在线",
        game_style="竞技"
    )
    
    user2 = UserProfile(
        user_id="test2",
        gender="男",
        gender_preference=["女"],
        games=["英雄联盟", "王者荣耀", "和平精英"],  # 端游MOBA + 手游MOBA + 手游FPS
        play_time="晚上",
        play_region="亚服",
        mbti="ISTJ",
        zodiac="射手座",
        game_experience="高级",
        online_status="在线",
        game_style="竞技"
    )
    
    user3 = UserProfile(
        user_id="test3",
        gender="男",
        gender_preference=["女"],
        games=["CS:GO", "和平精英"],  # 端游FPS + 手游FPS
        play_time="晚上",
        play_region="国服",
        mbti="ENTJ",
        zodiac="射手座",
        game_experience="高级",
        online_status="在线",
        game_style="竞技"
    )
    
    user4 = UserProfile(
        user_id="test4",
        gender="女",
        gender_preference=["男"],
        games=["第五人格", "我的世界"],  # 非对称竞技 + 沙盒
        play_time="晚上",
        play_region="国服",
        mbti="INFP",
        zodiac="双子座",
        game_experience="中级",
        online_status="在线",
        game_style="休闲"
    )

    user5 = UserProfile(
        user_id="test5",
        gender="女",
        gender_preference=["男"],
        games=["原神", "崩坏：星穹铁道"],  # RPG系列
        play_time="晚上",
        play_region="国服",
        mbti="ENFP",
        zodiac="天蝎座",
        game_experience="中级",
        online_status="在线",
        game_style="休闲"
    )

    
    user6 = UserProfile(
        user_id="test6",
        gender="女",
        gender_preference=["男"],
        games=["原神", "第五人格", "我的世界"],  # RPG + 非对称竞技 + 沙盒
        play_time="早上",
        play_region="美服",
        mbti="ISFJ",
        zodiac="天蝎座",
        game_experience="中级",
        online_status="在线",
        game_style="休闲"
    )
    
    # 创建测试游戏
    games = [
        GameProfile(
            name="英雄联盟",
            types=["MOBA", "端游", "竞技"],
            platforms=["PC"],
            tags=["团队", "策略"]
        ),
        GameProfile(
            name="王者荣耀",
            types=["MOBA", "手游", "竞技"],
            platforms=["Mobile"],
            tags=["团队", "策略"]
        ),
        GameProfile(
            name="原神",
            types=["RPG", "手游", "开放世界"],
            platforms=["Mobile", "PC"],
            tags=["冒险", "剧情"]
        ),
        GameProfile(
            name="崩坏：星穹铁道",
            types=["RPG", "手游", "回合制"],
            platforms=["Mobile", "PC"],
            tags=["冒险", "剧情"]
        ),
        GameProfile(
            name="CS:GO",
            types=["FPS", "端游", "竞技"],
            platforms=["PC"],
            tags=["团队", "射击"]
        ),
        GameProfile(
            name="和平精英",
            types=["FPS", "手游", "生存"],
            platforms=["Mobile"],
            tags=["团队", "射击", "生存"]
        ),
        GameProfile(
            name="第五人格",
            types=["生存恐怖", "手游", "非对称竞技"],
            platforms=["Mobile"],
            tags=["团队", "策略", "恐怖"]
        ),
        GameProfile(
            name="我的世界",
            types=["沙盒", "端游", "生存"],
            platforms=["PC", "Mobile", "Console"],
            tags=["创造", "生存", "冒险"]
        )
    ]
    
    # 初始化匹配器
    matcher = UserMatcher()
    
    # 测试不同用户组合的游戏相似度
    pairs = [
        (user1, user2),  # MOBA vs RPG
        (user1, user3),  # MOBA vs FPS
        (user1, user4),  # MOBA vs 非对称+沙盒
        (user2, user3),  # RPG vs FPS
        (user2, user4),  # RPG vs 非对称+沙盒
        (user3, user4),  # FPS vs 非对称+沙盒
        (user5, user6)   # 混合游戏组合
    ]
    
    for u1, u2 in pairs:
        similarity = matcher._calculate_game_similarity(u1, u2, games)
        print(f"\n用户 {u1.user_id} 和 {u2.user_id} 的游戏相似度:")
        print(f"用户1游戏: {', '.join(u1.games)}")
        print(f"用户2游戏: {', '.join(u2.games)}")
        print(f"相似度: {similarity:.2%}")
        
        # 显示游戏类型
        u1_types = set()
        u2_types = set()
        for game in u1.games:
            for g in games:
                if g.name == game:
                    u1_types.update(g.types)
        for game in u2.games:
            for g in games:
                if g.name == game:
                    u2_types.update(g.types)
        print(f"用户1游戏类型: {', '.join(u1_types)}")
        print(f"用户2游戏类型: {', '.join(u2_types)}")

def test_personality_similarity():
    """测试性格相似度计算"""
    print("\n测试性格相似度计算:")
    print("=" * 50)
    
    # 创建测试用户
    test_cases = [
        # 完全相同的MBTI和游戏风格
        (UserProfile(
            user_id="test1",
            gender="男",
            gender_preference=["女"],
            games=["英雄联盟"],
            play_time="晚上",
            play_region="国服",
            mbti="ISTJ",
            zodiac="天秤座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技"
        ),
        UserProfile(
            user_id="test2",
            gender="女",
            gender_preference=["男"],
            games=["王者荣耀"],
            play_time="晚上",
            play_region="国服",
            mbti="ISTJ",
            zodiac="天蝎座",
            game_experience="中级",
            online_status="在线",
            game_style="竞技"
        )),
        # 完全不同的MBTI但相同游戏风格
        (UserProfile(
            user_id="test3",
            gender="男",
            gender_preference=["女"],
            games=["英雄联盟"],
            play_time="晚上",
            play_region="国服",
            mbti="ISTJ",
            zodiac="天秤座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技"
        ),
        UserProfile(
            user_id="test4",
            gender="女",
            gender_preference=["男"],
            games=["王者荣耀"],
            play_time="晚上",
            play_region="国服",
            mbti="ENFP",
            zodiac="天蝎座",
            game_experience="中级",
            online_status="在线",
            game_style="竞技"
        )),
        # 使用之前定义的test5和test6
        (UserProfile(
            user_id="test5",
            gender="男",
            gender_preference=["女"],
            games=["英雄联盟", "王者荣耀", "和平精英"],
            play_time="晚上",
            play_region="亚服",
            mbti="ISTJ",
            zodiac="射手座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技"
        ),
        UserProfile(
            user_id="test6",
            gender="女",
            gender_preference=["男"],
            games=["原神", "第五人格", "我的世界"],
            play_time="早上",
            play_region="美服",
            mbti="ISFJ",
            zodiac="天蝎座",
            game_experience="中级",
            online_status="在线",
            game_style="休闲"
        ))
    ]
    
    # 初始化匹配器
    matcher = UserMatcher()
    
    # 测试不同组合的性格相似度
    for u1, u2 in test_cases:
        similarity = matcher._calculate_personality_similarity(u1, u2)
        print(f"\n用户 {u1.user_id} 和 {u2.user_id} 的性格相似度:")
        print(f"用户1: MBTI={u1.mbti}, 游戏风格={u1.game_style}")
        print(f"用户2: MBTI={u2.mbti}, 游戏风格={u2.game_style}")
        print(f"相似度: {similarity:.2%}")

def test_time_region_similarity():
    """测试时间和区服匹配度计算"""
    print("\n测试时间和区服匹配度计算:")
    print("=" * 50)
    
    # 创建测试用户
    test_cases = [
        # 完全相同的时间和区服
        (UserProfile(
            user_id="test1",
            gender="男",
            gender_preference=["女"],
            games=["英雄联盟"],
            play_time="晚上",
            play_region="国服",
            mbti="ISTJ",
            zodiac="天秤座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技"
        ),
        UserProfile(
            user_id="test2",
            gender="女",
            gender_preference=["男"],
            games=["王者荣耀"],
            play_time="晚上",
            play_region="国服",
            mbti="ISTJ",
            zodiac="天蝎座",
            game_experience="中级",
            online_status="在线",
            game_style="竞技"
        )),
        # 相同时间但不同区服
        (UserProfile(
            user_id="test3",
            gender="男",
            gender_preference=["女"],
            games=["英雄联盟"],
            play_time="晚上",
            play_region="国服",
            mbti="ISTJ",
            zodiac="天秤座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技"
        ),
        UserProfile(
            user_id="test4",
            gender="女",
            gender_preference=["男"],
            games=["王者荣耀"],
            play_time="晚上",
            play_region="美服",
            mbti="ENFP",
            zodiac="天蝎座",
            game_experience="中级",
            online_status="在线",
            game_style="竞技"
        )),
        # 使用之前定义的test5和test6
        (UserProfile(
            user_id="test5",
            gender="男",
            gender_preference=["女"],
            games=["英雄联盟", "王者荣耀", "和平精英"],
            play_time="晚上",
            play_region="亚服",
            mbti="ISTJ",
            zodiac="射手座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技"
        ),
        UserProfile(
            user_id="test6",
            gender="女",
            gender_preference=["男"],
            games=["原神", "第五人格", "我的世界"],
            play_time="早上",
            play_region="美服",
            mbti="ISFJ",
            zodiac="天蝎座",
            game_experience="中级",
            online_status="在线",
            game_style="休闲"
        ))
    ]
    
    # 初始化匹配器
    matcher = UserMatcher()
    
    # 测试不同组合的时间和区服匹配度
    for u1, u2 in test_cases:
        similarity = matcher._calculate_time_region_similarity(u1, u2)
        print(f"\n用户 {u1.user_id} 和 {u2.user_id} 的时间和区服匹配度:")
        print(f"用户1: 时间={u1.play_time}, 区服={u1.play_region}")
        print(f"用户2: 时间={u2.play_time}, 区服={u2.play_region}")
        print(f"匹配度: {similarity:.2%}")

if __name__ == "__main__":
    test_game_similarity()
    test_personality_similarity()
    test_time_region_similarity() 