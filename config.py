#  Конфигурация системы голосовой идентификации

# Пороги косинусного сходства для идентификации голоса.
# Resemblyzer возвращает значения от 0.0 до 1.0, где:
#   1.0 — идентичные голоса
#   0.0 — абсолютно разные голоса
# Значения подобраны экспериментально на основе тестовой выборки.

import os
from services.settings_manager import get_thresholds

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PHOTOS_DIR = os.path.join(BASE_DIR, "resources", "photos")
AUDIO_DIR = os.path.join(BASE_DIR, "records", "audioset")

# Создаём папки если не существуют
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

STRONG_THRESHOLD, WEAK_THRESHOLD, MIN_SIMILARITY = get_thresholds()

MIN_AUDIO_DURATION = 2.0

# ─────────────────────────────────────────────────────────────
#  Параметры сегментации аудио
# ─────────────────────────────────────────────────────────────

# Длина одного сегмента в секундах (рекомендуется 3.0)
SEGMENT_SEC = 3.0

# Процент перекрытия между сегментами (0.4 = 40%)
SEGMENT_OVERLAP = 0.4

# Минимальная громкость сегмента (тихие сегменты отфильтровываются)
SILENCE_THRESHOLD = 0.02

# Перцентиль для агрегации сходств по сегментам
# 85-й перцентиль устойчив к шумным/тихим сегментам
SIMILARITY_PERCENTILE = 85