from datetime import datetime, timedelta, date

def parse_line(line):
    d, tz = line.strip().split()
    y, m, day = map(int, d.split('-'))
    sign = tz[3]
    hh = int(tz[4:6])
    mm = int(tz[7:9])
    off = timedelta(hours=hh, minutes=mm)
    local = datetime(y, m, day)
    utc = local - off if sign == '+' else local + off
    return y, m, day, sign, off, utc

def is_leap(y):
    return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)

def bday_in_year(bm, bd, y):
    if bm == 2 and bd == 29 and not is_leap(y):
        return date(y, 2, 28)
    return date(y, bm, bd)

by, bm, bd, bsign, boff, _ = parse_line(input())
cy, cm, cd, csign, coff, cur_utc = parse_line(input())

cand_date = bday_in_year(bm, bd, cy)
cand_local = datetime(cand_date.year, cand_date.month, cand_date.day)
cand_utc = cand_local - boff if bsign == '+' else cand_local + boff

if cand_utc < cur_utc:
    cand_date = bday_in_year(bm, bd, cy + 1)
    cand_local = datetime(cand_date.year, cand_date.month, cand_date.day)
    cand_utc = cand_local - boff if bsign == '+' else cand_local + boff

delta = (cand_utc - cur_utc).total_seconds()
if delta == 0:
    print(0)
else:
    s = int(delta)
    print((s + 86400 - 1) // 86400)