from datetime import datetime, timedelta

def to_utc(line: str) -> datetime:
    date_part, tz = line.strip().split()      # "2025-01-01", "UTC+03:00"
    local_midnight = datetime.strptime(date_part, "%Y-%m-%d")

    sign = tz[3]                              # '+' немесе '-'
    hh = int(tz[4:6])
    mm = int(tz[7:9])
    offset = timedelta(hours=hh, minutes=mm)

    # local midnight -> UTC
    if sign == '+':
        return local_midnight - offset
    else:
        return local_midnight + offset

t1 = to_utc(input())
t2 = to_utc(input())

delta_seconds = abs((t1 - t2).total_seconds())
print(int(delta_seconds // 86400))