import os
from datetime import datetime
from tinydb import TinyDB, Query
import uuid
import numpy as np


class TinyDBVoiceManager:
    def __init__(self, db_path="data/voice_database.json"):
        """
        Инициализация менеджера TinyDB
        """
        # Создаем папку data если её нет
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db = TinyDB(db_path)
        self.voice_table = self.db.table('voices')
        self.query = Query()

        print(f"База данных загружена: {db_path}")

    def add_voice_person(self, full_name, audio_files, vector_data, notes=None):
        """
        Добавление человека в базу данных
        """
        try:
            # Генерируем уникальный ID
            record_id = str(uuid.uuid4())

            # Преобразуем numpy array в список для JSON
            if isinstance(vector_data, np.ndarray):
                vector_data = vector_data.tolist()

            # Создаем документ с нашим кастомным ID
            doc = {
                'id': record_id,
                'full_name': full_name,
                'audio_files': audio_files,
                'created_at': datetime.now().isoformat(),
                'vector_data': vector_data,
                'notes': notes or ""
            }

            # Добавляем в базу (TinyDB сам сгенерирует числовой doc_id)
            self.voice_table.insert(doc)

            print(f"✅ Добавлен: {full_name} (ID: {record_id})")
            return record_id

        except Exception as e:
            print(f"❌ Ошибка добавления {full_name}: {e}")
            return None

    def get_person_by_id(self, person_id):
        """
        Получение человека по нашему UUID
        """
        results = self.voice_table.search(self.query.id == person_id)
        return results[0] if results else None

    def get_person_by_name(self, full_name):
        """
        Поиск человека по ФИО
        """
        return self.voice_table.search(self.query.full_name == full_name)

    def get_all_people(self):
        """
        Получение всех записей из базы данных
        """
        return self.voice_table.all()

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