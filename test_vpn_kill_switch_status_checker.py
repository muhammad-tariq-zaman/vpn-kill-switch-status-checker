import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import check

def row(ws, vpn, kill, leak):
    return {"workstation": ws, "vpn_connected": vpn,
            "kill_switch_enabled": kill, "leak_test": leak}

class TestKillSwitch(unittest.TestCase):
    def test_protected(self):
        self.assertEqual(check([row("PC-1", "yes", "yes", "blocked")])[0][4], "PROTECTED")
    def test_kill_switch_off_is_at_risk(self):
        self.assertEqual(check([row("PC-1", "yes", "no", "blocked")])[0][4], "AT RISK")
    def test_vpn_disconnected_is_exposed(self):
        self.assertEqual(check([row("PC-1", "no", "yes", "blocked")])[0][4], "EXPOSED")
    def test_leak_allowed_is_exposed(self):
        self.assertEqual(check([row("PC-1", "yes", "yes", "allowed")])[0][4], "EXPOSED")
    def test_yes_values_case_insensitive(self):
        self.assertEqual(check([row("PC-1", "YES", "True", "BLOCKED")])[0][4], "PROTECTED")
    def test_exposed_first(self):
        r = check([row("PC-2", "yes", "yes", "blocked"),
                   row("PC-1", "no", "no", "allowed")])
        self.assertEqual(r[0][0], "PC-1")
    def test_empty_input(self):
        self.assertEqual(check([]), [])
