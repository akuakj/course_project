import time
import numpy as np
import soundfile as sf
from core.voice_encoder import VoiceEncoderWrapper
from core.db_manager import TinyDBVoiceManager


class VoiceAnalysisService:

    def __init__(self):
        self.encoder = VoiceEncoderWrapper()
        self.db = TinyDBVoiceManager()

        # Пороги (их потом можно тюнить)
        self.STRONG_THRESHOLD = 0.72  # было 0.85
        self.WEAK_THRESHOLD = 0.65  # было 0.75
        self.MIN_SIMILARITY = 0.50  # новый: минимальный порог

    def analyze(self, audio_file):
        start_time = time.time()
        try:
            audio, sr = sf.read(audio_file)
            if audio.ndim > 1:
                audio = audio.mean(axis=1)
        except Exception as e:
            return {"status": "error", "message": f"Не удалось прочитать аудио: {e}"}

        # УЛУЧШЕННАЯ сегментация с перекрытием
        segments = self._split_audio_with_overlap(audio, sr, segment_sec=3.0, overlap=0.4)
        if not segments:
            return self._error("Аудио слишком короткое")

        # Извлекаем эмбеддинги для ВСЕХ сегментов
        embeddings = []
        for segment in segments:
            emb = self.encoder.get_embedding_from_audio(segment, sr)
            if emb is not None:
                embeddings.append(emb)

        if not embeddings:
            return self._error("Не удалось извлечь голос")

        print(f"📊 Извлечено {len(embeddings)} сегментов")

        # УЛУЧШЕННОЕ сравнение с базой
        similarities = self._advanced_compare_with_db(embeddings)

        if not similarities:
            return self._not_found(len(embeddings), start_time)

        best_person_name, best_score = max(similarities.items(), key=lambda x: x[1])
        confidence = self._confidence(best_score)

        # Формируем топ-5 совпадений
        top_matches = sorted(
            [(name, score) for name, score in similarities.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            "status": "ok" if best_score >= self.WEAK_THRESHOLD else "not_found",
            "best_match": {
                "person": {"full_name": best_person_name},
                "similarity": round(best_score, 3),
                "confidence": confidence
            },
            "top_matches": top_matches,
            "segments": len(embeddings),
            "analysis_time": round(time.time() - start_time, 2)
        }

    # ================= ВСПОМОГАТЕЛЬНО =================

    def _split_audio(self, audio, sr, segment_sec=2.0):
        step = int(sr * segment_sec)
        return [audio[i:i+step] for i in range(0, len(audio), step) if len(audio[i:i+step]) > step // 2]

    def _compare_with_db(self, embeddings):
        people = self.db.get_all_people()
        results = {}
        for person in people:
            person_vec = np.array(person["vector_data"])
            sims = [self._cosine_similarity(emb, person_vec) for emb in embeddings]
            results[person["full_name"]] = float(np.mean(sims))
        return results

    def _split_audio_with_overlap(self, audio, sr, segment_sec=3.0, overlap=0.4):
        """
        Сегментация с перекрытием для лучшего охвата голоса
        segment_sec: длина сегмента в секундах (рекомендуется 3.0)
        overlap: процент перекрытия (0.4 = 40%)
        """
        segment_samples = int(sr * segment_sec)
        step_samples = int(segment_samples * (1 - overlap))

        segments = []

        # Если аудио короче сегмента, возвращаем целиком
        if len(audio) <= segment_samples:
            return [audio] if len(audio) > sr * 1.0 else []  # минимум 1 секунда

        for i in range(0, len(audio) - segment_samples + 1, step_samples):
            segment = audio[i:i + segment_samples]

            # Фильтруем слишком тихие сегменты
            if np.max(np.abs(segment)) > 0.02:  # порог громкости
                segments.append(segment)

        return segments if segments else [audio[:segment_samples]]

    def _advanced_compare_with_db(self, embeddings):
        """
        Улучшенное сравнение с учетом нескольких сегментов
        """
        people = self.db.get_all_people()
        results = {}

        for person in people:
            person_vec = np.array(person["vector_data"])

            # Для КАЖДОГО сегмента тестового аудио вычисляем сходство
            segment_similarities = []
            for emb in embeddings:
                similarity = self._cosine_similarity(emb, person_vec)
                segment_similarities.append(similarity)

            if not segment_similarities:
                continue

            # СТРАТЕГИЯ: используем 90-й ПЕРЦЕНТИЛЬ (устойчив к шумным сегментам)
            # Это лучше, чем среднее или максимум
            similarity_score = np.percentile(segment_similarities, 85)

            # Альтернативная стратегия: среднее по лучшим 3 сегментам
            # top_3 = sorted(segment_similarities, reverse=True)[:3]
            # similarity_score = np.mean(top_3) if top_3 else 0

            if similarity_score >= self.MIN_SIMILARITY:
                results[person["full_name"]] = float(similarity_score)

        return results

    def _cosine_similarity(self, a, b):
        """Вычисление косинусного сходства"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot_product / (norm_a * norm_b))

    def _confidence(self, score):
        """Определение уверенности в результате"""
        if score >= self.STRONG_THRESHOLD:
            return "высокая"
        elif score >= self.WEAK_THRESHOLD:
            return "средняя"
        elif score >= self.MIN_SIMILARITY:
            return "низкая"
        return "очень низкая"

    def _error(self, msg):
        return {"status": "error", "message": msg}

    def _not_found(self, segments, start_time):
        return {
            "status": "not_found",
            "segments": segments,
            "analysis_time": round(time.time() - start_time, 2)
        }