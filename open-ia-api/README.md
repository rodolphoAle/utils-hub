# 🤖 OpenAI API Utils - Biblioteca de Funções para OpenAI 🚀

Bem-vindo ao **OpenAI API Utils**! Este módulo faz parte do repositório **Utils Hub** e contém funções para facilitar a interação com a API da OpenAI, incluindo criação e gerenciamento de threads, envio de mensagens e obtenção de respostas do assistente.

## 📌 Funcionalidades

✅ Criar e gerenciar threads na OpenAI API  
✅ Adicionar mensagens a uma thread  
✅ Executar assistente em uma thread  
✅ Obter respostas do assistente de forma estruturada  
✅ Log automático para depuração

## 📂 Estrutura do Código

- `openai_utils.py` → Implementação das funções para interação com a OpenAI API.
- `.env` → Arquivo para armazenar a API Key (não incluído no repositório por segurança).
- `requirements.txt` → Lista de dependências necessárias.

## 📦 Instalação

1️⃣ Clone o repositório:
```sh
git clone https://github.com/rodolphoAle/utils-hub
cd utils-hub/OpenAI_API
```

2️⃣ Crie um ambiente virtual (opcional, mas recomendado):
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

3️⃣ Instale as dependências:
```sh
pip install -r requirements.txt
```

4️⃣ Configure sua chave de API da OpenAI:
Crie um arquivo `.env` no diretório do projeto e adicione:
```
API_KEY=your_openai_api_key
ASSISTANT_ID=your_assistant_id
```

## 🚀 Como Usar

### 🔹 Exemplo de Uso

```python
from openai_utils import processoGPT
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv("API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

prompts = ["Qual a capital da França?", "Explique a teoria da relatividade em termos simples."]
respostas = processoGPT(api_key, assistant_id, prompts)

for i, resposta in enumerate(respostas):
    print(f"Resposta {i+1}: {resposta}")
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **OpenAI API**
- **Logging para depuração**
- **dotenv para variáveis de ambiente**

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - consulte o arquivo `LICENSE` para mais detalhes.

---
📢 **Contribuições são bem-vindas!** Se você tem sugestões ou melhorias, fique à vontade para abrir um pull request. 😊

