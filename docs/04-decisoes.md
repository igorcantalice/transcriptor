# 04 · Registro de decisões (ADRs)

Formato: contexto → decisão → consequências. Novas decisões entram no fim, numeradas. Decisões substituídas ficam registradas com o status "Substituída".

## ADR-001 · Python + FastAPI
- **Contexto:** o núcleo do app é processamento de áudio e texto.
- **Decisão:** Python 3.12 com FastAPI.
- **Consequências:** acesso direto a `yt-dlp`, `faster-whisper` e WeasyPrint.

## ADR-002 · Legenda do YouTube primeiro, Whisper como alternativa
- **Decisão:** usar a legenda quando existir; transcrever com Whisper só quando não houver ou quando o usuário forçar.
- **Consequências:** muito mais rápido na maioria dos casos. Legendas automáticas vêm sem pontuação; o LLM repontua na tradução/resumo.

## ADR-003 · faster-whisper local na GPU
- **Decisão:** `faster-whisper` com `large-v3-turbo`, CUDA, float16, na RTX 3080.
- **Consequências:** custo zero e transcrição de 1 h de áudio em poucos minutos. `large-v3` fica disponível como opção (mais lento, um pouco mais preciso).

## ADR-004 · ~~Claude API para tradução e resumo~~ (Substituída pela ADR-008)

## ADR-005 · ~~RQ + Redis para jobs~~ (Substituída pela ADR-009)

## ADR-006 · PDF via HTML + WeasyPrint
- **Decisão:** gerar HTML com Jinja2 e converter com WeasyPrint.
- **Consequências:** layout fácil de ajustar com CSS. Exige Pango, trivial no Linux/WSL2 e trabalhoso no Windows nativo (um dos motivos da ADR-011).

## ADR-007 · CLI antes da interface web
- **Decisão:** entregar o pipeline completo pela linha de comando (etapas 1–4) antes da web.
- **Consequências:** valida a qualidade cedo, com menos código.

## ADR-008 · LLM local via Ollama (custo zero)
- **Contexto:** uso pessoal, sem orçamento para APIs; a máquina tem RTX 3080.
- **Decisão:** Ollama com `qwen3:8b` (Q4_K_M) para tradução e resumo. O acesso ao LLM fica atrás de uma interface `LLMClient`; um `AnthropicClient` pode ser adicionado depois, ativado por `LLM_PROVIDER=anthropic`, se em algum momento valer pagar por mais qualidade.
- **Consequências:** custo zero e privacidade total. Qualidade de tradução e resumo inferior a modelos grandes de API, mas boa para PT-BR; compensada com blocos menores (~1.000 palavras), saída estruturada e nova tentativa em caso de JSON inválido. Na Etapa 2, comparar `qwen3:8b` e `gemma3:12b` nos vídeos de referência e escolher o padrão.

## ADR-009 · Worker em thread + SQLite em vez de Redis
- **Contexto:** um único usuário e uma única GPU; só faz sentido um job por vez.
- **Decisão:** a tabela `jobs` no SQLite é a fila; uma thread dentro do processo FastAPI pega o próximo job pendente. Ao iniciar, jobs que estavam "em andamento" voltam para "pendente" e retomam da última etapa concluída.
- **Consequências:** um processo só, sem Redis e sem Docker. Se um dia houver vários usuários, trocar por RQ/Redis sem mexer no pipeline.

## ADR-010 · Interface com Jinja2 + HTMX em vez de React
- **Decisão:** páginas renderizadas pelo próprio FastAPI, com HTMX para progresso e interações.
- **Consequências:** sem Node, sem build, sem segundo projeto. Suficiente para as 4 telas do app.

## ADR-011 · Rodar em Linux/WSL2
- **Decisão:** se a máquina for Windows, rodar o app dentro do WSL2 (Ubuntu); o Ollama pode rodar no Windows ou no WSL2.
- **Consequências:** instalação de CUDA, ffmpeg e WeasyPrint sem atrito. O navegador do Windows acessa `http://localhost:8000` normalmente.
