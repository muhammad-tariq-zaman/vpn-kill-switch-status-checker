"""Check VPN kill-switch protection per workstation.

Usage: python3 main.py workstations.csv
CSV columns: workstation,vpn_connected,kill_switch_enabled,leak_test.
vpn_connected and kill_switch_enabled are yes/no.
leak_test is blocked or allowed (whether traffic leaked outside
the tunnel in a test).
- PROTECTED: VPN connected, kill switch on, leak test blocked.
- AT RISK: VPN connected and leak test blocked, but the kill
  switch is off — one dropped connection exposes traffic.
- EXPOSED: VPN not connected, or the leak test allowed traffic
  outside the tunnel.
Worst verdict first.
"""
import argparse, csv, sys

def _yes(value):
    return value.strip().lower() in ("yes", "y", "true", "1")

def check(rows):
    out = []
    for row in rows:
        vpn = _yes(row["vpn_connected"])
        kill = _yes(row["kill_switch_enabled"])
        leak_blocked = row["leak_test"].strip().lower() == "blocked"
        if not vpn or not leak_blocked:
            verdict = "EXPOSED"
        elif not kill:
            verdict = "AT RISK"
        else:
            verdict = "PROTECTED"
        out.append((row["workstation"].strip(), vpn, kill,
                    row["leak_test"].strip().lower(), verdict))
    rank = {"EXPOSED": 0, "AT RISK": 1, "PROTECTED": 2}
    return sorted(out, key=lambda r: (rank[r[4]], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = check(list(csv.DictReader(f)))
    for workstation, vpn, kill, leak, verdict in results:
        print(f"{workstation}: {verdict} (VPN {'connected' if vpn else 'disconnected'}, "
              f"kill switch {'on' if kill else 'off'}, leak test {leak})")
    print(f"{sum(1 for *_, v in results if v == 'EXPOSED')} workstation(s) exposed, "
          f"{sum(1 for *_, v in results if v == 'AT RISK')} at risk.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
