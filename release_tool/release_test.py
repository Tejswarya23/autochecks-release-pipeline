import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from release_tool.release import evaluate_gates, generate_manifest

class TestGateEvaluation(unittest.TestCase):

    # PASS TEST CASES
    def test_all_gates_pass(self):
        results = evaluate_gates(100.0, 0,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertTrue(all(v["passed"] for v in results.values()))

    def test_pass_rate_at_exact_threshold(self):
        """ 
           95.0% is the minimum - should still pass 
        """
        results = evaluate_gates(95.0, 0,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertTrue(results["test_pass_rate"]["passed"])

    def test_manifest_approved(self):
        m = generate_manifest(100.0, 0,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertTrue(m["release_approved"])
        self.assertEqual(m["summary"], "RELEASE APPROVED")

    #FAILURE TEST CASES
    def test_low_pass_rate_blocks_release(self):
        """
           80% pass rate is below 95% threshold -  must block 
        """
        results = evaluate_gates(80.0, 0,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertFalse(results["test_pass_rate"]["passed"])

    def test_zero_pass_rate_blocks_release(self):
        """ 
           0% pass rate - catastrophic failure
        """
        results = evaluate_gates(0.0, 0,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertFalse(results["test_pass_rate"]["passed"])

    def test_p0_issue_blocks_release(self):
        """ 
           Any open P0 bug must block release
        """
        results = evaluate_gates(100.0, 1,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertFalse(results["p0_issues"]["passed"])

    def test_multiple_p0_issues_blocks_release(self):
        """
           Multiple P0 bugs - still blocked
        """
        results = evaluate_gates(100.0, 5,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertFalse(results["p0_issues"]["passed"])

    def test_missing_single_module_blocks_release(self):
        """
           One missing module should block
        """
        results = evaluate_gates(100.0, 0,
            ["vehicle_simulator", "release_tool"], True)
        self.assertFalse(results["required_modules"]["passed"])
        self.assertIn("config", results["required_modules"]["missing"])

    def test_missing_all_modules_blocks_release(self):
        """
           No modules built -  must block
        """
        results = evaluate_gates(100.0, 0, [], True)
        self.assertFalse(results["required_modules"]["passed"])

    def test_missing_artifact_blocks_release(self):
        """
           No release artifact -  must block
        """
        results = evaluate_gates(100.0, 0,
            ["vehicle_simulator", "release_tool", "config"], False)
        self.assertFalse(results["artifact_exists"]["passed"])

    def test_manifest_blocked_low_pass_rate(self):
        m = generate_manifest(80.0, 0,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertFalse(m["release_approved"])
        self.assertIn("BLOCKED", m["summary"])

    def test_manifest_blocked_p0_issue(self):
        m = generate_manifest(100.0, 2,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertFalse(m["release_approved"])
        self.assertIn("BLOCKED", m["summary"])

    def test_worst_case_all_gates_fail(self):
        """
           Everything failing at once
        """
        m = generate_manifest(0.0, 5, [], False)
        self.assertFalse(m["release_approved"])
        self.assertIn("BLOCKED", m["summary"])

    def test_pass_rate_just_below_threshold_blocks(self):
        """
           94.9% is just below 95% - must block
        """
        results = evaluate_gates(94.9, 0,
            ["vehicle_simulator", "release_tool", "config"], True)
        self.assertFalse(results["test_pass_rate"]["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
