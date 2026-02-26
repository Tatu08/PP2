from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo

def days_between(d1: str, d2: str) -> int:
    a = datetime.strptime(d1, "%Y-%m-%d").date()
    b = datetime.strptime(d2, "%Y-%m-%d").date()
    return abs((b - a).days)

def add_days(d: str, n: int) -> str:
    """
    "YYYY-MM-DD" + n күн => "YYYY-MM-DD"
    """
    dt = datetime.strptime(d, "%Y-%m-%d").date()
    return (dt + timedelta(days=n)).isoformat()

def format_now_in_almaty() -> str:
    now = datetime.now(ZoneInfo("Asia/Almaty"))
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

def parse_datetime(s: str) -> datetime:
    """
    "YYYY-MM-DD HH:MM" -> datetime
    """
    return datetime.strptime(s, "%Y-%m-%d %H:%M")

def is_weekend(d: str) -> bool:
    """
    Демалыс па? (сенбі/жексенбі)
    """
    dt = datetime.strptime(d, "%Y-%m-%d").date()
    return dt.weekday() >= 5  # 5=Sat, 6=Sun

if __name__ == "__main__":
    print("Days between 2026-02-01 and 2026-02-26:", days_between("2026-02-01", "2026-02-26"))
    print("Add 10 days to 2026-02-26:", add_days("2026-02-26", 10))
    print("Now in Almaty:", format_now_in_almaty())
    print("Parse datetime:", parse_datetime("2026-02-26 18:30"))
    print("2026-02-22 weekend?:", is_weekend("2026-02-22"))