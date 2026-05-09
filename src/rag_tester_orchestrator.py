from importlib.resources import path
import os
import json
import pandas as pd
from typing import List, Dict
from base_rag import BaseRAG
from rag_tester import RAGTester

class RAGTesterOrchestrator:
    def __init__(self, dataset_path: str, source_file: str, output_path: str = "parcial_results"):
        """
        Args:
            dataset_path: Caminho para o arquivo JSON com o dataset.
            source_file: Caminho para o arquivo PDF/Texto de referência.
            output_path: Pasta onde os arquivos JSON parciais serão salvos.
        """
        self.dataset_path = dataset_path
        self.source_file = source_file
        self.output_path = output_path
        
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def _get_processed_workflows(self) -> List[str]:
        """Lê a pasta de resultados para saber quem já foi avaliado."""
        return [f.replace(".json", "") for f in os.listdir(self.output_path) if f.endswith(".json")]

    def run_comparison(self, workflows: Dict[str, BaseRAG]) -> pd.DataFrame:
        """
        Executa a avaliação para cada workflow fornecido.
        
        Args:
            workflows: Dict {"NomeDoGrupo": instancia_do_rag_do_grupo}
        Returns:
            pd.DataFrame: Tabela comparativa com as métricas médias por workflow.
        """
        processed = self._get_processed_workflows()
        all_summaries = []

        for name, rag_instance in workflows.items():
            file_path = os.path.join(self.output_path, f"{name}.json")
            
            if name in processed:
                print(f"Resultado parcial encontrado para '{name}'.")
                with open(file_path, "r", encoding='utf-8') as f:
                    all_summaries.append(json.load(f))
                continue

            print(f"Avaliando Workflow: {name}")
            
            try:
                evaluation_output = RAGTester.calculate_metrics(rag_instance, self.dataset_path)
                
                # Monta a linha da tabela com o nome do workflow + as médias calculadas
                workflow_row = {"workflow": name, **evaluation_output["summary"]}

                # Salva o resultado do workflow para persistência
                with open(file_path, "w", encoding='utf-8') as f:
                    json.dump(workflow_row, f, indent=4, ensure_ascii=False)
                
                all_summaries.append(workflow_row)

                print(f"Workflow '{name}' finalizado com sucesso.")

            except Exception as e:
                print(f"Erro ao avaliar o workflow '{name}': {str(e)}")
                
        if not all_summaries:
            return pd.DataFrame().set_index("workflow")

        return pd.DataFrame(all_summaries).set_index("workflow")