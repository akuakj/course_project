import os
import json

SETTINGS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "settings.json"
)

DEFAULT_SETTINGS = {
    "encoder_type": "resemblyzer",
    "thresholds": {
        "resemblyzer": {
            "strong": 0.88,
            "weak": 0.79,
            "min_similarity": 0.68
        },
        "speechbrain": {
            "strong": 0.55,
            "weak": 0.45,
            "min_similarity": 0.35
        }
    }
}


def load_settings() -> dict:
    """
    Читает settings.json.
    Если файл не существует или повреждён — возвращает DEFAULT_SETTINGS
    и сохраняет дефолт на диск.
    """
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Минимальная валидация: должны быть пороги
            if "thresholds" in data:
                # Дополняем недостающие ключи из дефолта (backward compat)
                for key, val in DEFAULT_SETTINGS.items():
                    if key not in data:
                        data[key] = val
                return data

        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    except Exception as e:
        print(f"[settings] Ошибка чтения настроек: {e} — используем дефолтные")
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict) -> bool:
    # Записывает весь словарь настроек в settings.json
    try:
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"[settings] Ошибка сохранения настроек: {e}")
        return False


def get_thresholds() -> tuple[float, float, float]:
    settings = load_settings()
    encoder = settings.get("encoder_type", "resemblyzer")
    
    all_thresholds = settings.get("thresholds", DEFAULT_SETTINGS["thresholds"])
    
    # Если старый формат (без разбивки по моделям) — мигрируем
    if "strong" in all_thresholds:
        t = all_thresholds
    else:
        t = all_thresholds.get(encoder, DEFAULT_SETTINGS["thresholds"][encoder])
    
    return (
        float(t.get("strong")),
        float(t.get("weak")),
        float(t.get("min_similarity"))
    )


def save_thresholds(strong: float, weak: float, min_similarity: float) -> bool:
    settings = load_settings()
    encoder = settings.get("encoder_type", "resemblyzer")
    
    if "strong" in settings.get("thresholds", {}):
        settings["thresholds"] = DEFAULT_SETTINGS["thresholds"].copy()
    
    settings["thresholds"][encoder] = {
        "strong": round(strong, 2),
        "weak": round(weak, 2),
        "min_similarity": round(min_similarity, 2)
    }
    return save_settings(settings)


def get_encoder_type() -> str:
    # Возвращает ID активного энкодера
    settings = load_settings()
    return settings.get("encoder_type", DEFAULT_SETTINGS["encoder_type"])


def save_encoder_type(encoder_type: str) -> bool:
    # Сохраняет выбранный энкодер в настройки
    settings = load_settings()
    settings["encoder_type"] = encoder_type
    return save_settings(settings)