import os
import sys

# Добавляем пути для импорта
sys.path.append(os.path.dirname(__file__))

from core.voice_encoder import VoiceEncoderWrapper
from core.db_manager import TinyDBVoiceManager


def fill_database():
    """
    Заполнение базы данных людьми
    """
    print("=== ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ ===\n")

    # Инициализируем компоненты
    encoder = VoiceEncoderWrapper()
    db_manager = TinyDBVoiceManager()

    # ДАННЫЕ ДЛЯ ЗАПОЛНЕНИЯ - ПРОСТО РЕДАКТИРУЙ ЭТОТ СПИСОК
    people_data = [
        {
            "full_name": "В. В. Путин",
            "audio_file": "records/dataset/putin2.wav",
            "notes": "Первый тестовый пользователь"
        },
        {
            "full_name": "Екатерина Альтуховна",
            "audio_file": "records/dataset/girl2.wav",  # ИСПРАВИЛ ОПЕЧАТКУ: было "recordы"
            "notes": "Второй тестовый пользователь"
        },
        # ДОБАВЛЯЙ ДАЛЬШЕ...
        # {
        #     "full_name": "Имя Фамилия",
        #     "audio_file": "путь/к/файлу.wav",
        #     "notes": "заметки"
        # },
    ]

    added_count = 0

    for person in people_data:
        full_name = person["full_name"]
        audio_file = person["audio_file"]
        notes = person.get("notes", "")

        print(f"👤 Обрабатываю: {full_name}")
        print(f"   📁 Аудио файл: {audio_file}")

        # Проверяем существование файла
        if not os.path.exists(audio_file):
            print(f"   ❌ Файл не найден: {audio_file}")
            continue

        # Извлекаем эмбеддинг
        embedding = encoder.get_voice_embedding(audio_file)

        if embedding is None:
            print(f"   ❌ Не удалось извлечь эмбеддинг")
            continue

        # Добавляем в базу данных
        record_id = db_manager.add_voice_person(
            full_name=full_name,
            audio_files=[audio_file],
            vector_data=embedding,
            notes=notes
        )

        if record_id:
            print(f"   ✅ Успешно добавлен")
            added_count += 1
        else:
            print(f"   ❌ Ошибка при добавлении")

    # Статистика
    stats = db_manager.get_statistics()

    print(f"\n=== РЕЗУЛЬТАТ ===")
    print(f"✅ Успешно добавлено: {added_count} человек")
    print(f"📊 Всего в базе: {stats['total_records']} записей")
    print(f"👥 Уникальных людей: {stats['unique_people']}")
    print(f"🎧 Всего аудиофайлов: {stats['total_audio_files']}")

    if added_count > 0:
        print("\n🎉 База данных заполнена! Теперь можно тестировать поиск.")
    else:
        print("\n💡 Создай аудио файлы и укажи правильные пути в people_data")


if __name__ == "__main__":
    fill_database()