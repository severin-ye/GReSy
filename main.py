"""游戏玩家匹配系统主程序

基于matcher模块实现的游戏玩家匹配系统主程序，提供命令行交互界面。
"""

import os
import sys
from typing import List, Tuple, Dict
from matching.matching_system import MatchingSystem
from loaders import LoaderManager
from models.user_profile import UserProfile
from models.game_profile import GameProfile
import pandas as pd
from datetime import datetime

# 系统配置参数
SYSTEM_CONFIG = {
    'debug_mode': False,                # 是否启用调试模式
    'data_dir': 'data/input',           # 数据文件目录
    'output_dir': 'matching_results',   # 输出结果目录
    'encoding': 'utf-8-sig'            # 文件编码
}

# 显示配置参数
DISPLAY_CONFIG = {
    'label_width': 16,     # 特征名称列宽
    'value_width': 30,     # 值列宽
    'contrib_width': 16,   # 贡献度列宽
    'separator_char': '=', # 分隔符字符
    'separator_length': 80 # 分隔符长度
}

# 匹配系统参数
MATCHING_CONFIG = {
    'default_top_n': 5,           # 默认返回的匹配结果数量
    'max_recommended_games': 1,     # 最大推荐游戏数量
    'min_similarity_threshold': 0.3 # 最小相似度阈值
}

class MatchingApp:
    """匹配系统应用类，封装主要的匹配功能和交互逻辑"""
    
    def __init__(self, debug_mode: bool = SYSTEM_CONFIG['debug_mode']):
        """初始化匹配系统
        
        Args:
            debug_mode: 是否启用调试模式
        """
        self.users: List[UserProfile] = []
        self.games: List[GameProfile] = []
        self.debug_mode = debug_mode
        self.matcher = None  # 延迟初始化匹配器，等待游戏数据加载完成
        
    def load_data(self) -> None:
        """加载用户和游戏数据"""
        print("正在加载数据...")
        try:
            # 获取data/input目录的绝对路径
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  SYSTEM_CONFIG['data_dir'])
            
            # 初始化加载器管理器
            loader = LoaderManager()
            pools_loader = loader.pools_loader
            
            # 加载用户和游戏数据
            self.users = pools_loader.load_user_pool()
            self.games = pools_loader.load_game_pool()
            
            # 初始化匹配器
            self.matcher = MatchingSystem(self.games)
                
            print(f"成功加载 {len(self.users)} 个用户和 {len(self.games)} 个游戏")
            
        except Exception as e:
            print(f"数据加载失败: {str(e)}")
            if self.debug_mode:
                raise
            sys.exit(1)
            
    def print_user_comparison(
        self,
        target_user: UserProfile,
        matched_user: UserProfile,
        similarity: float,
        contributions: Dict[str, float],
        recommended_games: List[Tuple[str, float]] = None
    ) -> None:
        """打印用户信息对比和匹配度
        
        Args:
            target_user: 目标用户
            matched_user: 匹配到的用户
            similarity: 总匹配度
            contributions: 各维度贡献度
            recommended_games: 推荐的游戏列表
        """
        def get_str_width(s: str) -> int:
            """计算字符串的显示宽度（中文字符计2个宽度）"""
            width = 0
            for c in str(s):
                width += 2 if ord(c) > 127 else 1
            return width
            
        def pad_str(s: str, width: int) -> str:
            """将字符串填充到指定显示宽度"""
            current_width = get_str_width(s)
            if current_width < width:
                return s + ' ' * (width - current_width)
            return s
            
        def wrap_text(text: str, width: int) -> List[str]:
            """将文本按显示宽度换行"""
            if get_str_width(str(text)) <= width:
                return [str(text)]
                
            result = []
            current_line = ''
            current_width = 0
            
            for char in str(text):
                char_width = get_str_width(char)
                if current_width + char_width <= width:
                    current_line += char
                    current_width += char_width
                else:
                    if current_line:
                        result.append(current_line)
                    current_line = char
                    current_width = char_width
                    
            if current_line:
                result.append(current_line)
            return result
            
        def get_user_game_types(user: UserProfile) -> str:
            """获取用户的游戏类型偏好"""
            game_types = set()
            for game in user.games:
                # 从游戏池中找到对应的游戏
                for game_profile in self.games:
                    if game_profile.name == game:
                        game_types.update(game_profile.types)
            return ", ".join(sorted(game_types)) if game_types else "未知"
            
        # 定义特征列表
        features = [
            ("用户ID", "user_id", None),
            ("性别", "gender", None),
            ("性别偏好", lambda u: ", ".join(u.gender_preference), None),
            ("游戏", lambda u: ", ".join(u.games) + 
                (f", {recommended_games[0][0]}(推荐度: {recommended_games[0][1]*100:.2f}%)" 
                 if u == target_user and recommended_games else ""), None),
            ("游戏时间", "play_time", "time"),
            ("游戏区服", "play_region", "server"),
            ("MBTI", "mbti", "mbti"),
            ("星座", "zodiac", "zodiac"),
            ("游戏经验", "game_experience", "experience"),
            ("在线状态", "online_status", "online_status"),
            ("游戏风格", "game_style", "style"),
            ("游戏类型", lambda u: get_user_game_types(u), "game_type")
        ]
        
        # 使用配置的列宽
        label_width = DISPLAY_CONFIG['label_width']
        value_width = DISPLAY_CONFIG['value_width']
        contrib_width = DISPLAY_CONFIG['contrib_width']
        
        # 获取所有值
        user1_values = []
        user2_values = []
        contribution_values = []
        
        for label, attr, contrib_key in features:
            # 获取用户值
            if callable(attr):
                value1 = attr(target_user)
                value2 = attr(matched_user)
            elif attr:
                value1 = getattr(target_user, attr)
                value2 = getattr(matched_user, attr)
            else:
                value1 = "-"
                value2 = "-"
            user1_values.append(value1)
            user2_values.append(value2)
            
            # 获取贡献度值
            if contrib_key:
                contrib = contributions.get(contrib_key, 0)
                contribution_values.append(f"{contrib*100:.1f}%")  # 将分数转换为百分比并添加%
            else:
                contribution_values.append("-")
                
        # 添加总匹配度
        features.append(("总匹配度", None, None))
        user1_values.append("-")
        user2_values.append("-")
        contribution_values.append(f"{similarity*100:.1f}%")  # 将分数转换为百分比并添加%
        
        # 计算分隔线长度
        total_width = label_width + value_width * 2 + contrib_width
        
        # 打印表头
        print("\n用户匹配结果:")
        print(DISPLAY_CONFIG['separator_char'] * total_width)
        
        # 打印列标题
        header = (
            pad_str("特征", label_width) +
            pad_str("目标用户", value_width) +
            pad_str("匹配用户", value_width) +
            pad_str("匹配度", contrib_width)
        )
        print(header)
        print("-" * total_width)
        
        # 打印每个特征的值
        for i, (label, _, _) in enumerate(features):
            # 将值按宽度换行
            value1_lines = wrap_text(user1_values[i], value_width - 2)
            value2_lines = wrap_text(user2_values[i], value_width - 2)
            contrib_line = contribution_values[i]
            
            # 获取最大行数
            max_lines = max(len(value1_lines), len(value2_lines))
            
            # 打印第一行（包含标签）
            first_line = (
                pad_str(label, label_width) +
                pad_str(value1_lines[0] if value1_lines else "", value_width) +
                pad_str(value2_lines[0] if value2_lines else "", value_width) +
                pad_str(contrib_line, contrib_width)
            )
            print(first_line)
            
            # 打印剩余行
            for line_idx in range(1, max_lines):
                next_line = (
                    pad_str("", label_width) +
                    pad_str(value1_lines[line_idx] if line_idx < len(value1_lines) else "", value_width) +
                    pad_str(value2_lines[line_idx] if line_idx < len(value2_lines) else "", value_width) +
                    pad_str("", contrib_width)
                )
                print(next_line)
        
        print(DISPLAY_CONFIG['separator_char'] * total_width)
        
    def save_results(
        self,
        matches: List[Tuple[UserProfile, float, Dict[str, float], List[Tuple[str, float]]]],
        target_user: UserProfile
    ) -> None:
        """保存匹配结果到CSV文件"""
        try:
            results = []
            for user, similarity, contributions, _ in matches:
                result = {
                    '目标用户ID': target_user.user_id,
                    '匹配用户ID': user.user_id,
                    '总匹配度': f"{similarity*100:.1f}%",
                    '时间匹配': f"{contributions.get('time', 0)*100:.1f}%",
                    '区服匹配': f"{contributions.get('server', 0)*100:.1f}%",
                    '游戏相似度': f"{contributions.get('game_type', 0)*100:.1f}%",
                    'MBTI匹配': f"{contributions.get('mbti', 0)*100:.1f}%",
                    '游戏风格匹配': f"{contributions.get('style', 0)*100:.1f}%"
                }
                results.append(result)
                
            df = pd.DataFrame(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    SYSTEM_CONFIG['output_dir'])
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, 
                                     f"matching_results_{target_user.user_id}_{timestamp}.csv")
            df.to_csv(output_file, index=False, encoding=SYSTEM_CONFIG['encoding'])
            print(f"\n结果已保存到: {output_file}")
            
        except Exception as e:
            print(f"保存结果失败: {str(e)}")
            if self.debug_mode:
                raise
                
    def run(self) -> None:
        """运行匹配系统主循环"""
        self.load_data()
        
        while True:
            try:
                # 显示用户选择提示
                print(f"\n请输入要查看的用户编号 (1-{len(self.users)})，输入0退出：")
                user_index = int(input().strip())
                
                # 检查是否退出
                if user_index == 0:
                    print("程序已退出")
                    break
                    
                # 验证输入范围
                if user_index < 1 or user_index > len(self.users):
                    print(f"请输入1到{len(self.users)}之间的数字！")
                    continue
                    
                # 获取目标用户并执行匹配
                target_user = self.users[user_index - 1]
                print("\n正在执行匹配...")
                matches = self.matcher.find_best_matches(
                    target_user, 
                    self.users,
                    top_n=MATCHING_CONFIG['default_top_n']
                )
                
                if not matches:
                    print("\n未找到匹配的用户。")
                    continue
                    
                # 显示匹配结果
                print(f"\n找到 {len(matches)} 个匹配结果，显示匹配度最高的 {MATCHING_CONFIG['default_top_n']} 个：")
                
                # 显示匹配结果
                for matched_user, match_scores in matches:
                    self.print_user_comparison(
                        target_user,
                        matched_user,
                        match_scores['total_score'],
                        match_scores,
                        None  # 新版本不支持游戏推荐
                    )
                    print("\n" + DISPLAY_CONFIG['separator_char'] * DISPLAY_CONFIG['separator_length'])
                
                # 询问是否保存结果
                print("\n是否要保存匹配结果到CSV文件？(y/n)")
                if input().strip().lower() == 'y':
                    self.save_results(
                        [(user, scores['total_score'], scores, None) for user, scores in matches],
                        target_user
                    )
                    
            except ValueError:
                print("输入错误：请输入有效的数字！")
            except Exception as e:
                print(f"发生错误: {str(e)}")
                if self.debug_mode:
                    raise
                    
def main():
    """主函数"""
    try:
        # 创建并运行匹配系统
        system = MatchingApp(debug_mode=SYSTEM_CONFIG['debug_mode'])
        system.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行失败: {str(e)}")
        
if __name__ == "__main__":
    main() 