from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class SignalDecision:
    lane: str
    green_duration: int
    reason: str


def decide_signal_control(
    lane_counts: dict[str, int],
    emergency_lanes: Iterable[str] | None = None,
    min_green: int = 10,
    max_green: int = 60,
) -> SignalDecision:
    """Decide which lane gets green light and for how long."""
    emergency_lanes = [lane for lane in (emergency_lanes or []) if lane in lane_counts]

    if emergency_lanes:
        return SignalDecision(
            lane=emergency_lanes[0],
            green_duration=max_green,
            reason="Emergency vehicle priority",
        )

    if not lane_counts:
        return SignalDecision(
            lane="none",
            green_duration=min_green,
            reason="No lanes available",
        )

    selected_lane = max(sorted(lane_counts), key=lambda lane: lane_counts[lane])
    total = sum(max(count, 0) for count in lane_counts.values())
    selected_count = max(lane_counts[selected_lane], 0)

    if total == 0:
        duration = min_green
    else:
        ratio = selected_count / total
        duration = int(min_green + ratio * (max_green - min_green))
        duration = max(min_green, min(max_green, duration))

    return SignalDecision(
        lane=selected_lane,
        green_duration=duration,
        reason="Highest congestion lane",
    )
