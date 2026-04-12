import numpy as np
import librosa
import os
from resemblyzer import VoiceEncoder, preprocess_wav

from services.base_encoder import BaseVoiceEncoder

class ResemblyzerEncoder(BaseVoiceEncoder):
    
    def __init__(self):
        self.encoder = VoiceEncoder()

    @property
    def embedding_dim(self) -> int:
        return 256
    
    @property
    def model_name(self) -> str:
        return f"Resemblyzer (GE2E)"
    
    @property
    def model_id(self) -> str:
        return "resemblyzer"
    

    def get_embedding(self, audio: np.ndarray, sr: int) -> np.ndarray | None:

        try:
            if audio.ndim > 1:
                audio = audio.mean(axis = 1)
            
            # Нормализация громкости: max амплитуда → 1.0
            # +1e-8 защищает от деления на ноль при тишине
            audio = audio / (np.max(np.abs(audio)) + 1e-8)

            # Обрезаем тишину в начале и конце
            trimmed, _ = librosa.effects.trim(audio, top_db=25)

            # Если после обрезки остался слишком короткий фрагмент
            if len(trimmed) >= sr * 0.5:
                audio = trimmed

            # ресемплинг до 16 кГц
            wav = preprocess_wav(audio, source_sr = sr)

            embedding = self.encoder.embed_utterance(wav)
            return embedding.astype(np.float32)

        except Exception as e:
            print(f"[ResemblyzerEncoder] Ошибка get_embedding: {e}")
            return None
        

    # Извлекает эмбеддинг напрямую из аудиофайла.
    def get_embedding_from_file(self, audio_path: str) -> np.ndarray | None:
        try:
            if not os.path.exists(audio_path):
                print(f"[ResemblyzerEncoder] Файл не найден: {audio_path}")
                return None

            wav = preprocess_wav(audio_path)
            embedding = self.encoder.embed_utterance(wav)
            return embedding.astype(np.float32)

        except Exception as e:
            print(f"[ResemblyzerEncoder] Ошибка get_embedding_from_file: {e}")
            return None