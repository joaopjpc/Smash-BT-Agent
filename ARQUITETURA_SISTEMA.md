# 🏗️ Arquitetura Atual do Sistema – Atendente Smash BT

## 📊 Diagrama de Fluxo de Agentes

```

┌─────────────────────────────────────────────────────────────────┐
│ USUÁRIO                                                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ TRIAGE AGENT                                                    │
│ • Entrada                                                       │
│ • Roteamento                                                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ FLOW AGENT  │ │  KNOWLEDGE  │ │  ESCALATION │
│             │ │     AGENT   │ │     AGENT   │
│ • Opções    │ │• Arquivos.md│ │   • Humano  │
│ • Direção   │ │             │ │             │
└─────┬───────┘ └─────┬───────┘ └─────────────┘
      │               │
      ▼               ▼
┌─────────────┐ ┌─────────────┐
│ INTERVIEW   │ │    ANSWER   │
│ AGENT       │ │ AGENT       │
│             │ │             │
│ • Coleta    │ │ • Síntese   │
│ dados agend.│ │   final     │
│ • Cria      │ │ • Resposta  │
│ estado      │ │             │
└─────┬───────┘ └─────────────┘
      │
      ▼
┌─────────────┐
│ ANSWER      │
│ AGENT       │
│             │
│ • Mensagem  │
│ final       │
└─────────────┘

```

