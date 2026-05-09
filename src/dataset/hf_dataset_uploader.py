from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from datasets import DatasetDict


@dataclass(frozen=True)
class HFDatasetUploadConfig:
    repo_id: str
    private: bool = False
    token_env_var: str = "HF_TOKEN"
    commit_message: Optional[str] = None


class HFDatasetUploader:
    """Faz upload de um `DatasetDict` para o Hugging Face Hub usando token via variável de ambiente."""

    def __init__(self, config: HFDatasetUploadConfig):
        self.config = config

    def push(self, dataset_dict: DatasetDict) -> None:
        token = os.getenv(self.config.token_env_var)
        if not token:
            raise ValueError(
                f"Token não encontrado. Defina a variável de ambiente {self.config.token_env_var} "
                f"(ex.: setx {self.config.token_env_var} \"hf_...\")"
            )

        push_kwargs = {
            "private": self.config.private,
            "token": token,
        }
        if self.config.commit_message:
            push_kwargs["commit_message"] = self.config.commit_message

        dataset_dict.push_to_hub(self.config.repo_id, **push_kwargs)
