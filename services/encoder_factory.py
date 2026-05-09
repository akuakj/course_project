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


def create_encoder(encoder_type: str | None = None) -> BaseVoiceEncoder:

    if encoder_type is None:
        encoder_type = _get_encoder_type_from_config()

    # Неизвестный ID → fallback
    if encoder_type not in AVAILABLE_ENCODERS:
        print(f"[encoder_factory] Неизвестный энкодер '{encoder_type}', используем '{DEFAULT_ENCODER}'")
        encoder_type = DEFAULT_ENCODER

    if encoder_type == "resemblyzer":
        from services.resemblyzer_encoder import ResemblyzerEncoder
        return ResemblyzerEncoder()

    if encoder_type == "speechbrain":
        from services.speechbrain_encoder import SpeechBrainEncoder
        return SpeechBrainEncoder()

    raise ValueError(f"Энкодер '{encoder_type}' есть в реестре, но не реализован в фабрике.")


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