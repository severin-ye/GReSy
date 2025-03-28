from openai import OpenAI  
import numpy as np  
import os  
from sklearn.preprocessing import MultiLabelBinarizer  # 导入用于特征编码的工具
from sklearn.metrics.pairwise import cosine_similarity  # 导入用于计算余弦相似度的函数
from key import OPENAI_API_KEY, ALIYUN_API_KEY, ALIYUN_BASE_URL

# 配置OpenAI客户端
# client = OpenAI(api_key=OPENAI_API_KEY)

# 配置阿里云通义千问API
client = OpenAI(
    api_key=ALIYUN_API_KEY,
    base_url=ALIYUN_BASE_URL  # 阿里云通义千问的API地址
)

# 测试API连接
completion = client.chat.completions.create(
    model="qwen-plus",  # 使用通义千问模型
    messages=[
        {"role": "system", "content": "推荐系统,根据用户输入的自我介绍标签,推荐相似的其他用户, 并说明理由"},
        {"role": "user", "content": "你好"}
    ]
)

class KB:
    """知识库类，用于处理用户数据和生成推荐"""
    
    def __init__(self):
        """初始化知识库"""
        # 读取用户数据文件
        with open('用户池.txt', 'r', encoding='utf-8') as f:
            self.content = f.read()
            
        # 初始化特征编码器，用于将文本特征转换为数值向量
        self.game_encoder = MultiLabelBinarizer()  # 游戏特征编码器
        self.region_encoder = MultiLabelBinarizer()  # 地区特征编码器
        self.time_encoder = MultiLabelBinarizer()  # 时间特征编码器
        self.style_encoder = MultiLabelBinarizer()  # 风格特征编码器
        
        # 解析用户数据并创建向量表示
        self.users, self.user_vectors = self.process_users()
    
    def parse_users(self):
        """解析用户数据为结构化字典列表"""
        users = []
        # 按行解析用户数据
        for line in self.content.strip().split('\n'):
            if line:
                parts = line.split()
                if len(parts) >= 5:  # 确保数据包含所有必要字段
                    # 创建用户字典
                    user = {
                        'username': parts[0],  # 用户名
                        'game': parts[1],      # 游戏
                        'region': parts[2],    # 地区
                        'time': parts[3],      # 时间
                        'style': parts[4]      # 风格
                    }
                    users.append(user)
        return users
    
    def process_users(self):
        """处理用户数据并创建向量表示"""
        users = self.parse_users()
        
        # 准备特征数据，将每个特征转换为列表格式
        games = [[u['game']] for u in users]
        regions = [[u['region']] for u in users]
        times = [[u['time']] for u in users]
        styles = [[u['style']] for u in users]
        
        # 使用编码器将文本特征转换为数值向量
        game_vectors = self.game_encoder.fit_transform(games)
        region_vectors = self.region_encoder.fit_transform(regions)
        time_vectors = self.time_encoder.fit_transform(times)
        style_vectors = self.style_encoder.fit_transform(styles)
        
        # 合并所有特征向量为一个完整的用户表示
        user_vectors = np.concatenate([
            game_vectors,
            region_vectors,
            time_vectors,
            style_vectors
        ], axis=1)
        
        return users, user_vectors
    
    def vectorize_new_user(self, user_info):
        """将新用户信息转换为向量表示"""
        # 准备特征数据
        game = [[user_info['game']]]
        region = [[user_info['region']]]
        time = [[user_info['time']]]
        style = [[user_info['style']]]
        
        # 使用已训练的编码器转换特征
        game_vector = self.game_encoder.transform(game)
        region_vector = self.region_encoder.transform(region)
        time_vector = self.time_encoder.transform(time)
        style_vector = self.style_encoder.transform(style)
        
        # 合并所有特征向量
        user_vector = np.concatenate([
            game_vector,
            region_vector,
            time_vector,
            style_vector
        ], axis=1)
        
        return user_vector
    
    def find_similar_users(self, query_user_info, show_all=True):
        """找到相似的用户，并计算相似度"""
        # 将查询用户转换为向量表示
        query_vector = self.vectorize_new_user(query_user_info)
        
        # 计算查询用户与所有用户之间的余弦相似度
        similarities = cosine_similarity(query_vector, self.user_vectors)[0]
        
        # 创建用户相似度列表
        all_users = []
        for idx, similarity in enumerate(similarities):
            all_users.append({
                'user': self.users[idx],
                'similarity': similarity
            })
        
        # 按相似度降序排序
        all_users.sort(key=lambda x: x['similarity'], reverse=True)
        return all_users
    
    def generate_recommendation_description(self, query_user, similar_users, top_n=2):
        """为每个相似用户生成推荐描述"""
        recommendations = []
        
        # 为top_n个最相似用户生成推荐描述
        for i in range(min(top_n, len(similar_users))):
            user = similar_users[i]
            # 构建提示文本
            prompt = f"""
                    基于搜索用户的信息：
                    游戏: {query_user['game']}
                    地区: {query_user['region']}
                    时间: {query_user['time']}
                    风格: {query_user['style']}

                    相似用户信息：
                    用户名: {user['user']['username']}
                    相似度: {user['similarity']:.2f}
                    游戏: {user['user']['game']}
                    地区: {user['user']['region']}
                    时间: {user['user']['time']}
                    风格: {user['user']['style']}

                    请分析这个用户与搜索用户的相似之处，并给出推荐理由。
                    """
            try:
                # 调用AI生成推荐描述
                completion = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": "你是一个游戏玩家匹配推荐助手，你会收到用户相似玩家的相关信息, 请根据这些信息，给出合理的推荐建议。(不要使用markdown格式)"},
                        {"role": "user", "content": prompt}
                    ]
                )
                # 格式化推荐描述
                recommendation = f"\n推荐用户 {user['user']['username']} 的分析：\n" + completion.choices[0].message.content
                # 添加分隔符
                if i < min(top_n, len(similar_users)) - 1:
                    recommendation += "\n" + "-" * 25
                recommendations.append(recommendation)
            except Exception as e:
                recommendations.append(f"生成推荐描述时发生错误: {str(e)}")
        
        return "\n".join(recommendations)

# 测试代码
if __name__ == "__main__":
    # 创建知识库实例
    kb = KB()
    
    # 创建测试查询用户
    query_user = {
        'game': '永劫无间',
        'region': '韩服',
        'time': '晚上玩',
        'style': '策略型'
    }
    
    # 查找相似用户
    similar_users = kb.find_similar_users(query_user)
    
    # 打印查询用户信息
    print("查询用户信息:")
    print(f"游戏: {query_user['game']}")
    print(f"地区: {query_user['region']}")
    print(f"时间: {query_user['time']}")
    print(f"风格: {query_user['style']}")
    
    # 打印相似用户列表
    print("\n相似用户列表:")
    print("-" * 50)
    for user in similar_users[:20]:  # 显示前几个最相似的用户
        print(f"用户名: {user['user']['username']}")
        print(f"相似度: {user['similarity']:.4f}")
        print(f"游戏: {user['user']['game']}")
        print(f"地区: {user['user']['region']}")
        print(f"时间: {user['user']['time']}")
        print(f"风格: {user['user']['style']}")
        print("-" * 25)
    
    # 生成并显示AI推荐分析
    print("-" * 50)
    print("\nAI 推荐分析:")
    recommendation = kb.generate_recommendation_description(query_user, similar_users, top_n=2)
    print(recommendation)
