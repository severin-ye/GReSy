"""游戏玩家匹配系统主入口

提供命令行界面来运行匹配系统
"""

from typing import List
import os
from matching.matcher import UserMatcher
from utils.data_loaders import DataLoader
from utils.data_exporters import MatchingResultExporter
from models.user_profile import UserProfile
from models.game_profile import GameProfile

def print_user_info(user: UserProfile, title: str = "用户信息"):
    """打印用户信息的辅助函数"""
    print(f"\n{title}:")
    print(f"游戏: {', '.join(user.games)}")
    print(f"性别: {user.gender}")
    print(f"性别倾向: {', '.join(user.gender_preference)}")
    print(f"游玩区服: {user.play_region}")
    print(f"游玩时间: {user.play_time}")
    print(f"MBTI: {user.mbti}")
    print(f"星座: {user.zodiac}")
    print(f"游戏经验: {user.game_experience}")
    print(f"在线状态: {user.online_status}")
    print(f"游戏风格: {user.game_style}")

def print_match_results(
    matches: List[tuple],
    target_user: UserProfile,
    exporter: MatchingResultExporter
):
    """打印匹配结果"""
    print(f"\n为用户 {target_user.user_id} 找到以下匹配：")
    print("=" * 50)
    
    for user, similarity, contributions, possible_games in matches:
        print(exporter.format_match_result(user, similarity, contributions))
        print("-" * 50)
        
    if possible_games:
        print("\n推荐游戏:")
        for game, sim in possible_games:
            print(f"- {game} (相似度: {sim:.2%})")

def main():
    """主函数"""
    try:
        # 1. 加载数据
        print("正在加载数据...")
        data_dir = os.path.join(os.path.dirname(__file__), "data", "json")
        users = DataLoader.load_user_pool(os.path.join(data_dir, "user_pool.json"))
        games = DataLoader.load_game_pool(os.path.join(data_dir, "game_pool.json"))
        
        # 2. 初始化系统组件
        print("初始化匹配系统...")
        matcher = UserMatcher(debug_mode=False)
        exporter = MatchingResultExporter()
        
        # 3. 添加用户到匹配系统
        for user in users:
            matcher.add_user(user)
            
        while True:
            try:
                # 显示用户选择提示
                print(f"\n请输入要查看的用户编号 (1-{len(users)})，输入0退出：")
                user_index = int(input().strip())
                
                # 检查是否退出
                if user_index == 0:
                    print("程序已退出")
                    break
                    
                # 验证输入范围
                if user_index < 1 or user_index > len(users):
                    print(f"请输入1到{len(users)}之间的数字！")
                    continue
                
                # 获取选中的用户
                target_user = users[user_index - 1]
                
                # 打印目标用户信息
                print_user_info(target_user, "目标用户信息")
                
                # 执行匹配
                matches = matcher.find_matches(target_user, games)
                
                if not matches:
                    print("\n未找到匹配的用户。")
                else:
                    # 打印匹配结果
                    print_match_results(matches, target_user, exporter)
                    
                    # 询问是否保存结果
                    print("\n是否要保存匹配结果到CSV文件？(y/n)")
                    if input().strip().lower() == 'y':
                        output_dir = os.path.join(os.path.dirname(__file__), "data", "output")
                        os.makedirs(output_dir, exist_ok=True)
                        output_file = os.path.join(output_dir, f"matching_results_{target_user.user_id}.csv")
                        exporter.export_to_csv(matches, target_user, output_file)
                        print(f"结果已保存到: {output_file}")
                    
            except ValueError as e:
                print(f"输入错误: {str(e)}")
            except Exception as e:
                print(f"发生错误: {str(e)}")
                if matcher.debug_mode:
                    raise
                
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        if matcher.debug_mode:
            raise
        
if __name__ == "__main__":
    main()