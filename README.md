[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/YwAhie6h)

# Valiador de RAGs - JK Biography

## Descrição

Este projeto implementa um sistema avaliação de RAGs.
O foco é avaliar a qualidade das respostas geradas por um modelo de linguagem em conjunto com um mecanismo de recuperação de documento.

> Projeto desenvolvido para a disciplina de **Sistemas Multiagentes**, semestre 2026.1, BCC, UFRPE.

## Equipe

- João Victor Morais Barreto da Silva
- Mariane Elisa dos Santos Souza
- Rony Elias de Oliveira

## Métricas Utilizadas

O avaliador implementa as seguintes métricas para comparar as respostas geradas pelo RAG com o gabarito:

- **BLEU**: mede a similaridade de n-gramas entre a resposta gerada e a resposta de referência.
- **ROUGE-1**: mede a sobreposição de unigramas entre a resposta gerada e a referência.
- **ROUGE-L**: mede a similaridade baseada na maior subsequência comum entre a resposta gerada e a referência.
- **Similaridade de cosseno**: compara a similaridade semântica baseada em contagem de tokens entre texto gerado e referência.
- **Acurácia de múltipla escolha**: verifica se a resposta gerada corresponde à alternativa correta do gabarito.
- **Latência**: tempo total de geração da resposta para cada item do dataset.

## Estrutura do Projeto

```
├── README.md
├── src/
│   ├── base_rag.py       # Interface base para implementações de RAG
│   ├── rag_tester.py     # Avaliação e cálculo de métricas
│   └── dataset/
│       ├── generate_jsonl.py
│       ├── hf_dataset_builder.py
│       ├── hf_dataset_uploader.py
│       └── publish_hf_dataset.py
├── kb/
│   ├── hf_ready/
│   └── raw/
├── notebooks/
│   └── RAGEvaluation.ipynb
├── results_parcial/
├── requirements.txt
└── README.md
```

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/<seu-usuario>/<seu-repositorio>.git
   cd <seu-repositorio>
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Dataset padrão

O dataset padrão usado pelo avaliador é:

- `https://huggingface.co/datasets/RonyOliveira/JK-RAG-Biography`

Por padrão, `RAGTester.calculate_metrics` carrega automaticamente os dados via Hugging Face a partir do mesmo dataset.
Também é possível usar qualquer outro dataset local passando o caminho do arquivo para `dataset_path`.

## Como Executar

### Rodar os testes de avaliação

Importe os arquivos `base_rag.py` e `rag_tester.py`, crie uma instância do seu RAG, que deve extender da classe BaseRAG, e execute a função de avaliação.

```python
from src.base_rag import BaseRAG
from src.rag_tester import RAGTester

# instância_rag deve ser um objeto que implementa BaseRAG
resultados = RAGTester.calculate_metrics(rag_instance=instancia_rag)
```

Para usar um dataset diferente, passe o caminho do arquivo para `dataset_path`:

```python
resultados = RAGTester.calculate_metrics(
    rag_instance=instancia_rag,
    dataset_path='caminho/para/seu_dataset.jsonl'
)
```

### O que a função retorna

A função `RAGTester.calculate_metrics` retorna um dicionário com duas chaves principais:

- `detailed`: lista de resultados por item do dataset, incluindo perguntas, respostas geradas, métricas e latência.
- `summary`: médias das métricas calculadas para todo o dataset.

Além disso, a função salva dois arquivos CSV locais:

- `resultados_detalhados.csv`
- `resultados_resumo.csv`

## Exemplos de saída

```python
{
    'detailed': [
        {
            'id': '1',
            'pergunta': '... Alternativas: ...',
            'gabarito': 'texto correto',
            'gerada': 'resposta do RAG',
            'latency': 1.23,
            'bleu': 0.45,
            'rouge1': 0.52,
            'rougeL': 0.48,
            'cosine': 0.60,
            'accuracy': 1.0
        },
        ...
    ],
    'summary': {
        'avg_latency': 1.03,
        'avg_bleu': 0.42,
        'avg_rouge1': 0.50,
        'avg_rougeL': 0.47,
        'avg_cosine': 0.58,
        'avg_accuracy': 0.80
    }
}
```

## Licença

Este projeto está sob a licença MIT.
