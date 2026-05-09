from __future__ import annotations

import argparse
import os

from dataset.hf_dataset_builder import JKDatasetBuildConfig, JKDatasetBuilder
from dataset.hf_dataset_uploader import HFDatasetUploadConfig, HFDatasetUploader


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Gera (e opcionalmente publica) o dataset JSONL do JK no formato do Hugging Face."
    )

    p.add_argument(
        "--input",
        default=os.path.join("kb", "processed", "jk_gold_standard.jsonl"),
        help="Caminho do JSONL de entrada (padrão: kb/processed/jk_gold_standard.jsonl)",
    )
    p.add_argument("--split", default="train", help="Nome do split (padrão: train)")
    p.add_argument(
        "--output-dir",
        default=os.path.join("kb", "hf_ready"),
        help="Pasta para salvar o Parquet localmente (padrão: kb/hf_ready)",
    )
    p.add_argument("--no-parquet", action="store_true", help="Não salvar Parquet local")

    p.add_argument(
        "--no-standard-columns",
        action="store_true",
        help="Não adicionar colunas padrão (question/answer/context)",
    )
    p.add_argument(
        "--no-pt-columns",
        action="store_true",
        help="Não manter as colunas em português (pergunta/resposta/trecho/etc)",
    )

    p.add_argument(
        "--expected-count",
        type=int,
        default=40,
        help="Quantidade esperada de registros (padrão: 40). Use 0 para desativar.",
    )

    p.add_argument("--push", action="store_true", help="Publicar no Hugging Face Hub")
    p.add_argument("--repo-id", default=None, help="Repo id no formato usuario/nome_do_dataset")
    p.add_argument("--private", action="store_true", help="Criar/atualizar como privado")
    p.add_argument(
        "--token-env",
        default="HF_TOKEN",
        help="Variável de ambiente que contém o token (padrão: HF_TOKEN)",
    )
    p.add_argument("--commit-message", default=None, help="Mensagem de commit (opcional)")

    return p.parse_args()


def main() -> None:
    args = parse_args()

    cfg = JKDatasetBuildConfig(
        input_jsonl=args.input,
        split_name=args.split,
        add_standard_columns=not args.no_standard_columns,
        keep_portuguese_columns=not args.no_pt_columns,
        output_dir=args.output_dir,
        save_parquet=not args.no_parquet,
        expected_count=None if args.expected_count == 0 else args.expected_count,
    )

    builder = JKDatasetBuilder(cfg)
    dataset_dict = builder.build()

    split = cfg.split_name
    print(f"✅ Build OK: split='{split}', registros={dataset_dict[split].num_rows}")
    print(f"📦 Colunas: {dataset_dict[split].column_names}")

    if args.push:
        if not args.repo_id:
            raise SystemExit("--push requer --repo-id (ex.: seu-usuario/jk-gold-standard)")

        up_cfg = HFDatasetUploadConfig(
            repo_id=args.repo_id,
            private=args.private,
            token_env_var=args.token_env,
            commit_message=args.commit_message,
        )
        uploader = HFDatasetUploader(up_cfg)
        uploader.push(dataset_dict)
        print(f"🚀 Push OK: {args.repo_id}")


if __name__ == "__main__":
    main()
