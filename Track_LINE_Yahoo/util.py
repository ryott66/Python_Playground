from datetime import datetime

TIME_FMT = "%Y/%m/%d-%H:%M:%S"

def parse_time(s: str) -> datetime:
    return datetime.strptime(s, TIME_FMT)

def seconds_between(t2: datetime, t1: datetime) -> int:
    return int((t2 - t1).total_seconds())

def _ceil_div_pos(x: int, y: int) -> int:
    if x <= 0:
        return 0
    return (x + y - 1) // y

def minutes_ceil_from_seconds(sec: int) -> int:
    return _ceil_div_pos(sec, 60)

def seat_tick_count(sec: int) -> int:
    return _ceil_div_pos(sec, 600)

def shower_tick_count(sec: int) -> int:
    return _ceil_div_pos(sec, 900)
