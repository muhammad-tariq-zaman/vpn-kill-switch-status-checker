# vpn-kill-switch-status-checker

Check VPN kill-switch protection per workstation from a CSV: PROTECTED when the VPN is connected, the kill switch is on and the leak test is blocked; AT RISK when the kill switch is off; EXPOSED when the VPN is down or traffic leaked — worst first.

## How to run

```sh
python3 main.py workstations.csv
```

## Example output

```
PC-2: EXPOSED (VPN disconnected, kill switch off, leak test allowed)
PC-1: PROTECTED (VPN connected, kill switch on, leak test blocked)
1 workstation(s) exposed, 0 at risk.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
