"""Network setup for AtendentePro."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from atendentepro.network import create_standard_network


def build_network() -> Any:
    """Create the AtendentePro network using local templates."""
    config_dir = Path(__file__).parent / "escolinha_beach"
    return create_standard_network(str(config_dir))


def run_turn(network: Any, message: str) -> str:
    """Send a user message through the network and return the text reply."""
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
