"""配置加载器测试"""

import os
import pytest
from loaders.config_loader import ConfigLoader

@pytest.fixture
def config_loader(tmp_path):
    """创建测试用的配置加载器"""
    # 创建临时配置目录
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # 创建测试配置文件
    platform_config = {
        "platform_weights": {
            "手游": 1.0,
            "端游": 0.8,
            "主机": 0.6
        }
    }
    
    experience_levels = {
        "experience_levels": {
            "初级": 1,
            "中级": 2,
            "高级": 3,
            "高超": 4
        }
    }
    
    # 写入测试文件
    (config_dir / "platform_config.json").write_text(
        str(platform_config).replace("'", '"'),
        encoding='utf-8'
    )
    (config_dir / "experience_levels.json").write_text(
        str(experience_levels).replace("'", '"'),
        encoding='utf-8'
    )
    
    return ConfigLoader(str(tmp_path))

def test_load_platform_config(config_loader):
    """测试加载平台配置"""
    config = config_loader.get_config('platform_config')
    assert config
    assert 'platform_weights' in config
    assert config['platform_weights']['手游'] == 1.0
    assert config['platform_weights']['端游'] == 0.8
    assert config['platform_weights']['主机'] == 0.6
    
def test_load_experience_levels(config_loader):
    """测试加载经验等级配置"""
    config = config_loader.get_config('experience_levels')
    assert config
    assert 'experience_levels' in config
    assert config['experience_levels']['初级'] == 1
    assert config['experience_levels']['中级'] == 2
    assert config['experience_levels']['高级'] == 3
    assert config['experience_levels']['高超'] == 4
    
def test_load_nonexistent_config(config_loader):
    """测试加载不存在的配置"""
    config = config_loader.get_config('nonexistent')
    assert config == {} 