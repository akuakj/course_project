import os
from datetime import datetime
from tinydb import TinyDB, Query
from tinydb.table import Document
import uuid
import numpy as np


class TinyDBVoiceManager:
    def __init__(self, db_path="data/voice_database.json"):
        """
        Инициализация менеджера TinyDB

        Args:
            db_path: путь к файлу базы данных
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

        Args:
            full_name: ФИО человека
            audio_files: список путей к аудиофайлам
            vector_data: вектор эмбеддинга (256 float32)
            notes: заметки (опционально)

        Returns:
            str: ID добавленной записи
        """
        try:
            # Генерируем уникальный ID
            record_id = str(uuid.uuid4())

            # Преобразуем numpy array в список для JSON
            if isinstance(vector_data, np.ndarray):
                vector_data = vector_data.tolist()

            # Создаем документ
            doc = Document({
                'id': record_id,
                'full_name': full_name,
                'audio_files': audio_files,
                'created_at': datetime.now().isoformat(),
                'vector_data': vector_data,
                'notes': notes or ""
            }, doc_id=record_id)

            # Добавляем в базу
            self.voice_table.insert(doc)

            print(f"✅ Добавлен: {full_name} (ID: {record_id})")
            return record_id

        except Exception as e:
            print(f"❌ Ошибка добавления {full_name}: {e}")
            return None

    def get_person_by_id(self, person_id):
        """
        Получение человека по ID

        Args:
            person_id: ID записи

        Returns:
            dict: данные человека или None
        """
        result = self.voice_table.get(doc_id=person_id)
        return result

    def get_person_by_name(self, full_name):
        """
        Поиск человека по ФИО

        Args:
            full_name: ФИО для поиска

        Returns:
            list: список найденных записей
        """
        results = self.voice_table.search(self.query.full_name == full_name)
        return results

    def get_all_people(self):
        """
        Получение всех записей из базы данных

        Returns:
            list: список всех людей
        """
        return self.voice_table.all()

    def search_similar_voices(self, query_vector, top_k=5, similarity_threshold=0.7):
        """
        Поиск похожих голосов по вектору

        Args:
            query_vector: вектор для поиска
            top_k: количество результатов
            similarity_threshold: порог сходства

        Returns:
            list: список совпадений [{'person': dict, 'similarity': float}]
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
        Удаление человека по ID

        Args:
            person_id: ID записи для удаления

        Returns:
            bool: успех операции
        """
        try:
            self.voice_table.remove(doc_ids=[person_id])
            print(f"✅ Удален человек с ID: {person_id}")
            return True
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
            return False

    def get_statistics(self):
        """
        Получение статистики базы данных

        Returns:
            dict: статистика
        """
        all_people = self.get_all_people()

        return {
            'total_records': len(all_people),
            'unique_people': len(set(person['full_name'] for person in all_people)),
            'total_audio_files': sum(len(person['audio_files']) for person in all_people),
            'last_update': max((person['created_at'] for person in all_people), default='Never')
        }

    def close(self):
        """Закрытие соединения с БД"""
        self.db.close()
        self.db.close()