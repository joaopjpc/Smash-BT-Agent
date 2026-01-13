# 🤖 Smash Beach Tennis – AtendentePro (Multi-Agentes)

Assistente de atendimento para o CT Smash Beach Tennis, baseado no framework **AtendentePro**.

## 🧩 Arquitetura Multiagente
Triage (router) direciona a conversa para:
1.  **Flow Agent**: sugere tópicos possíveis e caminhos de atendimento.
2.  **Knowledge Agent**: responde dúvidas do CT usando RAG (embedding combinado dos docs `.md`).
3.  **Interview Agent**: coleta dados para aula experimental.
4.  **Escalation Agent**: chama humano pra registrar pedidos que exigem pagamento (ex.: aluguel de quadra/churrasqueira). Usa horário 11h–19h (env).


## 📂 Estrutura do Projeto
- `beachbot/main_cli.py`: loop de chat em terminal.
- `beachbot/network.py`: cria a rede de agentes (seta canais de escalonamento).
- `beachbot/config/*.yaml`: prompts/configs dos agentes (triage, flow, knowledge, interview, guardrails, style).
- `beachbot/knowledge/`: conteúdo em markdown; embeddings em `knowledge/embeddings/ct_combined.pkl`.
- `beachbot/scripts/build_embeddings.py`: gera embeddings combinando os `.md` (usa `text-embedding-3-large`).
- `beachbot/db.py`: Camada de persistência SQLite: aplica migrations no init_db.


## 🏃 Como Rodar
1. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
2. Gerar embeddings:
   ```
   python beachbot/scripts/build_embeddings.py --preview-out beachbot/knowledge/embeddings/ct_combined_preview.md
   ```
3. Criar o banco aplicando migrations:
   ```
   python -m db.migrate
   ```
4. Executar o chat:
   ```
   python -m beachbot.main_cli
   ```
5. Encerrar: digite `sair`.

## ⚙️ Configuração
- `.env` (na raiz): `ATENDENTEPRO_LICENSE_KEY`, `OPENAI_API_KEY`, `ESCALATION_HOUR_START=11`, `ESCALATION_HOUR_END=19`.
- Embeddings: `knowledge_config.yaml` usa RAG com embeddings de `beachbot/knowledge/embeddings/ct_combined.pkl`.


## Banco de Dados (Dev)
Este projeto utiliza SQLite para desenvolvimento local.
- O caminho do banco é definido em **um único ponto** (`beachbot/db.py`).
- O arquivo do banco **não é versionado** no repositório.
### Aplicar migrations
Cria o banco (se não existir) e aplica todas as migrations:
```bash
python -m db.migrate
