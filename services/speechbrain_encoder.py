import numpy as np
from services.base_encoder import BaseVoiceEncoder


class SpeechBrainEncoder(BaseVoiceEncoder):

    def __init__(self):
        self._model = None  # ленивая загрузка

    def _load_model(self):
        if self._model is not None:
            return

        try:
            from speechbrain.inference.speaker import EncoderClassifier
            
            print("[SpeechBrainEncoder] Загрузка ECAPA-TDNN модели...")

            self._model = EncoderClassifier.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb",
                savedir="data/models/ecapa_tdnn",
                run_opts={"device": "cpu"}
            )
            print("[SpeechBrainEncoder] Модель загружена")
        except Exception as e:
            print(f"[SpeechBrainEncoder] Ошибка загрузки модели: {e}")
            raise

    @property
    def embedding_dim(self) -> int:
        return 192

    @property
    def model_name(self) -> str:
        return "ECAPA-TDNN (SpeechBrain)"

    @property
    def model_id(self) -> str:
        return "speechbrain"

    def get_embedding(self, audio: np.ndarray, sr: int) -> np.ndarray | None:
        """
        Принимает audio (np.ndarray, моно, float32/float64) и sample rate.
        Возвращает 192-мерный эмбеддинг или None при ошибке.
        """
        try:
            import torch
            import torchaudio

            self._load_model()

            # Приводим к моно float32
            if audio.ndim > 1:
                audio = audio.mean(axis=1)
            audio = audio.astype(np.float32)

            # Нормализация громкости
            max_val = np.max(np.abs(audio))
            if max_val > 0:
                audio = audio / (max_val + 1e-8)

            # SpeechBrain ожидает тензор [1, samples] и sr=16000
            wav_tensor = torch.tensor(audio).unsqueeze(0)  # [1, N]

            # Ресемплинг до 16 кГц если нужно
            if sr != 16000:
                resampler = torchaudio.transforms.Resample(
                    orig_freq=sr, new_freq=16000
                )
                wav_tensor = resampler(wav_tensor)

            # Длина в сэмплах после ресемплинга
            wav_lens = torch.tensor([1.0])  # относительная длина (1.0 = полный)

            with torch.no_grad():
                embedding = self._model.encode_batch(wav_tensor, wav_lens)

            result = embedding.squeeze().cpu().numpy().astype(np.float32)
            norm = np.linalg.norm(result)

            if norm > 0:
                result = result / norm
            return result

        except Exception as e:
            print(f"[SpeechBrainEncoder] Ошибка get_embedding: {e}")
            return 