"""Persistencia SQLite para conversas, aulas experimentais e tickets de atendimento humano."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA = (
    "CREATE TABLE IF NOT EXISTS conversas ("
    "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "  role TEXT NOT NULL,"
    "  content TEXT NOT NULL,"
    "  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ");",
    "CREATE TABLE IF NOT EXISTS aulas_experimentais ("
    "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "  nome TEXT NOT NULL,"
    "  telefone TEXT NOT NULL,"
    "  horario_escolhido TEXT NOT NULL,"
    "  nivel_aluno TEXT NOT NULL,"
    "  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ");",
    "CREATE TABLE IF NOT EXISTS atendimento_humano ("
    "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "  topico TEXT NOT NULL,"
    "  detalhes TEXT NOT NULL,"
    "  status TEXT NOT NULL DEFAULT 'open',"
    "  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ");",
)


def init_db(path: Path) -> sqlite3.Connection:
    """Cria o arquivo do banco SQLite e as tabelas necessarias."""
    connection = sqlite3.connect(path)
    for statement in SCHEMA:
        connection.execute(statement)
    connection.commit()
    return connection


def log_message(connection: sqlite3.Connection, role: str, content: str) -> None:
    """Armazena uma mensagem no historico da conversa."""
    connection.execute(
        "INSERT INTO conversas (role, content) VALUES (?, ?)",
        (role, content),
    )
    connection.commit()


def record_trial_request(
    connection: sqlite3.Connection,
    nome: str,
    telefone: str,
    horario_escolhido: str,
    nivel_aluno: str | None = None,
) -> None:
    """Persiste um pedido de aula experimental."""
    connection.execute(
        "INSERT INTO aulas_experimentais (nome, telefone, horario_escolhido, nivel_aluno) VALUES (?, ?, ?, ?)",
        (nome, telefone, horario_escolhido, nivel_aluno),
    )
    connection.commit()


def create_handoff_ticket(
    connection: sqlite3.Connection,
    topico: str,
    detalhes: str,
) -> None:
    """Abre um ticket para atendimento humano."""
    connection.execute(
        "INSERT INTO atendimento_humano (topico, detalhes) VALUES (?, ?)",
        (topico, detalhes),
    )
    connection.commit()
