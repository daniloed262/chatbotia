import openai
import os
from dotenv import load_dotenv
import sys
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Número máximo de mensagens para manter no histórico (memória)
MAX_HISTORY = 10

def limpar_historico(messages):
    """Remove as mensagens antigas para não passar do limite de tokens"""
    # Mantém sempre a primeira mensagem do sistema + as últimas MAX_HISTORY - 1 mensagens
    if len(messages) > MAX_HISTORY:
        return [messages[0]] + messages[-(MAX_HISTORY-1):]
    return messages

def chamar_api(messages):
    """Chama a API OpenAI e retorna a resposta do assistente"""
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,   # criatividade moderada
            max_tokens=500,    # limite da resposta
            n=1,              # número de respostas geradas
            stop=None
        )
        return resposta['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"[Erro na API OpenAI]: {e}")
        return None
    except Exception as e:
        print(f"[Erro inesperado]: {e}")
        return None

def conversar():
    print("🤖 ChatGPT com memória e tratamento de erros")
    print("Digite 'sair' para encerrar a conversa ou 'limpar' para reiniciar o contexto.\n")
    
    messages = [
        {"role": "system", "content": "Você é um assistente útil, educado e claro."}
    ]
    
    while True:
        mensagem = input("Você: ").strip()
        if mensagem.lower() == "sair":
            print("Até mais! Foi um prazer conversar com você.")
            break
        if mensagem.lower() == "limpar":
            messages = [messages[0]]
            print("Contexto da conversa foi limpo. Podemos começar de novo!")
            continue
        if not mensagem:
            print("Por favor, digite algo ou 'sair' para encerrar.")
            continue
        
        # Adiciona msg do usuário
        messages.append({"role": "user", "content": mensagem})
        
        # Limpa hist. 
        messages = limpar_historico(messages)
        
        print("🤖 Pensando...", end="\r")
        
        resposta_texto = chamar_api(messages)
        
        if resposta_texto is None:
            print("Não foi possível obter resposta da API. Tente novamente mais tarde.")
            continue
        
        # Add resposta do assistente
        messages.append({"role": "assistant", "content": resposta_texto})
        
        # Resposta
        print("Bot:", resposta_texto)
        
if __name__ == "__main__":
    conversar()
