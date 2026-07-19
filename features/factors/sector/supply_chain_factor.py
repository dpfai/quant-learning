"""Supply-chain propagation factor prototypes."""
from __future__ import annotations


def supply_chain_propagation(upstream_signal, exposure_weight, transmission_lag: int = 1):
    """Map an upstream operating signal into an exposed downstream company.

    Business logic: changes in supplier orders, lead times, or inventory can precede
    downstream revenue. ``exposure_weight`` represents sourced revenue/input share;
    a real pipeline would lag the point-in-time upstream signal, map supplier/customer
    relationships, and validate separate propagation speeds by industry.
    """
    if transmission_lag < 0:
        raise ValueError("transmission_lag cannot be negative")
    shifted = upstream_signal.shift(transmission_lag) if hasattr(upstream_signal, "shift") else upstream_signal
    return shifted * exposure_weight
