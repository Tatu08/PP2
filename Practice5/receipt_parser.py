import re
import json
from pathlib import Path

def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def to_float(num_str: str) -> float:
    # supports: "1 234,56" or "1234.56"
    s = num_str.replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

def parse_receipt(text: str) -> dict:
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    full = "\n".join(lines)

    # 1) Store name (take first non-empty, non-junk line)
    junk = re.compile(r"^(касс|чек|фиск|инн|бин|ккм|qr|thank|спасибо)", re.I)
    store_name = ""
    for l in lines[:10]:
        if not junk.search(l):
            store_name = clean(l)
            break

    # 2) Date + time
    # Examples: 01.02.2026 14:33, 2026-02-01 14:33, 01/02/2026 14:33:20
    dt_patterns = [
        r"(?P<date>\d{2}[./-]\d{2}[./-]\d{4})\s+(?P<time>\d{2}:\d{2}(?::\d{2})?)",
        r"(?P<date>\d{4}[./-]\d{2}[./-]\d{2})\s+(?P<time>\d{2}:\d{2}(?::\d{2})?)",
    ]
    date, time = None, None
    for pat in dt_patterns:
        m = re.search(pat, full)
        if m:
            date, time = m.group("date"), m.group("time")
            break

    # 3) Totals
    # TOTAL / ИТОГО / К ОПЛАТЕ, etc.
    total = None
    total_match = re.search(
        r"(?:ИТОГО|К\s*ОПЛАТЕ|ИТОГ|TOTAL|SUM)\s*[:\-]?\s*(?P<amt>\d[\d\s]*[.,]\d{2}|\d[\d\s]*)",
        full,
        re.I
    )
    if total_match:
        total = to_float(total_match.group("amt"))

    # VAT / НДС
    vat = None
    vat_match = re.search(
        r"(?:НДС|VAT)\s*[:\-]?\s*(?P<amt>\d[\d\s]*[.,]\d{2}|\d[\d\s]*)",
        full,
        re.I
    )
    if vat_match:
        vat = to_float(vat_match.group("amt"))

    # 4) Payment method
    pay_method = None
    # Look for words like: CARD / CASH / НАЛИЧ / КАРТА
    if re.search(r"(?:CASH|НАЛИЧ|НАЛ\.)", full, re.I):
        pay_method = "cash"
    if re.search(r"(?:CARD|КАРТ|БАНК\.?\s*КАРТ)", full, re.I):
        pay_method = "card"
    if re.search(r"(?:QR|KASPI\s*QR|APPLE\s*PAY|GOOGLE\s*PAY)", full, re.I):
        pay_method = "cashless/qr"

    # 5) Items parsing (best-effort)
    # Typical item lines:
    # "Milk 2 x 450.00 900.00"
    # "Bread 1 250,00"
    items = []
    item_pat = re.compile(
        r"""
        ^(?P<name>[^\d]{2,}?)\s+
        (?:
            (?P<qty>\d+(?:[.,]\d+)?)\s*[x×*]\s*(?P<price>\d[\d\s]*[.,]\d{2}|\d[\d\s]*)\s+(?P<sum>\d[\d\s]*[.,]\d{2}|\d[\d\s]*)
          |
            (?P<qty2>\d+(?:[.,]\d+)?)\s+(?P<sum2>\d[\d\s]*[.,]\d{2}|\d[\d\s]*)
        )
        $
        """,
        re.VERBOSE
    )

    stop_words = re.compile(r"^(итого|к оплате|сдача|nds|vat|налич|карта|total|sum)$", re.I)

    for l in lines:
        s = clean(l)
        if stop_words.search(s.lower()):
            continue

        m = item_pat.match(s)
        if not m:
            continue

        name = clean(m.group("name"))
        if len(name) < 2:
            continue

        if m.group("qty") and m.group("price") and m.group("sum"):
            qty = float(m.group("qty").replace(",", "."))
            price = to_float(m.group("price"))
            line_sum = to_float(m.group("sum"))
        else:
            qty = float((m.group("qty2") or "1").replace(",", "."))
            price = None
            line_sum = to_float(m.group("sum2"))

        items.append({
            "name": name,
            "qty": qty,
            "price": price,
            "sum": line_sum
        })

    # 6) If total missing, try compute from items
    if total is None and items:
        total = round(sum(i["sum"] for i in items), 2)

    return {
        "store_name": store_name or None,
        "date": date,
        "time": time,
        "items": items,
        "total": total,
        "vat": vat,
        "payment_method": pay_method
    }

def main():
    raw_path = Path("raw.txt")
    if not raw_path.exists():
        print("raw.txt табылмады. Сол папкаға raw.txt салыңыз.")
        return

    text = raw_path.read_text(encoding="utf-8", errors="ignore")
    data = parse_receipt(text)

    # Pretty JSON output
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()