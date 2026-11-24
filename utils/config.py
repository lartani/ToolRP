from pathlib import Path

versions = {
    "26.3": {"pack_format": 97, "syntax": "new"},
    "26.2": {"pack_format": 88, "syntax": "new"},
    "26.1": {"pack_format": 84, "syntax": "new"},
    "1.21.11": {"pack_format": 75, "syntax": "nbt"},
}

PROJECT_DIR = Path(__file__).resolve().parents[1]
RESOURCE_PACKS_DIR = PROJECT_DIR / "resource_packs"
EXPORTED_PACKS_DIR = PROJECT_DIR / "exported_packs"


def make_mcmeta_template(pack_format: int):
    return {"pack": {"description": "Created by ToolRP", "pack_format": pack_format}}


def make_item_template(pack_format: int, item: str):
    return {
        "model": {
            "type": "minecraft:range_dispatch",
            "property": "minecraft:custom_model_data",
            "index": 0,
            "fallback": {"type": "minecraft:model", "model": f"minecraft:item/{item}"},
            "entries": [],
        }
    }


def make_entry(model_path: str, threshold: int):
    return {
        "threshold": threshold,
        "model": {"type": "minecraft:model", "model": model_path},
    }
