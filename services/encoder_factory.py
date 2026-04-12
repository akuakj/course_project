from services.base_encoder import BaseVoiceEncoder

AVAILABLE_ENCODERS = {
    "resemblyzer": {
        "display_name": "Resemblyzer (GE2E)",
        "dim": 256,
        "description": "256-мерный вектор. Быстрый, стабильный на русской речи."
    },
}

DEFAULT_ENCODER = "resemblyzer"


def create_encoder(encoder_type: str | None = None) -> BaseVoiceEncoder:

    if encoder_type is None:
        encoder_type = _get_encoder_type_from_config()

    # Если в настройках сохранён несуществующий энкодер — fallback на дефолт
    if encoder_type not in AVAILABLE_ENCODERS:
        print(f"[encoder_factory] Неизвестный энкодер '{encoder_type}', используем '{DEFAULT_ENCODER}'")
        encoder_type = DEFAULT_ENCODER

    if encoder_type == "resemblyzer":
        from services.resemblyzer_encoder import ResemblyzerEncoder
        return ResemblyzerEncoder()

    raise ValueError(f"Энкодер '{encoder_type}' есть в реестре, но не реализован в фабрике.")


def get_available_encoders() -> dict:
    """Возвращает реестр доступных энкодеров для UI."""
    return AVAILABLE_ENCODERS.copy()


def _get_encoder_type_from_config() -> str:
    """Читает тип энкодера из настроек, с fallback на дефолт."""
    try:
        from services.settings_manager import SettingsManager
        return SettingsManager().get("encoder_type", DEFAULT_ENCODER)
    except Exception:
        pass

    try:
        import config
        return getattr(config, "ENCODER_TYPE", DEFAULT_ENCODER)
    except Exception:
        pass

    return DEFAULT_ENCODER