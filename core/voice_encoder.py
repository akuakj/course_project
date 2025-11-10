import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
import os


class VoiceEncoderWrapper:
    def __init__(self):
        """
        Инициализация энкодера голоса Resemblyzer
        """
        self.encoder = VoiceEncoder()

    def get_voice_embedding(self, audio_path):
        """
        Извлечение эмбеддинга голоса из аудиофайла

        Args:
            audio_path: путь к аудиофайлу

        Returns:
            numpy array: вектор эмбеддинга (256 измерений) или None при ошибке
        """
        try:
            # Проверяем существование файла
            if not os.path.exists(audio_path):
                print(f"Файл не найден: {audio_path}")
                return None

            # Загружаем и предобрабатываем аудио
            wav = preprocess_wav(audio_path)

            # Извлекаем эмбеддинг
            embedding = self.encoder.embed_utterance(wav)

            print(f"Эмбеддинг извлечен: {embedding.shape}")
            return embedding

        except Exception as e:
            print(f"Ошибка извлечения эмбеддинга: {e}")
            return None