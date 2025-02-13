"""数据池加载器测试"""

import os
import pytest
from loaders.pools_loader import PoolsLoader

@pytest.fixture
def pools_loader(tmp_path):
    """创建测试用的数据池加载器"""
    # 创建临时数据池目录
    pools_dir = tmp_path / "pools"
    pools_dir.mkdir()
    
    # 创建测试数据文件
    user_pool = {
        "users": [
            {
                "id": "test_user1",
                "游戏": ["王者荣耀", "英雄联盟"],
                "性别": "男",
                "性别倾向": ["女", "男"],
                "游玩服务器": "国服",
                "游玩固定时间": "晚上",
                "MBTI": "INFP",
                "星座": "双子座",
                "游戏经验": "初级",
                "在线状态": "在线",
                "游戏风格": "保守"
            }
        ]
    }
    
    game_pool = {
        "game_types": [
            {
                "游戏名字": "王者荣耀",
                "游戏类型": ["MOBA", "手游"],
                "platforms": ["iOS", "Android"],
                "tags": ["竞技", "团队"]
            }
        ]
    }
    
    server_pool = {
        "server_groups": {
            "亚洲": ["国服", "韩服", "日服"],
            "欧美": ["美服", "欧服"]
        }
    }
    
    # 写入测试文件
    (pools_dir / "user_pool.json").write_text(
        str(user_pool).replace("'", '"'),
        encoding='utf-8'
    )
    (pools_dir / "game_pool.json").write_text(
        str(game_pool).replace("'", '"'),
        encoding='utf-8'
    )
    (pools_dir / "server_pool.json").write_text(
        str(server_pool).replace("'", '"'),
        encoding='utf-8'
    )
    
    return PoolsLoader(str(tmp_path))

def test_load_user_pool(pools_loader):
    """测试加载用户池"""
    users = pools_loader.load_user_pool()
    assert users
    assert len(users) == 1
    user = users[0]
    assert user.user_id == "test_user1"
    assert "王者荣耀" in user.games
    assert user.gender == "男"
    assert user.play_region == "国服"
    
def test_load_game_pool(pools_loader):
    """测试加载游戏池"""
    games = pools_loader.load_game_pool()
    assert games
    assert len(games) == 1
    game = games[0]
    assert game.name == "王者荣耀"
    assert "MOBA" in game.types
    assert "iOS" in game.platforms
    assert "竞技" in game.tags
    
def test_load_server_groups(pools_loader):
    """测试加载服务器组"""
    server_groups = pools_loader.load_server_groups()
    assert server_groups
    assert "亚洲" in server_groups
    assert "国服" in server_groups["亚洲"]
    assert "欧美" in server_groups
    assert "美服" in server_groups["欧美"]
    
def test_get_game_types(pools_loader):
    """测试获取游戏类型"""
    games = pools_loader.load_game_pool()
    types = pools_loader.get_game_types_by_name("王者荣耀", games)
    assert types
    assert "MOBA" in types
    assert "手游" in types
    
def test_nonexistent_data(pools_loader):
    """测试加载不存在的数据"""
    # 测试不存在的用户池
    users = pools_loader.load_user_pool()
    assert isinstance(users, list)
    
    # 测试不存在的游戏池
    games = pools_loader.load_game_pool()
    assert isinstance(games, list)
    
    # 测试不存在的服务器组
    server_groups = pools_loader.load_server_groups()
    assert isinstance(server_groups, dict) 