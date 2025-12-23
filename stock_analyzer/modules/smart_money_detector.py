from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd


def detect_smart_money_activity(
    technical_df: Optional[pd.DataFrame],
    *,
    min_volume_ratio: float = 1.8,
    min_price_change_pct: float = 1.0,
    lookback_days: int = 60,
) -> Dict[str, Any]:
    """
    Flags potential "smart money" accumulation events based on volume and price action.

    Args:
        technical_df: DataFrame that includes at least 'Close' and 'Volume' columns.
        min_volume_ratio: Minimum multiple of the 20-session average volume to consider significant.
        min_price_change_pct: Minimum daily percentage gain required to confirm demand.
        lookback_days: Number of most recent sessions to inspect.

    Returns:
        Dictionary with detected signals and diagnostic metadata for downstream filtering.
    """
    if (
        technical_df is None
        or technical_df.empty
        or "Volume" not in technical_df.columns
        or "Close" not in technical_df.columns
    ):
        return {
            "signals": [],
            "total_sessions": 0,
            "filters": {
                "min_volume_ratio": min_volume_ratio,
                "min_price_change_pct": min_price_change_pct,
                "lookback_days": lookback_days,
            },
        }

    window = max(lookback_days, 25)
    df = technical_df.tail(window).copy()
    if df.empty:
        return {
            "signals": [],
            "total_sessions": 0,
            "filters": {
                "min_volume_ratio": min_volume_ratio,
                "min_price_change_pct": min_price_change_pct,
                "lookback_days": lookback_days,
            },
        }

    df["Volume_MA20"] = df["Volume"].rolling(window=20, min_periods=5).mean()
    df["Volume_Ratio"] = df["Volume"] / df["Volume_MA20"]
    df["Price_Change_Pct"] = df["Close"].pct_change() * 100
    df["Close_MA20"] = df["Close"].rolling(window=20, min_periods=5).mean()
    df["Pct_from_MA20"] = ((df["Close"] - df["Close_MA20"]) / df["Close_MA20"]) * 100
    df["High_20"] = df["Close"].rolling(window=20, min_periods=5).max()
    df["Is_Breakout"] = df["High_20"].notna() & (df["Close"] >= df["High_20"] * 0.998)
    if "RSI" in technical_df.columns:
        df["RSI"] = technical_df["RSI"].reindex(df.index)
    else:
        df["RSI"] = pd.Series(index=df.index, dtype=float)

    df = df.dropna(subset=["Volume_Ratio", "Price_Change_Pct"])

    df["Core_Signal"] = (df["Volume_Ratio"] >= min_volume_ratio) & (
        df["Price_Change_Pct"] >= min_price_change_pct
    )
    df["Early_Signal"] = (df["Volume_Ratio"] >= min_volume_ratio * 1.4) & (
        df["Price_Change_Pct"] >= min_price_change_pct * 0.6
    )
    signals_df = df[df["Core_Signal"] | df["Early_Signal"]].copy()

    signals: List[Dict[str, Any]] = []
    for idx, row in signals_df.iterrows():
        severity: str
        if row["Volume_Ratio"] >= min_volume_ratio * 2 or row["Price_Change_Pct"] >= min_price_change_pct * 2:
            severity = "Cực mạnh"
        elif row["Core_Signal"]:
            severity = "Mạnh"
        else:
            severity = "Cảnh báo sớm"

        if row["Is_Breakout"]:
            signal_type = "Breakout xác nhận"
        elif row["Price_Change_Pct"] >= min_price_change_pct:
            signal_type = "Tích lũy mạnh"
        else:
            signal_type = "Cảnh báo sớm"

        volume_score = min(50.0, (row["Volume_Ratio"] / max(min_volume_ratio, 0.1)) * 30)
        price_score = min(30.0, max(0.0, row["Price_Change_Pct"] - min_price_change_pct) * 4)
        trend_bonus = 0.0
        pct_from_ma20 = row.get("Pct_from_MA20")
        if pct_from_ma20 is not None and not pd.isna(pct_from_ma20):
            trend_bonus += min(15.0, max(0.0, pct_from_ma20) * 1.5)
        if row["Is_Breakout"]:
            trend_bonus += 5.0
        confidence = min(100.0, round(volume_score + price_score + trend_bonus, 1))

        risk_notes: List[str] = []
        rsi_value = float(row["RSI"]) if pd.notna(row["RSI"]) else None
        if rsi_value and rsi_value >= 75:
            risk_notes.append("RSI cao")
        if pct_from_ma20 is not None and not pd.isna(pct_from_ma20) and pct_from_ma20 >= 8:
            risk_notes.append("Giá xa MA20")
        note = ", ".join(risk_notes) if risk_notes else "Đạt yêu cầu"

        signals.append(
            {
                "date": idx.strftime("%Y-%m-%d"),
                "volume_ratio": float(row["Volume_Ratio"]),
                "price_change_pct": float(row["Price_Change_Pct"]),
                "close": float(row["Close"]),
                "severity": severity,
                "type": signal_type,
                "confidence": confidence,
                "score": confidence,
                "rsi": rsi_value,
                "distance_ma20": float(pct_from_ma20) if pct_from_ma20 is not None and not pd.isna(pct_from_ma20) else None,
                "is_breakout": bool(row["Is_Breakout"]),
                "note": note,
                "description": (
                    f"Khối lượng gấp {row['Volume_Ratio']:.1f} lần MA20, "
                    f"giá +{row['Price_Change_Pct']:.2f}% so với phiên trước."
                ),
            }
        )

    # Sort newest first for easier consumption in the UI
    signals.sort(key=lambda item: item["date"], reverse=True)

    return {
        "signals": signals,
        "total_sessions": int(len(df)),
        "filters": {
            "min_volume_ratio": min_volume_ratio,
            "min_price_change_pct": min_price_change_pct,
            "lookback_days": lookback_days,
        },
        "last_updated": df.index[-1].strftime("%Y-%m-%d") if len(df) else None,
    }

