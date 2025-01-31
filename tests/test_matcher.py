"""匹配算法测试模块

测试匹配系统的核心功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_profile import UserProfile
from models.game_profile import GameProfile
from matching.matcher import UserMatcher

def create_test_users():
    """创建测试用户数据"""
    users = [
        UserProfile(
            user_id="user1",
            gender="男",
            gender_preference=["女"],
            games=["英雄联盟", "王者荣耀"],
            play_time="晚上",
            play_region="国服",
            mbti="ISTJ",
            zodiac="天秤座",
            game_experience="高级",
            online_status="在线",
            game_style="竞技"
        ),
        UserProfile(
            user_id="user2",
            gender="女",
            gender_preference=["男"],
            games=["和平精英", "CS:GO"],
            play_time="晚上",
            play_region="亚服",
            mbti="ENFP",
            # zodiac="天蝎座",
            zodiac="天秤座",
            game_experience="初级",
            online_status="在线",
            game_style="保守"
        )
    ]
    return users

def create_test_games():
    """创建测试游戏数据"""
    games = [
        GameProfile(
            name="英雄联盟",
            types=["MOBA", "竞技"],
            platforms=["PC"],
            tags=["团队", "策略"]
        ),
        GameProfile(
            name="王者荣耀",
            types=["MOBA", "竞技"],
            platforms=["Mobile"],
            tags=["团队", "策略"]
        ),
        GameProfile(
            name="CS:GO",
            types=["FPS", "竞技"],
            platforms=["PC"],
            tags=["团队", "射击"]
        ),
        GameProfile(
            name="和平精英",
            types=["FPS", "生存"],
            platforms=["Mobile"],
            tags=["团队", "射击", "生存"]
        )
    ]
    return games

def test_matching():
    """测试匹配功能"""
    # 创建测试数据
    users = create_test_users()
    games = create_test_games()
    
    # 初始化匹配器
    matcher = UserMatcher(debug_mode=True)
    
    # 添加用户到匹配系统
    for user in users:
        matcher.add_user(user)
    
    # 获取两个用户
    user1 = users[0]
    user2 = users[1]
    
    # 获取匹配结果以获取推荐游戏
    matches = matcher.find_matches(user1, games, top_n=1)
    recommended_games = []
    if matches:
        _, _, _, possible_games = matches[0]
        if possible_games:
            recommended_games = [(game, sim) for game, sim in possible_games[:1]]
    
    # 定义特征列表
    features = [
        ("用户ID", "user_id"),
        ("性别", "gender"),
        ("性别偏好", lambda u: ", ".join(u.gender_preference)),
        ("游戏", lambda u: ", ".join(u.games) + (f", {recommended_games[0][0]}(可能性: {recommended_games[0][1]*100:.2f}%)" if u == user1 and recommended_games else "")),
        ("游戏时间", "play_time"),
        ("游戏区服", "play_region"),
        ("MBTI", "mbti"),
        ("星座", "zodiac"),
        ("游戏经验", "game_experience"),
        ("在线状态", "online_status"),
        ("游戏风格", "game_style")
    ]
    
    # 计算每列的最大宽度
    label_width = max(len(label) for label, _ in features) + 2  # 添加2个空格的padding
    user1_values = []
    user2_values = []
    
    for label, attr in features:
        if callable(attr):
            value1 = attr(user1)
            value2 = attr(user2)
        else:
            value1 = getattr(user1, attr)
            value2 = getattr(user2, attr)
        user1_values.append(value1)
        user2_values.append(value2)
    
    user1_width = max(len(str(value)) for value in user1_values) + 4  # 添加4个空格的padding
    user2_width = max(len(str(value)) for value in user2_values) + 4
    
    # 计算总宽度
    total_width = label_width + user1_width + user2_width
    
    # 打印表格
    print("\n用户信息对比:")
    print("=" * total_width)
    print(f"{'特征':<{label_width}}{'用户1':<{user1_width}}{'用户2':<{user2_width}}")
    print("-" * total_width)
    
    # 打印各项特征对比
    for i, (label, _) in enumerate(features):
        print(f"{label:<{label_width}}{user1_values[i]:<{user1_width}}{user2_values[i]:<{user2_width}}")
    
    print("=" * total_width)
    
    # 测试匹配结果
    if matches:
        print("\n匹配结果:")
        print("=" * total_width)
        matched_user, similarity, contributions, _ = matches[0]
        print(f"总匹配度: {similarity*100:.2f}%")
        
        # 显示各项特征的贡献度
        print("\n每个特征的贡献:")
        print("-" * total_width)
        
        # 获取所有贡献度
        contributions_list = [
            ("游戏时间", contributions.get('play_time', 0)),
            ("游戏区服", contributions.get('play_region', 0)),
            ("游戏相似度", contributions.get('game_similarity', 0)),
            ("在线状态", contributions.get('online_status', 0)),
            ("星座匹配", contributions.get('zodiac', 0)),
            ("MBTI匹配", contributions.get('mbti', 0)),
            ("游戏经验", contributions.get('game_experience', 0)),
            ("游戏风格", contributions.get('game_style', 0))
        ]
        
        # 计算贡献度值的最大宽度
        value_width = max(len(f"{value:.1f}%") for _, value in contributions_list) + 4
        
        # 打印贡献度
        for label, value in contributions_list:
            print(f"{label:<{label_width}}{f'{value:.1f}%':<{value_width}}")
        
        print("-" * total_width)
        total = sum(value for _, value in contributions_list)
        print(f"{'总计':<{label_width}}{f'{total:.1f}%':<{value_width}}")
    else:
        print("\n未找到合适的匹配")

if __name__ == "__main__":
    test_matching() 