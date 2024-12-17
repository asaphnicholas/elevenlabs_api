
import speech_recognition as sr
import requests
import pyttsx3
import os
import wikipedia
import pywhatkit


# Configurações da API
API_KEY = ""  # Substitua pela sua API Key
VOICE_ID = "7u8qsX4HQsSHJ0f8xsQZ"  # ID da voz (pode ser obtido no painel do ElevenLabs)
TEXT = "Olá, como você está? Eu sou o Jarvis seu brasileiro de programação, e quero falar com você sobre inteligência artificial."
OUTPUT_FILE = "output.mp3"  # Nome do arquivo de saída

# URL da API
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

# Cabeçalhos e dados
headers = {
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}

data = {
    "text": TEXT,
    "voice_settings": {
        "stability": 0.3,  # Mais expressiva e fluida
        "similarity_boost": 1.0  # Alta semelhança com a voz natural
    }
}

# Fazer a requisição para a API
response = requests.post(url, headers=headers, json=data)

# Salvar o áudio em um arquivo
if response.status_code == 200:
    with open(OUTPUT_FILE, "wb") as f:
        f.write(response.content)
    print(f"Áudio salvo como {OUTPUT_FILE}")
else:
    print(f"Erro: {response.status_code} - {response.text}")

# Inicializa as instâncias necessárias
audio = sr.Recognizer()  # Corrigido aqui
maquina = pyttsx3.init()

# Função para ouvir o comando
def listen_comand():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('Escutando...')
            recognizer.adjust_for_ambient_noise(source)
            voz = audio.listen(source, timeout=5, phrase_time_limit=5)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            if 'jarvis' in comando:
                comando = comando.replace('jarvis', '')
                maquina.say(comando)
                maquina.runAndWait()
                return comando  # Retorna o comando aqui
    except sr.WaitTimeoutError:
        print("Tempo de escuta excedido. Nenhum som detectado.")
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
    except sr.RequestError as e:
        print(f"Erro na requisição ao Google: {e}")
    except Exception as e:
        print(f"Erro desconhecido: {e}")
        return ""  # Retorna string vazia em caso de erro

# Função para executar comandos
def execute_command():
    comando = listen_comand()
    if 'procure por' in comando:  # Corrigido "procute" para "procure"
        procurar = comando.replace('procure por', '')
        wikipedia.set_lang('pt')
        resultado = wikipedia.summary(procurar, 2)
        print(resultado)
        maquina.say(resultado)
        maquina.runAndWait()
    else:
        pass

# Loop principal
while True:
    execute_command()


