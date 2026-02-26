import json
import re

token_re = re.compile(r'([^. \[\]]+)|\[(\d+)\]')

def resolve(obj, path):
    cur = obj
    for m in token_re.finditer(path):
        key = m.group(1)
        idx = m.group(2)

        if key is not None:
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                return None, False
        else:
            i = int(idx)
            if isinstance(cur, list) and 0 <= i < len(cur):
                cur = cur[i]
            else:
                return None, False
    return cur, True

J = json.loads(input().strip())
q = int(input().strip())

for _ in range(q):
    path = input().strip()
    val, ok = resolve(J, path)
    if not ok:
        print("NOT_FOUND")
    else:
        print(json.dumps(val, separators=(',', ':'), sort_keys=True))