"""加载器管理器测试"""

import os
import pytest
from utils.loaders import LoaderManager

@pytest.fixture
def loader_manager(tmp_path):
    """创建测试用的加载器管理器"""
    # 创建测试目录结构
    (tmp_path / "config").mkdir()
    (tmp_path / "weights").mkdir()
    (tmp_path / "pools").mkdir()
    
    # 创建测试配置文件
    platform_config = {
        "platform_weights": {
            "手游": 1.0,
            "端游": 0.8
        }
    }
    
    match_weights = {
        "time_match_weights": {
            "exact": 1.0,
            "adjacent": 0.7
        }
    }
    
    user_pool = {
        "users": [
            {
                "id": "test_user",
                "游戏": ["测试游戏"],
                "性别": "男",
                "性别倾向": ["女"],
                "游玩服务器": "测试服",
                "游玩固定时间": "晚上",
                "MBTI": "INFP",
                "星座": "双子座",
                "游戏经验": "初级",
                "在线状态": "在线",
                "游戏风格": "保守"
            }
        ]
    }
    
    # 写入测试文件
    (tmp_path / "config/platform_config.json").write_text(
        str(platform_config).replace("'", '"'),
        encoding='utf-8'
    )
    (tmp_path / "weights/match_weights.json").write_text(
        str(match_weights).replace("'", '"'),
        encoding='utf-8'
    )
    (tmp_path / "pools/user_pool.json").write_text(
        str(user_pool).replace("'", '"'),
        encoding='utf-8'
    )
    
    # 创建加载器管理器实例
    class TestLoaderManager(LoaderManager):
        def __init__(self, base_path):
            self.base_path = base_path
            super().__init__()
            
        def _get_base_path(self):
            return self.base_path
            
    return TestLoaderManager(str(tmp_path))

def test_get_config(loader_manager):
    """测试获取配置"""
    config = loader_manager.get_config('platform_config')
    assert config
    assert 'platform_weights' in config
    assert config['platform_weights']['手游'] == 1.0
    
def test_get_weights(loader_manager):
    """测试获取权重"""
    weights = loader_manager.get_weights('match_weights')
    assert weights
    assert 'time_match_weights' in weights
    assert weights['time_match_weights']['exact'] == 1.0
    
def test_get_pool_data(loader_manager):
    """测试获取数据池数据"""
    pool_data = loader_manager.get_pool_data('user_pool')
    assert pool_data
    assert 'users' in pool_data
    assert pool_data['users'][0]['id'] == 'test_user'
    
def test_nonexistent_data(loader_manager):
    """测试获取不存在的数据"""
    # 测试不存在的配置
    config = loader_manager.get_config('nonexistent')
    assert config == {}
    
    # 测试不存在的权重
    weights = loader_manager.get_weights('nonexistent')
    assert weights == {}
    
    # 测试不存在的数据池
    pool_data = loader_manager.get_pool_data('nonexistent')
    assert pool_data == {} 