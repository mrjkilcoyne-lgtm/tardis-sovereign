"""Trading engine. Vex-inspired dense financial operations.

Borrows from Vex-Lang: K/APL-inspired dense expressions,
adaptive risk management, DeFi primitives, exchange execution.

Fixed points and multiplicities. Time runs both directions.
Every story ever told is true - including the ones about
compound interest.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


# ── Risk Management (from Vex adaptive risk model) ──

class RiskLevel(Enum):
    MINIMAL = 0    # capital preservation only
    LOW = 1        # savings rates, switching bonuses
    MODERATE = 2   # matched betting, yield farming
    ACTIVE = 3     # trading with stops
    AGGRESSIVE = 4 # leveraged positions (NOT for £200)


@dataclass
class RiskProfile:
    """Adaptive risk. Adjusts based on capital, wins, losses."""
    max_risk_level: RiskLevel = RiskLevel.LOW
    capital: float = 200.0
    max_single_risk: float = 0.05  # never risk more than 5% on one play
    max_daily_risk: float = 0.10   # never risk more than 10% in a day
    wins: int = 0
    losses: int = 0
    streak: int = 0  # positive = winning streak, negative = losing

    @property
    def max_position_size(self) -> float:
        return self.capital * self.max_single_risk

    @property
    def daily_risk_budget(self) -> float:
        return self.capital * self.max_daily_risk

    def record_win(self, amount: float):
        self.capital += amount
        self.wins += 1
        self.streak = max(1, self.streak + 1)

    def record_loss(self, amount: float):
        self.capital -= amount
        self.losses += 1
        self.streak = min(-1, self.streak - 1)
        # Adaptive: tighten risk after losses
        if self.streak <= -3:
            self.max_single_risk = max(0.01, self.max_single_risk * 0.5)

    def reset_daily(self):
        """Reset daily counters. The risk budget refreshes."""
        pass  # daily_risk_budget recalculates from current capital

    @property
    def win_rate(self) -> float:
        total = self.wins + self.losses
        return self.wins / total if total > 0 else 0.0

    def status(self) -> dict:
        return {
            "capital": round(self.capital, 2),
            "max_position": round(self.max_position_size, 2),
            "daily_budget": round(self.daily_risk_budget, 2),
            "win_rate": f"{self.win_rate:.0%}",
            "streak": self.streak,
            "risk_level": self.max_risk_level.name,
        }


# ── Trade Types (from Vex DeFi primitives) ──

class TradeType(Enum):
    # Zero-risk (fixed points)
    BANK_SWITCH = "bank_switch"           # guaranteed £100-175
    SAVINGS_RATE = "savings_rate"         # guaranteed APR
    CASHBACK = "cashback"                 # guaranteed % back
    REFERRAL = "referral"                 # guaranteed per signup

    # Low-risk (near-fixed)
    MATCHED_BET = "matched_bet"          # mathematically locked
    STABLECOIN_YIELD = "stablecoin_yield"  # yield on stables

    # Moderate (multiplicities)
    SPOT_TRADE = "spot_trade"            # buy low sell high
    SWING_TRADE = "swing_trade"          # multi-day position
    ARBITRAGE = "arbitrage"              # cross-exchange price diff
    YIELD_FARM = "yield_farm"            # liquidity provision

    # Meta
    COMPOUND = "compound"                # reinvest returns


@dataclass
class Trade:
    """A single trade or financial action."""
    trade_type: TradeType
    description: str
    entry_amount: float
    expected_return: float     # in currency units
    expected_return_pct: float # as percentage
    risk_amount: float         # max you could lose
    time_horizon: str
    confidence: float          # 0-1
    platform: str = ""
    status: str = "pending"    # pending, active, won, lost, expired
    entered_at: datetime | None = None
    closed_at: datetime | None = None
    actual_return: float = 0.0

    @property
    def risk_reward_ratio(self) -> float:
        if self.risk_amount == 0:
            return float('inf')  # free money
        return self.expected_return / self.risk_amount

    def to_dict(self) -> dict:
        return {
            "type": self.trade_type.value,
            "description": self.description,
            "entry": self.entry_amount,
            "expected_return": self.expected_return,
            "expected_pct": f"{self.expected_return_pct:.1f}%",
            "risk": self.risk_amount,
            "rr_ratio": f"{self.risk_reward_ratio:.1f}:1" if self.risk_reward_ratio != float('inf') else "∞:1",
            "time": self.time_horizon,
            "confidence": f"{self.confidence:.0%}",
            "platform": self.platform,
            "status": self.status,
        }


# ── Trade Generator (the Vex expression engine, simplified) ──

@dataclass
class TradeBook:
    """The book of all trades. Past, present, proposed."""
    risk_profile: RiskProfile = field(default_factory=RiskProfile)
    trades: list[Trade] = field(default_factory=list)
    journal: list[dict] = field(default_factory=list)

    def propose(self, trade: Trade) -> bool:
        """Propose a trade. Returns True if it passes risk checks."""
        # Risk gate 1: position size
        if trade.risk_amount > self.risk_profile.max_position_size:
            self._log("REJECTED", trade, f"Risk {trade.risk_amount} > max position {self.risk_profile.max_position_size}")
            return False

        # Risk gate 2: risk-reward ratio (minimum 2:1 for non-fixed)
        if trade.trade_type not in (TradeType.BANK_SWITCH, TradeType.SAVINGS_RATE,
                                      TradeType.CASHBACK, TradeType.REFERRAL,
                                      TradeType.MATCHED_BET):
            if trade.risk_reward_ratio < 2.0:
                self._log("REJECTED", trade, f"R:R ratio {trade.risk_reward_ratio:.1f} < 2.0")
                return False

        # Risk gate 3: confidence threshold
        if trade.confidence < 0.5:
            self._log("REJECTED", trade, f"Confidence {trade.confidence:.0%} too low")
            return False

        # Passed all gates
        trade.status = "active"
        trade.entered_at = datetime.now()
        self.trades.append(trade)
        self._log("ENTERED", trade, "Passed all risk gates")
        return True

    def close(self, trade: Trade, actual_return: float):
        """Close a trade with the actual result."""
        trade.actual_return = actual_return
        trade.closed_at = datetime.now()

        if actual_return >= 0:
            trade.status = "won"
            self.risk_profile.record_win(actual_return)
            self._log("WON", trade, f"+£{actual_return:.2f}")
        else:
            trade.status = "lost"
            self.risk_profile.record_loss(abs(actual_return))
            self._log("LOST", trade, f"-£{abs(actual_return):.2f}")

    def generate_fixed_points(self, capital: float = None) -> list[Trade]:
        """Generate all zero/low-risk trades available right now."""
        cap = capital or self.risk_profile.capital
        trades = []

        # Bank switching - always available
        trades.append(Trade(
            trade_type=TradeType.BANK_SWITCH,
            description="Switch to First Direct for £175 bonus",
            entry_amount=0, expected_return=175, expected_return_pct=0,
            risk_amount=0, time_horizon="2-4 weeks",
            confidence=0.95, platform="First Direct",
        ))

        # Savings rate on capital
        if cap > 0:
            annual_return = cap * 0.051  # 5.1% Chase
            monthly_return = annual_return / 12
            trades.append(Trade(
                trade_type=TradeType.SAVINGS_RATE,
                description=f"£{cap:.0f} at 5.1% in Chase easy-access",
                entry_amount=cap, expected_return=round(monthly_return, 2),
                expected_return_pct=5.1, risk_amount=0,
                time_horizon="monthly", confidence=1.0,
                platform="Chase UK",
            ))

        # Cashback
        trades.append(Trade(
            trade_type=TradeType.CASHBACK,
            description="1% cashback on all spending via Chase debit",
            entry_amount=0, expected_return=10, expected_return_pct=1.0,
            risk_amount=0, time_horizon="monthly (on ~£1000 spend)",
            confidence=0.95, platform="Chase UK",
        ))

        # Matched betting
        if cap >= 50:
            trades.append(Trade(
                trade_type=TradeType.MATCHED_BET,
                description="Intro offer matched bets (mathematically locked profit)",
                entry_amount=50, expected_return=500, expected_return_pct=1000,
                risk_amount=0, time_horizon="2-4 weeks",
                confidence=0.90, platform="OddsMonkey",
            ))

        # Referrals
        trades.append(Trade(
            trade_type=TradeType.REFERRAL,
            description="Trading 212 + Chase + Chip referrals",
            entry_amount=0, expected_return=30, expected_return_pct=0,
            risk_amount=0, time_horizon="per referral",
            confidence=0.80, platform="Various",
        ))

        return trades

    def generate_multiplicities(self, capital: float = None) -> list[Trade]:
        """Generate variable-return opportunities."""
        cap = capital or self.risk_profile.capital
        max_risk = self.risk_profile.max_position_size
        trades = []

        # Stablecoin yield (if crypto-comfortable)
        if cap >= 50:
            trades.append(Trade(
                trade_type=TradeType.STABLECOIN_YIELD,
                description="USDC/DAI lending on Aave (variable APY ~3-8%)",
                entry_amount=min(cap * 0.3, 100),
                expected_return=round(min(cap * 0.3, 100) * 0.06 / 12, 2),
                expected_return_pct=6.0,
                risk_amount=round(min(cap * 0.3, 100) * 0.02, 2),  # smart contract risk
                time_horizon="monthly",
                confidence=0.75, platform="Aave",
            ))

        # Cross-exchange arbitrage scanning
        trades.append(Trade(
            trade_type=TradeType.ARBITRAGE,
            description="Monitor BTC/ETH price gaps between Kraken/Binance/Coinbase",
            entry_amount=min(cap * 0.2, max_risk),
            expected_return=round(min(cap * 0.2, max_risk) * 0.02, 2),
            expected_return_pct=2.0,
            risk_amount=round(min(cap * 0.2, max_risk) * 0.005, 2),
            time_horizon="per opportunity (minutes)",
            confidence=0.60, platform="Multiple exchanges",
        ))

        return trades

    def portfolio_summary(self) -> dict:
        """Current state of the book."""
        active = [t for t in self.trades if t.status == "active"]
        won = [t for t in self.trades if t.status == "won"]
        lost = [t for t in self.trades if t.status == "lost"]
        total_won = sum(t.actual_return for t in won)
        total_lost = sum(abs(t.actual_return) for t in lost)

        return {
            "capital": round(self.risk_profile.capital, 2),
            "active_trades": len(active),
            "total_trades": len(self.trades),
            "wins": len(won),
            "losses": len(lost),
            "total_won": round(total_won, 2),
            "total_lost": round(total_lost, 2),
            "net_pnl": round(total_won - total_lost, 2),
            "risk_status": self.risk_profile.status(),
        }

    def to_briefing(self) -> str:
        """Produce a readable trading briefing."""
        fixed = self.generate_fixed_points()
        mult = self.generate_multiplicities()

        lines = [
            "# Trading Briefing",
            f"*Capital: £{self.risk_profile.capital:.2f} | "
            f"Max position: £{self.risk_profile.max_position_size:.2f} | "
            f"Risk level: {self.risk_profile.max_risk_level.name}*",
            "",
            "## Fixed Points (zero/low risk)",
            "",
        ]
        for t in fixed:
            lines.append(f"**{t.description}**")
            lines.append(f"  Return: £{t.expected_return} | Risk: £{t.risk_amount} | "
                        f"R:R: {t.risk_reward_ratio if t.risk_reward_ratio != float('inf') else '∞'}:1 | "
                        f"Confidence: {t.confidence:.0%}")
            lines.append(f"  Platform: {t.platform} | Time: {t.time_horizon}")
            lines.append("")

        lines.append("## Multiplicities (variable return)")
        lines.append("")
        for t in mult:
            lines.append(f"**{t.description}**")
            lines.append(f"  Entry: £{t.entry_amount} | Expected: £{t.expected_return} | "
                        f"Risk: £{t.risk_amount} | R:R: {t.risk_reward_ratio:.1f}:1")
            lines.append(f"  Platform: {t.platform} | Confidence: {t.confidence:.0%}")
            lines.append("")

        summary = self.portfolio_summary()
        lines.append("## Portfolio Status")
        lines.append(f"Net P&L: £{summary['net_pnl']} | "
                     f"Wins: {summary['wins']} | Losses: {summary['losses']} | "
                     f"Win rate: {self.risk_profile.win_rate:.0%}")

        return "\n".join(lines)

    def _log(self, action: str, trade: Trade, note: str):
        self.journal.append({
            "time": datetime.now().isoformat(),
            "action": action,
            "type": trade.trade_type.value,
            "description": trade.description,
            "note": note,
        })


# ── Vex-style dense expressions for quick trade evaluation ──

def evaluate_trade(
    entry: float, target: float, stop: float,
    confidence: float = 0.7
) -> dict:
    """Quick trade evaluation. Vex-dense.

    Usage: evaluate_trade(100, 115, 95, 0.7)
    Meaning: Enter at 100, target 115, stop at 95, 70% confident
    """
    risk = entry - stop
    reward = target - entry
    rr = reward / risk if risk > 0 else float('inf')
    ev = (confidence * reward) - ((1 - confidence) * risk)  # expected value

    return {
        "entry": entry,
        "target": target,
        "stop": stop,
        "risk": round(risk, 2),
        "reward": round(reward, 2),
        "rr_ratio": round(rr, 2),
        "confidence": confidence,
        "expected_value": round(ev, 2),
        "verdict": "TAKE" if ev > 0 and rr >= 2 else "PASS",
    }


def compound(principal: float, rate: float, periods: int) -> list[dict]:
    """Compound growth projection. Time runs forward.

    Usage: compound(200, 0.05, 12)
    Meaning: £200 at 5% for 12 periods
    """
    history = []
    balance = principal
    for i in range(1, periods + 1):
        interest = balance * rate
        balance += interest
        history.append({
            "period": i,
            "balance": round(balance, 2),
            "interest": round(interest, 2),
            "total_interest": round(balance - principal, 2),
        })
    return history
