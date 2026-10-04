"""Verifica se a máquina tem tudo o que o Transcriptor precisa para rodar."""

import shutil
import subprocess
import sys
from dataclasses import dataclass

import httpx

from app.core.config import Settings


@dataclass(frozen=True)
class Verificacao:
    nome: str
    ok: bool
    detalhe: str


def verificar_python() -> Verificacao:
    versao = ".".join(str(n) for n in sys.version_info[:3])
    ok = sys.version_info >= (3, 11)
    return Verificacao("Python 3.11+", ok, versao if ok else f"{versao} (atualize o Python)")


def verificar_ffmpeg() -> Verificacao:
    caminho = shutil.which("ffmpeg")
    if caminho is None:
        return Verificacao("ffmpeg", False, "não encontrado (sudo apt install ffmpeg)")
    return Verificacao("ffmpeg", True, caminho)


def verificar_gpu(settings: Settings) -> Verificacao:
    if settings.whisper_device == "cpu":
        return Verificacao("GPU NVIDIA", True, "ignorada (WHISPER_DEVICE=cpu)")
    if shutil.which("nvidia-smi") is None:
        return Verificacao("GPU NVIDIA", False, "nvidia-smi não encontrado (driver NVIDIA/WSL2)")
    resultado = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
        capture_output=True,
        text=True,
        check=False,
    )
    if resultado.returncode != 0 or not resultado.stdout.strip():
        return Verificacao("GPU NVIDIA", False, "nvidia-smi falhou: " + resultado.stderr.strip())
    return Verificacao("GPU NVIDIA", True, resultado.stdout.strip().splitlines()[0])


def verificar_ollama(settings: Settings, client: httpx.Client | None = None) -> Verificacao:
    if settings.llm_provider != "ollama":
        return Verificacao("Ollama", True, f"ignorado (LLM_PROVIDER={settings.llm_provider})")
    client = client or httpx.Client(timeout=5)
    try:
        resposta = client.get(f"{settings.ollama_url}/api/tags")
        resposta.raise_for_status()
    except httpx.HTTPError:
        return Verificacao(
            "Ollama", False, f"não respondeu em {settings.ollama_url} (abra o Ollama)"
        )
    modelos = {m["name"] for m in resposta.json().get("models", [])}
    alvo = settings.llm_model
    if alvo in modelos or f"{alvo}:latest" in modelos:
        return Verificacao("Ollama", True, f"modelo {alvo} disponível")
    return Verificacao("Ollama", False, f"modelo {alvo} não baixado (ollama pull {alvo})")


def verificar_storage(settings: Settings) -> Verificacao:
    try:
        settings.storage_dir.mkdir(parents=True, exist_ok=True)
        teste = settings.storage_dir / ".teste_escrita"
        teste.write_text("ok")
        teste.unlink()
    except OSError as erro:
        return Verificacao("Pasta de dados", False, f"{settings.storage_dir}: {erro}")
    return Verificacao("Pasta de dados", True, str(settings.storage_dir.resolve()))


def verificar_tudo(settings: Settings) -> list[Verificacao]:
    return [
        verificar_python(),
        verificar_ffmpeg(),
        verificar_gpu(settings),
        verificar_ollama(settings),
        verificar_storage(settings),
    ]
