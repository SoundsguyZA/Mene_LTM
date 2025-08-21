from datetime import datetime, timezone
def time_decay(created_at, half_life_days: float)->float:
    if not created_at: return 1.0
    now=datetime.now(timezone.utc)
    dt=(now - created_at).total_seconds()
    half_life=half_life_days*86400.0
    if half_life<=0: return 1.0
    return pow(0.5, dt/half_life)
