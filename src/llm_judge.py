import os
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

class LLMJudge:
    def __init__(self, chat_model: BaseChatModel):
        """
        Recebe qualquer instância de chat_model que herde de BaseChatModel.
        Ex: ChatHuggingFace, ChatGoogleGenerativeAI, ChatOpenAI, etc.
        """
        self.chat_model = chat_model
        print(f"✅ Juiz inicializado com o modelo: {type(self.chat_model).__name__}")

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