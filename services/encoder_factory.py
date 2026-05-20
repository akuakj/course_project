from services.base_encoder import BaseVoiceEncoder

# Реестр доступных энкодеров.
# Ключ — строковый ID, по которому модель сохраняется в settings.json.
AVAILABLE_ENCODERS = {
    "resemblyzer": {
        "display_name": "Resemblyzer (GE2E)",
        "dim": 256,
        "description": "256-мерный вектор. Быстрый, стабильный на русской речи."
    },
    "speechbrain": {
        "display_name": "ECAPA-TDNN (SpeechBrain)",
        "dim": 192,
        "description": "192-мерный вектор. Точнее на коротких фрагментах, тяжелее."
    },
}

DEFAULT_ENCODER = "resemblyzer"
_encoder_instance = None


def create_encoder(encoder_type: str | None = None) -> BaseVoiceEncoder:
    global _encoder_instance

    if _encoder_instance is not None:
        return _encoder_instance
    
    if encoder_type is None:
        encoder_type = _get_encoder_type_from_config()

    # Неизвестный ID → fallback
    if encoder_type not in AVAILABLE_ENCODERS:
        print(f"[encoder_factory] Неизвестный энкодер '{encoder_type}', используем '{DEFAULT_ENCODER}'")
        encoder_type = DEFAULT_ENCODER

    if encoder_type == "resemblyzer":
        from services.resemblyzer_encoder import ResemblyzerEncoder
        _encoder_instance = ResemblyzerEncoder()

    elif encoder_type == "speechbrain":
        from services.speechbrain_encoder import SpeechBrainEncoder
        _encoder_instance = SpeechBrainEncoder()

    else:
        raise ValueError(f"Энкодер '{encoder_type}' есть в реестре, но не реализован в фабрике.")

    return _encoder_instance


def reset_encoder():
    # Сбрасываем синглтон при смене модели — вызывать перед перезапуском
    global _encoder_instance
    _encoder_instance = None

def get_available_encoders() -> dict:
    # возвращает реестр доступных энкодеров для UI
    return AVAILABLE_ENCODERS.copy()


def _get_encoder_type_from_config() -> str:
    # читает тип энкодера из settings.json, с fallback на DEFAULT_ENCODER
    try:
        from services.settings_manager import SettingsManager
        return SettingsManager().get("encoder_type", DEFAULT_ENCODER)
    except Exception:
        pass

    try:
        from services.settings_manager import load_settings
        settings = load_settings()
        return settings.get("encoder_type", DEFAULT_ENCODER)
    except Exception:
        pass

    return DEFAULT_ENCODER