import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
import os
import librosa


class VoiceEncoderWrapper:
    def __init__(self):
        self.encoder = VoiceEncoder()

    def get_embedding_from_audio(self, audio: np.ndarray, sr: int):
        try:
            if audio.ndim > 1:
                audio = audio.mean(axis=1)

            # НОРМАЛИЗАЦИЯ громкости
            audio = audio / np.max(np.abs(audio) + 1e-8)

            # ОБРЕЗКА ТИШИНЫ с помощью librosa
            audio, _ = librosa.effects.trim(audio, top_db=25)

            # Если после обрезки слишком коротко, используем оригинал
            if len(audio) < sr * 0.5:  # меньше 0.5 секунды
                audio = audio.copy()  # возвращаем оригинал

            wav = preprocess_wav(audio, source_sr=sr)
            embedding = self.encoder.embed_utterance(wav)
            return embedding.astype(np.float32)

        except Exception as e:
            print(f"Ошибка извлечения эмбеддинга: {e}")
            return None

    def get_voice_embedding(self, audio_path):
        """
        Извлечение эмбеддинга голоса из аудиофайла
        """
        try:
            if not os.path.exists(audio_path):
                print(f"Файл не найден: {audio_path}")
                return None
            wav = preprocess_wav(audio_path)
            embedding = self.encoder.embed_utterance(wav)
            return embedding.astype(np.float32)
        except Exception as e:
            print(f"Ошибка извлечения эмбеддинга: {e}")
            return None
