# Contexto para o Claude — Projeto MCP + BigQuery

## Quem é o usuário

- Nome: Gustavo Lettiere
- Trabalha numa empresa de CRM
- Está aprendendo na prática sobre MCP servers, DuckDB e engenharia de dados
- Prefere trabalhar passo a passo, aguardando confirmação antes de cada etapa

---

## O que foi construído (projeto concluído)

Repositório: https://github.com/gustavolettiere/mcp-olist

Um **MCP server em Python** que expõe um warehouse analítico local (DuckDB) para o Claude Desktop consultar dados do e-commerce Olist em linguagem natural.

**Arquivos:**
- `server.py` — MCP server com FastMCP 3.4.2
- `load_data.py` — carrega os 9 CSVs do Olist em `olist.duckdb`
- `README.md` — instruções completas de uso

**Primitivos implementados:**
- Tools: `list_tables`, `describe_table`, `run_query` (SELECT/WITH only, read_only=True)
- Resource: `schema://catalog`
- Prompt: `analisar_receita`

---

## Aprendizados e gotchas importantes (para não repetir erros)

1. **Caminho do banco sempre absoluto**: `DB_PATH = str(Path(__file__).parent / "olist.duckdb")`. Usar caminho relativo faz o Claude Desktop procurar o banco na sua própria pasta de instalação (`app-1.xxxxx`), não na pasta do projeto.

2. **FastMCP 3.x mudou a CLI**: o subcomando `fastmcp dev` e `fastmcp inspector` não existem mais. Usar `fastmcp inspect server.py` para verificar o server em texto.

3. **MCP Inspector via npx**: rodar `npx @modelcontextprotocol/inspector` sem argumentos e configurar na UI com caminhos absolutos:
   - Command: caminho absoluto para `.venv/Scripts/python.exe`
   - Arguments: `server.py`
   - O Inspector concatena caminhos errado no Windows se você passar o path completo no campo Arguments.

4. **Decoradores FastMCP 3.x**: usar `@mcp.tool()`, `@mcp.resource(...)` e `@mcp.prompt()` com parênteses.

5. **claude_desktop_config.json**: a chave é `mcpServers`, não `mcp_servers`. Após editar, fechar o Claude Desktop pelo system tray antes de reabrir.

6. **gh CLI no Windows**: instalar com `winget install --id GitHub.cli --accept-source-agreements --accept-package-agreements`. Após instalar, atualizar o PATH na sessão atual com:
   ```powershell
   $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
   ```

---

## Próximo projeto planejado

**MCP server para BigQuery** — análise de tabelas raw antes do refinamento para a camada silver.

**Contexto de negócio:**
- Gustavo trabalha numa empresa de CRM
- Precisa analisar tabelas raw no BigQuery para entender estrutura e qualidade antes de modelar para a camada silver
- Quer perguntar em linguagem natural: "quais campos têm mais nulos?", "qual a granularidade dessa tabela?", etc.

**Diferenças em relação ao projeto Olist:**
- Trocar `duckdb` por `google-cloud-bigquery`
- Autenticação via service account ou Application Default Credentials (ADC)
- Atenção ao custo: BigQuery cobra por bytes processados — implementar `LIMIT` forçado e considerar `dry_run` antes de executar

**Stack prevista:**
- Python + FastMCP (mesmo do projeto anterior)
- `google-cloud-bigquery` como cliente
- Autenticação GCP a definir com o usuário

---

## Preferências de trabalho do Gustavo

- Trabalha passo a passo — sempre perguntar antes de executar cada etapa
- Prefere entender o que está sendo feito antes de aplicar
- Usa Windows 11, VS Code, terminal integrado do VS Code
- Python 3.13, Node.js 24 instalados
