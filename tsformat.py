#!/usr/bin/env python3
"""tsformat - Timestamp converter (unix, ISO, human, relative). Zero deps."""
import sys, time, re, calendar
from datetime import datetime, timezone, timedelta

def now_ts():
    return time.time()

def parse_ts(s):
    s = s.strip()
    # Unix timestamp (seconds or milliseconds)
    if re.match(r'^\d{10}$', s): return float(s)
    if re.match(r'^\d{13}$', s): return float(s) / 1000
    if re.match(r'^\d+\.\d+$', s): return float(s)
    # ISO 8601
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try: return calendar.timegm(time.strptime(s[:19], fmt[:len(s)+2].replace("%z","")))
        except: pass
    # Relative
    m = re.match(r'^(\d+)\s*(s|sec|m|min|h|hr|d|day|w|week)s?\s*(ago|from now|later)?$', s, re.I)
    if m:
        val = int(m.group(1))
        unit = m.group(2)[0].lower()
        direction = -1 if m.group(3) and "ago" in m.group(3) else 1
        multiplier = {"s":1,"m":60,"h":3600,"d":86400,"w":604800}[unit]
        return now_ts() + direction * val * multiplier
    raise ValueError(f"Can't parse: {s}")

def relative(ts):
    diff = abs(now_ts() - ts)
    if diff < 60: return f"{int(diff)}s"
    if diff < 3600: return f"{int(diff/60)}m"
    if diff < 86400: return f"{int(diff/3600)}h"
    if diff < 604800: return f"{int(diff/86400)}d"
    return f"{int(diff/604800)}w"

def fmt_all(ts):
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    local = datetime.fromtimestamp(ts)
    ago = now_ts() - ts
    direction = "ago" if ago > 0 else "from now"
    
    print(f"  Unix:     {int(ts)}")
    print(f"  Unix ms:  {int(ts*1000)}")
    print(f"  ISO UTC:  {dt.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"  Local:    {local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  Human:    {local.strftime('%A, %B %d, %Y %I:%M %p')}")
    print(f"  Relative: {relative(ts)} {direction}")

def cmd_now(args):
    if "--unix" in args: print(int(now_ts()))
    elif "--ms" in args: print(int(now_ts()*1000))
    elif "--iso" in args: print(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    else: fmt_all(now_ts())

def cmd_convert(args):
    if not args: print("Usage: tsformat convert <timestamp|date|relative>"); sys.exit(1)
    try:
        ts = parse_ts(" ".join(args))
        fmt_all(ts)
    except ValueError as e:
        print(f"❌ {e}"); sys.exit(1)

def cmd_diff(args):
    if len(args) < 2: print("Usage: tsformat diff <ts1> <ts2>"); sys.exit(1)
    t1 = parse_ts(args[0])
    t2 = parse_ts(args[1])
    diff = abs(t2 - t1)
    days = int(diff // 86400)
    hours = int((diff % 86400) // 3600)
    mins = int((diff % 3600) // 60)
    secs = int(diff % 60)
    print(f"  Difference: {days}d {hours}h {mins}m {secs}s ({int(diff)} seconds)")

CMDS = {"now":cmd_now,"n":cmd_now,"convert":cmd_convert,"c":cmd_convert,"diff":cmd_diff,"d":cmd_diff}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h","--help"):
        print("tsformat - Timestamp converter")
        print("Commands: now [--unix|--ms|--iso], convert <input>, diff <ts1> <ts2>")
        print("Input: unix, ISO 8601, relative (5m ago, 2h from now)")
        sys.exit(0)
    cmd = args[0]
    if cmd in CMDS: CMDS[cmd](args[1:])
    else: cmd_convert(args)
