from pathlib import Path

import httpx
import pytest

from app.core import ambiente
from app.core.config import Settings


def _client(handler: httpx.MockTransport) -> httpx.Client:
    return httpx.Client(transport=handler)


def test_ollama_com_modelo_disponivel() -> None:
    transport = httpx.MockTransport(
        lambda req: httpx.Response(200, json={"models": [{"name": "qwen3:8b"}]})
    )
    r = ambiente.verificar_ollama(Settings(llm_model="qwen3:8b"), _client(transport))
    assert r.ok


def test_ollama_sem_modelo() -> None:
    transport = httpx.MockTransport(lambda req: httpx.Response(200, json={"models": []}))
    r = ambiente.verificar_ollama(Settings(llm_model="qwen3:8b"), _client(transport))
    assert not r.ok
    assert "ollama pull qwen3:8b" in r.detalhe


def test_ollama_fora_do_ar() -> None:
    def falha(req: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("recusado")

    r = ambiente.verificar_ollama(Settings(), _client(httpx.MockTransport(falha)))
    assert not r.ok


def test_ollama_ignorado_com_outro_provedor() -> None:
    assert ambiente.verificar_ollama(Settings(llm_provider="anthropic")).ok


def test_gpu_ignorada_em_cpu() -> None:
    assert ambiente.verificar_gpu(Settings(whisper_device="cpu")).ok


def test_gpu_sem_nvidia_smi(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ambiente.shutil, "which", lambda _: None)
    assert not ambiente.verificar_gpu(Settings(whisper_device="cuda")).ok


def test_storage_gravavel(tmp_path: Path) -> None:
    assert ambiente.verificar_storage(Settings(storage_dir=tmp_path / "data")).ok


def test_config_le_variaveis_de_ambiente(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_MODEL", "gemma3:12b")
    monkeypatch.setenv("MAX_VIDEO_MINUTES", "60")
    s = Settings()
    assert s.llm_model == "gemma3:12b"
    assert s.max_video_minutes == 60
