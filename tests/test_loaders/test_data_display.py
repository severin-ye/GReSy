"""加载器数据展示测试"""

'''
使用命令
# 只查看配置数据
pytest tests/test_loaders/test_data_display.py::test_display_config_data -v -s

# 只查看权重数据
pytest tests/test_loaders/test_data_display.py::test_display_weights_data -v -s

# 只查看数据池数据
pytest tests/test_loaders/test_data_display.py::test_display_pools_data -v -s
'''

import json
import pytest
from loaders import loader_manager

def _format_json(data):
    """格式化JSON数据为易读的字符串
    
    Args:
        data: 要格式化的数据
        
    Returns:
        str: 格式化后的字符串
    """
    return json.dumps(data, ensure_ascii=False, indent=2)

def test_display_config_data():
    """展示所有配置数据"""
    print("\n=== 系统配置数据 ===")
    
    # 平台配置
    platform_config = loader_manager.get_config('platform_config')
    print("\n平台配置:")
    print(_format_json(platform_config))
    
    # 经验等级配置
    experience_levels = loader_manager.get_config('experience_levels')
    print("\n经验等级配置:")
    print(_format_json(experience_levels))
    
def test_display_weights_data():
    """展示所有权重数据"""
    print("\n=== 权重配置数据 ===")
    
    # 匹配权重
    match_weights = loader_manager.get_weights('match_weights')
    print("\n匹配权重:")
    print(_format_json(match_weights))
    
    # 游戏相似度权重
    game_similarity = loader_manager.get_weights('game_similarity_weights')
    print("\n游戏相似度权重:")
    print(_format_json(game_similarity))
    
    # 游戏类型相关性
    game_correlations = loader_manager.get_weights('game_type_correlations')
    print("\n游戏类型相关性:")
    print(_format_json(game_correlations))
    
    # 时间相似度
    time_similarity = loader_manager.get_weights('time_similarity')
    print("\n时间相似度:")
    print(_format_json(time_similarity))
    
def test_display_pools_data():
    """展示所有数据池数据"""
    print("\n=== 数据池数据 ===")
    
    # 用户池
    users = loader_manager.pools_loader.load_user_pool()
    print("\n用户池数据:")
    for user in users:
        print(f"\n用户 {user.user_id}:")
        print(f"  游戏: {', '.join(user.games)}")
        print(f"  性别: {user.gender}")
        print(f"  性别倾向: {', '.join(user.gender_preference)}")
        print(f"  游玩服务器: {user.play_region}")
        print(f"  游玩时间: {user.play_time}")
        print(f"  MBTI: {user.mbti}")
        print(f"  星座: {user.zodiac}")
        print(f"  游戏经验: {user.game_experience}")
        print(f"  在线状态: {user.online_status}")
        print(f"  游戏风格: {user.game_style}")
    
    # 游戏池
    games = loader_manager.pools_loader.load_game_pool()
    print("\n游戏池数据:")
    for game in games:
        print(f"\n游戏 {game.name}:")
        print(f"  类型: {', '.join(game.types)}")
        print(f"  平台: {', '.join(game.platforms)}")
        print(f"  标签: {', '.join(game.tags)}")
    
    # 服务器组
    server_groups = loader_manager.pools_loader.load_server_groups()
    print("\n服务器组数据:")
    for group, servers in server_groups.items():
        print(f"\n{group}: {', '.join(servers)}")
    
    # MBTI数据
    mbti_data = loader_manager.pools_loader.load_mbti_data()
    print("\nMBTI数据:")
    print(_format_json(mbti_data))
    
    # 星座数据
    constellation_data = loader_manager.pools_loader.load_constellation_data()
    print("\n星座数据:")
    print(_format_json(constellation_data))

if __name__ == '__main__':
    # 设置更大的终端显示宽度
    import os
    os.environ['COLUMNS'] = '120'
    
    # 运行所有展示测试
    pytest.main(['-v', '-s', __file__]) 