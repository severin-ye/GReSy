# GReSy (Game Recommendation System)

GReSy is an intelligent game player matching recommendation system that recommends the most suitable gaming partners by analyzing multiple dimensions of user preferences, personal characteristics, and gaming habits.

## Features

- 🎮 Multi-dimensional Feature Matching
  - Game Preference Matching
  - Gender Feature Matching
  - Game Server Matching
  - Gaming Time Matching
  - MBTI Personality Matching
  - Gaming Experience Matching
  - Gaming Style Matching
  - Constellation Matching
  - Online Status Matching

- 📊 Smart Weight Distribution
  - Game Preferences: 80%
  - Gender Features: 20%
  - Game Servers: 15%
  - Gaming Time: 10%
  - MBTI Personality: 7.5%
  - Gaming Experience: 7.5%
  - Gaming Style: 5%
  - Constellation: 2.5%
  - Online Status: 2.5%

- 🔍 Precise Matching Algorithm
  - Basic Matching Module
  - Numerical Similarity Matching
  - Preference List Matching
  - Multi-dimensional Comprehensive Matching

## Installation

1. Clone the project
```bash
git clone [project-url]
cd GReSy
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare Data
   - Prepare the following data files in the `data/pools` directory:
     - `user_pool.json`: User data
     - `game_pool.json`: Game data
     - `mbti_pool.json`: MBTI personality data
     - `constellation_pool.json`: Constellation data
     - `server_pool.json`: Server data

2. Run the system
```bash
python main.py
```

## Project Structure

```
GReSy/
├── data/               # Data directory
├── loaders/           # Data loading modules
├── matching/          # Matching algorithm modules
├── models/           # Data models
├── tests/            # Test cases
├── main.py           # Main program entry
└── requirements.txt  # Project dependencies
```

## Documentation

- [System Structure Description](doc_Structure_Description.md)
- [Update Log](doc_log.md)
