import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_HISTORY = 10  # max de mensagens na memória pra não travar a API

def limpar_historico(messages):
    # mantém o system + últimas mensagens, evita excesso
    if len(messages) > MAX_HISTORY:
        return [messages[0]] + messages[-(MAX_HISTORY-1):]
    return messages

def chamar_api(messages):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            n=1
        )
        return resposta['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"Erro na API: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def conversar():
    print("🤖 ChatGPT com memória e tratamento de erros")
    print("Digite 'sair' pra fechar, 'limpar' pra zerar o papo.\n")
    
    messages = [
        {"role": "system", "content": "Você é um assistente útil, educado e claro."}
    ]
    
    while True:
        mensagem = input("Você: ").strip()
        if mensagem.lower() == "sair":
            print("Valeu! Até a próxima.")
            break
        if mensagem.lower() == "limpar":
            messages = [messages[0]]
            print("Contexto zerado, bora começar de novo!")
            continue
        if not mensagem:
            print("Escreve algo aí, ou 'sair' pra encerrar.")
            continue
        
        messages.append({"role": "user", "content": mensagem})
        messages = limpar_historico(messages)
        
        print("🤖 Pensando...", end="\r")
        
        resposta_texto = chamar_api(messages)
        if resposta_texto is None:
            print("Não rolou resposta da API. Tenta de novo depois.")
            continue
        
        messages.append({"role": "assistant", "content": resposta_texto})
        print("Bot:", resposta_texto)

if __name__ == "__main__":
    conversar()

        
        # resposta
        print("Bot:", resposta_texto)
        
if __name__ == "__main__":
    conversar()
