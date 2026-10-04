# 03 · Roadmap por etapas

Cada etapa termina com algo que funciona e pode ser testado. As etapas 1 a 4 entregam o valor principal pela linha de comando; a interface web vem depois, sobre um pipeline já validado.

| Etapa | Nome | Resultado visível |
|---|---|---|
| 0 | Fundação | Repositório, ambiente e CI prontos |
| 1 | Transcrição | `transcriptor <url>` gera `.txt` e `.srt` do vídeo inteiro |
| 2 | Tradução | `--traduzir` gera a versão em português |
| 3 | Resumo | Gera `summary.json` com resumo e ideias principais |
| 4 | PDF | Gera `report.pdf` completo — **MVP pela CLI** |
| 5 | App local e fila | Pipeline rodando em segundo plano dentro do app local |
| 6 | Interface web | Usuário cola o link no navegador e baixa os arquivos — **MVP web** |
| 7 | Conforto de uso | Inicia com um clique, acessível do celular, limpa arquivos antigos |
| 8 | Evoluções | Itens opcionais (ver fim do documento) |

---

## Etapa 0 · Fundação

**Tarefas**
- Criar repositório com a estrutura de pastas de [02-arquitetura.md](02-arquitetura.md).
- `pyproject.toml` com `uv` (ou `pip-tools`), Ruff (lint + formatação), Pytest, mypy.
- `pydantic-settings` para configuração; `.env.example` com as variáveis de [06-guia-de-desenvolvimento.md](06-guia-de-desenvolvimento.md).
- Ambiente local (WSL2/Linux) com ffmpeg, CUDA e Ollama funcionando; comando `transcriptor verificar` que testa GPU, ffmpeg e Ollama.
- CI (GitHub Actions, gratuito): lint + testes unitários a cada push.
- Copiar esta documentação para `docs/`.

**Critério de aceite:** testes e lint passam; `transcriptor verificar` confirma GPU, ffmpeg e Ollama.

## Etapa 1 · Transcrição

**Tarefas**
- `youtube.py`: extrair o `video_id` de qualquer formato de URL; ler metadados com `yt-dlp` (sem baixar o vídeo).
- Tentar legenda via `youtube-transcript-api` (preferência: manual > automática, no idioma original).
- Sem legenda: baixar só o áudio (`yt-dlp -f bestaudio`), converter para WAV 16 kHz mono com `ffmpeg`, transcrever com `faster-whisper` `large-v3-turbo` na GPU (com VAD ligado) e liberar a VRAM ao final.
- `normalize.py`: unificar as duas fontes em segmentos `{start, end, text}`; gerar `.txt` (com e sem timestamps) e `.srt`.
- Apagar o áudio ao final.
- CLI: `transcriptor <url> [--forcar-whisper] [--modelo large-v3-turbo]`.
- Medir o tempo real de transcrição de 1 h de áudio e registrar em [02-arquitetura.md](02-arquitetura.md).

**Critérios de aceite**
- Vídeo com legenda: transcrição pronta em segundos, `fonte = legenda_youtube`.
- Vídeo sem legenda de 30 min: transcrição completa, sem trechos faltando.
- URL inválida, vídeo privado ou acima do limite de duração: mensagem de erro clara.
- Testes unitários para parser de URL, normalização e geração de SRT.

## Etapa 2 · Tradução para português

**Tarefas**
- `LLMClient` em `llm/` com implementação `OllamaClient` (API HTTP do Ollama), retry e registro de tokens e tempo.
- Verificar se o Ollama está rodando e se o modelo está baixado; erro claro se não estiver.
- `chunking.py`: dividir segmentos em blocos de ~1.000 palavras sem cortar frases.
- `translate.py`: enviar segmentos numerados, receber a tradução no mesmo formato, preservar timestamps. Passar as últimas frases do bloco anterior como contexto.
- Pular a tradução quando o idioma original já for português.
- Prompts versionados em arquivos (`llm/prompts/traducao_v1.md`).
- CLI: `--traduzir`.

**Critérios de aceite**
- Vídeo em inglês de 1 hora traduzido inteiro; número de segmentos igual ao original.
- `.srt` traduzido abre corretamente em um player.
- Comparar `qwen3:8b` e `gemma3:12b` nos vídeos de referência (qualidade e tempo) e fixar o padrão.
- Modelo descarregado da GPU ao fim do job (`keep_alive: 0`).

## Etapa 3 · Resumo e ideias

**Tarefas**
- `summarize.py`: chamada única para transcrições curtas; map-reduce para longas.
- Saída estruturada (parâmetro `format` do Ollama com JSON Schema) no formato `summary.json` de [02-arquitetura.md](02-arquitetura.md), validada com Pydantic.
- Resumo sempre em português (padrão), independentemente do idioma do vídeo.
- Timestamps das ideias e citações apontando para o trecho real da transcrição.
- CLI: `--resumir`.

**Critérios de aceite**
- Para 3 vídeos de teste (aula, podcast, palestra), revisão manual confirma que o resumo cobre os pontos principais e que os timestamps batem com o vídeo.
- JSON sempre válido (teste com resposta malformada → nova tentativa).

## Etapa 4 · PDF (MVP pela CLI)

**Tarefas**
- Template HTML/CSS em `templates/report.html` seguindo a estrutura do PDF em [02-arquitetura.md](02-arquitetura.md).
- `pdf.py` com WeasyPrint; links de timestamp clicáveis.
- Opção de anexar a transcrição completa.
- CLI: `transcriptor <url> --traduzir --pdf` executa tudo de ponta a ponta.

**Critérios de aceite**
- PDF abre em leitores comuns, acentuação correta, quebra de página limpa.
- Fluxo completo funciona para um vídeo de 1 hora sem intervenção.

## Etapa 5 · App local e processamento em segundo plano

**Tarefas**
- Modelos `Video`, `Job`, `Artefato` com SQLAlchemy + SQLite.
- `runner.py`: orquestra as etapas, atualiza `status`/`progresso` no banco, retoma de onde parou.
- `worker.py`: thread iniciada junto com o FastAPI, que processa um job por vez a partir da tabela `jobs`.
- Rotas JSON da tabela de API em [02-arquitetura.md](02-arquitetura.md).
- Cache por `video_id` (reaproveita transcrição já feita).

**Critérios de aceite**
- Criar um job responde na hora; o processamento acontece em segundo plano.
- Fechar e reabrir o app no meio da tradução: o job continua da tradução.
- Dois jobs enviados em sequência são processados um depois do outro.

## Etapa 6 · Interface web (MVP web)

Páginas Jinja2 + HTMX servidas pelo próprio app.

**Telas**
1. **Início:** campo para o link, pré-visualização (miniatura, título, duração), opções (traduzir, gerar PDF, anexar transcrição), botão "Processar".
2. **Progresso:** etapas com indicador de status e porcentagem.
3. **Resultado:** abas "Resumo", "Transcrição" (original / português, com timestamps clicáveis que abrem o vídeo no ponto certo), botões de download (`.txt`, `.srt`, `.pdf`).
4. **Histórico:** lista de vídeos já processados, com fila de pendentes.

**Critérios de aceite**
- Fluxo completo pelo navegador do PC.
- Erros mostrados em linguagem simples (ex.: "O Ollama não está aberto").

## Etapa 7 · Conforto de uso

**Tarefas**
- `scripts/iniciar.sh` e atalho `.bat` no Windows: sobe o app (e o Ollama, se necessário) e abre o navegador.
- Opcional: iniciar junto com o sistema.
- Opcional: acesso pelo celular via Tailscale (`HOST=0.0.0.0`, só dentro da rede Tailscale).
- Limpeza automática de áudios e de resultados com mais de N dias (configurável).
- Backup simples da pasta `data/`.

**Critério de aceite:** do clique no atalho até colar o link, sem abrir terminal.

## Etapa 8 · Evoluções possíveis

- Contas de usuário e limites por plano.
- Upload de áudio/vídeo local.
- Playlists inteiras.
- Diarização (quem falou o quê) com `pyannote`.
- Exportar para Markdown, DOCX ou Notion.
- "Converse com o vídeo": perguntas e respostas sobre a transcrição.
- Escolha de outros idiomas de tradução.
