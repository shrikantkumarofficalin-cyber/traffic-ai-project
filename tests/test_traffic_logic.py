import unittest

from traffic_logic import decide_signal_control


class TrafficSignalDecisionTests(unittest.TestCase):
    def test_emergency_lane_gets_priority(self):
        decision = decide_signal_control(
            {"north": 2, "south": 20, "east": 1, "west": 1},
            emergency_lanes=["east"],
        )
        self.assertEqual(decision.lane, "east")
        self.assertEqual(decision.green_duration, 60)
        self.assertEqual(decision.reason, "Emergency vehicle priority")

    def test_highest_congestion_lane_selected(self):
        decision = decide_signal_control({"north": 10, "south": 3, "east": 2, "west": 1})
        self.assertEqual(decision.lane, "north")
        self.assertGreaterEqual(decision.green_duration, 10)
        self.assertLessEqual(decision.green_duration, 60)
        self.assertEqual(decision.reason, "Highest congestion lane")

    def test_empty_lane_counts_returns_none_lane(self):
        decision = decide_signal_control({})
        self.assertEqual(decision.lane, "none")
        self.assertEqual(decision.green_duration, 10)
        self.assertEqual(decision.reason, "No lanes available")

    def test_zero_traffic_uses_minimum_duration(self):
        decision = decide_signal_control({"north": 0, "south": 0, "east": 0, "west": 0})
        self.assertEqual(decision.green_duration, 10)
        self.assertEqual(decision.reason, "Highest congestion lane")


if __name__ == "__main__":
    unittest.main()
