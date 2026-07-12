# PROJECT_STATE.md

# GER — Geometria Espectral Relacional

**Status:** 🟢 Desenvolvimento Ativo

**Framework:** v1.0 (Validado)

**Fase Científica Atual:** S26-B2 — Caracterização Espectral

**Autor Principal:** Eduardo Batista de Freitas

---

# Estrutura do Projeto

```
GER/
│
├── GER/
│   └── CORE/          → Núcleo permanente do framework
│
├── GER_CORE/          → Experimentos (compatibilidade; futura pasta EXPERIMENTS)
│
├── TESTS/             → Testes persistentes
├── DOCS/              → Documentação técnica
├── RESULTS/           → Resultados, figuras e tabelas
│
├── README.md
├── PROJECT_STATE.md
├── CHANGELOG.md
└── start_ger.py
```

---

# Componentes Implementados

### Framework (GER/CORE)

- ✔ Motor temporal (`ger_engine`)
- ✔ Métricas globais (`ger_metrics`)
- ✔ Análise modal (`ger_modal`)
- ✔ Potenciais (`ger_potential`)
- ✔ Snapshots (`ger_snapshot`)
- ✔ Convergência (`ger_convergence`)
- ✔ Reversibilidade (`ger_reversibility`)
- ✔ Validação (`ger_validation`)
- ✔ Bootstrap oficial

---

### Série Experimental S26

- ✔ S26-B21 — Transferência Modal
- ✔ S26-B22 — Taxa de Mistura
- ✔ S26-B23 — Dependência com β
- ✔ S26-B24 — Robustez temporal
- ✔ S26-B25 — Refinamento crítico
- ✔ S26-B26 — Transition Scan
- ✔ S26-B28 — Crossover Mapping
- ✔ S26-B29 — Escalamento Assintótico
- ✔ S26-B31 a B34 — Robustez espectral
- ✔ S26-B35 — Métricas de Persistência
- ✔ S26-B36 — Classificador e Auditoria

---

# Estado Científico

## Concluído

- ✔ Validação do motor linear
- ✔ Conservação dos invariantes
- ✔ Validação do regime não linear
- ✔ Preservação espectral
- ✔ Robustez do classificador

---

## Em desenvolvimento

- Finalização da infraestrutura do projeto
- Ambiente oficial de inicialização (start_ger)
- Auditoria completa da Fase B2

---

# Próximo Marco Científico

Concluir a infraestrutura do framework e retomar a Série S26-B2 para finalizar a caracterização espectral antes do início da investigação de estados estacionários (Fase B3).

---

# Princípios do Projeto

- O núcleo (`GER/CORE`) permanece independente dos experimentos.
- Os experimentos nunca modificam o núcleo.
- Todo novo formalismo deve passar por auditoria antes da implementação.
- O Google Colab é utilizado apenas como ambiente de execução e validação.
- O GitHub é a fonte oficial do código do projeto.
