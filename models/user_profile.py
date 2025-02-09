"""用户档案模型

定义用户的基本信息和偏好
"""

from typing import List

class UserProfile:
    """用户档案类"""
    
    def __init__(
        self,
        user_id: str,
        gender: str,
        gender_preference: List[str],
        play_region: str,
        play_time: str,
        mbti: str,
        zodiac: str,
        game_experience: str,
        online_status: str,
        game_style: str,
        games: List[str]
    ):
        """初始化用户档案
        
        Args:
            user_id: 用户ID
            gender: 性别
            gender_preference: 性别偏好列表
            play_region: 游戏区服
            play_time: 游戏时间段
            mbti: MBTI性格类型
            zodiac: 星座
            game_experience: 游戏经验等级
            online_status: 在线状态
            game_style: 游戏风格
            games: 游戏列表
        """
        self.user_id = user_id
        self.gender = gender
        self.gender_preference = gender_preference
        self.play_region = play_region
        self.play_time = play_time
        self.mbti = mbti
        self.zodiac = zodiac
        self.game_experience = game_experience
        self.online_status = online_status
        self.game_style = game_style
        self.games = games
        
    def __eq__(self, other):
        """判断两个用户是否相同"""
        if not isinstance(other, UserProfile):
            return False
        return self.user_id == other.user_id

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