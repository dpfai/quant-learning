"""Sector-specific factor prototypes."""

from .ad_tech_signals import digital_ad_spend_growth, ecpm_trend, platform_mix
from .consumer_signals import consumer_demand_momentum, discretionary_pressure
from .supply_chain_factor import supply_chain_propagation

__all__ = ["digital_ad_spend_growth", "ecpm_trend", "platform_mix", "consumer_demand_momentum", "discretionary_pressure", "supply_chain_propagation"]
