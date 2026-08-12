# Sistema de Portaria com Reconhecimento Facial

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10-5C3EE8?logo=opencv&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-FF6F00?logo=tensorflow&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)

> 🚧 Projeto em desenvolvimento.

## Objetivo

Este projeto foi criado como estudo prático para entender, na prática, como funcionam as bibliotecas envolvidas em um pipeline de reconhecimento facial: **DeepFace** (geração de embeddings faciais e comparação de rostos), **OpenCV** (captura e manipulação de vídeo em tempo real) e **SQLite** (persistência de dados). A ideia central não é só ter um sistema funcionando, mas entender o que cada biblioteca faz por baixo dos panos e como elas se encaixam entre si.

## Status atual

O core do sistema já está funcional rodando 100% local, via OpenCV. A interface web (Streamlit) ainda não foi feita.

### ✅ Implementado

- **Cadastro de pessoa** (`cadastro.py`): captura foto pela webcam, gera embedding facial com DeepFace (modelo Facenet + detector RetinaFace) e salva no banco.
- **Reconhecimento em tempo real** (`main.py`): captura frames da webcam a cada 10 frames, gera o embedding do rosto atual e compara por distância euclidiana com os embeddings salvos, usando o threshold oficial do DeepFace para o modelo Facenet.
- **Liberação/negação de acesso**: feedback visual em tela (texto e cor) indicando "Acesso liberado" ou "Acesso negado".
- **Exibição de latência**: tempo de processamento do reconhecimento (em ms) exibido em tela a cada verificação.
- **Log de acessos**: cada tentativa (reconhecida ou desconhecida) é salva na tabela `acessos`, com timestamp automático e uma foto do momento salva em disco.
- **Banco de dados SQLite** (`database.py`): schema com as tabelas `pessoas` (id, nome, embedding) e `acessos` (id, pessoa_id, timestamp, resultado, foto_path), com foreign key entre elas.

### ⏳ Pendente

- Portar a interface de janela OpenCV para Streamlit (`st.camera_input` ou `streamlit-webrtc`).
- Deploy público no Streamlit Community Cloud.
- Gravação do vídeo de demonstração e prints das telas principais.

## Arquitetura

```
Webcam → Detecção/Embedding facial (DeepFace) → Comparação com banco (distância euclidiana)
       → Decisão (liberado/negado) → Feedback visual → Log no SQLite (com foto)
```

## Stack técnica

| Camada | Ferramenta | Motivo |
|---|---|---|
| Linguagem | Python 3.11 | Padrão em visão computacional |
| Reconhecimento facial | DeepFace (Facenet + RetinaFace) | Instalação simples via pip, sem exigir build C++ |
| Captura de vídeo | OpenCV | Padrão para acesso à webcam e exibição de frames |
| Banco de dados | SQLite | Zero configuração, embutido, ideal para deploy simples |
| Interface / Deploy (planejado) | Streamlit + streamlit-webrtc | Transforma o script em app web acessível pelo navegador |

## Estrutura de arquivos

```
├── database.py               # cria o schema do banco (tabelas pessoas e acessos)
├── cadastro.py                # cadastra uma nova pessoa (foto + embedding)
├── main.py                    # loop principal de reconhecimento em tempo real
├── visual_reconhecimento.py   # funções auxiliares de desenho de texto no frame
└── banco.db                   # banco SQLite gerado localmente
```

## Como rodar localmente

> ⚠️ O DeepFace depende do TensorFlow, que no Windows costuma exigir versões específicas de `numpy` e `protobuf` para não quebrar. As versões no `requirements.txt` são fixas de propósito — não atualize sem testar.

```bash
# 1. Clonar o repositório
git clone https://github.com/gelane-dev/facial-recognition.git
cd facial-recognition

# 2. Criar e ativar o ambiente virtual (Python 3.11)
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Criar o banco de dados e as tabelas
python database.py

# 5. Cadastrar uma pessoa (pressione 'q' com o rosto enquadrado para salvar a foto)
python cadastro.py

# 6. Rodar o reconhecimento em tempo real
python main.py
```

## Banco de dados

**pessoas**
| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER PK | Identificador único |
| nome | TEXT | Nome da pessoa cadastrada |
| embedding | TEXT (JSON) | Vetor de embedding facial (Facenet) |

**acessos**
| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER PK | Identificador único |
| pessoa_id | INTEGER FK | Referência à pessoa reconhecida (nulo se desconhecida) |
| timestamp | DATETIME | Data/hora automática da tentativa |
| resultado | TEXT | `reconhecido` ou `desconhecido` |
| foto_path | TEXT | Caminho da foto capturada no momento do acesso |

## Decisões técnicas de destaque

- **Latência exibida em tela**: cada reconhecimento mede e mostra o tempo de processamento (ms), tornando visível o custo computacional do pipeline em tempo real.
- **Log com foto**: cada tentativa de acesso (liberada ou negada) salva uma imagem do momento, permitindo auditoria posterior.

## Próximos passos (produção)

- Migração para edge computing (ex: Raspberry Pi) rodando localmente, sem depender de internet.
- Integração elétrica real com fechadura (protocolo Wiegand + relé).
- Suporte a múltiplas câmeras.
- Modelo de reconhecimento mais robusto para escala (ex: ArcFace).
- Anti-spoofing mais avançado (profundidade, textura).
- Criptografia dos dados biométricos armazenados (conformidade com LGPD).

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.
