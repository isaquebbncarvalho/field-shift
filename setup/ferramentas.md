# Ferramentas para agentes de código

Instale no notebook ANTES de começar a construir e rode um teste curto. Trocar de ferramenta no meio do hackathon custa mais do que ganha.

## Pré-requisitos

- Python 3.10+ e Git.
- Node.js 18+ (para `npx skills add`).
- Claude Code instalado e logado (`claude` no terminal).

## MCPs de dados (já configurados)

O arquivo `.mcp.json` na raiz já registra os dois. Ao abrir o Claude Code na pasta do projeto, aprove quando ele perguntar.

| Servidor | Para que serve | Login |
|---|---|---|
| `spacedata` (Space Data Atlas) | Mapeia cada desafio do Space Apps 2026 aos datasets e traz código inicial. Projeto independente, não oficial da NASA. | Não |
| `earthdata` (NASA, oficial) | Busca no catálogo de dados da NASA (CMR) | Não |

Se preferir adicionar na mão:

```bash
claude mcp add --transport http spacedata https://spacedata.swapniltamse.com/mcp
claude mcp add --transport http earthdata https://cmr.earthdata.nasa.gov/mcp/v1
```

## Plugins (rodar dentro do Claude Code)

```text
/plugin install superpowers@claude-plugins-official
/plugin marketplace add upstash/context7
/plugin install context7@context7-marketplace
```

- **Superpowers**: força o agente a planejar e quebrar em tarefas antes de codar, e a revisar no fim.
- **Context7**: documentação atual das bibliotecas (pandas, Streamlit, Plotly) na hora de codar.

## Skills (rodar no terminal)

```bash
npx skills add pbakaus/impeccable
npx skills add anthropics/skills --skill webapp-testing
```

- **Impeccable**: regras anti "cara de IA" na interface e comandos de crítica (`/impeccable critique`, `/impeccable audit`). Use no bloco de acabamento visual de domingo.
- **webapp-testing**: o agente abre o app num navegador e testa o que construiu.

## O que NÃO instalar agora

Skills de Next.js, Vercel ou Supabase: a stack do protótipo é Python + Streamlit. Skills de estilo pronto (bancos de templates) puxam o visual de volta para o genérico.

## Ordem de uso sugerida

1. Abrir o Claude Code na raiz do repositório (ele lê `CLAUDE.md` sozinho).
2. Pedir mudanças pequenas, uma por vez, com teste.
3. Antes de cada commit: `python -m pytest -q`.
