# 游戏玩家匹配推荐系统结构说明文档

## 1. 系统概述

### 1.1 系统目标
这是一个基于用户特征的游戏玩家匹配推荐系统。系统通过分析用户的游戏偏好、个人特征和游戏习惯等多个维度，为用户推荐最合适的游戏伙伴。

### 1.2 核心功能
- 用户档案管理
- 多维度特征匹配
- 基于性别偏好的优先级匹配
- 特征贡献度分析

## 2. 系统架构

### 2.1 数据层
#### 2.1.1 数据存储结构
- `pools` 目录：原始数据存储
  - `user_pool.json`：用户数据
  - `game_pool.json`：游戏数据
  - `mbti_pool.json`：MBTI性格数据
  - `constellation_pool.json`：星座数据
  - `server_pool.json`：服务器数据

#### 2.1.2 数据加载层
- `loaders` 目录：数据加载和处理
  - `pools_loader.py`：加载各种池数据
  - `weights_loader.py`：加载权重配置
  - `config_loader.py`：加载系统配置

#### 2.1.3 数据模型层
- `models` 目录：核心业务实体定义
  - `user_profile.py`：用户档案模型
  - `game_profile.py`：游戏档案模型

### 2.2 核心模型

#### 2.2.1 UserProfile 类
主要属性：
- user_id：用户唯一标识符
- games：用户玩的游戏列表
- gender：用户性别
- gender_preference：性别偏好列表
- play_region：游戏服务器区域
- play_time：常规游戏时间段
- mbti：MBTI性格类型
- zodiac：星座
- game_experience：游戏经验水平
- online_status：在线状态
- game_style：游戏风格

#### 2.2.2 UserMatchingSystem 类
主要功能：
- 用户特征编码
- 相似度计算
- 匹配推荐
- 特征贡献度分析

## 3. 匹配算法设计

### 3.1 特征权重分配
系统对不同特征设定了以下权重：
- 游戏偏好：80%
- 性别特征：20%
- 游戏区服：15%
- 游戏时间：10%
- MBTI性格：7.5%
- 游戏经验：7.5%
- 游戏风格：5%
- 星座：2.5%
- 在线状态：2.5%

### 3.2 匹配模块分类

#### 3.2.1 基础匹配模块
- 处理简单的二元匹配逻辑
- 适用于：
  - 在线状态（完全匹配/不匹配）
  - 服务器匹配（完全匹配/组内匹配/不匹配）

#### 3.2.2 数值相似度匹配模块
- 处理基于数值范围的匹配逻辑
- 适用于：
  - 游戏风格（0-10数值相似度）
  - 游戏经验（0-10数值相似度）
  - 游玩固定时间（0-10数值相似度）

#### 3.2.3 偏好列表匹配模块--权重
- 处理基于偏好列表顺位的匹配逻辑
- 适用于：
  - MBTI匹配（基于偏好列表顺位权重）
  - 星座匹配（基于偏好列表顺位权重）

#### 3.2.4 偏好列表匹配模块--强制顺位
- 处理基于列表顺位依次匹配的逻辑
- 适用于：
  - 性别匹配（基于列表顺位依次匹配）

#### 3.2.5 多维度综合匹配模块
- 处理需要多个维度综合考虑的复杂匹配逻辑
- 适用于游戏匹配的三个维度：
  - 游戏类型相似度
  - 游戏偏好相似度（共同游戏）
  - 社交属性相似度

### 3.3 匹配算法流程

1. **预处理阶段**
   - 将用户添加到系统
   - 对分类特征进行编码
   - 标准化特征数据

2. **匹配计算阶段**
   - 筛选共同游戏的用户
   - 计算用户间的特征相似度
   - 应用性别偏好权重
   - 计算特征贡献度

3. **结果排序阶段**
   - 按性别偏好优先级分组
   - 根据总体相似度排序
   - 返回指定数量的最佳匹配

## 4. 系统特征定义

### 4.1 游戏相关
- 游戏类型：
  - 王者荣耀
  - 英雄联盟
  - 绝地求生
  - 和平精英
- 游戏属性（隐藏）：
  - FPS
  - MOBA
  - 手游
  - 端游

### 4.2 用户特征
- 性别：男、女、赛博人
- 性别倾向：男、女、赛博人
- 游玩服务器：国服、亚服、欧服、美服
- 在线状态：在线、离线
- 游玩固定时间：早上、中午、晚上
- MBTI：16种性格类型
- 星座：12星座
- 游戏风格：强硬、保守
- 游戏经验：高超、初级

## 5. 推荐策略

### 5.1 离线索引
- 用户->物品
- 用户->喜爱->物品 (nk个)
- 用户->喜爱->物品 (n个) -> 物品-相似->物品 (k个)

### 5.2 在线召回
- 用户->喜爱->用户
- 用户->喜爱->标签(基于特征的ELO) -> 标签-相似->标签-对应->用户 