# 01 · Visão geral

## Objetivo

Transformar um vídeo do YouTube em material de leitura: a transcrição completa, a versão em português (quando o vídeo estiver em outro idioma) e um PDF com o resumo e as principais ideias do conteúdo.

## Para quem

Pessoas que querem estudar ou revisar o conteúdo de vídeos longos (aulas, palestras, podcasts, entrevistas) sem assistir tudo de novo, inclusive vídeos em inglês ou outros idiomas.

## Fluxo do usuário

1. Cola o link do YouTube.
2. Escolhe as opções: traduzir para português (sim/não) e gerar PDF de resumo (sim/não).
3. Acompanha o progresso (baixando, transcrevendo, traduzindo, resumindo, gerando PDF).
4. Lê a transcrição na tela e baixa os arquivos: `.txt`, `.srt` e `.pdf`.

## Requisitos funcionais

| ID | Requisito | Prioridade |
|---|---|---|
| RF01 | Aceitar URLs do YouTube nos formatos `youtube.com/watch?v=`, `youtu.be/`, `shorts/` e com parâmetros extras (`&t=`, `&list=`) | Must |
| RF02 | Validar a URL e mostrar título, canal, duração e miniatura antes de processar | Should |
| RF03 | Transcrever o vídeo inteiro, independentemente da duração (respeitando o limite configurado, ver RNF) | Must |
| RF04 | Usar a legenda oficial/automática do YouTube quando existir; caso contrário, transcrever o áudio com Whisper | Must |
| RF05 | Detectar o idioma original do vídeo | Must |
| RF06 | Manter marcações de tempo (timestamps) por trecho da transcrição | Should |
| RF07 | Traduzir a transcrição para português do Brasil quando o usuário pedir | Must |
| RF08 | Gerar resumo, principais ideias, conceitos citados e citações relevantes com timestamps | Must |
| RF09 | Gerar PDF com capa (título, canal, link, data), resumo, ideias principais e, opcionalmente, a transcrição completa em anexo | Must |
| RF10 | Permitir baixar a transcrição em `.txt` e `.srt` | Should |
| RF11 | Mostrar o progresso de cada etapa do processamento | Should |
| RF12 | Guardar histórico dos vídeos processados e reaproveitar resultados (cache por ID do vídeo) | Could |
| RF13 | Escolher o idioma do resumo/PDF (padrão: português) | Could |

## Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Vídeos de até 3 horas suportados na primeira versão (configurável em `MAX_VIDEO_MINUTES`) |
| RNF02 | Processamento assíncrono: a requisição web nunca espera a transcrição terminar |
| RNF03 | Falhas em uma etapa devem ser reexecutáveis sem refazer as anteriores (artefatos intermediários salvos) |
| RNF04 | Custo zero: tudo roda na máquina pessoal (GPU local), sem APIs pagas; tempo de cada etapa registrado no log |
| RNF05 | Configuração (modelos, limites) em variáveis de ambiente, nunca no código |
| RNF06 | Arquivos de áudio temporários apagados após a transcrição |
| RNF07 | Interface em português |

## Fora do escopo (por enquanto)

- Login, contas de usuário e cobrança (o app é de uso pessoal).
- Hospedagem na nuvem.
- Upload de arquivos de vídeo/áudio locais (pode entrar depois, o pipeline já suporta).
- Playlists inteiras e canais.
- Vídeos privados, com restrição de idade ou que exigem login.
- Identificação de quem está falando (diarização).
- App mobile nativo.
