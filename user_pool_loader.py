# 导入所需的模块
import json
from recommendation_system import UserProfile

def load_user_pool(file_path: str) -> list[UserProfile]:
    """从JSON文件加载用户池数据
    
    Args:
        file_path: JSON格式的用户池文件路径,包含用户的详细信息
        
    Returns:
        list[UserProfile]: 返回一个包含所有用户档案对象的列表
    """
    # 初始化空列表用于存储用户档案
    users = []
    
    # 打开并读取JSON文件
    with open(file_path, 'r', encoding='utf-8') as f:
        # 解析JSON数据
        data = json.load(f)
        # 遍历每个用户的数据
        for user_data in data['users']:
            # 创建UserProfile对象,使用get()方法安全地获取数据,并提供默认值
            user = UserProfile(
                games=[user_data.get('游戏', '')],  # 游戏列表,目前只支持一个游戏
                gender=user_data.get('性别', '不限'),  # 性别
                gender_preference=user_data.get('性别倾向', '不限'),  # 性别倾向
                play_region=user_data.get('游玩服务器', ''),  # 游戏服务器
                play_time=user_data.get('游玩固定时间', ''),  # 固定游戏时间
                mbti=user_data.get('MBTI', '未知'),  # MBTI性格类型
                zodiac=user_data.get('星座', '未知'),  # 星座
                game_experience=user_data.get('游戏经验', '初级')  # 游戏经验水平
            )
            users.append(user)
    
    return users

def print_user_info(user: UserProfile, user_id: str):
    """打印单个用户的详细信息
    
    Args:
        user: UserProfile对象,包含用户的所有属性
        user_id: 用户的唯一标识符
    """
    print(f"\n用户ID: {user_id}")
    print(f"游戏: {user.games[0]}")
    print(f"性别: {user.gender}")
    print(f"性别倾向: {user.gender_preference}")
    print(f"游玩服务器: {user.play_region}")
    print(f"游玩时间: {user.play_time}")
    print(f"MBTI: {user.mbti}")
    print(f"星座: {user.zodiac}")
    print(f"游戏经验: {user.game_experience}")
    print("-" * 30)

# 当直接运行此文件时执行以下代码
if __name__ == "__main__":
    print("开始读取用户池数据...")
    print("=" * 50)
    
    # 加载所有用户数据
    users = load_user_pool("user_pool.json")
    
    # 从JSON文件中获取用户ID列表
    with open("user_pool.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        # 如果用户没有id,则使用默认的编号
        user_ids = [user_data.get('id', f'用户{i+1}') for i, user_data in enumerate(data['users'])]
    
    # 打印用户总数和所有用户的详细信息
    print(f"共读取到 {len(users)} 个用户的信息：")
    print("=" * 50)
    
    # 使用zip()同时遍历用户对象和用户ID
    for user, user_id in zip(users, user_ids):
        print_user_info(user, user_id)
    
    print("\n数据读取完成！") 