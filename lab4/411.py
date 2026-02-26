import json

def apply_patch(source, patch):
    # егер patch dict болмаса, source толық ауысады
    if not isinstance(patch, dict):
        return patch

    # source dict болмаса, dict қылып аламыз (merge үшін)
    if not isinstance(source, dict):
        source = {}

    for k, pv in patch.items():
        if pv is None:
            # null -> key өшіру
            source.pop(k, None)
        else:
            sv = source.get(k)
            if isinstance(sv, dict) and isinstance(pv, dict):
                source[k] = apply_patch(sv, pv)
            else:
                source[k] = pv
    return source

source = json.loads(input().strip())
patch = json.loads(input().strip())

result = apply_patch(source, patch)

print(json.dumps(result, separators=(',', ':'), sort_keys=True))