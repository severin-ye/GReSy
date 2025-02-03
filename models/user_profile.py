from dataclasses import dataclass
from typing import List

@dataclass
class UserProfile:
    """用户档案类,存储用户的基本信息和偏好"""
    user_id: str                # 用户唯一标识符
    games: List[str]            # 用户玩的游戏列表
    gender: str                 # 用户性别
    gender_preference: List[str] # 用户性别偏好优先级列表
    play_region: str            # 用户常用游戏服务器
    play_time: str              # 用户常规游戏时间段
    mbti: str                   # 用户MBTI性格类型
    zodiac: str                 # 用户星座
    game_experience: str        # 用户游戏经验水平
    online_status: str          # 用户在线状态
    game_style: str             # 用户游戏风格
    
    def to_dict(self) -> dict:
        """将用户档案转换为字典格式"""
        return {
            'user_id': self.user_id,
            'games': self.games,
            'gender': self.gender,
            'gender_preference': self.gender_preference[0] if self.gender_preference else '不限',
            'play_region': self.play_region,
            'play_time': self.play_time,
            'mbti': self.mbti,
            'zodiac': self.zodiac,
            'game_experience': self.game_experience,
            'online_status': self.online_status,
            'game_style': self.game_style
        }