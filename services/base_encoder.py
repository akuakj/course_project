from abc import ABC, abstractmethod
import numpy as np

class BaseVoiceEncoder(ABC):
    
    @abstractmethod
    def get_embedding(self, audio: np.ndarray, sr: int) -> np.ndarray | None:
        pass

    @property
    @abstractmethod
    def embedding_dim(self) -> int:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_id(self) -> str:
        pass
