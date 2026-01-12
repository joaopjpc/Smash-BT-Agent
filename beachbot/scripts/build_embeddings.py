"""Gera embeddings combinados dos arquivos .md em content/ usando OpenAI. (base de informação do CT)"""
from __future__ import annotations

import argparse
import pickle
import textwrap
from pathlib import Path
from typing import Iterable, Optional, Sequence

from dotenv import load_dotenv
from openai import OpenAI


ROOT = Path(__file__).resolve().parent.parent # Raiz do beachbot
CONTENT_DIR = ROOT / "content"                # Diretório de conteúdo
DEFAULT_OUT = CONTENT_DIR / "embeddings" / "ct_combined.pkl" # Saída padrão
DEFAULT_FILES: Sequence[str] = [
    "faq_aula_experimental.md",
    "faq_publico_niveis.md",
    "faq_planos_matricula.md",
    "faq_estrutura_servicos.md",
    "faq_regras_acesso.md",
    "faq_atendimento.md",
    "horarios.md",
    "servicos.md",
    "infos.md",
    "planos.md",
]


def iter_chunks(paths: Iterable[Path], width: int) -> list[dict]: 
    """Lê e quebra os arquivos em blocos com metadados minimalistas."""
    chunks: list[dict] = []
    for path in paths:
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        section = f"# {path.name}\n\n{text}".strip()
        for idx, para in enumerate(textwrap.wrap(section, width)):
            chunks.append(
                {
                    "chunk": {
                        "source": path.name,
                        "index": idx,
                        "content": para,
                    }
                }
            )
    return chunks # Retorna a lista de chunks que 


def build_embeddings(
    files: Sequence[str],
    out_path: Path,
    model: str,
    wrap_width: int,
    preview_out: Optional[Path] = None,
) -> None:
    """Gera embeddings e salva em pickle."""
    load_dotenv(ROOT.parent / ".env")
    client = OpenAI()

    paths = [CONTENT_DIR / name for name in files]
    chunks = iter_chunks(paths, wrap_width)

    if preview_out:
        preview_out.parent.mkdir(parents=True, exist_ok=True)
        preview_out.write_text(
            "\n\n".join(c["chunk"]["content"] for c in chunks),
            encoding="utf-8",
        )

    embeds: list[dict] = []
    for item in chunks:
        content = item["chunk"]["content"]
        resp = client.embeddings.create(model=model, input=content)
        embeds.append({**item, "embedding": resp.data[0].embedding})

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        pickle.dump(embeds, f)

    print(f"Salvo {len(embeds)} embeddings em {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera embeddings combinados dos markdowns em content/."
    )
    parser.add_argument( # Argumento para modelo de embedding
        "--model",
        default="text-embedding-3-large",
        help="Modelo de embedding (default: text-embedding-3-large)",
    )
    parser.add_argument( # Argumento para largura de quebra
        "--wrap-width",
        type=int,
        default=900,
        help="Tamanho maximo de cada chunk (caracteres).",
    )
    parser.add_argument( # Argumento para caminho de saída
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Caminho do pickle de saida (default: {DEFAULT_OUT})",
    )
    parser.add_argument( # Argumento para caminho de pré-visualização
        "--preview-out",
        type=Path,
        help="Salva o texto combinado antes do embedding (ex: content/embeddings/preview.md)",
    )
    parser.add_argument( # Argumento para lista de arquivos
        "--files",
        nargs="*",
        default=DEFAULT_FILES,
        help=f"Lista de arquivos em content/ (default: {', '.join(DEFAULT_FILES)})",
    )
    args = parser.parse_args()

    build_embeddings(
        files=args.files,
        out_path=args.out,
        model=args.model,
        wrap_width=args.wrap_width,
        preview_out=args.preview_out,
    )


if __name__ == "__main__":
    main()
