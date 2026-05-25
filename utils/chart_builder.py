"""
Plotly chart builders for market data.
"""
from __future__ import annotations

from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.settings import DEFAULT_CHART_HEIGHT


class ChartBuilder:
    """Create reusable interactive market charts."""

    @staticmethod
    def candlestick(df: pd.DataFrame, title: str = "", show_volume: bool = True) -> go.Figure:
        """Build a candlestick chart with optional volume subplot."""
        rows = 2 if show_volume and "Volume" in df.columns else 1
        row_heights = [0.75, 0.25] if rows == 2 else [1.0]
        fig = make_subplots(
            rows=rows,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=row_heights,
        )

        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="OHLC",
            ),
            row=1,
            col=1,
        )

        if rows == 2:
            fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"), row=2, col=1)

        fig.update_layout(
            title=title,
            height=DEFAULT_CHART_HEIGHT,
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
        )
        return fig

    @staticmethod
    def line_chart(df: pd.DataFrame, column: str = "Close", title: str = "") -> go.Figure:
        """Build a line chart for one column."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode="lines", name=column))
        fig.update_layout(title=title, height=DEFAULT_CHART_HEIGHT, hovermode="x unified")
        return fig

    @staticmethod
    def multi_comparison(dfs: Dict[str, pd.DataFrame], column: str = "Close", normalize: bool = True) -> go.Figure:
        """Build a multi-ticker comparison chart, optionally normalized to 100."""
        fig = go.Figure()

        for ticker, df in dfs.items():
            if df.empty or column not in df.columns:
                continue

            series = df[column].dropna()
            if normalize and not series.empty:
                series = series / series.iloc[0] * 100

            fig.add_trace(go.Scatter(x=series.index, y=series, mode="lines", name=ticker))

        y_title = "Normalized Price (Start = 100)" if normalize else column
        fig.update_layout(
            title="Market Comparison",
            yaxis_title=y_title,
            height=DEFAULT_CHART_HEIGHT,
            hovermode="x unified",
        )
        return fig

    @staticmethod
    def returns_chart(df: pd.DataFrame, period: str = "D") -> go.Figure:
        """Build a returns chart using Close-to-Close percentage returns."""
        returns = df["Close"].resample(period).last().pct_change().dropna()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=returns.index, y=returns * 100, name="Return %"))
        fig.update_layout(title="Returns", yaxis_title="Return (%)", height=DEFAULT_CHART_HEIGHT)
        return fig

    @staticmethod
    def add_moving_averages(fig: go.Figure, df: pd.DataFrame, periods: List[int] | None = None) -> go.Figure:
        """Add moving average overlays to an existing figure."""
        periods = periods or [20, 50, 200]
        for period in periods:
            if len(df) >= period:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df["Close"].rolling(period).mean(),
                        mode="lines",
                        name=f"MA{period}",
                    )
                )
        return fig
