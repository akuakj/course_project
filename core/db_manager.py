import os
from datetime import datetime
from tinydb import TinyDB, Query
import uuid
import numpy as np
from config import BASE_DIR



def to_relative_path(absolute_path):
    try:
        return os.path.relpath(absolute_path, BASE_DIR)
    except ValueError:
        return absolute_path

def to_absolute_path(relative_path):
    if relative_path and not os.path.isabs(relative_path):
        return os.path.join(BASE_DIR, relative_path)
    return relative_path

class TinyDBVoiceManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(BASE_DIR, "data", "voice_database.json")

        # Создаем папку data если её нет
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db = TinyDB(db_path)
        self.voice_table = self.db.table('voices')
        self.query = Query()

        print(f"База данных загружена: {db_path}")

    def _normalize_person(self, person):
        if person.get('photo'):
            person['photo'] = to_absolute_path(person['photo'])
        if person.get('audio_files'):
            person['audio_files'] = [to_absolute_path(f) for f in person['audio_files']]
        return person

    def add_voice_person(self, full_name, audio_files, vector_data, notes=None, date_of_birth=None, photo=None):
        try:
            record_id = str(uuid.uuid4())

            if isinstance(vector_data, np.ndarray):
                vector_data = vector_data.tolist()

            doc = {
                'id': record_id,
                'full_name': full_name,
                'audio_files': [to_relative_path(f) for f in audio_files],
                'created_at': datetime.now().isoformat(),
                'photo': to_relative_path(photo) if photo else None,
                'vector_data': vector_data,
                'notes': notes or "",
                'date_of_birth': date_of_birth or ""  # ← НОВОЕ ПОЛЕ
            }

            self.voice_table.insert(doc)
            print(f"✅ Добавлен: {full_name}")
            return record_id
        except Exception as e:
            print(f"❌ Ошибка добавления {full_name}: {e}")
            return None

    def get_person_by_id(self, person_id):
        results = self.voice_table.search(self.query.id == person_id)
        return self._normalize_person(results[0]) if results else None

    def update_person(self, person_id, updated_data):
        try:
            if updated_data.get('photo'):
                updated_data['photo'] = to_relative_path(updated_data['photo'])
            if updated_data.get('audio_files'):
                updated_data['audio_files'] = [to_relative_path(f) for f in updated_data['audio_files']]

            self.voice_table.update(updated_data, self.query.id == person_id)
            print(f"✅ Обновлены данные человека {person_id}")
            return True
        except Exception as e:
            print(f"❌ Ошибка обновления человека: {e}")
            return False

    def update_person_photo(self, person_id, photo_path):
        """Обновляет путь к фото в записи пользователя"""
        try:
            # TinyDB ищет запись по полю 'id'
            relative_path = to_relative_path(photo_path)
            self.voice_table.update({'photo': relative_path}, self.query.id == person_id)
            return True
        except Exception as e:
            print(f"Ошибка обновления фото: {e}")
            return False

    def get_person_by_name(self, full_name):
        """
        Поиск человека по ФИО
        """
        return self.voice_table.search(self.query.full_name == full_name)

    def get_all_people(self):
        """
        Получение всех записей из базы данных
        """
        return [self._normalize_person(p) for p in self.voice_table.all()]

    def search_similar_voices(self, query_vector, top_k=5, similarity_threshold=0.7):
        """
        Поиск похожих голосов по вектору
        """
        if isinstance(query_vector, np.ndarray):
            query_vector = query_vector.tolist()

        all_people = self.get_all_people()
        similarities = []

        for person in all_people:
            person_vector = person['vector_data']
            similarity = self._cosine_similarity(query_vector, person_vector)

            if similarity >= similarity_threshold:
                similarities.append({
                    'person': person,
                    'similarity': similarity
                })

        # Сортируем по убыванию сходства
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        return similarities[:top_k]

    def _cosine_similarity(self, vec1, vec2):
        """
        Вычисление косинусного сходства между двумя векторами
        """
        if isinstance(vec1, list):
            vec1 = np.array(vec1)
        if isinstance(vec2, list):
            vec2 = np.array(vec2)

        # Нормализуем векторы
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(np.dot(vec1, vec2) / (norm1 * norm2))

    def delete_person(self, person_id):
        """
        Удаление человека по нашему UUID
        """
        try:
            self.voice_table.remove(self.query.id == person_id)
            print(f"✅ Удален человек с ID: {person_id}")
            return True
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
            return False

    def get_statistics(self):
        """
        Получение статистики базы данных
        """
        all_people = self.get_all_people()

        if not all_people:
            return {
                'total_records': 0,
                'unique_people': 0,
                'total_audio_files': 0,
                'last_update': 'Never'
            }

        return {
            'total_records': len(all_people),
            'unique_people': len(set(person['full_name'] for person in all_people)),
            'total_audio_files': sum(len(person['audio_files']) for person in all_people),
            'last_update': max((person['created_at'] for person in all_people), default='Never')
        }

    def close(self):
        """Закрытие соединения с БД"""
        self.db.close()