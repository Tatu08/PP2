from datetime import datetime, timedelta

def to_utc(line):
    d, t, tz = line.strip().split()
    dt = datetime.strptime(d + " " + t, "%Y-%m-%d %H:%M:%S")
    sign = tz[3]
    hh = int(tz[4:6])
    mm = int(tz[7:9])
    off = timedelta(hours=hh, minutes=mm)
    return dt - off if sign == '+' else dt + off

start = to_utc(input())
end = to_utc(input())

print(int((end - start).total_seconds()))