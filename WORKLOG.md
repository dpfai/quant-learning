# WORKLOG

## Session: 2026-06-14 (Claude)

### Agent: Claude

**完成：**
- 克隆 5 个 Finance AI Agent 参考仓库到 `reference-repos/`
- 创建 `reference-repos/README.md` — 仓库概述
- 创建 `reference-repos/STUDY_GUIDE.md` — 学习指南
- 更新 `.gitignore` 忽略克隆的仓库和图片
- 分析 Phase 1-3 实现与参考仓库的差异

**发现：**
- 当前 Phase 1-3 实现良好，无需大改
- 参考 TradingAgents 的 data provider 模式，建议重构数据层以支持多数据源
- 参考 ai-hedge-fund 的 Pydantic 数据模型，可用于数据验证

**下一步：**
- Codex 执行 Phase 1.5 — 数据层重构（见下方任务指令）
- 完成后继续 Phase 4-5

---

## 📦 Phase 1.5 — Data Layer Refactor (Codex Task)

**目标：** 重构数据层以支持多数据源，为未来扩展做准备

### 背景

参考 `reference-repos/TradingAgents/tradingagents/dataflows/` 的设计模式：
- 每个 data source 有独立的 module
- 统一的 interface 抽象
- 便于添加新数据源（Alpha Vantage, Polygon 等）

### 任务

#### 1. 创建目录结构

```
utils/
├── data_providers/
│   ├── __init__.py
│   ├── base.py           # 抽象基类
│   └── yfinance_provider.py  # 当前实现迁移
├── data_loader.py        # 保留，作为统一入口
└── cache_manager.py      # 保留
```

#### 2. utils/data_providers/base.py

```python
"""
Abstract base class for data providers.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import pandas as pd


class DataProvider(ABC):
    """Abstract interface for market data providers."""
    
    @abstractmethod
    def fetch_ohlcv(
        self, 
        ticker: str, 
        period: str = "2y",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """Fetch OHLCV data for a single ticker."""
        pass
    
    @abstractmethod
    def fetch_batch(
        self, 
        tickers: List[str], 
        period: str = "2y"
    ) -> Dict[str, pd.DataFrame]:
        """Fetch OHLCV data for multiple tickers."""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'yfinance', 'alpha_vantage')."""
        pass
```

#### 3. utils/data_providers/yfinance_provider.py

将现有 `data_loader.py` 中的 `DataLoader` 类逻辑迁移过来，实现 `DataProvider` 接口：

```python
"""
Yahoo Finance data provider implementation.
"""
import pandas as pd
import yfinance as yf
from typing import Dict, List, Optional
from pathlib import Path

from .base import DataProvider
from config.settings import (
    CACHE_FILE_FORMAT,
    CACHE_MAX_AGE_HOURS,
    DATA_CACHE_DIR,
    DEFAULT_PERIOD,
    TICKER_ALIASES,
)
from utils.cache_manager import CacheManager


class YFinanceProvider(DataProvider):
    """Yahoo Finance data provider with caching support."""
    
    REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]
    
    def __init__(self, cache_dir: str = DATA_CACHE_DIR, max_age_hours: int = CACHE_MAX_AGE_HOURS):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age_hours = max_age_hours
        self.cache_manager = CacheManager(str(self.cache_dir))
    
    @property
    def provider_name(self) -> str:
        return "yfinance"
    
    def fetch_ohlcv(
        self,
        ticker: str,
        period: str = DEFAULT_PERIOD,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """Fetch OHLCV data from Yahoo Finance."""
        # 迁移现有 DataLoader.download() 的逻辑
        # 支持 period 或 start_date/end_date 两种模式
        pass
    
    def fetch_batch(self, tickers: List[str], period: str = DEFAULT_PERIOD) -> Dict[str, pd.DataFrame]:
        """Fetch multiple tickers."""
        return {ticker: self.fetch_ohlcv(ticker, period=period) for ticker in tickers}
    
    # ... 其他私有方法迁移 (_normalize_ticker, _prepare_dataframe, 缓存相关方法)
```

#### 4. utils/data_loader.py (更新)

保留作为统一入口，简化为：

```python
"""
Unified data loading interface.
"""
from typing import Dict, List, Optional
import pandas as pd

from utils.data_providers.yfinance_provider import YFinanceProvider
from utils.data_providers.base import DataProvider


class DataLoader:
    """
    Unified interface for market data loading.
    
    Usage:
        loader = DataLoader()  # defaults to yfinance
        df = loader.download("SPY")
        
        # Future: use different provider
        # loader = DataLoader(provider="alpha_vantage")
    """
    
    def __init__(self, provider: str = "yfinance", **provider_kwargs):
        self._provider = self._get_provider(provider, **provider_kwargs)
    
    def _get_provider(self, name: str, **kwargs) -> DataProvider:
        if name == "yfinance":
            return YFinanceProvider(**kwargs)
        # Future providers:
        # elif name == "alpha_vantage":
        #     return AlphaVantageProvider(**kwargs)
        raise ValueError(f"Unknown provider: {name}")
    
    def download(self, ticker: str, period: str = "2y", use_cache: bool = True) -> pd.DataFrame:
        """Download single ticker data."""
        return self._provider.fetch_ohlcv(ticker, period=period)
    
    def download_batch(self, tickers: List[str], period: str = "2y") -> Dict[str, pd.DataFrame]:
        """Download multiple tickers."""
        return self._provider.fetch_batch(tickers, period=period)
    
    def is_cache_valid(self, ticker: str, max_age_hours: Optional[int] = None, period: str = "2y") -> bool:
        """Check cache validity."""
        return self._provider.is_cache_valid(ticker, max_age_hours, period)
    
    def clear_cache(self, ticker: Optional[str] = None) -> None:
        """Clear cache."""
        self._provider.clear_cache(ticker)
```

#### 5. 更新测试

更新 `tests/test_data_loader.py` 以适应新结构，确保测试通过。

### 完成标准

- [ ] `utils/data_providers/base.py` 创建并定义 `DataProvider` 抽象类
- [ ] `utils/data_providers/yfinance_provider.py` 实现具体 provider
- [ ] `utils/data_loader.py` 重构为统一入口
- [ ] 所有现有功能保持不变（向后兼容）
- [ ] `pytest tests/test_data_loader.py` 通过
- [ ] `streamlit run app.py` 正常运行

### 参考文件

- `reference-repos/TradingAgents/tradingagents/dataflows/` — Provider 模式参考
- `reference-repos/ai-hedge-fund/src/api.py` — 数据模型参考

### 备注

- 此重构为 Phase 1-3 的增强，不改变现有功能
- 为 Phase 3.5（基本面数据）和 Phase 4（多数据源）做准备
- 保持代码简洁，不要过度设计

---

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
tests/test_risk_metrics.py  # 单元测试
```

#### 2. features/risk_metrics.py 核心功能

```python
"""
风险指标计算模块
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple

def calculate_returns(df: pd.DataFrame, price_col: str = "Adj Close") -> pd.DataFrame:
    """计算日收益率"""
    pass

def calculate_annualized_return(returns: pd.Series, periods_per_year: int = 252) -> float:
    """计算年化收益率"""
    pass

def calculate_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    """计算年化波动率"""
    pass

def calculate_max_drawdown(prices: pd.Series) -> Tuple[float, pd.Timestamp, pd.Timestamp]:
    """计算最大回撤，返回 (回撤值, 起始日期, 结束日期)"""
    pass

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.05) -> float:
    """计算夏普比率"""
    pass

def calculate_sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.05) -> float:
    """计算 Sortino 比率（只考虑下行波动）"""
    pass

def calculate_beta(stock_returns: pd.Series, market_returns: pd.Series) -> float:
    """计算 Beta（相对于市场）"""
    pass

def calculate_correlation_matrix(returns_dict: Dict[str, pd.Series]) -> pd.DataFrame:
    """计算多资产相关性矩阵"""
    pass

def calculate_all_risk_metrics(prices: pd.Series, benchmark_prices: Optional[pd.Series] = None) -> Dict:
    """一次性计算所有风险指标"""
    pass
```

#### 3. 更新 pages/2_Stock_Detail.py

在现有页面添加风险指标面板：

```python
# 风险指标面板（在技术指标下方）
st.subheader("⚠️ Risk Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ann. Return", f"{metrics['ann_return']*100:.1f}%")
with col2:
    st.metric("Ann. Volatility", f"{metrics['ann_vol']*100:.1f}%")
with col3:
    st.metric("Max Drawdown", f"{metrics['max_dd']*100:.1f}%")
with col4:
    st.metric("Sharpe Ratio", f"{metrics['sharpe']:.2f}")

col5, col6, col7 = st.columns(3)
with col5:
    st.metric("Sortino Ratio", f"{metrics['sortino']:.2f}")
with col6:
    st.metric("Beta (vs SPY)", f"{metrics['beta']:.2f}")
with col7:
    st.metric("Win Rate", f"{metrics['win_rate']*100:.1f}%")
```

#### 4. 更新 config/settings.py

添加：
```python
# Risk settings
RISK_FREE_RATE = 0.05  # 无风险利率
SECTOR_ETFS = {
    "XLK": "Technology",
    "XLF": "Financials",
    "XLV": "Healthcare",
    "XLE": "Energy",
    "XLY": "Consumer Disc.",
    "XLP": "Consumer Staples",
    "XLI": "Industrials",
    "XLB": "Materials",
    "XLU": "Utilities",
    "XLRE": "Real Estate"
}
```

#### 5. 测试验证

创建 `tests/test_risk_metrics.py`：
```python
"""
测试风险指标模块
"""
import pandas as pd
import numpy as np
from features.risk_metrics import *

def test_calculate_returns():
    prices = pd.Series([100, 102, 101, 103, 105])
    returns = calculate_returns(prices)
    assert len(returns) == len(prices) - 1
    assert returns.iloc[0] == 0.02  # (102-100)/100

def test_max_drawdown():
    prices = pd.Series([100, 110, 90, 95, 85, 100])
    max_dd, start, end = calculate_max_drawdown(prices)
    assert abs(max_dd - (-0.227)) < 0.01  # 从110跌到85

def test_sharpe_ratio():
    returns = pd.Series([0.01, -0.005, 0.02, 0.015, -0.01] * 50)
    sharpe = calculate_sharpe_ratio(returns)
    assert isinstance(sharpe, float)
```

#### 6. 完成标准

- 所有风险指标函数独立可测试
- `pytest tests/test_risk_metrics.py` 通过
- Stock Detail 页面展示风险面板
- 数值计算正确（与 yfinance/手动计算对比验证）

---

### Phase 5 — Market Overview Dashboard

**目标：** 完善市场概览功能

#### 1. 创建模块文件

```
utils/market_regime.py     # 市场状态判断
config/settings.py         # 更新：添加板块 ETF 配置
```

#### 2. utils/market_regime.py 核心功能

```python
"""
市场状态判断模块
"""
import pandas as pd
from typing import Dict, Tuple
from utils.data_loader import DataLoader

def get_market_regime(spy_df: pd.DataFrame, vix_value: float) -> Dict:
    """
    判断市场状态
    
    Returns:
        {
            'regime': 'RISK-ON' | 'NEUTRAL' | 'RISK-OFF',
            'vix_level': float,
            'spy_above_ma50': bool,
            'spy_above_ma200': bool,
            'description': str
        }
    """
    pass

def get_sector_performance(period: str = "3m") -> pd.DataFrame:
    """
    获取板块表现
    
    Returns:
        DataFrame with columns: [Ticker, Name, Return, Rank]
    """
    pass

def get_market_breadth() -> Dict:
    """
    获取市场宽度指标（简化版）
    
    Returns:
        {
            'advancing': int,
            'declining': int,
            'adv_dec_ratio': float
        }
    """
    pass
```

#### 3. 更新 pages/1_Market_Overview.py

添加以下功能模块：

```python
# === 1. 市场状态面板 ===
st.subheader("🎯 Market Regime")

regime = get_market_regime(spy_df, vix_value)

if regime['regime'] == 'RISK-ON':
    st.success(f"🟢 {regime['regime']} - {regime['description']}")
elif regime['regime'] == 'RISK-OFF':
    st.error(f"🔴 {regime['regime']} - {regime['description']}")
else:
    st.warning(f"🟡 {regime['regime']} - {regime['description']}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("VIX", f"{regime['vix_level']:.1f}")
with col2:
    st.metric("SPY > MA50", "✅" if regime['spy_above_ma50'] else "❌")
with col3:
    st.metric("SPY > MA200", "✅" if regime['spy_above_ma200'] else "❌")

# === 2. VIX 风险面板 ===
st.subheader("📊 VIX Risk Panel")

vix_fig = create_vix_gauge(vix_value)  # 仪表盘样式
st.plotly_chart(vix_fig, use_container_width=True)

# VIX 历史分布
st.caption(f"VIX 52周范围: {vix_52w_low:.1f} - {vix_52w_high:.1f}")

# === 3. 板块表现 ===
st.subheader("🏭 Sector Performance")

sector_df = get_sector_performance("3m")

# 横向条形图
fig = px.bar(sector_df.sort_values('Return'), 
             x='Return', y='Name',
             orientation='h',
             color='Return',
             color_continuous_scale='RdYlGn')
st.plotly_chart(fig, use_container_width=True)
```

#### 4. 更新 ChartBuilder

添加 VIX 仪表盘图：

```python
@staticmethod
def create_vix_gauge(vix_value: float) -> go.Figure:
    """创建 VIX 仪表盘"""
    pass
```

#### 5. 完成标准

- Market Overview 页面展示市场状态判断
- VIX 风险面板正常显示
- 板块表现横向条形图正常
- 市场状态判断逻辑正确（可手动验证）

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
- [x] Phase 1-3 — 数据层 + 可视化 + 技术指标
- [ ] Phase 4-5 — 风险分析 + 市场概览
- [ ] Phase 6-7 — 股票详情 + Watchlist
- [ ] Phase 8-9 — 回测 + 预测

**下一步：** Codex 执行 Phase 4-5 开发。
