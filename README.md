# Transcriptor

Cole o link de um vídeo do YouTube e receba a transcrição completa, a tradução para português e um PDF com resumo e principais ideias. Tudo roda na sua máquina, sem custo: transcrição com Whisper na GPU e tradução/resumo com um LLM local via Ollama.

> Status: **Etapa 0 (fundação)**. Ainda não transcreve; veja o [roadmap](docs/03-roadmap.md).

## Requisitos

- Windows com WSL2 (Ubuntu) ou Linux, GPU NVIDIA com driver atualizado
- Python 3.11+ e [uv](https://docs.astral.sh/uv/)
- `ffmpeg` (`sudo apt install ffmpeg`)
- [Ollama](https://ollama.com) com o modelo baixado: `ollama pull qwen3:8b`

## Começando

```bash
cp .env.example .env
uv sync
uv run transcriptor verificar   # confere Python, ffmpeg, GPU, Ollama e pasta de dados
```

## Desenvolvimento

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy
```

## Documentação

- [Visão geral](docs/01-visao-geral.md)
- [Arquitetura](docs/02-arquitetura.md)
- [Roadmap](docs/03-roadmap.md)
- [Decisões](docs/04-decisoes.md)
- [Riscos e perguntas](docs/05-riscos-e-questoes.md)
- [Guia de desenvolvimento](docs/06-guia-de-desenvolvimento.md)
