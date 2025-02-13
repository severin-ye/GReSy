"""权重加载器测试"""

import os
import pytest
from loaders.weights_loader import WeightsLoader

@pytest.fixture
def weights_loader(tmp_path):
    """创建测试用的权重加载器"""
    # 创建临时权重目录
    weights_dir = tmp_path / "weights"
    weights_dir.mkdir()
    
    # 创建测试权重文件
    match_weights = {
        "time_match_weights": {
            "exact": 1.0,
            "adjacent": 0.7,
            "opposite": 0.3
        },
        "dimension_weights": {
            "online_status": 5,
            "server": 10,
            "time": 15
        }
    }
    
    game_similarity = {
        "type_weight": 0.6,
        "platform_weight": 0.4
    }
    
    # 写入测试文件
    (weights_dir / "match_weights.json").write_text(
        str(match_weights).replace("'", '"'),
        encoding='utf-8'
    )
    (weights_dir / "game_similarity_weights.json").write_text(
        str(game_similarity).replace("'", '"'),
        encoding='utf-8'
    )
    
    return WeightsLoader(str(tmp_path))

def test_load_match_weights(weights_loader):
    """测试加载匹配权重"""
    weights = weights_loader.get_weights('match_weights')
    assert weights
    assert 'time_match_weights' in weights
    assert weights['time_match_weights']['exact'] == 1.0
    assert weights['time_match_weights']['adjacent'] == 0.7
    assert weights['dimension_weights']['server'] == 10
    
def test_load_game_similarity_weights(weights_loader):
    """测试加载游戏相似度权重"""
    weights = weights_loader.get_weights('game_similarity_weights')
    assert weights
    assert weights['type_weight'] == 0.6
    assert weights['platform_weight'] == 0.4
    
def test_load_nonexistent_weights(weights_loader):
    """测试加载不存在的权重"""
    weights = weights_loader.get_weights('nonexistent')
    assert weights == {} 