# 导入所需的模块
from user_pool_loader import load_user_pool  # 用于加载用户池数据
from recommendation_system import UserMatchingSystem, UserProfile  # 用于用户匹配系统和用户档案
import pandas as pd  # 用于数据处理和保存CSV
from typing import List, Tuple  # 用于类型提示
import json  # 用于JSON文件处理

def save_matching_results(matches: List[Tuple[UserProfile, float]], target_user: UserProfile, output_file: str):
    """保存匹配结果到CSV文件
    
    Args:
        matches: 匹配结果列表,每个元素是(用户档案,相似度)的元组
        target_user: 目标用户的档案
        output_file: 输出CSV文件的路径
    """
    results = []
    for user, similarity in matches:
        # 构建每一行的数据字典
        result = {
            '目标用户游戏': ','.join(target_user.games),  # 将游戏列表转换为逗号分隔的字符串
            '目标用户性别': target_user.gender,
            '目标用户性别倾向': target_user.gender_preference,
            '目标用户游玩区服': target_user.play_region,
            '目标用户游玩时间': target_user.play_time,
            '目标用户MBTI': target_user.mbti,
            '目标用户星座': target_user.zodiac,
            '目标用户游戏经验': target_user.game_experience,
            '匹配用户游戏': ','.join(user.games),
            '匹配用户性别': user.gender,
            '匹配用户性别倾向': user.gender_preference,
            '匹配用户游玩区服': user.play_region,
            '匹配用户游玩时间': user.play_time,
            '匹配用户MBTI': user.mbti,
            '匹配用户星座': user.zodiac,
            '匹配用户游戏经验': user.game_experience,
            '匹配度': f"{similarity:.2%}"  # 将相似度转换为百分比格式
        }
        results.append(result)
    
    # 创建DataFrame并保存为CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')  # 使用utf-8-sig编码以支持中文

def print_user_info(user: UserProfile, title: str = "用户信息"):
    """打印用户信息的辅助函数"""
    print(f"\n{title}:")
    print(f"游戏: {', '.join(user.games)}")
    print(f"性别: {user.gender}")
    print(f"性别倾向: {user.gender_preference}")
    print(f"游玩区服: {user.play_region}")
    print(f"游玩时间: {user.play_time}")
    print(f"MBTI: {user.mbti}")
    print(f"星座: {user.zodiac}")
    print(f"游戏经验: {user.game_experience}")

def main():
    # 1. 加载用户池数据
    print("正在加载用户池数据...")
    users = load_user_pool("user_pool.json")
    
    # 2. 初始化匹配系统
    print("初始化匹配系统...")
    matching_system = UserMatchingSystem()
    for user in users:
        matching_system.add_user(user)
    
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
            
            # 获取所有匹配结果
            matches = matching_system.find_matches(target_user, top_n=len(users)-1)
            
            # 打印所有匹配用户信息（从最匹配到最不匹配）
            print("\n所有用户匹配结果（按匹配度从高到低排序）：")
            print("=" * 50)
            for i, (matched_user, similarity) in enumerate(matches, 1):
                print(f"\n第{i}名匹配用户 (匹配度: {similarity:.2%})")
                print("-" * 30)
                print_user_info(matched_user)
                
        except ValueError:
            print("请输入有效的数字！")
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()