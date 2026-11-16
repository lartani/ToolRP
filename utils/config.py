versions = {"26.3": {"pack_format": 97, "syntax": "new"},
           "26.2": {"pack_format": 88, "syntax": "new"},
           "26.1": {"pack_format": 84, "syntax": "new"},
           "1.21.11": {"pack_format": 75, "syntax": "nbt"},}


MCMETA_TEMPLATE = '''"pack": {
    "description": "Created by ToolRP",
    "pack_format": <pack_format>
}'''

NEW_TEMPLATE = {
  "model": {
    "type": "minecraft:range_dispatch",
    "property": "minecraft:custom_model_data",
    "index": 0,
    "fallback": {
      "type": "minecraft:model",
      "model": "minecraft:item/paper"
    },
    "entries": [

    ]
  }
}

def make_entry(model_path: str, threshold: int):
    return {
        "threshold": threshold,
        "model": {
            "type": "minecraft:model",
            "model": model_path
        }
    }