import os 
import json

SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "settings.json")

DEFAULT_SETTINGS = {
    "thresholds": {
        "strong": 0.88,
        "weak": 0.79,
        "min_similarity": 0.68
    }
}

def load_settings() -> dict:
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding = "utf-8") as f:
                data = json.load(f)
            
            if "thresholds" in data:
                return data
            
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    except Exception as e:
        print(f"[settings] Ошибка чтения настроек: {e} - используем дефолтные настройки")
        return DEFAULT_SETTINGS
    
def save_settings(settings: dict) -> bool:
    try:
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, "w", encoding = "utf-8") as f:
            json.dump(settings, f, ensure_ascii = False, indent = 4)
        return True
    except Exception as e:
        print(f"[settings] Ошибка сохранения настроек: {e}")
        return False
    
def get_thresholds() -> tuple[float, float, float]:
    settings = load_settings()
    t = settings.get("thresholds", DEFAULT_SETTINGS["thresholds"])
    return (
        float(t.get("strong", DEFAULT_SETTINGS["thresholds"]["strong"])),
        float(t.get("weak", DEFAULT_SETTINGS["thresholds"]["weak"])),
        float(t.get("min_similarity", DEFAULT_SETTINGS["thresholds"]["min_similarity"]))
    )

def save_thresholds(strong: float, weak: float, min_similarity: float) -> bool:
    settings = load_settings()
    settings["thresholds"] = {
        "strong": round(strong, 2),
        "weak": round(weak, 2),
        "min_similarity": round(min_similarity, 2)
    }
    return save_settings(settings)
