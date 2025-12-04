import time
import json

def timestamp():
    return int(time.time())

def guardar_json(data, path="output/resultados.json"):
    import os
    if not os.path.exists("output"):
        os.makedirs("output")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
