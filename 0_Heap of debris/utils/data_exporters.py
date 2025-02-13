"""数据导出器模块

负责将匹配结果导出为各种格式
"""

import pandas as pd
from typing import List, Tuple, Dict
from models.user_profile import UserProfile

class MatchingResultExporter:
    """匹配结果导出器类"""
    
    @staticmethod
    def export_to_csv(
        matches: List[Tuple[UserProfile, float, Dict[str, float]]],
        target_user: UserProfile,
        output_file: str
    ) -> None:
        """将匹配结果导出为CSV文件
        
        Args:
            matches: 匹配结果列表
            target_user: 目标用户
            output_file: 输出文件路径
        """
        results = []
        for user, similarity, _ in matches:
            result = {
                '目标用户游戏': ','.join(target_user.games),
                '目标用户性别': target_user.gender,
                '目标用户性别倾向': ','.join(target_user.gender_preference),
                '目标用户游玩区服': target_user.play_region,
                '目标用户游玩时间': target_user.play_time,
                '目标用户MBTI': target_user.mbti,
                '目标用户星座': target_user.zodiac,
                '目标用户游戏经验': target_user.game_experience,
                '匹配用户游戏': ','.join(user.games),
                '匹配用户性别': user.gender,
                '匹配用户性别倾向': ','.join(user.gender_preference),
                '匹配用户游玩区服': user.play_region,
                '匹配用户游玩时间': user.play_time,
                '匹配用户MBTI': user.mbti,
                '匹配用户星座': user.zodiac,
                '匹配用户游戏经验': user.game_experience,
                '匹配度': f"{similarity:.2%}"
            }
            results.append(result)
            
            df = pd.DataFrame(results)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
    @staticmethod
    def format_match_result(
        user: UserProfile,
        similarity: float,
        contributions: Dict[str, float]
    ) -> str:
        """格式化单个匹配结果为字符串
        
        Args:
            user: 匹配的用户
            similarity: 匹配度
            contributions: 各特征的贡献度
            
        Returns:
            str: 格式化的匹配结果字符串
        """
        result = [
            f"总匹配度: {similarity:.2%}",
            f"用户ID: {user.user_id}",
            f"游戏: {', '.join(user.games)}",
            f"性别: {user.gender}",
            f"游玩服务器: {user.play_region} (贡献: {contributions.get('play_region', 0):.1f}%)",
            f"游玩时间: {user.play_time} (贡献: {contributions.get('play_time', 0):.1f}%)",
            f"游戏经验: {user.game_experience} (贡献: {contributions.get('game_experience', 0):.1f}%)",
            f"游戏风格: {user.game_style} (贡献: {contributions.get('game_style', 0):.1f}%)",
            f"在线状态: {user.online_status} (贡献: {contributions.get('online_status', 0):.1f}%)",
            f"MBTI: {user.mbti} (贡献: {contributions.get('mbti', 0):.1f}%)",
            f"星座: {user.zodiac} (贡献: {contributions.get('zodiac', 0):.1f}%)"
        ]
        return "\n".join(result) 