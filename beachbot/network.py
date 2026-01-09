"""Configuracao de rede para o AtendentePro."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from atendentepro.network import create_standard_network


def build_network() -> Any:
    """Cria a rede do AtendentePro usando templates locais."""
    return create_standard_network(
        templates_root=Path(__file__).parent,
        client="escolinha_beach",
        include_knowledge=False,
    )


def run_turn(network: Any, message: str) -> str:
    """Envia uma mensagem do usuario pela rede e retorna a resposta em texto."""
    if hasattr(network, "run"):
        result = network.run(message)
    elif hasattr(network, "handle_message"):
        result = network.handle_message(message)
    else:
        raise AttributeError("Network object does not expose a run method.")

    if isinstance(result, str):
        return result
    if hasattr(result, "text"):
        return result.text
    return str(result)
