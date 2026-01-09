import sys
import asyncio
from pathlib import Path
from atendentepro import activate, create_standard_network
from agents import Runner
from atendentepro import activate
from dotenv import load_dotenv
load_dotenv()

activate("ATP_eyJvcmciOiJMdWNhcyIsImV4cCI6bnVsbCwiZmVhdCI6WyJmdWxsIl0sInYiOjF9.408a9003de63c1f6")


async def test_triage(client_path: str):
    print(f"\n🔍 Testando Triage com config: {client_path}")
    network = create_standard_network(
        templates_root=Path("."), client=client_path,
        include_escalation=True, include_feedback=False
    )

    messages = [{"role": "user", "content": "quero falar com atendente"}]
    result = await Runner.run(network.triage, messages)
    print("Resposta:", result.final_output)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python test.py [test_dict | test_lista]")
    else:
        asyncio.run(test_triage(sys.argv[1]))
