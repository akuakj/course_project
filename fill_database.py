import os
import sys
import numpy as np

# Добавляем пути для импорта
sys.path.append(os.path.dirname(__file__))

from core.voice_encoder import VoiceEncoderWrapper
from core.db_manager import TinyDBVoiceManager


def fill_database():
    """
    Заполнение базы данных людьми
    """
    print("=== ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ ===\n")

    # Инициализация компонентов
    encoder = VoiceEncoderWrapper()
    db_manager = TinyDBVoiceManager()

    # ДАННЫЕ ДЛЯ ЗАПОЛНЕНИЯ - редактируй по своему усмотрению
    people_data = [
        {
            "full_name": "Tyler Derden",
            "audio_files": [
                "records/dataset/tyler_derden/tayler1.wav",  # оригинальный
                "records/dataset/tyler_derden/tayler2.wav",  # еще одна фраза
                "records/dataset/tyler_derden/tayler3.wav",  # медленная речь
            ],
            "notes": "Почему все вокруг путают нас с тобой?",
            "photo": None
        },
    ]

    added_count = 0

    for person in people_data:
        full_name = person["full_name"]
        audio_files = person["audio_files"]
        notes = person.get("notes", "")
        photo = person.get("photo", None)

        print(f"👤 Обрабатываю: {full_name}")
        for af in audio_files:
            print(f"   📁 Аудио файл: {af}")
            if not os.path.exists(af):
                print(f"   ❌ Файл не найден: {af}")
                continue

        # Извлекаем эмбеддинги для каждого файла и усредняем
        embeddings = []
        for af in audio_files:
            emb = encoder.get_voice_embedding(af)
            if emb is not None:
                embeddings.append(emb)
        if not embeddings:
            print(f"   ❌ Не удалось извлечь эмбеддинг ни для одного файла")
            continue

        avg_embedding = np.mean(np.stack(embeddings), axis=0)

        # Добавляем в базу данных
        record_id = db_manager.add_voice_person(
            full_name=full_name,
            audio_files=audio_files,
            vector_data=avg_embedding,
            notes=notes
        )

        # Если есть фото, обновляем
        if photo:
            db_manager.update_person(record_id, {"photo": photo})

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
