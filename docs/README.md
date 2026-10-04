# Transcriptor

App que recebe o link de um vídeo do YouTube, transcreve o vídeo inteiro, oferece tradução para português e gera um PDF com resumo e principais ideias.

## Documentação

| Documento | Conteúdo |
|---|---|
| [01-visao-geral.md](01-visao-geral.md) | Objetivo, usuários, escopo, requisitos funcionais e não funcionais |
| [02-arquitetura.md](02-arquitetura.md) | Premissas, stack, uso da GPU, componentes, fluxo de processamento, API, modelo de dados, estrutura de pastas |
| [03-roadmap.md](03-roadmap.md) | Etapas de desenvolvimento com entregáveis e critérios de aceite |
| [04-decisoes.md](04-decisoes.md) | Registro de decisões técnicas (ADRs) |
| [05-riscos-e-questoes.md](05-riscos-e-questoes.md) | Riscos, limitações e perguntas em aberto |
| [06-guia-de-desenvolvimento.md](06-guia-de-desenvolvimento.md) | Setup local, variáveis de ambiente, padrões de código e testes |

## Resumo em uma tela

- **Entrada:** URL do YouTube + opções (traduzir para PT? gerar PDF?).
- **Pipeline:** validar URL → obter legenda oficial (se houver) **ou** baixar áudio e transcrever com Whisper → (opcional) traduzir para português → gerar resumo e ideias com LLM → montar PDF.
- **Saídas:** transcrição (texto e .srt/.txt), tradução, PDF com resumo.
- **Onde roda:** inteiramente na máquina pessoal (i7-11700, RTX 3080, 32 GB), uso pessoal, **custo zero**.
- **Stack:** Python 3.12 + FastAPI com páginas HTMX, worker em thread + SQLite, `yt-dlp` + `faster-whisper` na GPU (transcrição), Ollama com `qwen3:8b` (tradução e resumo), WeasyPrint (PDF). Linux ou WSL2.
- **Primeira entrega útil:** uma CLI (`transcriptor <url>`) que já gera transcrição, tradução e PDF, antes de existir interface web.
