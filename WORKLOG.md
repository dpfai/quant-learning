# WORKLOG

## Active Branch Context: development

### Branch Goal

Build the project from a learning-focused market dashboard into a more practical
quant trading decision-support tool.

The platform should help users:

- Understand market regime and risk context before forming a trade idea.
- Analyze individual stocks with trend, momentum, volatility, relative strength,
  and risk metrics.
- Compare candidates across watchlists instead of forcing a single ticker.
- Backtest rule-based setups with realistic costs and no same-bar look-ahead.
- Use ML experiments as supporting evidence, not as guaranteed predictions.
- Use AI summaries to explain data, surface risks, and suggest follow-up research.
- Record trade hypotheses and review outcomes over time.

### Current Development Direction

Prioritize features that make the app closer to a quant trading workflow while
keeping human-in-the-loop decision making:

- Trading Journal for trade hypotheses, screenshots/metrics snapshots, and review.
- Signal scoring that combines trend, momentum, volatility, relative strength,
  risk, backtest evidence, and model evidence.
- Position sizing helpers based on account risk, stop distance, and volatility.
- Risk dashboard for portfolio/watchlist exposure, drawdowns, beta, and correlation.
- Trade setup workflow that converts data into structured bullish/bearish/neutral
  research cases.
- Model and strategy comparison tools across tickers, horizons, and market regimes.

### Important Boundaries

- Do not build real-money automatic trading.
- Do not connect to a broker or place orders unless the user explicitly starts a
  future broker-integration phase.
- Avoid presenting AI or ML output as guaranteed buy/sell instructions.
- Keep the app educational and practical: explain calculations, assumptions, and
  limitations clearly.
- Preserve simple, readable code patterns suitable for a learner and a data
  scientist inspecting the implementation.

### Stable Main Baseline

- `main` is the deployed/stable branch.
- `development` was created from `main` commit `5676f2b`
  (`Add learning center and Qianfan LLM defaults`).
- Development branch initialization commit: `3644226`
  (`Initialize development branch`).

### Immediate Next Step

Start the quant trading workflow phase on `development`. A strong first feature is
Trading Journal because it connects research, AI summaries, model evidence,
backtest results, risk notes, and later review into one repeatable process.

---

## Session: 2026-06-16 23:40 PDT

### Agent: Codex

**完成：**
- 从当前已部署的 `main` 最新提交 `5676f2b` 创建新的 `development` 分支。
- 将 `development` 推送到 GitHub。
- 设置本地 `development` 跟踪远端 `origin/development`。
- 确认后续更接近 quant trading 工具的新功能可以在 `development` 上继续开发。

**文件变更：**
- 更新 `WORKLOG.md`

**验证：**
- `git status --short` — 创建分支前工作区干净。
- `git branch --show-current` — 当前分支为 `development`。
- `git push -u origin development` — 成功，新建远端分支并设置 upstream。

**阻塞或注意事项：**
- 普通沙箱内 `git ls-remote` 因 DNS/network 限制失败；提升权限后 `git push` 成功。
- 普通沙箱内 `git switch -c development` 因 `.git` 写入权限失败；提升权限后创建成功。

**下一步：**
- 在 `development` 上规划并实现下一阶段更接近 quant trading 工具的功能，例如 Trading Journal、signal scoring、position sizing、risk dashboard 和 trade setup workflow。

## Session: 2026-06-16 22:35 PDT

### Agent: Codex

**完成：**
- 将 `app.py` 首页从简单欢迎页升级为交易决策支持导览页。
- 首页新增平台定位、推荐使用流程、页面用途表、交易决策 checklist、AI 使用边界说明。
- 新增 `pages/6_Learning_Center.py`，作为网页内学习中心。
- Learning Center 新增 7 个 tab：Trading Workflow、Code Map、AI Calls、Features、Models、Metrics、Experiments。
- 详细说明如何用平台辅助股票交易决策，同时保持不自动下单、不直接给买卖指令的边界。
- 详细说明代码结构、AI 调用方式、环境变量配置、feature 设计、模型选择、metric 解读、模型比较和实验方法。
- 更新 README，将项目描述从纯 learning dashboard 扩展为 AI-assisted stock research and trading decision-support platform。
- 更新 USER_GUIDE，加入 Home Page 和 Learning Center 的使用说明，并将页面数量更新为 6。

**文件变更：**
- 更新 `app.py`
- 新增 `pages/6_Learning_Center.py`
- 更新 `README.md`
- 更新 `USER_GUIDE.md`
- 更新 `WORKLOG.md`

**验证：**
- `venv/bin/python -m py_compile app.py pages/6_Learning_Center.py` — 通过。
- `venv/bin/python -m pytest tests/test_productization.py -q` — 6 passed。
- `git diff --check` — 通过。
- `venv/bin/streamlit run app.py --server.headless true --server.port 8501` — 8501 已被占用。
- `venv/bin/streamlit run app.py --server.headless true --server.port 8502` — 启动成功。
- `curl -I http://localhost:8502` — HTTP 200 OK。
- `venv/bin/python -m pytest -q` — 45 passed。
- `venv/bin/python -m py_compile app.py pages/1_Market_Overview.py pages/2_Stock_Detail.py pages/3_Watchlist.py pages/4_Backtest.py pages/5_Prediction.py pages/6_Learning_Center.py` — 通过。

**阻塞或注意事项：**
- In-app Browser 插件返回 `Browser is not available: iab`，因此本次未能做截图级视觉检查；已用 Streamlit 启动、HTTP 200、py_compile 和测试做替代验证。
- 本次内容仍明确定位为交易决策支持，不连接 broker、不自动执行真钱交易。

**下一步：**
- 从浏览器手动打开 `http://localhost:8502` 或当前 Streamlit 端口，检查 Home 和 Learning Center 的实际阅读体验；后续可增加 Trading Journal 页面记录交易假设和复盘。

## Session: 2026-06-16 22:21 PDT

### Agent: Codex

**完成：**
- 按用户请求尝试验证百度千帆 LLM 环境变量是否可被当前 Codex 执行环境读取。
- 检查 `BAIDU_API_KEY`、`QIANFAN_API_KEY`、`LLM_API_KEY`、`OPENAI_API_KEY` 是否存在，仅输出布尔值，未打印任何 secret。
- 检查项目根目录 `.env`、`~/.zshrc`、`~/.zprofile` 中是否有相关变量名。
- 尝试通过 `LLMClient` 发起最小调用，确认当前失败点是 API key 未进入本执行环境。

**文件变更：**
- 更新 `WORKLOG.md`

**验证：**
- `venv/bin/python -c "... bool(os.getenv(...)) ..."` — 四个 key 变量均为 False。
- `zsh -ic 'venv/bin/python -c "... bool(os.getenv(...)) ..."'` — 四个 key 变量均为 False。
- `test -f .env` — `ENV_FILE_ABSENT`。
- `~/.zshrc` 检查 — 未发现 `BAIDU_API_KEY`、`QIANFAN_API_KEY`、`LLM_API_KEY` 变量名。
- `~/.zprofile` 检查 — 文件不存在。
- `venv/bin/python -c "from agents.llm_client import LLMClient; ..."` — 失败，报错为 `LLM API key is not configured...`。

**阻塞或注意事项：**
- 当前 Codex shell 看不到用户设置的 API key，因此尚未发送真实百度千帆 API 请求。
- 如果 key 是在 IDE 的另一个终端临时 `export` 的，它不会自动传递到 Codex 的执行环境。

**下一步：**
- 将 key 设置到 Codex 可读取的环境中，或创建本地 `.env` 并添加 dotenv 加载支持后，再做真实端到端调用测试。

## Session: 2026-06-16 22:16 PDT

### Agent: Codex

**完成：**
- 将 AI Summary 默认 LLM provider 从 OpenAI 改为百度千帆 Coding OpenAI-compatible endpoint。
- 默认模型改为 `glm-5`，并在配置中记录 `deepseek-v3.2`、`kimi-k2.5` 作为备选模型。
- 将 LLM client 从 OpenAI Responses-only 改为支持 `chat_completions` 和 `responses` 两种 API 格式。
- 支持通过环境变量覆盖 provider/model/base_url/api format/API key：`LLM_PROVIDER`、`LLM_MODEL`、`LLM_BASE_URL`、`LLM_API_FORMAT`、`LLM_API_KEY`、`BAIDU_API_KEY`、`QIANFAN_API_KEY`、`OPENAI_API_KEY`。
- 更新 README 和 USER_GUIDE，说明 API key 应放在环境变量或本地 `.env` 中，不应提交到 GitHub。
- 更新 `.gitignore` 忽略 `.env` 和 `.env.*`。
- 确认用户提供的真实 API key 未写入仓库文件。

**文件变更：**
- 更新 `.gitignore`
- 更新 `config/config.yaml`
- 更新 `agents/llm_client.py`
- 更新 `tests/test_productization.py`
- 更新 `README.md`
- 更新 `USER_GUIDE.md`
- 更新 `WORKLOG.md`

**验证：**
- `venv/bin/python -m pytest tests/test_productization.py -q` — 6 passed。
- `venv/bin/python -m pytest -q` — 45 passed。
- `venv/bin/python -m py_compile app.py config/loader.py agents/llm_client.py agents/market_summarizer.py pages/1_Market_Overview.py pages/2_Stock_Detail.py` — 通过。
- `git diff --check` — 通过。
- `rg -n "bce-v3|ALTAKSP|dc4e31ffa061af2d1a8c66ab63319b05cab679d9" .` — 无命中。

**阻塞或注意事项：**
- 未发送真实百度千帆 API 请求；本次验证使用 mock client 和本地测试。
- 用户已在聊天中贴出真实 API key，建议在百度控制台轮换该 key。

**下一步：**
- 在本地设置 `BAIDU_API_KEY` 后，从 Streamlit 页面点击 AI Summary 做一次真实端到端验证。

## Session: 2026-06-14 00:53 PDT

### Agent: Codex

**完成：**
- 完成 Phase 6：实现多时间框架相对收益、Alpha、tracking error、information ratio，并集成 Stock Detail。
- 完成 Phase 7：实现 JSON watchlist 管理、添加/删除 ticker、watchlist 创建/删除、排名表、风险收益散点图和 CSV 下载。
- 完成 Phase 8：实现 MA crossover、RSI mean reversion、Bollinger Band 策略和避免 same-bar look-ahead 的成本感知回测引擎。
- 完成 Phase 9：实现 trailing feature engineering、forward target、时间顺序 train/test split、三种分类模型、walk-forward validation、feature importance 和实验日志。
- 完成 Phase 10：实现可选 OpenAI Responses API 客户端、市场/个股 prompt、摘要生成器和页面 AI Summary；无 API key 时不影响其他功能。
- 完成 Phase 11：实现 YAML 配置、幂等 logger、用户友好错误处理、依赖声明、README 和 USER_GUIDE。
- 完成 Phase 12：选择并实现 CSV data export，可导出市场快照、个股指标、watchlist metrics 和 backtest trades。
- 更新 `.gitignore`，忽略本地 watchlist 和 experiment 数据。

**文件变更：**
- 新增 `utils/relative_performance.py`、`utils/watchlist_manager.py`、`utils/logger.py`、`utils/export.py`
- 新增 `backtest/`、`ml/`、`agents/`
- 新增 `config/config.yaml`、`config/loader.py`
- 新增 `pages/3_Watchlist.py`、`pages/4_Backtest.py`、`pages/5_Prediction.py`
- 更新 `pages/1_Market_Overview.py`、`pages/2_Stock_Detail.py`
- 新增 5 个测试文件
- 更新 `requirements.txt`、`.gitignore`、`README.md`
- 新增 `USER_GUIDE.md`
- 更新 `WORKLOG.md`

**验证：**
- Phase 6-8 focused tests — 11 passed。
- Phase 9 focused tests — 4 passed。
- `venv/bin/python -m pytest -q` — 44 passed。
- coverage test — 44 passed，TOTAL 81%。
- 所有新增/更新 Python 文件 `py_compile` — 通过。
- `venv/bin/streamlit run app.py --server.headless true --server.port 8501` — 启动成功。
- `curl -I http://localhost:8501` — HTTP 200 OK。
- `git diff --check` — 通过。
- Commit `c81d468` — `Complete phases 6-12 research features`。
- `git push origin main` — 成功。

**阻塞或注意事项：**
- 无功能阻塞。
- AI Summary 需要用户设置 `OPENAI_API_KEY`；本次使用 mock client 测试 Responses API 集成，未发送真实 API 请求。
- ML 输出和回测结果仅用于学习研究，不是预测保证或投资建议。

**下一步：**
- Phase 6-12 已完成并推送；后续优先增加页面级 Streamlit 测试和更严格的模型校准/回测方法。

## Session: 2026-06-14 02:00 PDT

### Agent: Claude

**完成：**
- 编写 Phase 6-12 完整任务计划
- 更新 STUDY_GUIDE.md 添加详细的 Agent 架构文档
- 提交并推送 Phase 4-5 变更

**下一步：**
- Codex 按顺序执行 Phase 6-12

---

# 📦 Phase 6-12 Complete Task Plan (Codex)

以下是 Phase 6-12 的完整任务计划，按顺序执行。

---

## Phase 6 — Stock Detail Enhancement

**目标：** 完善个股分析页面，添加相对表现分析

### 任务

#### 1. 创建 `utils/relative_performance.py`

```python
"""
相对表现计算模块
"""
import pandas as pd
from typing import Dict, Optional


def calculate_relative_performance(
    stock_prices: pd.Series,
    benchmark_prices: pd.Series,
    periods: list[int] = [5, 20, 60, 252]
) -> Dict[str, float]:
    """
    计算股票相对于基准的表现
    
    Returns:
        {
            'stock_5d': float,      # 股票5日收益率
            'benchmark_5d': float,  # 基准5日收益率
            'alpha_5d': float,      # 超额收益
            'stock_20d': float,
            'benchmark_20d': float,
            'alpha_20d': float,
            ...
            'stock_ytd': float,
            'benchmark_ytd': float,
            'alpha_ytd': float,
        }
    """
    pass


def calculate_rolling_alpha(
    stock_returns: pd.Series,
    benchmark_returns: pd.Series,
    window: int = 20
) -> pd.Series:
    """计算滚动 Alpha"""
    pass


def calculate_information_ratio(
    stock_returns: pd.Series,
    benchmark_returns: pd.Series
) -> float:
    """计算信息比率"""
    pass


def calculate_tracking_error(
    stock_returns: pd.Series,
    benchmark_returns: pd.Series
) -> float:
    """计算跟踪误差"""
    pass
```

#### 2. 更新 `pages/2_Stock_Detail.py`

添加功能：
- 多时间框架收益表格（5d, 20d, 60d, YTD）
- 相对表现 vs SPY（超额收益）
- Alpha 信息比率
- 与板块 ETF 对比（可选）

```python
# 相对表现面板
st.subheader("📊 Relative Performance vs SPY")

from utils.relative_performance import calculate_relative_performance

rel_perf = calculate_relative_performance(df["Adj Close"], spy_data["Adj Close"])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("5d Return", f"{rel_perf['stock_5d']*100:.1f}%", f"α: {rel_perf['alpha_5d']*100:.1f}%")
with col2:
    st.metric("20d Return", f"{rel_perf['stock_20d']*100:.1f}%", f"α: {rel_perf['alpha_20d']*100:.1f}%")
# ... 继续
```

#### 3. 创建 `tests/test_relative_performance.py`

#### 完成标准

- [x] `utils/relative_performance.py` 创建
- [x] `pages/2_Stock_Detail.py` 添加相对表现面板
- [x] 测试通过

---

## Phase 7 — Watchlist System

**目标：** 实现多股票追踪和排名系统

### 任务

#### 1. 创建 `utils/watchlist_manager.py`

```python
"""
Watchlist 管理模块
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd


class WatchlistManager:
    """管理用户 watchlist"""
    
    DEFAULT_WATCHLIST = {
        "Tech Growth": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META"],
        "ETFs": ["SPY", "QQQ", "DIA", "IWM"],
        "Sectors": ["XLK", "XLF", "XLV", "XLE", "XLY"]
    }
    
    def __init__(self, storage_path: str = "data/watchlists.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get_watchlist(self, name: str) -> List[str]:
        """获取指定 watchlist"""
        pass
    
    def add_ticker(self, watchlist_name: str, ticker: str) -> None:
        """添加股票到 watchlist"""
        pass
    
    def remove_ticker(self, watchlist_name: str, ticker: str) -> None:
        """从 watchlist 移除股票"""
        pass
    
    def create_watchlist(self, name: str, tickers: List[str] = None) -> None:
        """创建新 watchlist"""
        pass
    
    def delete_watchlist(self, name: str) -> None:
        """删除 watchlist"""
        pass
    
    def list_watchlists(self) -> List[str]:
        """列出所有 watchlist"""
        pass
```

#### 2. 创建 `pages/3_Watchlist.py`

```python
"""
Watchlist 页面
"""
import streamlit as st
import pandas as pd
from utils.watchlist_manager import WatchlistManager
from utils.data_loader import DataLoader
from features.risk_metrics import calculate_all_risk_metrics
from utils.relative_performance import calculate_relative_performance

st.title("📋 Watchlist")

manager = WatchlistManager()
loader = DataLoader()

# 侧边栏：选择 watchlist
watchlists = manager.list_watchlists()
selected_watchlist = st.selectbox("Select Watchlist", watchlists)

# 显示和编辑 watchlist
tickers = manager.get_watchlist(selected_watchlist)
new_ticker = st.text_input("Add Ticker", key="new_ticker")
if st.button("Add") and new_ticker:
    manager.add_ticker(selected_watchlist, new_ticker.upper())
    st.rerun()

# 批量获取数据并计算指标
@st.cache_data
def get_watchlist_metrics(tickers: list) -> pd.DataFrame:
    results = []
    spy_data = loader.download("SPY")
    
    for ticker in tickers:
        try:
            df = loader.download(ticker)
            metrics = calculate_all_risk_metrics(df["Adj Close"], spy_data["Adj Close"])
            rel_perf = calculate_relative_performance(df["Adj Close"], spy_data["Adj Close"])
            
            results.append({
                "Ticker": ticker,
                "Price": df["Close"].iloc[-1],
                "5d": rel_perf["stock_5d"],
                "20d": rel_perf["stock_20d"],
                "60d": rel_perf["stock_60d"],
                "YTD": rel_perf["stock_ytd"],
                "Volatility": metrics["ann_volatility"],
                "Max DD": metrics["max_drawdown"],
                "Sharpe": metrics["sharpe_ratio"],
                "Alpha 20d": rel_perf["alpha_20d"],
            })
        except Exception as e:
            st.warning(f"Failed to load {ticker}: {e}")
    
    return pd.DataFrame(results)

df = get_watchlist_metrics(tickers)

# 排序和显示
sort_col = st.selectbox("Sort by", df.columns[1:], index=3)
df_sorted = df.sort_values(sort_col, ascending=False)
st.dataframe(df_sorted.style.format({
    "Price": "${:.2f}",
    "5d": "{:.1%}",
    "20d": "{:.1%}",
    "60d": "{:.1%}",
    "YTD": "{:.1%}",
    "Volatility": "{:.1%}",
    "Max DD": "{:.1%}",
    "Sharpe": "{:.2f}",
    "Alpha 20d": "{:.1%}",
}), use_container_width=True)

# 风险收益散点图
st.subheader("Risk-Return Scatter")
import plotly.express as px
fig = px.scatter(df, x="Volatility", y="YTD", text="Ticker",
                 hover_data=["Sharpe", "Max DD"])
fig.update_traces(textposition="top center")
st.plotly_chart(fig, use_container_width=True)
```

#### 3. 创建 `tests/test_watchlist_manager.py`

#### 完成标准

- [x] `utils/watchlist_manager.py` 创建
- [x] `pages/3_Watchlist.py` 创建
- [x] 支持添加/删除股票
- [x] 显示多时间框架收益
- [x] 风险收益散点图
- [x] 测试通过

---

## Phase 8 — Backtesting

**目标：** 实现简单回测框架

### 任务

#### 1. 创建目录结构

```
backtest/
├── __init__.py
├── engine.py           # 回测引擎
├── strategies.py       # 策略定义
├── metrics.py          # 绩效指标
└── signals.py          # 信号生成
```

#### 2. `backtest/strategies.py`

```python
"""
交易策略定义
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional


def ma_crossover_signal(
    df: pd.DataFrame,
    fast_period: int = 20,
    slow_period: int = 50
) -> pd.Series:
    """
    MA 交叉策略信号
    
    Returns:
        Series with values: 1 (long), 0 (flat), -1 (short)
    """
    fast_ma = df["Close"].rolling(fast_period).mean()
    slow_ma = df["Close"].rolling(slow_period).mean()
    
    signal = pd.Series(0, index=df.index)
    signal[fast_ma > slow_ma] = 1
    signal[fast_ma < slow_ma] = -1
    
    return signal


def rsi_mean_reversion_signal(
    df: pd.DataFrame,
    rsi_period: int = 14,
    oversold: float = 30,
    overbought: float = 70
) -> pd.Series:
    """
    RSI 均值回归策略信号
    
    当 RSI < oversold 时买入
    当 RSI > overbought 时卖出
    """
    # 计算 RSI (复用 features/indicators.py)
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    avg_gain = gain.ewm(alpha=1/rsi_period, min_periods=rsi_period).mean()
    avg_loss = loss.ewm(alpha=1/rsi_period, min_periods=rsi_period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    signal = pd.Series(0, index=df.index)
    signal[rsi < oversold] = 1
    signal[rsi > overbought] = -1
    
    return signal


def bollinger_band_signal(
    df: pd.DataFrame,
    period: int = 20,
    std_dev: float = 2
) -> pd.Series:
    """
    布林带策略信号
    """
    ma = df["Close"].rolling(period).mean()
    std = df["Close"].rolling(period).std()
    upper = ma + std_dev * std
    lower = ma - std_dev * std
    
    signal = pd.Series(0, index=df.index)
    signal[df["Close"] < lower] = 1   # 价格触及下轨，买入
    signal[df["Close"] > upper] = -1  # 价格触及上轨，卖出
    
    return signal
```

#### 3. `backtest/engine.py`

```python
"""
回测引擎
"""
import pandas as pd
import numpy as np
from typing import Callable, Dict, Optional
from backtest.strategies import ma_crossover_signal, rsi_mean_reversion_signal


class BacktestEngine:
    """简单回测引擎"""
    
    def __init__(
        self,
        commission: float = 0.001,  # 0.1% 交易成本
        slippage: float = 0.0005,   # 0.05% 滑点
    ):
        self.commission = commission
        self.slippage = slippage
    
    def run(
        self,
        prices: pd.Series,
        signals: pd.Series,
        initial_capital: float = 100000,
    ) -> Dict:
        """
        运行回测
        
        Args:
            prices: 收盘价序列
            signals: 交易信号 (1=long, 0=flat, -1=short)
            initial_capital: 初始资金
            
        Returns:
            {
                'equity_curve': pd.Series,
                'trades': pd.DataFrame,
                'metrics': Dict,
            }
        """
        # 实现回测逻辑
        # 注意避免 look-ahead bias
        pass
    
    def calculate_metrics(self, equity_curve: pd.Series) -> Dict:
        """计算回测绩效指标"""
        returns = equity_curve.pct_change().dropna()
        
        return {
            'total_return': (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1,
            'annualized_return': returns.mean() * 252,
            'annualized_volatility': returns.std() * np.sqrt(252),
            'sharpe_ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)),
            'max_drawdown': self._max_drawdown(equity_curve),
            'win_rate': self._win_rate(returns),
            'profit_factor': self._profit_factor(returns),
            'num_trades': self._count_trades(signals),
        }
```

#### 4. `pages/4_Backtest.py`

```python
"""
回测页面
"""
import streamlit as st
from utils.data_loader import DataLoader
from backtest.engine import BacktestEngine
from backtest.strategies import ma_crossover_signal, rsi_mean_reversion_signal, bollinger_band_signal

st.title("📈 Backtesting")

# 输入
ticker = st.text_input("Ticker", "SPY")
strategy = st.selectbox("Strategy", ["MA Crossover", "RSI Mean Reversion", "Bollinger Band"])
fast_period = st.slider("Fast Period", 5, 50, 20)
slow_period = st.slider("Slow Period", 20, 200, 50)

# 运行回测
loader = DataLoader()
df = loader.download(ticker)

engine = BacktestEngine(commission=0.001)

if strategy == "MA Crossover":
    signals = ma_crossover_signal(df, fast_period, slow_period)
elif strategy == "RSI Mean Reversion":
    signals = rsi_mean_reversion_signal(df)
else:
    signals = bollinger_band_signal(df)

result = engine.run(df["Close"], signals)

# 显示结果
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Return", f"{result['metrics']['total_return']*100:.1f}%")
with col2:
    st.metric("Sharpe Ratio", f"{result['metrics']['sharpe_ratio']:.2f}")
with col3:
    st.metric("Max Drawdown", f"{result['metrics']['max_drawdown']*100:.1f}%")
with col4:
    st.metric("Win Rate", f"{result['metrics']['win_rate']*100:.1f}%")

# Equity curve
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=result['equity_curve'].index, y=result['equity_curve'], name="Equity"))
st.plotly_chart(fig, use_container_width=True)
```

#### 完成标准

- [x] `backtest/` 目录创建
- [x] 3个策略实现
- [x] 回测引擎实现（考虑交易成本、避免 look-ahead bias）
- [x] `pages/4_Backtest.py` 创建
- [x] 测试通过

---

## Phase 9 — Prediction System

**目标：** 实现基础 ML 预测功能

### 任务

#### 1. 创建目录结构

```
ml/
├── __init__.py
├── features.py         # 特征工程
├── models.py           # 模型定义
├── validation.py       # 验证方法
└── experiments.py      # 实验管理
```

#### 2. `ml/features.py`

```python
"""
特征工程模块
参考 reference-repos/qlib/qlib/contrib/data/handler.py (Alpha158)
"""
import pandas as pd
import numpy as np
from typing import List, Tuple


def create_price_features(df: pd.DataFrame, windows: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
    """创建价格相关特征"""
    features = pd.DataFrame(index=df.index)
    
    for w in windows:
        # 收益率
        features[f'return_{w}d'] = df['Close'].pct_change(w)
        
        # 波动率
        features[f'volatility_{w}d'] = df['Close'].pct_change().rolling(w).std()
        
        # MA distance
        features[f'ma_dist_{w}d'] = (df['Close'] - df['Close'].rolling(w).mean()) / df['Close'].rolling(w).mean()
        
        # High/Low ratio
        features[f'high_low_ratio_{w}d'] = df['High'].rolling(w).max() / df['Low'].rolling(w).min()
        
        # Volume change
        features[f'volume_change_{w}d'] = df['Volume'].pct_change(w)
    
    return features


def create_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    """创建技术指标特征"""
    features = pd.DataFrame(index=df.index)
    
    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/14, min_periods=14).mean()
    avg_loss = loss.ewm(alpha=1/14, min_periods=14).mean()
    features['rsi_14'] = 100 - (100 / (1 + avg_gain / avg_loss))
    
    # MACD
    ema_12 = df['Close'].ewm(span=12).mean()
    ema_26 = df['Close'].ewm(span=26).mean()
    features['macd'] = ema_12 - ema_26
    features['macd_signal'] = features['macd'].ewm(span=9).mean()
    features['macd_hist'] = features['macd'] - features['macd_signal']
    
    # Bollinger Band position
    ma_20 = df['Close'].rolling(20).mean()
    std_20 = df['Close'].rolling(20).std()
    features['bb_position'] = (df['Close'] - ma_20) / (2 * std_20)
    
    # ATR ratio
    high_low = df['High'] - df['Low']
    atr = high_low.ewm(alpha=1/14).mean()
    features['atr_ratio'] = atr / df['Close']
    
    return features


def create_target(
    df: pd.DataFrame,
    forward_days: int = 5,
    target_type: str = 'return'
) -> pd.Series:
    """
    创建目标变量
    
    target_type:
        'return': 未来N日收益率
        'binary': 涨/跌 (1/0)
        'bucket': 分位数 (0=bottom 20%, 4=top 20%)
    """
    future_return = df['Close'].shift(-forward_days) / df['Close'] - 1
    
    if target_type == 'return':
        return future_return
    elif target_type == 'binary':
        return (future_return > 0).astype(int)
    elif target_type == 'bucket':
        return pd.qcut(future_return, 5, labels=False, duplicates='drop')
    
    return future_return


def prepare_ml_data(
    df: pd.DataFrame,
    forward_days: int = 5,
    test_ratio: float = 0.2
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    准备 ML 数据（防止数据泄露）
    
    时间序列划分：训练集在前，测试集在后
    """
    # 创建特征
    price_features = create_price_features(df)
    tech_features = create_technical_features(df)
    X = pd.concat([price_features, tech_features], axis=1)
    
    # 创建目标
    y = create_target(df, forward_days)
    
    # 移除 NaN
    valid_idx = ~(X.isna().any(axis=1) | y.isna())
    X = X[valid_idx]
    y = y[valid_idx]
    
    # 时间序列划分（不能用 random split）
    split_idx = int(len(X) * (1 - test_ratio))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    return X_train, X_test, y_train, y_test
```

#### 3. `ml/models.py`

```python
"""
模型定义
"""
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np


def get_model(model_type: str = 'random_forest'):
    """获取模型"""
    if model_type == 'logistic':
        return Pipeline([
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(max_iter=1000))
        ])
    elif model_type == 'random_forest':
        return RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    elif model_type == 'gradient_boost':
        return GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
    
    raise ValueError(f"Unknown model type: {model_type}")


def evaluate_model(model, X_test, y_test) -> dict:
    """评估模型"""
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    return {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1': f1_score(y_test, y_pred, zero_division=0),
    }


def get_feature_importance(model, feature_names: list) -> pd.DataFrame:
    """获取特征重要性"""
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
    elif hasattr(model, 'named_steps') and 'model' in model.named_steps:
        importance = model.named_steps['model'].coef_[0]
    else:
        return None
    
    return pd.DataFrame({
        'feature': feature_names,
        'importance': np.abs(importance)
    }).sort_values('importance', ascending=False)
```

#### 4. `pages/5_Prediction.py`

```python
"""
预测页面
"""
import streamlit as st
from utils.data_loader import DataLoader
from ml.features import prepare_ml_data
from ml.models import get_model, evaluate_model, get_feature_importance

st.title("🔮 Prediction")

# 输入
ticker = st.text_input("Ticker", "SPY")
forward_days = st.slider("Prediction Horizon (days)", 1, 20, 5)
model_type = st.selectbox("Model", ["random_forest", "logistic", "gradient_boost"])

# 加载数据
loader = DataLoader()
df = loader.download(ticker, period="5y")

# 准备 ML 数据
X_train, X_test, y_train, y_test = prepare_ml_data(df, forward_days)

st.write(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

# 训练模型
model = get_model(model_type)
model.fit(X_train, y_train)

# 评估
metrics = evaluate_model(model, X_test, y_test)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Accuracy", f"{metrics['accuracy']:.1%}")
with col2:
    st.metric("Precision", f"{metrics['precision']:.1%}")
with col3:
    st.metric("Recall", f"{metrics['recall']:.1%}")
with col4:
    st.metric("F1 Score", f"{metrics['f1']:.1%}")

# 特征重要性
st.subheader("Feature Importance")
importance_df = get_feature_importance(model, X_train.columns.tolist())
if importance_df is not None:
    st.bar_chart(importance_df.set_index('feature')['importance'])

# 最新预测
st.subheader("Latest Prediction")
latest_features = X_test.iloc[[-1]]
prediction = model.predict(latest_features)[0]
probability = model.predict_proba(latest_features)[0]

if prediction == 1:
    st.success(f"📈 Predicted UP (probability: {probability[1]:.1%})")
else:
    st.error(f"📉 Predicted DOWN (probability: {probability[0]:.1%})")
```

#### 完成标准

- [x] `ml/` 目录创建
- [x] 特征工程实现（防止数据泄露）
- [x] 模型训练和评估
- [x] `pages/5_Prediction.py` 创建
- [x] 测试通过

---

## Phase 10 — AI Summary System

**目标：** 使用 LLM 生成市场分析摘要

### 任务

#### 1. 创建 `agents/` 目录

```
agents/
├── __init__.py
├── llm_client.py       # LLM 客户端
├── market_summarizer.py # 市场摘要生成
└── prompts.py          # Prompt 模板
```

#### 2. `agents/llm_client.py`

```python
"""
LLM 客户端
参考 reference-repos/TradingAgents/tradingagents/llm_clients/
"""
import os
from typing import Optional
import openai


class LLMClient:
    """统一 LLM 客户端"""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4o-mini"):
        self.provider = provider
        self.model = model
        
        if provider == "openai":
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # 可扩展其他 provider
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """生成回复"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content
        
        raise NotImplementedError(f"Provider {self.provider} not implemented")
```

#### 3. `agents/prompts.py`

```python
"""
Prompt 模板
"""

MARKET_SUMMARY_SYSTEM = """You are a professional market analyst. 
Provide concise, objective market analysis without giving investment advice.
Focus on facts, data, and logical reasoning.
Always include appropriate disclaimers."""

MARKET_SUMMARY_PROMPT = """Based on the following market data, provide a brief analysis:

**Market State:** {regime}
**VIX Level:** {vix:.1f}
**SPY Position:** {spy_price:.2f} ({spy_change:+.1%} from MA50)

**Sector Performance (3-month):**
{sector_performance}

**Key Observations:**
- Market regime is {regime}
- VIX indicates {volatility_level}
- Top performing sector: {top_sector}
- Weakest sector: {weak_sector}

Please provide:
1. A 2-3 sentence market overview
2. Key risk factors to watch
3. Potential opportunities (without specific stock recommendations)

Remember: This is for educational purposes only. Not financial advice."""

STOCK_ANALYSIS_PROMPT = """Analyze the following stock metrics:

**Ticker:** {ticker}
**Current Price:** ${price:.2f}

**Performance:**
- 5-day: {return_5d:+.1%}
- 20-day: {return_20d:+.1%}
- YTD: {return_ytd:+.1%}

**Risk Metrics:**
- Annualized Volatility: {volatility:.1%}
- Max Drawdown: {max_dd:.1%}
- Sharpe Ratio: {sharpe:.2f}
- Beta (vs SPY): {beta:.2f}

**Technical Indicators:**
- RSI (14): {rsi:.1f}
- MACD: {macd:.2f}
- Above MA50: {above_ma50}
- Above MA200: {above_ma200}

Provide a brief, objective analysis in 3-4 sentences. 
Include the key strength and key risk.
Do NOT give buy/sell recommendations."""
```

#### 4. `agents/market_summarizer.py`

```python
"""
市场摘要生成
"""
from typing import Dict
from agents.llm_client import LLMClient
from agents.prompts import MARKET_SUMMARY_SYSTEM, MARKET_SUMMARY_PROMPT


class MarketSummarizer:
    """生成市场分析摘要"""
    
    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()
    
    def summarize_market(self, market_data: Dict) -> str:
        """生成市场摘要"""
        prompt = MARKET_SUMMARY_PROMPT.format(**market_data)
        return self.llm.generate(prompt, MARKET_SUMMARY_SYSTEM)
    
    def analyze_stock(self, stock_data: Dict) -> str:
        """生成个股分析"""
        from agents.prompts import STOCK_ANALYSIS_PROMPT
        prompt = STOCK_ANALYSIS_PROMPT.format(**stock_data)
        return self.llm.generate(prompt, MARKET_SUMMARY_SYSTEM)
```

#### 5. 更新 `pages/1_Market_Overview.py` 和 `pages/2_Stock_Detail.py`

添加 AI Summary 部分：

```python
# AI Summary
st.subheader("🤖 AI Analysis")

if st.button("Generate AI Summary"):
    with st.spinner("Analyzing..."):
        from agents.market_summarizer import MarketSummarizer
        
        summarizer = MarketSummarizer()
        summary = summarizer.summarize_market({
            'regime': regime['regime'],
            'vix': regime['vix_level'],
            'spy_price': spy_df['Close'].iloc[-1],
            'spy_change': (spy_df['Close'].iloc[-1] / spy_df['Close'].rolling(50).mean().iloc[-1]) - 1,
            'sector_performance': sector_df.to_string(),
            'top_sector': sector_df.iloc[0]['Name'],
            'weak_sector': sector_df.iloc[-1]['Name'],
            'volatility_level': 'high volatility' if regime['vix_level'] > 25 else 'normal volatility',
        })
        
        st.markdown(summary)
        st.caption("⚠️ This is AI-generated analysis for educational purposes only. Not financial advice.")
```

#### 完成标准

- [x] `agents/` 目录创建
- [x] LLM 客户端实现
- [x] Prompt 模板定义
- [x] 市场摘要生成器
- [x] 页面集成 AI Summary
- [x] 添加适当的免责声明

---

## Phase 11 — Productization

**目标：** 改进代码质量和用户体验

### 任务

#### 1. 添加日志系统

创建 `utils/logger.py`:

```python
import logging
import sys

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)
    
    return logger
```

#### 2. 添加错误处理

- 在数据加载处添加 try-except
- 显示用户友好的错误消息
- 添加 loading spinner

#### 3. 改进配置

创建 `config/config.yaml`:

```yaml
data:
  cache_dir: "data/cache"
  cache_max_age_hours: 24
  default_period: "2y"

risk:
  risk_free_rate: 0.05

llm:
  provider: "openai"
  model: "gpt-4o-mini"

ui:
  theme: "light"
  default_tickers:
    - SPY
    - QQQ
    - DIA
```

#### 4. 添加文档

- 更新 README.md
- 添加 API 文档注释
- 创建用户指南

#### 5. 添加更多测试

- 集成测试
- UI 测试 (可选)

#### 完成标准

- [x] 日志系统实现
- [x] 错误处理完善
- [x] 配置文件支持
- [x] 文档更新
- [x] 测试覆盖率 > 80%

---

## Phase 12 — Future Features (Optional)

**目标：** 高级功能和扩展

### 可选功能

#### 1. Paper Trading

- 模拟交易账户
- 买卖操作记录
- 组合跟踪

#### 2. Alert System

- 价格预警
- 技术指标预警
- Email/Discord 通知

#### 3. Multi-Agent System

参考 `reference-repos/TradingAgents/` 实现：

```
agents/
├── analysts/
│   ├── fundamentals_analyst.py
│   ├── sentiment_analyst.py
│   ├── technical_analyst.py
├── researchers/
│   ├── bull_researcher.py
│   ├── bear_researcher.py
├── trader.py
├── risk_manager.py
└── portfolio_manager.py
```

#### 4. Data Export

- 导出分析报告 (PDF)
- 导出数据 (CSV/Excel)

#### 完成标准

- [x] 至少实现 1 个可选功能
- [x] 测试通过
- [x] 文档更新

---

## 执行顺序

```
Phase 6  → Stock Detail Enhancement
Phase 7  → Watchlist System
Phase 8  → Backtesting
Phase 9  → Prediction System
Phase 10 → AI Summary System
Phase 11 → Productization
Phase 12 → Future Features (Optional)
```

每完成一个 Phase：
1. 运行 `pytest` 确保测试通过
2. 运行 `streamlit run app.py` 验证功能
3. 更新 WORKLOG.md 记录完成状态
4. 提交代码（如果无法推送，告知 Claude）

---

## Session: 2026-06-14 00:36 PDT

### Agent: Codex

**完成：**
- 完成 Phase 4 — 风险分析模块。
- 实现日收益率、年化收益、年化波动率、最大回撤、Sharpe、Sortino、Beta、相关矩阵和汇总风险指标。
- 在 Stock Detail 页面添加 SPY 基准风险面板和最大回撤区间。
- 完成 Phase 5 — 市场概览增强。
- 实现基于 VIX、SPY MA50 和 MA200 的透明市场状态判断。
- 实现 10 个 sector ETF 的三个月收益排名。
- 添加 VIX Plotly gauge、52 周区间、市场状态面板和板块表现图表。
- 添加风险指标和市场状态单元测试。

**文件变更：**
- 更新 `config/settings.py`
- 新增 `features/risk_metrics.py`
- 新增 `utils/market_regime.py`
- 更新 `utils/chart_builder.py`
- 更新 `pages/1_Market_Overview.py`
- 更新 `pages/2_Stock_Detail.py`
- 新增 `tests/test_risk_metrics.py`
- 新增 `tests/test_market_regime.py`
- 更新 `WORKLOG.md`

**验证：**
- `venv/bin/python -m py_compile app.py config/settings.py features/risk_metrics.py utils/market_regime.py utils/chart_builder.py pages/1_Market_Overview.py pages/2_Stock_Detail.py` — 通过。
- `venv/bin/python -m pytest tests/test_risk_metrics.py tests/test_market_regime.py -q` — 11 passed。
- `venv/bin/python -m pytest -q` — 24 passed。
- `venv/bin/streamlit run app.py --server.headless true --server.port 8501` — 启动成功。
- `curl -I http://localhost:8501` — HTTP 200 OK。
- `git diff --check` — 通过。

**阻塞或注意事项：**
- in-app browser 在本次 session 不可用，因此未完成浏览器截图级 UI 检查。
- `reference-repos/STUDY_GUIDE.md` 存在非本次工作产生的未提交修改，已保留且未改动。
- Sector performance 依赖 Yahoo Finance 在线数据；单个 ticker 无数据时会跳过。

**下一步：**
- 审阅并提交 Phase 4-5 变更，然后按 roadmap 继续 Phase 6-7。

## Session: 2026-06-14 01:30 PDT

### Agent: Claude

**完成：**
- 验证 Codex 完成的 Phase 1.5 工作
- 提交并推送 Phase 1.5 变更（Codex 因 GitHub 认证问题无法推送）
- 编写 Phase 4-5 任务计划

**文件变更：**
- 提交 Phase 1.5 所有变更
- 更新 `WORKLOG.md` 添加 Phase 4-5 任务

**下一步：**
- Codex 执行 Phase 4-5 — 风险分析和市场概览

---

## 🔐 Git 认证说明 (Codex 注意)

### 问题
Codex 使用 `gh auth` 认证失败，导致无法 push。

### 解决方案

**方法 1：使用 SSH (推荐)**

```bash
# 检查当前 remote
git remote -v

# 如果是 HTTPS，切换到 SSH
git remote set-url origin git@github.com:dpfai/quant-learning.git

# 确保 SSH key 已添加到 GitHub
ssh -T git@github.com
```

**方法 2：重新认证 GitHub CLI**

```bash
gh auth login -h github.com
# 选择 GitHub.com
# 选择 HTTPS
# 选择 "Paste an authentication token"
# 从 https://github.com/settings/tokens 生成 Personal Access Token (需要 repo 权限)
```

**方法 3：在 URL 中嵌入 token (不推荐，仅临时)**

```bash
git remote set-url origin https://<TOKEN>@github.com/dpfai/quant-learning.git
```

### 推送流程

```bash
# 1. 检查状态
git status

# 2. 暂存变更
git add <files>

# 3. 提交
git commit -m "message"

# 4. 推送
git push origin main
# 或推送到新分支
git push origin <branch-name>
```

---

## 📦 Phase 4-5 — Risk Analysis & Market Overview (Codex Task)

**目标：** 实现风险分析指标和完善市场概览功能

### Phase 4 — Risk Analysis

#### 1. 创建 `features/risk_metrics.py`

参考 `reference-repos/ai-hedge-fund/src/agents/risk_manager.py` 的风险指标实现。

```python
"""
风险指标计算模块
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple


def calculate_returns(prices: pd.Series) -> pd.Series:
    """计算日收益率"""
    pass


def calculate_annualized_return(returns: pd.Series, periods_per_year: int = 252) -> float:
    """计算年化收益率"""
    pass


def calculate_annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
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


def calculate_all_risk_metrics(
    prices: pd.Series, 
    benchmark_prices: Optional[pd.Series] = None,
    risk_free_rate: float = 0.05
) -> Dict:
    """
    一次性计算所有风险指标
    
    Returns:
        {
            'total_return': float,
            'ann_return': float,
            'ann_volatility': float,
            'max_drawdown': float,
            'max_dd_start': pd.Timestamp,
            'max_dd_end': pd.Timestamp,
            'sharpe_ratio': float,
            'sortino_ratio': float,
            'beta': float or None,
            'win_rate': float,
            'avg_gain': float,
            'avg_loss': float,
        }
    """
    pass
```

#### 2. 更新 `config/settings.py`

添加风险相关配置：

```python
# Risk settings
RISK_FREE_RATE = 0.05  # 无风险利率 (5%)

# Sector ETFs for market overview
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

#### 3. 更新 `pages/2_Stock_Detail.py`

在现有页面添加风险指标面板：

```python
# 在技术指标下方添加
st.subheader("⚠️ Risk Metrics")

from features.risk_metrics import calculate_all_risk_metrics

# 获取 SPY 作为基准
spy_data = loader.download("SPY", period=period)
metrics = calculate_all_risk_metrics(df["Adj Close"], spy_data["Adj Close"])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Ann. Return", f"{metrics['ann_return']*100:.1f}%")
with col2:
    st.metric("Ann. Volatility", f"{metrics['ann_volatility']*100:.1f}%")
with col3:
    st.metric("Max Drawdown", f"{metrics['max_drawdown']*100:.1f}%")
with col4:
    st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")

col5, col6, col7 = st.columns(3)
with col5:
    st.metric("Sortino Ratio", f"{metrics['sortino_ratio']:.2f}")
with col6:
    if metrics['beta'] is not None:
        st.metric("Beta (vs SPY)", f"{metrics['beta']:.2f}")
with col7:
    st.metric("Win Rate", f"{metrics['win_rate']*100:.1f}%")
```

#### 4. 创建 `tests/test_risk_metrics.py`

```python
"""测试风险指标模块"""
import pandas as pd
import numpy as np
from features.risk_metrics import *


def test_calculate_returns():
    prices = pd.Series([100, 102, 101, 103, 105])
    returns = calculate_returns(prices)
    assert len(returns) == len(prices) - 1
    assert abs(returns.iloc[0] - 0.02) < 0.001  # (102-100)/100


def test_max_drawdown():
    prices = pd.Series([100, 110, 90, 95, 85, 100])
    max_dd, start, end = calculate_max_drawdown(prices)
    assert abs(max_dd - (-0.227)) < 0.01  # 从110跌到85


def test_sharpe_ratio():
    returns = pd.Series([0.01, -0.005, 0.02, 0.015, -0.01] * 50)
    sharpe = calculate_sharpe_ratio(returns)
    assert isinstance(sharpe, float)


def test_beta():
    stock = pd.Series([0.01, 0.02, -0.01, 0.015, 0.005])
    market = pd.Series([0.008, 0.015, -0.005, 0.012, 0.003])
    beta = calculate_beta(stock, market)
    assert isinstance(beta, float)
```

---

### Phase 5 — Market Overview Enhancement

#### 1. 创建 `utils/market_regime.py`

参考 `reference-repos/TradingAgents/tradingagents/agents/` 的市场分析逻辑。

```python
"""
市场状态判断模块
"""
import pandas as pd
from typing import Dict
from utils.data_loader import DataLoader


def get_market_regime(spy_df: pd.DataFrame, vix_value: float) -> Dict:
    """
    判断市场状态
    
    规则（简化版）：
    - RISK-ON: VIX < 20 且 SPY > MA50 且 SPY > MA200
    - RISK-OFF: VIX > 25 或 SPY < MA50 且 SPY < MA200
    - NEUTRAL: 其他情况
    
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
```

#### 2. 更新 `utils/chart_builder.py`

添加 VIX 仪表盘图：

```python
@staticmethod
def create_vix_gauge(vix_value: float) -> go.Figure:
    """
    创建 VIX 仪表盘
    
    颜色区间：
    - 0-15: 绿色 (低波动)
    - 15-20: 黄色 (正常)
    - 20-25: 橙色 (偏高)
    - 25+: 红色 (高波动)
    """
    pass
```

#### 3. 更新 `pages/1_Market_Overview.py`

添加以下功能模块：

```python
# === 1. 市场状态面板 ===
st.subheader("🎯 Market Regime")

from utils.market_regime import get_market_regime

regime = get_market_regime(spy_df, vix_value)

if regime['regime'] == 'RISK-ON':
    st.success(f"🟢 {regime['regime']} - {regime['description']}")
elif regime['regime'] == 'RISK-OFF':
    st.error(f"🔴 {regime['regime']} - {regime['description']}")
else:
    st.warning(f"🟡 {regime['regime']} - {regime['description']}")

# === 2. VIX 风险面板 ===
st.subheader("📊 VIX Risk Panel")

vix_fig = ChartBuilder.create_vix_gauge(vix_value)
st.plotly_chart(vix_fig, use_container_width=True)

# === 3. 板块表现 ===
st.subheader("🏭 Sector Performance")

from utils.market_regime import get_sector_performance

sector_df = get_sector_performance("3m")
fig = px.bar(sector_df.sort_values('Return'), 
             x='Return', y='Name',
             orientation='h',
             color='Return',
             color_continuous_scale='RdYlGn')
st.plotly_chart(fig, use_container_width=True)
```

---

### 完成标准

- [x] `features/risk_metrics.py` 创建并实现所有风险指标
- [x] `tests/test_risk_metrics.py` 创建并通过所有测试
- [x] `utils/market_regime.py` 创建并实现市场状态判断
- [x] `utils/chart_builder.py` 添加 VIX 仪表盘
- [x] `pages/2_Stock_Detail.py` 添加风险指标面板
- [x] `pages/1_Market_Overview.py` 添加市场状态和板块表现
- [x] `config/settings.py` 更新风险相关配置
- [x] `pytest` 全部通过
- [x] `streamlit run app.py` 正常运行

### 参考文件

| 文件 | 用途 |
|------|------|
| `reference-repos/ai-hedge-fund/src/agents/risk_manager.py` | 风险指标计算 |
| `reference-repos/TradingAgents/tradingagents/agents/technical_analyst.py` | 技术分析逻辑 |
| `reference-repos/Qlib/qlib/contrib/report/` | 报告生成模式 |

### 备注

- 风险指标计算要考虑边界情况（空数据、单一数据点）
- VIX 仪表盘使用 Plotly 的 gauge chart 类型
- 板块表现使用 SECTOR_ETFS 配置中的 ETF 列表
- 保持代码简洁，后续可在 Phase 9 增强预测功能

---

## Session: 2026-06-14 00:22 PDT

### Agent: Codex

**完成：**
- 检查 Phase 1.5 发布范围、当前分支和 GitHub remote。
- 确认工作区仅包含 Phase 1.5 相关变更。

**文件变更：**
- 更新 `WORKLOG.md`

**验证：**
- `git diff --check` — 通过。
- `gh --version` — GitHub CLI 2.92.0 已安装。
- `gh auth status` — 失败，`dpfai` 的 GitHub token 已失效。

**阻塞或注意事项：**
- GitHub authentication 阻塞 commit/push/PR 发布流程。
- 需要先运行 `gh auth login -h github.com` 重新认证。

**下一步：**
- 认证成功后创建 `codex/phase-1-5-data-provider-refactor`，提交并 push Phase 1.5 变更，然后创建 draft PR。

## Session: 2026-06-14 00:19 PDT

### Agent: Codex

**完成：**
- 完成 Phase 1.5 — Data Layer Refactor。
- 新增 `DataProvider` 抽象接口和 `YFinanceProvider` 实现。
- 将 yfinance 下载、ticker alias、DataFrame 清理和 parquet 缓存逻辑从 `DataLoader` 迁移到 provider。
- 将 `DataLoader` 重构为统一入口，保留原有 `download`、`download_batch`、`is_cache_valid`、`clear_cache` 和 `use_cache=False` 行为。
- 新增 start/end date 下载支持，并为日期范围使用独立缓存键。
- 扩展 data loader 测试，覆盖缓存复用、绕过缓存、批量下载、VIX alias、日期参数、provider 选择和未知 provider。
- 新增 `pytest.ini`，避免 pytest 收集 `reference-repos/` 内第三方项目测试。

**文件变更：**
- 新增 `utils/data_providers/__init__.py`
- 新增 `utils/data_providers/base.py`
- 新增 `utils/data_providers/yfinance_provider.py`
- 重构 `utils/data_loader.py`
- 更新 `tests/test_data_loader.py`
- 新增 `pytest.ini`
- 更新 `WORKLOG.md`

**验证：**
- `venv/bin/python -m py_compile app.py config/settings.py utils/data_loader.py utils/data_providers/base.py utils/data_providers/yfinance_provider.py` — 通过。
- `venv/bin/python -m pytest tests/test_data_loader.py -q` — 7 passed。
- `venv/bin/python -m pytest -q` — 13 passed。
- `venv/bin/streamlit run app.py --server.headless true --server.port 8501` — 启动成功。
- `curl -I http://localhost:8501` — HTTP 200 OK。
- `git diff --check` — 通过。

**阻塞或注意事项：**
- 无阻塞。
- 当前仅注册 `yfinance` provider；后续 provider 可通过 `DataLoader._get_provider()` 接入。

**下一步：**
- 按 roadmap 继续 Phase 4-5 — 风险分析和市场概览。

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

- [x] `utils/data_providers/base.py` 创建并定义 `DataProvider` 抽象类
- [x] `utils/data_providers/yfinance_provider.py` 实现具体 provider
- [x] `utils/data_loader.py` 重构为统一入口
- [x] 所有现有功能保持不变（向后兼容）
- [x] `pytest tests/test_data_loader.py` 通过
- [x] `streamlit run app.py` 正常运行

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
- [x] Phase 4-5 — 风险分析 + 市场概览
- [x] Phase 6-7 — 股票详情 + Watchlist
- [x] Phase 8-9 — 回测 + 预测

**下一步：** Codex 执行 Phase 4-5 开发。
