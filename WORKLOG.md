# WORKLOG

## Session: 2026-05-25 14:00

### Agent: Claude

**完成：**
- 建立全局用户偏好系统 (`~/.claude/user_preferences.md`)
- 定义 Claude+Codex 协作模式
- 定义 WORKLOG 格式规范
- 审阅 `ai_quant_learning_roadmap.md`，评估可行性
- 更新 roadmap：
  - Phase 0 结构更完整（加入 config/, tests/, utils/）
  - 新增 Phase 3.5 基本面数据
  - Phase 9 补充特征工程和实验追踪
  - 每个 Phase 加入完成标准
- 创建完整学习 notebook 系列：
  - `notebooks/learning_guide_p1_p3.ipynb` — 数据层、可视化、技术指标
  - `notebooks/learning_guide_p4_p5.ipynb` — 风险分析、市场概览
  - `notebooks/learning_guide_p6_p7.ipynb` — 股票详情、Watchlist
  - `notebooks/learning_guide_p8_p9.ipynb` — 回测、预测系统
  - `notebooks/experiments/` — 自由实验目录

**下一步：**
- 用户阅读 notebook 学习概念
- Codex 执行 Phase 1-3 开发（指令见下方）

---

## Session: 2026-05-25 12:44

### Agent: Codex

**完成：**
- 读取 `ai_quant_learning_roadmap.md` 和 `WORKLOG.md`
- 执行 Phase 0 初始化，创建可运行项目骨架：
  - `app.py`
  - `requirements.txt`
  - `config/settings.py`
  - `config/__init__.py`
  - `data/raw/`, `data/processed/`, `data/cache/`
  - `features/`, `pages/`, `utils/`, `notebooks/`, `tests/`
- 更新 `README.md`，加入 setup、run 和项目结构说明
- 新增 `.gitignore`，忽略 `.DS_Store`、Python 缓存和本地虚拟环境
- 创建本地虚拟环境 `venv`
- 安装 Phase 0 依赖：
  - `streamlit`
  - `pandas`
  - `numpy`
  - `plotly`
  - `yfinance`

**验证：**
- `python -m py_compile app.py config/settings.py` 通过
- `venv/bin/streamlit run app.py --server.headless true --server.port 8501` 成功启动
- `curl -I http://localhost:8501` 返回 `HTTP/1.1 200 OK`
- 验证后已停止 Streamlit 测试服务

**备注：**
- 内置浏览器插件当前没有可用 `iab` 实例，因此页面验证采用本地 HTTP 请求完成
- `ai_quant_learning_roadmap.md` 在本次开始前已有未提交修改，本次未改动

**下一步：**
- 开始 Phase 1 Data Layer：
  - 下载 SPY、QQQ、DIA、IWM、VIX
  - 设计 watchlist 支持
  - 增加数据缓存
  - 建立历史价格存储模块

---

## Session: 2026-05-25 12:46

### Agent: Codex

**完成：**
- 新增 `AGENTS.md`
- 记录后续 AI agent 的工作规范：
  - session 开始先读 `WORKLOG.md` 和 `ai_quant_learning_roadmap.md`
  - 检查 `git status --short`
  - 根据 `WORKLOG.md` 的下一步继续工作
  - session 结束前必须更新 `WORKLOG.md`
  - 不覆盖或回滚用户/其他 agent 的已有修改
  - 每个阶段或重要改动都要验证并记录结果
- 明确当前状态：
  - Phase 0 已完成
  - 下一步是 Phase 1 Data Layer

**验证：**
- 文件已创建：`AGENTS.md`

**下一步：**
- 执行 Phase 1-3 开发（指令见下方）

---

## Session: 2026-05-25 14:57

### Agent: Codex

**完成：**
- 按 `AGENTS.md` 读取 `WORKLOG.md`、`ai_quant_learning_roadmap.md` 并检查 `git status --short`
- 执行 Phase 1-3 开发：
  - 新增 `utils/data_loader.py`
  - 新增 `utils/cache_manager.py`
  - 新增 `utils/chart_builder.py`
  - 新增 `features/indicators.py`
  - 新增 `features/trend.py`
  - 新增 `features/momentum.py`
  - 新增 `features/volatility.py`
  - 新增 `pages/1_Market_Overview.py`
  - 新增 `pages/2_Stock_Detail.py`
  - 新增 `tests/test_data_loader.py`
  - 新增 `tests/test_indicators.py`
- 更新 `config/settings.py`：
  - `DEFAULT_PERIOD`
  - `CACHE_MAX_AGE_HOURS`
  - `CACHE_FILE_FORMAT`
  - `TICKER_ALIASES`
  - `DATA_PROCESSED_DIR`
- 更新 `requirements.txt`：
  - `pyarrow>=14.0.0`
  - `pytest>=8.0.0`
- 更新 `README.md`，加入测试命令
- 更新 `.gitignore`，忽略真实下载产生的 `data/cache/*.parquet`
- 安装新增依赖到本地 `venv`

**实现细节：**
- `DataLoader` 支持单股票下载、批量下载、parquet 缓存、缓存过期检查和清理
- `VIX` 自动映射到 yfinance 的 `^VIX`
- 单元测试使用 mock yfinance，避免测试依赖网络
- `ChartBuilder` 支持 K 线图、成交量、折线图、多股票归一化对比、收益率图和移动均线叠加
- 技术指标支持 MA20 / MA50 / MA200、RSI14、MACD、Bollinger Bands、ATR14
- Streamlit 多页面：
  - Market Overview：默认 ETF 多股票对比和最新价格表
  - Stock Detail：个股 K 线图、移动均线、指标快照

**验证：**
- `venv/bin/python -m py_compile app.py config/settings.py utils/cache_manager.py utils/data_loader.py utils/chart_builder.py features/indicators.py features/trend.py features/momentum.py features/volatility.py pages/1_Market_Overview.py pages/2_Stock_Detail.py tests/test_data_loader.py tests/test_indicators.py` 通过
- `venv/bin/python -m pytest tests/test_data_loader.py tests/test_indicators.py` 通过：`9 passed`
- 真实 yfinance 下载验证通过：`SPY`、`QQQ`、`DIA`、`IWM`、`VIX`
- `venv/bin/streamlit run app.py --server.headless true --server.port 8501` 成功启动
- `curl -I http://localhost:8501` 返回 `HTTP/1.1 200 OK`
- 验证后已停止 Streamlit 测试服务

**备注：**
- 初次真实 yfinance 下载在沙箱网络下失败；授权联网后验证通过
- 真实下载产生的缓存文件保留在 `data/cache/`，但已被 `.gitignore` 忽略
- `ai_quant_learning_roadmap.md` 在本次开始前已有未提交修改，本次未改动

**下一步：**
- 开始 Phase 4-5：
  - 实现 `features/risk_metrics.py`
  - 在 Stock Detail 页面加入风险指标面板
  - 扩展 Market Overview 页面：VIX 风险面板、市场状态判断、板块 ETF 表现
  - 创建 `utils/market_regime.py`

---
---

# Codex 任务指令

以下任务按 Phase 归类，对应学习 notebook 的分组方式。

---

## 📦 Phase 1-3：数据层 + 可视化 + 技术指标

**对应学习材料：** `notebooks/learning_guide_p1_p3.ipynb`

---

### Phase 1 — Data Layer

**目标：** 建立数据获取、缓存、存储体系

#### 1. 创建模块文件

```
utils/data_loader.py      # 数据下载与缓存核心逻辑
utils/cache_manager.py    # 缓存管理（过期检查、清理）
config/settings.py        # 更新：添加数据相关配置
```

#### 2. utils/data_loader.py 核心功能

```python
"""
数据加载模块
- 从 yfinance 下载 OHLCV 数据
- 本地缓存（避免重复请求）
- 支持单股票和多股票批量下载
"""
import yfinance as yf
import pandas as pd
from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict

class DataLoader:
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def download(self, ticker: str, period: str = "2y", use_cache: bool = True) -> pd.DataFrame:
        """下载单只股票数据，优先使用缓存"""
        pass
    
    def download_batch(self, tickers: List[str], period: str = "2y") -> Dict[str, pd.DataFrame]:
        """批量下载多只股票"""
        pass
    
    def _load_from_cache(self, ticker: str) -> Optional[pd.DataFrame]:
        """从缓存加载"""
        pass
    
    def _save_to_cache(self, ticker: str, df: pd.DataFrame) -> None:
        """保存到缓存"""
        pass
    
    def is_cache_valid(self, ticker: str, max_age_hours: int = 24) -> bool:
        """检查缓存是否有效（未过期）"""
        pass
    
    def clear_cache(self, ticker: Optional[str] = None) -> None:
        """清理缓存"""
        pass
```

#### 3. 更新 config/settings.py

添加：
```python
# Data settings
DEFAULT_PERIOD = "2y"  # 默认下载两年数据
CACHE_MAX_AGE_HOURS = 24  # 缓存有效期
DEFAULT_TICKERS = ["SPY", "QQQ", "DIA", "IWM", "VIX"]

# 缓存文件格式
CACHE_FILE_FORMAT = "{ticker}_{date}.parquet"
```

#### 4. 更新 requirements.txt

添加：
```
pyarrow>=14.0.0  # parquet 支持
```

#### 5. 测试验证

创建 `tests/test_data_loader.py`

#### 6. 完成标准

- `DataLoader` 类能下载单只/多只股票
- 缓存功能正常（第二次读取走缓存）
- `pytest tests/test_data_loader.py` 通过
- 无 API 报错

---

### Phase 2 — Visualization

**目标：** 创建可视化能力，建立市场直觉

#### 1. 创建模块文件

```
utils/chart_builder.py        # 图表构建核心
pages/1_Market_Overview.py    # 市场概览页面
```

#### 2. utils/chart_builder.py 核心功能

```python
"""
图表构建模块
使用 Plotly 创建交互式图表
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List

class ChartBuilder:
    @staticmethod
    def candlestick(df: pd.DataFrame, title: str = "", show_volume: bool = True) -> go.Figure:
        """K线图（含成交量）"""
        pass
    
    @staticmethod
    def line_chart(df: pd.DataFrame, column: str = "Close", title: str = "") -> go.Figure:
        """折线图"""
        pass
    
    @staticmethod
    def multi_comparison(dfs: dict, column: str = "Close", normalize: bool = True) -> go.Figure:
        """多股票对比图（归一化）"""
        pass
    
    @staticmethod
    def returns_chart(df: pd.DataFrame, period: str = "D") -> go.Figure:
        """收益率图"""
        pass
    
    @staticmethod
    def add_moving_averages(fig: go.Figure, df: pd.DataFrame, periods: List[int] = [20, 50, 200]) -> go.Figure:
        """添加移动平均线"""
        pass
```

#### 3. pages/1_Market_Overview.py

```python
"""
市场概览页面
- 显示默认 ETF 列表
- 快速对比功能
"""
import streamlit as st
from utils.data_loader import DataLoader
from utils.chart_builder import ChartBuilder
from config.settings import DEFAULT_TICKERS

st.title("📊 Market Overview")

# 侧边栏：选择股票
tickers = st.multiselect("Select Tickers", DEFAULT_TICKERS, default=DEFAULT_TICKERS[:3])

# 下载数据
loader = DataLoader()
data = {}
for ticker in tickers:
    data[ticker] = loader.download(ticker)

# 显示对比图
if data:
    fig = ChartBuilder.multi_comparison(data, normalize=True)
    st.plotly_chart(fig, use_container_width=True)
```

#### 4. 完成标准

- `streamlit run app.py` 能看到侧边栏导航
- Market Overview 页面能展示多股票对比图
- K线图能正常显示蜡烛和成交量
- 图表交互正常（缩放、hover）

---

### Phase 3 — Technical Indicators

**目标：** 实现常用技术指标，为分析打基础

#### 1. 创建模块文件

```
features/indicators.py    # 技术指标计算
features/trend.py         # 趋势类指标（MA）
features/momentum.py      # 动量类指标（RSI, MACD）
features/volatility.py    # 波动率指标（BB, ATR）
```

#### 2. features/indicators.py 核心功能

```python
"""
技术指标汇总模块
"""
import pandas as pd
import numpy as np
from typing import Optional

def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """一次性添加所有常用指标"""
    df = df.copy()
    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_bollinger_bands(df)
    df = add_atr(df)
    return df

def add_moving_averages(df: pd.DataFrame, periods: list = [20, 50, 200]) -> pd.DataFrame:
    """添加移动平均线"""
    pass

def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """添加 RSI 指标"""
    pass

def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """添加 MACD 指标"""
    pass

def add_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
    """添加布林带"""
    pass

def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """添加 ATR（平均真实波幅）"""
    pass
```

#### 3. 创建 pages/2_Stock_Detail.py

股票详情页面，展示 K 线图和技术指标面板。

#### 4. 测试验证

创建 `tests/test_indicators.py`

#### 5. 完成标准

- 所有指标函数独立可测试
- `pytest tests/test_indicators.py` 通过
- Stock Detail 页面能展示指标
- 指标数值合理（RSI 在 0-100 之间）

---

## 📦 Phase 4-5：风险分析 + 市场概览

**对应学习材料：** `notebooks/learning_guide_p4_p5.ipynb`

---

### Phase 4 — Risk Analysis

**目标：** 实现风险评估体系

#### 1. 创建模块文件

```
features/risk_metrics.py    # 风险指标计算
```

#### 2. 实现的风险指标

- 日收益率 / 年化收益率
- 波动率（日/年化）
- 最大回撤
- 夏普比率
- Sortino 比率
- Beta（相对于 SPY）
- 相关性矩阵

#### 3. 更新 pages/2_Stock_Detail.py

添加风险指标面板。

#### 4. 完成标准

- 能计算所有风险指标
- Stock Detail 页面展示风险面板
- 数值计算正确

---

### Phase 5 — Market Overview Dashboard

**目标：** 完善市场概览功能

#### 1. 更新 pages/1_Market_Overview.py

添加功能：
- 板块 ETF 表现
- VIX 风险面板
- 市场状态判断（Risk-On / Neutral / Risk-Off）

#### 2. 创建 utils/market_regime.py

市场状态判断逻辑。

#### 3. 完成标准

- 能展示板块轮动
- VIX 指标实时显示
- 市场状态判断正确

---

## 📦 Phase 6-7：股票详情 + Watchlist

**对应学习材料：** `notebooks/learning_guide_p6_p7.ipynb`

---

### Phase 6 — Stock Detail Page

**目标：** 完善个股分析页面

#### 1. 完善 pages/2_Stock_Detail.py

添加功能：
- 相对表现分析（vs SPY、vs 板块）
- Alpha 计算
- 多时间框架收益（5d/20d/60d/YTD）
- 综合分析报告

#### 2. 创建 utils/relative_performance.py

相对表现计算逻辑。

#### 3. 完成标准

- 能对比股票 vs 基准
- 显示超额收益
- 页面信息完整

---

### Phase 7 — Watchlist System

**目标：** 实现多股票追踪系统

#### 1. 创建模块文件

```
utils/watchlist_manager.py    # Watchlist 管理
pages/3_Watchlist.py          # Watchlist 页面
```

#### 2. 功能

- 添加/删除股票
- 多股票数据同步
- 多时间框架收益对比
- 风险收益排名
- 风险收益散点图

#### 3. 数据存储

使用 JSON 存储 watchlist 配置。

#### 4. 完成标准

- 能管理多个 watchlist
- 排名功能正常
- 可视化对比正常

---

## 📦 Phase 8-9：回测 + 预测

**对应学习材料：** `notebooks/learning_guide_p8_p9.ipynb`

---

### Phase 8 — Backtesting

**目标：** 实现简单回测框架

#### 1. 创建模块文件

```
backtest/
├── __init__.py
├── engine.py           # 回测引擎
├── strategies.py       # 策略定义
├── metrics.py          # 绩效指标
pages/4_Backtest.py     # 回测页面
```

#### 2. 实现的策略

- MA 交叉策略
- RSI 均值回归策略

#### 3. 绩效指标

- 年化收益
- 年化波动
- 夏普比率
- 最大回撤
- 胜率
- 盈亏比

#### 4. 完成标准

- 回测引擎运行正常
- 避免 look-ahead bias
- 考虑交易成本
- 可视化回测结果

---

### Phase 9 — Prediction System

**目标：** 实现基础预测功能

#### 1. 创建模块文件

```
ml/
├── __init__.py
├── features.py         # 特征工程
├── models.py           # 模型定义
├── validation.py       # 验证方法
├── experiments.py      # 实验管理
pages/5_Prediction.py   # 预测页面
```

#### 2. 功能

- 特征工程（收益率、波动率、技术指标）
- 目标变量创建（未来 N 天收益分类）
- 时间序列划分
- Walk-Forward 验证
- 特征重要性分析

#### 3. 模型

- Logistic Regression
- RandomForest

#### 4. 完成标准

- 特征工程正确（无数据泄露）
- 时间序列划分正确
- 模型训练和预测正常
- 实验记录完整

---

# 当前状态

- [x] Phase 0 — 项目初始化
- [ ] Phase 1-3 — 数据层 + 可视化 + 技术指标
- [ ] Phase 4-5 — 风险分析 + 市场概览
- [ ] Phase 6-7 — 股票详情 + Watchlist
- [ ] Phase 8-9 — 回测 + 预测

**下一步：** 用户学习 Phase 1-3 notebook，然后 Codex 执行 Phase 1-3 开发。
