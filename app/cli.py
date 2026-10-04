"""Linha de comando do Transcriptor."""

import argparse
import sys

from app import __version__
from app.core.ambiente import verificar_tudo
from app.core.config import get_settings


def cmd_verificar() -> int:
    resultados = verificar_tudo(get_settings())
    for r in resultados:
        marca = "OK  " if r.ok else "FALHA"
        print(f"[{marca}] {r.nome}: {r.detalhe}")
    if all(r.ok for r in resultados):
        print("\nAmbiente pronto.")
        return 0
    print("\nCorrija os itens com FALHA antes de continuar.")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="transcriptor",
        description="Transcreve vídeos do YouTube, traduz e gera PDF com resumo.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("verificar", help="verifica GPU, ffmpeg, Ollama e pasta de dados")

    args = parser.parse_args(argv)
    if args.comando == "verificar":
        return cmd_verificar()
    return 2


if __name__ == "__main__":
    sys.exit(main())
