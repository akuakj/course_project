# Voice Identification System
Десктопное приложение для идентификации личности по голосовому биометрическому признаку.

## Технологии
- Python 3.13
- PySide6 — графический интерфейс
- Resemblyzer (GE2E) — 256-мерные голосовые эмбеддинги
- ECAPA-TDNN (SpeechBrain) — 192-мерные голосовые эмбеддинги
- TinyDB — база данных
- Архитектура MVC

## Возможности
- Запись голоса в реальном времени через микрофон
- Загрузка аудиофайлов (WAV, MP3, FLAC)
- Идентификация личности по голосу
- Управление базой голосовых профилей
- Визуализация матрицы межличностного сходства
- Переключение между моделями энкодера

## Установка
```bash
git clone https://github.com/your/repo.git
cd voice-identification
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск
```bash
python main.py
```

> **Windows:** для работы модели SpeechBrain включи 
> Включить "Режим разработчика" в Параметрах Windows