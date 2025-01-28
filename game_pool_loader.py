# 导入所需的模块
import json
from dataclasses import dataclass
from typing import List

@dataclass
class GameProfile:
    """游戏档案类，存储游戏的基本信息"""
    name: str  # 游戏名称
    types: List[str]  # 游戏类型列表

def load_game_pool(file_path: str) -> list[GameProfile]:
    """从JSON文件加载游戏池数据
    
    Args:
        file_path: JSON格式的游戏池文件路径,包含游戏的详细信息
        
    Returns:
        list[GameProfile]: 返回一个包含所有游戏档案对象的列表
    """
    # 初始化空列表用于存储游戏档案
    games = []
    
    # 打开并读取JSON文件
    with open(file_path, 'r', encoding='utf-8') as f:
        # 解析JSON数据
        data = json.load(f)
        # 遍历每个游戏的数据
        for game_data in data['game_types']:
            # 创建GameProfile对象
            game = GameProfile(
                name=game_data['游戏名字'],
                types=game_data['游戏类型']
            )
            games.append(game)
    
    return games

def print_game_info(game: GameProfile):
    """打印单个游戏的详细信息
    
    Args:
        game: GameProfile对象,包含游戏的所有属性
    """
    print(f"\n游戏名称: {game.name}")
    print(f"游戏类型: {', '.join(game.types)}")
    print("-" * 30)

def get_game_types_by_name(game_name: str, games: List[GameProfile]) -> List[str]:
    """根据游戏名称获取游戏类型
    
    Args:
        game_name: 游戏名称
        games: 游戏档案列表
        
    Returns:
        List[str]: 游戏类型列表
    """
    for game in games:
        if game.name == game_name:
            return game.types
    return []

# 当直接运行此文件时执行以下代码
if __name__ == "__main__":
    print("开始读取游戏池数据...")
    print("=" * 50)
    
    # 加载所有游戏数据
    games = load_game_pool("game_pool.json")
    
    # 打印游戏总数和所有游戏的详细信息
    print(f"共读取到 {len(games)} 个游戏的信息：")
    print("=" * 50)
    
    # 遍历并打印每个游戏的信息
    for game in games:
        print_game_info(game)
    
    print("\n数据读取完成！") 