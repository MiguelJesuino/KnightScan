# KnightScan
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

                _____________________________________________________|_,_,_,_,_,_,_,_,_,_,    
              /______________________________________________________||#|#|#|#|#|#|#|#|#|#
             '-------------------------------------------------------|-'-'-'-'-'-'-'-'-'-'
                 ____  __.      .__       .__     __   _________                     
                |    |/ _| ____ |__| ____ |  |___/  |_/   _____/ ____ _____    ____  
                |      <  /    \|  |/ ___\|  |  \   __\_____  \_/ ___\\__  \  /    \ 
                |    |  \|   |  \  / /_/  >   Y  \  | /        \  \___ / __ \|   |  \
                |____|__ \___|  /__\___  /|___|  /__|/_______  /\___  >____  /___|  /
                        \/    \/  /_____/      \/            \/     \/     \/     \/ 
                             
              ,_,_,_,_,_,_,_,_,_,_|______________________________________________________
              |#|#|#|#|#|#|#|#|#|#|_____________________________________________________/
              '-'-'-'-'-'-'-'-'-'-|----------------------------------------------------'
              
## 💡 Descrição


**KnightScan** é um scanner de portas simples e eficiente escrito em Python, projetado para aprendizado, testes básicos de conectividade e análise leve de hosts. Ele identifica portas abertas, banners de serviços e tenta inferir o sistema operacional de forma básica.


---

## 🚀 Funcionalidades

- 🔎 **Varredura de portas TCP** – varredura de portas únicas ou em intervalo.
- 🌐 **Suporte a múltiplos hosts** – possibilita escanear mais de um host simultaneamente.
- ⚡ **Multi-threading** – desempenho otimizado com o controle do número de threads.
- 🧾 **Detecção de banners e inferência básica de SO** – coleta informações do serviço ativo e tenta identificar o sistema operacional.
- 💾 **Salvamento de resultados** – exporta os resultados em `.txt` ou `.json`.
- 🖥️ **Interface CLI amigável** – fácil de usar e personalizar.

---

## 📦 Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/MiguelJesuino/KnightScan.git
cd KnightScan
python -m venv .venv
```
#### No Windows:
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```
#### No Linux/Mac:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Uso
Rode o script principal especificando o host e demais parâmetros:

  ```bash
  python KnightScan.py <host> [opções]
  ```

## Argumentos
| Argumento         | Descrição                                           |
|-------------------|-----------------------------------------------------|
| `<host>`          | IP ou domínio alvo. Para múltiplos, separe por `,`. |
| `-p`, `--ports`   | Porta única ou intervalo (ex: `80` ou `1-1024`).     |
| `-t`, `--threads` | Número de threads (padrão: `100`).                   |
| `--timeout`       | Tempo de timeout por conexão (segundos, padrão: 1).  |
| `--log`           | Exibe portas fechadas também.                       |
| `--save`          | Salva os resultados em `.txt` ou `.json`.           |

## 📂 Estrutura do Projeto
```plaintext
KnightScan/
├── Scanner.py         # Lógica de escaneamento
├── KnightScan.py      # Script principal com argparse e saída
└── requirements.txt   # Dependências do projeto
```

## 🤝 Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

----------
Desenvolvido por [MiguelJesuino](https://github.com/MiguelJesuino/).
