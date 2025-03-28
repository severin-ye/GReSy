# GReSy (Game Recommendation System)

GReSy 是一个智能游戏玩家匹配推荐系统，通过分析用户的游戏偏好、个人特征和游戏习惯等多个维度，为用户推荐最合适的游戏伙伴。

## 功能特性

- 🎮 多维度特征匹配
  - 游戏偏好匹配
  - 性别特征匹配
  - 游戏区服匹配
  - 游戏时间匹配
  - MBTI性格匹配
  - 游戏经验匹配
  - 游戏风格匹配
  - 星座匹配
  - 在线状态匹配

- 📊 智能权重分配
  - 游戏偏好：80%
  - 性别特征：20%
  - 游戏区服：15%
  - 游戏时间：10%
  - MBTI性格：7.5%
  - 游戏经验：7.5%
  - 游戏风格：5%
  - 星座：2.5%
  - 在线状态：2.5%

- 🔍 精确匹配算法
  - 基础匹配模块
  - 数值相似度匹配
  - 偏好列表匹配
  - 多维度综合匹配

## 安装说明

1. 克隆项目
```bash
git clone [项目地址]
cd GReSy
```

2. 创建并激活虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

1. 准备数据
   - 在 `data/pools` 目录下准备以下数据文件：
     - `user_pool.json`：用户数据
     - `game_pool.json`：游戏数据
     - `mbti_pool.json`：MBTI性格数据
     - `constellation_pool.json`：星座数据
     - `server_pool.json`：服务器数据

2. 运行系统
```bash
python main.py
```

## 项目结构

```
GReSy/
├── data/               # 数据目录
├── loaders/           # 数据加载模块
├── matching/          # 匹配算法模块
├── models/           # 数据模型
├── tests/            # 测试用例
├── main.py           # 主程序入口
└── requirements.txt  # 项目依赖
```

## 文档

- [系统结构说明](doc_Structure_Description.md)
- [更新日志](doc_log.md)

## 许可证

[待补充]

## 贡献指南

[待补充] 