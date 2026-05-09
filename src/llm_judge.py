import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage

class LLMJudge:
    def __init__(self, repo_id="moonshotai/Kimi-K2.6"):
        """
        Inicializa o Juiz usando o endpoint remoto do Hugging Face (Kimi via Fireworks-AI).
        Baseado no notebook da Aula 03 da disciplina.
        """
        print(f"Conectando ao Juiz HF (Kimi): {repo_id}...")
        
        # O token do Hugging Face deve estar nas variáveis de ambiente
        self.hf_token = os.getenv("HF_TOKEN")
        if not self.hf_token:
            raise ValueError("Erro: Variável de ambiente HF_TOKEN não configurada.")

        # 1. Configura o modelo base (Endpoint) conforme o exemplo do professor
        self.llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            provider="fireworks-ai",
            task="text-generation",
            max_new_tokens=10, # Só precisamos de uma letra
            huggingfacehub_api_token=self.hf_token,
            temperature=0.1
        )

        # 2. Transforma em ChatHuggingFace para suportar SystemMessage e HumanMessage
        self.chat_model = ChatHuggingFace(llm=self.llm)
        print(f"✅ Juiz {repo_id} pronto para avaliação!")

    def identify_choice(self, pergunta: str, alternativas: str, resposta_rag: str) -> str:
        """
        Lê a resposta do RAG e identifica qual alternativa (A, B, C, D ou E) foi escolhida.
        """
        prompt = f"""Analise a Resposta do RAG abaixo e identifique qual das Alternativas ela escolheu.
            Pergunta: {pergunta}
            Alternativas: {alternativas}
            Resposta do RAG: {resposta_rag}

            Instrução: Com base na Resposta do RAG, qual letra das alternativas foi selecionada? 
            Responda APENAS com a letra correspondente (A, B, C, D ou E). Não explique.

            Letra: """

        messages = [
            SystemMessage(content="Você é um classificador de respostas de múltipla escolha estrito."),
            HumanMessage(content=prompt)
        ]

        try:
            response = self.chat_model.invoke(messages)
            # O ChatHuggingFace retorna um AIMessage, acessamos o content
            veredito = response.content.strip().upper()
            
            # Garante que retornamos apenas a letra limpa (primeiro caractere)
            if veredito and veredito[0] in "ABCDE":
                return veredito[0]
            
            return "Z" # Caso o modelo não identifique a letra
        except Exception as e:
            print(f"Erro na chamada do Juiz HF: {e}")
            return "Z"