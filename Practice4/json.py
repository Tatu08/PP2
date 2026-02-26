import json
from pathlib import Path
from typing import Any

DATA_FILE = Path("sample-data.json")  

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def pretty_print(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))

def get_all_keys_if_dict(data: Any) -> list[str]:
    if isinstance(data, dict):
        return list(data.keys())
    return []

def find_values_by_key(data: Any, key: str) -> list[Any]:
    found = []

    def walk(x: Any):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == key:
                    found.append(v)
                walk(v)
        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(data)
    return found

def create_example_output(input_data: Any) -> dict:
    result = {
        "root_type": type(input_data).__name__,
        "root_keys": get_all_keys_if_dict(input_data),
        "how_many_items": len(input_data) if isinstance(input_data, list) else None,
        "extracted_names": find_values_by_key(input_data, "name"),
    }
    return result

if __name__ == "__main__":
    if not DATA_FILE.exists():
        print("ERROR: sample-data.json табылмады. Файл осы папкада тұрғанын тексер.")
    else:
        data = load_json(DATA_FILE)

        print("=== Loaded JSON (first look) ===")
        
        print("Root type:", type(data).__name__)
        print("Root keys:", get_all_keys_if_dict(data))

        names = find_values_by_key(data, "name")
        print("Found 'name' values count:", len(names))
        if names:
            print("First 5 names:", names[:5])

        out = create_example_output(data)
        save_json(Path("output.json"), out)
        print("Saved output.json ✅")