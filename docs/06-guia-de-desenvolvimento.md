# 06 · Guia de desenvolvimento

## Pré-requisitos (máquina do Igor)

- Se for Windows: WSL2 com Ubuntu 24.04 e driver NVIDIA atualizado no Windows (o WSL2 enxerga a GPU sem instalar driver dentro do Linux).
- Python 3.12 e `uv`
- `ffmpeg` (`sudo apt install ffmpeg`)
- Bibliotecas do WeasyPrint (`sudo apt install libpango-1.0-0 libpangoft2-1.0-0`)
- Bibliotecas CUDA 12 + cuDNN 9 para o `faster-whisper` (instaladas via pip: `nvidia-cublas-cu12`, `nvidia-cudnn-cu12`)
- [Ollama](https://ollama.com) e o modelo: `ollama pull qwen3:8b`

Nada disso tem custo.

## Variáveis de ambiente (`.env.example`)

```bash
# LLM
LLM_PROVIDER=ollama            # ollama | anthropic (opcional, pago)
OLLAMA_URL=http://localhost:11434
LLM_MODEL=qwen3:8b             # alternativa: gemma3:12b
LLM_NUM_CTX=16384
ANTHROPIC_API_KEY=             # só se LLM_PROVIDER=anthropic

# Transcrição
WHISPER_MODEL=large-v3-turbo   # large-v3 | medium | small
WHISPER_DEVICE=cuda            # cuda | cpu
WHISPER_COMPUTE_TYPE=float16   # float16 (gpu) | int8 (cpu)

# Limites
MAX_VIDEO_MINUTES=180
CHUNK_WORDS=1000

# Infra
DATABASE_URL=sqlite:///./data/transcriptor.db
STORAGE_DIR=./data
HOST=127.0.0.1                 # 0.0.0.0 para acessar de outros aparelhos (ex.: via Tailscale)
PORT=8000
```

## Comandos

```bash
uv sync
uv run transcriptor "https://youtu.be/<id>" --traduzir --pdf   # CLI (etapas 1–4)
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000         # app web (etapas 5–6)
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Na Etapa 7, `scripts/iniciar.sh` (e um atalho `.bat` no Windows) sobe o app e abre o navegador.

## Padrões

- **Código:** Ruff para lint e formatação; tipagem nas funções públicas.
- **Pipeline:** cada etapa lê e grava em `data/<video_id>/`; nada de estado global. Modelos (Whisper, LLM) são carregados no início da etapa e liberados no fim.
- **Prompts:** em arquivos versionados (`app/llm/prompts/*.md`), nunca inline no código.
- **Erros:** exceções próprias (`VideoIndisponivel`, `VideoMuitoLongo`, `FalhaNaTranscricao`, `FalhaNoLLM`, `OllamaIndisponivel`) com mensagens em português.
- **Git:** Conventional Commits (`feat:`, `fix:`, `docs:`...). Uma branch por tarefa do roadmap.

## Testes

| Tipo | O que cobre | Como |
|---|---|---|
| Unitário | parser de URL, chunking, normalização, SRT, validação do `summary.json` | Pytest, sem rede e sem GPU |
| Integração | pipeline completo com YouTube, Whisper e LLM simulados | Pytest + respostas salvas em `tests/fixtures/` |
| Ponta a ponta | 2–3 vídeos curtos reais | Manual, na máquina com GPU |

## Vídeos de referência para teste

Escolher e registrar aqui, na Etapa 1:
- Vídeo curto (< 5 min) em português com legenda manual.
- Vídeo em inglês de ~1 hora com legenda automática (palestra/podcast).
- Vídeo sem legenda (para forçar o Whisper).
