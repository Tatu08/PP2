import json

MISSING = object()

def to_compact_json(v):
    if v is MISSING:
        return "<missing>"
    return json.dumps(v, separators=(',', ':'), sort_keys=True)

def diff(a, b, path, out):
    # Екеуі де dict болса — ішіне кіреміз
    if isinstance(a, dict) and isinstance(b, dict):
        keys = sorted(set(a.keys()) | set(b.keys()))
        for k in keys:
            av = a.get(k, MISSING)
            bv = b.get(k, MISSING)
            new_path = f"{path}.{k}" if path else k
            diff(av, bv, new_path, out)
        return

    # Егер біреуі missing болса немесе тип/мән әртүрлі болса — айырмашылық
    if a is MISSING or b is MISSING or a != b:
        out.append((path, f"{path} : {to_compact_json(a)} -> {to_compact_json(b)}"))

a = json.loads(input().strip())
b = json.loads(input().strip())

out = []
diff(a, b, "", out)

if not out:
    print("No differences")
else:
    out.sort(key=lambda x: x[0])
    for _, line in out:
        print(line)