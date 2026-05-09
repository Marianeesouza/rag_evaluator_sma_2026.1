from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from datasets import Dataset, DatasetDict


REQUIRED_KEYS: Tuple[str, ...] = ("id", "pergunta", "resposta", "capitulo", "pagina", "trecho")


@dataclass(frozen=True)
class JKDatasetBuildConfig:
    input_jsonl: str = os.path.join("kb", "processed", "jk_gold_standard.jsonl")
    split_name: str = "train"

    add_standard_columns: bool = True
    keep_portuguese_columns: bool = True

    output_dir: Optional[str] = os.path.join("kb", "hf_ready")
    save_parquet: bool = True

    expected_count: Optional[int] = 40


class JKDatasetBuilder:
    """Transforma um arquivo JSONL estrito em um `DatasetDict` do Hugging Face.

    Premissas:
    - a entrada está no formato JSON Lines válido (um objeto JSON por linha)
    - cada objeto contém todas as chaves em `REQUIRED_KEYS`
    """

    def __init__(self, config: JKDatasetBuildConfig):
        self.config = config

    def load_jsonl(self) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        with open(self.config.input_jsonl, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(f"JSON inválido na linha {line_no}: {e}") from e
                if not isinstance(obj, dict):
                    raise ValueError(f"Registro na linha {line_no} não é objeto JSON (dict)")
                records.append(obj)

        if not records:
            raise ValueError("Nenhum registro encontrado no JSONL")

        if self.config.expected_count is not None and len(records) != self.config.expected_count:
            raise ValueError(
                f"Quantidade inesperada de registros: {len(records)} (esperado: {self.config.expected_count})"
            )

        return records

    def validate_and_normalize(self, records: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
        normalized: List[Dict[str, Any]] = []
        seen_ids = set()

        for idx, rec_in in enumerate(records, start=1):
            missing = [k for k in REQUIRED_KEYS if k not in rec_in]
            if missing:
                raise ValueError(f"Registro #{idx} sem chaves obrigatórias: {missing}")

            rec: Dict[str, Any] = dict(rec_in)

            rec["id"] = self._to_int(rec["id"], field="id", idx=idx)
            rec["pagina"] = self._to_int(rec["pagina"], field="pagina", idx=idx)

            for key in ("pergunta", "resposta", "capitulo", "trecho"):
                val = rec.get(key)
                if not isinstance(val, str):
                    raise ValueError(
                        f"Registro #{idx}: campo '{key}' deve ser str. Recebido: {type(val).__name__}"
                    )
                rec[key] = val.replace("\r\n", "\n").strip()

            if rec["id"] in seen_ids:
                raise ValueError(f"Registro #{idx}: id duplicado: {rec['id']}")
            seen_ids.add(rec["id"])

            out: Dict[str, Any] = {}

            if self.config.keep_portuguese_columns:
                for key in REQUIRED_KEYS:
                    out[key] = rec[key]

            if self.config.add_standard_columns:
                out["question"] = rec["pergunta"]
                out["answer"] = rec["resposta"]
                out["context"] = rec["trecho"]
                out["language"] = "pt"

            normalized.append(out)

        normalized.sort(key=lambda r: r.get("id", 0))
        return normalized

    def to_datasetdict(self, records: Sequence[Mapping[str, Any]]) -> DatasetDict:
        dataset = Dataset.from_list([dict(r) for r in records])
        return DatasetDict({self.config.split_name: dataset})

    def save_local(self, dataset_dict: DatasetDict) -> None:
        if not self.config.output_dir or not self.config.save_parquet:
            return

        os.makedirs(self.config.output_dir, exist_ok=True)
        split = self.config.split_name
        out_path = os.path.join(self.config.output_dir, f"{split}.parquet")
        dataset_dict[split].to_parquet(out_path)

    def build(self) -> DatasetDict:
        raw = self.load_jsonl()
        cleaned = self.validate_and_normalize(raw)
        dataset_dict = self.to_datasetdict(cleaned)
        self.save_local(dataset_dict)
        return dataset_dict

    @staticmethod
    def _to_int(value: Any, field: str, idx: int) -> int:
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            s = value.strip()
            if s.isdigit():
                return int(s)
        raise ValueError(
            f"Registro #{idx}: campo '{field}' deve ser int ou string numérica. Recebido: {value!r}"
        )
