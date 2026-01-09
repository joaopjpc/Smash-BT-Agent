"""Ponto de entrada CLI do bot Smash Beach Tennis.

Execute com: python -m beachbot.main_cli
"""
from __future__ import annotations

from pathlib import Path

from beachbot import db
from beachbot.network import build_network, run_turn


DATA_PATH = Path(__file__).with_name("data.sqlite")


def main() -> None:
    """Executa um loop simples de chat no terminal."""
    connection = db.init_db(DATA_PATH)
    network = build_network()

    print("Smash Beach Tennis - Atendimento (digite 'sair' para encerrar)\n")

    while True:
        user_message = input("Você: ").strip()
        if not user_message:
            continue
        if user_message.lower() in {"sair", "exit", "quit"}:
            print("Até logo! 👋")
            break

        db.log_message(connection, role="user", content=user_message)

        response = run_turn(network, user_message)
        print(f"Bot: {response}")
        db.log_message(connection, role="assistant", content=response)


if __name__ == "__main__":
    main()
