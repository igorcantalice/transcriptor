# 05 · Riscos e perguntas em aberto

## Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| YouTube bloqueia downloads ou muda a página (quebra do `yt-dlp`) | Alto | Manter `yt-dlp` sempre atualizado (comando de atualização no script de inicialização); priorizar legendas; mensagens de erro claras |
| Termos de uso do YouTube e direitos autorais | Médio | Uso pessoal; não redistribuir áudio nem os PDFs; apagar o áudio após transcrever |
| Falta de VRAM (Whisper e LLM juntos, ou GPU ocupada por outro programa) | Médio | Etapas em sequência com descarga dos modelos; `int8_float16` no Whisper e modelo menor no LLM como plano B; erro claro se faltar memória |
| Qualidade do LLM local abaixo de modelos de API | Médio | Blocos menores, saída estruturada, comparação de modelos na Etapa 2; opção futura de `LLM_PROVIDER=anthropic` |
| Vídeos muito longos demoram | Baixo | Limite de duração; cache por `video_id`; fila processa em segundo plano |
| Resumo inventando informação | Médio | Prompt exige basear-se só na transcrição e citar timestamps; revisão manual nos vídeos de teste |
| Legendas automáticas com erros (nomes próprios, termos técnicos) | Baixo | Opção "forçar Whisper"; LLM corrige pontuação na tradução |
| Vídeos com música, ruído ou vários idiomas | Baixo | VAD do Whisper; documentar a limitação |

## Perguntas em aberto para o Igor

Respondido em 04/10/2026: **uso pessoal**, rodando **sem custo** na máquina própria (i7-11700, RTX 3080 **10 GB**, 32 GB) com **Windows** (o app roda no WSL2).

Os padrões abaixo já foram assumidos e podem ser mudados:

1. **Duração máxima dos vídeos?** (padrão: 3 horas)
2. **O PDF deve incluir a transcrição completa?** (padrão: opcional, desligado)
3. **Quer acessar pelo celular?** (padrão: não; Tailscale como opção na Etapa 7)
