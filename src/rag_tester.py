import json
import time
import math
import numpy as np
import pandas as pd
from collections import Counter
from typing import List, Dict, Any, Optional
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from base_rag import BaseRAG
from llm_judge import LLMJudge

class RAGTester:
    """
    Classe utilitária estática para avaliação técnica de sistemas RAG.
    """

    # --- Métricas de Texto ---

    @staticmethod
    def _calculate_bleu(reference: str, candidate: str) -> float:
        ref_tokens = str(reference).lower().split()
        cand_tokens = str(candidate).lower().split()
        smoothie = SmoothingFunction().method1
        return sentence_bleu([ref_tokens], cand_tokens, smoothing_function=smoothie)

    @staticmethod
    def _calculate_rouge(reference: str, candidate: str) -> Dict[str, float]:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        scores = scorer.score(str(reference), str(candidate))
        return {
            'rouge1': scores['rouge1'].fmeasure,
            'rougeL': scores['rougeL'].fmeasure
        }

    @staticmethod
    def _calculate_cosine_similarity(reference: str, candidate: str) -> float:
        def text_to_vector(text):
            return Counter(str(text).lower().split())
        v1, v2 = text_to_vector(reference), text_to_vector(candidate)
        intersection = set(v1.keys()) & set(v2.keys())
        numerator = sum([v1[x] * v2[x] for x in intersection])
        sum1 = sum([v1[x]**2 for x in v1.keys()])
        sum2 = sum([v2[x]**2 for x in v2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        return float(numerator) / denominator if denominator else 0.0

    # --- Orquestração ---

    @staticmethod
    def calculate_metrics(rag_instance: BaseRAG, dataset_path: Optional[str] = None, metrics_to_run: Optional[List[str]] = None) -> Dict:
        if metrics_to_run is None:
            metrics_to_run = ['latency', 'bleu', 'rouge', 'cosine', 'llm_judge']
        
        # Só cria o objeto se o usuário pediu a métrica.
        judge_internal = None
        if 'llm_judge' in metrics_to_run:
            try:
                judge_internal = LLMJudge()
            except Exception as e:
                print(f"Erro ao instanciar LLM Judge internamente: {e}")
                # Remove a métrica da lista para não quebrar o loop depois
                metrics_to_run.remove('llm_judge')     

        results = []

        if dataset_path:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                dataset = [json.loads(line) for line in f]
        else:
                df = pd.read_parquet("hf://datasets/RonyOliveira/JK-RAG-Biography/data/train-00000-of-00001.parquet")
                dataset = df.to_dict('records')

        for item in dataset:
            # --- Formatação da Pergunta Completa ---
            pergunta_base = item['pergunta']
            alternativas = item.get('alternativas', {})
            
            # Cria uma string formatada: "Pergunta? a) Texto A, b) Texto B..."
            str_alternativas = ", ".join([f"{k}) {v}" for k, v in alternativas.items()])
            pergunta_completa = f"{pergunta_base} Alternativas: {str_alternativas}"

            gabarito_texto = item['resposta_texto']
            gabarito_chave = item['resposta_correta_chave']
            
            # Execução do RAG (retorna string)
            start_time = time.time()
            
            try:
                output_rag = rag_instance.answer_question(pergunta_completa)
            except Exception as e:
                print(f"Erro ao executar RAG: {e}")
                return {
                    "detailed": [],
                    "summary": []
                }
            
            latency = time.time() - start_time

            res = {
                'id': item.get('id'),
                'pergunta': pergunta_completa,
                'gabarito': gabarito_texto,
                'gabarito_chave': gabarito_chave,
                'gerada': output_rag,
                'latency': latency if 'latency' in metrics_to_run else None
            }

            # Métricas de Texto
            if 'bleu' in metrics_to_run:
                res['bleu'] = RAGTester._calculate_bleu(gabarito_texto, output_rag)
            if 'rouge' in metrics_to_run:
                res.update(RAGTester._calculate_rouge(gabarito_texto, output_rag))
            if 'cosine' in metrics_to_run:
                res['cosine'] = RAGTester._calculate_cosine_similarity(gabarito_texto, output_rag)

            # --- Métrica : Acurácia via LLM Judge ---
            if 'llm_judge' in metrics_to_run and judge_internal is not None:
                letra_detectada = judge_internal.identify_choice(
                    pergunta=pergunta_base, 
                    alternativas=str_alternativas, 
                    resposta_rag=output_rag
                )
                res['llm_detectou'] = letra_detectada
                
                # Compara a letra do juiz com o gabarito
                res['llm_judge'] = 1.0 if letra_detectada == gabarito_chave.upper() else 0.0

            results.append(res)

        # Limpeza de hardware via interface BaseRAG
        rag_instance.teardown()

# Cálculo das Médias (Summary)
        numeric_keys = [k for k, v in results[0].items() if isinstance(v, (int, float)) and k != 'id']
        averages = {f"avg_{k}": np.mean([r[k] for r in results if r.get(k) is not None]) for k in numeric_keys}

        return {
            "detailed": results,
            "summary": averages
        }