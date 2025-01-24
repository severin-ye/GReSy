from user_pool_loader import load_user_pool
from recommendation_system import UserMatchingSystem, UserProfile
from typing import List, Tuple
import pandas as pd

def generate_matching_list(users: List[UserProfile]) -> pd.DataFrame:
    """生成所有用户之间的匹配度列表"""
    # 创建匹配系统
    matching_system = UserMatchingSystem()
    
    # 添加所有用户到系统
    for user in users:
        matching_system.add_user(user)
    
    # 存储所有匹配结果
    all_matches = []
    
    # 为每个用户计算匹配度
    for user1 in users:
        matches = matching_system.find_matches(user1)
        for user2, similarity in matches:
            all_matches.append({
                "用户1": f"{user1.games[0]}玩家",
                "用户2": f"{user2.games[0]}玩家",
                "匹配度": round(similarity * 100, 2),
                "用户1地区": user1.play_region,
                "用户2地区": user2.play_region,
                "用户1时间": user1.play_time,
                "用户2时间": user2.play_time
            })
    
    # 转换为DataFrame并排序
    df = pd.DataFrame(all_matches)
    df = df.sort_values(by="匹配度", ascending=False)
    return df

def main():
    # 加载用户池
    users = load_user_pool("user_pool.txt")
    
    # 生成匹配列表
    matches_df = generate_matching_list(users)
    
    # 打印结果
    print("\n所有用户匹配度排行榜：")
    print("=" * 80)
    pd.set_option('display.max_rows', None)
    print(matches_df)
    
    # 保存到CSV文件
    matches_df.to_csv("matching_results.csv", index=False, encoding='utf-8-sig')
    print("\n匹配结果已保存到 matching_results.csv")

if __name__ == "__main__":
    main() 